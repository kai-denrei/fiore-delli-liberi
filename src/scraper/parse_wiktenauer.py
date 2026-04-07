"""
Parse Wiktenauer wikitext to extract the two English translations
(Hatcher from Getty, Chidester from Morgan) aligned with folio references.

Also captures Pisani Dossi translations (Chidester) from the preface sections
that use a different table layout.

The Getty Italian text is transcluded ({{section|...}}) and not inline,
so we extract folio refs and inline English text only.
"""

import re
import json
from pathlib import Path

WIKITEXT = Path(__file__).resolve().parents[2] / "data" / "raw" / "wiktenauer" / "fiore_dei_liberi_raw.wikitext"
OUTPUT = Path(__file__).resolve().parents[2] / "data" / "wiktenauer_translations.json"


def strip_wiki_markup(text):
    """Remove MediaWiki markup, keeping readable text."""
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref[^/]*/>', '', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</?p>', '\n', text)
    text = re.sub(r'</?em>', '*', text)
    text = re.sub(r'</?[a-zA-Z][^>]*>', '', text)
    text = re.sub(r'\[\[[^|\]]*\|([^\]]*)\]\]', r'\1', text)
    text = re.sub(r'\[\[([^\]]*)\]\]', r'\1', text)
    text = re.sub(r'\{\{rating\|[^}]*\}\}', '', text)
    text = re.sub(r'\{\{edit index\|[^}]*\}\}', '', text)
    text = re.sub(r'\{\{plainlist[^}]*\}\}', '', text)
    text = re.sub(r'\{\{red\|[^|]*\|([^}]*)\}\}', r'\1', text)  # {{red|b=1|text}} -> text
    text = re.sub(r'\{\{dec\|[^|]*\|([^}]*)\}\}', r'\1', text)  # {{dec|u|seven}} -> seven
    text = re.sub(r'\{\{[^}]*\}\}', '', text)
    text = re.sub(r'\}\}', '', text)  # Clean up any stray closing braces
    text = re.sub(r'^\s*Other Prologue\s*', '', text, flags=re.MULTILINE)  # Remove header text
    text = re.sub(r"'{2,5}", '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def find_getty_refs(text):
    """Find Getty folio refs in a row, handling both URL formats.

    Format 1 (main body): Page:MS Ludwig XV 13 01r.jpg
    Format 2 (preface):   Page:Getty Ms. Ludwig XV 13 01v - Fiore dei Liberi...jpg
    Also matches File: references for illustrations.
    """
    refs = []

    # Format 1: MS Ludwig XV 13 01r.jpg|section_ref
    for m in re.finditer(r'Page:MS Ludwig XV 13 (\d+[rv])\.jpg\|([^}|]+)', text):
        refs.append((m.group(1), m.group(2).strip()))

    # Format 2: Getty Ms. Ludwig XV 13 01v - Fiore dei Liberi - ...jpg|section_ref
    for m in re.finditer(r'Page:Getty Ms\. Ludwig XV 13 (\d+[rv]) - [^|]+\|([^}|]+)', text):
        folio = m.group(1)
        # Normalize folio to zero-padded 2-digit format (e.g. "2r" -> "02r")
        folio = re.sub(r'^(\d)([rv])$', r'0\1\2', folio)
        refs.append((folio, m.group(2).strip()))

    # Also check File: refs for illustration images (e.g. [[File:MS Ludwig XV 13 01r.jpg|...]])
    if not refs:
        for m in re.finditer(r'(?:File|file):MS Ludwig XV 13 (\d+[rv])\.jpg', text):
            refs.append((m.group(1), 'img'))

    return refs


def find_pisani_dossi_refs(text):
    """Find Pisani Dossi folio refs in a row."""
    refs = []
    for m in re.finditer(r'Page:Pisani-Dossi MS (\d+[ab]?)\.jpg\|([^}|]+)', text):
        refs.append((m.group(1), m.group(2).strip()))
    return refs


def find_morgan_refs(text):
    """Find Morgan folio refs in a row."""
    refs = []
    for m in re.finditer(r'Page:MS M\.383 (\d+[rv])\.jpg\|([^}|]+)', text):
        folio = m.group(1)
        # Normalize to zero-padded 2-digit format
        folio = re.sub(r'^(\d)([rv])$', r'0\1\2', folio)
        refs.append((folio, m.group(2).strip()))
    return refs


def is_english_text(cleaned, min_words=3):
    """Check if cleaned text contains enough English words."""
    english_words = len(re.findall(
        r'\b(the|and|of|is|was|that|with|his|her|this|for|from|have|has|'
        r'will|can|are|you|my|your|who|which|but|not|all|one|into|its|or|'
        r'be|he|she|it|they|him|his|would|could|should|also|been|had|may|'
        r'make|made|like|then|when|here|there|how|now|just|so|than|if|no|'
        r'do|does|did|each|other|both|these|those|between|through|same|'
        r'over|such|after|before|above|below|against|during|without|'
        r'because|sword|master|scholar|player|guard|remedy|counter|'
        r'strike|thrust|cut|arm|hand|foot|step|opponent|combat|knight|'
        r'fight|first|said|being|art|men|man|any|many|were|their|them|'
        r'about|upon|more|some|most|what|whom|very|only|such|than|'
        r'fencing|play|book|know|wish|lord|dukes|princes|duke|prince)\b',
        cleaned.lower()))
    return english_words >= min_words


def extract_english_from_cells(cells):
    """Extract English text cells from a list of wikitext cells."""
    english_cells = []
    for cell in cells:
        # Skip cells that are primarily section template refs
        if '{{section|' in cell and len(re.sub(r'\{\{section\|[^}]*\}\}', '', cell).strip()) < 50:
            continue
        # Skip image cells
        if ('[[File:' in cell or '[[file:' in cell) and len(cell) < 200:
            continue
        # Skip header cells
        if cell.strip().startswith('!'):
            continue
        # Skip rowspan image cells
        if re.match(r'\s*rowspan\s*=', cell.strip()):
            continue

        cleaned = strip_wiki_markup(cell)
        if len(cleaned) > 30 and is_english_text(cleaned):
            english_cells.append(cleaned)

    return english_cells


def detect_preface_subsection(text):
    """Detect which preface subsection a row belongs to based on context."""
    if 'Other Prologue' in text:
        return 'other_prologue'
    return None


# PD carta -> approximate Getty folio mapping for preface content
_PD_TO_GETTY = {
    "01a": "01r",  # PD opening -> Getty opening
    "01b": "01r",
    "02a": "02r",  # PD grappling intro (7 things) -> Getty grappling intro (8 things)
    "02b": "04r",  # PD pedagogical system -> Getty pedagogical system
}


def _map_pd_to_getty(ref_labels):
    """Map Pisani Dossi folio refs to approximate Getty folio equivalents."""
    for ref in ref_labels:
        # Extract PD folio from ref like "pd.02a.2a.13"
        m = re.match(r'pd\.(\d+[ab])', ref)
        if m:
            pd_fol = m.group(1)
            if pd_fol in _PD_TO_GETTY:
                return _PD_TO_GETTY[pd_fol]
    return "02r"  # Default to 02r for unmapped PD preface content


def parse_preface_section(wikitext, section_start, section_end, subsection_title):
    """Parse a preface subsection with its specific column layout.

    First Italian Preface columns (8 cols):
      0: Illustrations
      1: Hatcher EN (Getty)
      2: Chidester EN (Morgan)
      3: San Daniele IT
      4: Morgan IT
      5: Getty IT
      6: Pisani Dossi IT
      7: Paris Latin

    Latin Preface columns (8 cols):
      0: Illustrations
      1: Chidester EN (from PD) - draft
      2: [Paris - empty]
      3: San Daniele IT
      4: Morgan IT
      5: Getty IT
      6: Pisani Dossi IT
      7: Paris Latin

    Second Italian Preface columns (8 cols):
      0: Illustrations
      1: Chidester EN (from PD)
      2: [Paris - empty]
      3: San Daniele IT
      4: Morgan IT
      5: Getty IT
      6: Pisani Dossi IT
      7: Paris Latin
    """
    entries = []
    section_text = wikitext[section_start:section_end]
    rows = re.split(r'\n\|-\s*\n', section_text)

    # Track ongoing rowspan state for column 0 (illustrations)
    # When rowspan="N" appears in col 0, subsequent rows have one fewer cell
    rowspan_remaining = 0

    for row in rows:
        # Skip header rows (start with ! or {|)
        stripped = row.strip()
        if stripped.startswith('!') or stripped.startswith('{|'):
            # Count header columns to confirm layout
            continue

        # Find folio references
        getty_refs = find_getty_refs(row)
        pd_refs = find_pisani_dossi_refs(row)
        morgan_refs = find_morgan_refs(row)

        # Determine the folio from available references
        folio = None
        ref_labels = []

        if getty_refs:
            folio = getty_refs[0][0]
            ref_labels = [f"{r[0]}.{r[1]}" for r in getty_refs]
        elif morgan_refs:
            folio = morgan_refs[0][0]
            ref_labels = [f"morgan.{r[0]}.{r[1]}" for r in morgan_refs]
        elif pd_refs:
            folio = None
            ref_labels = [f"pd.{r[0]}.{r[1]}" for r in pd_refs]

        # Split into cells by pipe at start of line
        cells = re.split(r'\n\|', row)
        # Remove the first element if it's just whitespace/empty (before the first |)
        if cells and not cells[0].strip():
            cells = cells[1:]

        # Determine column offset due to rowspan
        col_offset = 0
        if rowspan_remaining > 0:
            # The illustration column is carried over from a previous row
            col_offset = 1
            rowspan_remaining -= 1
        else:
            # Check if this row starts a new rowspan
            if cells:
                rowspan_m = re.search(r'rowspan\s*=\s*"?(\d+)"?', cells[0])
                if rowspan_m:
                    rowspan_remaining = int(rowspan_m.group(1)) - 1

        # Map cells to actual column indices
        # cell[i] corresponds to column (i + col_offset)
        def get_cell_text(col_idx):
            """Get cleaned text from a specific column index."""
            cell_i = col_idx - col_offset
            if 0 <= cell_i < len(cells):
                cell = cells[cell_i]
                # Strip leading whitespace after the pipe
                cell = re.sub(r'^\s*', '', cell, count=1)
                cleaned = strip_wiki_markup(cell)
                if len(cleaned) > 20:
                    return cleaned
            return None

        # For First Italian Preface: col 1 = Hatcher, col 2 = Chidester
        if subsection_title == "First Italian Preface":
            if not folio:
                continue

            hatcher_text = get_cell_text(1)
            chidester_text = get_cell_text(2)

            # Validate that these are English
            if hatcher_text and not is_english_text(hatcher_text, min_words=2):
                hatcher_text = None
            if chidester_text and not is_english_text(chidester_text, min_words=2):
                chidester_text = None

            if not hatcher_text and not chidester_text:
                continue

            entry = {
                "folio": folio,
                "section": "Preface",
                "getty_refs": ref_labels,
            }
            if hatcher_text:
                entry["hatcher_en"] = hatcher_text
            if chidester_text:
                entry["chidester_en"] = chidester_text
            entries.append(entry)

        # Latin Preface: col 1 = Chidester (PD draft)
        elif subsection_title == "Latin Preface":
            en_text = get_cell_text(1)
            if not en_text or not is_english_text(en_text, min_words=2):
                continue

            # Map PD preface to approximate Getty folio
            mapped_folio = folio if folio else _map_pd_to_getty(ref_labels)

            entry = {
                "folio": mapped_folio,
                "section": "Preface (Latin)",
                "getty_refs": ref_labels,
                "pisani_dossi_hatcher": en_text,
            }
            entries.append(entry)

        # Second Italian Preface / Other Prologue: col 1 = Chidester (PD)
        elif subsection_title == "Second Italian Preface":
            en_text = get_cell_text(1)
            if not en_text or not is_english_text(en_text, min_words=2):
                continue

            # Map PD preface to approximate Getty folio
            mapped_folio = folio if folio else _map_pd_to_getty(ref_labels)

            entry = {
                "folio": mapped_folio,
                "section": "Preface (Other Prologue)",
                "getty_refs": ref_labels,
                "pisani_dossi_hatcher": en_text,
            }
            entries.append(entry)

    return entries


def parse_passages(wikitext):
    """Extract passages with folio refs and English translations."""
    entries = []

    # First, find and parse preface subsections separately
    # Find all master subsection blocks
    subsection_pattern = r'\{\{master subsection begin\s*\n\s*\|\s*title\s*=\s*([^\n|}]+)'
    subsection_starts = list(re.finditer(subsection_pattern, wikitext))

    preface_subsection_ranges = []
    for i, m in enumerate(subsection_starts):
        title = m.group(1).strip()
        start = m.start()
        # Find the end of this subsection
        end_pattern = r'\{\{master subsection end\}\}'
        end_m = re.search(end_pattern, wikitext[start:])
        if end_m:
            end = start + end_m.end()
        else:
            end = len(wikitext)

        if title in ("First Italian Preface", "Latin Preface", "Second Italian Preface"):
            preface_subsection_ranges.append((start, end, title))
            preface_entries = parse_preface_section(wikitext, start, end, title)
            entries.extend(preface_entries)

    # Mark preface region to skip in main parser
    preface_region_start = preface_subsection_ranges[0][0] if preface_subsection_ranges else 0
    preface_region_end = preface_subsection_ranges[-1][1] if preface_subsection_ranges else 0

    # Now parse the main body (everything outside preface subsections)
    # Split into rows
    rows = re.split(r'\n\|-\s*\n', wikitext)

    current_section = "unknown"

    for row in rows:
        # Skip rows that fall within preface subsections
        # Use a simple heuristic: check if this row's content appears in a preface range
        row_start = wikitext.find(row[:80]) if len(row) > 80 else wikitext.find(row)
        if row_start >= 0 and preface_region_start <= row_start < preface_region_end:
            # Still track section changes
            section_m = re.search(r'title\s*=\s*([^\n|}]+)', row)
            if section_m:
                current_section = section_m.group(1).strip()
            continue

        # Detect section headers
        section_m = re.search(r'title\s*=\s*([^\n|}]+)', row)
        if section_m:
            current_section = section_m.group(1).strip()

        # Find all Getty folio refs in this row (main body format)
        getty_refs = re.findall(r'Page:MS Ludwig XV 13 (\d+[rv])\.jpg\|([^}|]+)', row)
        if not getty_refs:
            continue

        folio = getty_refs[0][0]

        # Split into cells
        cells = re.split(r'\n\|\s*', row)

        # Collect all English text blocks
        english_cells = extract_english_from_cells(cells)

        if english_cells:
            entry = {
                "folio": folio,
                "section": current_section,
                "getty_refs": [f"{r[0]}.{r[1]}" for r in getty_refs],
            }
            # First English cell is typically Hatcher (Getty translation)
            # Second is typically Chidester (Morgan translation)
            if len(english_cells) >= 1:
                entry["hatcher_en"] = english_cells[0]
            if len(english_cells) >= 2:
                entry["chidester_en"] = english_cells[1]
            entries.append(entry)

    return entries


def main():
    print("Reading wikitext...")
    wikitext = WIKITEXT.read_text()
    print(f"Wikitext size: {len(wikitext)} chars")

    print("Parsing passages...")
    entries = parse_passages(wikitext)
    print(f"Extracted {len(entries)} passages with English translations")

    # Stats
    folios = set(e['folio'] for e in entries)
    with_hatcher = sum(1 for e in entries if e.get('hatcher_en'))
    with_chidester = sum(1 for e in entries if e.get('chidester_en'))
    with_pd_hatcher = sum(1 for e in entries if e.get('pisani_dossi_hatcher'))
    sections = set(e['section'] for e in entries)

    print(f"Folios covered: {len(folios)}")
    print(f"With Hatcher translation: {with_hatcher}")
    print(f"With Chidester translation: {with_chidester}")
    print(f"With Pisani Dossi translation: {with_pd_hatcher}")
    print(f"Sections: {sorted(sections)}")

    # Preface coverage
    preface_folios = sorted(set(
        e['folio'] for e in entries
        if e['section'].startswith('Preface')
    ))
    print(f"Preface folios: {preface_folios}")

    output = {
        "source": "Wiktenauer raw wikitext - Fiore de'i Liberi author page",
        "extracted": "2026-04-07",
        "translators": {
            "hatcher_en": "Completed Translation (from the Getty) by Colin Hatcher",
            "chidester_en": "Completed Translation (from the Morgan) by Michael Chidester",
            "pisani_dossi_hatcher": "Translation (from the Pisani Dossi) by Michael Chidester"
        },
        "stats": {
            "total_passages": len(entries),
            "folios_covered": len(folios),
            "with_hatcher": with_hatcher,
            "with_chidester": with_chidester,
            "with_pisani_dossi": with_pd_hatcher,
        },
        "passages": entries
    }

    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nWritten to {OUTPUT}")
    print(f"File size: {OUTPUT.stat().st_size / 1024:.0f} KB")

    # Sample
    print("\n--- Sample preface entries ---")
    for e in entries:
        if e.get('folio') in ('01v', '02r') or e.get('pisani_dossi_hatcher'):
            print(json.dumps(e, indent=2, ensure_ascii=False)[:500])
            print()
            break

    print("\n--- Sample main body entry ---")
    for e in entries[20:22]:
        print(json.dumps(e, indent=2, ensure_ascii=False)[:500])
        print()


if __name__ == "__main__":
    main()
