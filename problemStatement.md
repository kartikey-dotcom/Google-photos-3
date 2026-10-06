# Product Requirement & Build Brief: Anti-Gravity MVP Engine

## 1. Executive Problem Statement & Scope Definition

> "High-stakes utility and site documentation photos (Category D) stored in consumer cloud galleries fail catastrophically during time-critical professional disputes because existing multimodal search models rely on conversational chat paradigms, generic OCR optimized only for planar black-and-white documents, and flat chronological libraries that interleave sensitive personal media with professional assets."

**Methodological Scope & Segmentation Note:**
While Category-D utility retrieval failures spanned our entire research cohort (e.g., medicine strips, identity cards, domestic receipts in P#1, P#2, and P#5), this MVP intentionally focuses on the high-consequence sub-segment instantiated by P#3 and P#6—where retrieval carries immediate financial, legal, and reputational risk on active job sites.

When field professionals (architects, site engineers, project managers) attempt on-site retrieval under direct scrutiny from clients, contractors, or municipal authorities, current solutions (Google Photos / "Ask Photos") break down across three fatal friction points:

* **Semantic Cross-Contamination:** Natural language and object queries (e.g., "measuring tape pipe") contaminate professional search grids with domestic family photos (e.g., children’s crafts, living room curtain rods), causing acute professional embarrassment.
* **Text-on-Texture Blindness:** Existing OCR engines fail to index non-planar, low-contrast, or rough-surface markings—such as red grease pencil on pitted travertine, chalk on formwork, black wax marker on wire-cut brick, or faded circular seals on dot-matrix lab reports.
* **Conversational Latency & Thumbnail Blindness:** Conversational chat interfaces consume 40%+ of mobile viewports with conversational prose and compress search results into single-row horizontal carousels (8–10s latency). Standard 1-inch thumbnails force high-friction modal tap-and-zoom inspection cycles that reset scroll positions upon exit.

## 2. Product Vision & MVP Objective

Build **"Evidence Lens" (SiteLens Core)**: An AI-native, multimodal retrieval feature embedded within a Google Photos–style media container that turns photo galleries from a passive nostalgic scrapbook into a high-density, zero-latency physical evidence audit engine.

The MVP must enable an external evaluator to successfully execute the "May 2024 Silver Travertine Lot Code Retrieval", the "Jubilee Hills Plumbing Offset Verification", and the "Municipal Lab Cube Test Report" within 10 seconds, demonstrating:

* Zero cross-domain leakage from family/domestic media.
* Instant visual legibility of handwritten marks on non-planar construction surfaces.
* Sub-100ms UI response without conversational chat overhead.

## 3. Core Functional Requirements (The 4 AI-Native Pillars)

### Pillar 1: Autonomous Ingest Partitioning (Work vs. Personal Quarantine)
* **Spatial-Temporal Clustering (DBSCAN):** Automatically cluster captures based on recurrent visits to unmapped commercial/job-site micro-radii (e.g., construction sites, industrial yards, municipal offices) and architectural scene priors (exposed rebar, masonry, formwork, scaffolding).
* **Domain Quarantine:** High-entropy utility captures are isolated into a dedicated "Evidence / Site Stream." Queries executed within work contexts strictly exclude domestic/personal images from candidate search results.

### Pillar 2: Substrate-Aware Visual OCR (Non-Planar Text Extraction)
* **Texture & Marker Tuning:** Detect non-standard, low-fidelity, handwritten text:
  * Red/black wax grease pencil on textured travertine stone and rough clay brick.
  * Spray paint and chalk on cured concrete and formwork.
  * Dot-matrix printing, handwritten margin notes, and blue stamped municipal/lab seals on physical paper.
* **Surface Classification:** Tag images with substrate attributes (Rough Stone, Wire-Cut Brick, A4 Document / Seal, Timber Frame) to enable instant multi-modal facet narrowing.

### Pillar 3: Dynamic Evidence-Centered Cropping (Thumbnail Telemetry)
* **Attention-Crop Previews:** When a query matches a detected marking or tool (e.g., LOT-GR-408, OFFSET 150mm, or Stanley Tape), the thumbnail preview dynamically crops and centers directly on the localized bounding box of that evidence, rather than rendering an unreadable wide shot.
* **Inline Verification Badges:** Render detected alphanumeric tokens as high-contrast overlay pills directly on thumbnails in the grid view.

### Pillar 4: High-Density Triage Canvas (Zero-Chat UX)
* **Dense Multi-Column Grid:** 3-to-4 column vertical scroll layout on mobile/desktop, utilizing 100% of vertical screen space. No conversational text introductions or single-row carousels.
* **Persistent Scroll Indexing:** Tapping to inspect an asset full-screen and backing out must retain the exact scroll offset without reloading or shifting the grid.
* **Telegraphic & Multimodal Inputs:** Support direct token queries (LOT-GR-408), material facets (Travertine), and reference image inputs (point camera at current floor → retrieve historical rough-in).

## 4. Ground-Truth Test Matrix & Acceptance Benchmarks (64-Asset Pool)

The deployed MVP must demonstrate clear differentiation when toggling between "Legacy Search / Ask Photos" and "Evidence Lens AI" across the 64-asset benchmark suite:

| Scenario / Task | Target Evidence to Surface | Ground Truth Context | Expected Legacy Failure Mode | Required Anti-Gravity MVP Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Test Case 1: Unresolved Stone Yard Task** | Red wax pencil marking: LOT-GR-408 / SL-14 on rough stone face with steel pocket rule. | Late May / Early June 2024; Nagarjuna Sagar industrial yard. | Returns "No results" for lot code; timeline drowns in Himachal family holiday vacation photos (50.0% contamination). | Auto-filters family photos; surfaces stone slab in <50ms; dynamically crops thumbnail onto red wax code LOT-GR-408 (0% contamination). |
| **Test Case 2: Structural Plumbing Offset** | Black marker on red wire-cut brick: OFFSET 150mm -> VP 08/11 next to yellow tape measure and grey PVC pipe. | Nov 8, 2025; Jubilee Hills Villa 42 site inspection. | "measuring tape pipe" surfaces 10 items including living room curtain measurement and child's hand (30.0% contamination). | Work partition isolates site media; inline badge displays OFFSET 150mm; zero domestic false positives (0% contamination). |
| **Test Case 3: Municipal Lab Certificate** | Third-party compressive cube test report: Grade M35, 41.2 N/mm², blue circular lab seal. | August 18, 2025; Madhapur commercial studio file. | White-paper camouflage: indistinguishable grid of invoices, medical prescriptions, and Aadhaar cards (55.5% contamination). | Substrate filter isolates "A4 / Stamped Document"; badge highlights M35 & laboratory seal without modal click (0% contamination). |

## 5. Technical Deliverables Expected from Anti-Gravity

* **Deployable Web Prototype:** An interactive, single-page application (Streamlit or Next.js / React) populated with the 64-asset benchmark dataset (`benchmark_assets.json`).
* **Dual-Mode Toggle Engine:**
  * **Mode A (The Baseline):** Simulates standard conversational search (6–8s latency spinner, conversational text bubbles, horizontal carousel, 30–55% domestic false-positive pollution).
  * **Mode B (Evidence Lens):** Executes instant partition filtering, non-planar OCR badge overlays, and dynamic evidence bounding-box cropping.
* **Live Metric Instrumentation HUD:** Real-time metrics bar comparing:
  * **Retrieval Time-to-Evidence:** Target <3.0s (vs. >180s / abandonment baseline).
  * **Domain Contamination Rate:** Target 0.0% (vs. 30–55% baseline).
  * **Clicks to Verification:** Target 0 clicks via dynamic thumbnail badges (vs. 8+ clicks baseline).
