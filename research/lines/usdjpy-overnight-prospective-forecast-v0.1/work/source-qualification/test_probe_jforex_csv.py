import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from probe_jforex_csv import HEADER, START_MS, END_MS, inspect


class ControlledJForexCSVTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.path = Path(self.t.name) / "sample.csv"

    def write(self, rows, header=HEADER):
        with self.path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)

    def row(self, ts=START_MS, bid="157.101", ask="157.103", bv="2.0", av="3.0", instrument="USDJPY"):
        return [str(ts), bid, ask, bv, av, instrument]

    def test_valid_sample_no_market_outcome_fields(self):
        self.write([self.row(), self.row(END_MS)])
        x = inspect(self.path)
        self.assertEqual(x["status"], "STRUCTURE_PASS_SOURCE_GATE_STILL_BLOCKED")
        self.assertFalse(x["source_gate_passed"])
        self.assertEqual(x["decoded_record_count"], 2)
        self.assertEqual(x["window_start_utc"], "2024-01-15T12:59:00.000Z")
        self.assertNotIn("realized_return_bps", x)
        self.assertNotIn("pnl", x)
        self.assertNotIn("brier", x)

    def test_no_ticks(self):
        self.write([])
        self.assertEqual(inspect(self.path)["status"], "NO_TICKS_NOT_QUALIFIED")

    def test_exact_header_required(self):
        self.write([self.row()], header=["time", "bid", "ask", "bid_volume", "ask_volume", "instrument"])
        with self.assertRaises(ValueError):
            inspect(self.path)

    def test_wrong_instrument_blocked(self):
        self.write([self.row(instrument="EURJPY")])
        x = inspect(self.path)
        self.assertEqual(x["counts"]["wrong_instrument"], 1)
        self.assertEqual(x["status"], "BLOCKED_SOURCE_STRUCTURE")

    def test_crossed_market_blocked(self):
        self.write([self.row(bid="157.103", ask="157.101")])
        self.assertEqual(inspect(self.path)["counts"]["crossed_ask_below_bid"], 1)

    def test_bad_decimal_blocked(self):
        self.write([self.row(ask="not-a-number")])
        self.assertEqual(inspect(self.path)["counts"]["malformed_row"], 1)

    def test_nan_rejected(self):
        self.write([self.row(bid="NaN")])
        self.assertEqual(inspect(self.path)["counts"]["invalid_bid_ask"], 1)

    def test_negative_volume_rejected(self):
        self.write([self.row(av="-1")])
        self.assertEqual(inspect(self.path)["counts"]["invalid_volume"], 1)

    def test_outside_window_rejected(self):
        self.write([self.row(ts=START_MS-1)])
        self.assertEqual(inspect(self.path)["counts"]["timestamp_outside_predeclared_window"], 1)

    def test_unsorted_timestamp_rejected(self):
        self.write([self.row(ts=END_MS), self.row(ts=START_MS)])
        self.assertEqual(inspect(self.path)["counts"]["out_of_order_timestamps"], 1)

    def test_duplicate_timestamp_recorded_not_automatically_rejected(self):
        self.write([self.row(), self.row()])
        x = inspect(self.path)
        self.assertEqual(x["duplicate_timestamp_count"], 1)
        self.assertEqual(x["status"], "STRUCTURE_PASS_SOURCE_GATE_STILL_BLOCKED")

    def test_absurd_epoch_blocked_not_crashed(self):
        self.write([self.row(ts=999999999999999999)])
        x = inspect(self.path)
        self.assertEqual(x["status"], "BLOCKED_SOURCE_STRUCTURE")
        self.assertEqual(x["first_record_utc"], "INVALID_EPOCH_MS")

    def test_wrong_number_of_columns_rejected(self):
        self.write([self.row()[:3]])
        self.assertEqual(inspect(self.path)["counts"]["malformed_row"], 1)

    def test_append_only_receipt_never_overwritten(self):
        self.write([self.row()])
        receipt = Path(self.t.name) / "out.json"
        cmd = [sys.executable, "probe_jforex_csv.py", "--file", str(self.path), "--receipt", str(receipt)]
        d = Path(__file__).parent
        self.assertEqual(subprocess.run(cmd, cwd=d, capture_output=True).returncode, 0)
        before = receipt.read_bytes()
        self.assertNotEqual(subprocess.run(cmd, cwd=d, capture_output=True).returncode, 0)
        self.assertEqual(receipt.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
