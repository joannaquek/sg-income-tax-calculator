# Design Brief: Singapore Income Tax Calculator

## Problem

Filing income tax in Singapore is anxiety-inducing for regular salaried workers. IRAS provides Excel spreadsheets and dense documentation, but most people don't know which of the 15+ reliefs they qualify for, whether they're hitting the $80,000 relief cap, or how to split reliefs with a spouse to minimize household tax. The result: people either overpay or miss reliefs they're entitled to, and they never feel confident their filing is right.

## Solution

A clean, mobile-friendly calculator that walks users through their situation in a few simple steps, computes their estimated tax, and — critically — tells them what they could do differently. It should feel like a knowledgeable friend reviewing your tax situation over coffee: approachable, clear, and actionable. Not a government form. Not an accountant's spreadsheet.

## Experience Principles

1. **Confidence over completeness** — Show the user exactly what they need to know, in language they understand. Hide complexity behind progressive disclosure. The first result should arrive in under 60 seconds with minimal input.
2. **Guidance over data entry** — The tool should feel like it's advising you, not interrogating you. Pre-compute what can be computed (CPF from salary + age). Explain each relief in plain English. Surface optimization suggestions proactively.
3. **Mobile-first, share-ready** — The primary distribution is a WhatsApp/Telegram link. The interface must work flawlessly at 375px. Results must be screenshot-friendly and copy-pasteable.

## Aesthetic Direction

- **Philosophy**: Scandinavian — warmth plus restraint. Rounded corners, generous whitespace, soft shadows, accessible by default.
- **Tone**: Trustworthy, calm, approachable. Like a modern fintech app, not a government portal.
- **Reference points**: Endowus, Syfe, StashAway (SG fintech). Wise (clean financial UI). Apple Calculator (simplicity).
- **Anti-references**: IRAS website (dense, bureaucratic). Bloomberg terminal (information overload). Dark hacker aesthetic (alienating for general public). Excel spreadsheets.

## Existing Patterns

This is a redesign of an existing self-contained HTML file. Current state:

- **Typography**: DM Sans (body), JetBrains Mono (numbers). Keep both — they work well together.
- **Colors**: Dark-only palette with teal accent (`#38b2ac`). Redesign will add a light mode as default, with dark mode via `prefers-color-scheme` + manual toggle. Teal accent can carry forward.
- **Spacing**: Ad-hoc pixel values. Redesign will introduce a systematic spacing scale.
- **Components**: Cards, stepper pills, grid-2 layout, input fields, checkboxes, buttons (primary/ghost), results table, callout boxes, compare cards. All inline CSS — no external framework.
- **Architecture**: Self-contained HTML. All tax logic in a `TAX_CONFIG` JSON object. No build step, no dependencies beyond Google Fonts CDN.

## Component Inventory

| Component | Status | Notes |
| --- | --- | --- |
| Progress stepper | Modify | Collapse from 8 pills to 4 steps. Horizontal bar on mobile, not wrapping pills. |
| Income input card | Modify | Add currency formatting, inline help text for each field. |
| Checkbox/toggle group | Modify | Restyle for Scandinavian warmth. Larger touch targets (44px min). |
| Child/parent entry block | Modify | Dashed-border blocks → clean sub-cards with add/remove. |
| Results hero (net tax) | Modify | Larger, more celebratory. Color-coded (green if low/zero, neutral otherwise). |
| Relief breakdown table | Modify | Add relief cap progress bar above table. Cleaner row styling. |
| Optimization callout | Modify | Upgrade from generic warning box to actionable suggestion cards with savings amounts. |
| Spouse comparison grid | Modify | Side-by-side cards with clear "best option" highlight. |
| Theme toggle | New | Sun/moon icon button for light/dark mode switching. |
| Copy summary button | New | Copies a plain-text tax breakdown to clipboard for sharing. |
| Print stylesheet | New | `@media print` rules for clean paper output. |
| Collapsible sections | New | Accordion-style expand/collapse within each step for optional fields. |

## Key Interactions

1. **Step navigation**: User progresses through 4 steps via Next/Back buttons. Steps are also clickable in the progress bar to jump. Completed steps show a checkmark.
2. **Real-time estimates**: As the user fills in income on Step 1, an inline preview shows "Estimated tax: ~$X" before they even proceed. This hooks engagement.
3. **Relief auto-detection**: Based on age, gender, marital status, and citizenship entered in Steps 1-2, the tool auto-checks applicable reliefs and greys out ineligible ones in Step 3.
4. **Relief cap warning**: If total reliefs approach or exceed $80k, a progress bar fills and turns amber/red with a clear message.
5. **Optimization cards**: On the Results step, actionable cards say "You could save $X by contributing $Y to SRS" with a clear call to action.
6. **Copy to clipboard**: Single button copies a formatted text summary. Brief toast notification confirms "Copied!"
7. **Theme toggle**: Smooth transition between light/dark. Persists choice in `localStorage`.

## Responsive Behavior

- **Mobile (375px)**: Single column. Progress bar is horizontal with step numbers only (no labels). Input fields stack. Results table scrolls horizontally if needed. Spouse comparison stacks vertically. "Copy summary" is full-width at bottom.
- **Tablet (768px)**: Two-column grid for input fields. Progress bar shows abbreviated labels. Results and comparison side by side.
- **Desktop (1024px+)**: Max-width 720px centered. Full labels on progress bar. All two-column grids active. Comfortable whitespace.

## Accessibility Requirements

- WCAG 2.1 AA contrast ratios (4.5:1 for text, 3:1 for large text and UI components) in both light and dark modes.
- All form inputs have visible labels (not placeholder-only).
- Keyboard navigation through all steps and form controls. Focus ring visible on all interactive elements.
- Screen reader: semantic HTML (`<form>`, `<fieldset>`, `<legend>`, `<label>`, `<table>` with headers). ARIA labels on icon-only buttons (theme toggle, copy).
- Touch targets minimum 44x44px on mobile.
- No information conveyed by color alone (relief cap uses bar + text + icon).

## Out of Scope

- Singpass/MyInfo API integration (future phase, requires backend).
- SRS account balance auto-pull (no API available).
- Multi-year comparison or historical YA data.
- PDF export (copy-to-clipboard and print CSS are sufficient).
- User accounts, saving, or server-side storage.
- Rental income, trade income, or self-employed calculations (employment income only for v1 redesign).
- Non-resident tax computation (simplified view only).
