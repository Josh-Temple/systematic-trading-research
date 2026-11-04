import random
import unittest
from dataclasses import replace
from cost_fixture import (EvidenceHold, RoundTrip, SelectionManifest,
                          roundtrip_pnl, select_training_winner,
                          validate_synthetic_bars)


class CostTests(unittest.TestCase):
    def setUp(self):
        self.t = RoundTrip(1, 2, 100, 101)

    def test_zero_cost(self):
        self.assertEqual(roundtrip_pnl(self.t)["net"], 2)

    def test_all_components_both_fills(self):
        t = replace(self.t, entry_half_spread=.1, exit_half_spread=.2,
                    entry_slippage=.05, exit_slippage=.05,
                    entry_impact=.02, exit_impact=.03,
                    entry_fee=.4, exit_fee=.6, funding_charge=.3)
        a = roundtrip_pnl(t)
        for name, expected in {"spread": .6, "slippage": .2, "impact": .1,
                               "fees": 1.0, "funding": .3,
                               "total_cost": 2.2, "net": -.2}.items():
            self.assertAlmostEqual(a[name], expected)

    def test_nonnegative_cost_monotonicity(self):
        for name in ("entry_half_spread", "exit_half_spread", "entry_slippage",
                     "exit_slippage", "entry_impact", "exit_impact",
                     "entry_fee", "exit_fee", "funding_charge"):
            with self.subTest(name=name):
                t = replace(self.t, **{name: .01})
                self.assertLess(roundtrip_pnl(t)["net"], 2)

    def test_short_and_zero_turnover(self):
        self.assertEqual(roundtrip_pnl(replace(self.t, side=-1))["gross"], -2)
        self.assertEqual(roundtrip_pnl(replace(self.t, quantity=0,
                                entry_half_spread=4, exit_half_spread=4))["net"], 0)
        with self.assertRaises(EvidenceHold):
            roundtrip_pnl(replace(self.t, quantity=0, entry_fee=1))

    def test_invalid_numbers_and_overflow(self):
        for name, value in (("side", 0), ("side", True), ("quantity", -1),
                            ("quantity", True), ("entry_mid", 0),
                            ("exit_mid", float("nan")),
                            ("entry_half_spread", -1),
                            ("exit_fee", float("inf"))):
            with self.subTest(name=name), self.assertRaises(EvidenceHold):
                roundtrip_pnl(replace(self.t, **{name: value}))
        with self.assertRaises(EvidenceHold):
            roundtrip_pnl(RoundTrip(1, 1e308, 1, 1e308))

    def test_timestamp_validation(self):
        good = [("2026-01-01T00:00:00+00:00", 100),
                ("2026-01-01T00:01:00+00:00", 101)]
        validate_synthetic_bars(good)
        for bad in (good[::-1], good[:1]*2, [],
                    [("2026-01-01T00:00:00", 100)],
                    [("2026-01-01T00:00:00+00:00", -1)],
                    [("2026-01-01T00:00:00+00:00", None)]):
            with self.subTest(bad=bad), self.assertRaises(EvidenceHold):
                validate_synthetic_bars(bad)


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.m = SelectionManifest("SYNTHETIC", "trainA", "evalB", ("A", "B", "C"))

    def test_selection_no_evaluation_argument(self):
        scores = {"A": -.2, "B": .8, "C": .8}
        self.assertEqual(select_training_winner(scores, self.m), "B")
        # There is intentionally no evaluation-series argument in select_training_winner.

    def test_split_registry_and_input_holds(self):
        invalid = [replace(self.m, source_kind="REAL"),
                   replace(self.m, evaluation_sample_id="trainA"),
                   replace(self.m, evaluation_sample_id=""),
                   replace(self.m, candidate_ids=("A", "A")),
                   replace(self.m, candidate_ids=())]
        for manifest in invalid:
            with self.subTest(manifest=manifest), self.assertRaises(EvidenceHold):
                select_training_winner({"A": 1, "B": 2, "C": 3}, manifest)
        for scores in ({"A": 1, "B": 2},
                       {"A": 1, "B": 2, "C": 3, "D": 4},
                       {"A": 1, "B": float("nan"), "C": 3}):
            with self.subTest(scores=scores), self.assertRaises(EvidenceHold):
                select_training_winner(scores, self.m)

    def test_iid_null_many_candidates_didactic(self):
        rng = random.Random(20261104)
        selection, evaluation = [], []
        for _ in range(200):
            train = [sum(rng.gauss(0, 1) for _ in range(80))/80 for _ in range(50)]
            idx = max(range(50), key=train.__getitem__)
            selection.append(train[idx])
            evaluation.append(sum(rng.gauss(0, 1) for _ in range(80))/80)
        self.assertGreater(sum(selection)/len(selection), .15)
        self.assertLess(abs(sum(evaluation)/len(evaluation)), .05)


if __name__ == "__main__":
    unittest.main()
