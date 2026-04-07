---
role: arch
owner: Gerald
status: active
last-updated: 2026-04-07
---

# Architecture

## Scope
Pipeline design, data schema, file/directory structure, and technology choices. Owns the data flow from source → raw → cleaned → segmented → exported.

## Decisions
| Date | Decision | Rationale | Linked roles |
|---|---|---|---|
| 2026-04-07 | Play-as-atomic-unit data model with JSON schema | Matches manuscript structure — each text block belongs to one figure in one folio. Enables per-play querying and validation. | [[dev]], [[qa]] |
| 2026-04-07 | Three-source strategy: Wiktenauer HTML (primary), concordance PDF (fallback), Getty IIIF+OCR (secondary) | Redundancy against Wiktenauer 403. OCR covers gaps in transcription. | [[dev]] |
| 2026-04-07 | Five-step pipeline: IIIF fetch → PDF extract → HTML scrape → segment → export | IIIF first so OCR can run in parallel with scraping. | [[dev]], [[devops]] |
| 2026-04-07 | IIIF manifest URL: `928f4025-a697-4b9f-b5ee-9a5d7e15a6ff` (v2 manifest, 94 canvases) | Discovered via Getty collection page. No auth required. Full-res images at `/full/full/0/default.jpg`. Alternative: v3 manifest — not found, v2 is what Getty serves. | [[dev]] |
| 2026-04-07 | Directory structure: `data/raw/images/` for Getty folio JPEGs | Matches brief's project structure. Images are the raw input for OCR pipeline. | [[dev]], [[devops]] |
| 2026-04-07 | Cleaned text output: `data/cleaned/fol_NNx.md` — one markdown per folio with Transcription/Translation/Notes | 1:1 mapping with source images. Each file is self-contained. Blank pages included for completeness. This is the intermediate format between raw images and final segmented JSON. | [[dev]], [[ux]] |
| 2026-04-07 | OCR approach changed: Claude vision instead of Kraken/Transkribus pipeline | The brief's OCR toolchain (Kraken + Zenodo model, Transkribus fallback) was bypassed. Claude vision reads medieval script and translates in a single pass. This collapses Steps 1-3 of the brief's pipeline into a single step. Trade-off: less paleographically rigorous than a trained HTR model, but produces usable first-pass results immediately. | [[dev]], [[qa]] |
| 2026-04-07 | Final deliverable: static single-page reader, not the brief's three-file export (.txt/.json/.md) | The GrapplingPrimitives history page goal replaced the original brief's deliverables. Single HTML file with data.json, deployed to GitHub Pages. No build step, no framework. | [[dev]], [[ux]], [[pm]] |
| 2026-04-07 | 5-tab navigation: Manuscript, Lexicon, Analysis, Amore, About | Manuscript contains Getty/PD dual viewer. Lexicon and Analysis separated from Manuscript for cleaner reading. Amore tab for cross-manuscript vocabulary comparison. Alternative considered: single scrolling page — rejected because it mixed browsing (folio viewer) with reading (lexicon/analysis). | [[ux]] |
| 2026-04-07 | Dual-manuscript viewer sharing one layout container | Getty and PD render in same div, same image size (1200x1727), same grid. Switching swaps content in place. PD images padded to match Getty dimensions. Section nav shared with strikethrough for missing sections. Eliminates layout jump. | [[ux]], [[dev]] |
| 2026-04-07 | All translation tabs always visible, strikethrough when unavailable | 6 tabs for Getty (Hatcher, Chidester, Hatcher PD, PD Italian, Getty Italian, Raw OCR), 2 for PD. Unavailable tabs disabled+struck through. Blank pages show same tab bar. No layout jump between folios. | [[ux]] |

## Dead Ends
<!-- APPEND ONLY. Never delete. -->
| Date | What was tried | Why it failed / was rejected |
|---|---|---|

## Lessons
<!-- Distilled principles from Dead Ends. Written to be read cold. -->

## Open Questions
- [ ] Should the pipeline be orchestrated (Makefile, task runner) or just sequential scripts? — owner: Gerald — since: 2026-04-07
- [ ] Is the `figure_role` detection heuristic (text pattern matching) sufficient, or will ambiguous plays need manual annotation? — owner: Gerald — since: 2026-04-07

## Assumptions
- The data schema covers all play types in the Getty MS — status: untested — since: 2026-04-07
- Segmentation by `¶` markers and "Qui comincia/finisce" patterns will catch all section boundaries — status: untested — since: 2026-04-07
- Claude vision OCR is accurate enough for a usable first pass — status: **partially validated** — since: 2026-04-07 — note: prologue pages cross-checked against existing OCR showed corrections needed (previous OCR garbled "magistro" etc.). Illustration page captions not yet cross-checked against any reference. All agents flagged fol. 35r+ as uncertain.

## Dependencies
Blocked by: nothing
Feeds into: [[dev]], [[qa]]

## Session Log
<!-- One line per session, newest first -->
2026-04-07 — SYNC — Final architecture: 5-tab static reader on GitHub Pages. Dual MS viewer (Getty/PD), 6 translation sources, full-text search, lexicon, sentiment analysis, Amore comparison tab. Brief's original 3-file export plan replaced entirely. Deployed to kai-denrei.github.io/fiore-delli-liberi.
2026-04-07 — SYNC — Full OCR complete via Claude vision. Pipeline architecture changed: brief's 5-step plan collapsed. Kraken/Transkribus bypassed. New intermediate format: data/cleaned/*.md. Accuracy assumption partially validated but needs cross-referencing.
2026-04-07 — SYNC — IIIF manifest structure confirmed (v2, 94 canvases). Image download path and naming convention decided. fol. 40v absent — noted as physical MS blank.
2026-04-07 — INIT — role created, initial architecture decisions recorded from brief
