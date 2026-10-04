import json
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest.mock import Mock

from holdout_loader import load_holdout
from imom_core import (
    AmbiguousTrade, Contract, DegenerateSample, JST, Observation, Trade,
    bootstrap_beta, bootstrap_signed_mean, build_observation, evaluate_sample,
    first_trade_at_or_after, ols_beta, quarterly_front, same_front_across_dates,
)


def dt(d, h, m, s=0):
    return datetime(d.year, d.month, d.day, h, m, s, tzinfo=JST)


class TestIMOMCore(unittest.TestCase):
    def test_front_contract_and_roll_transition(self):
        contracts = [
            Contract("2025-03", date(2025, 3, 13)),
            Contract("2025-06", date(2025, 6, 12)),
        ]
        self.assertEqual(quarterly_front(date(2025, 3, 12), contracts).code, "2025-03")
        self.assertEqual(quarterly_front(date(2025, 3, 14), contracts).code, "2025-06")
        self.assertEqual(
            same_front_across_dates(date(2025, 3, 11), date(2025, 3, 12), contracts),
            "2025-03",
        )
        self.assertIsNone(
            same_front_across_dates(date(2025, 3, 13), date(2025, 3, 14), contracts)
        )

    def test_mapping_first_trade_within_60_seconds(self):
        d = date(2025, 1, 6)
        b = dt(d, 9, 30)
        trades = [
            Trade(b + timedelta(seconds=61), 101),
            Trade(b + timedelta(seconds=30), 100),
        ]
        self.assertEqual(first_trade_at_or_after(trades, b).price, 100)

    def test_mapping_none_after_window(self):
        d = date(2025, 1, 6)
        b = dt(d, 9, 30)
        self.assertIsNone(first_trade_at_or_after([Trade(b + timedelta(seconds=61), 100)], b))

    def test_ambiguous_same_time_requires_order(self):
        d = date(2025, 1, 6)
        b = dt(d, 9, 30)
        with self.assertRaises(AmbiguousTrade):
            first_trade_at_or_after([Trade(b, 100), Trade(b, 101)], b)

    def test_source_order_resolves_same_time(self):
        d = date(2025, 1, 6)
        b = dt(d, 9, 30)
        t = first_trade_at_or_after([
            Trade(b, 101, 2),
            Trade(b, 100, 1),
        ], b)
        self.assertEqual(t.price, 100)

    def test_build_observation_long_and_short(self):
        prev, cur = date(2025, 1, 6), date(2025, 1, 7)
        trades = [
            Trade(dt(prev, 15, 30), 100),
            Trade(dt(cur, 9, 30), 102),
            Trade(dt(cur, 15, 0), 200),
            Trade(dt(cur, 15, 30), 202),
        ]
        o = build_observation(prev, cur, "2025-03", trades)
        self.assertAlmostEqual(o.early_return, 0.02)
        self.assertAlmostEqual(o.late_return, 0.01)
        self.assertAlmostEqual(o.signed_return, 0.01)
        self.assertEqual(o.signed_points, 2)

    def test_missing_boundary_makes_day_unavailable(self):
        prev, cur = date(2025, 1, 6), date(2025, 1, 7)
        trades = [
            Trade(dt(prev, 15, 30), 100),
            Trade(dt(cur, 9, 30), 102),
            Trade(dt(cur, 15, 0), 200),
        ]
        self.assertIsNone(build_observation(prev, cur, "2025-03", trades))

    def test_ols(self):
        alpha, beta = ols_beta([1, 2, 3], [3, 5, 7])
        self.assertAlmostEqual(alpha, 1)
        self.assertAlmostEqual(beta, 2)
        with self.assertRaises(DegenerateSample):
            ols_beta([1, 1, 1], [1, 2, 3])

    def positive_observations(self, n=220):
        rows = []
        for i in range(n):
            x = (i - n / 2) / 10000
            y = 0.25 * x + 0.0002
            signed = y if x > 0 else (-y if x < 0 else None)
            rows.append(Observation(
                trade_date=date(2025, 1, 1) + timedelta(days=i),
                contract="Q",
                early_return=x,
                late_return=y,
                signed_return=signed,
                signed_points=None if signed is None else signed * 30000,
            ))
        return rows

    def test_bootstraps_deterministic(self):
        rows = self.positive_observations()
        self.assertEqual(bootstrap_beta(rows), bootstrap_beta(rows))
        self.assertEqual(bootstrap_signed_mean(rows), bootstrap_signed_mean(rows))

    def test_supported_and_negative(self):
        rows = self.positive_observations()
        r = evaluate_sample(rows, 180)
        self.assertEqual(r["status"], "SUPPORTED")
        negative = [
            Observation(o.trade_date, o.contract, o.early_return, -o.late_return,
                        -o.signed_return if o.signed_return is not None else None,
                        -o.signed_points if o.signed_points is not None else None)
            for o in rows
        ]
        self.assertEqual(evaluate_sample(negative, 180)["status"], "NOT_SUPPORTED")

    def test_insufficient(self):
        self.assertEqual(evaluate_sample(self.positive_observations(50), 180)["status"],
                         "INSUFFICIENT_EVENTS")


class TestHoldoutGuard(unittest.TestCase):
    def test_reader_not_called_when_locked(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "decision.json"
            p.write_text(json.dumps({
                "confirmation_advancement": False,
                "classification": "IMOM_NOT_SUPPORTED_2025",
                "sample": "2025_CONFIRMATION",
                "binding": {},
            }, sort_keys=True, separators=(",", ":")))
            import hashlib
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            reader = Mock()
            with self.assertRaises(PermissionError):
                load_holdout("NONEXISTENT_2026", p, sha, {}, reader)
            reader.assert_not_called()


if __name__ == "__main__":
    unittest.main()
