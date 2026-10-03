import unittest
from datetime import date, datetime

from strategy_semantics import (
    JST,
    breakout_signal,
    is_new_entry_allowed,
    ny_close_jst,
    review_delay_hours,
    review_window_jst,
    validate_exit_mode,
    weekend_forced_exit_at,
)


class BreakoutSemanticsTests(unittest.TestCase):
    def bars(self):
        return [{"high": 110 + i, "low": 90 - i, "close": 100} for i in range(20)]

    def test_requires_20_prior_bars_plus_signal_day(self):
        self.assertEqual(breakout_signal(self.bars()), "INSUFFICIENT")

    def test_long_uses_prior_20_and_excludes_signal_day_high(self):
        prior = self.bars()
        prior_high = max(b["high"] for b in prior)
        current = {"high": prior_high + 50, "low": 80, "close": prior_high + 1}
        self.assertEqual(breakout_signal(prior + [current]), "LONG")

    def test_equal_prior_high_is_not_breakout(self):
        prior = self.bars()
        prior_high = max(b["high"] for b in prior)
        current = {"high": prior_high + 10, "low": 80, "close": prior_high}
        self.assertEqual(breakout_signal(prior + [current]), "NONE")

    def test_short_is_strict(self):
        prior = self.bars()
        prior_low = min(b["low"] for b in prior)
        current = {"high": 120, "low": prior_low - 5, "close": prior_low - 1}
        self.assertEqual(breakout_signal(prior + [current]), "SHORT")

    def test_dst_summer_close_and_delay(self):
        close = ny_close_jst(date(2026, 7, 1))
        self.assertEqual((close.hour, close.minute), (6, 0))
        self.assertEqual(review_delay_hours(date(2026, 7, 1)), 14.0)

    def test_dst_winter_close_and_delay(self):
        close = ny_close_jst(date(2026, 1, 15))
        self.assertEqual((close.hour, close.minute), (7, 0))
        self.assertEqual(review_delay_hours(date(2026, 1, 15)), 13.0)

    def test_review_window_is_five_minutes(self):
        start, end = review_window_jst(date(2026, 7, 1))
        self.assertEqual((start.hour, start.minute), (20, 0))
        self.assertEqual((end - start).total_seconds(), 300)

    def test_exit_mode_is_fixed_to_weekend_flat(self):
        self.assertEqual(validate_exit_mode("WEEKEND_FLAT"), "WEEKEND_FLAT")
        for bad in ("TEN_CHECK_HOLD", "", "BOTH", "AUTO", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                validate_exit_mode(bad)

    def test_friday_new_entry_is_disabled(self):
        friday = datetime(2026, 10, 2, 20, 0, tzinfo=JST)
        self.assertFalse(is_new_entry_allowed(friday))

    def test_monday_through_thursday_entries_are_eligible(self):
        for day in (5, 6, 7, 8):
            with self.subTest(day=day):
                review = datetime(2026, 10, day, 20, 0, tzinfo=JST)
                self.assertTrue(is_new_entry_allowed(review))

    def test_friday_forced_exit_request_is_2300_jst(self):
        friday = date(2026, 10, 2)
        exit_at = weekend_forced_exit_at(friday)
        self.assertEqual((exit_at.hour, exit_at.minute), (23, 0))
        self.assertEqual(exit_at.tzinfo, JST)
        self.assertIsNone(weekend_forced_exit_at(date(2026, 10, 1)))


if __name__ == "__main__":
    unittest.main()
