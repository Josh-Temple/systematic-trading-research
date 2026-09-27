import copy
import json
import math
import random
import tempfile
import unittest
from pathlib import Path

import evaluator


SEED = 20260927


def candidate(
    *,
    candidate_id="FUZZ",
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


class PhaseAFuzzPropertyTests(unittest.TestCase):
    def test_exhaustive_declared_grammar_receipt_invariants(self):
        thresholds = (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0)
        position_sizes = (0.1, 1.0)
        transforms = [("identity", 0)] + [("lag_diff", lag) for lag in range(1, 6)]
        count = 0

        for source in ("feature_a", "feature_b"):
            for transform, lag in transforms:
                for operator in ("gt", "lt"):
                    for side in ("long", "short"):
                        for threshold in thresholds:
                            for position_size in position_sizes:
                                c = candidate(
                                    candidate_id=f"GRID-{count}",
                                    source=source,
                                    transform=transform,
                                    lag=lag,
                                    operator=operator,
                                    threshold=threshold,
                                    side=side,
                                    position_size=position_size,
                                )
                                r = evaluator.evaluate(c)
                                count += 1

                                self.assertEqual(r["execution_status"], "SUCCESS")
                                self.assertEqual(r["scientific_status"], "NOT_APPLICABLE")
                                self.assertIn(r["validity_status"], {"VALID", "INVALID"})
                                self.assertEqual(r["dataset_id"], evaluator.DATASET_ID)
                                self.assertTrue(r["candidate_hash"])
                                self.assertTrue(r["strategy_fingerprint"])
                                self.assertTrue(r["evaluator_identity"])
                                self.assertTrue(r["dataset_hash"])
                                self.assertTrue(r["result_hash"])

                                if r["validity_status"] == "VALID":
                                    self.assertTrue(math.isfinite(r["metrics"]["mean_return"]))
                                    self.assertGreaterEqual(r["metrics"]["active_count"], 1)
                                    self.assertLessEqual(
                                        r["metrics"]["active_count"],
                                        r["metrics"]["scored_observations"],
                                    )
                                else:
                                    self.assertEqual(r["metrics"], {})

        self.assertEqual(count, 672)

    def test_seeded_valid_json_roundtrip_preserves_evidence(self):
        rng = random.Random(SEED)
        for i in range(300):
            transform = rng.choice(("identity", "lag_diff"))
            lag = 0 if transform == "identity" else rng.randint(1, 5)
            c = candidate(
                candidate_id=f"ROUNDTRIP-{i}",
                source=rng.choice(("feature_a", "feature_b")),
                transform=transform,
                lag=lag,
                operator=rng.choice(("gt", "lt")),
                threshold=rng.uniform(-2.0, 2.0),
                side=rng.choice(("long", "short")),
                position_size=rng.uniform(1e-6, 1.0),
            )
            if rng.random() < 0.25:
                c["researcher_note"] = f"seeded-{i}"

            text = json.dumps(c, ensure_ascii=False, allow_nan=False)
            parsed = evaluator.load_candidate_json(text)
            via_json = evaluator.evaluate_json(text)
            direct = evaluator.evaluate(parsed)

            self.assertEqual(via_json["candidate_hash"], direct["candidate_hash"])
            self.assertEqual(via_json["strategy_fingerprint"], direct["strategy_fingerprint"])
            self.assertEqual(via_json["metrics"], direct["metrics"])
            self.assertEqual(via_json["validity_status"], direct["validity_status"])
            self.assertEqual(via_json["result_hash"], direct["result_hash"])

    def test_seeded_invalid_mutations_never_receive_valid_score(self):
        rng = random.Random(SEED)
        mutation_kinds = (
            "unknown_top",
            "unknown_feature",
            "missing_required",
            "bad_source",
            "bad_transform",
            "bad_lag",
            "bad_operator",
            "bad_side",
            "bad_threshold",
            "bad_position",
            "bad_candidate_id",
            "bad_note",
        )

        for i in range(1000):
            c = candidate(candidate_id=f"MUT-{i}")
            kind = rng.choice(mutation_kinds)

            if kind == "unknown_top":
                c[rng.choice(("code", "url", "path", "future_return", "metric"))] = "forbidden"
            elif kind == "unknown_feature":
                c["feature"]["future"] = 1
            elif kind == "missing_required":
                del c[rng.choice(("candidate_id", "feature", "operator", "threshold", "side", "position_size"))]
            elif kind == "bad_source":
                c["feature"]["source"] = rng.choice(("next_return", "target", "future_return", "close"))
            elif kind == "bad_transform":
                c["feature"]["transform"] = rng.choice(("shift_future", "eval", "rolling_future", "python"))
            elif kind == "bad_lag":
                c["feature"]["transform"] = "lag_diff"
                c["feature"]["lag"] = rng.choice((-100, -1, 0, 6, 999, 1.5, True, "1", None))
            elif kind == "bad_operator":
                c["operator"] = rng.choice((">=", "eval", "between", "", None))
            elif kind == "bad_side":
                c["side"] = rng.choice(("both", "flat", "BUY", "", None))
            elif kind == "bad_threshold":
                c["threshold"] = rng.choice((math.nan, math.inf, -math.inf, True, "0", None, [], {}))
            elif kind == "bad_position":
                c["position_size"] = rng.choice((0.0, -1.0, 1.000001, 1000.0, math.nan, math.inf, True, "1"))
            elif kind == "bad_candidate_id":
                c["candidate_id"] = rng.choice(("", None, 123, "X" * 81))
            elif kind == "bad_note":
                c["researcher_note"] = "X" * 1001

            r = evaluator.evaluate(c)
            self.assertEqual(r["execution_status"], "SUCCESS", msg=(kind, c, r))
            self.assertEqual(r["validity_status"], "INVALID", msg=(kind, c, r))
            self.assertEqual(r["scientific_status"], "NOT_APPLICABLE")
            self.assertEqual(r["metrics"], {})

    def test_result_hash_is_stable_for_identical_evidence(self):
        rng = random.Random(SEED)
        for i in range(100):
            c = candidate(
                candidate_id=f"HASH-{i}",
                threshold=rng.uniform(-1.5, 1.5),
                position_size=rng.uniform(0.01, 1.0),
                source=rng.choice(("feature_a", "feature_b")),
                operator=rng.choice(("gt", "lt")),
                side=rng.choice(("long", "short")),
            )
            a = evaluator.evaluate(c)
            b = evaluator.evaluate(copy.deepcopy(c))
            self.assertNotEqual(a["created_at"], "")
            self.assertEqual(a["result_hash"], b["result_hash"])

    def test_ledger_strict_parser_rejects_duplicate_keys_and_nan(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            record = evaluator.append_ledger(path, {"kind": "evaluation", "n": 1})
            line = path.read_text(encoding="utf-8").strip()

            path.write_text(line[:-1] + ',"event_hash":"duplicate"}\n', encoding="utf-8")
            with self.assertRaises(evaluator.EvaluatorFailure):
                evaluator.verify_ledger(path)

            path.unlink()
            evaluator.append_ledger(path, {"kind": "evaluation", "n": 1})
            line = path.read_text(encoding="utf-8").strip()
            tampered = line.replace('"n":1', '"n":NaN')
            path.write_text(tampered + "\n", encoding="utf-8")
            with self.assertRaises(evaluator.EvaluatorFailure):
                evaluator.verify_ledger(path)

            self.assertTrue(record["event_hash"])

    def test_ledger_suffix_truncation_remains_a_documented_limitation(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            evaluator.append_ledger(path, {"kind": "evaluation", "n": 1})
            evaluator.append_ledger(path, {"kind": "evaluation", "n": 2})
            lines = path.read_text(encoding="utf-8").splitlines()
            path.write_text(lines[0] + "\n", encoding="utf-8")

            # A self-contained hash chain cannot prove that its tail was deleted
            # without an external checkpoint/anchor.
            state = evaluator.verify_ledger(path)
            self.assertEqual(state["events"], 1)


if __name__ == "__main__":
    unittest.main()
