# Git Chronoscope - GUI Enhancement Proposal

## 1. Executive Summary

This proposal outlines a comprehensive redesign of the Git Chronoscope web interface (`src/web_app.py`, `templates/index.html`). The goal is to transition from the current basic utility look to a **"Professional Dashboard"** aesthetic, similar to developer tools like GitHub, Vercel, or Linear.

The new design will prioritize information density, clear hierarchy, and sophisticated interactions, making the tool feel like a polished software product rather than a simple script wrapper.

## 2. Visual Design System

### 2.1. Aesthetic Theme: "Dark Data-Dense"
We will adopt a refined dark theme that uses subtle contrast rather than stark black/white to define hierarchy.

*   **Backgrounds:** Deep blue-grays (Slate/Zinc) instead of pure black.
*   **Borders:** Thin, subtle borders to define grid areas (1px solid `rgba(255,255,255,0.1)`).
*   **Typography:** Inter or system sans-serif (San Francisco/Segoe UI). Small, legible font sizes (13px-14px for data, 16px for headings).
*   **Accents:** A single primary color (e.g., Indigo or Blue) used sparingly for actions. Status colors (Green/Red/Amber) for job states.

### 2.2. Color Palette (Tailwind-aligned)
*   **Base/Bg:** `bg-slate-950` (Main), `bg-slate-900` (Cards/Panels).
*   **Surface:** `bg-slate-800` (Inputs, Hover states).
*   **Borders:** `border-slate-800` (Subtle), `border-slate-700` (Active).
*   **Text:** `text-slate-200` (Primary), `text-slate-400` (Secondary/Labels).
*   **Primary:** `blue-600` (Buttons), `blue-500` (Focus rings).

### 2.3. Typography
*   **Headings:** semibold, tracking-tight.
*   **Labels:** uppercase, text-xs, tracking-wider, text-slate-500.
*   **Data:** monospaced for file paths, hashes, and IDs.

## 3. Technical Architecture

To achieve the "sophisticated interactions" and "polished feel" without introducing a heavy Node.js build chain, we will use a **Modern Lightweight Stack**:

1.  **Tailwind CSS (CDN):** For utility-first styling. This allows rapid development of complex "data-dense" grids without writing hundreds of lines of custom CSS.
2.  **Alpine.js (CDN/Vendor):** For reactive state management. This replaces the vanilla `document.getElementById` spaghetti code with declarative data binding (`x-data`, `x-bind`, `x-model`).
3.  **Flask (Existing):** Remains as the backend, serving the static HTML and API.

**Why this stack?**
*   **Zero Build Step:** No `npm install` or webpack required for the end user.
*   **Responsive:** Tailwind handles mobile/tablet layouts natively.
*   **Interactive:** Alpine.js provides smooth transitions and instant UI updates.

## 4. UI Layout & Component Specification

The interface will move away from a single centered column to a **Two-Column Dashboard Layout**.

### 4.1. App Shell
*   **Sidebar (Left, 250px):**
    *   **Logo/Header:** "Git Chronoscope" with a subtle icon.
    *   **Job History List:** A vertical list of recent jobs, showing status icons and timestamps. Clicking a job loads its details.
    *   **Footer:** Version info and links.
*   **Main Content Area (Right, Flex-grow):**
    *   **Top Bar:** Breadcrumbs or Page Title (e.g., "New Generation").
    *   **Content Grid:** The main configuration and preview area.

### 4.2. Configuration Panel (Data-Dense Grid)
Instead of a long vertical form, we use a structured grid to group related settings.

*   **Repository Card (Full Width):**
    *   Input group for `Repo Path` with a "Load Branches" action integrated inside the input grouping (like a search bar).
*   **Settings Grid (2 Columns):**
    *   **Visuals:** Resolution, FPS, Colors (with live circular swatches).
    *   **Scope:** Branch selector, Email privacy toggle.
*   **Preview Card (Right/Bottom):**
    *   A persistent preview area that updates when "Preview" is clicked, rather than a modal.

### 4.3. Job Queue & Status
*   **Progress Bar:** Moved to the bottom of the active job card, thin and animated (pulsing).
*   **Status Indicators:** specific badges (`badge-success`, `badge-running`) with concise text.

## 5. Interaction Design

### 5.1. Transitions
*   **Page Loads:** Content fades in slightly (`x-transition:enter`).
*   **Panel Toggles:** Smooth height expansion for "Custom Resolution" or "Advanced Settings".
*   **Hover States:** Subtle brightness lift on cards and inputs.

### 5.2. Reactive Feedback
*   **Input Validation:** Real-time checking (e.g., if Repo Path is empty, the "Load Branches" button is dimmed).
*   **Branch Loading:** The input shows a spinner *inside* the right edge while fetching.

## 6. Implementation Roadmap

### Phase 1: Setup & Layout
1.  Update `templates/index.html` to include Tailwind CSS and Alpine.js via CDN.
2.  Refactor the HTML structure into the Sidebar/Main Layout.
3.  Implement the "Dark Data-Dense" color theme using Tailwind classes.

### Phase 2: Reactivity with Alpine.js
1.  Migrate `static/js/app.js` logic into Alpine `x-data` components.
    *   `jobStore`: Manages the list of jobs.
    *   `configForm`: Manages the form state and two-way binding.
2.  Implement the "Live Preview" logic (fetching the image and displaying it in the UI).

### Phase 3: Polish & Animation
1.  Add transition classes for all state changes (loading spinners, success messages).
2.  Refine the typography and spacing (padding, gaps) to match the "Linear-like" aesthetic.
3.  Test responsiveness (Stack columns on mobile).

### Phase 4: Backend Tweaks (Optional)
1.  Add a `GET /api/system/info` to display version/status in the sidebar.

## 7. Mockup Description

**Sidebar:**
```
+------------------+
| 🎬 Chronoscope   |
+------------------+
| RECENT JOBS      |
| • my-repo (Success)|
| • other-pr (Run...) |
|                  |
|                  |
+------------------+
```

**Main Area:**
```
+------------------------------------------+
|  Configure Time-lapse                    |
+------------------------------------------+
|  REPO PATH                               |
|  [ /path/to/repo       ] [ Load Branch ] |
+----------------------+-------------------+
|  SETTINGS            |  PREVIEW          |
|  [Format v] [FPS v]  |                   |
|  [Color  ] [Res v]   |  [ IMAGE RENDER ] |
|  [ ] Hide Emails     |                   |
|                      |                   |
+----------------------+-------------------+
|  [ GENERATE VIDEO ]                      |
+------------------------------------------+
```
