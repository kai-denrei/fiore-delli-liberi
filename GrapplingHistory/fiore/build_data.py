"""
Build data.json for the Fiore reader page.
Combines cleaned OCR files + Wiktenauer translations into a single JSON.
"""

import json
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
CLEANED_DIR = PROJECT / "data" / "cleaned"
WIKI_JSON = PROJECT / "data" / "wiktenauer_translations.json"
PD_ITALIAN_JSON = PROJECT / "data" / "pd_italian_extracted.json"
OUTPUT = Path(__file__).resolve().parent / "data.json"

# Section assignments by folio range (Getty MS order)
SECTION_MAP = [
    ("01r", "04v", "Preface"),
    ("05r", "05v", "Preface"),
    ("06r", "08r", "Grappling"),
    ("08v", "08v", "Grappling / Dagger"),
    ("09r", "18v", "Dagger"),
    ("19r", "19v", "Sword & Dagger"),
    ("20r", "21v", "Sword in One Hand"),
    ("22r", "22r", "Baton"),
    ("22v", "24v", "Sword Guards"),
    ("25r", "31v", "Sword in Two Hands"),
    ("32r", "32r", "Seven Swords"),
    ("32v", "34v", "Sword in Armor"),
    ("35r", "37v", "Poleaxe"),
    ("38r", "38v", "Dagger (misbound)"),
    ("39r", "40r", "Spear"),
    ("41r", "47r", "Mounted Combat"),
]


def folio_sort_key(fol_id):
    m = re.match(r'(\d+)([rv])', fol_id)
    if m:
        return (int(m.group(1)), 0 if m.group(2) == 'r' else 1)
    return (999, 0)


def get_section(fol_id):
    fol_num = folio_sort_key(fol_id)
    for start, end, section in SECTION_MAP:
        if folio_sort_key(start) <= fol_num <= folio_sort_key(end):
            return section
    return ""


def parse_cleaned_file(path):
    content = path.read_text()
    sections = {"transcription": "", "translation": "", "notes": ""}
    current = None
    for line in content.split("\n"):
        if line.startswith("## Transcription"):
            current = "transcription"
            continue
        elif line.startswith("## Translation"):
            current = "translation"
            continue
        elif line.startswith("## Notes"):
            current = "notes"
            continue
        elif line.startswith("# "):
            continue
        if current:
            sections[current] += line + "\n"
    for k in sections:
        sections[k] = sections[k].strip()

    is_blank = ("blank" in content.lower()[:300] and len(content) < 600)
    return sections, is_blank


def main():
    # Load Wiktenauer
    wiki_data = json.loads(WIKI_JSON.read_text())
    wiki_by_folio = {}
    for p in wiki_data["passages"]:
        fol = p["folio"]
        if fol not in wiki_by_folio:
            wiki_by_folio[fol] = {"hatcher": [], "chidester": [], "pisani_dossi": [], "section": p.get("section", "")}
        if p.get("hatcher_en"):
            wiki_by_folio[fol]["hatcher"].append(p["hatcher_en"])
        if p.get("chidester_en"):
            wiki_by_folio[fol]["chidester"].append(p["chidester_en"])
        if p.get("pisani_dossi_hatcher"):
            wiki_by_folio[fol]["pisani_dossi"].append(p["pisani_dossi_hatcher"])

    # Load PD Italian
    pd_italian = {}
    if PD_ITALIAN_JSON.exists():
        pd_data = json.loads(PD_ITALIAN_JSON.read_text())
        for getty_fol, passages in pd_data.get("by_getty_folio", {}).items():
            pd_italian[getty_fol] = [p["text"] for p in passages if p.get("text")]

    # Load cleaned files
    cleaned_files = sorted(CLEANED_DIR.glob("fol_*.md"), key=lambda f: folio_sort_key(f.stem.replace("fol_", "")))

    folios = []
    sections_index = {}

    for f in cleaned_files:
        fol_id = f.stem.replace("fol_", "")
        parsed, is_blank = parse_cleaned_file(f)
        section = get_section(fol_id)
        wiki = wiki_by_folio.get(fol_id, {})

        entry = {
            "id": fol_id,
            "section": section,
            "blank": is_blank,
        }

        if not is_blank:
            entry["transcription"] = parsed["transcription"]
            entry["claude_translation"] = parsed["translation"]
            entry["notes"] = parsed["notes"]
            if wiki.get("hatcher"):
                entry["hatcher"] = wiki["hatcher"]
            if wiki.get("chidester"):
                entry["chidester"] = wiki["chidester"]
            if wiki.get("pisani_dossi"):
                entry["pisani_dossi"] = wiki["pisani_dossi"]
            if pd_italian.get(fol_id):
                entry["pd_italian"] = pd_italian[fol_id]

        folios.append(entry)

        if section:
            if section not in sections_index:
                sections_index[section] = []
            sections_index[section].append(fol_id)

    # Build PD folio list
    pd_data = json.loads(PD_ITALIAN_JSON.read_text()) if PD_ITALIAN_JSON.exists() else {}
    pd_map = pd_data.get("pd_to_getty_map", {})
    pd_folios_raw = sorted(
        set(pd_map.keys()),
        key=lambda f: (int(re.search(r'(\d+)', f).group(1)), 0 if f.endswith('a') else 1)
    )
    pd_folios = []
    for pf in pd_folios_raw:
        getty_equiv = pd_map.get(pf)
        texts = []
        # Find PD Italian text for this folio
        if getty_equiv and getty_equiv in pd_italian:
            # Filter to passages from this specific PD folio
            for entry in pd_data.get("by_getty_folio", {}).get(getty_equiv, []):
                if entry.get("pd_folio") == pf:
                    texts.append(entry["text"])
        # Find PD Hatcher translation
        hatcher = []
        for p in wiki_data.get("passages", []):
            if p.get("folio") == getty_equiv and p.get("pisani_dossi_hatcher"):
                hatcher.append(p["pisani_dossi_hatcher"])

        pd_folios.append({
            "id": pf,
            "getty_equiv": getty_equiv,
            "italian": texts,
            "hatcher": hatcher,
        })

    output = {
        "title": "Fior di Battaglia — MS Ludwig XV 13",
        "author": "Fiore dei Liberi",
        "date": "c. 1410",
        "folios": folios,
        "sections": sections_index,
        "pd_folios": pd_folios,
        "stats": {
            "total_folios": len(folios),
            "blank": sum(1 for f in folios if f.get("blank")),
            "with_hatcher": sum(1 for f in folios if f.get("hatcher")),
            "with_chidester": sum(1 for f in folios if f.get("chidester")),
            "pd_folios": len(pd_folios),
        },
        "getty_to_pd": {g: pds for g, pds in sorted({
            f["getty_equiv"]: [] for f in pd_folios if f.get("getty_equiv")
        }.items())},
    }
    # Build getty_to_pd properly
    g2pd = {}
    for f in pd_folios:
        if f.get("getty_equiv"):
            g2pd.setdefault(f["getty_equiv"], []).append(f["id"])
    output["getty_to_pd"] = g2pd

    OUTPUT.write_text(json.dumps(output, ensure_ascii=False))
    print(f"Written: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size / 1024:.0f} KB")
    print(f"Folios: {len(folios)} ({sum(1 for f in folios if f.get('blank'))} blank)")
    print(f"With Hatcher: {output['stats']['with_hatcher']}")
    print(f"With Chidester: {output['stats']['with_chidester']}")
    print(f"Sections: {list(sections_index.keys())}")


if __name__ == "__main__":
    main()
