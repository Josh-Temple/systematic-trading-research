"""Outcome-blind monetary-policy feature builder for RL-FXMP-001.

This module does not read FX prices or outcomes. It consumes already-selected
synthetic/event pair identities plus BIS policy-rate endpoint values.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
import json
import re
from typing import Any

MONTH_RE = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])$")

STATUS_AVAILABLE = "AVAILABLE"
STATUS_UNAVAILABLE = "UNAVAILABLE"

REASON_RATE_UNAVAILABLE = "POLICY_RATE_UNAVAILABLE"
REASON_BREAK = "POLICY_INSTRUMENT_BREAK_CROSSED"
REASON_MISSING = "POLICY_SOURCE_MISSING"
REASON_INVALID = "POLICY_SOURCE_INVALID"


def month_index(month: str) -> int:
    m = MONTH_RE.match(month)
    if not m:
        raise ValueError(f"invalid month: {month}")
    return int(m.group(1)) * 12 + int(m.group(2)) - 1


def _finite_decimal(raw: Any) -> Decimal | None:
    if raw is None:
        return None
    try:
        value = Decimal(str(raw))
    except (InvalidOperation, ValueError):
        return None
    if not value.is_finite():
        return None
    return value


def _guard_reason(currency: str, old_month: str, new_month: str, source_lock: dict) -> str | None:
    old_i = month_index(old_month)
    new_i = month_index(new_month)
    if old_i >= new_i:
        return REASON_INVALID

    guards = source_lock["monthly_feature_guards"]

    for start, end in guards.get("unavailable_month_ranges", {}).get(currency, []):
        start_i = month_index(start)
        end_i = month_index(end)
        if old_i <= end_i and new_i >= start_i:
            return REASON_RATE_UNAVAILABLE

    switch = guards.get("instrument_switch_months", {}).get(currency)
    if switch is not None:
        switch_i = month_index(switch)
        if old_i < switch_i <= new_i:
            return REASON_BREAK

    return None


def policy_change(
    currency: str,
    old_month: str,
    new_month: str,
    policy_values: dict[tuple[str, str], Any],
    source_lock: dict,
) -> tuple[Decimal | None, str | None]:
    reason = _guard_reason(currency, old_month, new_month, source_lock)
    if reason is not None:
        return None, reason

    old_key = (currency, old_month)
    new_key = (currency, new_month)
    if old_key not in policy_values or new_key not in policy_values:
        return None, REASON_MISSING

    old_value = _finite_decimal(policy_values[old_key])
    new_value = _finite_decimal(policy_values[new_key])
    if old_value is None or new_value is None:
        return None, REASON_INVALID

    return new_value - old_value, None


def build_feature_record(event: dict, policy_values: dict, source_lock: dict) -> dict:
    required = ("event_id", "a", "b", "policy_old_month", "policy_new_month")
    for key in required:
        if key not in event:
            raise KeyError(key)

    a = event["a"]
    b = event["b"]
    old_month = event["policy_old_month"]
    new_month = event["policy_new_month"]

    p_a, reason_a = policy_change(a, old_month, new_month, policy_values, source_lock)
    p_b, reason_b = policy_change(b, old_month, new_month, policy_values, source_lock)

    base = {
        "event_id": event["event_id"],
        "a": a,
        "b": b,
        "policy_old_month": old_month,
        "policy_new_month": new_month,
    }

    if reason_a is not None or reason_b is not None:
        reasons = sorted(set(r for r in (reason_a, reason_b) if r is not None))
        return {
            **base,
            "status": STATUS_UNAVAILABLE,
            "reason_codes": reasons,
            "p_a": None,
            "p_b": None,
            "z": None,
            "classification": None,
        }

    assert p_a is not None and p_b is not None
    z = p_a - p_b
    if z > 0:
        classification = "ALIGNED"
    elif z < 0:
        classification = "OPPOSED"
    else:
        classification = "NEUTRAL"

    return {
        **base,
        "status": STATUS_AVAILABLE,
        "reason_codes": [],
        "p_a": format(p_a, "f"),
        "p_b": format(p_b, "f"),
        "z": format(z, "f"),
        "classification": classification,
    }


def build_feature_ledger(events: list[dict], policy_values: dict, source_lock: dict) -> list[dict]:
    records = [build_feature_record(e, policy_values, source_lock) for e in events]
    records.sort(key=lambda x: str(x["event_id"]))
    return records


def canonical_ledger_bytes(records: list[dict]) -> bytes:
    return (json.dumps(records, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
