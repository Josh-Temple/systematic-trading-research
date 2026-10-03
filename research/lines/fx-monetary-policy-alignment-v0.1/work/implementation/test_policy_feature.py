from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from policy_feature import (
    build_feature_ledger,
    canonical_ledger_bytes,
    policy_change,
    REASON_BREAK,
    REASON_INVALID,
    REASON_MISSING,
    REASON_RATE_UNAVAILABLE,
)

WORK = Path(__file__).resolve().parents[1]
LOCK = WORK / "source-qualification" / "SOURCE_LOCK.json"


class PolicyFeatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))

    def test_aligned(self):
        values = {
            ("AUD", "2020-01"): "1.00",
            ("AUD", "2020-04"): "1.50",
            ("JPY", "2020-01"): "-0.10",
            ("JPY", "2020-04"): "-0.10",
        }
        events = [{"event_id": "e1", "a": "AUD", "b": "JPY", "policy_old_month": "2020-01", "policy_new_month": "2020-04"}]
        rec = build_feature_ledger(events, values, self.lock)[0]
        self.assertEqual(rec["classification"], "ALIGNED")
        self.assertEqual(rec["z"], "0.50")

    def test_opposed(self):
        values = {
            ("AUD", "2020-01"): "1.50",
            ("AUD", "2020-04"): "1.00",
            ("JPY", "2020-01"): "-0.10",
            ("JPY", "2020-04"): "-0.10",
        }
        events = [{"event_id": "e1", "a": "AUD", "b": "JPY", "policy_old_month": "2020-01", "policy_new_month": "2020-04"}]
        rec = build_feature_ledger(events, values, self.lock)[0]
        self.assertEqual(rec["classification"], "OPPOSED")

    def test_neutral_exact_decimal(self):
        values = {
            ("AUD", "2020-01"): "1.10",
            ("AUD", "2020-04"): "1.20",
            ("CAD", "2020-01"): "2.30",
            ("CAD", "2020-04"): "2.40",
        }
        events = [{"event_id": "e1", "a": "AUD", "b": "CAD", "policy_old_month": "2020-01", "policy_new_month": "2020-04"}]
        rec = build_feature_ledger(events, values, self.lock)[0]
        self.assertEqual(rec["classification"], "NEUTRAL")
        self.assertEqual(rec["z"], "0.00")

    def test_missing_endpoint_fails_closed(self):
        change, reason = policy_change("AUD", "2020-01", "2020-04", {("AUD", "2020-01"): "1"}, self.lock)
        self.assertIsNone(change)
        self.assertEqual(reason, REASON_MISSING)

    def test_invalid_decimal_fails_closed(self):
        values = {("AUD", "2020-01"): "1", ("AUD", "2020-04"): "NaN"}
        change, reason = policy_change("AUD", "2020-01", "2020-04", values, self.lock)
        self.assertIsNone(change)
        self.assertEqual(reason, REASON_INVALID)

    def test_ch_switch_crossing_fails_closed(self):
        values = {("CHF", "2019-03"): "-0.75", ("CHF", "2019-06"): "-0.75"}
        change, reason = policy_change("CHF", "2019-03", "2019-06", values, self.lock)
        self.assertIsNone(change)
        self.assertEqual(reason, REASON_BREAK)

    def test_ch_same_side_of_switch_is_allowed(self):
        values = {("CHF", "2019-06"): "-0.75", ("CHF", "2019-09"): "-0.75"}
        change, reason = policy_change("CHF", "2019-06", "2019-09", values, self.lock)
        self.assertEqual(change, 0)
        self.assertIsNone(reason)

    def test_euro_switch_crossing_fails_closed(self):
        values = {("EUR", "2024-06"): "4.25", ("EUR", "2024-09"): "3.50"}
        change, reason = policy_change("EUR", "2024-06", "2024-09", values, self.lock)
        self.assertIsNone(change)
        self.assertEqual(reason, REASON_BREAK)

    def test_japan_no_policy_month_fails_closed_even_if_value_supplied(self):
        values = {("JPY", "2013-01"): "0.1", ("JPY", "2013-04"): "0.1"}
        change, reason = policy_change("JPY", "2013-01", "2013-04", values, self.lock)
        self.assertIsNone(change)
        self.assertEqual(reason, REASON_RATE_UNAVAILABLE)

    def test_japan_interval_bridging_no_policy_range_fails_closed(self):
        values = {("JPY", "2013-03"): "0.1", ("JPY", "2016-10"): "-0.1"}
        change, reason = policy_change("JPY", "2013-03", "2016-10", values, self.lock)
        self.assertIsNone(change)
        self.assertEqual(reason, REASON_RATE_UNAVAILABLE)

    def test_outcome_fields_cannot_change_ledger_bytes(self):
        values = {
            ("AUD", "2020-01"): "1.0",
            ("AUD", "2020-04"): "1.5",
            ("CAD", "2020-01"): "1.0",
            ("CAD", "2020-04"): "1.0",
        }
        base = [{"event_id": "e1", "a": "AUD", "b": "CAD", "policy_old_month": "2020-01", "policy_new_month": "2020-04", "future_return": "999"}]
        changed = copy.deepcopy(base)
        changed[0]["future_return"] = "-999"
        removed = copy.deepcopy(base)
        removed[0].pop("future_return")
        hashes = {
            hashlib.sha256(canonical_ledger_bytes(build_feature_ledger(events, values, self.lock))).hexdigest()
            for events in (base, changed, removed)
        }
        self.assertEqual(len(hashes), 1)

    def test_ledger_order_is_deterministic(self):
        values = {
            ("AUD", "2020-01"): "1", ("AUD", "2020-04"): "2",
            ("CAD", "2020-01"): "1", ("CAD", "2020-04"): "1",
        }
        a = {"event_id": "a", "a": "AUD", "b": "CAD", "policy_old_month": "2020-01", "policy_new_month": "2020-04"}
        b = {"event_id": "b", "a": "AUD", "b": "CAD", "policy_old_month": "2020-01", "policy_new_month": "2020-04"}
        x = canonical_ledger_bytes(build_feature_ledger([b, a], values, self.lock))
        y = canonical_ledger_bytes(build_feature_ledger([a, b], values, self.lock))
        self.assertEqual(x, y)


if __name__ == "__main__":
    unittest.main()
