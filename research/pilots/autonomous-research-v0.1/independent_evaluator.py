"""Second Phase A evaluator implementation.

This module is intentionally separate from evaluator.py and does not import it.
It is NOT independently authored: it provides implementation diversity, not reviewer/model independence.
"""

from __future__ import annotations

import math
from typing import Any, Iterable

ALLOWED_TOP = {
    "candidate_id",
    "feature",
    "operator",
    "threshold",
    "side",
    "position_size",
    "researcher_note",
}
REQUIRED_TOP = {
    "candidate_id",
    "feature",
    "operator",
    "threshold",
    "side",
    "position_size",
}
ALLOWED_FEATURE = {"source", "transform", "lag"}
REQUIRED_FEATURE = {"source", "transform", "lag"}
SOURCES = {"feature_a", "feature_b"}
TRANSFORMS = {"identity", "lag_diff"}
OPERATORS = {"gt", "lt"}
SIDES = {"long", "short"}


class IndependentInvalid(ValueError):
    pass


class IndependentDatasetFailure(RuntimeError):
    pass


def _finite_float(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise IndependentInvalid(f"{field} must be numeric")
    try:
        value = float(value)
    except (OverflowError, ValueError) as exc:
        raise IndependentInvalid(f"{field} cannot convert to finite float") from exc
    if not math.isfinite(value):
        raise IndependentInvalid(f"{field} must be finite")
    return 0.0 if value == 0.0 else value


def normalize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        raise IndependentInvalid("candidate must be object")

    keys = set(candidate)
    if keys - ALLOWED_TOP:
        raise IndependentInvalid("unknown top-level field")
    if REQUIRED_TOP - keys:
        raise IndependentInvalid("missing top-level field")

    cid = candidate["candidate_id"]
    if not isinstance(cid, str) or not cid or len(cid) > 80:
        raise IndependentInvalid("invalid candidate_id")
    try:
        cid.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise IndependentInvalid("candidate_id must be valid UTF-8") from exc

    note = candidate.get("researcher_note")
    if note is not None:
        if not isinstance(note, str) or len(note) > 1000:
            raise IndependentInvalid("invalid researcher_note")
        try:
            note.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise IndependentInvalid("researcher_note must be valid UTF-8") from exc

    feature = candidate["feature"]
    if not isinstance(feature, dict):
        raise IndependentInvalid("feature must be object")
    fkeys = set(feature)
    if fkeys - ALLOWED_FEATURE or REQUIRED_FEATURE - fkeys:
        raise IndependentInvalid("invalid feature fields")

    source = feature["source"]
    transform = feature["transform"]
    lag = feature["lag"]

    if not isinstance(source, str) or source not in SOURCES:
        raise IndependentInvalid("invalid source")
    if not isinstance(transform, str) or transform not in TRANSFORMS:
        raise IndependentInvalid("invalid transform")
    if isinstance(lag, bool) or not isinstance(lag, int):
        raise IndependentInvalid("invalid lag type")
    if transform == "identity":
        if lag != 0:
            raise IndependentInvalid("identity lag must be zero")
    elif not 1 <= lag <= 5:
        raise IndependentInvalid("lag_diff lag out of range")

    operator = candidate["operator"]
    side = candidate["side"]
    if not isinstance(operator, str) or operator not in OPERATORS:
        raise IndependentInvalid("invalid operator")
    if not isinstance(side, str) or side not in SIDES:
        raise IndependentInvalid("invalid side")

    threshold = _finite_float(candidate["threshold"], "threshold")
    position_size = _finite_float(candidate["position_size"], "position_size")
    if not 0 < position_size <= 1.0:
        raise IndependentInvalid("position_size out of range")

    out = {
        "candidate_id": cid,
        "feature": {"source": source, "transform": transform, "lag": lag},
        "operator": operator,
        "threshold": threshold,
        "side": side,
        "position_size": position_size,
    }
    if note is not None:
        out["researcher_note"] = note
    return out


def clean_rows(rows: Iterable[dict[str, Any]]) -> list[dict[str, float | str]]:
    rows = list(rows)
    if len(rows) < 3:
        raise IndependentDatasetFailure("too few rows")

    out: list[dict[str, float | str]] = []
    previous_ts: str | None = None
    expected = {"timestamp", "feature_a", "feature_b", "next_return"}

    for row in rows:
        if not isinstance(row, dict) or set(row) != expected:
            raise IndependentDatasetFailure("invalid row fields")
        ts = row["timestamp"]
        if not isinstance(ts, str) or ("+" not in ts and not ts.endswith("Z")):
            raise IndependentDatasetFailure("timestamp lacks timezone")
        if previous_ts is not None and ts <= previous_ts:
            raise IndependentDatasetFailure("timestamps not increasing")
        previous_ts = ts

        clean: dict[str, float | str] = {"timestamp": ts}
        for key in ("feature_a", "feature_b", "next_return"):
            value = row[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise IndependentDatasetFailure("dataset value must be numeric")
            try:
                value = float(value)
            except (OverflowError, ValueError) as exc:
                raise IndependentDatasetFailure("dataset value conversion failure") from exc
            if not math.isfinite(value):
                raise IndependentDatasetFailure("dataset value must be finite")
            clean[key] = value
        out.append(clean)
    return out


def evaluate_candidate(
    candidate: dict[str, Any],
    rows: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    c = normalize_candidate(candidate)
    data = clean_rows(rows)

    positions: list[float | None] = []
    feature = c["feature"]
    side_mult = 1.0 if c["side"] == "long" else -1.0

    for i, row in enumerate(data):
        if feature["transform"] == "identity":
            value = float(row[feature["source"]])
        else:
            lag = int(feature["lag"])
            if i < lag:
                positions.append(None)
                continue
            value = float(row[feature["source"]]) - float(data[i - lag][feature["source"]])

        if not math.isfinite(value):
            raise IndependentInvalid("derived feature non-finite")

        hit = value > c["threshold"] if c["operator"] == "gt" else value < c["threshold"]
        positions.append(side_mult * c["position_size"] if hit else 0.0)

    usable = [x for x in positions if x is not None]
    if not usable:
        raise IndependentInvalid("no usable positions")
    if any(not math.isfinite(float(x)) or abs(float(x)) > 1.0 for x in usable):
        raise IndependentInvalid("invalid position")
    if min(usable) == max(usable):
        raise IndependentInvalid("constant position")

    pnl = []
    active = 0
    for pos, row in zip(positions, data):
        if pos is None:
            continue
        if pos != 0.0:
            active += 1
        pnl.append(float(pos) * float(row["next_return"]))

    mean_return = sum(pnl) / len(pnl)
    if not math.isfinite(mean_return):
        raise IndependentInvalid("non-finite mean")

    return {
        "validity_status": "VALID",
        "metrics": {
            "mean_return": mean_return,
            "active_count": active,
            "scored_observations": len(pnl),
        },
    }


def safe_evaluate(
    candidate: dict[str, Any],
    rows: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    try:
        return evaluate_candidate(candidate, rows)
    except IndependentInvalid:
        return {"validity_status": "INVALID", "metrics": {}}
    except IndependentDatasetFailure:
        return {"validity_status": "UNVERIFIED", "metrics": {}}
