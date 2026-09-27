import math
import unittest

import evaluator
import independent_evaluator


def candidate(
    *,
    candidate_id="SECOND",
    source="feature_a",
    transform="identity",
    lag=0,
    operator="gt",
    threshold=0.0,
    side="long",
    position_size=1.0,
):
    return {
        "candidate_id": candidate_id,
        "feature": {"source": source, "transform": transform, "lag": lag},
        "operator": operator,
        "threshold": threshold,
        "side": side,
        "position_size": position_size,
    }


class IndependentEvaluatorReproductionTests(unittest.TestCase):
    def test_declared_grammar_matches_primary_evaluator(self):
        thresholds = (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0)
        transforms = [("identity", 0)] + [("lag_diff", lag) for lag in range(1, 6)]
        count = 0

        for source in ("feature_a", "feature_b"):
            for transform, lag in transforms:
                for operator in ("gt", "lt"):
                    for side in ("long", "short"):
                        for threshold in thresholds:
                            for position_size in (0.1, 1.0):
                                c = candidate(
                                    candidate_id=f"SECOND-{count}",
                                    source=source,
                                    transform=transform,
                                    lag=lag,
                                    operator=operator,
                                    threshold=threshold,
                                    side=side,
                                    position_size=position_size,
                                )
                                primary = evaluator.evaluate(c)
                                second = independent_evaluator.safe_evaluate(
                                    c, evaluator.SYNTHETIC_ROWS
                                )
                                count += 1

                                self.assertEqual(
                                    primary["validity_status"],
                                    second["validity_status"],
                                    msg=c,
                                )
                                if primary["validity_status"] == "VALID":
                                    self.assertEqual(
                                        primary["metrics"]["active_count"],
                                        second["metrics"]["active_count"],
                                        msg=c,
                                    )
                                    self.assertEqual(
                                        primary["metrics"]["scored_observations"],
                                        second["metrics"]["scored_observations"],
                                        msg=c,
                                    )
                                    self.assertTrue(
                                        math.isclose(
                                            primary["metrics"]["mean_return"],
                                            second["metrics"]["mean_return"],
                                            rel_tol=0.0,
                                            abs_tol=1e-15,
                                        ),
                                        msg=(c, primary, second),
                                    )
                                else:
                                    self.assertEqual(second["metrics"], {})

        self.assertEqual(count, 672)

    def test_selected_invalid_candidates_match(self):
        invalids = []

        c = candidate(candidate_id="INV-1")
        c["feature"]["source"] = "future_return"
        invalids.append(c)

        c = candidate(candidate_id="INV-2")
        c["position_size"] = 1.5
        invalids.append(c)

        c = candidate(candidate_id="INV-3")
        c["threshold"] = math.inf
        invalids.append(c)

        c = candidate(candidate_id="INV-4")
        c["feature"] = {"source": "feature_a", "transform": "lag_diff", "lag": 0}
        invalids.append(c)

        c = candidate(candidate_id="INV-5")
        c["unknown"] = "field"
        invalids.append(c)

        for c in invalids:
            primary = evaluator.evaluate(c)
            second = independent_evaluator.safe_evaluate(c, evaluator.SYNTHETIC_ROWS)
            self.assertEqual(primary["validity_status"], "INVALID")
            self.assertEqual(second["validity_status"], "INVALID")

    def test_second_implementation_is_not_primary_import_alias(self):
        self.assertIsNot(
            independent_evaluator.evaluate_candidate,
            evaluator.evaluate,
        )


if __name__ == "__main__":
    unittest.main()
