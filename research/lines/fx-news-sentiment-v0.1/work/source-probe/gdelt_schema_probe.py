#!/usr/bin/env python3
"""Network/schema probe for GDELT DOC 2.0.

This probe does not calculate, fetch, or inspect any FX market outcome.
It deliberately uses a short recent window and emits schema metadata only.
"""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://api.gdeltproject.org/api/v2/doc/doc"
PROBE_QUERY = "euro sourcelang:english"


def stamp(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H%M%S")


def main() -> int:
    end = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(minutes=15)
    start = end - timedelta(hours=1)
    params = {
        "query": PROBE_QUERY,
        "mode": "artlist",
        "maxrecords": "10",
        "startdatetime": stamp(start),
        "enddatetime": stamp(end),
        "sort": "datedesc",
        "format": "json",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "systematic-trading-research-source-probe/0.1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
        status = response.status
        content_type = response.headers.get("Content-Type")

    payload = json.loads(raw.decode("utf-8"))
    articles = payload.get("articles")
    if not isinstance(articles, list):
        raise RuntimeError(f"Expected articles list; top-level keys={sorted(payload.keys())}")

    article_keys = sorted(articles[0].keys()) if articles else []
    summary = {
        "probe_query": PROBE_QUERY,
        "start_utc": start.isoformat(),
        "end_utc": end.isoformat(),
        "http_status": status,
        "content_type": content_type,
        "raw_bytes": len(raw),
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "top_level_keys": sorted(payload.keys()),
        "article_count": len(articles),
        "article_keys": article_keys,
        "maxrecords": 10,
        "market_outcomes_accessed": False,
    }
    Path("gdelt_probe_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
