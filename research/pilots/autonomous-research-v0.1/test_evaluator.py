import json
import math
import tempfile
import unittest
from pathlib import Path

import evaluator


def valid_candidate(candidate_id="CAND-0001"):
    return {
        "candidate_id": candidate_id,
        "feature": {"source": "feature_a", "transform": "identity", "lag": 0},
        "operator": "gt",
        "threshold": 0.0,
        "side": "long",
        "position_size": 1.0,
    }


class PhaseAEvaluatorTests(unittest.TestCase):
    def test_valid_candidate_scores(self):
        r = evaluator.evaluate(valid_candidate())
        self.assertEqual(r["execution_status"], "SUCCESS")
        self.assertEqual(r["validity_status"], "VALID")
        self.assertEqual(r["scientific_status"], "NOT_APPLICABLE")
        self.assertGreater(r["metrics"]["active_count"], 0)

    def test_repeated_evaluation_is_deterministic_for_evidence_fields(self):
        r1 = evaluator.evaluate(valid_candidate())
        r2 = evaluator.evaluate(valid_candidate())
        self.assertEqual(r1["metrics"], r2["metrics"])
        self.assertEqual(r1["candidate_hash"], r2["candidate_hash"])
        self.assertEqual(r1["dataset_hash"], r2["dataset_hash"])
        self.assertEqual(r1["evaluator_identity"], r2["evaluator_identity"])
        self.assertEqual(r1["result_hash"], r2["result_hash"])

    def test_nan_and_infinity_thresholds_rejected(self):
        for value in (math.nan, math.inf, -math.inf):
            c = valid_candidate()
            c["threshold"] = value
            r = evaluator.evaluate(c)
            self.assertEqual(r["validity_status"], "INVALID")

    def test_extreme_position_rejected(self):
        c = valid_candidate()
        c["position_size"] = 1000.0
        self.assertEqual(evaluator.evaluate(c)["validity_status"], "INVALID")

    def test_missing_required_field_rejected(self):
        c = valid_candidate()
        del c["side"]
        self.assertEqual(evaluator.evaluate(c)["validity_status"], "INVALID")

    def test_future_source_rejected(self):
        c = valid_candidate()
        c["feature"]["source"] = "future_return"
        self.assertEqual(evaluator.evaluate(c)["validity_status"], "INVALID")

    def test_resampling_and_file_network_fields_rejected(self):
        for field, value in (
            ("resample", "1h"),
            ("path", "/tmp/secret"),
            ("url", "https://example.invalid"),
            ("code", "open('/hidden')"),
        ):
            c = valid_candidate()
            c[field] = value
            self.assertEqual(evaluator.evaluate(c)["validity_status"], "INVALID")

    def test_fabricated_metric_field_rejected(self):
        c1 = valid_candidate("CAND-A")
        c2 = valid_candidate("CAND-B")
        c1["reported_metric"] = 999999
        c2["reported_metric"] = -999999
        self.assertEqual(evaluator.evaluate(c1)["validity_status"], "INVALID")
        self.assertEqual(evaluator.evaluate(c2)["validity_status"], "INVALID")

    def test_malformed_parser_shape_rejected(self):
        c = valid_candidate()
        c["threshold"] = {"value": 0.0}
        self.assertEqual(evaluator.evaluate(c)["validity_status"], "INVALID")

    def test_all_constant_signal_rejected(self):
        c = valid_candidate()
        c["threshold"] = -999.0
        self.assertEqual(evaluator.evaluate(c)["validity_status"], "INVALID")

    def test_signal_validator_rejects_length_mismatch(self):
        with self.assertRaises(evaluator.CandidateInvalid):
            evaluator.validate_signal([0.0, 1.0], expected_len=3)

    def test_signal_validator_rejects_nonfinite_and_unbounded(self):
        with self.assertRaises(evaluator.CandidateInvalid):
            evaluator.validate_signal([0.0, math.nan, 1.0], expected_len=3)
        with self.assertRaises(evaluator.CandidateInvalid):
            evaluator.validate_signal([0.0, 2.0, 1.0], expected_len=3)

    def test_invalid_timestamp_is_evaluator_failure_not_scientific_negative(self):
        rows = [dict(r) for r in evaluator.SYNTHETIC_ROWS]
        rows[3]["timestamp"] = rows[2]["timestamp"]
        r = evaluator.evaluate(valid_candidate(), rows)
        self.assertEqual(r["execution_status"], "FAILED")
        self.assertEqual(r["validity_status"], "UNVERIFIED")
        self.assertEqual(r["scientific_status"], "NOT_APPLICABLE")
        self.assertEqual(r["metrics"], {})

    def test_dataset_identity_changes_when_data_change(self):
        rows = [dict(r) for r in evaluator.SYNTHETIC_ROWS]
        h1 = evaluator.dataset_hash(rows)
        rows[0]["feature_a"] += 0.001
        h2 = evaluator.dataset_hash(rows)
        self.assertNotEqual(h1, h2)

    def test_evaluator_identity_hash_function_changes_with_source_bytes(self):
        self.assertNotEqual(evaluator.hash_bytes(b"evaluator-v1"), evaluator.hash_bytes(b"evaluator-v2"))

    def test_duplicate_strategy_ignores_candidate_id_and_note(self):
        a = valid_candidate("A")
        b = valid_candidate("B")
        b["researcher_note"] = "same strategy, different metadata"
        self.assertEqual(evaluator.strategy_fingerprint(a), evaluator.strategy_fingerprint(b))
        fp = evaluator.strategy_fingerprint(a)
        r = evaluator.evaluate(b, known_strategy_fingerprints={fp})
        self.assertEqual(r["validity_status"], "DUPLICATE")
        self.assertEqual(r["metrics"], {})

    def test_candidate_hash_canonicalizes_key_order(self):
        a = valid_candidate()
        b = {
            "position_size": 1.0,
            "side": "long",
            "threshold": 0.0,
            "operator": "gt",
            "feature": {"lag": 0, "transform": "identity", "source": "feature_a"},
            "candidate_id": "CAND-0001",
        }
        self.assertEqual(evaluator.evaluate(a)["candidate_hash"], evaluator.evaluate(b)["candidate_hash"])

    def test_ledger_appends_without_overwriting(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            r1 = evaluator.evaluate(valid_candidate("A"))
            r2 = evaluator.evaluate(valid_candidate("B"))
            evaluator.append_ledger(path, {"event": "evaluation", "receipt": r1})
            evaluator.append_ledger(path, {"event": "evaluation", "receipt": r2})
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["receipt"]["candidate_id"], "A")
            self.assertEqual(json.loads(lines[1])["receipt"]["candidate_id"], "B")


if __name__ == "__main__":
    unittest.main()
