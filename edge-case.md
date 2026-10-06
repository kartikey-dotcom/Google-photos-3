# Edge Cases & Mitigation Strategies: Anti-Gravity MVP Engine

This document outlines potential edge cases across the four AI-Native pillars of the "Evidence Lens" (SiteLens Core) MVP and proposes technical and UX mitigation strategies to handle them gracefully.

---

## 1. Autonomous Ingest Partitioning (Domain Quarantine)

| Edge Case | Description | Proposed Mitigation |
| :--- | :--- | :--- |
| **Missing EXIF Metadata** | Images received via messaging apps (e.g., WhatsApp, Slack) often have stripped GPS/Timestamp data, breaking the DBSCAN clustering algorithm. | **Fallback to Scene Prior & OCR:** If EXIF is missing, rely entirely on the visual scene classifier (e.g., detecting scaffolding, wire-cut brick) and any detected technical OCR tokens to classify the image into the Site Stream. |
| **Mixed-Use GPS Coordinates** | The user works from home, or lives temporarily on/near the active construction site, causing domestic and professional GPS clusters to overlap perfectly. | **Strict Scene Prior Weighting:** Decrease the weight of spatial clustering and increase the strictness of the Scene Prior classifier. A photo must visually look like a utility/site photo (e.g., exposed rebar, blueprints) to be routed to Evidence, despite the location. |
| **Historical Tourism (False Positives)** | The user takes personal vacation photos at a historical ruin (masonry, stone). The Scene Prior classifier might falsely flag this as a construction site. | **Human-in-the-Loop Toggle:** Allow users to easily swipe/mark an image as "Not Work," which feeds back into the clustering engine to correct the user's specific embeddings. |

## 2. Substrate-Aware Visual OCR (Text Extraction)

| Edge Case | Description | Proposed Mitigation |
| :--- | :--- | :--- |
| **Obscured or Degraded Markings** | Wax pencil or chalk is partially rubbed off, covered in mud splatter, or physically chipped away from the stone. | **Fuzzy Token Matching:** Use Levenshtein distance and wildcard search capabilities in the Vector DB/Search Engine (e.g., matching `L?T-GR-408` if the `O` is obscured). |
| **Alphanumeric Ambiguity** | Low-fidelity handwriting makes characters indistinguishable (e.g., '0' vs 'O', '5' vs 'S', '1' vs 'I' or '7'). | **Contextual VLM Interpretation:** Leverage the Vision-Language Model to look at the format. If the pattern is typically `LOT-[Letters]-[Numbers]`, the model restricts character predictions based on the expected regex pattern. |
| **Extreme Lighting Conditions** | Harsh direct sunlight causing blown-out highlights on concrete, or deep shadows obscuring text in a trench. | **Pre-Processing Pipeline:** Apply adaptive histogram equalization (CLAHE) or contrast stretching using OpenCV before passing the image to the OCR model. |
| **Multi-Language or Mixed Scripts** | Site workers write annotations in a local language (e.g., Hindi, Telugu) next to English alphanumeric codes (like M35 or OFFSET). | **Multilingual OCR Fallback:** Ensure the VLM is capable of identifying and extracting primary English utility tokens even when surrounded by unsupported scripts, discarding the irrelevant text. |

## 3. Dynamic Telemetry & Cropping (Thumbnail Engine)

| Edge Case | Description | Proposed Mitigation |
| :--- | :--- | :--- |
| **Multiple Evidence Marks** | A single wide-shot photo captures 4 different stone slabs, each with a different LOT code. | **Multi-Badge & Smart Zoom:** The thumbnail renders multiple Verification Badges. When a specific query (e.g., `SL-14`) is searched, the dynamic crop prioritizes centering *only* the searched bounding box. |
| **Extreme Distance (Micro Bounding Box)** | The user took a photo from 30 feet away. The dynamic crop zooms in so far that the thumbnail becomes heavily pixelated and unreadable. | **Maximum Zoom Threshold:** Implement a zoom limit (e.g., max 300% crop). If the bounding box requires more zoom, crop to the threshold and rely on the high-contrast Inline Verification Badge to communicate the extracted text. |
| **Full-Width Bounding Box** | The text spans the entire width of the image (e.g., a macro shot of a document), making a "crop" redundant. | **Aspect-Ratio Respect:** If the bounding box covers >80% of the image, bypass the Attention-Crop generator and render the standard center-crop thumbnail to preserve context. |

## 4. High-Density Triage Canvas (UI/UX)

| Edge Case | Description | Proposed Mitigation |
| :--- | :--- | :--- |
| **Mobile Memory Exhaustion** | Loading a 4-column dense grid with hundreds of dynamically cropped thumbnail blobs causes the mobile browser to crash. | **Virtualization/Recycler Windowing:** Implement UI virtualization (e.g., `react-window` or `react-virtuoso`). Only render the DOM nodes for thumbnails currently visible in the viewport plus a small buffer. |
| **Network Latency / Drop-Outs** | Field engineers on remote construction sites have edge/3G network connections, stalling thumbnail retrieval. | **Aggressive Local Caching & Skeleton States:** Cache Evidence Stream thumbnails aggressively via Service Workers (PWA). Render structural skeleton grids immediately so the user can still interact with cached text metadata and badges while images stream in. |
