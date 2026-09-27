import tempfile
import unittest
from pathlib import Path

import phase_b_ai
import phase_b_core


SEED = bytes.fromhex("44" * 32)
KEY = b"phase-b-ai-test-checkpoint-key!!"


class PhaseBAITests(unittest.TestCase):
    def test_round_packet_excludes_hidden_and_final_data(self):
        packet = phase_b_ai.make_round_packet(
            world_id="STABLE-01",
            round_number=1,
            remaining_budget=16,
            prior_feedback=[],
        )
        encoded = repr(packet).lower()
        self.assertNotIn("seed_hex", encoded)
        self.assertNotIn("adaptive_rows", encoded)
        self.assertNotIn("final_rows", encoded)
        self.assertNotIn("planted", encoded)
        self.assertNotIn("dataset_hash", encoded)

    def test_ai_search_obeys_four_round_sixteen_budget(self):
        world = phase_b_core.generate_world(
            world_id="STABLE-AI-TEST",
            archetype="STABLE",
            seed=SEED,
        )
        space = phase_b_core.enumerate_strategy_space()
        cursor = {"i": 0}

        def researcher(packet):
            start = cursor["i"]
            chosen = []
            for candidate in space[start : start + 4]:
                c = dict(candidate)
                c["candidate_id"] = f"AI-{start + len(chosen):03d}"
                chosen.append(c)
            cursor["i"] += 4
            return {"stop": False, "proposals": chosen}

        with tempfile.TemporaryDirectory() as td:
            result = phase_b_ai.run_ai_search(
                world=world,
                run_id="AI-TEST",
                ledger_path=Path(td) / "ledger.jsonl",
                checkpoint_key=KEY,
                researcher=researcher,
            )

        summary = result["summary"]
        self.assertEqual(summary["submitted_count"], 16)
        self.assertEqual(len(result["researcher_visible_round_packets"]), 4)
        self.assertEqual(len(result["researcher_feedback_history"]), 16)

    def test_malformed_researcher_response_does_not_gain_extra_budget(self):
        world = phase_b_core.generate_world(
            world_id="STABLE-AI-MALFORMED",
            archetype="STABLE",
            seed=SEED,
        )
        good = phase_b_core.enumerate_strategy_space()[20]
        calls = {"n": 0}

        def researcher(packet):
            calls["n"] += 1
            if calls["n"] == 1:
                return {"stop": False, "proposals": [good]}
            return {"unexpected": True}

        with tempfile.TemporaryDirectory() as td:
            result = phase_b_ai.run_ai_search(
                world=world,
                run_id="AI-MALFORMED",
                ledger_path=Path(td) / "ledger.jsonl",
                checkpoint_key=KEY,
                researcher=researcher,
            )

        self.assertEqual(result["summary"]["submitted_count"], 1)
        self.assertEqual(calls["n"], 2)

    def test_explicit_stop_closes_remaining_rounds_without_reallocation(self):
        world = phase_b_core.generate_world(
            world_id="STABLE-AI-STOP",
            archetype="STABLE",
            seed=SEED,
        )
        candidate = phase_b_core.enumerate_strategy_space()[20]
        calls = {"n": 0}

        def researcher(packet):
            calls["n"] += 1
            return {"stop": True, "proposals": [candidate]}

        with tempfile.TemporaryDirectory() as td:
            result = phase_b_ai.run_ai_search(
                world=world,
                run_id="AI-STOP",
                ledger_path=Path(td) / "ledger.jsonl",
                checkpoint_key=KEY,
                researcher=researcher,
            )

        self.assertEqual(result["summary"]["submitted_count"], 1)
        self.assertEqual(calls["n"], 1)


if __name__ == "__main__":
    unittest.main()
