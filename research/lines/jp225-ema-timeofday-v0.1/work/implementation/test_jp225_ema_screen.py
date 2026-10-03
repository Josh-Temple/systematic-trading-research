import unittest
from datetime import datetime, timedelta, timezone

from jp225_ema_screen import (
    Quote,
    authorize_holdout_candidate,
    cluster_bootstrap_mean,
    crossover_directions,
    evaluate_holdout_gate,
    map_executable_outcome,
    price_slow_crossover_directions,
    recursive_ema,
    select_discovery_candidate,
    time_flags,
)


class TestJP225EMAScreen(unittest.TestCase):
    def test_ema_recursion(self):
        self.assertEqual(recursive_ema([1, 2, 3], 3), [1.0, 1.5, 2.25])

    def test_long_cross_from_equality(self):
        self.assertEqual(crossover_directions([1, 2], [1, 1.5]), [0, 1])

    def test_short_cross(self):
        self.assertEqual(crossover_directions([2, 1], [1.5, 1.5]), [0, -1])

    def test_price_comparator(self):
        self.assertEqual(price_slow_crossover_directions([1, 2], [1, 1.5]), [0, 1])

    def test_no_missing_bar_fabrication(self):
        self.assertEqual(len(recursive_ema([100, 102], 5)), 2)

    def test_tokyo_open_boundaries(self):
        jst = timezone(timedelta(hours=9))
        self.assertIn("TOKYO_OPEN_30", time_flags(datetime(2026, 1, 5, 8, 45, tzinfo=jst)))
        self.assertNotIn("TOKYO_OPEN_30", time_flags(datetime(2026, 1, 5, 9, 15, tzinfo=jst)))

    def test_tokyo_close_boundaries(self):
        jst = timezone(timedelta(hours=9))
        self.assertIn("TOKYO_CLOSE_30", time_flags(datetime(2026, 1, 5, 15, 15, tzinfo=jst)))
        self.assertNotIn("TOKYO_CLOSE_30", time_flags(datetime(2026, 1, 5, 15, 45, tzinfo=jst)))

    def test_us_dst_spring(self):
        self.assertIn("US_CASH_OPEN_60", time_flags(datetime(2026, 3, 16, 13, 30, tzinfo=timezone.utc)))

    def test_us_standard_time(self):
        self.assertIn("US_CASH_OPEN_60", time_flags(datetime(2026, 1, 5, 14, 30, tzinfo=timezone.utc)))

    def test_long_execution_ask_to_bid(self):
        t = datetime(2026, 1, 5, tzinfo=timezone.utc)
        qs = [Quote(t + timedelta(seconds=1), 100, 101), Quote(t + timedelta(minutes=15), 110, 111)]
        got = map_executable_outcome(qs, t, 1, 15)
        self.assertEqual((got.status, got.entry_price, got.exit_price, got.net_points), ("OK", 101, 110, 9))

    def test_short_execution_bid_to_ask(self):
        t = datetime(2026, 1, 5, tzinfo=timezone.utc)
        qs = [Quote(t + timedelta(seconds=1), 100, 101), Quote(t + timedelta(minutes=15), 90, 91)]
        got = map_executable_outcome(qs, t, -1, 15)
        self.assertEqual((got.entry_price, got.exit_price, got.net_points), (100, 91, 9))

    def test_missing_entry(self):
        t = datetime(2026, 1, 5, tzinfo=timezone.utc)
        got = map_executable_outcome([Quote(t + timedelta(seconds=61), 100, 101)], t, 1, 15)
        self.assertEqual(got.status, "NO_EXECUTABLE_ENTRY_QUOTE")

    def test_missing_target(self):
        t = datetime(2026, 1, 5, tzinfo=timezone.utc)
        qs = [Quote(t + timedelta(seconds=1), 100, 101), Quote(t + timedelta(minutes=15, seconds=61), 110, 111)]
        self.assertEqual(map_executable_outcome(qs, t, 1, 15).status, "NO_EXECUTABLE_TARGET_QUOTE")

    def test_exact_target_quote(self):
        t = datetime(2026, 1, 5, tzinfo=timezone.utc)
        qs = [Quote(t + timedelta(seconds=1), 100, 101), Quote(t + timedelta(minutes=15), 102, 103)]
        self.assertEqual(map_executable_outcome(qs, t, 1, 15).exit_timestamp, t + timedelta(minutes=15))

    def test_first_after_target(self):
        t = datetime(2026, 1, 5, tzinfo=timezone.utc)
        qs = [
            Quote(t + timedelta(seconds=1), 100, 101),
            Quote(t + timedelta(minutes=15, seconds=20), 102, 103),
            Quote(t + timedelta(minutes=15, seconds=30), 104, 105),
        ]
        self.assertEqual(map_executable_outcome(qs, t, 1, 15).exit_timestamp, t + timedelta(minutes=15, seconds=20))

    def test_bootstrap_seed_deterministic(self):
        data = {1: [1.0, 2.0], 2: [-1.0, 0.5], 3: [3.0]}
        self.assertEqual(cluster_bootstrap_mean(data, reps=100), cluster_bootstrap_mean(data, reps=100))

    def test_discovery_tie_prefers_broader(self):
        m = {
            "ALL": {"event_count": 120, "distinct_dates": 80, "mean_net_points": 1.00, "ci_lower": 0.1},
            "TOKYO_OPEN_30": {"event_count": 110, "distinct_dates": 70, "mean_net_points": 1.005, "ci_lower": 0.1},
        }
        self.assertEqual(select_discovery_candidate(m), "ALL")

    def test_no_advancement(self):
        m = {"ALL": {"event_count": 120, "distinct_dates": 80, "mean_net_points": 1.0, "ci_lower": -0.01}}
        self.assertIsNone(select_discovery_candidate(m))

    def test_holdout_locked_without_advancement(self):
        with self.assertRaises(PermissionError):
            authorize_holdout_candidate(None)

    def test_holdout_gate(self):
        self.assertEqual(evaluate_holdout_gate(60, 40, 0.2, 0.05), "SUPPORTED_IN_HOLDOUT")
        self.assertEqual(evaluate_holdout_gate(60, 40, 0.2, -0.01), "NOT_SUPPORTED_IN_HOLDOUT")
        self.assertEqual(evaluate_holdout_gate(49, 40, 0.2, 0.05), "INSUFFICIENT_HOLDOUT_EVENTS")


if __name__ == "__main__":
    unittest.main()
