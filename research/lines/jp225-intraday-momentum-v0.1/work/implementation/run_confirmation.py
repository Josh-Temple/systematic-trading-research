"""One-shot 2025 confirmation runner over a source-qualified normalized price-point file."""
from __future__ import annotations

import hashlib
import json
from datetime import date
from math import isfinite
from pathlib import Path

from imom_core import Observation, evaluate_sample

HERE = Path(__file__).resolve().parent
LINE = HERE.parents[1]
SPEC = LINE / "specifications" / "SPEC-JP225-IMOM-001-v01.md"


def digest(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def code_identity() -> str:
    paths = [Path(__file__), HERE / "imom_core.py"]
    payload = {p.name: digest(p) for p in paths}
    return hashlib.sha256(canonical(payload)).hexdigest()


def _load_input(path: str | Path) -> list[Observation]:
    obj = json.loads(Path(path).read_text())
    if set(obj) != {"version", "sample", "rows"}:
        raise ValueError("INPUT_SCHEMA_FAILURE")
    if obj["version"] != "JP225_IMOM_INPUT_v1" or obj["sample"] != "2025_CONFIRMATION":
        raise ValueError("INPUT_IDENTITY_FAILURE")
    rows = obj["rows"]
    if not isinstance(rows, list):
        raise ValueError("INPUT_ROWS_FAILURE")

    out: list[Observation] = []
    seen: set[str] = set()
    for row in rows:
        required = {
            "date", "contract", "early_return", "late_return",
            "signed_return", "signed_points"
        }
        if set(row) != required:
            raise ValueError("ROW_SCHEMA_FAILURE")
        d = date.fromisoformat(row["date"])
        if d.year != 2025 or row["date"] in seen:
            raise ValueError("SAMPLE_BOUNDARY_OR_DUPLICATE")
        seen.add(row["date"])
        if not isinstance(row["contract"], str) or not row["contract"]:
            raise ValueError("CONTRACT_FAILURE")
        for key in ("early_return", "late_return"):
            if not isfinite(float(row[key])):
                raise ValueError("NONFINITE_RETURN")
        for key in ("signed_return", "signed_points"):
            if row[key] is not None and not isfinite(float(row[key])):
                raise ValueError("NONFINITE_SIGN_VALUE")
        early = float(row["early_return"])
        if (early == 0) != (row["signed_return"] is None or row["signed_points"] is None):
            # Both signed fields must be None only for zero predictor.
            if early == 0 or row["signed_return"] is None or row["signed_points"] is None:
                raise ValueError("SIGN_TRANSLATION_FAILURE")
        out.append(Observation(
            trade_date=d,
            contract=row["contract"],
            early_return=early,
            late_return=float(row["late_return"]),
            signed_return=None if row["signed_return"] is None else float(row["signed_return"]),
            signed_points=None if row["signed_points"] is None else float(row["signed_points"]),
        ))
    out.sort(key=lambda x: x.trade_date)
    return out


def run(input_path, gate_path, expected_gate_sha256, out_dir):
    if digest(gate_path) != expected_gate_sha256:
        raise PermissionError("GATE_IDENTITY_FAILURE")

    gate = json.loads(Path(gate_path).read_text())
    input_sha = digest(input_path)
    identity = {
        "spec_sha256": digest(SPEC),
        "code_sha256": code_identity(),
        "input_sha256": input_sha,
        "source_sha256": gate.get("binding", {}).get("source_sha256"),
    }
    if (
        gate.get("status") != "PASS"
        or gate.get("independent_review") != "PASS"
        or gate.get("sample") != "2025_CONFIRMATION"
        or gate.get("binding") != identity
        or not isinstance(identity["source_sha256"], str)
        or len(identity["source_sha256"]) != 64
    ):
        raise PermissionError("CONFIRMATION_GATE_CLOSED")

    marker = Path(str(input_path) + ".CONSUMED.json")
    with marker.open("xb") as f:
        f.write(canonical({
            "status": "STARTED_SAMPLE_CONSUMPTION",
            "gate_sha256": expected_gate_sha256,
            "binding": identity,
        }))

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    (out / "RUN_STARTED.json").write_bytes(canonical({
        "status": "STARTED_SAMPLE_CONSUMPTION",
        "sample": "2025_CONFIRMATION",
        "binding": identity,
    }))

    try:
        obs = _load_input(input_path)
        metrics = evaluate_sample(obs, min_rows=180)
        if metrics["status"] == "INSUFFICIENT_EVENTS":
            classification = "INSUFFICIENT_2025_EVENTS"
            advance = False
        elif metrics["status"] == "SUPPORTED":
            classification = "IMOM_ADVANCE_TO_2026_HOLDOUT"
            advance = True
        else:
            classification = "IMOM_NOT_SUPPORTED_2025"
            advance = False

        if (
            digest(input_path) != input_sha
            or digest(gate_path) != expected_gate_sha256
            or code_identity() != identity["code_sha256"]
            or digest(SPEC) != identity["spec_sha256"]
        ):
            raise PermissionError("INPUT_CHANGED_DURING_RUN")

        result = {
            "status": "COMPLETE",
            "sample": "2025_CONFIRMATION",
            "classification": classification,
            "metrics": metrics,
            "binding": identity,
            "gate_sha256": expected_gate_sha256,
        }
        (out / "RESULT.json").write_bytes(canonical(result))
        result_sha = digest(out / "RESULT.json")
        decision = {
            "confirmation_advancement": advance,
            "classification": classification,
            "sample": "2025_CONFIRMATION",
            "binding": {
                **identity,
                "result_sha256": result_sha,
            },
        }
        (out / "CONFIRMATION_DECISION.json").write_bytes(canonical(decision))
        (out / "sha256_manifest.json").write_bytes(canonical({
            p.name: digest(p) for p in out.iterdir() if p.is_file()
        }))
        return result
    except Exception:
        (out / "RUN_FAILED.json").write_bytes(canonical({
            "status": "FAILED_SAMPLE_CONSUMPTION_RESERVED",
            "requires_recovery_decision": True,
        }))
        raise
