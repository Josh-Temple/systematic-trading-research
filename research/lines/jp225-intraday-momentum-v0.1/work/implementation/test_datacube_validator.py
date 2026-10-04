import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parents[1] / "source-qualification"
sys.path.insert(0, str(SOURCE_DIR))

from validate_datacube_2025 import (  # noqa: E402
    EXPECTED_HEADER,
    build_receipt,
)


TEST_DAY = "20250106"
TEST_ISO_DAY = "2025-01-06"
CONTRACT = "202503"
SECURITY = "169060019"
FIXED_NOW = "2026-10-04T22:00:00+00:00"


def row(
    time_value="093000000",
    *,
    trade_date=TEST_DAY,
    execution_date=TEST_DAY,
    index_type="19",
    contract_month=CONTRACT,
    sco_category="0",
    sequence_no="1",
    trade_price="100000.00",
    trade_volume="1",
):
    return {
        "trade_date": trade_date,
        "execution_date": execution_date,
        "index_type": index_type,
        "security_code": SECURITY,
        "time": time_value,
        "trade_price": trade_price,
        "price_type": "N",
        "trade_volume": trade_volume,
        "no": sequence_no,
        "contract_month": contract_month,
        "sco_category": sco_category,
    }


def write_csv(path, rows, header=EXPECTED_HEADER):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for source in rows:
            writer.writerow({key: value for key, value in source.items() if key in header})


class DataCubeValidatorSyntheticTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.raw_dir = self.root / "raw"
        self.raw_dir.mkdir()
        self.calendar = self.root / "calendar.csv"
        with self.calendar.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(["execution_date", "expected_front_contract_month"])
            writer.writerow([TEST_ISO_DAY, CONTRACT])

    def tearDown(self):
        self.temp.cleanup()

    def receipt(self, rows, header=EXPECTED_HEADER):
        write_csv(self.raw_dir / "2025-01.csv", rows, header=header)
        return build_receipt(
            self.raw_dir,
            calendar_path=self.calendar,
            generated_at=FIXED_NOW,
        )

    def test_correct_nikkei_225_mini_row_counts_without_emitting_values(self):
        receipt = self.receipt([
            row("093000000", sequence_no="1"),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        self.assertEqual(receipt["files"][0]["index_type_values"], ["19"])
        self.assertEqual(receipt["files"][0]["contract_month_counts"], {CONTRACT: 3})
        self.assertEqual(receipt["boundary_coverage"]["09:30:00"]["dates_with_qualifying_rows"], 1)
        self.assertEqual(receipt["boundary_coverage"]["15:00:00"]["dates_with_qualifying_rows"], 1)
        self.assertEqual(receipt["boundary_coverage"]["15:30:00"]["dates_with_qualifying_rows"], 1)
        self.assertFalse(receipt["gate_checks"]["outcome_blindness_integrity_preserved"])
        self.assertFalse(receipt["gate_checks"]["packet_a_pass"])
        self.assert_no_market_values(receipt)

    def test_wrong_index_type_is_reported_and_not_counted(self):
        receipt = self.receipt([
            row("093000000", index_type="18"),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        self.assertEqual(receipt["files"][0]["index_type_values"], ["18", "19"])
        self.assertFalse(receipt["gate_checks"]["index_type_matches_nikkei_225_mini_19"])
        self.assertEqual(receipt["boundary_coverage"]["09:30:00"]["dates_with_qualifying_rows"], 0)

    def test_wrong_contract_month_is_not_counted_for_expected_contract(self):
        receipt = self.receipt([
            row("093000000", contract_month="202506"),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        self.assertEqual(receipt["boundary_coverage"]["09:30:00"]["dates_with_qualifying_rows"], 0)
        self.assertIn("202506", receipt["row_metadata"]["contract_month_counts"])

    def test_strategy_category_one_is_excluded(self):
        receipt = self.receipt([
            row("093000000", sco_category="1"),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        self.assertEqual(receipt["files"][0]["sco_category_counts"], {"0": 2, "1": 1})
        self.assertEqual(receipt["boundary_coverage"]["09:30:00"]["dates_with_qualifying_rows"], 0)

    def test_missing_sequence_is_diagnosed_and_not_used(self):
        receipt = self.receipt([
            row("093000000", sequence_no=""),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        self.assertEqual(receipt["sequence_diagnostics"]["missing_sequence_rows"], 1)
        self.assertEqual(receipt["boundary_coverage"]["09:30:00"]["dates_with_qualifying_rows"], 0)

    def test_duplicate_sequence_makes_same_timestamp_ambiguous(self):
        receipt = self.receipt([
            row("093000000", sequence_no="1"),
            row("093000000", sequence_no="1", trade_price="100001.00"),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        self.assertGreater(receipt["sequence_diagnostics"]["duplicate_sequence_groups"], 0)
        self.assertGreater(receipt["sequence_diagnostics"]["ambiguous_same_timestamp_groups"], 0)
        self.assertEqual(receipt["boundary_coverage"]["09:30:00"]["dates_with_qualifying_rows"], 0)

    def test_same_timestamp_with_unique_sequence_is_deterministic(self):
        receipt = self.receipt([
            row("093000000", sequence_no="1"),
            row("093000000", sequence_no="2", trade_price="100001.00"),
            row("150000000", sequence_no="3"),
            row("153000000", sequence_no="4"),
        ])
        self.assertGreater(receipt["sequence_diagnostics"]["same_millisecond_timestamp_groups"], 0)
        self.assertEqual(receipt["sequence_diagnostics"]["ambiguous_same_timestamp_groups"], 0)
        self.assertEqual(receipt["boundary_coverage"]["09:30:00"]["dates_with_qualifying_rows"], 1)

    def test_missing_boundary_window_is_unavailable_not_a_script_error(self):
        receipt = self.receipt([
            row("093101000", sequence_no="1"),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        boundary = receipt["boundary_coverage"]["09:30:00"]
        self.assertEqual(boundary["dates_with_qualifying_rows"], 0)
        self.assertEqual(boundary["unavailable_dates"][0]["reason"], "NO_QUALIFYING_ROW_IN_WINDOW")

    def test_execution_date_mismatch_does_not_satisfy_boundary(self):
        receipt = self.receipt([
            row("093000000", execution_date="20250107"),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        self.assertEqual(receipt["boundary_coverage"]["09:30:00"]["dates_with_qualifying_rows"], 0)

    def test_schema_mismatch_is_rejected(self):
        bad_header = tuple("trade_px" if key == "trade_price" else key for key in EXPECTED_HEADER)
        receipt = self.receipt([row()], header=bad_header)
        self.assertFalse(receipt["files"][0]["schema_match"])
        self.assertFalse(receipt["gate_checks"]["schema_matches"])

    def test_2024_row_is_rejected_from_2025_scope(self):
        receipt = self.receipt([
            row("093000000", trade_date="20241230", execution_date="20241230"),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        self.assertEqual(receipt["row_metadata"]["out_of_scope_date_rows_rejected"], 1)
        self.assertFalse(receipt["gate_checks"]["no_2024_or_2026_execution_or_trade_dates"])

    def test_2026_row_is_rejected_from_2025_scope(self):
        receipt = self.receipt([
            row("093000000", trade_date="20260105", execution_date="20260105"),
            row("150000000", sequence_no="2"),
            row("153000000", sequence_no="3"),
        ])
        self.assertEqual(receipt["row_metadata"]["out_of_scope_date_rows_rejected"], 1)
        self.assertFalse(receipt["gate_checks"]["no_2024_or_2026_execution_or_trade_dates"])

    def test_receipt_has_no_price_field_or_raw_price_value(self):
        receipt = self.receipt([
            row("093000000", sequence_no="1", trade_price="123456.78"),
            row("150000000", sequence_no="2", trade_price="234567.89"),
            row("153000000", sequence_no="3", trade_price="345678.90"),
        ])
        self.assert_no_market_values(receipt)
        serialized = json.dumps(receipt, ensure_ascii=False)
        self.assertNotIn("123456.78", serialized)
        self.assertNotIn("234567.89", serialized)
        self.assertNotIn("345678.90", serialized)

    def test_output_does_not_encode_up_or_down_direction(self):
        rising = self.receipt([
            row("093000000", sequence_no="1", trade_price="100.00"),
            row("150000000", sequence_no="2", trade_price="101.00"),
            row("153000000", sequence_no="3", trade_price="102.00"),
        ])
        (self.raw_dir / "2025-01.csv").unlink()
        falling = self.receipt([
            row("093000000", sequence_no="1", trade_price="102.00"),
            row("150000000", sequence_no="2", trade_price="101.00"),
            row("153000000", sequence_no="3", trade_price="100.00"),
        ])
        rising["files"][0]["sha256"] = None
        falling["files"][0]["sha256"] = None
        self.assertEqual(rising, falling)

    def assert_no_market_values(self, receipt):
        forbidden = {"price", "trade_price", "return", "sign", "direction", "long", "short", "pnl"}
        def check(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    self.assertNotIn(key.lower(), forbidden)
                    check(child)
            elif isinstance(value, list):
                for child in value:
                    check(child)
        check(receipt)


if __name__ == "__main__":
    unittest.main()
