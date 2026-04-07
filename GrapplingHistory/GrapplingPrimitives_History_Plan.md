# History of Grappling — GrapplingPrimitives Section Plan

## Vision

A dedicated section of GrapplingPrimitives tracing grappling as a continuous human
practice across ~4000 years of documented history. The **interactive timeline** is the
organizing spine. Each node on the timeline is a documented tradition with primary sources,
linked back to the Grappling Primitives movement taxonomy.

The thesis: the underlying movement vocabulary is ancient and stable. The names, rules,
and contexts change. The primitives don't.

---

## The Fiore Project as Proof of Concept

The Fior di Battaglia work in progress is the template for every node:

1. **Primary source** — manuscript images (CC0 where possible)
2. **Raw OCR** — direct from hi-res images via Kraken
3. **New translation** — Claude translation from OCR output
4. **Comparison layer** — diff against established translations (Leoni, Hatcher, Windsor)
5. **Primitives mapping** — each play tagged to movement taxonomy
6. **Interactive display** — image + Italian + translation + primitives tags

This is the deliverable for Fiore. Replicate the structure for each timeline node.

---

## Timeline Nodes (Priority Order)

### Tier 1 — Rich primary sources, strong scholarly record

| Date | Tradition | Primary Source | Status |
|---|---|---|---|
| ~2000 BCE | Egyptian wrestling (Beni Hassan) | Tomb paintings, Middle Kingdom | Images CC0 via Cairo Museum |
| 648 BCE | Greek Pankration | Vase paintings, literary sources (Pindar, Philostratus) | Public domain |
| ~77 CE | Roman wrestling | Pliny, Statius; relief sculptures | Public domain |
| ~1410 | Fiore dei Liberi — Fior di Battaglia | Getty MS Ludwig XV 13 | **IN PROGRESS** |
| ~1443 | Hans Talhoffer — Fechtbuch | Multiple MSS, several digitized | CC0 (some) |
| ~1539 | Fabian von Auerswald — Ringer kunst | Printed edition, digitized | Public domain |
| 1882 | Judo (Kano Jigoro) | Kodokan founding documents | Mixed copyright |

### Tier 2 — Good sources, more work required

| Date | Tradition | Notes |
|---|---|---|
| ~700 CE | Sumo (Nihon Shoki) | Japanese records, translation needed |
| ~1300s | Ott Jud (German wrestling) | In Liechtenauer MSS, no standalone |
| ~1480s | Filippo di Vadi | Direct Fiore successor, Latin MS |
| ~1525 | Pietro Monte — Collectanea | Italian humanist wrestling treatise |
| ~1600s | Japanese jujutsu systematization | Multiple ryu, complex provenance |
| ~1870s | Lancashire / Catch wrestling | Primarily oral tradition + newspaper records |
| 1925 | Gracie jiu-jitsu | Contemporary, copyright issues |

---

## Page Architecture

```
/history
  /timeline          ← interactive timeline (main entry point)
  /fiore             ← Fior di Battaglia deep dive
  /pankration        ← Greek pankration
  /beni-hassan       ← Egyptian wrestling
  /talhoffer         ← Fechtbuch
  /...
```

### Timeline Component

- Horizontal scrubber: ~2000 BCE → present
- Nodes: positioned by date, sized by richness of primary sources
- Click node → expands to tradition card
- Tradition card contains:
  - Thumbnail of primary source
  - 2-sentence context
  - "Explore" → full tradition page
- Filter by: **continent**, **weapon/no weapon**, **sport/combat**, **primitives present**

### Tradition Page (template, Fiore as example)

```
┌─────────────────────────────────────────────┐
│ HEADER: Title, date, tradition, location     │
├──────────────┬──────────────────────────────┤
│ Manuscript   │ Introduction text             │
│ viewer       │ (context, significance)       │
│ (zoomable)   │                              │
├──────────────┴──────────────────────────────┤
│ TEXT COMPARISON PANEL                        │
│ [Italian original] [New translation] [Leoni] │
│ [Hatcher] [Windsor]                          │
│ — toggle between, highlight differences      │
├─────────────────────────────────────────────┤
│ PLAYS BROWSER                                │
│ Grid of plays with: image | text | tags      │
│ Tags: primitives present in each play        │
│ Filter by primitive type                     │
├─────────────────────────────────────────────┤
│ PRIMITIVES CROSSWALK                         │
│ "This technique appears in..." → links to    │
│ modern equivalents in main GP taxonomy       │
└─────────────────────────────────────────────┘
```

---

## Translation Comparison Format

For each play, store as JSON:

```json
{
  "folio": "6v-a",
  "section": "abrazare",
  "play_id": 1,
  "figure_role": "remedy_master",
  "text_original_ocr": "...",
  "translations": {
    "claude_new": "...",
    "leoni": "...",
    "hatcher": "...",
    "windsor": "..."
  },
  "translation_notes": "Key divergence: 'presa' rendered as 'grip' (Leoni) vs 'hold' (Windsor) vs 'lock' (Hatcher). Claude reads as 'hold' on balance of context.",
  "primitives_tags": ["single_leg", "head_control", "hip_throw"],
  "danger_level": "mortal"
}
```

The comparison layer is where the scholarly value lives. Disagreements between translators
are almost always technically significant — they reflect genuine ambiguity in Fiore's
language that has real implications for how a technique is interpreted.

---

## Pankration Node — Quick Sketch

**Primary sources:**
- Pindar's Odes (5th c. BCE) — literary descriptions
- Philostratus — *Gymnasticus* (3rd c. CE) — most detailed technical account
- Vase paintings: British Museum, Louvre, Athens National Museum (CC0 images available)
- Bronze sculptures

**Key texts for translation:**
- Philostratus on technique: discusses use of the hands vs feet, standing vs ground
- Milo of Croton references — the legendary strength tradition
- Olympic records (Eusebius)

**Primitives present in Pankration:**
- Striking to create grappling entries (the bridge to wrestling)
- Ground control (Kato pale — ground fighting, explicitly documented)
- Chokes (references in literary sources)
- Leg attacks (debated — some sources suggest prohibited in some variants)

**Connection to Fiore:**
- Both distinguish sport variant from "mortal" variant — Fiore's *solaço* vs *ira*
  maps directly to the Greek distinction between *pale* (sport wrestling) and
  *pankration* (everything permitted)
- Both use a pedagogical progression from basics to compound techniques

---

## Beni Hassan Node — Quick Sketch

**Primary source:**
- Tomb of Khnumhotep II, Beni Hassan, Egypt (~1900 BCE)
- 400+ wrestling figures painted on tomb walls
- Represent the oldest continuous visual sequence of grappling instruction

**What makes it remarkable:**
- Techniques are clearly sequential — it reads as a teaching progression
- Identifiable techniques: hip throw, double leg, arm drag entries, guard-like position,
  ankle pick, seated grappling
- Several figures show what appears to be a referee figure
- Confirms grappling *as a discipline* (not just fighting) at ~2000 BCE

**Digitization status:**
- High-res images available via Oriental Institute, Chicago (some CC0)
- Full photographic record in Newberry 1893 (public domain)

---

## Primitives Crosswalk Logic

Each historical play tagged with GP taxonomy terms. Example for Fiore folio 6v-a:

```
Fiore 6v-a (Remedy Master, Abrazare)
→ tags: [grip_break, arm_control, rotation_throw]
→ modern equivalents:
   - grip_break → appears in 47 GP nodes
   - arm_control → appears in 83 GP nodes  
   - rotation_throw → appears in 31 GP nodes
→ "This 1410 technique shares movement structure with..."
```

This is the core product insight: Fiore's plays aren't historical curiosities — they're
documented instances of the same primitives that show up in modern BJJ/wrestling.

---

## Build Priority

**Phase 1 — Fiore standalone page** (leverage OCR pipeline already running)
- Manuscript viewer (Getty IIIF)
- 4-way translation comparison panel
- Plays browser with primitive tags

**Phase 2 — Timeline component**
- Interactive horizontal timeline
- First 3 nodes: Beni Hassan, Pankration, Fiore
- Establishes the pattern

**Phase 3 — Expand timeline nodes**
- Talhoffer, Auerswald, Ott
- Sumo records
- Judo founding documents

**Phase 4 — Primitives crosswalk**
- Tag all historical plays
- Connect to main GP taxonomy
- "Time travel" feature: see how a specific primitive is documented across history

---

## The Differentiator

Most grappling history content is either:
- Academic (wall of text, no interactivity)
- Enthusiast (HEMA recreation videos, no scholarly apparatus)

GrapplingPrimitives can be neither: **primary sources + movement analysis + modern connection**.
The interactive timeline makes it navigable. The primitives crosswalk makes it useful
for practitioners, not just historians.

The solaço/ira passage from Fiore's prologue is the opening line for the whole section:
*"Grappling is of two kinds."* It's been two kinds for at least 4000 years.
