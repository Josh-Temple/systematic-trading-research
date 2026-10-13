import unittest
from datetime import date, datetime, timedelta, timezone

from forecast_core import (
    Quote,
    TOKYO,
    absolute_error_bps,
    binary_up,
    brier_score,
    canonical_sha256,
    overnight_event_times,
    realized_return_bps,
    reject_future_information,
    select_first_quote_at_or_after,
    select_last_quote_at_or_before,
    validate_probability,
    weekly_event_times,
)


class ForecastCoreTests(unittest.TestCase):
    def test_quote_mid(self):
        q = Quote(datetime(2026, 10, 5, 13, 0, tzinfo=timezone.utc), 157.80, 157.82)
        self.assertAlmostEqual(q.mid, 157.81)

    def test_quote_rejects_naive_time(self):
        with self.assertRaises(ValueError):
            Quote(datetime(2026, 10, 5, 13, 0), 157.80, 157.82)

    def test_quote_rejects_crossed_market(self):
        with self.assertRaises(ValueError):
            Quote(datetime(2026, 10, 5, 13, 0, tzinfo=timezone.utc), 157.82, 157.80)

    def test_overnight_window(self):
        got = overnight_event_times(date(2026, 10, 5))
        self.assertEqual((got.forecast_cutoff.hour, got.target_end.hour), (22, 8))
        self.assertEqual(got.forecast_cutoff.tzinfo, TOKYO)
        self.assertEqual(got.target_end.date(), date(2026, 10, 6))

    def test_overnight_rejects_friday(self):
        with self.assertRaises(ValueError):
            overnight_event_times(date(2026, 10, 9))

    def test_weekly_window(self):
        got = weekly_event_times(date(2026, 10, 11))
        self.assertEqual(got.forecast_cutoff, datetime(2026, 10, 11, 20, 0, tzinfo=TOKYO))
        self.assertEqual(got.target_start, datetime(2026, 10, 12, 8, 0, tzinfo=TOKYO))
        self.assertEqual(got.target_end, datetime(2026, 10, 16, 22, 0, tzinfo=TOKYO))
        self.assertLess(got.forecast_cutoff, got.target_start)

    def test_weekly_rejects_non_sunday(self):
        with self.assertRaises(ValueError):
            weekly_event_times(date(2026, 10, 12))

    def test_last_quote_exact_boundary(self):
        target = datetime(2026, 10, 5, 22, 0, tzinfo=TOKYO)
        q = Quote(target, 157.0, 157.02)
        self.assertIs(select_last_quote_at_or_before([q], target), q)

    def test_last_quote_60_seconds_allowed(self):
        target = datetime(2026, 10, 5, 22, 0, tzinfo=TOKYO)
        q = Quote(target - timedelta(seconds=60), 157.0, 157.02)
        self.assertIs(select_last_quote_at_or_before([q], target), q)

    def test_last_quote_61_seconds_rejected(self):
        target = datetime(2026, 10, 5, 22, 0, tzinfo=TOKYO)
        q = Quote(target - timedelta(seconds=61), 157.0, 157.02)
        self.assertIsNone(select_last_quote_at_or_before([q], target))

    def test_first_quote_60_seconds_allowed(self):
        target = datetime(2026, 10, 6, 8, 0, tzinfo=TOKYO)
        q = Quote(target + timedelta(seconds=60), 157.0, 157.02)
        self.assertIs(select_first_quote_at_or_after([q], target), q)

    def test_first_quote_61_seconds_rejected(self):
        target = datetime(2026, 10, 6, 8, 0, tzinfo=TOKYO)
        q = Quote(target + timedelta(seconds=61), 157.0, 157.02)
        self.assertIsNone(select_first_quote_at_or_after([q], target))

    def test_binary_equal_is_non_up(self):
        t = datetime(2026, 10, 5, tzinfo=timezone.utc)
        a = Quote(t, 157.0, 157.02)
        b = Quote(t + timedelta(hours=10), 157.0, 157.02)
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
        cutoff = datetime(2026, 10, 4, 20, 0, tzinfo=TOKYO)
        with self.assertRaises(PermissionError):
            reject_future_information(
                [{"available_at": cutoff + timedelta(seconds=1)}],
                cutoff,
            )

    def test_pre_cutoff_schedule_metadata_allowed(self):
        cutoff = datetime(2026, 10, 4, 20, 0, tzinfo=TOKYO)
        reject_future_information(
            [{"available_at": cutoff - timedelta(minutes=5), "scheduled_for": cutoff + timedelta(days=3)}],
            cutoff,
        )

    def test_hash_is_key_order_independent(self):
        self.assertEqual(canonical_sha256({"a": 1, "b": 2}), canonical_sha256({"b": 2, "a": 1}))


if __name__ == "__main__":
    unittest.main()
