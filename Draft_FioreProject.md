Here’s a clean, implementation-ready project plan as a .md file, structured for actual execution (not just theory):

# Fiore dei Liberi — Full Transcription Project

## 🎯 Objective

Build a **local pipeline** that extracts, normalizes, and compiles a **complete Middle Italian transcription** of *Fior di Battaglia*, including:

- All textual content
- All illustration captions (plays)
- Clean `.txt` export
- Structured `.json` for downstream use (search, visualization, training tools)

---

## 🧱 Scope Definition

### Primary Target
- Getty MS (Ludwig XV 13)
  - Most complete
  - Prose format
  - Includes captions tied to illustrations

### Optional Extensions (Phase 2)
- Morgan MS
- Pisani-Dossi (poetic variant)
- Latin Florius version

---

## 🏗️ System Architecture

### Pipeline Overview
[Source Images / HTML]
↓
[Scraper / Downloader]
↓
[OCR Layer]
↓
[Post-OCR Cleaning]
↓
[Segmentation (Plays / Sections)]
↓
[Normalization Layer]
↓
[Structured Output]
↓
[Exports: .txt / .json / .md]


---

## 📦 Project Structure
fiore-transcription/
│
├── data/
│ ├── raw/
│ │ ├── images/
│ │ └── html/
│ ├── ocr/
│ ├── cleaned/
│ └── final/
│
├── src/
│ ├── scraper/
│ ├── ocr/
│ ├── cleaning/
│ ├── segmentation/
│ ├── normalization/
│ └── export/
│
├── config/
│ ├── manuscripts.yaml
│ └── normalization_rules.yaml
│
├── outputs/
│ ├── fiore_full.txt
│ ├── fiore_structured.json
│ └── fiore.md
│
└── README.md


---

## 🔍 Data Sources

### Primary
- Wiktenauer (HTML structured pages)
- Manuscript image scans (Getty)

### Strategy
- Prefer **HTML transcription when available**
- Fall back to **OCR for missing sections**

---

## ⚙️ Core Components

### 1. Scraper

**Goal:** Extract structured text + metadata

- Input:
  - Wiktenauer pages
- Output:
  - Raw HTML + extracted text blocks

**Tech:**
- Python
- `requests`, `BeautifulSoup`

---

### 2. OCR Layer

**Goal:** Extract text from manuscript images

**Options:**
- Tesseract (baseline)
- Kraken (better for historical scripts)

**Challenges:**
- Gothic / semi-humanist scripts
- Abbreviations (ꝑ, q̃, etc.)

---

### 3. Cleaning Layer

**Tasks:**
- Remove OCR noise
- Normalize spacing
- Fix common OCR errors

Example:
lanza → lanza
q̃ → que
ꝑ → per


---

### 4. Segmentation

**Goal:** Split into meaningful units

- Sections:
  - Abrazare
  - Daga
  - Spada
- Plays:
  - "Io sono..."
  - "Questo è..."

Output format:
```json
{
  "section": "abrazare",
  "play_id": 1,
  "text": "Io sono lo primo zogho..."
}
5. Normalization Layer
Two modes:

A. Diplomatic
Preserve original spelling

B. Normalized
Convert to consistent Middle Italian

Example:

zogho → zogho
gioco → zogho (optional mapping)
6. Export Layer
Generate:

.txt
Flat, readable

.json
Structured for apps

.md
Human-readable with sections

🧠 Key Design Decisions
1. "Zogho" Preservation
Do NOT modernize to "gioco"

Keep semantic fidelity

2. Caption Linking
Each play tied to:

image id

section

3. Variant Handling (Phase 2)
Allow multiple versions per play

🚧 Implementation Phases
Phase 1 — MVP (1–2 days)
Scrape Wiktenauer

Extract all Italian text

Output single .txt

Phase 2 — Structure (2–4 days)
Segment plays

Build JSON schema

Export structured data

Phase 3 — OCR Completion (3–7 days)
Process missing sections from images

Integrate into pipeline

Phase 4 — Normalization & QA
Fix inconsistencies

Manual review pass

🧪 Validation
Checks
No missing sections

No duplicate plays

Consistent spelling

Alignment with manuscript order

🔮 Future Extensions
🔍 Search engine (concept → plays)

🧠 Mapping to grappling primitives

📊 Visualization (flow of techniques)

📱 Mobile study interface

🧩 Anki-style training cards

🛠️ Tech Stack
Python

BeautifulSoup

Tesseract / Kraken

JSON / Markdown outputs

Optional:

SQLite (indexing)

FastAPI (local API)

🚀 First Step
Start with:

mkdir fiore-transcription
cd fiore-transcription
python -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4
Then implement:

src/scraper/wiktenauer_scraper.py
🎯 End State
A clean, complete, local corpus of Fiore’s work:

usable for:

study

search

modeling

grappling analysis