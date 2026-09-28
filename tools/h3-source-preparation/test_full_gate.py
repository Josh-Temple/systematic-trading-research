"""Outcome-blind H3 source-gate regression tests."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

import build_h3_source_gate as gate
import classify_m1_structure as structure


class H3FullSourceGateTests(unittest.TestCase):
    def test_gate_waits_at_55_without_freeze_authority(self):
        self.assertEqual(
            gate.gate_state(eligible_count=55, all_components_pass=True),
            (
                "NOT_EVALUATED_PENDING_MATURITY",
                "WAITING_FOR_MATURITY",
                "ACQUIRE_NEXT_FULLY_COMPLETED_UTC_CANDIDATE_OUTCOME_BLIND",
            ),
        )

    def test_gate_opens_only_at_60_with_all_components_pass(self):
        self.assertEqual(
            gate.gate_state(eligible_count=60, all_components_pass=True),
            (
                "PASS",
                "READY_FOR_FROZEN_H3_RUN",
                "RUN_EXISTING_POST_H2_PREREGISTRATION_ONCE",
            ),
        )

    def test_component_failure_is_fail_closed_even_before_maturity(self):
        self.assertEqual(
            gate.gate_state(eligible_count=55, all_components_pass=False),
            ("HOLD", "HALTED_FAIL_CLOSED", "HALTED_FAIL_CLOSED"),
        )

    def test_summer_scope_covers_next_five_candidate_weekdays_only(self):
        self.assertEqual(len(structure.expected_minutes(date(2026, 10, 1))), 1380)
        self.assertEqual(len(structure.expected_minutes(date(2026, 10, 2))), 1260)
        with self.assertRaises(ValueError):
            structure.expected_minutes(date(2026, 10, 5))

    def test_tick_recompute_rejects_duplicate_timestamp(self):
        start = int(
            datetime(2026, 7, 10, tzinfo=timezone.utc).timestamp() * 1000
        )
        raw = json.dumps(
            {
                "timestamp": start,
                "multiplier": 1,
                "ask": 101,
                "bid": 100,
                "times": [1, 0],
                "asks": [0, 0],
                "bids": [0, 0],
            }
        ).encode()
        result = gate.inspect_tick_raw(raw, "2026-07-10", 0)
        self.assertEqual(result["duplicate_timestamp_count"], 1)
        self.assertEqual(result["validation"], "FAIL")

    def test_missing_original_tick_time_can_be_supported_by_exact_refetch_receipt(self):
        day = "2026-07-10"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            records = []
            for hour in range(24):
                stamp = int(
                    datetime(
                        2026, 7, 10, hour, tzinfo=timezone.utc
                    ).timestamp()
                    * 1000
                )
                raw = json.dumps(
                    {
                        "timestamp": stamp,
                        "multiplier": 1,
                        "ask": 101,
                        "bid": 100,
                        "times": [],
                        "asks": [],
                        "bids": [],
                    },
                    separators=(",", ":"),
                ).encode()
                path = root / "raw_tick" / day / f"{hour:02d}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                digest = hashlib.sha256(raw).hexdigest()
                record = {
                    "date": day,
                    "hour": hour,
                    "relative_path": f"raw_tick/{day}/{hour:02d}.json",
                    "retrieved_at_utc": (
                        "2026-09-28T00:00:00+00:00" if hour != 7 else None
                    ),
                    "byte_count": len(raw),
                    "sha256": digest,
                    "quote_count": 0,
                    "json_and_quote_validation": "PASS",
                    "status": "SOURCE_RECORDED",
                }
                records.append(record)
                if hour == 7:
                    receipt = {
                        "date": day,
                        "hour": hour,
                        "stored_sha256": digest,
                        "verified_response_bytes": len(raw),
                        "verified_response_sha256": digest,
                        "verified_retrieval_at_utc": "2026-09-28T04:00:00+00:00",
                        "status": "EXACT_MATCH",
                    }
                    receipt_path = (
                        root
                        / "tick_retrieval_verification"
                        / f"{day}_{hour:02d}.json"
                    )
                    receipt_path.parent.mkdir(parents=True, exist_ok=True)
                    receipt_path.write_text(json.dumps(receipt))

            manifest = {
                "date": day,
                "hours_requested": 24,
                "outcome_computed": False,
                "confirmation_outcome_comparison": False,
                "bootstrap_run": False,
                "records": records,
            }
            (root / f"tick_source_manifest_{day}.json").write_text(
                json.dumps(manifest)
            )

            result = gate.verify_ticks(root, root, [day])
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["original_retrieval_timestamp_count"], 23)
            self.assertEqual(result["exact_refetch_receipt_count"], 1)
            self.assertEqual(result["empty_bucket_count"], 24)


if __name__ == "__main__":
    unittest.main()
