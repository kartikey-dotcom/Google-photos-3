# Phase-Wise Implementation Plan: Anti-Gravity MVP Engine

This document outlines the step-by-step implementation plan for the **Anti-Gravity MVP Engine ("Evidence Lens")**, derived from the `problemStatement.md` requirements and the `architecture.md` technical design.

---

## Phase 1: Foundation & Baseline Setup (Weeks 1-2)
**Objective:** Establish the project repository, core architecture, and the legacy baseline (Mode A) to measure against.

* **Task 1.1: Project Initialization**
  * Scaffold a Next.js (React) application for the frontend.
  * Set up a Python/Node.js backend API with foundational endpoints.
  * Provision initial cloud storage buckets (AWS S3 / GCS) for media.
* **Task 1.2: Benchmark Dataset Integration**
  * Ingest the 64-Asset Pool (`benchmark_assets.json`) including ground truth context for the 3 core test cases (Stone Yard, Plumbing Offset, Lab Certificate).
* **Task 1.3: Mode A (Baseline) Implementation**
  * Build the legacy conversational search UI (chat paradigms).
  * Implement standard 1-inch thumbnails with single-row horizontal carousels.
  * Introduce simulated latency (6-8s) and intentional "contamination" behaviors for benchmarking.

## Phase 2: High-Density Canvas & Partitioning Pipeline (Weeks 3-4)
**Objective:** Implement the frontend triage canvas (Pillar 4) and the basic ingestion/partitioning logic (Pillar 1).

* **Task 2.1: High-Density Triage Canvas (Pillar 4)**
  * Build the 3-to-4 column vertical scroll layout optimized for mobile and desktop.
  * Implement persistent scroll indexing so grid states are retained upon returning from full-screen image views.
  * Build the Dual-Mode Toggle to switch between Mode A and Mode B (Evidence Lens).
* **Task 2.2: Autonomous Ingest Partitioning (Pillar 1)**
  * Set up the Scikit-learn DBSCAN clustering module on the backend to process EXIF metadata (GPS/Time).
  * Develop the Scene Prior classifier to identify architectural elements (rebar, scaffolding).
  * Build the Domain Quarantine Router to isolate the "Evidence / Site Stream" from personal/domestic photos.

## Phase 3: Vision Engine & Substrate OCR (Weeks 5-6)
**Objective:** Build the core AI pipeline to extract non-planar, low-fidelity text from challenging substrates (Pillar 2).

* **Task 3.1: Surface Classification**
  * Train or deploy an ML classifier to tag images with substrate attributes (e.g., Rough Stone, Wire-Cut Brick, A4 Document / Seal).
  * Store substrate tags in the Metadata Store / Vector DB for multi-modal facet narrowing.
* **Task 3.2: Substrate-Aware OCR Tuning**
  * Deploy fine-tuned Vision-Language Models (e.g., Florence-2 or TrOCR) specifically trained on non-standard handwriting (red wax grease pencil, chalk, spray paint).
  * Ensure accurate extraction of specific tokens like `LOT-GR-408` and `OFFSET 150mm`.

## Phase 4: Dynamic Telemetry & Badging (Weeks 7-8)
**Objective:** Connect OCR bounding box data to the UI for dynamic cropping and zero-click verification (Pillar 3).

* **Task 4.1: Bounding Box & Cropping Service**
  * Configure the OCR engine to return exact coordinate bounding boxes for detected evidence.
  * Develop the Attention-Crop generator to dynamically slice and center thumbnail previews directly onto the evidence marks.
* **Task 4.2: Inline Verification Badges**
  * Create high-contrast UI overlay pills to display extracted alphanumeric tokens directly on the Next.js grid thumbnails.

## Phase 5: Instrumentation, Testing & Optimization (Weeks 9-10)
**Objective:** Finalize the MVP by ensuring it meets the 10-second external evaluator criteria and the zero-contamination benchmarks.

* **Task 5.1: Live Metric Instrumentation HUD**
  * Implement the real-time metrics dashboard overlaying:
    * Retrieval Time-to-Evidence (Target: < 3.0s)
    * Domain Contamination Rate (Target: 0.0%)
    * Clicks to Verification (Target: 0)
* **Task 5.2: Ground-Truth Matrix Testing**
  * Execute Test Case 1: Unresolved Stone Yard Task (`LOT-GR-408`).
  * Execute Test Case 2: Structural Plumbing Offset (`OFFSET 150mm`).
  * Execute Test Case 3: Municipal Lab Certificate (`Grade M35`, Blue Seal).
* **Task 5.3: Performance Tuning**
  * Optimize database queries (PostgreSQL/Vector DB) and frontend rendering to ensure sub-100ms UI responsiveness for Mode B.
  * Finalize end-to-end bug bash and prepare the deployable web prototype.
