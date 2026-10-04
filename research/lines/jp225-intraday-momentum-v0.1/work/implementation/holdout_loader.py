"""Fail-closed 2026 holdout gate. Both decision and independent review validate before reader invocation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _valid_sha256(value) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(c in "0123456789abcdef" for c in value)
    )


def load_holdout(
    path,
    decision_path,
    expected_decision_sha256,
    audit_path,
    expected_audit_sha256,
    expected_binding,
    reader,
):
    if not _valid_sha256(expected_decision_sha256) or not _valid_sha256(expected_audit_sha256):
        raise PermissionError("HOLDOUT_RECEIPT_IDENTITY_FAILURE")

    decision_bytes = Path(decision_path).read_bytes()
    if _digest_bytes(decision_bytes) != expected_decision_sha256:
        raise PermissionError("CONFIRMATION_DECISION_IDENTITY_FAILURE")

    d = json.loads(decision_bytes)
    required = {
        "spec_sha256",
        "code_sha256",
        "input_sha256",
        "source_manifest_sha256",
        "result_sha256",
    }
    if (
        d.get("confirmation_advancement") is not True
        or d.get("classification") != "IMOM_ADVANCE_TO_2026_HOLDOUT"
        or d.get("sample") != "2025_CONFIRMATION"
        or d.get("binding") != expected_binding
        or set(expected_binding) != required
        or any(not _valid_sha256(v) for v in expected_binding.values())
    ):
        raise PermissionError("HOLDOUT_LOCKED")

    audit_bytes = Path(audit_path).read_bytes()
    if _digest_bytes(audit_bytes) != expected_audit_sha256:
        raise PermissionError("INDEPENDENT_REVIEW_IDENTITY_FAILURE")
    audit = json.loads(audit_bytes)
    if (
        audit.get("status") != "PASS"
        or audit.get("independent_review") != "PASS"
        or audit.get("scope") != "2026_HOLDOUT_UNLOCK"
        or audit.get("sample") != "2025_CONFIRMATION"
        or audit.get("decision_sha256") != expected_decision_sha256
        or audit.get("binding") != expected_binding
    ):
        raise PermissionError("HOLDOUT_INDEPENDENT_REVIEW_REQUIRED")

    return reader(path)
