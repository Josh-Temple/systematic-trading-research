from __future__ import annotations

from datetime import datetime
import hashlib
import json
from typing import Any, Mapping

ALLOWED_CHECKPOINT_TYPES = {
    "MORNING_STATE",
    "TOKYO_CLOSE_STATE",
    "PRE_FORECAST_STATE",
    "EVENT_DRIVEN",
    "MANUAL",
    "CORRECTION",
}

ALLOWED_CONFIDENCE = {
    "LOW",
    "LOW_TO_MEDIUM",
    "MEDIUM",
    "MEDIUM_TO_HIGH",
    "HIGH",
    "UNKNOWN",
}

REQUIRED_FIELDS = {
    "schema_version",
    "state_id",
    "research_line_id",
    "observed_at",
    "retrieved_at",
    "checkpoint_type",
    "source_cutoff",
    "market_open_state",
    "price_state",
    "rates_state",
    "policy_state",
    "macro_news_facts",
    "scheduled_events_known",
    "source_refs",
    "facts",
    "interpretations",
    "change_since_prior",
    "base_case",
    "alternative_case",
    "invalidation_conditions",
    "confidence",
    "next_watch_items",
    "benchmark_relation",
    "corrects_state_id",
    "entry_hash",
}

BENCHMARK_FALSE_FIELDS = {
    "is_scored_forecast",
    "may_overwrite_frozen_forecast",
    "may_supply_post_cutoff_information_retroactively",
    "canonical_scored_input_substitute",
}


def _aware_iso8601(value: str, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must be timezone-aware")
    return parsed


def canonical_entry_sha256(entry: Mapping[str, Any]) -> str:
    payload = {k: v for k, v in entry.items() if k != "entry_hash"}
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_state_entry(entry: Mapping[str, Any], *, verify_hash: bool = True) -> None:
    missing = REQUIRED_FIELDS - set(entry)
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")

    checkpoint_type = entry["checkpoint_type"]
    if checkpoint_type not in ALLOWED_CHECKPOINT_TYPES:
        raise ValueError("invalid checkpoint_type")

    if entry["confidence"] not in ALLOWED_CONFIDENCE:
        raise ValueError("invalid confidence")

    observed_at = _aware_iso8601(entry["observed_at"], "observed_at")
    retrieved_at = _aware_iso8601(entry["retrieved_at"], "retrieved_at")
    source_cutoff = _aware_iso8601(entry["source_cutoff"], "source_cutoff")

    if source_cutoff > observed_at:
        raise ValueError("source_cutoff must not be after observed_at")
    if observed_at > retrieved_at:
        raise ValueError("observed_at must not be after retrieved_at")

    benchmark_relation = entry["benchmark_relation"]
    if not isinstance(benchmark_relation, Mapping):
        raise ValueError("benchmark_relation must be an object")
    for field in BENCHMARK_FALSE_FIELDS:
        if benchmark_relation.get(field) is not False:
            raise ValueError(f"{field} must remain false for live journal entries")

    corrects_state_id = entry["corrects_state_id"]
    if checkpoint_type == "CORRECTION":
        if corrects_state_id in ("", "UNKNOWN", "NOT_APPLICABLE", None):
            raise ValueError("CORRECTION requires corrects_state_id")
    elif corrects_state_id != "NOT_APPLICABLE":
        raise ValueError("non-correction entry must use NOT_APPLICABLE")

    if verify_hash and entry["entry_hash"] != canonical_entry_sha256(entry):
        raise ValueError("entry_hash mismatch")
