import copy
import json
import tempfile
import unittest
from pathlib import Path

import evaluator
import phase_b_official_baselines as official


FIXED_HOST_STATE = {
    "state_version": "0.1",
    "run_label": "TEST-OFFICIAL",
    "protocol_id": "ARP-B-v0.1",
    "amendment_id": "ARP-B-v0.1.1-A1",
    "checkpoint_key_hex": ("44" * 32),
    "worlds": [
        {
            "world_id": "STABLE-TEST-OFFICIAL",
            "archetype": "STABLE",
            "seed_hex": ("55" * 32),
            "seed_commitment": (
                "850c9d0e1ac4a35493601a23917cd44f056f9f63a7d3c18550a69a907c2c606e"
            ),
        }
    ],
}


class OfficialBaselineRunnerTests(unittest.TestCase):
    def test_frozen_protocol_and_amendment_validate(self):
        official.validate_frozen_protocol()

    def test_public_commitments_exclude_raw_secrets(self):
        host_state = official.make_host_state("TEST-COMMIT")
        public = official.public_commitments(host_state)
        encoded = json.dumps(public, sort_keys=True)
        self.assertNotIn("seed_hex", encoded)
        self.assertNotIn("checkpoint_key", encoded)
        self.assertEqual(len(public["worlds"]), 6)
        self.assertEqual(public["protocol_id"], "ARP-B-v0.1")
        self.assertEqual(public["amendment_id"], "ARP-B-v0.1.1-A1")

    def test_host_state_hash_binds_secret_state(self):
        a = copy.deepcopy(FIXED_HOST_STATE)
        b = copy.deepcopy(FIXED_HOST_STATE)
        b["worlds"][0]["seed_hex"] = "66" * 32
        # Make the tampered state internally self-consistent before comparing hashes.
        import phase_b_core
        b["worlds"][0]["seed_commitment"] = phase_b_core.seed_commitment(
            bytes.fromhex(b["worlds"][0]["seed_hex"])
        )
        self.assertNotEqual(
            official.public_commitments(a)["host_state_hash"],
            official.public_commitments(b)["host_state_hash"],
        )

    def test_reduced_batch_separates_host_state_and_results(self):
        import phase_b_core
        host_state = copy.deepcopy(FIXED_HOST_STATE)
        host_state["worlds"][0]["seed_commitment"] = phase_b_core.seed_commitment(
            bytes.fromhex(host_state["worlds"][0]["seed_hex"])
        )

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = official.run_batch(
                output_root=root,
                host_state=host_state,
                random_repetitions=2,
                print_progress=False,
            )

            host_file = root / "host_state" / "host_state.json"
            public_file = root / "public" / "commitments.json"
            summaries_file = root / "results" / "baseline_summaries.jsonl"
            results_manifest = root / "results" / "results_manifest.json"

            self.assertTrue(host_file.exists())
            self.assertTrue(public_file.exists())
            self.assertTrue(summaries_file.exists())
            self.assertTrue(results_manifest.exists())

            host_text = host_file.read_text(encoding="utf-8")
            public_text = public_file.read_text(encoding="utf-8")
            result_manifest_text = results_manifest.read_text(encoding="utf-8")

            self.assertIn("seed_hex", host_text)
            self.assertIn("checkpoint_key_hex", host_text)
            self.assertNotIn("seed_hex", public_text)
            self.assertNotIn("checkpoint_key_hex", public_text)
            self.assertNotIn("seed_hex", result_manifest_text)
            self.assertNotIn("checkpoint_key_hex", result_manifest_text)

            summaries = [
                json.loads(line)
                for line in summaries_file.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(summaries), 3)
            self.assertEqual(manifest["total_method_world_runs"], 3)
            self.assertFalse(manifest["ai_researcher_run"])
            self.assertFalse(manifest["market_data_used"])
            self.assertFalse(manifest["metric_results_in_workflow_log"])

            key = bytes.fromhex(host_state["checkpoint_key_hex"])
            for summary in summaries:
                ledger = root / summary["ledger_path"]
                evaluator.verify_ledger_checkpoint(
                    ledger, summary["ledger_checkpoint"], key
                )

    def test_random_baseline_seed_derivation_is_reproducible_and_distinct(self):
        seed = bytes.fromhex("77" * 32)
        a0 = official.derive_random_baseline_seed(seed, 0)
        a0_repeat = official.derive_random_baseline_seed(seed, 0)
        a1 = official.derive_random_baseline_seed(seed, 1)
        self.assertEqual(a0, a0_repeat)
        self.assertNotEqual(a0, a1)


if __name__ == "__main__":
    unittest.main()
