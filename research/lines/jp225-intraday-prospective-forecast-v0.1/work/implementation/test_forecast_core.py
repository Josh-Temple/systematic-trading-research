import unittest
from datetime import date, datetime, timedelta, timezone

from forecast_core import (
    Quote,
    TOKYO,
    absolute_error_bps,
    binary_up,
    brier_score,
    canonical_sha256,
    intraday_event_times,
    realized_return_bps,
    reject_future_information,
    select_first_quote_at_or_after,
    select_last_quote_at_or_before,
    validate_probability,
)


class ForecastCoreTests(unittest.TestCase):
    def test_quote_mid(self):
        q = Quote(datetime(2026, 10, 6, 0, 0, tzinfo=timezone.utc), 50000.0, 50002.0)
        self.assertAlmostEqual(q.mid, 50001.0)

    def test_quote_rejects_naive_time(self):
        with self.assertRaises(ValueError):
            Quote(datetime(2026, 10, 6, 0, 0), 50000.0, 50002.0)

    def test_quote_rejects_crossed_market(self):
        with self.assertRaises(ValueError):
            Quote(datetime(2026, 10, 6, 0, 0, tzinfo=timezone.utc), 50002.0, 50000.0)

    def test_intraday_window(self):
        got = intraday_event_times(date(2026, 10, 6), scheduled_jpx_trading_day=True)
        self.assertEqual(got.forecast_cutoff, datetime(2026, 10, 6, 9, 0, tzinfo=TOKYO))
        self.assertEqual(got.target_end, datetime(2026, 10, 6, 15, 30, tzinfo=TOKYO))
        self.assertEqual(got.forecast_cutoff, got.target_start)

    def test_intraday_rejects_weekend(self):
        with self.assertRaises(ValueError):
            intraday_event_times(date(2026, 10, 10), scheduled_jpx_trading_day=True)

    def test_intraday_rejects_non_trading_day(self):
        with self.assertRaises(ValueError):
            intraday_event_times(date(2026, 10, 12), scheduled_jpx_trading_day=False)

    def test_last_quote_exact_boundary(self):
        target = datetime(2026, 10, 6, 9, 0, tzinfo=TOKYO)
        q = Quote(target, 50000.0, 50002.0)
        self.assertIs(select_last_quote_at_or_before([q], target), q)

    def test_last_quote_60_seconds_allowed(self):
        target = datetime(2026, 10, 6, 9, 0, tzinfo=TOKYO)
        q = Quote(target - timedelta(seconds=60), 50000.0, 50002.0)
        self.assertIs(select_last_quote_at_or_before([q], target), q)

    def test_last_quote_61_seconds_rejected(self):
        target = datetime(2026, 10, 6, 9, 0, tzinfo=TOKYO)
        q = Quote(target - timedelta(seconds=61), 50000.0, 50002.0)
        self.assertIsNone(select_last_quote_at_or_before([q], target))

    def test_first_quote_60_seconds_allowed(self):
        target = datetime(2026, 10, 6, 15, 30, tzinfo=TOKYO)
        q = Quote(target + timedelta(seconds=60), 50000.0, 50002.0)
        self.assertIs(select_first_quote_at_or_after([q], target), q)

    def test_first_quote_61_seconds_rejected(self):
        target = datetime(2026, 10, 6, 15, 30, tzinfo=TOKYO)
        q = Quote(target + timedelta(seconds=61), 50000.0, 50002.0)
        self.assertIsNone(select_first_quote_at_or_after([q], target))

    def test_binary_equal_is_non_up(self):
        t = datetime(2026, 10, 6, 9, 0, tzinfo=TOKYO)
        a = Quote(t, 50000.0, 50002.0)
        b = Quote(t + timedelta(hours=6, minutes=30), 50000.0, 50002.0)
        self.assertEqual(binary_up(a, b), 0)
        self.assertAlmostEqual(realized_return_bps(a, b), 0.0)

    def test_brier(self):
        self.assertAlmostEqual(brier_score(0.70, 1), 0.09)
        self.assertAlmostEqual(brier_score(0.30, 0), 0.09)

    def test_probability_bounds(self):
        self.assertEqual(validate_probability(0.01), 0.01)
        self.assertEqual(validate_probability(0.99), 0.99)
        for value in (0.0, 1.0, float("nan")):
            with self.assertRaises(ValueError):
                validate_probability(value)

    def test_absolute_error(self):
        self.assertEqual(absolute_error_bps(-15.0, 10.0), 25.0)

    def test_future_information_rejected(self):
        cutoff = datetime(2026, 10, 6, 9, 0, tzinfo=TOKYO)
        with self.assertRaises(PermissionError):
            reject_future_information(
                [{"available_at": cutoff + timedelta(seconds=1)}],
                cutoff,
            )

    def test_pre_cutoff_schedule_metadata_allowed(self):
        cutoff = datetime(2026, 10, 6, 9, 0, tzinfo=TOKYO)
        reject_future_information(
            [{"available_at": cutoff - timedelta(minutes=5),
              "scheduled_for": cutoff + timedelta(hours=3)}],
            cutoff,
        )

    def test_hash_is_key_order_independent(self):
        self.assertEqual(
            canonical_sha256({"a": 1, "b": 2}),
            canonical_sha256({"b": 2, "a": 1}),
        )


if __name__ == "__main__":
    unittest.main()
