---
project: Fiore dei Liberi Transcription
created: 2026-04-07
status: active
mode: solo
stale_threshold_days: 30
---

# Fiore dei Liberi Transcription — Index

## Brief
A local pipeline to produce a clean, complete, structured Middle Italian transcription of *Fior di Battaglia* (The Flower of Battle) by Fiore de'i Liberi, c. 1410. Primary target: Getty MS Ludwig XV 13. The pipeline scrapes/OCRs source material (Wiktenauer HTML, concordance PDF, Getty IIIF images), segments text into per-play atomic units with metadata, and exports to .txt, .json, and .md formats. All source material is public domain (CC0 for Getty images, CC BY-NC-SA 4.0 for Wiktenauer compilation).

## Active Roles
- [[dev]] — owner: Gerald
- [[arch]] — owner: Gerald
- [[pm]] — owner: Gerald
- [[ux]] — owner: Gerald
- [[qa]] — owner: Gerald
- [[devops]] — owner: Gerald

## Key Decisions
<!-- Cross-role summary, maintained by COMPACT -->

## Open Questions (cross-role)
- Wiktenauer 403 bypass — will polite headers actually work? (see [[pm]], [[dev]])
- Hroarr PDF — is the 2016 concordance URL still live? (see [[dev]])
- Kraken model compatibility — does the Zenodo model work with current Kraken? (see [[dev]], [[qa]])
