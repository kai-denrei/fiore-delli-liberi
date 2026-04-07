"""
Extract Pisani Dossi Italian text from the rendered Wiktenauer HTML.
The PD text is Novati's 1902 transcription, re-transcribed by Chidester.

Maps PD folios (carta 2a-36b) to approximate Getty folio equivalents
so they can appear as a tab in the reader.
"""

import re
import json
from pathlib import Path

HTML_FILE = Path(__file__).resolve().parents[2] / "data" / "raw" / "wiktenauer" / "fiore_dei_liberi.html"
WIKITEXT_FILE = Path(__file__).resolve().parents[2] / "data" / "raw" / "wiktenauer" / "fiore_dei_liberi_raw.wikitext"
OUTPUT = Path(__file__).resolve().parents[2] / "data" / "pd_italian_extracted.json"


def extract_from_html(html):
    """Extract PD Italian text blocks from rendered HTML.

    The HTML has table rows where PD text appears in a specific column.
    PD text is identified by proximity to Pisani-Dossi image references
    and by being Italian (not English/Latin).
    """
    entries = []

    # Strategy: find all table cells that contain PD folio references,
    # then extract the Italian text from those cells.
    # PD refs look like: Pisani-Dossi MS 02a.jpg or Pisani-Dossi_MS_02a

    # Split HTML into table rows
    rows = re.split(r'<tr[^>]*>', html)

    current_getty_folio = None
    current_section = ""

    for row in rows:
        # Track Getty folio references for mapping
        getty_m = re.findall(r'MS Ludwig XV 13 (\d+[rv])', row)
        if getty_m:
            current_getty_folio = getty_m[0]

        # Track section headers
        section_m = re.search(r'title\s*=\s*"?([^"<>]+)"?', row)
        if section_m:
            current_section = section_m.group(1).strip()

        # Find PD folio references in this row
        pd_refs = re.findall(r'Pisani.Dossi.MS.(\d+[ab])', row)
        if not pd_refs:
            continue

        pd_folio = pd_refs[0]

        # Find Italian text in the PD column
        # The PD column contains text transcribed from Novati's facsimile
        # Look for <td> or <p> content near PD references
        # Extract text from the cell containing the PD section reference

        # Find all cell contents
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)

        for cell in cells:
            # Skip cells that are primarily images
            if '<img' in cell and len(re.sub(r'<[^>]+>', '', cell).strip()) < 30:
                continue
            # Skip cells that are primarily English
            clean = re.sub(r'<[^>]+>', ' ', cell)
            clean = re.sub(r'\s+', ' ', clean).strip()
            if len(clean) < 20:
                continue

            # Check if this cell references PD
            if f'Pisani-Dossi' not in cell and f'Pisani_Dossi' not in cell:
                continue

            # Extract just the text content (not the reference markup)
            # Remove the section template calls
            text = re.sub(r'\{\{section\|[^}]*\}\}', '', cell)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()

            if len(text) > 15:
                entries.append({
                    'pd_folio': pd_folio,
                    'getty_folio': current_getty_folio,
                    'text': text,
                    'section': current_section,
                })

    return entries


def extract_from_rendered_cells(html):
    """Alternative: extract PD Italian from the fully rendered page.

    The Wiktenauer HTML renders transcluded content inline.
    PD Italian text appears in specific columns of the concordance table.
    We can identify it by the column position and Italian language markers.
    """
    entries = []

    # The concordance table structure varies by section, but PD is always
    # in its own column. Let's find rendered PD text by looking for
    # characteristic medieval Italian near PD image references.

    # Find all PD folio image references and their surrounding text
    for m in re.finditer(r'Pisani.Dossi.MS.(\d+[ab])(?:[-_]([a-d]))?\.(?:jpg|png)', html):
        pd_folio = m.group(1)
        pd_sub = m.group(2) or ''

        # Get surrounding context (the table cell this is in)
        # Go back to find the cell start
        cell_start = html.rfind('<td', max(0, m.start() - 3000), m.start())
        cell_end = html.find('</td>', m.end())

        if cell_start < 0 or cell_end < 0:
            continue

        cell = html[cell_start:cell_end]

        # Extract text, removing HTML
        text = re.sub(r'<[^>]+>', ' ', cell)
        text = re.sub(r'\s+', ' ', text).strip()

        # Remove common noise
        text = re.sub(r'Pisani.Dossi MS \d+[ab]\.jpg', '', text)
        text = re.sub(r'\d+px\s*center', '', text)
        text = text.strip()

        if len(text) > 10:
            entries.append({
                'pd_folio': pd_folio,
                'pd_sub': pd_sub,
                'text': text,
            })

    return entries


def extract_pd_from_full_html(html):
    """Most reliable approach: parse the actual rendered Italian text
    that appears between PD section markers in the HTML.

    The PD Italian column in the table has content rendered from
    {{section|Page:Pisani-Dossi MS XX.jpg|ref}} templates.
    In the rendered HTML, this becomes actual Italian text.
    """

    # Find the PD column text by parsing the rendered table structure
    # Each concordance row has columns in order:
    # [Illustrations] [Hatcher EN] [Chidester EN] [Morgan IT] [Getty IT] [PD IT] [Paris Latin]
    # But the column order varies by section...

    # Better approach: find all <p> blocks that contain medieval Italian
    # near PD image references, and are NOT in the Getty or Morgan columns

    # Actually, the simplest reliable approach: extract from the raw cell text
    # in the HTML where we can identify PD column by the column header

    # Let me find table headers that identify the PD column
    pd_col_headers = list(re.finditer(r'Pisani.Dossi Version.*?</(?:th|p)>', html, re.DOTALL))
    print(f"Found {len(pd_col_headers)} PD column headers")

    results = {}  # pd_folio -> list of text blocks

    # For each section of the table, find which column is PD
    # Then extract text from that column in each row

    # Alternative simpler approach: the PD text in the HTML is the content
    # that was transcluded from Page:Pisani-Dossi MS XX.jpg wiki pages.
    # These render as <p> tags with specific content.
    # Let's find them by looking for Italian text patterns near PD markers.

    # Split into rough row-like chunks around PD references
    pd_pattern = r'(?:Page:|File:)Pisani.Dossi.MS.(\d+[ab])(?:[-_]([a-d]))?\.(?:jpg|png)'

    for m in re.finditer(pd_pattern, html):
        pd_folio = m.group(1)
        pd_sub = m.group(2) or ''
        ref = f"{pd_folio}" + (f"-{pd_sub}" if pd_sub else "")

        # Look at the table cell containing this reference
        # Go back to <td and forward to </td>
        search_back = max(0, m.start() - 5000)
        cell_start = html.rfind('<td', search_back, m.start())
        if cell_start < 0:
            continue
        cell_end = html.find('</td>', m.start())
        if cell_end < 0:
            continue

        cell_html = html[cell_start:cell_end]

        # Get all <p> tag contents in this cell
        p_blocks = re.findall(r'<p[^>]*>(.*?)</p>', cell_html, re.DOTALL)

        for block in p_blocks:
            # Clean HTML
            clean = re.sub(r'<[^>]+>', '', block)
            clean = re.sub(r'&[a-z]+;', '', clean)
            clean = re.sub(r'\s+', ' ', clean).strip()

            # Skip very short blocks or English text
            if len(clean) < 15:
                continue

            # Skip if it looks like a reference/caption rather than manuscript text
            if clean.startswith('[') or 'Pisani' in clean or 'Novati' in clean:
                continue

            if ref not in results:
                results[ref] = []
            results[ref].append(clean)

    return results


def build_pd_to_getty_map():
    """Map PD folios to Getty folios based on the concordance structure.

    This is approximate — the PD and Getty have different orderings.
    We use the Wiktenauer concordance table which aligns them.
    """
    wikitext = WIKITEXT_FILE.read_text()

    # Find rows that contain both PD and Getty references
    rows = re.split(r'\n\|-\s*\n', wikitext)

    mapping = {}  # pd_ref -> getty_folio
    current_getty = None

    for row in rows:
        # Find Getty refs
        getty_refs = re.findall(r'Page:MS Ludwig XV 13 (\d+[rv])\.jpg', row)
        if getty_refs:
            current_getty = getty_refs[0]

        # Find PD refs
        pd_refs = re.findall(r'Page:Pisani-Dossi MS (\d+[ab]?)\.jpg\|([^}|]+)', row)
        for pd_fol, pd_sub in pd_refs:
            ref = f"{pd_fol}-{pd_sub}" if pd_sub else pd_fol
            if current_getty:
                mapping[pd_fol] = current_getty
                mapping[ref] = current_getty

    return mapping


def main():
    print("Reading HTML...")
    html = HTML_FILE.read_text()
    print(f"HTML size: {len(html)} chars")

    print("\nExtracting PD Italian text...")
    pd_texts = extract_pd_from_full_html(html)
    print(f"Extracted text for {len(pd_texts)} PD references")

    print("\nBuilding PD → Getty folio mapping...")
    pd_to_getty = build_pd_to_getty_map()
    print(f"Mapped {len(pd_to_getty)} PD refs to Getty folios")

    # Group by Getty folio
    by_getty = {}
    unmapped = []

    for pd_ref, texts in pd_texts.items():
        pd_folio = re.match(r'(\d+[ab])', pd_ref).group(1) if re.match(r'(\d+[ab])', pd_ref) else pd_ref
        getty = pd_to_getty.get(pd_ref) or pd_to_getty.get(pd_folio)

        if getty:
            if getty not in by_getty:
                by_getty[getty] = []
            for t in texts:
                by_getty[getty].append({
                    'pd_ref': pd_ref,
                    'pd_folio': pd_folio,
                    'text': t,
                })
        else:
            for t in texts:
                unmapped.append({'pd_ref': pd_ref, 'text': t})

    print(f"\nGetty folios with PD Italian: {len(by_getty)}")
    print(f"Unmapped PD passages: {len(unmapped)}")

    # Sample output
    for getty_fol in sorted(by_getty.keys())[:5]:
        texts = by_getty[getty_fol]
        print(f"\n  Getty {getty_fol}: {len(texts)} PD passages")
        for t in texts[:2]:
            print(f"    [{t['pd_ref']}] {t['text'][:100]}...")

    output = {
        'source': 'Pisani Dossi MS (1409), Novati 1902 facsimile, transcribed by Chidester',
        'note': 'Same author as Getty (Fiore dei Liberi). Dated Feb 10, 1409. Shorter, more condensed redaction. Dedicated to Niccolò III d\'Este.',
        'extracted': '2026-04-07',
        'by_getty_folio': by_getty,
        'unmapped': unmapped,
        'pd_to_getty_map': {k: v for k, v in pd_to_getty.items() if not '-' in k},  # Only base folios
        'stats': {
            'total_pd_refs': len(pd_texts),
            'getty_folios_covered': len(by_getty),
            'unmapped_passages': len(unmapped),
        }
    }

    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\nWritten to {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
