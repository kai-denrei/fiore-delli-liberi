---
role: ux
owner: Gerald
status: active
last-updated: 2026-04-07
---

# UX / Output Design

## Scope
Design of the interactive reader page — the Fiore node of the GrapplingPrimitives History of Grappling timeline. Audience: martial arts practitioners and historians browsing primary sources.

## Decisions
| Date | Decision | Rationale | Linked roles |
|---|---|---|---|
| 2026-04-07 | 5-tab navigation: Manuscript, Lexicon, Analysis, Amore, About | Separates browsing (folio viewer) from reading (lexicon/analysis) from scholarship (Amore comparison). Alternative: single scrolling page — rejected for mixing modes. | [[arch]] |
| 2026-04-07 | Dual-manuscript viewer with cross-navigation | Getty and PD in same container, same image size, click to swap. Section nav shared with strikethrough for missing sections. PD tags on Getty headings and vice versa. User can compare equivalent folios by toggling. | [[arch]], [[dev]] |
| 2026-04-07 | All tabs always visible, strikethrough when unavailable | Prevents layout jump when navigating between folios with different source coverage. Blank pages show same tab bar (all struck through). | [[arch]] |
| 2026-04-07 | Permanent search bar in nav | Human insisted on this for source verification after AI fabrication was caught. Searches all folios, all sources, auto-switches to Manuscript tab. | [[qa]] |
| 2026-04-07 | Source-linked quotes throughout lexicon and analysis | Every quoted passage is a clickable link that navigates to the folio, switches to the correct tab, and highlights the match. Establishes trust in editorial claims. | [[qa]] |
| 2026-04-07 | Mise-en-page typography: Spectral serif, Inter UI, 64ch measure | Following the mise-en-page skill principles. Tiered spacing, pilcrow marks colored, position labels in faint uppercase. Manuscript images carry the visual weight. | [[arch]] |
| 2026-04-07 | Images normalized to identical 1200x1727px | Both manuscripts render at same size in same container. PD images padded with background color to match Getty aspect ratio. Zero layout shift on MS switch. | [[dev]] |

## Dead Ends
<!-- APPEND ONLY. Never delete. -->
| Date | What was tried | Why it failed / was rejected |
|---|---|---|

## Lessons
<!-- Distilled principles from Dead Ends. Written to be read cold. -->

## Open Questions
- [x] Who is the audience for each output format? — **resolved 2026-04-07**: audience is martial arts practitioners and grappling historians via the GrapplingPrimitives site. Single interactive reader page replaces the three-file export.
- [x] Should the output include folio images alongside transcription? — **resolved 2026-04-07**: yes, manuscript images are the left column of the viewer, sticky on scroll.

## Assumptions
- Three output formats (.txt, .json, .md) are sufficient for MVP — status: **superseded** — since: 2026-04-07 — note: replaced by interactive reader page. The .md and .json still exist in `data/` as build artifacts but are not the deliverable.

## Dependencies
Blocked by: [[dev]] (needs structured data before export design matters)
Feeds into: nothing (terminal)

## Session Log
<!-- One line per session, newest first -->
2026-04-07 — SYNC — Full UX shipped. 5-tab reader, dual MS viewer, permanent search, source-linked quotes, normalized images, all-tabs-always-visible layout. Deployed to GitHub Pages.
2026-04-07 — INIT — role created
