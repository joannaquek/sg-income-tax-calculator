# Device / viewport checklist

Test the live site: https://sg-income-tax-calculator.vercel.app/

Use the browser **responsive design mode** (Chrome: F12 → device toolbar) or real devices.

## Widths to sample

| Label | Viewport (w×h) | What to check |
|-------|----------------|---------------|
| Phone (small) | 360×800 | Stepper scrolls horizontally; Continue full-width; tooltips; PDF upload stack; **Top-up charts** scroll horizontally in grey box |
| Phone (iOS) | 390×844 | Same + date/number inputs (16px font, no zoom) |
| Tablet | 768×1024 | Two-column grids; step labels visible; charts readable |
| Desktop | 1280×800 | Wider content (~860px max); both chart panels full width |

## Key CSS breakpoints in the app

- **&lt; 560px**: single-column form grids, full-width primary button in nav, upload CTA stacks
- **560px+**: two-column `.grid-2`
- **580px+**: step names show next to step numbers
- **900px+**: slightly wider main column

## Flow to smoke-test (5 min)

1. Land → read **intro** + **upload** card (no layout break)
2. Step 1 → income field (S$ prefix, commas)
3. Step 2–3 → Reliefs (caps bar)
4. **Results** → net tax, **Top-up simulator** (two charts if tax resident + income &gt; 0)
5. Toggle **dark mode**; repeat on phone width

## Real-device spot check

Open the link from **WhatsApp** on iPhone + **Chrome** on Android once before wider launch.
