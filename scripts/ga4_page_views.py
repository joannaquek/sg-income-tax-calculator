#!/usr/bin/env python3
"""
Fetch page-view style traffic from GA4 using the Data API (runReport).

Docs: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport

Auth: Application Default Credentials — set either:
  export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
or run on a machine where you're logged in with:
  gcloud auth application-default login

GA4: grant the service account email "Viewer" on the property
     (Admin → Property access management).

Env:
  GA4_PROPERTY_ID  Numeric property ID (default: 535765444)
"""
from __future__ import annotations

import argparse
import json
import os
import sys


def run_page_view_report(
    property_id: str,
    start_date: str,
    end_date: str,
    limit: int,
) -> None:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        OrderBy,
        RunReportRequest,
    )

    client = BetaAnalyticsDataClient()
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="pagePath"),
            Dimension(name="pageTitle"),
        ],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[
            DateRange(start_date=start_date, end_date=end_date),
        ],
        order_bys=[
            OrderBy(
                metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"),
                desc=True,
            )
        ],
        limit=limit,
    )
    resp = client.run_report(req)

    rows = []
    for row in resp.rows:
        path = row.dimension_values[0].value
        title = row.dimension_values[1].value
        views = row.metric_values[0].value
        rows.append({"pagePath": path, "pageTitle": title, "screenPageViews": views})

    out = {
        "property": property_id,
        "dateRange": {"start": start_date, "end": end_date},
        "rowCount": len(rows),
        "rows": rows,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


def run_realtime_snapshot(property_id: str, limit: int) -> None:
    """Uses runRealtimeReport — schema differs from standard reports (see GA docs)."""
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        Dimension,
        Metric,
        RunRealtimeReportRequest,
    )

    client = BetaAnalyticsDataClient()
    req = RunRealtimeReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="unifiedScreenName")],
        metrics=[Metric(name="activeUsers")],
        limit=limit,
    )
    try:
        resp = client.run_realtime_report(req)
    except Exception as e:
        print(
            json.dumps(
                {
                    "error": str(e),
                    "hint": "Realtime dimensions vary by property; try adjusting dimensions in this script.",
                },
                indent=2,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    rows = []
    for row in resp.rows:
        screen = row.dimension_values[0].value
        users = row.metric_values[0].value
        rows.append({"unifiedScreenName": screen, "activeUsers": users})

    print(
        json.dumps(
            {
                "property": property_id,
                "kind": "realtime",
                "rowCount": len(rows),
                "rows": rows,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def main() -> None:
    pid = os.environ.get("GA4_PROPERTY_ID", "535765444")
    p = argparse.ArgumentParser(description="GA4 Data API — page views (runReport)")
    p.add_argument(
        "--property",
        default=pid,
        help="Numeric GA4 property ID (not G-xxxxxxxx)",
    )
    p.add_argument(
        "--start",
        default="28daysAgo",
        help="Start date: YYYY-MM-DD or relative e.g. 7daysAgo",
    )
    p.add_argument("--end", default="today", help="End date")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument(
        "--realtime",
        action="store_true",
        help="Use runRealtimeReport instead (last ~30 min; different dimensions)",
    )
    args = p.parse_args()

    if args.realtime:
        run_realtime_snapshot(args.property, args.limit)
    else:
        run_page_view_report(args.property, args.start, args.end, args.limit)


if __name__ == "__main__":
    main()
