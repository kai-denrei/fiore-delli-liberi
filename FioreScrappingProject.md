# CLAUDE.md — Fiore dei Liberi Transcription Project

## What this project is

A local pipeline to produce a clean, complete, structured **Middle Italian transcription** of
*Fior di Battaglia* (The Flower of Battle) by Fiore de'i Liberi, c. 1410.

Primary target: **Getty MS Ludwig XV 13** — the most complete manuscript, in prose format,
fully digitized under CC0 by the J. Paul Getty Museum.

All source material is **public domain**. No copyright concerns.

---

## End deliverables

| File | Description |
|---|---|
| `fiore_full.txt` | Flat text, all sections in manuscript order |
| `fiore_structured.json` | Each play as an object with metadata |
| `fiore.md` | Human-readable with section headers |

---

## Data schema (plays as atomic units)

```json
{
  "ms": "Getty",
  "folio": "6v",
  "section": "abrazare",
  "subsection": "remedy_master_1",
  "play_id": 1,
  "figure_role": "scholar",
  "text_original": "Io son lo primo zogho...",
  "text_normalized": null,
  "notes": ""
}
```

`figure_role` values: `guard_master`, `remedy_master`, `scholar`, `counter_master`,
`counter_scholar`, `player`

`section` values (Getty order): `abrazare`, `bastoncello`, `daga`, `spada_un_mano`,
`spada_dui_mani`, `spada_en_arme`, `azza`, `lanza`, `mounted`

---

## Source strategy

### Primary: Wiktenauer HTML transcription

Wiktenauer has a full concordance of all four manuscripts with Italian transcription.
URL: `https://wiktenauer.com/wiki/Fior_di_Battaglia_(MS_Ludwig_XV_13)`

**Known issue:** Wiktenauer returns 403 to standard scrapers. Mitigations:
- Use a real browser User-Agent header
- Add `Referer` header
- Add polite delays (2–3s between requests)
- If still blocked: fall back to their public PDF export (hroarr.com hosts the 2016
  concordance PDF — see below)

**Fallback PDF:** `https://hroarr.com/wp-content/uploads/downloads/2016/08/wiktenauer-Fiore-de-i-Liberi-compilation-2016.pdf`  
This is the Wiktenauer print compilation (CC BY-NC-SA 4.0) with full Italian transcription
by Colin Hatcher (Getty) and Michael Chidester (Morgan, Pisani-Dossi). Scraping this
PDF is the most reliable fallback.

### Secondary: Getty manuscript images (CC0)

For sections where HTML transcription is absent or unclear, OCR the source images.

Getty image URL pattern:
```
https://media.getty.edu/iiif/image/{object_id}/full/max/0/default.jpg
```

The Getty IIIF manifest for MS Ludwig XV 13:
```
https://media.getty.edu/iiif/manifest/63b4f3e9-ec74-49da-b5e7-e0e57d30be34
```

Fetch the manifest to get all folio image URLs programmatically. This is CC0 — download
freely.

---

## OCR notes

**Do NOT use Tesseract for this.** It is not trained for medieval Italian humanist script.

Use **Kraken** instead:
```bash
pip install kraken
kraken get 10.5281/zenodo.10592716  # HTR-United medieval Italian model
```

Or use the **Transkribus** Public API (free tier) if Kraken quality is insufficient —
it has dedicated medieval Italian models fine-tuned on similar manuscripts.

Key OCR challenges:
- Abbreviations: `ꝑ` = per, `q̃` = que, `ā` = an/am, trailing `·` for nasal
- Paragraph markers: alternating red/blue ¶ signs — treat as sentence separators
- Ligatures: `st`, `ct`, `fi` combinations
- Word-final `-o` often written as superscript loop

---

## Segmentation logic

Fiore's text has a consistent structure. Use it to auto-segment:

**Section openers** (in Italian):
- `"Qui comincia..."` — section start
- `"Qui finisce..."` — section end

**Play separators:**
- Coloured ¶ paragraph markers in source
- In Wiktenauer HTML: `<p>` tags with class annotations
- In PDF text: bare ¶ character

**Figure role detection** (from text patterns):
| Pattern | Role |
|---|---|
| `"Io son lo primo magistro..."` | `remedy_master` |
| `"Io son lo contrario..."` | `counter_master` |
| `"Io son scolaro..."` | `scholar` |
| `"Io son zugadore..."` | `player` |
| Guards section: `"Io son posta..."` | `guard_master` |

**Known ambiguity:** Some plays are spoken in first person by the figure without explicit
role declaration. Cross-reference folio position and context (scholarly consensus: if it
follows a remedy master and uses the same hold, it's a scholar).

---

## Known gotchas

1. **Folio 38 is misbound.** In the physical Getty MS, folio 38 (additional dagger plays)
   appears out of sequence. It belongs between ff. 14–15. Some editions reorder it; Wiktenauer
   preserves physical order. Note this in the JSON with `"misbound": true`.

2. **Wiktenauer concordance columns:** The Wiktenauer page lays out all four MSS in parallel
   columns. When scraping, only extract the **Getty column** (leftmost of the two long-text
   columns). Do not mix in Morgan variants without flagging them.

3. **"Solaço" vs "ira" passage** — this appears in the preface (ff. 1v–2v), not in the
   plays. It's the abrazare introduction distinguishing training grappling from mortal
   grappling. Segment it as section `"preface"`, play_id `null`.

4. **The seven swords (segno)** diagram at f. 32r has surrounding text (the four animals:
   elephant, tiger, lion, lynx). Treat as section `"segno"`, separate from sword plays.

5. **Wiktenauer uses MediaWiki markup** in raw page source. If scraping raw wiki, strip
   `{{`, `}}`, `[[`, `]]`, `''`, `'''` etc. before processing.

---

## Project structure

```
fiore-transcription/
├── CLAUDE.md               ← this file
├── README.md
│
├── data/
│   ├── raw/
│   │   ├── images/         ← Getty IIIF downloads (CC0)
│   │   ├── html/           ← Wiktenauer page HTML
│   │   └── pdf/            ← Wiktenauer concordance PDF
│   ├── ocr/                ← Kraken output per folio
│   ├── cleaned/            ← Post-cleaning text per folio
│   └── segments/           ← Per-play JSON fragments
│
├── src/
│   ├── scraper/
│   │   ├── wiktenauer.py   ← HTML scraper with polite headers
│   │   ├── getty_iiif.py   ← IIIF manifest fetcher + image downloader
│   │   └── pdf_extract.py  ← PDF text extraction (pdfminer or pymupdf)
│   ├── ocr/
│   │   └── run_kraken.py   ← Batch OCR runner
│   ├── cleaning/
│   │   └── clean.py        ← Abbreviation expansion, noise removal
│   ├── segmentation/
│   │   └── segment.py      ← Split into plays, assign roles
│   ├── normalization/
│   │   └── normalize.py    ← Optional: consistent spelling pass
│   └── export/
│       └── export.py       ← Generate .txt, .json, .md
│
├── config/
│   ├── manuscripts.yaml    ← MS metadata, folio ranges per section
│   ├── sections.yaml       ← Section names, folio ranges, play counts
│   └── abbrev_map.yaml     ← Abbreviation expansion rules
│
└── outputs/
    ├── fiore_full.txt
    ├── fiore_structured.json
    └── fiore.md
```

---

## Implementation order

### Step 1 — Getty IIIF manifest
```python
# src/scraper/getty_iiif.py
# Fetch manifest, extract all canvas/image URLs, download to data/raw/images/
# ~47 folios for Getty MS
```

### Step 2 — PDF extraction (fastest path to full text)
```python
# src/scraper/pdf_extract.py
# Extract text from Wiktenauer 2016 concordance PDF
# Target pages 21–473 (preface through appendix)
# The PDF has clear column structure — use pdfminer.six for layout-aware extraction
```

### Step 3 — Wiktenauer HTML scraper (for structured metadata)
```python
# src/scraper/wiktenauer.py
# Scrape the concordance table, extract per-play text + folio refs
# Handle 403: use requests.Session with browser-like headers + 3s delay
```

### Step 4 — Segmentation
```python
# src/segmentation/segment.py
# Input: cleaned text blocks
# Output: list of play dicts matching schema above
```

### Step 5 — Export
```python
# src/export/export.py
# Generate all three output formats from structured data
```

---

## First command to run

```bash
mkdir -p fiore-transcription/{data/{raw/{images,html,pdf},ocr,cleaned,segments},src/{scraper,ocr,cleaning,segmentation,normalization,export},config,outputs}
cd fiore-transcription
python -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 pdfminer.six kraken Pillow tqdm pyyaml
```

Then start with `src/scraper/getty_iiif.py` — get the images first so OCR can run in
parallel with scraping.

---

## Validation targets

Cross-check against known play counts:
- Abrazare: 16 plays + 4 guards (Getty)
- Daga: 9 remedy masters, ~100+ plays total
- Spada a dui mani wide: 20 plays
- Spada a dui mani narrow: ~30 plays

Source for counts: Wiktenauer concordance table of contents.

---

## Future extensions (out of scope for MVP)

- Alignment with Grappling Primitives taxonomy (map plays → movement primitives)
- Search index: concept → relevant plays
- Multi-MS variant collation (Getty vs Morgan for shared plays)
- Anki deck export (image + Italian + English per play)
