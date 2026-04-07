---
role: devops
owner: Gerald
status: active
last-updated: 2026-04-07
---

# DevOps / Infrastructure

## Scope
Environment setup, dependency management, reproducibility. Owns venv, pip requirements, and any containerization if needed.

## Decisions
| Date | Decision | Rationale | Linked roles |
|---|---|---|---|
| 2026-04-07 | Getty IIIF scraper uses Python stdlib only — no pip dependencies for Step 1 | `urllib.request` + `json` + `re` sufficient. Defers venv/dependency setup until Steps 2-3 (PDF/HTML scraping need `pdfminer.six`, `beautifulsoup4`). | [[dev]] |

## Dead Ends
<!-- APPEND ONLY. Never delete. -->
| Date | What was tried | Why it failed / was rejected |
|---|---|---|

## Lessons
<!-- Distilled principles from Dead Ends. Written to be read cold. -->

## Open Questions
- [ ] Should dependencies be pinned in a `requirements.txt` or `pyproject.toml`? The brief uses bare `pip install`. — owner: Gerald — since: 2026-04-07
- [ ] Kraken installation: does it have heavy native dependencies (torch, etc.) that could complicate the venv? — owner: Gerald — since: 2026-04-07

## Assumptions
- Python venv on macOS (M4) is sufficient — no Docker needed for MVP — status: **partially validated** — since: 2026-04-07 — note: Step 1 ran with system Python3 without venv. Venv still untested for heavier deps (kraken, pdfminer).
- All pip packages in the brief install cleanly on ARM64 — status: untested — since: 2026-04-07

## Dependencies
Blocked by: nothing
Feeds into: [[dev]]

## Session Log
<!-- One line per session, newest first -->
2026-04-07 — SYNC — Step 1 ran on system python3, no venv needed. stdlib-only approach confirmed viable for IIIF fetching.
2026-04-07 — INIT — role created
