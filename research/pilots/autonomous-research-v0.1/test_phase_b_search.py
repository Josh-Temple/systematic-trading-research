import tempfile
import unittest
from pathlib import Path

import evaluator
import phase_b_baselines
import phase_b_core
from phase_b_search import PhaseBProtocolError, SearchHost, select_best_record


SEED = bytes.fromhex("33" * 32)
KEY = b"phase-b-test-checkpoint-key-32!!"


def world():
    return phase_b_core.generate_world(
        world_id="STABLE-HOST-TEST",
        archetype="STABLE",
        seed=SEED,
    )


class PhaseBSearchTests(unittest.TestCase):
    def test_invalid_and_duplicate_submissions_consume_budget(self):
        with tempfile.TemporaryDirectory() as td:
            host = SearchHost(
                run_id="HOST-1",
                method="AI",
                world=world(),
                ledger_path=Path(td) / "ledger.jsonl",
                checkpoint_key=KEY,
            )
            valid = phase_b_core.enumerate_strategy_space()[20]
            bad = dict(valid)
            bad["candidate_id"] = "BAD"
            bad["feature"] = dict(valid["feature"])
            bad["feature"]["source"] = "next_return"

            f1 = host.submit(round_number=1, candidate=bad)
            f2 = host.submit(round_number=1, candidate=valid)
            duplicate = dict(valid)
            duplicate["candidate_id"] = "DUP"
            f3 = host.submit(round_number=1, candidate=duplicate)

            self.assertEqual(host.submission_count, 3)
            self.assertEqual(f1.validity_status, "INVALID")
            self.assertIsNone(f1.adaptive_mean_return)
            self.assertEqual(f2.validity_status, "VALID")
            self.assertIsNotNone(f2.adaptive_mean_return)
            self.assertEqual(f3.validity_status, "DUPLICATE")
            self.assertTrue(f3.duplicate)
            self.assertIsNone(f3.adaptive_mean_return)

    def test_round_limit_is_enforced(self):
        with tempfile.TemporaryDirectory() as td:
            host = SearchHost(
                run_id="HOST-2",
                method="AI",
                world=world(),
                ledger_path=Path(td) / "ledger.jsonl",
                checkpoint_key=KEY,
            )
            space = phase_b_core.enumerate_strategy_space()
            for c in space[:4]:
                host.submit(round_number=1, candidate=c)
            with self.assertRaises(PhaseBProtocolError):
                host.submit(round_number=1, candidate=space[4])

    def test_final_is_blocked_until_all_rounds_close(self):
        with tempfile.TemporaryDirectory() as td:
            host = SearchHost(
                run_id="HOST-3",
                method="AI",
                world=world(),
                ledger_path=Path(td) / "ledger.jsonl",
                checkpoint_key=KEY,
            )
            host.submit(
                round_number=1,
                candidate=phase_b_core.enumerate_strategy_space()[20],
            )
            host.close_round(1)
            with self.assertRaises(PhaseBProtocolError):
                host.finalize()

    def test_final_is_one_shot_and_checkpoint_verifies(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            host = SearchHost(
                run_id="HOST-4",
                method="AI",
                world=world(),
                ledger_path=path,
                checkpoint_key=KEY,
            )
            space = phase_b_core.enumerate_strategy_space()
            cursor = 0
            for round_number in range(1, 5):
                for _ in range(4):
                    host.submit(round_number=round_number, candidate=space[cursor])
                    cursor += 1
                host.close_round(round_number)

            summary = host.finalize()
            self.assertEqual(summary["submitted_count"], 16)
            self.assertIsNotNone(summary["final_mean_return"])
            state = evaluator.verify_ledger_checkpoint(
                path, summary["ledger_checkpoint"], KEY
            )
            self.assertGreater(state["events"], 16)

            with self.assertRaises(PhaseBProtocolError):
                host.finalize()

    def test_feedback_does_not_expose_final_or_hidden_seed(self):
        with tempfile.TemporaryDirectory() as td:
            host = SearchHost(
                run_id="HOST-5",
                method="AI",
                world=world(),
                ledger_path=Path(td) / "ledger.jsonl",
                checkpoint_key=KEY,
            )
            feedback = host.submit(
                round_number=1,
                candidate=phase_b_core.enumerate_strategy_space()[20],
            ).as_dict()
            forbidden = {"final_mean_return", "seed_hex", "planted_strategy"}
            self.assertTrue(forbidden.isdisjoint(feedback))

    def test_tie_break_uses_smallest_strategy_fingerprint(self):
        records = [
            {
                "validity_status": "VALID",
                "adaptive_mean_return": 0.01,
                "strategy_fingerprint": "bbb",
            },
            {
                "validity_status": "VALID",
                "adaptive_mean_return": 0.01,
                "strategy_fingerprint": "aaa",
            },
            {
                "validity_status": "VALID",
                "adaptive_mean_return": 0.005,
                "strategy_fingerprint": "000",
            },
        ]
        self.assertEqual(
            select_best_record(records)["strategy_fingerprint"],
            "aaa",
        )

    def test_random_baseline_obeys_budget_and_checkpoint(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "random.jsonl"
            summary = phase_b_baselines.run_random_search(
                world=world(),
                run_id="RANDOM-TEST",
                baseline_seed=12345,
                ledger_path=path,
                checkpoint_key=KEY,
            )
            self.assertEqual(summary["submitted_count"], 16)
            self.assertEqual(summary["duplicate_count"], 0)
            evaluator.verify_ledger_checkpoint(
                path, summary["ledger_checkpoint"], KEY
            )

    def test_deterministic_adaptive_baseline_obeys_budget(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "adaptive.jsonl"
            summary = phase_b_baselines.run_deterministic_adaptive(
                world=world(),
                run_id="ADAPTIVE-TEST",
                ledger_path=path,
                checkpoint_key=KEY,
            )
            self.assertEqual(summary["submitted_count"], 16)
            self.assertEqual(summary["duplicate_count"], 0)
            evaluator.verify_ledger_checkpoint(
                path, summary["ledger_checkpoint"], KEY
            )


if __name__ == "__main__":
    unittest.main()
