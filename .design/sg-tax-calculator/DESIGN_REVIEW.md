# Design Review: SG Income Tax Calculator v2

Reviewed against: `DESIGN_BRIEF.md`
Philosophy: Scandinavian (warmth + restraint)
Date: 2 May 2026

## Screenshots Captured

No automated screenshots captured — no browser MCP tool available. Manual visual verification recommended at:

| Breakpoint | Width x Height | What to check |
| ---------- | -------------- | ------------- |
| Mobile | 375 x 812 | Single column, sticky progress, sticky nav bar, no horizontal scroll |
| Tablet | 768 x 1024 | Two-column grids, progress labels visible |
| Desktop | 1280 x 800 | Max-width 720px centered, generous whitespace |
| Dark mode | All above | Toggle to dark, verify all elements switch cleanly |

## Summary

Strong implementation that faithfully follows the Scandinavian brief — warm off-white palette, teal accent, soft shadows, rounded corners, generous whitespace. The 4-step flow, live preview, relief cap bar, optimization cards, and copy-to-clipboard are all implemented. Three issues need fixing before shipping: input font-size will trigger iOS auto-zoom, semantic HTML landmarks are missing from the accessibility spec, and the grid breakpoint uses desktop-first media queries.

## Must Fix

1. **Input font-size triggers iOS auto-zoom**: `--fs-base` is `0.9375rem` (15px). On iOS Safari, any `<input>` or `<select>` with `font-size < 16px` triggers an automatic viewport zoom on focus, which is disorienting on mobile. The income field is fine (`--fs-lg`, 20px), but all other inputs will zoom.
   _Fix: Add a mobile override — `@media (max-width: 559px) { input, select { font-size: 16px; } }` — or bump `--fs-base` to `1rem`. The brief specifically requires "Body text >= 16px" on mobile._

2. **Missing semantic landmarks**: The brief's accessibility section calls for `<main>`, `<form>`, `<fieldset>`, `<legend>`, and associated `<label>` elements. Currently:
   - No `<main>` element — the `.wrap` div should be `<main>`
   - No `<form>` wrapping the input steps
   - No `<fieldset>` / `<legend>` grouping the step sections
   - The `<nav>` progress bar lacks `aria-label`
   _Fix: Wrap `.wrap` content in `<main>`. Add `aria-label="Step progress"` to the `<nav>`. Each step's section could use `role="group"` with `aria-labelledby` pointing to the h2._

3. **Inline `onclick` handler**: Line 277 uses `onclick="toggleCollapse(this)"` which leaks `toggleCollapse` to the global `window` scope and is fragile. The other collapsible (line 305) uses the same pattern.
   _Fix: Use `addEventListener` in the JS init block — query all `.collapsible-trigger` elements and attach click handlers programmatically, matching the pattern used for all other interactive elements._

## Should Fix

4. **Desktop-first grid breakpoint**: `.grid-2` uses `@media (max-width: 559px)` to stack columns. The brief specifies mobile-first design (min-width queries). Same issue for `.compare-grid`.
   _Fix: Default `.grid-2` to `grid-template-columns: 1fr`, then add `@media (min-width: 560px) { .grid-2 { grid-template-columns: 1fr 1fr } }`. Apply the same pattern to `.compare-grid`._

5. **Inline styles on section headings**: Multiple `<h3>` elements throughout Steps 1–3 have repeated inline styles like `style="font-size:var(--fs-sm);font-weight:var(--fw-semi);color:var(--color-text-secondary);margin-bottom:var(--space-5)"`. This violates DRY and makes future changes error-prone.
   _Fix: Create a `.section-heading` CSS class and apply it to all these h3 elements._

6. **No disabled button state**: The `.btn` class lacks a `:disabled` style. If the user is on a step where "Back" should be hidden (step 0), it uses `visibility: hidden` instead of disabled. No disabled styling exists for potential future validation.
   _Fix: Add `.btn:disabled { opacity: 0.4; cursor: not-allowed; pointer-events: none; }` to the token system._

7. **Checkbox touch target**: Checkboxes are `18x18px`. While the containing `.chk-row` is `min-height: 44px`, the actual checkbox hit area on some browsers is limited to the checkbox itself, not the row.
   _Fix: Ensure the `<label>` wraps or is clickable alongside the checkbox (already done with `for=` attributes on most checkboxes, but some dynamically-generated child/parent checkboxes lack `for`/`id` associations, meaning the label isn't clickable)._

8. **Cap bar doesn't include spouse/parent/child reliefs**: The `updateCapBar()` function on Step 3 only sums CPF, SRS, NSman, and voluntary reliefs — it omits Earned Income, Spouse, QCR, WMCR, Parent reliefs from the cap bar calculation. The bar will show a misleadingly low total.
   _Fix: Add the auto-granted reliefs (EIR, CPF, Spouse, QCR, WMCR, Parent, GCR) to the `updateCapBar()` total, matching the full set computed in `updateReliefsStep()`._

## Could Improve

9. **Replace emoji with inline SVG**: The theme toggle (☀️/🌙), copy button (📋), checkmarks (✓), chevrons (▶), and opt card icons (⚠/💡) use Unicode emoji. These render inconsistently across platforms (especially Windows vs macOS vs Android). Inline SVGs would be more reliable and styleable.

10. **Step transition animation**: Steps currently use `display: none` via `.hidden`. The brief mentions "Animate step transitions (fade or slide, using token durations)". A simple CSS fade using opacity + a brief delay would add polish without complexity.

11. **Hardcoded values in JS-generated HTML**: `style="margin-top:22px"` on line 492 (child checkbox alignment) is a magic number not from the spacing scale. `font-size:10px` on `.config-note` is also hardcoded.
    _Suggestion: Use `var(--space-7)` for the margin, `var(--fs-xs)` for the config note._

12. **Print stylesheet shows all hidden panels**: `@media print` sets `.hidden { display: block !important }` and `.step-panel { display: block !important }`. This means *all four steps* will print, including the form inputs. Most users printing would only want the results.
    _Suggestion: Use a more targeted print rule — only force-show `[data-step="3"]` (results) and hide the form steps._

13. **No "effective tax rate" display**: Users commonly want to know their effective tax rate as a percentage. This is a one-line addition to the results hero (`netTax / income * 100`).

14. **Live preview in Step 1 doesn't account for disability EIR**: `updateLivePreview()` hardcodes `earnedIncomeReliefAmount(age, false, inc)` — it ignores the disability checkbox. Minor since it's in the advanced section.

## What Works Well

- **Token system is comprehensive and consistent**: Every color, spacing value, shadow, radius, and font in the CSS references a custom property. Dark mode tokens feel intentional — not just an inversion. Shadows deepen, accent brightens, backgrounds warm properly.
- **4-step flow is a major UX improvement**: Collapsing 8 steps to 4 reduces cognitive load dramatically. The "Family & Dependants" merge of spouse + children + parents into one step with smart conditional visibility is well-executed.
- **Relief cap progress bar**: The green → amber → red bar on Step 3 with live updates as the user adjusts SRS/CPF/insurance is the kind of real-time feedback the brief asks for. Users will intuitively understand how close they are to the $80k cap.
- **Auto-granted reliefs zone**: Showing checkmarked reliefs computed from earlier steps (EIR, CPF, Spouse, QCR) in a read-only list is a clever design. It gives users confidence that the tool has understood their situation without requiring extra input.
- **Optimization suggestion cards**: Upgrading from generic bullet points to distinct amber cards with titles ("SRS opportunity", "CPF top-up opportunity") and dollar amounts is a significant clarity improvement over v1.
- **Household QCR comparison grid**: The 3-card comparison with "best" highlighted in teal is clean and immediately actionable. Users can see the dollar impact of shifting QCR allocation at a glance.
- **Copy-to-clipboard with toast**: Clean, functional. The plain-text format is share-friendly for WhatsApp/Telegram as intended.
- **Theme toggle with localStorage + system preference fallback**: The three-tier cascade (localStorage > system preference > default light) is correct and complete.
