from __future__ import annotations

from datetime import datetime, time
from math import isfinite
from typing import Any, Mapping
from zoneinfo import ZoneInfo

TOKYO = ZoneInfo("Asia/Tokyo")
FORECAST_SCHEMA = "JP225_FORECAST_RECORD_v0.1"
REVIEW_SCHEMA = "JP225_REVIEW_RECORD_v0.1"
DRY_RUN_STATUS = "EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT"
ALLOWED_SYSTEMS = {"A1", "A2", "A3"}
ALLOWED_XM_INPUT_STATUS = {"AVAILABLE", "UNAVAILABLE", "PARTIAL"}
ALLOWED_OUTCOME_STATUS = {
    "AVAILABLE",
    "MARKET_OUTCOME_UNAVAILABLE",
    "SOURCE_RETRIEVAL_FAILED",
}


def _parse_iso(value: str, field: str) -> datetime:
    try:
        dt = datetime.fromisoformat(value)
    except Exception as exc:
        raise ValueError(f"{field} must be ISO-8601") from exc
    if dt.tzinfo is None:
        raise ValueError(f"{field} must be timezone-aware")
    return dt


def _assert_list(value: Any, field: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")


def validate_forecast_record(record: Mapping[str, Any]) -> None:
    required = {
        "schema_version",
        "event_id",
        "research_line_id",
        "cohort_status",
        "system_id",
        "forecast_system_version",
        "model_identifier",
        "information_cutoff",
        "issued_at",
        "p_up",
        "forecast_return_bps",
        "top_drivers",
        "counterevidence",
        "invalidation_conditions",
        "source_refs",
        "exact_xm_input_status",
        "protocol_deviations",
        "action_status",
    }
    missing = required.difference(record)
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")

    if record["schema_version"] != FORECAST_SCHEMA:
        raise ValueError("unexpected forecast schema")
    if record["research_line_id"] != "RL-JP225-PROSPECTIVE-001":
        raise ValueError("unexpected research line")
    if record["cohort_status"] != DRY_RUN_STATUS:
        raise PermissionError("formal cohort record is not authorized")
    if record["system_id"] not in ALLOWED_SYSTEMS:
        raise ValueError("system_id must be A1/A2/A3")
    if record["exact_xm_input_status"] not in ALLOWED_XM_INPUT_STATUS:
        raise ValueError("invalid exact_xm_input_status")
    if record["action_status"] != "NO_TRADE":
        raise PermissionError("trading action is not authorized")

    cutoff = _parse_iso(record["information_cutoff"], "information_cutoff").astimezone(TOKYO)
    issued = _parse_iso(record["issued_at"], "issued_at").astimezone(TOKYO)

    if cutoff.timetz().replace(tzinfo=None) != time(8, 0):
        raise ValueError("information cutoff must be 08:00 JST")
    if issued < cutoff:
        raise ValueError("issued_at cannot be before cutoff")
    if issued.date() != cutoff.date():
        raise ValueError("forecast must be issued on the event date")

    p = float(record["p_up"])
    if not isfinite(p) or not 0.01 <= p <= 0.99:
        raise ValueError("p_up must be finite and in [0.01, 0.99]")

    ret = float(record["forecast_return_bps"])
    if not isfinite(ret):
        raise ValueError("forecast_return_bps must be finite")

    for field in (
        "top_drivers",
        "counterevidence",
        "invalidation_conditions",
        "source_refs",
        "protocol_deviations",
    ):
        _assert_list(record[field], field)


def validate_review_record(record: Mapping[str, Any]) -> None:
    required = {
        "schema_version",
        "event_id",
        "research_line_id",
        "cohort_status",
        "reviewed_at",
        "exact_xm_outcome_status",
        "start_quote",
        "end_quote",
        "realized_return_bps",
        "y_up",
        "scores",
        "facts",
        "interpretation",
        "error_attribution",
        "rule_change",
        "notes",
    }
    missing = required.difference(record)
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")

    if record["schema_version"] != REVIEW_SCHEMA:
        raise ValueError("unexpected review schema")
    if record["research_line_id"] != "RL-JP225-PROSPECTIVE-001":
        raise ValueError("unexpected research line")
    if record["cohort_status"] != DRY_RUN_STATUS:
        raise PermissionError("formal cohort review is not authorized")
    if record["exact_xm_outcome_status"] not in ALLOWED_OUTCOME_STATUS:
        raise ValueError("invalid exact_xm_outcome_status")

    reviewed = _parse_iso(record["reviewed_at"], "reviewed_at").astimezone(TOKYO)
    if reviewed.timetz().replace(tzinfo=None) < time(15, 30):
        raise PermissionError("review cannot be finalized before 15:30 JST")

    for field in ("facts", "interpretation", "error_attribution", "notes"):
        _assert_list(record[field], field)

    if record["rule_change"] != "NONE_FROM_SINGLE_DRY_RUN":
        raise PermissionError("single dry run cannot modify v0.1")

    outcome_status = record["exact_xm_outcome_status"]
    if outcome_status != "AVAILABLE":
        forbidden_nonnull = (
            "start_quote",
            "end_quote",
            "realized_return_bps",
            "y_up",
        )
        for field in forbidden_nonnull:
            if record[field] is not None:
                raise ValueError(
                    f"{field} must be null when exact XM outcome is unavailable"
                )
