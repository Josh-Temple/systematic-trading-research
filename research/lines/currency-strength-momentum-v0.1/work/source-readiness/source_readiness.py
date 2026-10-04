#!/usr/bin/env python3
"""Metadata-only full-history source-readiness check for CSM.

Raw ECB CSV bytes exist only in memory on the isolated CI runner.
OBS_VALUE contents are never printed, persisted, uploaded, or committed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

START = "2009-11-01"
END = "2026-09-30"
API = "https://data-api.ecb.europa.eu/service/data/EXR/{key}?startPeriod={start}&endPeriod={end}&format=csvdata"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_decimal_reason(text: str) -> str | None:
    if text == "":
        return "blank"
    try:
        value = Decimal(text)
    except InvalidOperation:
        return "nonnumeric"
    if not value.is_finite():
        return "nonfinite"
    if value <= 0:
        return "nonpositive"
    return None


def fetch(url: str) -> tuple[bytes, dict[str, Any]]:
    last_type = None
    for attempt in range(3):
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "text/csv",
                "User-Agent": "systematic-trading-research-csm-source-readiness/0.2",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                raw = response.read()
                meta = {
                    "http_status": getattr(response, "status", None),
                    "content_type": response.headers.get("Content-Type"),
                    "http_date": response.headers.get("Date"),
                    "last_modified": response.headers.get("Last-Modified"),
                    "etag": response.headers.get("ETag"),
                    "cache_control": response.headers.get("Cache-Control"),
                }
            if not raw:
                raise RuntimeError("empty response")
            return raw, meta
        except Exception as exc:
            last_type = type(exc).__name__
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"acquisition failed after retries ({last_type})")


def check_series(
    entry: dict[str, Any],
    expected_dates: list[str],
    expected_schema: list[str],
) -> dict[str, Any]:
    ccy = entry["currency"]
    key = entry["key"]
    url = API.format(key=key, start=START, end=END)
    expected_set = set(expected_dates)

    try:
        raw, http_meta = fetch(url)
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""))
        header = list(reader.fieldnames or [])
        schema_match = header == expected_schema

        dates: list[str] = []
        seen: set[str] = set()
        status_counts: Counter[str] = Counter()
        duplicate_count = 0
        value_reasons: Counter[str] = Counter()
        dimension_mismatch_count = 0
        source_agency_mismatch_count = 0

        for row in reader:
            period = (row.get("TIME_PERIOD") or "").strip()
            if period in seen:
                duplicate_count += 1
            seen.add(period)
            dates.append(period)

            status = (row.get("OBS_STATUS") or "").strip() or "<BLANK>"
            status_counts[status] += 1

            reason = safe_decimal_reason((row.get("OBS_VALUE") or "").strip())
            if reason is not None:
                value_reasons[reason] += 1

            if (
                (row.get("FREQ") or "").strip() != "D"
                or (row.get("CURRENCY") or "").strip() != ccy
                or (row.get("CURRENCY_DENOM") or "").strip() != "EUR"
                or (row.get("EXR_TYPE") or "").strip() != "SP00"
                or (row.get("EXR_SUFFIX") or "").strip() != "A"
                or (row.get("UNIT") or "").strip() != entry["unit"]
                or (row.get("UNIT_MULT") or "").strip() != str(entry["unit_mult"])
            ):
                dimension_mismatch_count += 1

            if (row.get("SOURCE_AGENCY") or "").strip() != "4F0":
                source_agency_mismatch_count += 1

        date_set = set(dates)
        missing_expected = sorted(expected_set - date_set)
        unexpected_dates = sorted(date_set - expected_set)
        unexpected_status_count = sum(v for k, v in status_counts.items() if k != "A")
        ordered = dates == sorted(dates)

        gap = (
            not schema_match
            or duplicate_count != 0
            or missing_expected
            or unexpected_dates
            or unexpected_status_count != 0
            or sum(value_reasons.values()) != 0
            or dimension_mismatch_count != 0
            or source_agency_mismatch_count != 0
            or not ordered
        )

        return {
            "series": key,
            "currency": ccy,
            "request_url": url,
            "raw_response_bytes": len(raw),
            "raw_response_sha256": sha256(raw),
            **http_meta,
            "schema_match": schema_match,
            "schema_sha256": sha256(("\n".join(header) + "\n").encode()),
            "row_count": len(dates),
            "unique_date_count": len(date_set),
            "first_date": min(dates) if dates else None,
            "last_date": max(dates) if dates else None,
            "dates_sha256": sha256(("\n".join(dates) + "\n").encode()),
            "status_counts": dict(sorted(status_counts.items())),
            "duplicate_count": duplicate_count,
            "missing_expected_count": len(missing_expected),
            "missing_expected_dates": missing_expected,
            "unexpected_date_count": len(unexpected_dates),
            "unexpected_dates": unexpected_dates,
            "blank_obs_value_count": value_reasons["blank"],
            "nonnumeric_obs_value_count": value_reasons["nonnumeric"],
            "nonfinite_obs_value_count": value_reasons["nonfinite"],
            "nonpositive_obs_value_count": value_reasons["nonpositive"],
            "dimension_mismatch_count": dimension_mismatch_count,
            "source_agency_mismatch_count": source_agency_mismatch_count,
            "date_order_strict_non_decreasing": ordered,
            "readiness_status": "PASS" if not gap else "GAP",
            "obs_value_contents_emitted": False,
            "raw_response_persisted": False,
        }

    except Exception as exc:
        return {
            "series": key,
            "currency": ccy,
            "request_url": url,
            "readiness_status": "ACQUISITION_FAILURE",
            "error_type": type(exc).__name__,
            "obs_value_contents_emitted": False,
            "raw_response_persisted": False,
        }


def safe_summary(receipt: dict[str, Any]) -> dict[str, Any]:
    if receipt["readiness_status"] == "ACQUISITION_FAILURE":
        return {
            "series": receipt["series"],
            "readiness_status": receipt["readiness_status"],
            "error_type": receipt["error_type"],
            "obs_value_contents_emitted": False,
        }
    return {
        "series": receipt["series"],
        "readiness_status": receipt["readiness_status"],
        "rows": receipt["row_count"],
        "unique_dates": receipt["unique_date_count"],
        "first_date": receipt["first_date"],
        "last_date": receipt["last_date"],
        "status_counts": receipt["status_counts"],
        "missing_expected_count": receipt["missing_expected_count"],
        "unexpected_date_count": receipt["unexpected_date_count"],
        "blank_obs_value_count": receipt["blank_obs_value_count"],
        "invalid_obs_value_count": (
            receipt["nonnumeric_obs_value_count"]
            + receipt["nonfinite_obs_value_count"]
            + receipt["nonpositive_obs_value_count"]
        ),
        "raw_response_sha256": receipt["raw_response_sha256"],
        "obs_value_contents_emitted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-lock", type=Path, required=True)
    parser.add_argument("--probe-metadata", type=Path, required=True)
    parser.add_argument("--expected-calendar", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    lock = json.loads(args.source_lock.read_text(encoding="utf-8"))
    probe = json.loads(args.probe_metadata.read_text(encoding="utf-8"))
    calendar = json.loads(args.expected_calendar.read_text(encoding="utf-8"))

    expected_dates = list(calendar["expected_open_dates"])
    expected_schema = list(probe["series"][0]["schema"])
    if calendar["range_start_inclusive"] != START or calendar["range_end_inclusive"] != END:
        raise RuntimeError("calendar range mismatch")

    receipts: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(check_series, entry, expected_dates, expected_schema): entry["key"]
            for entry in lock["series"]
        }
        for future in as_completed(futures):
            receipt = future.result()
            receipts.append(receipt)
            print(json.dumps(safe_summary(receipt), sort_keys=True))

    receipts.sort(key=lambda x: x["series"])
    any_gap = any(r["readiness_status"] != "PASS" for r in receipts)

    result = {
        "receipt_id": "CSM-SOURCE-READINESS-20261004-01",
        "scope": "metadata_only_full_history_readiness",
        "checker_version": "0.2",
        "source_lock_id": lock["source_lock_id"],
        "source_lock_sha256": sha256(args.source_lock.read_bytes()),
        "probe_metadata_sha256": sha256(args.probe_metadata.read_bytes()),
        "expected_calendar_sha256": sha256(args.expected_calendar.read_bytes()),
        "expected_open_day_count": len(expected_dates),
        "source_period": {"start": START, "end": END},
        "series_count": len(receipts),
        "series": receipts,
        "overall_status": "PASS" if not any_gap else "PARTIAL_WITH_GAPS",
        "market_outcome_access": False,
        "ranking_computed": False,
        "returns_computed": False,
        "obs_value_contents_emitted": False,
        "raw_responses_persisted": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "receipt_id": result["receipt_id"],
        "overall_status": result["overall_status"],
        "expected_open_day_count": result["expected_open_day_count"],
        "series_count": result["series_count"],
        "obs_value_contents_emitted": False,
        "raw_responses_persisted": False,
        "receipt_sha256": sha256(args.output.read_bytes()),
    }, sort_keys=True))
    return 0 if not any_gap else 2


if __name__ == "__main__":
    raise SystemExit(main())
