"""Boundary checks for source inventories; uses synthetic quotes only."""

import importlib.util
import json
import unittest
from datetime import date
from pathlib import Path


def load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m1 = load("fetch_m1")
ticks = load("fetch_ticks")


class SourceBoundaryTests(unittest.TestCase):
    def test_m1_rejects_invalid_ohlc_and_duplicate_timestamp(self):
        payload = {"timestamp": 1783641600000, "shift": 60000, "multiplier": 1,
                   "open": 100, "high": 101, "low": 99, "close": 100,
                   "times": [0, 0], "opens": [0, 0], "highs": [0, -3],
                   "lows": [0, 0], "closes": [0, 0]}
        result = m1.inspect(json.dumps(payload).encode(), date(2026, 7, 10))
        self.assertEqual(result["basic_validation"], "FAIL")
        self.assertIn("duplicate_or_reversed_timestamp", result["basic_validation_reasons"])
        self.assertIn("invalid_ohlc", result["basic_validation_reasons"])

    def test_tick_empty_bucket_is_preserved(self):
        payload = {"timestamp": 1783641600000, "times": [], "asks": [], "bids": []}
        result = ticks.inspect(json.dumps(payload).encode(), date(2026, 7, 10), 0)
        self.assertEqual(result["quote_count"], 0)
        self.assertEqual(result["json_and_quote_validation"], "PASS")

    def test_tick_rejects_nonpositive_spread_and_reverse_time(self):
        payload = {"timestamp": 1783641600000, "multiplier": 1, "ask": 101, "bid": 100,
                   "times": [1, -1], "asks": [0, -2], "bids": [0, 0]}
        result = ticks.inspect(json.dumps(payload).encode(), date(2026, 7, 10), 0)
        self.assertEqual(result["json_and_quote_validation"], "FAIL")
        self.assertEqual(result["reversed_timestamp_count"], 1)
        self.assertEqual(result["nonpositive_spread_count"], 1)


if __name__ == "__main__":
    unittest.main()
