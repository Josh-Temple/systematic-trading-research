import copy
import inspect
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import phase_b_core
import phase_b_official_ai_relay as relay
import phase_b_official_baselines as official
import phase_b_run_manifest


class PhaseBOfficialAIRelayTests(unittest.TestCase):
    def _test_inputs(self):
        manifest = phase_b_run_manifest.load_manifest(relay.MANIFEST_PATH)
        binding = relay.load_json(relay.BINDING_PATH)
        host_state = official.make_host_state("TEST-AI-RELAY")
        commitments = official.public_commitments(host_state)
        binding = copy.deepcopy(binding)
        binding["host_state_hash"] = commitments["host_state_hash"]
        return manifest, binding, host_state, commitments

    def test_frozen_binding_matches_manifest_and_forbids_result_visibility(self):
        manifest = phase_b_run_manifest.load_manifest(relay.MANIFEST_PATH)
        binding = relay.load_json(relay.BINDING_PATH)
        relay.validate_binding(binding, manifest)
        self.assertFalse(binding["market_data_allowed"])
        self.assertFalse(binding["baseline_result_visibility_to_researcher"])
        self.assertFalse(binding["host_state_visibility_to_researcher"])
        self.assertEqual(binding["world_ids"], manifest["world_ids"])

    def test_host_inputs_are_bound_by_exact_commitments(self):
        manifest, binding, host_state, commitments = self._test_inputs()
        relay.validate_host_inputs(
            host_state=host_state,
            commitments=commitments,
            binding=binding,
            manifest=manifest,
        )

        changed = copy.deepcopy(host_state)
        changed["worlds"][0]["seed_hex"] = "11" * 32
        with self.assertRaises(relay.OfficialAIRelayError):
            relay.validate_host_inputs(
                host_state=changed,
                commitments=commitments,
                binding=binding,
                manifest=manifest,
            )

    def test_relay_has_no_baseline_result_input(self):
        params = set(inspect.signature(relay.run_official_ai_session).parameters)
        self.assertEqual(
            params,
            {"host_state", "commitments", "output_root", "researcher"},
        )
        self.assertNotIn("baseline_results", params)
        self.assertNotIn("baseline_result_artifact", params)

    def test_strict_response_parser_rejects_duplicate_keys_and_nan(self):
        with self.assertRaises(relay.OfficialAIRelayError):
            relay.parse_researcher_response(
                '{"stop":false,"stop":true,"proposals":[]}'
            )
        with self.assertRaises(relay.OfficialAIRelayError):
            relay.parse_researcher_response(
                '{"stop":false,"proposals":[{"x":NaN}]}'
            )

    def test_output_root_is_fail_closed_against_restart(self):
        manifest = phase_b_run_manifest.load_manifest(relay.MANIFEST_PATH)
        binding = relay.load_json(relay.BINDING_PATH)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "official-ai"
            root.mkdir()
            with self.assertRaises(relay.OfficialAIRelayError):
                relay.prepare_output_root(
                    output_root=root,
                    manifest=manifest,
                    binding=binding,
                )

    def test_full_synthetic_relay_keeps_metrics_private(self):
        _, binding, host_state, commitments = self._test_inputs()
        space = phase_b_core.enumerate_strategy_space()

        def researcher(packet):
            start = (int(packet["round"]) - 1) * 4
            proposals = []
            for offset, candidate in enumerate(space[start : start + 4]):
                clean = json.loads(json.dumps(candidate))
                clean["candidate_id"] = (
                    f"AI-{packet['world_id']}-{start + offset:03d}"
                )
                proposals.append(clean)
            return {"stop": False, "proposals": proposals}

        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "official-ai"
            with mock.patch.object(relay, "load_json", return_value=binding):
                status = relay.run_official_ai_session(
                    host_state=host_state,
                    commitments=commitments,
                    output_root=root,
                    researcher=researcher,
                )
            public_text = (
                root / "public" / "session_status.json"
            ).read_text(encoding="utf-8")
            private_text = (
                root / "private" / "official_ai_summaries.json"
            ).read_text(encoding="utf-8")

            self.assertEqual(status["state"], "COMPLETE_PENDING_COMPARISON")
            self.assertEqual(status["completed_worlds"], binding["world_ids"])
            self.assertFalse(status["metric_values_exposed"])
            self.assertFalse(status["baseline_results_read"])
            self.assertFalse(status["market_data_used"])
            self.assertNotIn("final_mean_return", public_text)
            self.assertNotIn("best_adaptive_mean_return", public_text)
            self.assertIn("final_mean_return", private_text)
            self.assertTrue(
                (
                    root
                    / "researcher_exchange"
                    / "PHASE_B_AI_RESEARCHER_INSTRUCTION_v0.1.md"
                ).is_file()
            )

    def test_wrong_frozen_host_hash_fails_before_output_creation(self):
        _, _, host_state, commitments = self._test_inputs()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "official-ai"
            with self.assertRaises(relay.OfficialAIRelayError):
                relay.run_official_ai_session(
                    host_state=host_state,
                    commitments=commitments,
                    output_root=root,
                    researcher=lambda packet: {"stop": True, "proposals": []},
                )
            self.assertFalse(root.exists())


if __name__ == "__main__":
    unittest.main()
