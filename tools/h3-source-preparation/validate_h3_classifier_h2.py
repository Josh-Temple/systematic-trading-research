#!/usr/bin/env python3
"""Validate H3 confirmation classification against consumed H2 M1 only.

This validation uses the exact frozen H2 135-file M1 prefix and exact legacy
run_v01.py. It does not read H3 post-2026-07-09 M1, Tick data, returns, group
contrasts, or bootstrap output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import run_h3_once as h3


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--h2-prefix-root", type=Path, required=True)
    parser.add_argument("--legacy-generator", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    legacy = h3.load_legacy_generator(args.legacy_generator)
    identity_path = args.h2_prefix_root / "h2_prefix_source_identity.json"
    identity = json.loads(identity_path.read_text(encoding="utf-8"))

    records = identity["records"]
    if len(records) != 135:
        raise ValueError("h2_prefix_record_count_mismatch")

    all_bars = []
    for record in records:
        path = args.h2_prefix_root / record["relative_path"]
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != record["sha256"]:
            raise ValueError(
                f"h2_prefix_raw_identity_mismatch:{record['date']}"
            )
        rows = legacy.decode_m1(json.loads(raw))
        for row in rows:
            row["source_date"] = record["date"]
            all_bars.append(row)

    all_bars.sort(key=lambda row: row["ts"])
    if any(
        all_bars[i]["ts"] >= all_bars[i + 1]["ts"]
        for i in range(len(all_bars) - 1)
    ):
        raise ValueError("h2_global_m1_not_strictly_increasing")

    date_ranges = {}
    for i, bar in enumerate(all_bars):
        date_ranges.setdefault(bar["source_date"], [i, i + 1])[1] = i + 1
    date_ranges = {
        key: tuple(value)
        for key, value in date_ranges.items()
    }

    abs_change_prefix = [0.0]
    for i in range(1, len(all_bars)):
        abs_change_prefix.append(
            abs_change_prefix[-1]
            + abs(all_bars[i]["c"] - all_bars[i - 1]["c"])
        )

    selected = [
        record["date"]
        for record in records
        if record["sample_role"] == "FROZEN_H2_SELECTED_SESSION"
    ]
    if len(selected) != 60:
        raise ValueError("h2_selected_session_count_mismatch")

    checks = []
    for day in selected:
        classified = h3.classify_session(
            all_bars,
            day,
            date_ranges,
            abs_change_prefix,
        )
        checks.append(
            h3.crosscheck_with_legacy(
                legacy,
                all_bars,
                day,
                date_ranges,
                abs_change_prefix,
                classified,
            )
        )

    all_pass = all(
        all(value is True for key, value in row.items() if key != "date")
        for row in checks
    )
    result = {
        "scope": "H3_CLASSIFIER_VALIDATION_ON_CONSUMED_H2_M1_ONLY",
        "h2_prefix_identity_file_sha256": hashlib.sha256(
            identity_path.read_bytes()
        ).hexdigest(),
        "legacy_generator_sha256": hashlib.sha256(
            args.legacy_generator.read_bytes()
        ).hexdigest(),
        "selected_sessions": len(selected),
        "crosscheck_sessions": len(checks),
        "all_pass": all_pass,
        "h3_post_h2_source_accessed": False,
        "tick_outcome_accessed": False,
        "primary_contrast_computed": False,
        "bootstrap_run": False,
    }
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False))

    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
