import copy
import json
import unittest
from pathlib import Path

import evaluator


CORPUS_PATH = Path(__file__).with_name("MODEL_REDTEAM_ATTACKS_v01.json")


def base_candidate():
    return {
        "candidate_id": "REDTEAM",
        "feature": {"source": "feature_a", "transform": "identity", "lag": 0},
        "operator": "gt",
        "threshold": 0.0,
        "side": "long",
        "position_size": 1.0,
    }


def set_path(obj, path, value):
    parts = path.split(".")
    target = obj
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = value


def compact(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def raw_for_case(case):
    kind = case["kind"]

    if kind == "raw":
        return case["raw"]

    c = base_candidate()

    if kind == "field_value":
        set_path(c, case["path"], case["value"])
        return compact(c)

    if kind == "candidate_id_nonstring":
        c["candidate_id"] = case["value"]
        return compact(c)

    if kind == "huge_integer":
        raw = compact(c)
        literal = "1" + ("0" * (int(case["digits"]) - 1))
        needle = f'"{case["field"]}":1.0' if case["field"] == "position_size" else f'"{case["field"]}":0.0'
        if needle not in raw:
            raise AssertionError(f"replacement anchor not found for {case['id']}")
        return raw.replace(needle, f'"{case["field"]}":{literal}')

    if kind == "exponent_overflow":
        raw = compact(c)
        needle = f'"{case["field"]}":0.0'
        return raw.replace(needle, f'"{case["field"]}":{case["literal"]}')

    if kind == "lone_surrogate_id":
        c["candidate_id"] = "\ud800"
        return compact(c)

    if kind == "oversized_note":
        c["researcher_note"] = "X" * int(case["chars"])
        return compact(c)

    if kind == "deep_unknown_array":
        raw = compact(c)
        depth = int(case["depth"])
        return raw[:-1] + ',"unknown":' + ("[" * depth) + "0" + ("]" * depth) + "}"

    raise AssertionError(f"unknown attack kind: {kind}")


def direct_candidate_for_case(case):
    kind = case["kind"]
    c = base_candidate()

    if kind == "field_value":
        set_path(c, case["path"], copy.deepcopy(case["value"]))
        return c
    if kind == "candidate_id_nonstring":
        c["candidate_id"] = copy.deepcopy(case["value"])
        return c
    if kind == "huge_integer":
        c[case["field"]] = int("1" + ("0" * (int(case["digits"]) - 1)))
        return c
    if kind == "exponent_overflow":
        c[case["field"]] = float("inf")
        return c
    if kind == "lone_surrogate_id":
        c["candidate_id"] = "\ud800"
        return c
    if kind == "oversized_note":
        c["researcher_note"] = "X" * int(case["chars"])
        return c
    if kind == "deep_unknown_array":
        c["unknown"] = [[0]]
        return c
    return None


class ModelRedTeamCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))

    def test_corpus_provenance_boundary_is_explicit(self):
        self.assertEqual(self.corpus["generator"]["model"], "GPT-5.6 Sol")
        self.assertEqual(self.corpus["independence"], "NOT_INDEPENDENT")
        self.assertFalse(self.corpus["market_data_used"])
        self.assertEqual(len(self.corpus["cases"]), 15)

    def test_every_source_informed_attack_is_rejected_at_json_boundary(self):
        for case in self.corpus["cases"]:
            with self.subTest(case=case["id"]):
                raw = raw_for_case(case)
                with self.assertRaises(evaluator.CandidateInvalid):
                    evaluator.evaluate_json(raw)

    def test_structured_attack_inputs_are_invalid_not_evaluator_failures(self):
        for case in self.corpus["cases"]:
            c = direct_candidate_for_case(case)
            if c is None:
                continue
            with self.subTest(case=case["id"]):
                receipt = evaluator.evaluate(c)
                self.assertEqual(receipt["execution_status"], "SUCCESS")
                self.assertEqual(receipt["validity_status"], "INVALID")
                self.assertEqual(receipt["scientific_status"], "NOT_APPLICABLE")
                self.assertEqual(receipt["metrics"], {})
                self.assertTrue(receipt["result_hash"])

    def test_candidate_json_size_limit_is_enforced_before_parse(self):
        c = base_candidate()
        c["researcher_note"] = "X" * evaluator.MAX_CANDIDATE_JSON_BYTES
        raw = compact(c)
        self.assertGreater(len(raw.encode("utf-8")), evaluator.MAX_CANDIDATE_JSON_BYTES)
        with self.assertRaises(evaluator.CandidateInvalid):
            evaluator.load_candidate_json(raw)


if __name__ == "__main__":
    unittest.main()
