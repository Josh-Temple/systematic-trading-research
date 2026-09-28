#!/usr/bin/env python3
"""Apply the reconstructed summer UTC M1 trading-minute gate without outcomes.

This gate is limited to the July–September 2026 summer schedule. Its expected
minute sets (Mon–Thu 00:00–20:59 and 22:00–23:59; Fri 00:00–20:59 UTC)
reproduce the H1 frozen sample's 1,380 / 1,260 expected-minute counts and
the 151-minute exclusion of a shortened Monday. The H1 freeze records counts
and reasons but does not itself enumerate the minute set. This implementation
therefore records an explicit reconstruction for review. It does not choose a H3 sample
or inspect Tick prices, touches, confirmation or outcomes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path

from fetch_m1 import decode_m1, inspect


def expected_minutes(day: date) -> set[int]:
    if not (date(2026, 7, 10) <= day <= date(2026, 9, 25)) or day.weekday() >= 5:
        raise ValueError("outside_verified_summer_weekday_scope")
    return set(range(0, 21 * 60)) | (set(range(22 * 60, 24 * 60)) if day.weekday() < 4 else set())


def classify(day: date, raw: bytes) -> dict:
    basic = inspect(raw, day)
    rows = decode_m1(json.loads(raw))
    start_ms = int(datetime(day.year, day.month, day.day, tzinfo=timezone.utc).timestamp() * 1000)
    observed = [(row["ts"] - start_ms) // 60_000 for row in rows]
    expected = expected_minutes(day)
    missing = sorted(expected - set(observed))
    extra = sorted(set(observed) - expected)
    duplicate = len(observed) - len(set(observed))
    eligible = basic["basic_validation"] == "PASS" and not missing and not extra and duplicate == 0
    return {
        "date": day.isoformat(), "eligible": eligible,
        "reason": "PASS" if eligible else (
            "basic_validation_failed" if basic["basic_validation"] != "PASS" else
            f"missing_expected_tradable_minutes={len(missing)}" if missing else
            f"extra_minutes={len(extra)}" if extra else f"duplicate_minutes={duplicate}"
        ),
        "rows": len(rows), "expected": len(expected), "missing": len(missing),
        "extra": len(extra), "duplicate": duplicate,
        "basic_validation": basic["basic_validation"],
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source_path = args.source / "m1_source_manifest.json"
    source_raw = source_path.read_bytes()
    source = json.loads(source_raw)
    records = []
    for prior in source["records"]:
        day = date.fromisoformat(prior["date"])
        raw = (args.source / prior["relative_path"]).read_bytes()
        if len(raw) != prior["byte_count"] or hashlib.sha256(raw).hexdigest() != prior["sha256"]:
            raise ValueError(f"source_identity_mismatch:{day}")
        records.append(classify(day, raw))
    count = sum(item["eligible"] for item in records)
    result = {
        "scope": "H3_OUTCOME_BLIND_SUMMER_M1_STRUCTURAL_GATE",
        "basis": "Reconstructed summer UTC minute set from H1 frozen sample_freeze.json expected counts and observed source intervals; exact schedule provenance pending",
        "basis_url": "https://drive.google.com/file/d/1k69iHCQwQ2GMQahPFYHTY1bQKrdz4daR/view",
        "input_manifest_sha256": hashlib.sha256(source_raw).hexdigest(),
        "candidate_start": source["candidate_start"],
        "latest_candidate_date_checked": source["latest_candidate_date_checked"],
        "calendar_candidate_count": len(records),
        "structurally_eligible_count": count,
        "classification_status": "RECONSTRUCTED_SCHEDULE_PENDING_PROVENANCE",
        "frozen_selected_count": 0,
        "source_gate": "NOT_EVALUATED",
        "current_state": "WAITING_FOR_MATURITY",
        "outcome_computed": False,
        "records": records,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidates": len(records), "eligible": count, "excluded": [r for r in records if not r["eligible"]]}))


if __name__ == "__main__":
    main()
