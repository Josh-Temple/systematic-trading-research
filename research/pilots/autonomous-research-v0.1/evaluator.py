"""Trusted synthetic evaluator for Autonomous Research Pilot v0.1 Phase A.

Standard-library only. No market data is used.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PILOT_ID = "AUTONOMOUS-RESEARCH-PILOT-v0.1-PHASE-A"
RECEIPT_VERSION = "0.1"
DATASET_ID = "SYNTHETIC-PHASE-A-v01"

_ALLOWED_TOP = {
    "candidate_id",
    "feature",
    "operator",
    "threshold",
    "side",
    "position_size",
    "researcher_note",
}
_REQUIRED_TOP = {
    "candidate_id",
    "feature",
    "operator",
    "threshold",
    "side",
    "position_size",
}
_ALLOWED_FEATURE = {"source", "transform", "lag"}
_REQUIRED_FEATURE = {"source", "transform", "lag"}
_ALLOWED_SOURCES = {"feature_a", "feature_b"}
_ALLOWED_TRANSFORMS = {"identity", "lag_diff"}
_ALLOWED_OPERATORS = {"gt", "lt"}
_ALLOWED_SIDES = {"long", "short"}

SYNTHETIC_ROWS = (
    {"timestamp": "2026-01-01T00:00:00+00:00", "feature_a": -1.0, "feature_b": 0.4, "next_return": -0.010},
    {"timestamp": "2026-01-01T00:01:00+00:00", "feature_a": -0.5, "feature_b": 0.2, "next_return": -0.006},
    {"timestamp": "2026-01-01T00:02:00+00:00", "feature_a": 0.2, "feature_b": -0.1, "next_return": 0.003},
    {"timestamp": "2026-01-01T00:03:00+00:00", "feature_a": 0.7, "feature_b": -0.4, "next_return": 0.009},
    {"timestamp": "2026-01-01T00:04:00+00:00", "feature_a": 1.1, "feature_b": -0.6, "next_return": 0.013},
    {"timestamp": "2026-01-01T00:05:00+00:00", "feature_a": -0.2, "feature_b": 0.3, "next_return": -0.002},
    {"timestamp": "2026-01-01T00:06:00+00:00", "feature_a": 0.8, "feature_b": -0.5, "next_return": 0.011},
    {"timestamp": "2026-01-01T00:07:00+00:00", "feature_a": -0.8, "feature_b": 0.6, "next_return": -0.009},
)


class CandidateInvalid(ValueError):
    pass


class EvaluatorFailure(RuntimeError):
    pass


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def hash_json(value: Any) -> str:
    return hash_bytes(_canonical_json(value))


def evaluator_identity() -> str:
    return hash_bytes(Path(__file__).read_bytes())


def dataset_hash(rows: Iterable[dict[str, Any]]) -> str:
    return hash_json(list(rows))


def _finite_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CandidateInvalid(f"{field} must be a number")
    value = float(value)
    if not math.isfinite(value):
        raise CandidateInvalid(f"{field} must be finite")
    # Normalize signed zero so semantically identical strategies share a fingerprint.
    return 0.0 if value == 0.0 else value


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise CandidateInvalid(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def _reject_json_constant(value: str) -> None:
    raise CandidateInvalid(f"non-standard JSON constant is forbidden: {value}")


def load_candidate_json(text: str) -> dict[str, Any]:
    """Parse candidate JSON without duplicate keys or NaN/Infinity extensions."""
    if not isinstance(text, str):
        raise CandidateInvalid("candidate JSON must be text")
    try:
        candidate = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_json_constant,
        )
    except CandidateInvalid:
        raise
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise CandidateInvalid("invalid candidate JSON") from exc
    if not isinstance(candidate, dict):
        raise CandidateInvalid("candidate JSON root must be an object")
    return validate_candidate(candidate)


def validate_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        raise CandidateInvalid("candidate must be an object")

    unknown = set(candidate) - _ALLOWED_TOP
    missing = _REQUIRED_TOP - set(candidate)
    if unknown:
        raise CandidateInvalid(f"unknown top-level fields: {sorted(unknown)}")
    if missing:
        raise CandidateInvalid(f"missing required fields: {sorted(missing)}")

    cid = candidate["candidate_id"]
    if not isinstance(cid, str) or not cid or len(cid) > 80:
        raise CandidateInvalid("candidate_id must be a non-empty string up to 80 chars")

    note = candidate.get("researcher_note")
    if note is not None and (not isinstance(note, str) or len(note) > 1000):
        raise CandidateInvalid("researcher_note must be a string up to 1000 chars")

    feature = candidate["feature"]
    if not isinstance(feature, dict):
        raise CandidateInvalid("feature must be an object")
    unknown_feature = set(feature) - _ALLOWED_FEATURE
    missing_feature = _REQUIRED_FEATURE - set(feature)
    if unknown_feature:
        raise CandidateInvalid(f"unknown feature fields: {sorted(unknown_feature)}")
    if missing_feature:
        raise CandidateInvalid(f"missing feature fields: {sorted(missing_feature)}")

    source = feature["source"]
    transform = feature["transform"]
    lag = feature["lag"]

    if source not in _ALLOWED_SOURCES:
        raise CandidateInvalid("feature.source is not allowed")
    if transform not in _ALLOWED_TRANSFORMS:
        raise CandidateInvalid("feature.transform is not allowed")
    if isinstance(lag, bool) or not isinstance(lag, int):
        raise CandidateInvalid("feature.lag must be an integer")
    if transform == "identity" and lag != 0:
        raise CandidateInvalid("identity transform requires lag=0")
    if transform == "lag_diff" and not 1 <= lag <= 5:
        raise CandidateInvalid("lag_diff requires lag in [1, 5]")

    operator = candidate["operator"]
    side = candidate["side"]
    if operator not in _ALLOWED_OPERATORS:
        raise CandidateInvalid("operator is not allowed")
    if side not in _ALLOWED_SIDES:
        raise CandidateInvalid("side is not allowed")

    threshold = _finite_number(candidate["threshold"], "threshold")
    position_size = _finite_number(candidate["position_size"], "position_size")
    if not 0 < position_size <= 1.0:
        raise CandidateInvalid("position_size must be in (0, 1]")

    return {
        "candidate_id": cid,
        "feature": {"source": source, "transform": transform, "lag": lag},
        "operator": operator,
        "threshold": threshold,
        "side": side,
        "position_size": position_size,
        **({"researcher_note": note} if note is not None else {}),
    }


def strategy_projection(candidate: dict[str, Any]) -> dict[str, Any]:
    """Return only fields that define strategy behavior, excluding IDs/notes."""
    c = validate_candidate(candidate)
    return {
        "feature": c["feature"],
        "operator": c["operator"],
        "threshold": c["threshold"],
        "side": c["side"],
        "position_size": c["position_size"],
    }


def strategy_fingerprint(candidate: dict[str, Any]) -> str:
    return hash_json(strategy_projection(candidate))


def validate_dataset(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = list(rows)
    if len(rows) < 3:
        raise EvaluatorFailure("dataset must contain at least 3 rows")

    out = []
    last_ts = None
    required = {"timestamp", "feature_a", "feature_b", "next_return"}
    for idx, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != required:
            raise EvaluatorFailure(f"row {idx} has invalid fields")
        try:
            ts = datetime.fromisoformat(row["timestamp"])
        except Exception as exc:
            raise EvaluatorFailure(f"row {idx} has invalid timestamp") from exc
        if ts.tzinfo is None:
            raise EvaluatorFailure(f"row {idx} timestamp must be timezone-aware")
        if last_ts is not None and ts <= last_ts:
            raise EvaluatorFailure("timestamps must be strictly increasing")
        last_ts = ts

        clean = {"timestamp": row["timestamp"]}
        for field in ("feature_a", "feature_b", "next_return"):
            value = row[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise EvaluatorFailure(f"row {idx} {field} must be numeric")
            value = float(value)
            if not math.isfinite(value):
                raise EvaluatorFailure(f"row {idx} {field} must be finite")
            clean[field] = value
        out.append(clean)
    return out


def compile_signal(candidate: dict[str, Any], rows: list[dict[str, Any]]) -> list[float | None]:
    c = validate_candidate(candidate)
    f = c["feature"]
    side = 1.0 if c["side"] == "long" else -1.0
    signal: list[float | None] = []

    for i, row in enumerate(rows):
        if f["transform"] == "identity":
            value = row[f["source"]]
        else:
            lag = f["lag"]
            if i < lag:
                signal.append(None)
                continue
            value = row[f["source"]] - rows[i - lag][f["source"]]

        if not math.isfinite(value):
            raise CandidateInvalid("transformed feature must be finite")
        cond = value > c["threshold"] if c["operator"] == "gt" else value < c["threshold"]
        signal.append(side * c["position_size"] if cond else 0.0)

    return signal


def validate_signal(signal: list[float | None], expected_len: int) -> None:
    if len(signal) != expected_len:
        raise CandidateInvalid("compiled signal length mismatch")
    usable = []
    for idx, value in enumerate(signal):
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise CandidateInvalid(f"signal[{idx}] must be numeric or null")
        value = float(value)
        if not math.isfinite(value):
            raise CandidateInvalid(f"signal[{idx}] must be finite")
        if abs(value) > 1.0:
            raise CandidateInvalid(f"signal[{idx}] exceeds max absolute position")
        usable.append(value)

    if not usable:
        raise CandidateInvalid("signal has no usable observations")
    if max(usable) == min(usable):
        raise CandidateInvalid("all-constant signal is invalid in Phase A")


def score_signal(signal: list[float | None], rows: list[dict[str, Any]]) -> dict[str, float | int]:
    pnl = []
    active = 0
    for s, row in zip(signal, rows):
        if s is None:
            continue
        if s != 0:
            active += 1
        pnl.append(float(s) * row["next_return"])
    if not pnl:
        raise CandidateInvalid("no scorable observations")
    mean_return = sum(pnl) / len(pnl)
    if not math.isfinite(mean_return):
        raise CandidateInvalid("non-finite score")
    return {
        "mean_return": mean_return,
        "active_count": active,
        "scored_observations": len(pnl),
    }


def _result_hash_payload(receipt: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in receipt.items() if k not in {"created_at", "result_hash"}}


def _base_receipt(
    candidate: Any,
    rows: Iterable[dict[str, Any]],
    dataset_id: str,
) -> dict[str, Any]:
    candidate_id = candidate.get("candidate_id") if isinstance(candidate, dict) else None
    try:
        candidate_hash = hash_json(candidate)
    except Exception:
        candidate_hash = hash_bytes(repr(candidate).encode("utf-8"))

    try:
        d_hash = dataset_hash(rows)
    except Exception:
        d_hash = None

    return {
        "receipt_version": RECEIPT_VERSION,
        "pilot_id": PILOT_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "candidate_id": candidate_id,
        "candidate_hash": candidate_hash,
        "strategy_fingerprint": None,
        "evaluator_identity": evaluator_identity(),
        "dataset_id": dataset_id,
        "dataset_hash": d_hash,
        "execution_status": "NOT_RUN",
        "validity_status": "UNVERIFIED",
        "scientific_status": "NOT_APPLICABLE",
        "metrics": {},
        "diagnostics": [],
    }


def _evaluate_on_rows(
    candidate: dict[str, Any],
    rows: Iterable[dict[str, Any]],
    *,
    dataset_id: str,
    known_strategy_fingerprints: set[str] | None = None,
) -> dict[str, Any]:
    """Host-only evaluation primitive with explicit dataset authority."""
    rows_list = list(rows)
    receipt = _base_receipt(candidate, rows_list, dataset_id)

    try:
        clean_rows = validate_dataset(rows_list)
        clean_candidate = validate_candidate(candidate)
        receipt["candidate_hash"] = hash_json(clean_candidate)
        fp = strategy_fingerprint(clean_candidate)
        receipt["strategy_fingerprint"] = fp

        if known_strategy_fingerprints and fp in known_strategy_fingerprints:
            receipt["execution_status"] = "SUCCESS"
            receipt["validity_status"] = "DUPLICATE"
            receipt["diagnostics"].append("DUPLICATE_STRATEGY_FINGERPRINT")
        else:
            signal = compile_signal(clean_candidate, clean_rows)
            validate_signal(signal, len(clean_rows))
            metrics = score_signal(signal, clean_rows)
            receipt["execution_status"] = "SUCCESS"
            receipt["validity_status"] = "VALID"
            receipt["metrics"] = metrics
            receipt["diagnostics"].append("CANDIDATE_SCHEMA_VALID")
            receipt["diagnostics"].append("SIGNAL_FINITE_AND_BOUNDED")
            receipt["diagnostics"].append("METRICS_RECOMPUTED_BY_EVALUATOR")

    except CandidateInvalid as exc:
        receipt["execution_status"] = "SUCCESS"
        receipt["validity_status"] = "INVALID"
        receipt["diagnostics"].append(f"CANDIDATE_REJECTED:{exc}")
    except EvaluatorFailure as exc:
        receipt["execution_status"] = "FAILED"
        receipt["validity_status"] = "UNVERIFIED"
        receipt["diagnostics"].append(f"EVALUATOR_FAILURE:{exc}")
    except Exception as exc:
        receipt["execution_status"] = "FAILED"
        receipt["validity_status"] = "UNVERIFIED"
        receipt["diagnostics"].append(f"UNEXPECTED_EVALUATOR_FAILURE:{type(exc).__name__}")

    receipt["result_hash"] = hash_json(_result_hash_payload(receipt))
    return receipt


def evaluate(
    candidate: dict[str, Any],
    *,
    known_strategy_fingerprints: set[str] | None = None,
) -> dict[str, Any]:
    """Evaluate against the Phase A host-owned dataset. Candidate cannot select rows."""
    return _evaluate_on_rows(
        candidate,
        SYNTHETIC_ROWS,
        dataset_id=DATASET_ID,
        known_strategy_fingerprints=known_strategy_fingerprints,
    )


def _event_hash_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in record.items() if k != "event_hash"}


def verify_ledger(path: str | Path) -> dict[str, Any]:
    """Verify the local hash chain. This detects edits; it does not prevent full-file rewrite."""
    path = Path(path)
    if not path.exists():
        return {"events": 0, "last_event_hash": None}

    previous = None
    count = 0
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EvaluatorFailure(f"ledger line {line_no} is not valid JSON") from exc
        if not isinstance(record, dict):
            raise EvaluatorFailure(f"ledger line {line_no} must be an object")
        if record.get("previous_event_hash") != previous:
            raise EvaluatorFailure(f"ledger chain mismatch at line {line_no}")
        expected = hash_json(_event_hash_payload(record))
        if record.get("event_hash") != expected:
            raise EvaluatorFailure(f"ledger event hash mismatch at line {line_no}")
        previous = expected
        count += 1
    return {"events": count, "last_event_hash": previous}


def append_ledger(path: str | Path, event: dict[str, Any]) -> dict[str, Any]:
    """Append a hash-chained canonical JSON event and return the stored record."""
    if not isinstance(event, dict):
        raise EvaluatorFailure("ledger event must be an object")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = verify_ledger(path)
    record = {
        "previous_event_hash": state["last_event_hash"],
        "event": event,
    }
    record["event_hash"] = hash_json(record)
    with path.open("a", encoding="utf-8") as f:
        f.write(_canonical_json(record).decode("utf-8") + "\n")
    return record
