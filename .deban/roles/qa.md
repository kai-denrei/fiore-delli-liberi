---
role: qa
owner: Gerald
status: active
last-updated: 2026-04-07
---

# Quality Assurance

## Scope
Validation of transcription accuracy, segmentation correctness, and output completeness. Owns play count validation, OCR quality checks, and cross-source consistency.

## Decisions
| Date | Decision | Rationale | Linked roles |
|---|---|---|---|
| 2026-04-07 | OCR quality bar: first-pass usable, cross-referencing with scholarly editions deferred | All 8 agents flagged paleographic uncertainty, especially fol. 35r+. Acceptable for "clean text references for every page" goal. Scholarly accuracy requires cross-referencing with Novati, Mondschein, Leoni editions — not blocked on this. | [[dev]], [[pm]] |

## Dead Ends
<!-- APPEND ONLY. Never delete. -->
| Date | What was tried | Why it failed / was rejected |
|---|---|---|

## Lessons
<!-- Distilled principles from Dead Ends. Written to be read cold. -->

## Open Questions
- [x] What is the acceptable OCR error rate before manual correction is needed? The brief doesn't set a quality bar. — owner: Gerald — since: 2026-04-07 — **partially resolved 2026-04-07**: first-pass quality accepted for now. Cross-referencing with editions will be the correction mechanism. No formal error rate measured yet.
- [ ] Transcription accuracy of fol. 35r–47r: multiple agents flagged faded/small text and heavy abbreviation in this range. These folios need priority cross-referencing. — owner: Gerald — since: 2026-04-07
- [ ] How to validate segmentation when play counts are approximate ("~100+ plays")? Need authoritative counts. — owner: Gerald — since: 2026-04-07
- [ ] Should there be a spot-check process: randomly sample N plays, compare against manuscript images? — owner: Gerald — since: 2026-04-07
- [ ] The misbound folio 38 — how to verify it's handled correctly in the output? — owner: Gerald — since: 2026-04-07

## Assumptions
- Wiktenauer concordance play counts are authoritative enough for validation — status: untested — since: 2026-04-07
- Cross-checking PDF vs HTML extraction will catch most errors — status: untested — since: 2026-04-07

## Dependencies
Blocked by: [[dev]] (needs outputs to validate)
Feeds into: [[pm]] (quality gates)

## Session Log
<!-- One line per session, newest first -->
2026-04-07 — SYNC — 92 folio transcriptions produced. Quality bar set: first-pass usable, correction via cross-referencing deferred. Later folios (35r+) flagged as lower confidence. Folio 38 misbinding correctly noted in output.
2026-04-07 — INIT — role created, 4 open questions on validation strategy
