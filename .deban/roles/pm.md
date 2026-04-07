---
role: pm
owner: Gerald
status: active
last-updated: 2026-04-07
---

# Project Management

## Scope
Project scope, milestones, priorities, and risk tracking. Owns the implementation order and validation targets.

## Decisions
| Date | Decision | Rationale | Linked roles |
|---|---|---|---|
| 2026-04-07 | MVP scope: Getty MS only, no multi-MS collation, no English translation | Keep scope tight. Collation and Anki export listed as future extensions. | [[arch]], [[dev]] |
| 2026-04-07 | Scope expanded: English translations now included per folio | Gerald's intermediary goal is "translations for every page in one place." This changes the MVP — translation is no longer a future extension. The cleaned files already contain translations from the Claude vision OCR pass. | [[dev]], [[ux]] |

## Dead Ends
<!-- APPEND ONLY. Never delete. -->
| Date | What was tried | Why it failed / was rejected |
|---|---|---|

## Lessons
<!-- Distilled principles from Dead Ends. Written to be read cold. -->

## Open Questions
- [ ] Wiktenauer 403: the brief assumes polite headers will work. No evidence this has been tested. If it fails, Step 3 is blocked and Step 2 (PDF) becomes the primary path, not a fallback. This changes the implementation order. — owner: Gerald — since: 2026-04-07
- [ ] Validation play counts are vague ("Daga: ~100+ plays total"). What are the authoritative counts per section? Without firm numbers, QA can't validate segmentation. — owner: Gerald — since: 2026-04-07
- [x] The brief lists Step 1 as IIIF image download, but OCR (which needs those images) is not a numbered step — it's implied. When does OCR actually run? — owner: Gerald — since: 2026-04-07 — **resolved 2026-04-07**: OCR ran immediately after image download using Claude vision. The brief's 5-step pipeline was collapsed — Steps 2-3 (PDF/HTML scraping) bypassed for now.
- [ ] Is there a realistic timeline or is this open-ended? Solo mode suggests exploratory, but the 5-step plan reads like a sprint. — owner: Gerald — since: 2026-04-07
- [x] The brief mentions Transkribus as a Kraken alternative but provides no decision criteria for switching. What's the trigger? — owner: Gerald — since: 2026-04-07 — **resolved 2026-04-07**: Both Kraken and Transkribus bypassed entirely. Claude vision used instead. If transcription accuracy proves insufficient after cross-referencing with scholarly editions, Kraken/Transkribus could still be tried on specific problem folios.

## Assumptions
- All source URLs (Wiktenauer, Hroarr, Getty IIIF) are currently live and accessible — status: untested — since: 2026-04-07
- Solo mode means no external collaborators or deadlines — status: untested — since: 2026-04-07

## Dependencies
Blocked by: nothing
Feeds into: all roles

## Session Log
<!-- One line per session, newest first -->
2026-04-07 — SYNC — Scope expanded to include translations. 2 open questions resolved (OCR sequencing, Transkribus trigger). Brief's pipeline collapsed from 5 steps. 92 folios transcribed+translated in one pass.
2026-04-07 — INIT — role created, 5 open questions surfaced from brief gaps
