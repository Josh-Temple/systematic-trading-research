import unittest
from datetime import date

from strategy_semantics import (
    breakout_signal,
    ny_close_jst,
    review_delay_hours,
    review_window_jst,
    validate_exit_mode,
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

    def test_exit_mode_requires_one_explicit_choice(self):
        self.assertEqual(validate_exit_mode("WEEKEND_FLAT"), "WEEKEND_FLAT")
        self.assertEqual(validate_exit_mode("TEN_CHECK_HOLD"), "TEN_CHECK_HOLD")
        for bad in ("", "BOTH", "AUTO", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                validate_exit_mode(bad)


if __name__ == "__main__":
    unittest.main()