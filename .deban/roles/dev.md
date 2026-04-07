---
role: dev
owner: Gerald
status: active
last-updated: 2026-04-07
---

# Development

## Scope
Implementation of the scraping, OCR, segmentation, and export pipeline. Owns all code in `src/`, dependency management, and the five-step implementation order defined in the brief.

## Decisions
| Date | Decision | Rationale | Linked roles |
|---|---|---|---|
| 2026-04-07 | Getty IIIF scraper implemented using stdlib only (`urllib`, `json`, `re`) | No external dependencies needed for IIIF manifest parsing + image download. Avoids adding `requests` as a dependency for this step. Alternative considered: `requests` library — rejected as unnecessary for simple GET requests. | [[arch]], [[devops]] |
| 2026-04-07 | Image naming convention: `fol_{NN}{r|v}.jpg` (e.g., `fol_01r.jpg`, `fol_12v.jpg`) | Zero-padded 2-digit folio numbers sort correctly in filesystem. `r`/`v` suffix matches manuscript recto/verso convention. Non-folio images (3D view, crops) get sanitized label names. | [[arch]] |
| 2026-04-07 | Scraper is resumable — skips files >100KB that already exist on disk | Avoids re-downloading 341MB on retry. 100KB threshold prevents treating partial/corrupt downloads as complete. | [[devops]] |
| 2026-04-07 | Used Claude vision (8 parallel agents) for OCR instead of Kraken/Transkribus | Medieval Italian script is not well-served by standard OCR. Claude can read the manuscript images directly and provide both transcription and translation in one pass. Alternatives considered: Kraken + Zenodo model (untested, heavy dependency), Transkribus API (free tier limits, setup overhead). The brief's OCR toolchain was bypassed entirely. | [[arch]], [[qa]] |
| 2026-04-07 | Per-folio cleaned output: `data/cleaned/fol_NNx.md` with Transcription + Translation + Notes sections | One file per folio matches 1:1 with source images. Markdown format readable by humans and parseable for downstream segmentation. Blank pages still get files (noted as blank) for complete coverage. | [[arch]], [[ux]] |
| 2026-04-07 | Parallelized OCR across 8 agents, each handling ~12 folios | 91 folios serial would take hours. 8-way parallel completed in ~7 minutes. Ranges split to keep agents under context limits. | [[devops]] |

## Dead Ends
<!-- APPEND ONLY. Never delete. -->
| Date | What was tried | Why it failed / was rejected |
|---|---|---|

## Lessons
<!-- Distilled principles from Dead Ends. Written to be read cold. -->

## Open Questions
- [ ] Will Wiktenauer respond 200 with polite User-Agent + Referer headers, or do we need the PDF fallback from day one? — owner: Gerald — since: 2026-04-07
- [ ] Is the Hroarr concordance PDF (`hroarr.com/wp-content/uploads/downloads/2016/08/...`) still available? — owner: Gerald — since: 2026-04-07
- [ ] Does Kraken's current version accept the Zenodo model `10.5281/zenodo.10592716` without version conflicts? — owner: Gerald — since: 2026-04-07
- [ ] pdfminer.six layout-aware extraction: does it handle the concordance PDF's column layout correctly, or will pymupdf be needed? — owner: Gerald — since: 2026-04-07

## Assumptions
- Wiktenauer HTML is the fastest path to structured text — status: untested — since: 2026-04-07
- pdfminer.six can extract the concordance PDF with "clear column structure" — status: untested — since: 2026-04-07
- Kraken + Zenodo medieval Italian model produces usable OCR on Getty images — status: **bypassed** — since: 2026-04-07 — note: used Claude vision instead; Kraken never tested. Open question remains whether Kraken would produce more paleographically accurate results for uncertain readings.
- Getty IIIF manifest is stable and returns all ~47 folio images — status: **validated** — since: 2026-04-07 — validated: 2026-04-07 (94 canvases returned, 91 folios + 3 intro images, 341MB total, fol. 40v absent from manifest consistent with blank page in physical MS)

## Dependencies
Blocked by: nothing (first to execute)
Feeds into: [[qa]], [[arch]]

## Session Log
<!-- One line per session, newest first -->
2026-04-07 — SYNC — Full OCR pass complete. 92 cleaned markdown files in data/cleaned/ (4,419 lines). Used Claude vision via 8 parallel agents instead of Kraken. Existing OCR from OCR_/ cross-referenced for fol. 1r, 2r, 4r. Corrections made (e.g., "ayagro" → "magistro"). All agents flagged later folios (35r+) as having faded/uncertain text.
2026-04-07 — SYNC — Getty IIIF scraper built and run. 94 images (341MB) downloaded to data/raw/images/. IIIF manifest assumption validated. fol. 12v appears twice in manifest (sample + in-sequence); in-sequence overwrites sample on disk.
2026-04-07 — INIT — role created, open questions seeded from brief assumptions
