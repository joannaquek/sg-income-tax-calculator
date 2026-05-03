# Information Architecture: SG Income Tax Calculator

## Site Map

Single-page application. No URL routing. All views are step panels within one HTML document.

- Calculator `/` (single page)
  - Step 1: You & Income
  - Step 2: Family & Dependants
  - Step 3: Reliefs & Contributions
  - Step 4: Results & Optimizer

## Navigation Model

- **Primary navigation**: Horizontal progress bar at the top with 4 numbered steps. Completed steps are clickable to jump back. Current step is highlighted. No labels on mobile (numbers only); abbreviated labels on tablet; full labels on desktop.
- **Secondary navigation**: Next / Back buttons at the bottom of each step card. "Next" is primary (filled). "Back" is ghost (outlined). On the final step, "Next" becomes "Recalculate" (re-runs computation with current inputs).
- **Utility navigation**: Theme toggle (light/dark) in the top-right corner. IRAS link in the footer. "Copy summary" button on the results step. Collapsible "Tax rules JSON" reference at the very bottom.
- **Mobile navigation**: Progress bar stays fixed/sticky at the top. Steps scroll naturally. Back/Next are sticky at the bottom within a safe-area-aware bar.

## Content Hierarchy

### Step 1: You & Income
1. **Gross employment income** — The single most important input. Large, prominent field. Currency-formatted.
2. **Age / citizenship / gender** — Three fields in a row. These drive auto-computation (CPF rate, Earned Income Relief tier, SRS cap, WMCR eligibility).
3. **Tax resident checkbox** — Defaults to checked. Unchecking disables all personal reliefs and shows a non-resident warning.
4. **Inline tax preview** — Below the inputs, a subtle live estimate: "Estimated tax before reliefs: ~$X". Updates as the user types. Hooks engagement before they even proceed.
5. **Advanced (collapsible)** — Disability earned income relief toggle, CPF override field. Hidden by default — most users won't need these.

### Step 2: Family & Dependants
1. **Marital status toggle** — Single prominent toggle. If "not married," the entire spouse and WMCR section collapses away.
2. **Spouse section (conditional)** — Spouse income, age, disability toggle. Spouse income determines Spouse Relief eligibility (≤$8k threshold shown inline). Husband NSman checkbox for Wife relief.
3. **Children section** — "Add child" button. Each child: DOB date picker, SG citizen checkbox, disability checkbox, qualifying checkbox. Show child order label ("1st child", "2nd child") based on DOB sort order.
4. **Parents / grandparents section** — "Add dependant" button. Each: age, income, living arrangement, disability. Max 2 note shown inline.
5. **Sharing controls** — QCR % share slider, PTR % share slider, Parent Relief % share slider. These are meaningful for married couples; collapse/hide for single users.
6. **Grandparent Caregiver Relief** — Checkbox, visible only if user is a married working mother.

### Step 3: Reliefs & Contributions
1. **Auto-granted reliefs summary** — Read-only display of reliefs already computed from Steps 1-2: Earned Income Relief, CPF Employee Relief, Spouse Relief, QCR, WMCR, NSman. Shows amounts with checkmarks. User can see what the tool already knows.
2. **Voluntary contributions** — SRS contribution field, CPF cash top-up (self + family) fields. These are the actionable levers for optimization.
3. **Other reliefs** — Life Insurance relief field, Sibling Disability checkbox, NSman self tier dropdown, NSman parent checkbox.
4. **Relief cap meter** — A progress bar showing total reliefs vs. $80,000 cap. Updates live as user adjusts voluntary contributions. Color shifts from green → amber → red as it approaches/exceeds the cap.
5. **Spouse reliefs (conditional, collapsible)** — If married with spouse income >0: spouse SRS, spouse CPF override, spouse disability. For the comparison engine.

### Step 4: Results & Optimizer
1. **Net tax hero number** — Large, centered, prominent. Color-coded: green if zero or very low, neutral otherwise. This is what people screenshot.
2. **Tax computation breakdown** — Clean table: income → reliefs (itemized) → cap → chargeable income → gross tax → PTR → rebate → net tax. Each relief line shows the granted amount, with a subtle indicator if partially capped.
3. **Relief cap status** — If over cap: amber callout with the dollar amount wasted and which reliefs were proportionally reduced.
4. **Optimization suggestions** — Individual cards (not a bullet list). Each card: title, dollar savings amount, brief explanation. Examples: "Contribute $X to SRS → save $Y", "Transfer QCR to spouse → household saves $Z".
5. **Spouse results (conditional)** — If spouse data entered: spouse's tax breakdown in a second column/card.
6. **Household comparison** — Grid of 3 cards comparing QCR allocation scenarios (0% / 50% / 100% to you). Best option highlighted.
7. **Copy summary button** — Fixed at the bottom of results. Copies a formatted text block to clipboard.

## User Flows

### Flow 1: Quick Solo Estimate (80% of users)
1. User opens link (likely on mobile, shared via WhatsApp).
2. Step 1: Enters income, age is pre-filled at 35, sees instant tax preview.
3. Taps "Next". Step 2: Leaves "not married" (default), skips children/parents.
4. Taps "Next". Step 3: Sees auto-granted reliefs (Earned Income, CPF). Optionally enters SRS.
5. Taps "Next". Step 4: Sees net tax. Screenshots it. Done in <60 seconds.

### Flow 2: Married Couple Optimization
1. User opens on desktop or tablet.
2. Step 1: Enters income, age, gender.
3. Step 2: Checks "married". Enters spouse income, children DOBs, parent details. Adjusts QCR/PTR sharing %.
4. Step 3: Enters SRS for self and spouse. Watches relief cap meter.
5. Step 4: Reviews household comparison grid. Adjusts QCR % back on Step 2 based on optimizer suggestion. Recalculates.
6. Copies summary. Shares with spouse.

### Flow 3: Returning User (annual re-check)
1. User opens saved bookmark.
2. All fields are blank (no localStorage persistence in v1 — out of scope).
3. Fills in updated income for new year.
4. Checks results against last year's Notice of Assessment.

## Naming Conventions

| Concept | Label in UI | Notes |
|---------|-------------|-------|
| Gross salary + bonus | "Gross employment income" | IRAS terminology. Not "salary" alone — includes bonus, commission. |
| Chargeable income | "Chargeable income" | Keep IRAS term — users see it on their NOA. |
| Relief | "Relief" (not "deduction") | IRAS uses "relief" for personal items. "Deduction" is for expenses/donations. |
| Year of Assessment | "YA 2026" | Always abbreviated. Show "(income earned in 2025)" as a subtitle. |
| Net tax | "Net tax payable" | What you actually owe after all rebates. |
| PTR | "Parenthood Tax Rebate" | Spell out on first use, abbreviate after. |
| WMCR | "Working Mother's Child Relief" | Spell out on first use. |
| QCR | "Qualifying Child Relief" | Spell out on first use. |
| Relief cap | "Personal relief cap" | Not "overall cap" — too vague. |

## Component Reuse Map

| Component | Used in | Behavior differences |
|-----------|---------|---------------------|
| Step card (`.card`) | Steps 1-4 | Same container. Step 4 is wider on desktop (full-width results). |
| Input field | Steps 1-3 | Currency fields get `$` prefix and thousand separators. Number fields get increment buttons. |
| Checkbox row | Steps 1-3 | Same styling everywhere. |
| Add/remove block | Step 2 (children, parents) | Same pattern: add button, numbered sub-cards, remove button per block. |
| Progress bar | All steps | Fixed/sticky on mobile. Changes state per step. |
| Callout box | Steps 3-4 | Step 3: relief cap warning. Step 4: optimization suggestions. Same visual container, different accent color. |
| Summary table | Step 4 | Used for both "You" and "Spouse" breakdowns. |
| Compare card | Step 4 | Grid of 3. Highlight variant for best option. |

## Content Growth Plan

This is a single-purpose calculator with fixed content structure. Growth vectors:

- **YA versioning**: Each year, update `TAX_CONFIG`. The IA does not change — only the data values. A "YA selector" dropdown could be added in the future (header utility nav) to compare across years.
- **Additional income types**: Rental, trade, and self-employed income could be added as optional fields in Step 1 behind a collapsible "Other income" section. The IA accommodates this without restructuring.
- **More relief types**: New reliefs announced in Budget can be added to Step 3 without changing the step structure.

## URL Strategy

Single-page app — no URL routing needed. Future consideration:

- Hash-based step anchors (`#step-1`, `#step-2`) for direct linking and browser back button support.
- Query parameter pre-fill (`?income=85000&age=35`) for shareable pre-configured links.

Neither is in scope for v1 but the IA supports both without restructuring.
