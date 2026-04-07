"""
Merge our Claude vision OCR translations with Wiktenauer's Hatcher/Chidester
translations into a single comparison document.

Output: data/fiore_comparison.md — per-folio with all available translations side by side.
"""

import json
import re
from pathlib import Path

CLEANED_DIR = Path(__file__).resolve().parents[2] / "data" / "cleaned"
WIKI_JSON = Path(__file__).resolve().parents[2] / "data" / "wiktenauer_translations.json"
OUTPUT = Path(__file__).resolve().parents[2] / "data" / "fiore_comparison.md"


def load_claude_translations():
    """Load our OCR translations, keyed by folio."""
    translations = {}
    for f in sorted(CLEANED_DIR.glob("fol_*.md")):
        folio = f.stem.replace("fol_", "")
        content = f.read_text()

        # Extract transcription section
        transcription = ""
        translation = ""
        notes = ""
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

            if current == "transcription":
                transcription += line + "\n"
            elif current == "translation":
                translation += line + "\n"
            elif current == "notes":
                notes += line + "\n"

        translations[folio] = {
            "transcription": transcription.strip(),
            "translation": translation.strip(),
            "notes": notes.strip(),
            "is_blank": "blank" in content.lower()[:300] and len(content) < 600,
        }
    return translations


def load_wiktenauer():
    """Load Wiktenauer translations, grouped by folio."""
    data = json.loads(WIKI_JSON.read_text())
    by_folio = {}
    for p in data["passages"]:
        fol = p["folio"]
        # Normalize: "01r" -> "01r"
        if fol not in by_folio:
            by_folio[fol] = {"hatcher": [], "chidester": [], "section": p.get("section", "")}
        if p.get("hatcher_en"):
            by_folio[fol]["hatcher"].append(p["hatcher_en"])
        if p.get("chidester_en"):
            by_folio[fol]["chidester"].append(p["chidester_en"])
    return by_folio


def main():
    claude = load_claude_translations()
    wiki = load_wiktenauer()

    print(f"Claude translations: {len(claude)} folios")
    print(f"Wiktenauer translations: {len(wiki)} folios")

    # Build all folio IDs in order
    all_folio_ids = set(list(claude.keys()) + list(wiki.keys()))
    # Filter out non-standard folio IDs (e.g. 'pd_preface')
    all_folio_ids = {f for f in all_folio_ids if re.match(r'^\d+[rv]$', f)}
    all_folios = sorted(
        all_folio_ids,
        key=lambda f: (int(re.search(r'(\d+)', f).group(1)), 0 if f.endswith('r') else 1)
    )

    out = []
    out.append("# Fior di Battaglia — Translation Comparison")
    out.append("")
    out.append("Three translation sources aligned by folio:")
    out.append("- **Claude Vision OCR** (2026-04-07) — first-pass from manuscript images")
    out.append("- **Colin Hatcher** (via Wiktenauer) — scholarly translation from Getty MS")
    out.append("- **Michael Chidester** (via Wiktenauer) — scholarly translation from Morgan MS")
    out.append("")
    out.append("---")
    out.append("")

    # Stats
    has_all_three = 0
    has_claude_only = 0
    has_wiki_only = 0
    blank_count = 0

    for fol in all_folios:
        c = claude.get(fol, {})
        w = wiki.get(fol, {})

        if c.get("is_blank"):
            blank_count += 1
            continue

        has_c = bool(c.get("translation"))
        has_h = bool(w.get("hatcher"))
        has_ch = bool(w.get("chidester"))

        if has_c and has_h:
            has_all_three += 1
        elif has_c and not has_h:
            has_claude_only += 1
        elif has_h and not has_c:
            has_wiki_only += 1

        out.append(f"## Folio {fol}")
        if w.get("section"):
            out.append(f"**Section:** {w['section']}")
        out.append("")

        # Claude transcription (Italian)
        if c.get("transcription"):
            out.append("### Original Text (Claude OCR)")
            out.append("")
            out.append(c["transcription"])
            out.append("")

        # Claude translation
        if c.get("translation"):
            out.append("### Translation — Claude Vision")
            out.append("")
            out.append(c["translation"])
            out.append("")

        # Hatcher
        if w.get("hatcher"):
            out.append("### Translation — Colin Hatcher (Getty)")
            out.append("")
            for block in w["hatcher"]:
                out.append(block)
                out.append("")

        # Chidester
        if w.get("chidester"):
            out.append("### Translation — Michael Chidester (Morgan)")
            out.append("")
            for block in w["chidester"]:
                out.append(block)
                out.append("")

        # Notes
        if c.get("notes"):
            out.append("### Notes")
            out.append("")
            out.append(c["notes"])
            out.append("")

        out.append("---")
        out.append("")

    # Summary at top
    summary = [
        f"**Coverage:** {len(all_folios)} folios total, {blank_count} blank",
        f"- All three sources: {has_all_three} folios",
        f"- Claude only (no Wiktenauer): {has_claude_only} folios",
        f"- Wiktenauer only (no Claude): {has_wiki_only} folios",
        "",
    ]
    # Insert after the --- line
    idx = out.index("---") + 2
    for i, line in enumerate(summary):
        out.insert(idx + i, line)

    combined = "\n".join(out)
    OUTPUT.write_text(combined)
    print(f"\nWritten: {OUTPUT}")
    print(f"Size: {len(combined) / 1024:.0f} KB")
    print(f"Folios with all three: {has_all_three}")
    print(f"Claude only: {has_claude_only}")
    print(f"Wiktenauer only: {has_wiki_only}")
    print(f"Blank: {blank_count}")


if __name__ == "__main__":
    main()
