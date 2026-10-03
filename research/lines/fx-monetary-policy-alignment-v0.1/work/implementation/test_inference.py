from __future__ import annotations

import math
import unittest

from inference import (
    InferenceConfig,
    InferenceError,
    difference,
    draw_circular_indices,
    evaluate,
    normalize_grid,
    type7_percentile,
)


class InferenceTests(unittest.TestCase):
    def test_type7_known_value(self):
        self.assertEqual(type7_percentile([0.0, 10.0], 0.25), 2.5)
        self.assertEqual(type7_percentile([0.0, 10.0], 0.5), 5.0)

    def test_circular_draw_has_exact_grid_length(self):
        import random
        rng = random.Random(123)
        idx = draw_circular_indices(25, 12, rng)
        self.assertEqual(len(idx), 25)
        self.assertTrue(all(0 <= i < 25 for i in idx))

    def test_constant_group_difference_is_exact(self):
        grid = []
        for i in range(24):
            grid.append({"slot_id": f"a{i}", "classification": "ALIGNED", "y": "0.02"})
            grid.append({"slot_id": f"o{i}", "classification": "OPPOSED", "y": "0.00"})
        result = evaluate(
            grid,
            InferenceConfig(block_length=12, replicates=200, seed=20261004, min_aligned=24, min_opposed=24),
        )
        self.assertEqual(result["status"], "OK")
        self.assertAlmostEqual(result["observed_d"], 0.02)
        self.assertAlmostEqual(result["bootstrap"]["lower_95"], 0.02)
        self.assertEqual(result["decision"], "PROMISING_EXPLORATORY")

    def test_insufficient_group_counts_hold(self):
        grid = [
            {"classification": "ALIGNED", "y": 0.01} for _ in range(23)
        ] + [
            {"classification": "OPPOSED", "y": 0.00} for _ in range(30)
        ]
        result = evaluate(grid, InferenceConfig(replicates=10, min_aligned=24, min_opposed=24))
        self.assertEqual(result["status"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(result["n_aligned"], 23)
        self.assertIsNone(result["bootstrap"])

    def test_neutral_and_missing_slots_remain_in_grid_but_not_groups(self):
        raw = [
            {"slot_id": "a", "classification": "ALIGNED", "y": 0.02},
            {"slot_id": "n", "classification": "NEUTRAL", "y": 0.50},
            {"slot_id": "m", "classification": None, "y": None},
            {"slot_id": "o", "classification": "OPPOSED", "y": 0.01},
        ]
        grid = normalize_grid(raw)
        self.assertEqual(len(grid), 4)
        d, na, no = difference(grid)
        self.assertAlmostEqual(d, 0.01)
        self.assertEqual((na, no), (1, 1))

    def test_nonfinite_outcome_fails_closed(self):
        with self.assertRaises(InferenceError):
            normalize_grid([{"classification": "ALIGNED", "y": math.nan}])

    def test_invalid_classification_fails_closed(self):
        with self.assertRaises(InferenceError):
            normalize_grid([{"classification": "MAYBE", "y": 0.1}])

    def test_empty_group_fails_closed(self):
        grid = normalize_grid([
            {"classification": "ALIGNED", "y": 0.01},
            {"classification": "ALIGNED", "y": 0.02},
        ])
        with self.assertRaises(InferenceError):
            difference(grid)

    def test_same_seed_is_byte_for_byte_value_deterministic(self):
        grid = []
        for i in range(40):
            grid.append({"classification": "ALIGNED", "y": (i % 7) / 1000})
            grid.append({"classification": "OPPOSED", "y": -((i % 5) / 1000)})
            if i % 3 == 0:
                grid.append({"classification": "NEUTRAL", "y": 0.0})
        cfg = InferenceConfig(block_length=12, replicates=250, seed=20261004, min_aligned=24, min_opposed=24)
        self.assertEqual(evaluate(grid, cfg), evaluate(grid, cfg))

    def test_negative_difference_maps_not_supported(self):
        grid = []
        for _ in range(24):
            grid.append({"classification": "ALIGNED", "y": -0.01})
            grid.append({"classification": "OPPOSED", "y": 0.01})
        result = evaluate(grid, InferenceConfig(replicates=100, min_aligned=24, min_opposed=24))
        self.assertEqual(result["decision"], "NOT_SUPPORTED")


if __name__ == "__main__":
    unittest.main()
