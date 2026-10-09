import copy
import unittest

from live_state_journal import canonical_entry_sha256, validate_state_entry


def sample_entry():
    entry = {
        "schema_version": "LIVE_MARKET_STATE_ENTRY_v0.1",
        "state_id": "STATE-USDJPY-20261005T083000+0900-MORNING_STATE",
        "research_line_id": "RL-USDJPY-OVERNIGHT-001",
        "observed_at": "2026-10-05T08:30:00+09:00",
        "retrieved_at": "2026-10-05T08:30:05+09:00",
        "checkpoint_type": "MORNING_STATE",
        "source_cutoff": "2026-10-05T08:30:00+09:00",
        "market_open_state": "OPEN",
        "price_state": {},
        "rates_state": {},
        "policy_state": {},
        "macro_news_facts": [],
        "scheduled_events_known": [],
        "source_refs": [],
        "facts": [],
        "interpretations": [],
        "change_since_prior": "NO_MATERIAL_CHANGE",
        "base_case": "UNKNOWN",
        "alternative_case": "UNKNOWN",
        "invalidation_conditions": [],
        "confidence": "UNKNOWN",
        "next_watch_items": [],
        "benchmark_relation": {
            "is_scored_forecast": False,
            "may_overwrite_frozen_forecast": False,
            "may_supply_post_cutoff_information_retroactively": False,
            "canonical_scored_input_substitute": False,
        },
        "corrects_state_id": "NOT_APPLICABLE",
        "entry_hash": "",
    }
    entry["entry_hash"] = canonical_entry_sha256(entry)
    return entry


class LiveStateJournalTests(unittest.TestCase):
    def test_valid_entry(self):
        validate_state_entry(sample_entry())

    def test_hash_is_key_order_stable(self):
        a = sample_entry()
        b = dict(reversed(list(a.items())))
        self.assertEqual(canonical_entry_sha256(a), canonical_entry_sha256(b))

    def test_hash_tamper_rejected(self):
        entry = sample_entry()
        entry["base_case"] = "changed after hash"
        with self.assertRaises(ValueError):
            validate_state_entry(entry)

    def test_future_source_cutoff_rejected(self):
        entry = sample_entry()
        entry["source_cutoff"] = "2026-10-05T08:31:00+09:00"
        entry["entry_hash"] = canonical_entry_sha256(entry)
        with self.assertRaises(ValueError):
            validate_state_entry(entry)

    def test_retrieval_before_observation_rejected(self):
        entry = sample_entry()
        entry["retrieved_at"] = "2026-10-05T08:29:59+09:00"
        entry["entry_hash"] = canonical_entry_sha256(entry)
        with self.assertRaises(ValueError):
            validate_state_entry(entry)

    def test_benchmark_promotion_rejected(self):
        entry = sample_entry()
        entry["benchmark_relation"]["is_scored_forecast"] = True
        entry["entry_hash"] = canonical_entry_sha256(entry)
        with self.assertRaises(ValueError):
            validate_state_entry(entry)

    def test_retroactive_supply_rejected(self):
        entry = sample_entry()
        entry["benchmark_relation"]["may_supply_post_cutoff_information_retroactively"] = True
        entry["entry_hash"] = canonical_entry_sha256(entry)
        with self.assertRaises(ValueError):
            validate_state_entry(entry)

    def test_canonical_input_substitution_rejected(self):
        entry = sample_entry()
        entry["benchmark_relation"]["canonical_scored_input_substitute"] = True
        entry["entry_hash"] = canonical_entry_sha256(entry)
        with self.assertRaises(ValueError):
            validate_state_entry(entry)

    def test_non_correction_cannot_reference_correction_target(self):
        entry = sample_entry()
        entry["corrects_state_id"] = "STATE-OLD"
        entry["entry_hash"] = canonical_entry_sha256(entry)
        with self.assertRaises(ValueError):
            validate_state_entry(entry)

    def test_correction_requires_target(self):
        entry = sample_entry()
        entry["checkpoint_type"] = "CORRECTION"
        entry["corrects_state_id"] = "NOT_APPLICABLE"
        entry["entry_hash"] = canonical_entry_sha256(entry)
        with self.assertRaises(ValueError):
            validate_state_entry(entry)

    def test_valid_correction(self):
        entry = sample_entry()
        entry["checkpoint_type"] = "CORRECTION"
        entry["corrects_state_id"] = "STATE-USDJPY-OLD"
        entry["entry_hash"] = canonical_entry_sha256(entry)
        validate_state_entry(entry)

    def test_naive_timestamp_rejected(self):
        entry = sample_entry()
        entry["observed_at"] = "2026-10-05T08:30:00"
        entry["entry_hash"] = canonical_entry_sha256(entry)
        with self.assertRaises(ValueError):
            validate_state_entry(entry)


if __name__ == "__main__":
    unittest.main()
