# GA4 Data API — pull page views

This folder contains a small Python client for [`analyticsdata.googleapis.com`](https://analyticsdata.googleapis.com) using [`properties.runReport`](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport).

The **Measurement ID** (`G-ELPM2185P7`) is only for the website tag. API calls use the **numeric Property ID** (e.g. `535765444`), in the form `properties/535765444`.

## One-time Google Cloud setup

1. In [Google Cloud Console](https://console.cloud.google.com/), pick or create a project.
2. Enable **Google Analytics Data API**: APIs & Services → Library → search “Google Analytics Data API” → Enable.
3. Create a **service account** (IAM & Admin → Service Accounts → Create). Download the JSON key.
4. In **Google Analytics** → **Admin** → your property → **Property access management** → **Add users** → paste the service account email (e.g. `something@project-id.iam.gserviceaccount.com`) with role **Viewer**.

## Run locally

```bash
cd scripts
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-ga4.txt

export GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json
export GA4_PROPERTY_ID=535765444   # optional; defaults to this in the script

python ga4_page_views.py
python ga4_page_views.py --start 7daysAgo --end today --limit 100
```

Output is JSON: `pagePath`, `pageTitle`, `screenPageViews` (GA4’s page-view style metric for web + app).

### Realtime (optional)

```bash
python ga4_page_views.py --realtime
```

Uses `runRealtimeReport` with `unifiedScreenName` + `activeUsers`. Realtime **dimensions/metrics differ** from standard reports; if you get an error, check [Realtime schema](https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-api-schema) and edit the script.

## REST equivalent (curl)

After obtaining an OAuth2 access token with scope `https://www.googleapis.com/auth/analytics.readonly` (e.g. `gcloud auth print-access-token` with a user that has GA4 access, or a service account token exchange):

```bash
PROPERTY_ID=535765444
TOKEN="$(gcloud auth print-access-token)"

curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/${PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{ "startDate": "7daysAgo", "endDate": "today" }],
    "dimensions": [{ "name": "pagePath" }, { "name": "pageTitle" }],
    "metrics": [{ "name": "screenPageViews" }],
    "orderBys": [{ "desc": true, "metric": { "metricName": "screenPageViews" } }],
    "limit": 50
  }'
```

Service accounts cannot use `gcloud auth print-access-token` by default; use **Application Default Credentials** with the Python script instead.

## Troubleshooting

| Issue | What to check |
|--------|----------------|
| `403 PERMISSION_DENIED` | Service account email added as **Viewer** on the **GA4 property** (not only GCP IAM). |
| `404 NOT_FOUND` | Wrong numeric property ID or API not enabled for the GCP project tied to the credentials. |
| Empty `rows` | No traffic in date range, or reporting delay (rare for standard reports). |
| Metric/dimension error | Pair must be valid — use [Dimensions & Metrics Explorer](https://ga-dev-tools.web.app/ga4/dimensions-metrics-explorer/) or `properties/getMetadata`. |

## Official libraries

- Python: `google-analytics-data`
- Node: `@google-analytics/data`
- REST: base URL `https://analyticsdata.googleapis.com`
