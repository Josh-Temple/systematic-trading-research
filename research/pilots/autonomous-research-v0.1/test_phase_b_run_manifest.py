import copy
import unittest
from pathlib import Path

import phase_b_run_manifest


ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = Path(__file__).with_name("RUN_MANIFEST_PHASE_B_AI_v0.1.json")


class PhaseBRunManifestTests(unittest.TestCase):
    def test_frozen_manifest_matches_committed_instruction_and_protocol(self):
        manifest = phase_b_run_manifest.load_manifest(MANIFEST_PATH)
        phase_b_run_manifest.validate_manifest(manifest, root=ROOT)
        self.assertEqual(manifest["model_provider"], "OpenAI")
        self.assertEqual(manifest["model_identity"], "GPT-5.6 Sol")
        self.assertFalse(manifest["market_data_allowed"])

    def test_instruction_hash_change_is_rejected(self):
        manifest = phase_b_run_manifest.load_manifest(MANIFEST_PATH)
        changed = copy.deepcopy(manifest)
        changed["researcher_instruction_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            phase_b_run_manifest.validate_manifest(changed, root=ROOT)

    def test_budget_change_is_rejected(self):
        manifest = phase_b_run_manifest.load_manifest(MANIFEST_PATH)
        changed = copy.deepcopy(manifest)
        changed["search_budget"]["submissions_per_world_method"] = 17
        with self.assertRaises(ValueError):
            phase_b_run_manifest.validate_manifest(changed, root=ROOT)

    def test_feedback_schema_change_is_rejected(self):
        manifest = phase_b_run_manifest.load_manifest(MANIFEST_PATH)
        changed = copy.deepcopy(manifest)
        changed["feedback_schema"] = list(changed["feedback_schema"]) + ["extra"]
        with self.assertRaises(ValueError):
            phase_b_run_manifest.validate_manifest(changed, root=ROOT)

    def test_world_ids_are_six_unique_ids(self):
        manifest = phase_b_run_manifest.load_manifest(MANIFEST_PATH)
        changed = copy.deepcopy(manifest)
        changed["world_ids"][-1] = changed["world_ids"][0]
        with self.assertRaises(ValueError):
            phase_b_run_manifest.validate_manifest(changed, root=ROOT)


if __name__ == "__main__":
    unittest.main()
