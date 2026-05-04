# SG Income Tax Calculator — Handoff Document
*Last updated: 4 May 2026 (session close — family UX, GA4 API tooling, handoff refresh)*

---

## Recent changes (for next session)

- **Family step (v2.7)**: Master checkbox **“I have a spouse or dependants to declare”** (off by default). When on, user picks **Spouse / marriage**, **Qualifying children**, and/or **Parents or grandparents** independently. Tax logic uses `effectiveMarried()`, `childrenForTax()`, `parentsForTax()` — see `syncFamilyUI()` in the HTML. PDF pre-fill enables opt-in + children layer when children are detected.
- **Simulator charts**: Hover tooltips + **“Your inputs”** marker `(netTax, 0)` on voluntary + donation curves; `drawLineChart(..., opts)`.
- **GA4**: Snippet uses Measurement ID **`G-ELPM2185P7`** (same as property’s web stream). If Realtime is empty, usual causes are **ad blockers**, **wrong GA4 property selected in UI**, or **stream/property mismatch** — not a different “manual” install. **Data API** uses numeric **Property ID** `535765444` (`properties/535765444`), not `G-…`.
- **Repo tooling**: `scripts/ga4_page_views.py` + `scripts/README_GA4_DATA_API.md` — pulls `screenPageViews` by `pagePath` via `runReport` (needs GCP service account + GA4 property Viewer). `.gitignore` ignores `scripts/.venv/` and `*credentials*.json`.

---

## What Was Built

A self-contained single-file HTML tax calculator for Singapore YA 2026 (income earned in 2025), shared via link (WhatsApp/Telegram) and hosted on Vercel + GitHub Pages.

### Live URL
- **Primary**: https://sg-income-tax-calculator.vercel.app/
- **Backup**: https://joannaquek.github.io/sg-income-tax-calculator/
- **Repo**: https://github.com/joannaquek/sg-income-tax-calculator

### Current Version: v2.7

---

## Feature Inventory

| Feature | Status | Notes |
|---------|--------|-------|
| Progressive tax bands (YA 2026) | ✅ Done | All 13 IRAS bands |
| 15+ reliefs engine | ✅ Done | EIR, CPF, Spouse, QCR, WMCR, Parent, GCR, SRS, Top-ups, NSman, Life Ins, Sibling, Donations |
| $80k relief cap with proportional scaling | ✅ Done | Shows per-relief wasted amounts |
| PTR + personal income tax rebate | ✅ Done | PTR: $5k/$10k/$20k per SG citizen child |
| 4-step stepper UI | ✅ Done | You & Income → Family → Reliefs → Results |
| Light/dark mode (sun/moon slider) | ✅ Done | System preference + manual toggle |
| Tooltip on every field | ✅ Done | Pure CSS hover/focus, mobile-safe |
| Categorized relief breakdown in results | ✅ Done | Personal / Family / Voluntary / Other with subtotals |
| Optimizer cards | ✅ Done | SRS opportunity, CPF top-up, donation suggestion, QCR split, cap exceeded warning |
| QCR spouse split comparison (3-way) | ✅ Done | 0% / 50% / 100% to you |
| Donation relief (250% IPC deduction) | ✅ Done | Separate from $80k cap |
| Copy summary to clipboard | ✅ Done | WhatsApp/notes friendly |
| Print stylesheet | ✅ Done | |
| IRAS Pre-Filled PDF upload | ✅ Done | Client-side PDF.js, extracts income/CPF/children/donations |
| Income formatting (S$, comma formatting) | ✅ Done | Live as-you-type |
| Age validation (16–100 bounds) | ✅ Done | Inline error message |
| Citizenship + tax residency grouped | ✅ Done | Visual group with joint tooltip |
| Mobile sticky Continue button | ✅ Done | Full-width on <560px |
| Homepage intro (what the app does) | ✅ Done | v2.7 |
| Responsive layout pass | ✅ Done | Wider max-width on desktop; horizontal scroll stepper on phone; header stacks on small screens |
| Top-up simulator (line charts) | ✅ Done | Results: extra SRS+CPF voluntary vs net tax; extra IPC donations vs net tax; $80k cap callout; hover tooltips + current-scenario marker |
| Family step progressive disclosure | ✅ Done | Opt-in + layers (spouse / children / parents); sharing UI split QCR/PTR vs parent % |
| GA4 analytics | ✅ Done | Measurement ID: G-ELPM2185P7 (gtag.js in `<head>`) |
| GA4 Data API script (local) | ✅ Done | `scripts/ga4_page_views.py` — optional; not part of deployed site |
| Microsoft Clarity | ✅ Done | Project ID: wl75letgzu |
| GitHub Pages deployment | ✅ Done | Auto-deploys on push |
| Vercel deployment | ✅ Done | Auto-deploys on push, ~30s |

---

## File Structure

```
SingaporeIncomeTax/
├── index.html                          ← live file (copy of latest version)
├── sg-income-tax-calculator-v2.7.html  ← current version source
├── .gitignore                          ← venv + credential JSON patterns
├── DEVICE_TEST_CHECKLIST.md           ← viewport QA checklist
├── VERSION.md                          ← version history + changelog
├── ANALYTICS.md                        ← GA4/Clarity setup + KPI guide
├── PHASE2_SINGPASS.md                  ← spec for future Singpass integration
├── HANDOFF.md                          ← this file
├── scripts/
│   ├── ga4_page_views.py               ← GA4 Data API: page views (runReport)
│   ├── requirements-ga4.txt
│   └── README_GA4_DATA_API.md         ← API enable, service account, curl example
├── archive/
│   ├── sg-income-tax-calculator-ya2026.html  (v1.0)
│   ├── sg-income-tax-calculator-v2.html      (v2.2)
│   ├── sg-income-tax-calculator-v2.3.html    (v2.3)
│   ├── sg-income-tax-calculator-v2.4.html    (v2.4)
│   └── sg-income-tax-calculator-v2.5.html    (v2.5)
└── .design/sg-tax-calculator/
    ├── DESIGN_BRIEF.md
    ├── INFORMATION_ARCHITECTURE.md
    ├── DESIGN_TOKENS.css
    ├── TASKS.md
    └── DESIGN_REVIEW.md
```

### Deployment Workflow
1. Edit `sg-income-tax-calculator-v2.X.html` locally
2. Copy to `index.html` (the live file Vercel/GitHub Pages serves)
3. Archive the previous version to `archive/`
4. `git add -A && git commit -m "..." && git push`
5. Vercel auto-deploys in ~30 seconds

---

## Analytics Setup

| Tool | ID | Dashboard |
|------|----|-----------|
| GA4 | G-ELPM2185P7 | analytics.google.com |
| Clarity | wl75letgzu | clarity.microsoft.com |

### Key GA4 Events Tracked
- `step_view` — step_number (0–3), step_name → use for funnel drop-off
- `calculate_tax` — income_bracket, net_tax, married, **family_opt_in**, children_count, relief_cap_hit, donations
- `family_opt_in`, `family_layer_toggle` — family step disclosure
- `pdf_prefill` — fields_extracted, income_found, children_found
- `copy_summary` — proxy for "found it useful enough to share"
- `theme_toggle`, `married_toggle`, `add_child`, `add_parent`

### TODO: Set up GA4 Funnel Report
Explore → Funnel Exploration → 4 steps filtering on `step_view` + `step_number = 0/1/2/3`
See ANALYTICS.md for step-by-step.

---

## Outstanding Items for Next Session

### High Priority
- [ ] **Validate PDF parsing** — test with more real IRAS Pre-Filled statements (different scenarios: no children, no WMCR, foreigner, etc.) to ensure the regex extraction is robust
- [ ] **Error Resilience pass** — PRIZM scored this 58/100. Add validation to more fields: spouse income, SRS amount, CPF top-up amounts (should not exceed caps). Show inline errors on invalid input before allowing Continue.
- [ ] **Help icon consistency pass** — PRIZM issue #3 (low priority, wait for Clarity data first)

### Medium Priority
- [ ] **Citizenship dropdown chevron** — add CSS custom arrow (PRIZM issue #5, cosmetic)
- [ ] **"Results" step UX** — currently shows a blank `—` until Calculate is hit. Consider auto-running calculation when arriving at step 3.
- [ ] **Spouse age field** — currently no validation, add min/max like the main age field
- [ ] **Child DOB placeholder fix** — when PDF pre-fills children, placeholder DOB is set (2019-06-01). Add a yellow warning banner in Step 2 prompting the user to update it.

### Low Priority / Future
- [ ] **Singpass MyInfo integration** — full spec in `PHASE2_SINGPASS.md`. Requires GovTech onboarding + Node.js backend. Parked until traffic justifies complexity.
- [ ] **NOA comparison feature** — upload last year's Notice of Assessment to compare vs calculator estimate. Builds trust and shows users what they missed.
- [ ] **IRAS tax rates update** — update `TAX_CONFIG` in the HTML when YA 2027 rates are published (usually ~Feb each year)
- [ ] **SRS bank data** — no public API exists; would need manual entry or screen-scraping (not recommended). Keep as manual field.

---

## User Acquisition — Where to Start

### Immediate (free, high relevance)
1. **HardwareZone Finance forum** — `forums.hardwarezone.com.sg/forums/money-mind.103/` — Singapore's most active personal finance community. Post a "Built a free SG tax calculator" thread with screenshots.
2. **r/singaporefi** — `reddit.com/r/singaporefi` — active SG FIRE/personal finance subreddit. Share as a useful tool post.
3. **Seedly Community** — `community.seedly.com` — SG-focused personal finance Q&A. Answer tax questions and link the calculator.
4. **WhatsApp/Telegram group chats** — Your existing networks. Tax filing is very topical in Apr–May. A screenshot of the results page shared in a chat group spreads organically.

### Medium-term (content-driven)
5. **LinkedIn post** — Frame it as a side project: "I built a free Singapore tax calculator — here's what I learned". SG fintech/finance community engages well with this type of post.
6. **Singaporeans' Facebook groups** — "SGFinDex Users", "Singapore Personal Finance" group. File-sharing season = high engagement.
7. **Answer questions on CPF/tax** — Quora, Reddit, Seedly — answer specific tax questions and include the calculator as a resource.

### Timing note
Filing season runs **1 March – 18 April** each year. You're slightly past peak for YA 2026 filing. Best strategy now is to build awareness for **next year's filing season** and keep the URL memorable. Consider collecting emails via a simple "Notify me when YA 2027 rates are updated" form.

### Track acquisition in GA4
- Reports → Acquisition → Traffic Acquisition → look at `Session default channel group`
- Most early traffic will show as `Direct` (shared via WhatsApp/chat)
- If you post on Reddit/Seedly, tag the URLs with UTM parameters so GA4 shows the source:
  `https://sg-income-tax-calculator.vercel.app/?utm_source=reddit&utm_medium=social&utm_campaign=launch`

---

## Known Limitations / Tax Caveats
- WMCR/QCR conditions simplified (child order by DOB, not legal birth order in edge cases)
- PTR is a rebate (not relief) — correctly excluded from $80k cap
- Life Insurance relief requires CPF < $5,000 (most employees won't qualify — the tool allows entry but doesn't auto-block)
- Non-resident tax is simplified (flat 15% vs progressive, whichever higher)
- Donations: uses 250% deduction — verify if payroll-giving donations via employer may have different treatment
- All figures are estimates — users should verify with IRAS

---

## Design System
- **Aesthetic**: Scandinavian — warm off-white, teal accent (`#38b2ac`), soft shadows, rounded corners
- **Font**: DM Sans (body) + JetBrains Mono (numbers) from Google Fonts
- **Design tokens**: All colors/spacing in CSS custom properties at top of HTML file
- **Dark mode**: `[data-theme="dark"]` attribute on `<html>`, synced to localStorage + system preference
