import hashlib
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
from run_confirmation import _load_input, canonical, code_identity, digest, run, spec_identity


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

    def test_build_observation_long(self):
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

    def test_build_observation_short(self):
        prev, cur = date(2025, 1, 6), date(2025, 1, 7)
        trades = [
            Trade(dt(prev, 15, 30), 100),
            Trade(dt(cur, 9, 30), 98),
            Trade(dt(cur, 15, 0), 200),
            Trade(dt(cur, 15, 30), 198),
        ]
        o = build_observation(prev, cur, "2025-03", trades)
        self.assertLess(o.early_return, 0)
        self.assertLess(o.late_return, 0)
        self.assertGreater(o.signed_return, 0)
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
            y = 0.25 * x
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
        self.assertEqual(evaluate_sample(rows, 180)["status"], "SUPPORTED")
        negative = [
            Observation(
                o.trade_date, o.contract, o.early_return, -o.late_return,
                -o.signed_return if o.signed_return is not None else None,
                -o.signed_points if o.signed_points is not None else None,
            )
            for o in rows
        ]
        self.assertEqual(evaluate_sample(negative, 180)["status"], "NOT_SUPPORTED")

    def test_degenerate_is_nonadvancing_status(self):
        rows = [
            Observation(date(2025, 1, 1) + timedelta(days=i), "Q", 1.0, float(i), 1.0, 1.0)
            for i in range(180)
        ]
        r = evaluate_sample(rows, 180)
        self.assertEqual(r["status"], "BOOTSTRAP_DEGENERATE")

    def test_insufficient(self):
        self.assertEqual(
            evaluate_sample(self.positive_observations(50), 180)["status"],
            "INSUFFICIENT_EVENTS",
        )


class TestConfirmationInput(unittest.TestCase):
    def _envelope(self, source_sha):
        return {
            "version": "JP225_IMOM_MAPPED_POINTS_v1",
            "sample": "2025_CONFIRMATION",
            "source_manifest_sha256": source_sha,
            "rows": [{
                "date": "2025-01-07",
                "previous_date": "2025-01-06",
                "contract": "2025-03",
                "p_prev_1530": 100.0,
                "p_0930": 102.0,
                "p_1500": 200.0,
                "p_1530": 202.0,
            }],
        }

    def test_returns_recomputed_from_raw_mapped_prices(self):
        source_sha = "a" * 64
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "input.json"
            p.write_bytes(canonical(self._envelope(source_sha)))
            rows = _load_input(p, source_sha)
            self.assertAlmostEqual(rows[0].early_return, 0.02)
            self.assertAlmostEqual(rows[0].late_return, 0.01)
            self.assertAlmostEqual(rows[0].signed_return, 0.01)

    def test_source_manifest_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "input.json"
            p.write_bytes(canonical(self._envelope("b" * 64)))
            with self.assertRaises(ValueError):
                _load_input(p, "a" * 64)


    def test_gate_is_checked_before_input_file_is_opened(self):
        source_sha = "a" * 64
        expected_input_sha = "b" * 64
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            missing_input = root / "missing-input.json"
            identity = {
                "spec_sha256": spec_identity(),
                "code_sha256": code_identity(),
                "input_sha256": expected_input_sha,
                "source_manifest_sha256": source_sha,
            }
            gate = root / "gate.json"
            gate.write_bytes(canonical({
                "status": "FAIL",
                "independent_review": "FAIL",
                "sample": "2025_CONFIRMATION",
                "binding": identity,
            }))
            gate_sha = digest(gate)
            with self.assertRaisesRegex(PermissionError, "CONFIRMATION_GATE_CLOSED"):
                run(
                    missing_input,
                    gate,
                    gate_sha,
                    expected_input_sha,
                    source_sha,
                    root / "out",
                )
            self.assertFalse(Path(str(missing_input) + ".CONSUMED.json").exists())

    def test_one_shot_insufficient_run_and_consumption_marker(self):
        source_sha = "a" * 64
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inp = root / "input.json"
            inp.write_bytes(canonical(self._envelope(source_sha)))
            identity = {
                "spec_sha256": spec_identity(),
                "code_sha256": code_identity(),
                "input_sha256": digest(inp),
                "source_manifest_sha256": source_sha,
            }
            gate = root / "gate.json"
            gate.write_bytes(canonical({
                "status": "PASS",
                "independent_review": "PASS",
                "sample": "2025_CONFIRMATION",
                "binding": identity,
            }))
            gate_sha = digest(gate)
            out = root / "out"
            result = run(inp, gate, gate_sha, digest(inp), source_sha, out)
            self.assertEqual(result["classification"], "INSUFFICIENT_2025_EVENTS")
            self.assertTrue(Path(str(inp) + ".CONSUMED.json").exists())
            with self.assertRaises(FileExistsError):
                run(inp, gate, gate_sha, digest(inp), source_sha, root / "other-out")


class TestHoldoutGuard(unittest.TestCase):
    def _binding(self):
        return {
            "spec_sha256": "1" * 64,
            "code_sha256": "2" * 64,
            "input_sha256": "3" * 64,
            "source_manifest_sha256": "4" * 64,
            "result_sha256": "5" * 64,
        }

    def test_reader_not_called_when_decision_does_not_advance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            decision = root / "decision.json"
            decision.write_bytes(canonical({
                "confirmation_advancement": False,
                "classification": "IMOM_NOT_SUPPORTED_2025",
                "sample": "2025_CONFIRMATION",
                "binding": self._binding(),
            }))
            decision_sha = hashlib.sha256(decision.read_bytes()).hexdigest()
            reader = Mock()
            with self.assertRaises(PermissionError):
                load_holdout(
                    "NONEXISTENT_2026",
                    decision,
                    decision_sha,
                    root / "nonexistent-audit.json",
                    "a" * 64,
                    self._binding(),
                    reader,
                )
            reader.assert_not_called()

    def test_reader_requires_and_accepts_bound_independent_audit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            binding = self._binding()
            decision = root / "decision.json"
            decision.write_bytes(canonical({
                "confirmation_advancement": True,
                "classification": "IMOM_ADVANCE_TO_2026_HOLDOUT",
                "sample": "2025_CONFIRMATION",
                "binding": binding,
            }))
            decision_sha = hashlib.sha256(decision.read_bytes()).hexdigest()
            audit = root / "audit.json"
            audit.write_bytes(canonical({
                "status": "PASS",
                "independent_review": "PASS",
                "scope": "2026_HOLDOUT_UNLOCK",
                "sample": "2025_CONFIRMATION",
                "decision_sha256": decision_sha,
                "binding": binding,
            }))
            audit_sha = hashlib.sha256(audit.read_bytes()).hexdigest()

            reader = Mock(return_value="HOLDOUT_BYTES")
            self.assertEqual(
                load_holdout(
                    "2026_PATH", decision, decision_sha, audit, audit_sha, binding, reader
                ),
                "HOLDOUT_BYTES",
            )
            reader.assert_called_once_with("2026_PATH")

            tampered = root / "tampered-audit.json"
            tampered.write_bytes(canonical({
                "status": "PASS",
                "independent_review": "FAIL",
                "scope": "2026_HOLDOUT_UNLOCK",
                "sample": "2025_CONFIRMATION",
                "decision_sha256": decision_sha,
                "binding": binding,
            }))
            bad_sha = hashlib.sha256(tampered.read_bytes()).hexdigest()
            reader2 = Mock()
            with self.assertRaises(PermissionError):
                load_holdout(
                    "2026_PATH", decision, decision_sha, tampered, bad_sha, binding, reader2
                )
            reader2.assert_not_called()


if __name__ == "__main__":
    unittest.main()
