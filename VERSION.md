# SG Income Tax Calculator — Version History

## Versioning Convention

- **Major** (v1, v2, v3): Significant UI/UX redesigns, new calculation engines, or architecture changes
- **Minor** (v2.1, v2.2): Feature additions, new fields, tooltip/copy/optimizer enhancements
- **Patch** (v2.1.1): Bug fixes, relief rate updates, typo corrections

**Rule: Never modify a released version file in-place. Always copy to a new version first.**

File naming: `sg-income-tax-calculator-v{version}.html`

Older versions live in `archive/`. Only the latest version stays in the main folder.

---

## Versions

### v1.0 — Original calculator
- **File**: `archive/sg-income-tax-calculator-ya2026.html`
- **Date**: 2 May 2026
- **Status**: Archived
- **Summary**: First build. Dark-only theme, 8-step stepper, all tax computation logic (TAX_CONFIG, computePerson, applyCap, PTR, progressive tax). Self-contained HTML. Full Singapore YA 2026 tax rules.
- **Features**: Progressive tax bands, 15+ reliefs, spouse comparison (3-way QCR grid), $80k cap with proportional scaling, optimization suggestions (bullet list), config JSON preview.

### v2.0 — Scandinavian redesign *(overwritten — no backup)*
- **Date**: 2 May 2026
- **Status**: Lost (was modified in-place before versioning was established)
- **Summary**: Complete UI rebuild: Scandinavian design tokens (warm off-white, teal accent, soft shadows), 4-step flow (collapsed from 8), light/dark mode with system preference + toggle, live tax preview on Step 1, relief cap progress bar, auto-granted reliefs zone, optimization suggestion cards, copy-to-clipboard with toast, print stylesheet, mobile-first responsive, accessibility pass (semantic landmarks, ARIA, focus rings).

### v2.1 — Design review fixes *(merged into v2, no separate file)*
- **Date**: 2 May 2026
- **Status**: Merged into v2.0 file (pre-versioning)
- **Changes**:
  - Fixed iOS auto-zoom: input font-size 16px on mobile
  - Added `<main>` landmark + `aria-label` on nav
  - Replaced inline `onclick` with `addEventListener`
  - Fixed cap bar to include all reliefs (was missing auto-granted)
  - Extracted inline h3 styles to `.section-heading` class
  - Flipped grid-2 to mobile-first `min-width` query
  - Added `.btn:disabled` state

### v2.2 — Tooltips, categorized breakdown, smart cap callouts
- **File**: `archive/sg-income-tax-calculator-v2.html`
- **Date**: 3 May 2026
- **Status**: Archived
- **Changes**:
  - **Tooltips**: `(?)` icon on every input field with plain-English explanations, caps, and calculation notes. Pure CSS (hover + focus), mobile-responsive positioning.
  - **Categorized relief breakdown**: Results table grouped into Personal Reliefs, Family Reliefs, Voluntary Contributions, Other Reliefs — each with subtotals.
  - **Effective tax rate**: New row in results showing net tax as % of income.
  - **Smart cap callout**: When reliefs exceed $80k, lists each partially-wasted relief with exact dollar amounts. Advises deferring voluntary contributions if they're being capped. Suggests spouse reallocation for married users.
  - **Copy function**: Updated to handle categorized table format with category headers.

### v2.3 — Theme slider, subtitle fix, donation relief
- **File**: `archive/sg-income-tax-calculator-v2.3.html`
- **Date**: 3 May 2026
- **Status**: Archived
- **Changes**:
  - **Theme toggle**: Replaced button with sun/moon slider toggle. Checkbox-based with animated thumb, active icon highlighting.
  - **Subtitle alignment**: Removed `max-width:44ch` constraint so "verify with IRAS" stays on one line.
  - **Donation relief**: New field in Reliefs step for donations to approved IPCs. 250% tax deduction (separate from $80k relief cap). Includes tooltip, results table row, optimizer suggestion card.

### v2.4 — Analytics (GA4 + Clarity)
- **File**: `archive/sg-income-tax-calculator-v2.4.html`
- **Date**: 3 May 2026
- **Status**: Archived
- **Changes**:
  - **Google Analytics 4**: Step funnel tracking, calculate_tax events (with income bracket, married status, children count, relief cap hit), theme toggle, copy summary, add child/parent.
  - **Microsoft Clarity**: Session recordings, heatmaps, rage click detection — no config needed beyond the script tag.
  - **Deployment**: GitHub Pages ready with `index.html` entry point.

### v2.5 — IRAS Pre-Filled Statement PDF upload
- **File**: `sg-income-tax-calculator-v2.5.html` / `index.html` *(current)*
- **Date**: 3 May 2026
- **Status**: Active (latest)
- **Changes**:
  - **PDF upload zone**: Drag-and-drop or click-to-upload before the stepper. Processes 100% client-side via PDF.js (lazily loaded, only when user triggers upload).
  - **Document mockup tooltip**: Visual mini-replica of the IRAS Pre-Filled Income and Deduction Statement with redacted fields, plus step-by-step instructions to find it on myTax Portal.
  - **Field extraction**: Parses Employment Income, CPF Relief, CPF Cash Top-up, Total Donations, number of qualifying children, and WMCR presence (to infer gender = Female).
  - **Smart child handling**: Detects pre/post Jan 2024 birth year from WMCR amounts (old % rates vs new fixed rates), sets placeholder DOBs accordingly with a warning to update.
  - **Success state**: Shows a card listing all extracted fields with values, YA note (e.g. "Pre-filled from YA 2025 — review for YA 2026"), and re-upload link.
  - **GA4 event**: `pdf_prefill` tracks extraction success, fields found, children count, WMCR presence.
  - **Privacy**: Prominent "processed locally, never uploaded" notice; PDF.js runs entirely in browser.

---

## Planned

### v3.0 — Singpass MyInfo integration
- **Spec**: `PHASE2_SINGPASS.md`
- **Status**: Parked
- **Summary**: Backend (Node.js) + Singpass OAuth flow to auto-fill income, CPF, children, marital status, NSman data. Requires GovTech onboarding.

---

## File inventory

| File | Version | Status |
|------|---------|--------|
| `archive/sg-income-tax-calculator-ya2026.html` | v1.0 | Archived |
| `archive/sg-income-tax-calculator-v2.html` | v2.2 | Archived |
| `archive/sg-income-tax-calculator-v2.3.html` | v2.3 | Archived |
| `archive/sg-income-tax-calculator-v2.4.html` | v2.4 | Archived |
| `sg-income-tax-calculator-v2.5.html` / `index.html` | v2.5 | Active (latest) |
| `PHASE2_SINGPASS.md` | — | Spec for v3.0 |
| `VERSION.md` | — | This file |
| `.design/sg-tax-calculator/` | — | Design artifacts (brief, IA, tokens, tasks, review) |
