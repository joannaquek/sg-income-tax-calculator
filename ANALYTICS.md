# Analytics Setup — SG Income Tax Calculator

## Tracking Stack

| Tool | Purpose | Dashboard |
|------|---------|-----------|
| **Google Analytics 4** | Quantitative: user counts, funnel drop-off, event frequency | [analytics.google.com](https://analytics.google.com) |
| **Microsoft Clarity** | Qualitative: session recordings, heatmaps, rage clicks | [clarity.microsoft.com](https://clarity.microsoft.com) |

### GA4 Property
- **Measurement ID**: `G-ELPM2185P7` (Vercel stream, primary)
- **Stream name**: Tax Calculator
- **Stream URL**: `https://sg-income-tax-calculator.vercel.app/` (primary)
- **GitHub Pages (backup)**: `https://joannaquek.github.io/sg-income-tax-calculator/`

### Microsoft Clarity
- **Project name**: SG Tax Calculator
- **Project ID**: `wl75letgzu`

---

## Custom Events Tracked

All events are fired via a `track(event, params)` wrapper in the JS (calls `gtag('event', ...)`).

| Event | When it fires | Parameters |
|-------|--------------|------------|
| `step_view` | User navigates to any step | `step_number` (0–3), `step_name` ("You & Income", "Family", "Reliefs", "Results") |
| `calculate_tax` | Results page is rendered | `income_bracket`, `net_tax`, `married`, `children_count`, `relief_cap_hit`, `donations` |
| `theme_toggle` | User switches light/dark mode | `theme` ("light" / "dark") |
| `married_toggle` | Married checkbox toggled | `married` (true / false) |
| `add_child` | User adds a child row | `count` (cumulative child count) |
| `add_parent` | User adds a parent/dependant row | — |
| `copy_summary` | Copy summary button clicked | — |
| `pdf_prefill` | IRAS Pre-Filled PDF parsed successfully | `income_found`, `children_found`, `has_wmcr`, `ya` |
| `simulator_render` | Results charts drawn (tax resident + income &gt; 0) | `max_voluntary_delta`, `hit_cap` |

### `income_bracket` values
| Value | Range |
|-------|-------|
| `<40k` | Below $40,000 |
| `40-80k` | $40,000 – $79,999 |
| `80-160k` | $80,000 – $159,999 |
| `160-320k` | $160,000 – $319,999 |
| `320k+` | $320,000 and above |

---

## Key Metrics to Monitor

### 1. User Acquisition
- **Total users** — how many unique visitors
- **Sessions** — total visits (one user can have multiple sessions)
- **Traffic source** — where users come from (Direct, Social, Referral)
  - Most traffic expected as "Direct" since the URL is shared via WhatsApp/Telegram

### 2. Funnel Drop-off (most important)
Set up a **Funnel Exploration** in GA4 (Explore → Funnel exploration) using `step_view` events:

| Step | Event filter | What it measures |
|------|-------------|-----------------|
| Step 1 | `step_number = 0` | Users who landed and saw "You & Income" |
| Step 2 | `step_number = 1` | Users who continued to "Family" |
| Step 3 | `step_number = 2` | Users who continued to "Reliefs" |
| Step 4 | `step_number = 3` | Users who reached "Results" |

**Target**: < 30% drop-off at each step. High drop-off at Step 1→2 may mean the income/age fields are confusing. High drop-off at Step 2→3 may mean the family section feels complex.

### 3. Engagement Quality
| Metric | Where to find | Target |
|--------|--------------|--------|
| `calculate_tax` event count | Events report | > 60% of Step 4 viewers should trigger this |
| `copy_summary` count | Events report | Proxy for "found this useful enough to share" |
| Average session duration | Overview report | > 3 minutes = high engagement |
| Bounce rate (single-page sessions) | Engagement report | < 60% is healthy for a tool like this |

### 4. User Profile Insights (from `calculate_tax`)
| Dimension | Business insight |
|-----------|----------------|
| `income_bracket` distribution | Which income segment uses this most |
| `married = true` % | How many users need the spouse comparison feature |
| `children_count > 0` % | Demand for QCR/WMCR/PTR features |
| `relief_cap_hit = true` % | How many users are over the $80k cap |
| `donations = true` % | Uptake of the donation relief feature |

### 5. UX Issues (via Microsoft Clarity)
| Signal | What to look for |
|--------|----------------|
| **Session recordings** | Where users pause, scroll back, or abandon |
| **Heatmaps** | Which input fields get the most/least interaction |
| **Rage clicks** | Elements users click repeatedly in frustration |
| **Dead clicks** | Clicks on non-interactive elements (suggests confusion) |

---

## How to Set Up the GA4 Funnel Report

1. Go to [analytics.google.com](https://analytics.google.com) → your property
2. Left sidebar → **Explore** → click **"+"** → choose **Funnel exploration**
3. Under **Steps**, add 4 steps:
   - Step 1: Event = `step_view`, add filter `step_number equals 0`
   - Step 2: Event = `step_view`, add filter `step_number equals 1`
   - Step 3: Event = `step_view`, add filter `step_number equals 2`
   - Step 4: Event = `step_view`, add filter `step_number equals 3`
4. Set date range to last 28 days
5. Save the exploration as "Step Funnel"

---

## Review Cadence

| Frequency | What to check |
|-----------|--------------|
| **Weekly** | Total users, funnel completion rate, `copy_summary` count |
| **Monthly** | Income bracket distribution, married %, `relief_cap_hit` %, session duration trend |
| **After each release** | Compare funnel completion rate before vs after to validate improvements |

---

## Future Tracking to Add

- **Field-level timing**: Time spent on each input field (identify confusing fields)
- **Tooltip engagement**: Track when users hover/tap the `?` icons to see which reliefs need better explanation
- **Error/edge cases**: Track when `net_tax = 0` (may indicate bad input)
- **Return visitors**: Segment repeat users vs first-time (GA4 does this automatically via User report)
