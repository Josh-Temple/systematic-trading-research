import unittest
from copy import deepcopy

from record_contract import validate_forecast_record, validate_review_record


BASE_FORECAST = {
    "schema_version": "JP225_FORECAST_RECORD_v0.1",
    "event_id": "XPF-JP225-20261006",
    "research_line_id": "RL-JP225-PROSPECTIVE-001",
    "cohort_status": "EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT",
    "system_id": "A3",
    "forecast_system_version": "candidate-v0.1",
    "model_identifier": "test-model",
    "information_cutoff": "2026-10-06T08:00:00+09:00",
    "issued_at": "2026-10-06T08:00:10+09:00",
    "p_up": 0.55,
    "forecast_return_bps": 5.0,
    "top_drivers": [],
    "counterevidence": [],
    "invalidation_conditions": [],
    "source_refs": [],
    "exact_xm_input_status": "UNAVAILABLE",
    "protocol_deviations": [],
    "action_status": "NO_TRADE",
}


BASE_REVIEW = {
    "schema_version": "JP225_REVIEW_RECORD_v0.1",
    "event_id": "XPF-JP225-20261006",
    "research_line_id": "RL-JP225-PROSPECTIVE-001",
    "cohort_status": "EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT",
    "reviewed_at": "2026-10-06T15:31:00+09:00",
    "exact_xm_outcome_status": "MARKET_OUTCOME_UNAVAILABLE",
    "start_quote": None,
    "end_quote": None,
    "realized_return_bps": None,
    "y_up": None,
    "scores": {},
    "facts": [],
    "interpretation": [],
    "error_attribution": [],
    "rule_change": "NONE_FROM_SINGLE_DRY_RUN",
    "notes": [],
}


class RecordContractTests(unittest.TestCase):
    def test_valid_dry_run_forecast(self):
        validate_forecast_record(BASE_FORECAST)

    def test_formal_cohort_rejected(self):
        x = deepcopy(BASE_FORECAST)
        x["cohort_status"] = "FORMAL"
        with self.assertRaises(PermissionError):
            validate_forecast_record(x)

    def test_pre_cutoff_issuance_rejected(self):
        x = deepcopy(BASE_FORECAST)
        x["issued_at"] = "2026-10-06T07:59:59+09:00"
        with self.assertRaises(ValueError):
            validate_forecast_record(x)

    def test_wrong_cutoff_rejected(self):
        x = deepcopy(BASE_FORECAST)
        x["information_cutoff"] = "2026-10-06T08:01:00+09:00"
        with self.assertRaises(ValueError):
            validate_forecast_record(x)

    def test_trade_action_rejected(self):
        x = deepcopy(BASE_FORECAST)
        x["action_status"] = "BUY"
        with self.assertRaises(PermissionError):
            validate_forecast_record(x)

    def test_valid_unavailable_review(self):
        validate_review_record(BASE_REVIEW)

    def test_early_review_rejected(self):
        x = deepcopy(BASE_REVIEW)
        x["reviewed_at"] = "2026-10-06T15:29:59+09:00"
        with self.assertRaises(PermissionError):
            validate_review_record(x)

    def test_fake_outcome_on_unavailable_status_rejected(self):
        x = deepcopy(BASE_REVIEW)
        x["realized_return_bps"] = 12.0
        with self.assertRaises(ValueError):
            validate_review_record(x)

    def test_rule_change_rejected(self):
        x = deepcopy(BASE_REVIEW)
        x["rule_change"] = "MOVE_CUTOFF"
        with self.assertRaises(PermissionError):
            validate_review_record(x)


if __name__ == "__main__":
    unittest.main()
