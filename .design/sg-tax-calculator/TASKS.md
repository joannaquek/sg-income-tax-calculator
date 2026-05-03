# Build Tasks: SG Income Tax Calculator Redesign

Generated from: `.design/sg-tax-calculator/DESIGN_BRIEF.md`
Date: 2 May 2026

Existing codebase: single self-contained HTML file (`sg-income-tax-calculator-ya2026.html`, 1279 lines). All tax computation logic (`TAX_CONFIG`, `computePerson`, `applyCap`, `ptrTotal`, etc.) is correct and reusable. The redesign replaces CSS + HTML structure + stepper logic. JS computation functions are carried forward unchanged.

---

## Foundation

- [x] **1. Apply design tokens**: Replace the existing `:root` CSS variables with the full token system from `DESIGN_TOKENS.css`. Wire up `[data-theme="dark"]` and `@media (prefers-color-scheme: dark)` support. Add `prefers-reduced-motion`. Keep DM Sans + JetBrains Mono font imports. _Modifies: existing `:root` block. Establishes: Scandinavian aesthetic baseline (warm off-white, charcoal text, teal accent, soft shadows, rounded corners)._

- [x] **2. Theme toggle + persistence**: Add a sun/moon toggle button in the header. On click: set `data-theme` attribute on `<html>`, save preference to `localStorage`. On load: read `localStorage`, fall back to system preference. _New component. Depends on: Task 1 tokens._

- [x] **3. Page shell + header**: Rebuild the `<header>` and `.wrap` container. Header includes: title ("Singapore Income Tax Calculator"), subtitle ("YA 2026 · Income earned in 2025"), IRAS link, and theme toggle (top-right). Max-width `720px` centered. Warm background. _Modifies: existing header/wrap._

## Core UI

- [x] **4. Progress bar (4 steps)**: Replace 8-pill stepper with a horizontal 4-step progress bar. Steps: "You & Income", "Family", "Reliefs", "Results". Mobile: numbers only (no labels). Tablet+: abbreviated labels. Completed steps get checkmark + clickable. Current step highlighted with teal. Sticky on mobile (top). _Modifies: existing `.stepper` + `STEP_LABELS` array. Reduce from 8 to 4 steps._

- [x] **5. Step 1 — You & Income**: Single card. Fields: gross employment income (large, with `$` prefix), age, citizenship (select), gender (select). Tax resident checkbox (default checked). Inline live tax preview ("Estimated tax: ~$X") that updates on input change — computed using `taxResidentProgressive()` on raw income minus estimated CPF. Collapsible "Advanced" section: disability toggle, CPF override. _Modifies: existing step 0. Merges: none. New: live preview, collapsible advanced, `$` prefix formatting._

- [x] **6. Step 2 — Family & Dependants**: Single card with conditional sections. Top: married toggle. If married → spouse section (income, age, disability, husband NSman checkbox). Children section: "Add child" button, sub-cards with DOB, SG citizen, disability, qualifying checkboxes. Show child order ("1st", "2nd") from DOB sort. Parents section: "Add dependant" button (max 2), sub-cards with age, income, living arrangement, disability. Sharing sliders: QCR %, PTR %, Parent Relief %. Grandparent Caregiver checkbox (visible only for married working mothers). Hide sharing controls + spouse section for single users. _Modifies: merges old steps 1, 2, 3, 6 into one. Complex conditional visibility._

- [x] **7. Step 3 — Reliefs & Contributions**: Split into two zones. Zone A (read-only): auto-granted reliefs computed from Steps 1-2 — Earned Income Relief, CPF Relief, Spouse Relief, QCR, WMCR, NSman Wife — shown as checked items with amounts. Zone B (editable): SRS contribution, CPF cash top-up (self + family), Life Insurance, Sibling Disability checkbox, NSman self tier dropdown, NSman parent checkbox. Relief cap progress bar at top showing total vs $80k (green → amber → red). Collapsible "Spouse reliefs" section for comparison data (spouse SRS, spouse CPF override). _Modifies: merges old steps 4, 5. New: auto-granted zone, relief cap progress bar._

- [x] **8. Step 4 — Results & Optimizer**: Full results view. Hero number: net tax payable (large, centered, mono font, green if ≤$200, neutral otherwise). Tax breakdown table: income → reliefs (itemized, with partial-cap indicators) → chargeable income → gross tax → PTR → rebate → net tax. Relief cap callout if hit (amber, with wasted amounts). Optimization suggestion cards (not bullets): each card has title, dollar savings, brief explanation (SRS opportunity, CPF top-up, QCR transfer). Spouse results (conditional second column/card). Household comparison grid: 3 cards for 0%/50%/100% QCR split, best highlighted. _Modifies: merges old steps 7 + optimizer. New: optimization cards, relief cap callout upgrade._

## Interactions & States

- [x] **9. Step navigation + validation**: Wire Next/Back buttons to the 4-step model. "Next" on step 4 becomes "Recalculate". Progress bar steps are clickable to jump. Animate step transitions (fade or slide, using token durations). Back button hidden on step 1. Mobile: sticky bottom bar for Next/Back with safe-area padding. _Modifies: existing `currentStep` / `updateStep()` logic. Reduce `STEP_LABELS` from 8→4._

- [x] **10. Copy summary to clipboard**: Button on Step 4 ("Copy summary"). On click: build a plain-text formatted breakdown (income, reliefs, tax, suggestions) and copy to clipboard via `navigator.clipboard.writeText()`. Show brief toast notification "Copied!" that auto-dismisses after 2 seconds. _New component + new function._

- [x] **11. Collapsible / accordion sections**: Implement expand/collapse for "Advanced" (Step 1), "Spouse reliefs" (Step 3), and "Tax rules JSON" (footer). Click header → toggle body with smooth height animation. Chevron icon rotates. Default collapsed. _New pattern. Applied to 3 locations._

## Responsive & Polish

- [x] **12. Mobile layout (375px)**: Single column throughout. Progress bar: sticky top, numbers only. Input fields full-width. Spouse comparison stacks vertically. Results table horizontally scrollable. Copy button full-width. Next/Back sticky bottom bar. Touch targets ≥ 44px. Body text ≥ 16px (prevents iOS zoom). _Modifies: all steps. Mobile-first rewrite of layout CSS._

- [x] **13. Tablet + desktop (768px / 1024px+)**: Two-column grid for input fields (`.grid-2`). Progress bar shows labels. Spouse comparison side-by-side. Results table full-width, no scroll. Comfortable whitespace at max-width 720px. _Modifies: media query breakpoints._

- [x] **14. Print stylesheet**: `@media print` rules. Hide: progress bar, navigation buttons, theme toggle, collapsible toggles, copy button. Show: all sections expanded, all results visible. Clean black-on-white rendering. Page break before results. _New._

- [x] **15. Accessibility pass**: Semantic HTML (`<form>`, `<fieldset>`, `<legend>` for each step, `<label>` on all inputs). ARIA labels on icon buttons (theme toggle, copy). Focus ring using `--shadow-focus` token. Tab order follows visual order. Contrast check: all text/bg combinations meet WCAG 2.1 AA (4.5:1). Color-blind safe: relief cap uses bar + text + icon, not color alone. _Modifies: all HTML elements._

## Review

- [ ] **16. Design review**: Run `/design-review` against the brief. Check: Scandinavian aesthetic applied, mobile-first layout, light/dark mode working, relief cap visualization, optimization cards, copy-to-clipboard, print output.
