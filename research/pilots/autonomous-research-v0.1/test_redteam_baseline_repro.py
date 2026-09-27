import json
import unittest

import evaluator


def base_candidate():
    return {
        "candidate_id": "BASELINE-REDTEAM",
        "feature": {"source": "feature_a", "transform": "identity", "lag": 0},
        "operator": "gt",
        "threshold": 0.0,
        "side": "long",
        "position_size": 1.0,
    }


class BaselineRedTeamReproduction(unittest.TestCase):
    def test_unhashable_source_should_be_clean_candidate_rejection(self):
        c = base_candidate()
        c["feature"]["source"] = []
        raw = json.dumps(c, separators=(",", ":"))
        with self.assertRaises(evaluator.CandidateInvalid):
            evaluator.evaluate_json(raw)

    def test_huge_integer_should_be_clean_candidate_rejection(self):
        raw = json.dumps(base_candidate(), separators=(",", ":"))
        huge = "1" + ("0" * 999)
        raw = raw.replace('"threshold":0.0', '"threshold":' + huge)
        with self.assertRaises(evaluator.CandidateInvalid):
            evaluator.evaluate_json(raw)

    def test_deep_json_should_be_clean_candidate_rejection(self):
        raw = json.dumps(base_candidate(), separators=(",", ":"))
        depth = 1500
        raw = raw[:-1] + ',"unknown":' + ("[" * depth) + "0" + ("]" * depth) + "}"
        with self.assertRaises(evaluator.CandidateInvalid):
            evaluator.evaluate_json(raw)

    def test_lone_surrogate_id_should_not_break_receipt_serialization(self):
        c = base_candidate()
        c["candidate_id"] = "\ud800"
        receipt = evaluator.evaluate(c)
        self.assertEqual(receipt["execution_status"], "SUCCESS")
        self.assertEqual(receipt["validity_status"], "INVALID")


if __name__ == "__main__":
    unittest.main()
