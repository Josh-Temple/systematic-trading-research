#!/usr/bin/env python3
"""Metadata-only full-history source-readiness check for CSM.

This script receives full ECB CSV bytes on an isolated CI runner but never emits,
persists, uploads, or commits OBS_VALUE contents. It emits only source metadata,
date/status distributions, validity counts, and hashes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import sys
import urllib.request
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

START = "2009-11-01"
END = "2026-09-30"
API = "https://data-api.ecb.europa.eu/service/data/EXR/{key}?startPeriod={start}&endPeriod={end}&format=csvdata"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_decimal_ok(text: str) -> tuple[bool, str | None]:
    if text == "":
        return False, "blank"
    try:
        value = Decimal(text)
    except InvalidOperation:
        return False, "nonnumeric"
    if not value.is_finite():
        return False, "nonfinite"
    if value <= 0:
        return False, "nonpositive"
    return True, None


def fetch(url: str) -> tuple[bytes, dict[str, Any]]:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "text/csv",
            "User-Agent": "systematic-trading-research-csm-source-readiness/0.1",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as response:
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
    expected_set = set(expected_dates)
    expected_schema = list(probe["series"][0]["schema"])
    expected_by_ccy = {entry["currency"]: entry for entry in lock["series"]}

    if calendar["range_start_inclusive"] != START or calendar["range_end_inclusive"] != END:
        raise RuntimeError("calendar range does not match fixed source interval")

    series_receipts = []
    any_gap = False

    for entry in lock["series"]:
        ccy = entry["currency"]
        key = entry["key"]
        url = API.format(key=key, start=START, end=END)

        try:
            raw, http_meta = fetch(url)
            text_stream = io.StringIO(raw.decode("utf-8-sig"), newline="")
            reader = csv.DictReader(text_stream)
            header = list(reader.fieldnames or [])
            schema_match = header == expected_schema

            dates: list[str] = []
            status_counts: Counter[str] = Counter()
            duplicate_count = 0
            blank_value_count = 0
            nonnumeric_value_count = 0
            nonfinite_value_count = 0
            nonpositive_value_count = 0
            dimension_mismatch_count = 0
            source_agency_mismatch_count = 0
            unexpected_status_count = 0
            seen: set[str] = set()

            for row in reader:
                period = (row.get("TIME_PERIOD") or "").strip()
                if period in seen:
                    duplicate_count += 1
                else:
                    seen.add(period)
                dates.append(period)

                status = (row.get("OBS_STATUS") or "").strip() or "<BLANK>"
                status_counts[status] += 1
                if status not in {"A"}:
                    unexpected_status_count += 1

                value_text = (row.get("OBS_VALUE") or "").strip()
                ok, reason = safe_decimal_ok(value_text)
                if not ok:
                    if reason == "blank":
                        blank_value_count += 1
                    elif reason == "nonnumeric":
                        nonnumeric_value_count += 1
                    elif reason == "nonfinite":
                        nonfinite_value_count += 1
                    elif reason == "nonpositive":
                        nonpositive_value_count += 1

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
            ordered = dates == sorted(dates)
            date_hash = sha256(("\n".join(dates) + "\n").encode("utf-8"))

            gap_fields = {
                "schema_match": schema_match,
                "duplicate_count": duplicate_count,
                "missing_expected_count": len(missing_expected),
                "unexpected_date_count": len(unexpected_dates),
                "unexpected_status_count": unexpected_status_count,
                "blank_value_count": blank_value_count,
                "nonnumeric_value_count": nonnumeric_value_count,
                "nonfinite_value_count": nonfinite_value_count,
                "nonpositive_value_count": nonpositive_value_count,
                "dimension_mismatch_count": dimension_mismatch_count,
                "source_agency_mismatch_count": source_agency_mismatch_count,
                "date_order_strict_non_decreasing": ordered,
            }
            series_gap = (
                not schema_match
                or duplicate_count != 0
                or len(missing_expected) != 0
                or len(unexpected_dates) != 0
                or unexpected_status_count != 0
                or blank_value_count != 0
                or nonnumeric_value_count != 0
                or nonfinite_value_count != 0
                or nonpositive_value_count != 0
                or dimension_mismatch_count != 0
                or source_agency_mismatch_count != 0
                or not ordered
            )
            any_gap = any_gap or series_gap

            receipt = {
                "series": key,
                "currency": ccy,
                "request_url": url,
                "raw_response_bytes": len(raw),
                "raw_response_sha256": sha256(raw),
                **http_meta,
                "schema_match": schema_match,
                "schema_sha256": sha256(("\n".join(header) + "\n").encode("utf-8")),
                "row_count": len(dates),
                "unique_date_count": len(date_set),
                "first_date": min(dates) if dates else None,
                "last_date": max(dates) if dates else None,
                "dates_sha256": date_hash,
                "status_counts": dict(sorted(status_counts.items())),
                "duplicate_count": duplicate_count,
                "missing_expected_count": len(missing_expected),
                "missing_expected_dates": missing_expected,
                "unexpected_date_count": len(unexpected_dates),
                "unexpected_dates": unexpected_dates,
                "unexpected_status_count": unexpected_status_count,
                "blank_obs_value_count": blank_value_count,
                "nonnumeric_obs_value_count": nonnumeric_value_count,
                "nonfinite_obs_value_count": nonfinite_value_count,
                "nonpositive_obs_value_count": nonpositive_value_count,
                "dimension_mismatch_count": dimension_mismatch_count,
                "source_agency_mismatch_count": source_agency_mismatch_count,
                "date_order_strict_non_decreasing": ordered,
                "readiness_status": "PASS" if not series_gap else "GAP",
                "obs_value_contents_emitted": False,
                "raw_response_persisted": False,
            }
            series_receipts.append(receipt)

            # Only safe metadata is printed.
            print(
                json.dumps(
                    {
                        "series": key,
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
                    },
                    sort_keys=True,
                )
            )

        except Exception as exc:
            any_gap = True
            series_receipts.append(
                {
                    "series": key,
                    "currency": ccy,
                    "readiness_status": "ACQUISITION_FAILURE",
                    "error_type": type(exc).__name__,
                    "obs_value_contents_emitted": False,
                    "raw_response_persisted": False,
                }
            )
            print(json.dumps({"series": key, "readiness_status": "ACQUISITION_FAILURE", "error_type": type(exc).__name__}))
            # Continue to capture all-series readiness without leaking exception content.

    result = {
        "receipt_id": "CSM-SOURCE-READINESS-20261004-01",
        "scope": "metadata_only_full_history_readiness",
        "source_lock_id": lock["source_lock_id"],
        "source_lock_sha256": sha256(args.source_lock.read_bytes()),
        "probe_metadata_sha256": sha256(args.probe_metadata.read_bytes()),
        "expected_calendar_sha256": sha256(args.expected_calendar.read_bytes()),
        "expected_open_day_count": len(expected_dates),
        "source_period": {"start": START, "end": END},
        "series_count": len(series_receipts),
        "series": series_receipts,
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
