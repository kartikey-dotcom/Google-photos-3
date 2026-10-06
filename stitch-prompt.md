# Google Stitch Frontend Design Prompt: Anti-Gravity MVP Engine

**Copy and paste the following prompt into Google Stitch to generate the UI design:**

---

## **Project Context & Objective**
I need a high-fidelity frontend UI design for a web application called **"Anti-Gravity: Evidence Lens (SiteLens Core)."** This is a professional-grade, AI-native media retrieval tool built for field engineers, architects, and project managers. Unlike consumer photo galleries (which are designed as nostalgic scrapbooks), this tool is a high-density, zero-latency physical evidence audit engine used in time-critical disputes on active job sites.

## **Aesthetic & Visual Identity**
* **Vibe:** Professional, utilitarian, high-stakes, data-dense, and highly responsive. Think of a cross between a Bloomberg Terminal, an IDE (like VS Code), and Google Photos, but entirely stripped of consumer "fluff".
* **Color Palette:** Clean, high-contrast technical UI. A sleek Dark Mode (slate/charcoal backgrounds with crisp neon/yellow accents for AI highlights) or a highly legible Light Mode with stark contrasting elements.
* **Typography:** Modern, highly legible sans-serif (e.g., Inter, Roboto Mono for data points) emphasizing scan-ability over decorative prose.

## **Core Layout Requirements**
The interface must be a Single Page Application layout encompassing the following core areas:

1. **Top Navigation / Header:**
   * A clean, telegraphic search bar (Input placeholder: *"e.g., LOT-GR-408, measuring tape, OFFSET 150mm"*). No chat interfaces or conversational prose.
   * **Dual-Mode Toggle:** A prominent, highly styled switch or segmented control toggling between **"Legacy Baseline"** and **"Evidence Lens"**.

2. **Live Metric Instrumentation HUD (Top Bar / Dashboard):**
   * A persistent, real-time metrics dashboard overlaying the grid with three key data points:
     * *Retrieval Time-to-Evidence* (e.g., `80ms` with a green indicator)
     * *Domain Contamination Rate* (e.g., `0.0%`)
     * *Clicks to Verification* (e.g., `0 clicks`)

3. **Sidebar (Facet Narrowing):**
   * A sleek filter panel for "Vision Facets".
   * Include checkboxes or pills for "Surface Classification" (e.g., *Rough Stone*, *Wire-Cut Brick*, *A4 Document / Seal*, *Timber Frame*).

4. **Main Content Area (High-Density Triage Canvas):**
   * **Layout:** A dense 3-to-4 column vertical scrolling grid utilizing 100% of vertical screen space. **Do not use horizontal single-row carousels.**
   * **Cards/Thumbnails:** The images must appear strictly utilitarian.

## **Specific Component Details (Crucial for the AI)**
* **Dynamic Evidence-Centered Cropping:** The thumbnails in the grid should appear "dynamically cropped" (zoomed-in) to focus on a specific piece of evidence (e.g., a handwritten wax pencil mark on a stone, or a chalk mark on concrete), rather than showing a wide, unreadable shot.
* **Inline Verification Badges (The "Wow" Factor):** On top of these cropped thumbnails, overlay high-contrast "pills" or badges containing alphanumeric text (e.g., `LOT-GR-408` or `OFFSET 150mm`). These badges should look like AI-extracted data points injected directly onto the image card, allowing the user to read the evidence without clicking into the image.

## **State Comparisons (Show two views if possible)**
1. **View A (Evidence Lens Active - Target Design):** Show the dense 4-column grid, the sidebar filters active, the HUD showing perfect metrics, and the thumbnails dynamically cropped with bright yellow/neon Verification Badges overlaid on the images. 
2. **View B (Legacy Baseline - What we are replacing):** Show a cluttered layout with a massive conversational chat bubble taking up 40% of the screen ("Here are some photos I found..."), a tiny single-row horizontal carousel of 1-inch uncropped thumbnails, and mixed personal photos (vacations/kids) alongside professional photos.

---
