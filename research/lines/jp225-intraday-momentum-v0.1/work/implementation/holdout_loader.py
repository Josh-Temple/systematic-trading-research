"""Fail-closed 2026 holdout gate. Decision validation happens before reader invocation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def load_holdout(path, decision_path, expected_decision_sha256, expected_binding, reader):
    decision_bytes = Path(decision_path).read_bytes()
    if hashlib.sha256(decision_bytes).hexdigest() != expected_decision_sha256:
        raise PermissionError("CONFIRMATION_DECISION_IDENTITY_FAILURE")

    d = json.loads(decision_bytes)
    required = {
        "spec_sha256", "code_sha256", "input_sha256", "source_sha256", "result_sha256"
    }
    if (
        d.get("confirmation_advancement") is not True
        or d.get("classification") != "IMOM_ADVANCE_TO_2026_HOLDOUT"
        or d.get("sample") != "2025_CONFIRMATION"
        or d.get("binding") != expected_binding
        or set(expected_binding) != required
        or any(
            not isinstance(v, str)
            or len(v) != 64
            or any(c not in "0123456789abcdef" for c in v)
            for v in expected_binding.values()
        )
    ):
        raise PermissionError("HOLDOUT_LOCKED")

    return reader(path)
