#!/usr/bin/env python3
"""Outcome-blind BIS WS_CBPOL source preflight for RL-FXMP-001.

Downloads only the official BIS central-bank-policy-rate bulk archive.
It never reads FX price or return data. Observation values are parsed only
for validity/missingness and are never emitted to stdout or the JSON report.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
import urllib.request
import zipfile
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

URL = "https://data.bis.org/static/bulk/WS_CBPOL_csv_flat.zip"
AREAS = ("AU", "CA", "CH", "XM", "GB", "JP", "NZ", "US")
START = "2009-09"
END = "2026-08"
OUT_DIR = Path("artifacts/fxmp-source-preflight")
ZIP_PATH = OUT_DIR / "WS_CBPOL_csv_flat.zip"
REPORT_PATH = OUT_DIR / "fxmp_source_preflight.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def column_code(header: str) -> str:
    """BIS flat CSV uses headers such as FREQ:Frequency."""
    return header.split(":", 1)[0].strip()


def dimension_code(value: str | None) -> str:
    """BIS flat CSV uses values such as M: Monthly and AU: Australia."""
    if value is None:
        return ""
    return value.split(":", 1)[0].strip()


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "systematic-trading-research-fxmp-source-preflight/0.1",
            "Accept": "application/zip,application/octet-stream,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        raw = response.read()
        status = getattr(response, "status", None)
        content_type = response.headers.get("Content-Type")

    if not raw:
        raise RuntimeError("BIS bulk response was empty")

    ZIP_PATH.write_bytes(raw)
    archive_sha = sha256_bytes(raw)

    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        csv_members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise RuntimeError(f"Expected exactly one CSV member, found {len(csv_members)}")
        member = csv_members[0]
        csv_info = zf.getinfo(member)

        member_hasher = hashlib.sha256()
        with zf.open(member) as binary_member:
            while True:
                chunk = binary_member.read(1024 * 1024)
                if not chunk:
                    break
                member_hasher.update(chunk)
        member_sha = member_hasher.hexdigest()

        with zf.open(member) as binary_member:
            text_stream = io.TextIOWrapper(binary_member, encoding="utf-8-sig", newline="")
            reader = csv.DictReader(text_stream)
            if not reader.fieldnames:
                raise RuntimeError("CSV has no header")

            raw_headers = list(reader.fieldnames)
            normalized = {column_code(h): h for h in raw_headers}
            required = {"FREQ", "REF_AREA", "TIME_PERIOD", "OBS_VALUE"}
            missing_columns = sorted(required - set(normalized))
            if missing_columns:
                raise RuntimeError(
                    f"Missing required normalized columns: {missing_columns}; "
                    f"available={sorted(normalized)}"
                )

            def value(row: dict[str, str], code: str) -> str:
                return (row.get(normalized[code]) or "").strip()

            per_area = {
                area: {
                    "row_count": 0,
                    "first_period": None,
                    "last_period": None,
                    "duplicate_period_count": 0,
                    "missing_obs_value_count": 0,
                    "nonnumeric_obs_value_count": 0,
                    "obs_status_counts": Counter(),
                    "obs_conf_counts": Counter(),
                    "nonempty_supp_info_breaks_count": 0,
                    "supp_info_breaks_sha256": hashlib.sha256(),
                }
                for area in AREAS
            }
            seen_periods = {area: set() for area in AREAS}
            selected_total = 0

            for row in reader:
                if dimension_code(value(row, "FREQ")) != "M":
                    continue
                area = dimension_code(value(row, "REF_AREA"))
                if area not in per_area:
                    continue
                period = value(row, "TIME_PERIOD")
                if not (START <= period <= END):
                    continue

                rec = per_area[area]
                selected_total += 1
                rec["row_count"] += 1
                if rec["first_period"] is None or period < rec["first_period"]:
                    rec["first_period"] = period
                if rec["last_period"] is None or period > rec["last_period"]:
                    rec["last_period"] = period
                if period in seen_periods[area]:
                    rec["duplicate_period_count"] += 1
                seen_periods[area].add(period)

                obs = value(row, "OBS_VALUE")
                if not obs:
                    rec["missing_obs_value_count"] += 1
                else:
                    try:
                        Decimal(obs)
                    except InvalidOperation:
                        rec["nonnumeric_obs_value_count"] += 1

                if "OBS_STATUS" in normalized:
                    status_value = dimension_code(value(row, "OBS_STATUS")) or "<BLANK>"
                    rec["obs_status_counts"][status_value] += 1
                if "OBS_CONF" in normalized:
                    conf_value = dimension_code(value(row, "OBS_CONF")) or "<BLANK>"
                    rec["obs_conf_counts"][conf_value] += 1

                if "SUPP_INFO_BREAKS" in normalized:
                    break_text = value(row, "SUPP_INFO_BREAKS")
                    if break_text:
                        rec["nonempty_supp_info_breaks_count"] += 1
                        rec["supp_info_breaks_sha256"].update(break_text.encode("utf-8"))
                        rec["supp_info_breaks_sha256"].update(b"\0")

    safe_per_area = {}
    failures = []
    for area in AREAS:
        rec = per_area[area]
        safe_per_area[area] = {
            "row_count": rec["row_count"],
            "unique_period_count": len(seen_periods[area]),
            "first_period": rec["first_period"],
            "last_period": rec["last_period"],
            "duplicate_period_count": rec["duplicate_period_count"],
            "missing_obs_value_count": rec["missing_obs_value_count"],
            "nonnumeric_obs_value_count": rec["nonnumeric_obs_value_count"],
            "obs_status_counts": dict(sorted(rec["obs_status_counts"].items())),
            "obs_conf_counts": dict(sorted(rec["obs_conf_counts"].items())),
            "nonempty_supp_info_breaks_count": rec["nonempty_supp_info_breaks_count"],
            "supp_info_breaks_sha256": rec["supp_info_breaks_sha256"].hexdigest(),
        }
        if rec["row_count"] == 0:
            failures.append(f"{area}: no rows in requested interval")
        if rec["duplicate_period_count"]:
            failures.append(f"{area}: duplicate TIME_PERIOD rows")
        if rec["nonnumeric_obs_value_count"]:
            failures.append(f"{area}: nonnumeric OBS_VALUE rows")

    report = {
        "schema_version": "fxmp-source-preflight-v0.2",
        "source_url": URL,
        "http_status": status,
        "content_type": content_type,
        "archive_bytes": len(raw),
        "archive_sha256": archive_sha,
        "csv_member": member,
        "csv_member_uncompressed_bytes": csv_info.file_size,
        "csv_member_sha256": member_sha,
        "raw_header": raw_headers,
        "normalized_header_codes": sorted(normalized),
        "requested_frequency": "M",
        "requested_areas": list(AREAS),
        "requested_period_start": START,
        "requested_period_end": END,
        "selected_row_count": selected_total,
        "per_area": safe_per_area,
        "observation_values_emitted": False,
        "fx_price_or_return_data_accessed": False,
        "preflight_failures": failures,
        "status": "PASS" if not failures else "PARTIAL_OR_FAIL",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "status": report["status"],
                "archive_sha256": archive_sha,
                "archive_bytes": len(raw),
                "csv_member_uncompressed_bytes": csv_info.file_size,
                "selected_row_count": selected_total,
                "areas": {
                    a: {
                        "rows": safe_per_area[a]["row_count"],
                        "unique_periods": safe_per_area[a]["unique_period_count"],
                        "missing": safe_per_area[a]["missing_obs_value_count"],
                        "duplicates": safe_per_area[a]["duplicate_period_count"],
                        "nonnumeric": safe_per_area[a]["nonnumeric_obs_value_count"],
                    }
                    for a in AREAS
                },
                "failures": failures,
                "observation_values_emitted": False,
            },
            sort_keys=True,
        )
    )
    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
