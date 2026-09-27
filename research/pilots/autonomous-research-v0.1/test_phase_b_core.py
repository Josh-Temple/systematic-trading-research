import json
import unittest

import evaluator
import phase_b_core


SEED_A = bytes.fromhex("11" * 32)
SEED_B = bytes.fromhex("22" * 32)


class PhaseBCoreTests(unittest.TestCase):
    def test_protocol_is_frozen_and_market_data_forbidden(self):
        protocol = phase_b_core.load_protocol()
        self.assertEqual(protocol["status"], "FROZEN_BEFORE_PHASE_B_RESULTS")
        self.assertFalse(protocol["market_data_allowed"])
        self.assertEqual(protocol["candidate_space"]["strategy_count"], 240)

    def test_candidate_space_has_240_unique_fingerprints(self):
        candidates = phase_b_core.enumerate_strategy_space()
        self.assertEqual(len(candidates), 240)
        fps = [evaluator.strategy_fingerprint(c) for c in candidates]
        self.assertEqual(len(set(fps)), 240)
        for c in candidates:
            self.assertEqual(c["position_size"], 1.0)
            self.assertIn(c["threshold"], {-1.0, -0.5, 0.0, 0.5, 1.0})

    def test_world_generation_is_reproducible_for_same_seed(self):
        a = phase_b_core.generate_world(
            world_id="STABLE-TEST-A",
            archetype="STABLE",
            seed=SEED_A,
        )
        b = phase_b_core.generate_world(
            world_id="STABLE-TEST-A",
            archetype="STABLE",
            seed=SEED_A,
        )
        self.assertEqual(a.seed_commitment, b.seed_commitment)
        self.assertEqual(
            phase_b_core.dataset_hash(a.adaptive_rows),
            phase_b_core.dataset_hash(b.adaptive_rows),
        )
        self.assertEqual(
            phase_b_core.dataset_hash(a.final_rows),
            phase_b_core.dataset_hash(b.final_rows),
        )
        self.assertEqual(
            evaluator.strategy_fingerprint(a.adaptive_planted_candidate),
            evaluator.strategy_fingerprint(b.adaptive_planted_candidate),
        )

    def test_different_seeds_change_commitment_and_data(self):
        a = phase_b_core.generate_world(
            world_id="STABLE-TEST-A",
            archetype="STABLE",
            seed=SEED_A,
        )
        b = phase_b_core.generate_world(
            world_id="STABLE-TEST-B",
            archetype="STABLE",
            seed=SEED_B,
        )
        self.assertNotEqual(a.seed_commitment, b.seed_commitment)
        self.assertNotEqual(
            phase_b_core.dataset_hash(a.adaptive_rows),
            phase_b_core.dataset_hash(b.adaptive_rows),
        )

    def test_public_manifest_does_not_reveal_seed_or_planted_strategy(self):
        world = phase_b_core.generate_world(
            world_id="WEAKENING-TEST",
            archetype="WEAKENING",
            seed=SEED_A,
        )
        manifest = world.public_manifest()
        encoded = json.dumps(manifest, sort_keys=True)
        self.assertNotIn("seed_hex", manifest)
        self.assertNotIn("planted", encoded.lower())
        self.assertEqual(manifest["adaptive_rows"], 512)
        self.assertEqual(manifest["final_rows"], 512)
        self.assertEqual(manifest["seed_commitment"], phase_b_core.seed_commitment(SEED_A))

    def test_generated_splits_are_valid_and_separate(self):
        world = phase_b_core.generate_world(
            world_id="STABLE-TEST",
            archetype="STABLE",
            seed=SEED_A,
        )
        evaluator.validate_dataset(world.adaptive_rows)
        evaluator.validate_dataset(world.final_rows)
        self.assertEqual(len(world.adaptive_rows), 512)
        self.assertEqual(len(world.final_rows), 512)
        self.assertNotEqual(
            phase_b_core.dataset_hash(world.adaptive_rows),
            phase_b_core.dataset_hash(world.final_rows),
        )

    def test_planted_candidate_is_valid_and_positive_in_stable_world(self):
        world = phase_b_core.generate_world(
            world_id="STABLE-TEST",
            archetype="STABLE",
            seed=SEED_A,
        )
        adaptive = phase_b_core.evaluate_on_adaptive(
            world, world.adaptive_planted_candidate
        )
        final = phase_b_core.evaluate_on_final(
            world, world.final_planted_candidate
        )
        self.assertEqual(adaptive["validity_status"], "VALID")
        self.assertEqual(final["validity_status"], "VALID")
        self.assertGreater(adaptive["metrics"]["mean_return"], 0.0)
        self.assertGreater(final["metrics"]["mean_return"], 0.0)

    def test_weakening_world_keeps_relation_but_reduces_effect(self):
        world = phase_b_core.generate_world(
            world_id="WEAKENING-TEST",
            archetype="WEAKENING",
            seed=SEED_A,
        )
        self.assertEqual(
            evaluator.strategy_fingerprint(world.adaptive_planted_candidate),
            evaluator.strategy_fingerprint(world.final_planted_candidate),
        )
        adaptive = phase_b_core.evaluate_on_adaptive(
            world, world.adaptive_planted_candidate
        )
        final = phase_b_core.evaluate_on_final(
            world, world.final_planted_candidate
        )
        self.assertGreater(adaptive["metrics"]["mean_return"], 0.0)
        self.assertGreater(final["metrics"]["mean_return"], 0.0)

    def test_break_world_flips_planted_side(self):
        world = phase_b_core.generate_world(
            world_id="BREAK-TEST",
            archetype="BREAK",
            seed=SEED_A,
        )
        self.assertNotEqual(
            evaluator.strategy_fingerprint(world.adaptive_planted_candidate),
            evaluator.strategy_fingerprint(world.final_planted_candidate),
        )
        self.assertNotEqual(
            world.adaptive_planted_candidate["side"],
            world.final_planted_candidate["side"],
        )
        adaptive = phase_b_core.evaluate_on_adaptive(
            world, world.adaptive_planted_candidate
        )
        original_on_final = phase_b_core.evaluate_on_final(
            world, world.adaptive_planted_candidate
        )
        final_plant = phase_b_core.evaluate_on_final(
            world, world.final_planted_candidate
        )
        self.assertGreater(adaptive["metrics"]["mean_return"], 0.0)
        self.assertLess(original_on_final["metrics"]["mean_return"], 0.0)
        self.assertGreater(final_plant["metrics"]["mean_return"], 0.0)

    def test_reveal_packet_matches_seed_commitment_and_hashes(self):
        world = phase_b_core.generate_world(
            world_id="STABLE-REVEAL",
            archetype="STABLE",
            seed=SEED_B,
        )
        packet = phase_b_core.reveal_world(world)
        self.assertEqual(
            phase_b_core.seed_commitment(bytes.fromhex(packet["seed_hex"])),
            packet["seed_commitment"],
        )
        self.assertEqual(
            packet["adaptive_dataset_hash"],
            phase_b_core.dataset_hash(world.adaptive_rows),
        )
        self.assertEqual(
            packet["final_dataset_hash"],
            phase_b_core.dataset_hash(world.final_rows),
        )


if __name__ == "__main__":
    unittest.main()
