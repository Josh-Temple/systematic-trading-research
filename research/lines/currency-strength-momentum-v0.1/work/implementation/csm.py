"""Outcome-blind deterministic core for the frozen CSM-002 screen.

The module has no network client and accepts only a source-lock-described CSV
adapter. The human freeze fixes the contract bytes but does not authorize a
market run; independent audit, Integrator gate, and separate X instruction
remain required.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import csv
import hashlib
import hmac
import json
import os
import platform
import random
import re
import shutil
import stat
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence


SPEC_ID = "SPEC-CSM-002-v01"
SPEC_GIT_BLOB_SHA1 = "7fe114e2fcfa33b0565b51c717455abd8837d5d9"
SPEC_SHA256 = "a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2"
ACCEPTED_SPEC_GIT_BLOB_SHA1 = "a073e77dec14337ee20609ed6136e50a8c1e76e2"
ACCEPTED_SPEC_SHA256 = "e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90"
HUMAN_DECISION_ID = "HDEC-CSM-002-20261001"
FREEZE_DECISION_ID = "DEC-CSM-003-FREEZE-20261001"
FREEZE_RECORD_COMMIT = "4ac1e797c777f33a467ec73b250401886d160e80"
HYPOTHESIS_ID = "HYP-CSM-002"
CURRENCIES = ("AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "USD")
NON_EUR_CURRENCIES = tuple(c for c in CURRENCIES if c != "EUR")
EXPECTED_SERIES_BY_CURRENCY = {
    c: f"D.{c}.EUR.SP00.A" for c in NON_EUR_CURRENCIES
}
PACKET_C_LOCK_ID = "CSM-SOURCE-LOCK-ECB-001"
PACKET_C_CALENDAR_ID = "ECB_TARGET_LONG_TERM_2002_RULE"
TARGET_START = "2010-01"
TARGET_END = "2026-09"
SOURCE_START = "2009-11"
SOURCE_END = "2026-09"
BOOTSTRAP_BLOCK_LENGTH = 12
BOOTSTRAP_REPLICATES = 10_000
BOOTSTRAP_SEED = 20_261_001
MIN_ELIGIBLE = 120
MIN_COVERAGE = Decimal("0.80")
CONFIG_PATH = Path(__file__).with_name("config.json")
TRUST_STORE_PATH = Path("/etc/csm-002/trusted-keys.json")
MAX_RECEIPT_TTL_SECONDS = 86_400
SCORE_IDENTITY_SPEC = "CSM-002-EXACT-RATIO-SCORE-IDENTITY-V1"
RSA_SHA256_DIGEST_INFO_PREFIX = bytes.fromhex(
    "3031300d060960864801650304020105000420"
)

# Production validation intentionally does not pin mutable I/E commit identities.
# The integrator and independent-auditor receipts are authenticated by trusted keys,
# carry exact immutable artifact identities, and independently bind the current D bytes.
I2_GATE_PR_NUMBER = 37
E_AUDIT_PR_NUMBER = 38



class DataError(ValueError):
    """Invalid or identity-inconsistent input; never a scientific result."""


class GateError(RuntimeError):
    """Execution is not authorized or a required preflight failed."""


@dataclass(frozen=True)
class QuoteTable:
    values: Mapping[date, Mapping[str, Decimal]]
    statuses: Mapping[date, Mapping[str, str]]
    row_dates: frozenset[date]


@dataclass(frozen=True)
class Signal:
    status: str
    winner: str | None
    loser: str | None
    exact_growth_ratios: Mapping[str, Fraction]


@dataclass(frozen=True)
class SignalEvent:
    target_month: str
    formation_start_month: str
    formation_end_month: str
    target_end_month: str
    formation_start_date: str | None
    formation_end_date: str | None
    target_end_date: str | None
    winner: str | None
    loser: str | None
    status: str
    skip_reason: str | None
    score_identities: Mapping[str, Mapping[str, Any]] = field(default_factory=dict)


@dataclass(frozen=True)
class BootstrapSummary:
    lower_95: Decimal
    upper_95: Decimal
    median: Decimal
    valid_replicates: int
    block_length: int
    seed: int


@dataclass(frozen=True)
class Metrics:
    mean_bps: Decimal | None
    median_bps: Decimal | None
    positive_proportion: Decimal | None
    eligible_count: int
    scheduled_count: int
    skip_count: int
    skip_reasons: Mapping[str, int]


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        _json_safe(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _json_safe(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_safe(item) for item in value]
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def parse_decimal(value: Any, *, field: str = "value") -> Decimal:
    if isinstance(value, (bool, float)) or value is None:
        raise DataError(f"{field}: expected decimal text")
    try:
        parsed = Decimal(str(value).strip())
    except (InvalidOperation, ValueError, AttributeError) as exc:
        raise DataError(f"{field}: invalid decimal") from exc
    if not parsed.is_finite() or parsed <= 0:
        raise DataError(f"{field}: value must be finite and strictly positive")
    return parsed


def parse_iso_date(value: Any, *, field: str = "date") -> date:
    try:
        parsed = date.fromisoformat(str(value))
    except (TypeError, ValueError) as exc:
        raise DataError(f"{field}: expected YYYY-MM-DD") from exc
    if parsed.isoformat() != str(value):
        raise DataError(f"{field}: expected canonical YYYY-MM-DD")
    return parsed


def is_packet_c_source_lock(source_lock: Mapping[str, Any]) -> bool:
    return source_lock.get("source_lock_id") == PACKET_C_LOCK_ID


def is_synthetic_source_lock(source_lock: Mapping[str, Any]) -> bool:
    return (source_lock.get("fixture_status") == "SYNTHETIC"
            or source_lock.get("source_transport") == "SYNTHETIC_FIXTURE_ONLY")


def source_lock_id(source_lock: Mapping[str, Any]) -> Any:
    return source_lock.get("source_lock_id", source_lock.get("id"))


def source_transport(source_lock: Mapping[str, Any]) -> Any:
    if is_packet_c_source_lock(source_lock):
        route = source_lock.get("route", {})
        return route.get("transport") if isinstance(route, Mapping) else None
    return source_lock.get("source_transport")


def source_unit_status_map(source_lock: Mapping[str, Any]) -> dict[str, Any]:
    if is_packet_c_source_lock(source_lock):
        series = source_lock.get("series", [])
        return {
            "unit_by_currency": {
                item["currency"]: item["quote_unit"]
                for item in series if isinstance(item, Mapping)
            },
            "status_policy": {"valid": ["A"], "missing": []},
        }
    return {
        "unit_by_currency": source_lock.get("unit_by_currency"),
        "status_policy": source_lock.get("status_policy"),
    }


def validate_packet_c_source_lock(source_lock: Mapping[str, Any]) -> None:
    """Validate Packet C's exact bounded ECB lock without treating it as gate approval."""
    if source_lock_id(source_lock) != PACKET_C_LOCK_ID:
        raise GateError("Packet C source-lock identity mismatch")
    if source_lock.get("version") != "1.0.0":
        raise GateError("Packet C source-lock version mismatch")
    if source_lock.get("status") != "QUALIFIED_BOUNDED_ROUTE_ONLY":
        raise GateError("Packet C source route is not qualified")
    if source_lock.get("scientific_status") != "NOT_APPLICABLE":
        raise GateError("Packet C source lock claims a scientific result")
    if source_lock.get("market_outcome_access") is not False:
        raise GateError("Packet C source lock cannot authorize market-outcome access")
    if not str(source_lock.get("authoritative_spec", "")).endswith(
        f"{SPEC_ID}.md"
    ):
        raise GateError("Packet C source lock SPEC reference mismatch")

    route = source_lock.get("route")
    if not isinstance(route, Mapping):
        raise GateError("Packet C route identity is absent")
    route_identity = {
        "provider": "European Central Bank (ECB)",
        "dataset": "EXR",
        "transport": "official SDMX REST API",
        "format": "csvdata",
        "organization_code": "4F0",
    }
    if any(route.get(key) != value for key, value in route_identity.items()):
        raise GateError("Packet C route identity mismatch")
    if not str(route.get("endpoint_template", "")).startswith(
        "https://data-api.ecb.europa.eu/service/data/EXR/"
    ):
        raise GateError("Packet C endpoint is not the locked ECB EXR route")

    series = source_lock.get("series")
    if not isinstance(series, list) or len(series) != len(NON_EUR_CURRENCIES):
        raise GateError("Packet C lock must identify exactly seven series")
    by_currency: dict[str, Mapping[str, Any]] = {}
    for item in series:
        if not isinstance(item, Mapping):
            raise GateError("Packet C series record is malformed")
        currency = item.get("currency")
        if currency in by_currency:
            raise GateError("Packet C series currency is duplicated")
        by_currency[str(currency)] = item
    if set(by_currency) != set(NON_EUR_CURRENCIES):
        raise GateError("Packet C series currency universe mismatch")
    for currency, item in by_currency.items():
        expected = {
            "key": EXPECTED_SERIES_BY_CURRENCY[currency],
            "currency_denom": "EUR",
            "quote_unit": f"{currency} per EUR 1",
            "frequency": "D",
            "exr_type": "SP00",
            "exr_suffix": "A",
            "unit": currency,
            "unit_mult": 0,
            "source_agency": "4F0",
            "allowed_statuses": [{"code": "A", "label": "Normal value"}],
        }
        if any(item.get(key) != value for key, value in expected.items()):
            raise GateError("Packet C series identity, unit, or status mismatch")

    parsing = source_lock.get("parsing_and_validation")
    if not isinstance(parsing, Mapping):
        raise GateError("Packet C parse policy is absent")
    if parsing.get("key_identity") != (
        "Each row key/dimension must agree with the requested series and currency; "
        "CURRENCY_DENOM=EUR, FREQ=D, EXR_TYPE=SP00, EXR_SUFFIX=A."
    ):
        raise GateError("Packet C row identity policy mismatch")
    if "Exact 32-column CSV schema" not in str(parsing.get("schema", "")):
        raise GateError("Packet C exact CSV schema policy is absent")
    if "Accept only OBS_STATUS=A" not in str(parsing.get("status", "")):
        raise GateError("Packet C observation-status policy mismatch")

    calendar = source_lock.get("calendar")
    if not isinstance(calendar, Mapping):
        raise GateError("Packet C calendar identity is absent")
    if (calendar.get("id") != PACKET_C_CALENDAR_ID
            or calendar.get("range_start_inclusive") != "2009-11-01"
            or calendar.get("range_end_inclusive") != "2026-09-30"
            or calendar.get("expected_open_day_count") != 4331):
        raise GateError("Packet C calendar scope mismatch")
    for hash_key in ("sha256", "open_dates_sha256", "month_end_identity_sha256"):
        digest = calendar.get(hash_key)
        if not isinstance(digest, str) or len(digest) != 64:
            raise GateError("Packet C calendar hash identity is invalid")

    probe = source_lock.get("probe")
    publication = source_lock.get("publication_and_vintage")
    if not isinstance(probe, Mapping) or not isinstance(publication, Mapping):
        raise GateError("Packet C probe or publication boundary is absent")
    if (probe.get("bounded_period") != {"start": "2009-11-01", "end": "2009-11-30"}
            or probe.get("full_history_coverage_tested") is not False
            or probe.get("obs_value_values_extracted_or_used") is not False
            or probe.get("obs_value_values_emitted") is not False):
        raise GateError("Packet C bounded-probe boundary mismatch")
    outcome_gate = source_lock.get("outcome_gate")
    if not isinstance(outcome_gate, Mapping) or outcome_gate.get("state") != "CLOSED":
        raise GateError("Packet C outcome gate is not recorded CLOSED")
    if (publication.get("same_day_availability") != "UNKNOWN"
            or publication.get("historical_vintage_or_revision_access") != "UNKNOWN"
            or "No same-day tradability" not in str(publication.get("safe_interpretation", ""))):
        raise GateError("Packet C publication-time boundary mismatch")


def validate_series_identity(source_lock: Mapping[str, Any]) -> None:
    if is_packet_c_source_lock(source_lock):
        validate_packet_c_source_lock(source_lock)
        return
    if source_lock.get("id") in (None, ""):
        raise GateError("source lock has no identity")
    if source_lock.get("spec_id") != SPEC_ID:
        raise GateError("source lock SPEC identity mismatch")
    if source_lock.get("series_by_currency") != EXPECTED_SERIES_BY_CURRENCY:
        raise GateError("source lock series identity mismatch")
    field_map = source_lock.get("csv_field_map")
    required_fields = {"date", "series", "value", "unit", "status"}
    if not isinstance(field_map, dict) or not required_fields.issubset(field_map):
        raise GateError("source lock lacks a complete CSV field map")
    if not source_lock.get("unit_by_currency"):
        raise GateError("source lock has no unit map")
    statuses = source_lock.get("status_policy")
    if not isinstance(statuses, dict) or not statuses.get("valid"):
        raise GateError("source lock has no valid-status mapping")
    if set(statuses.get("valid", [])).intersection(statuses.get("missing", [])):
        raise GateError("source lock status mappings overlap")


def _is_placeholder(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return True
    normalized = re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()
    forbidden = {"unknown", "none", "null", "placeholder", "tbd", "todo", "test", "example"}
    return (normalized in forbidden or "synthetic" in normalized
            or "placeholder" in normalized or normalized.startswith("test "))


def _require_identity(value: Any, field: str) -> str:
    if _is_placeholder(value) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{2,127}", value):
        raise GateError(f"gate has missing or placeholder {field}")
    return value


def _parse_aware_time(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise GateError(f"signed receipt missing {field}")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise GateError(f"signed receipt has invalid {field}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise GateError(f"signed receipt {field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _rsa_sha256_verify(message: bytes, signature_b64: str, public_key: Mapping[str, Any]) -> None:
    try:
        modulus = int(str(public_key["n_hex"]), 16)
        exponent = int(public_key["e"])
        signature = base64.b64decode(signature_b64, validate=True)
    except (KeyError, TypeError, ValueError, binascii.Error) as exc:
        raise GateError("receipt signature or trusted public key is malformed") from exc
    length = (modulus.bit_length() + 7) // 8
    if modulus.bit_length() < 2048 or exponent < 3 or exponent % 2 == 0:
        raise GateError("trusted RSA key is below the required security floor")
    if len(signature) != length or int.from_bytes(signature, "big") >= modulus:
        raise GateError("receipt signature has invalid length or range")
    encoded = pow(int.from_bytes(signature, "big"), exponent, modulus).to_bytes(length, "big")
    digest_info = RSA_SHA256_DIGEST_INFO_PREFIX + hashlib.sha256(message).digest()
    padding_length = length - len(digest_info) - 3
    if padding_length < 8:
        raise GateError("trusted RSA key is too short for SHA-256")
    expected = b"\x00\x01" + b"\xff" * padding_length + b"\x00" + digest_info
    if not hmac.compare_digest(encoded, expected):
        raise GateError("receipt signature verification failed")


def _verify_signed_envelope(
    envelope: Mapping[str, Any], trusted_keys: Mapping[str, Mapping[str, Any]],
    *, required_role: str, now: datetime,
) -> Mapping[str, Any]:
    payload = envelope.get("payload")
    signature_doc = envelope.get("signature")
    if not isinstance(payload, Mapping) or not isinstance(signature_doc, Mapping):
        raise GateError("gate receipt is not a signed envelope")
    key_id = _require_identity(signature_doc.get("key_id"), "signing key ID")
    if signature_doc.get("algorithm") != "RSASSA-PKCS1-v1_5-SHA256":
        raise GateError("unsupported receipt signature algorithm")
    key = trusted_keys.get(key_id)
    if not isinstance(key, Mapping):
        raise GateError("receipt signer is not in the trusted key store")
    if key.get("role") != required_role or key.get("revoked") is True:
        raise GateError("receipt signer role is not trusted or key is revoked")
    principal = _require_identity(key.get("principal_id"), "trusted principal ID")
    if payload.get("signer_principal_id") != principal:
        raise GateError("receipt signer principal does not match trusted key")
    issued_at = _parse_aware_time(signature_doc.get("issued_at"), "issued_at")
    expires_at = _parse_aware_time(signature_doc.get("expires_at"), "expires_at")
    current = now.astimezone(timezone.utc)
    if issued_at > current or expires_at <= current:
        raise GateError("receipt is not currently valid or has expired")
    if expires_at <= issued_at or (expires_at - issued_at).total_seconds() > MAX_RECEIPT_TTL_SECONDS:
        raise GateError("receipt validity window is invalid or exceeds 24 hours")
    for field, bound in (("valid_from", issued_at), ("valid_until", expires_at)):
        if key.get(field) is not None:
            key_time = _parse_aware_time(key[field], f"trusted key {field}")
            if (field == "valid_from" and bound < key_time) or (field == "valid_until" and bound > key_time):
                raise GateError("receipt validity exceeds signing key validity")
    signed = {
        "payload": payload,
        "key_id": key_id,
        "algorithm": signature_doc["algorithm"],
        "issued_at": signature_doc["issued_at"],
        "expires_at": signature_doc["expires_at"],
    }
    value = signature_doc.get("signature_b64")
    if not isinstance(value, str) or not value:
        raise GateError("signed receipt is missing its signature")
    _rsa_sha256_verify(canonical_json_bytes(signed), value, key)
    return payload


def load_protected_trust_store(path: Path = TRUST_STORE_PATH) -> dict[str, Mapping[str, Any]]:
    """Load only a root-provisioned, root-owned trust store from the fixed path."""
    if path != TRUST_STORE_PATH:
        raise GateError("production trust store path is fixed")
    try:
        info = path.lstat()
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0
                or info.st_mode & 0o022 or path.is_symlink()):
            raise GateError("trusted key store is not a protected root-owned regular file")
        document = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateError("protected trusted key store is unavailable") from exc
    records = document.get("keys") if isinstance(document, Mapping) else None
    if not isinstance(records, list) or not records:
        raise GateError("protected trusted key store has no configured keys")
    result: dict[str, Mapping[str, Any]] = {}
    for record in records:
        if not isinstance(record, Mapping):
            raise GateError("trusted key store contains a malformed key")
        key_id = _require_identity(record.get("key_id"), "trusted key ID")
        if key_id in result:
            raise GateError("trusted key store contains duplicate key IDs")
        result[key_id] = record
    return result


def _require_hex_digest(value: Any, length: int, field: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(rf"[0-9a-f]{{{length}}}", value):
        raise GateError(f"{field} has invalid digest identity")
    return value


def _validate_i2_gate_identity(identity: Mapping[str, Any]) -> None:
    if identity.get("pr_number") != I2_GATE_PR_NUMBER:
        raise GateError("I2 gate PR identity mismatch")
    for field in ("head_sha", "gate_blob_sha1", "gate_markdown_blob_sha1"):
        _require_hex_digest(identity.get(field), 40, f"I2 {field}")
    for field in ("gate_sha256", "gate_markdown_sha256"):
        _require_hex_digest(identity.get(field), 64, f"I2 {field}")
    if identity.get("gate_status") != "PASS":
        raise GateError("current I2 gate is not PASS")
    if identity.get("market_outcome_access") is not True:
        raise GateError("current I2 gate does not authorize market outcome access")


def _validate_e_audit_identity(identity: Mapping[str, Any]) -> None:
    _require_identity(identity.get("audit_id"), "independent audit ID")
    if identity.get("pr_number") != E_AUDIT_PR_NUMBER:
        raise GateError("independent audit PR identity mismatch")
    for field in ("head_sha", "result_blob_sha1", "matrix_blob_sha1"):
        _require_hex_digest(identity.get(field), 40, f"E {field}")
    for field in ("result_sha256", "matrix_sha256"):
        _require_hex_digest(identity.get(field), 64, f"E {field}")
    if identity.get("status") != "PASS":
        raise GateError("current E audit status is not PASS")
    if identity.get("recommendation") != "ALLOW_I2":
        raise GateError("current E audit does not authorize I2 reconsideration")


def validate_gate_receipt(
    receipt: Mapping[str, Any], source_lock: Mapping[str, Any], *,
    source_lock_raw_bytes: bytes,
    trusted_keys: Mapping[str, Mapping[str, Any]] | None = None,
    expected_file_hashes: Mapping[str, str],
    expected_environment_sha256: str,
    expected_probe_metadata_sha256: str | None,
    expected_calendar_sha256: str,
    now: datetime | None = None,
    expected_current_i2_gate: Mapping[str, Any] | None = None,
    expected_e_audit: Mapping[str, Any] | None = None,
    allow_synthetic_test_fixtures: bool = False,
) -> Mapping[str, Any]:
    """Verify signed E and I2 evidence and every byte identity; reject by default."""
    validate_series_identity(source_lock)
    if not source_lock_raw_bytes:
        raise GateError("exact source-lock file bytes are required")
    try:
        parsed_lock = json.loads(source_lock_raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateError("source-lock bytes are not valid UTF-8 JSON") from exc
    if parsed_lock != source_lock:
        raise GateError("source-lock bytes do not parse to the supplied object")
    if is_synthetic_source_lock(source_lock) and not allow_synthetic_test_fixtures:
        raise GateError("synthetic source lock cannot authorize market access")
    payload = receipt.get("payload") if isinstance(receipt, Mapping) else None
    if not isinstance(payload, Mapping):
        raise GateError("gate receipt is not a signed envelope")
    if payload.get("human_freeze_status") != "FROZEN":
        raise GateError("human has not frozen the exact research contract")
    if payload.get("gate_status") != "PASS":
        raise GateError("market-outcome gate is not PASS")
    if payload.get("market_outcome_access_authorized") is not True:
        raise GateError("market-outcome access is not explicitly authorized")
    if payload.get("data_role") != "EXPLORATORY_DISCOVERY":
        raise GateError("dataset role mismatch")
    for field, expected in (("spec_id", SPEC_ID), ("spec_git_blob_sha1", SPEC_GIT_BLOB_SHA1),
                            ("spec_sha256", SPEC_SHA256), ("hypothesis_id", HYPOTHESIS_ID)):
        if payload.get(field) != expected:
            raise GateError(f"gate {field} identity mismatch")
    for field in ("human_contract_decision_id", "gate_id", "integrator_principal_id", "run_id",
                  "raw_capture_process_id", "access_ledger_id", "outcome_access_operator_id"):
        _require_identity(payload.get(field), field)
    operator_name = payload.get("outcome_access_operator_name")
    if (not isinstance(operator_name, str) or _is_placeholder(operator_name)
            or len(operator_name.split()) < 2):
        raise GateError("gate lacks a named outcome-access operator")
    if payload.get("source_lock_id") != source_lock_id(source_lock):
        raise GateError("gate source-lock identity mismatch")
    if payload.get("source_transport") != source_transport(source_lock):
        raise GateError("gate source transport does not match source lock")
    object_hash = sha256_bytes(canonical_json_bytes(source_lock))
    raw_lock_hash = sha256_bytes(source_lock_raw_bytes)
    if payload.get("source_lock_sha256") != object_hash:
        raise GateError("gate source-lock canonical object identity mismatch")
    if payload.get("source_lock_raw_sha256") != raw_lock_hash:
        raise GateError("gate source-lock raw-byte identity mismatch")
    unit_status_hash = sha256_bytes(canonical_json_bytes(source_unit_status_map(source_lock)))
    if payload.get("unit_status_map_sha256") != unit_status_hash:
        raise GateError("gate unit/status identity mismatch")
    if payload.get("expected_calendar_sha256") != expected_calendar_sha256:
        raise GateError("gate calendar identity mismatch")
    if is_packet_c_source_lock(source_lock):
        if expected_probe_metadata_sha256 is None:
            raise GateError("exact Packet C probe-metadata bytes are required for gate validation")
        if payload.get("probe_metadata_sha256") != expected_probe_metadata_sha256:
            raise GateError("gate Packet C probe-metadata identity mismatch")
        if expected_calendar_sha256 != source_lock["calendar"].get("sha256"):
            raise GateError("expected calendar differs from source-lock identity")
    expected_range = {"source_start": SOURCE_START, "source_end": SOURCE_END,
                      "target_start": TARGET_START, "target_end": TARGET_END}
    if payload.get("time_range") != expected_range:
        raise GateError("gate time-range identity mismatch")
    if payload.get("source_series_keys") != list(EXPECTED_SERIES_BY_CURRENCY.values()):
        raise GateError("gate series keys mismatch")
    if payload.get("code_file_hashes") != dict(expected_file_hashes):
        raise GateError("gate D code/test/config/environment file identity mismatch")
    if payload.get("environment_identity_sha256") != expected_environment_sha256:
        raise GateError("gate environment identity mismatch")
    for field, digest in expected_file_hashes.items():
        if not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
            raise GateError(f"expected D file digest is invalid: {field}")
    if payload.get("synthetic_test_log_sha256") != expected_file_hashes.get("TEST_LOG.txt"):
        raise GateError("gate test-log identity mismatch")
    if payload.get("full_history_run_authorized") is not True:
        raise GateError("full-history execution is not explicitly authorized")
    i2_identity = payload.get("current_i2_gate_identity")
    if not isinstance(i2_identity, Mapping):
        raise GateError("signed receipt lacks the current I2 gate identity")
    _validate_i2_gate_identity(i2_identity)
    if expected_current_i2_gate is not None and i2_identity != dict(expected_current_i2_gate):
        raise GateError("signed receipt does not identify the expected I2 gate")

    audit_identity = payload.get("independent_audit_identity")
    if not isinstance(audit_identity, Mapping):
        raise GateError("signed receipt lacks the current E audit identity")
    _validate_e_audit_identity(audit_identity)
    if expected_e_audit is not None and audit_identity != dict(expected_e_audit):
        raise GateError("signed receipt does not identify the expected E audit")

    key_store = trusted_keys
    if key_store is None:
        key_store = load_protected_trust_store()
    current_time = now or datetime.now(timezone.utc)
    e_envelope = payload.get("independent_audit_attestation")
    if not isinstance(e_envelope, Mapping):
        raise GateError("current independent E audit attestation is missing")
    e_payload = _verify_signed_envelope(
        e_envelope, key_store, required_role="independent_auditor", now=current_time
    )
    if any(e_payload.get(key) != value for key, value in audit_identity.items()):
        raise GateError("signed E audit identity or content does not match gate identity")
    if e_payload.get("audited_d_file_hashes") != dict(expected_file_hashes):
        raise GateError("signed E audit does not bind the current D file hashes")
    if e_payload.get("audited_environment_identity_sha256") != expected_environment_sha256:
        raise GateError("signed E audit does not bind the current environment identity")
    if e_payload.get("audited_spec_sha256") != SPEC_SHA256:
        raise GateError("signed E audit does not bind the frozen SPEC")
    if e_payload.get("audited_source_lock_raw_sha256") != raw_lock_hash:
        raise GateError("signed E audit does not bind the exact source-lock bytes")
    if e_payload.get("audited_calendar_sha256") != expected_calendar_sha256:
        raise GateError("signed E audit does not bind the expected calendar identity")
    if payload.get("independent_audit_envelope_sha256") != sha256_bytes(canonical_json_bytes(e_envelope)):
        raise GateError("signed gate receipt does not bind the E audit signature bytes")
    i2_payload = _verify_signed_envelope(
        receipt, key_store, required_role="integrator", now=current_time
    )
    if i2_payload is not payload:
        raise GateError("signed I2 payload changed during validation")
    trusted_integrator = key_store.get(str(receipt["signature"].get("key_id")), {})
    if payload.get("integrator_principal_id") != trusted_integrator.get("principal_id"):
        raise GateError("integrator identity does not match the trusted signer")
    return payload


def validate_capture_manifest(
    manifest: Mapping[str, Any], raw_bytes: bytes, source_lock: Mapping[str, Any],
    *, source_lock_raw_bytes: bytes, expected_metadata_sha256: str | None = None,
) -> None:
    if manifest.get("capture_status") != "CAPTURED":
        raise GateError("raw-capture preflight is not complete")
    if manifest.get("source_lock_id") != source_lock_id(source_lock):
        raise GateError("raw-capture source identity mismatch")
    if manifest.get("source_lock_sha256") != sha256_bytes(canonical_json_bytes(source_lock)):
        raise GateError("raw-capture source-lock content identity mismatch")
    if manifest.get("source_lock_raw_sha256") != sha256_bytes(source_lock_raw_bytes):
        raise GateError("raw-capture source-lock raw-byte identity mismatch")
    try:
        if json.loads(source_lock_raw_bytes.decode("utf-8")) != source_lock:
            raise GateError("source-lock raw bytes do not parse to the supplied object")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateError("source-lock bytes are not valid UTF-8 JSON") from exc
    if manifest.get("spec_id") != SPEC_ID:
        raise GateError("raw-capture SPEC identity mismatch")
    if manifest.get("data_role") != "EXPLORATORY_DISCOVERY":
        raise GateError("raw-capture dataset role mismatch")
    if manifest.get("requested_start") != "2009-11-01" or manifest.get("requested_end") != "2026-09-30":
        raise GateError("raw-capture requested range differs from the fixed contract")
    if manifest.get("raw_snapshot_sha256") != sha256_bytes(raw_bytes):
        raise GateError("raw-snapshot hash mismatch")
    if manifest.get("source_series_keys") != list(EXPECTED_SERIES_BY_CURRENCY.values()):
        raise GateError("raw-capture series keys mismatch")
    for field in ("access_ledger_id", "retrieval_timestamp", "snapshot_uri"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            raise GateError(f"raw-capture manifest missing {field}")
    try:
        datetime.fromisoformat(manifest["retrieval_timestamp"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise GateError("raw-capture retrieval timestamp is not ISO-8601") from exc
    if manifest.get("identity_check") != "PASS":
        raise GateError("raw-capture identity check did not pass")
    if is_packet_c_source_lock(source_lock) and expected_metadata_sha256 is None:
        raise GateError("exact Packet C probe-metadata bytes are required for capture validation")
    if expected_metadata_sha256 is not None and (
        manifest.get("probe_metadata_sha256") != expected_metadata_sha256
    ):
        raise GateError("raw-capture probe-metadata identity mismatch")


def validate_packet_c_probe_metadata(
    source_lock: Mapping[str, Any], metadata: Mapping[str, Any]
) -> tuple[str, ...]:
    """Return the exact CSV header established by Packet C's metadata artifact."""
    validate_packet_c_source_lock(source_lock)
    probe = source_lock["probe"]
    if metadata.get("probe_id") != probe.get("probe_id"):
        raise GateError("Packet C probe-metadata identity mismatch")
    if metadata.get("data_values_visible") is not False:
        raise GateError("Packet C metadata artifact is not metadata-only")
    if metadata.get("expected_calendar_sha256") != source_lock["calendar"].get("sha256"):
        raise GateError("Packet C metadata calendar identity mismatch")
    records = metadata.get("series")
    if not isinstance(records, list) or len(records) != len(NON_EUR_CURRENCIES):
        raise GateError("Packet C metadata must contain exactly seven series schemas")
    expected_keys = set(EXPECTED_SERIES_BY_CURRENCY.values())
    observed_keys: set[str] = set()
    expected_schema: tuple[str, ...] | None = None
    required = {
        "KEY", "FREQ", "CURRENCY", "CURRENCY_DENOM", "EXR_TYPE", "EXR_SUFFIX",
        "TIME_PERIOD", "OBS_VALUE", "OBS_STATUS", "UNIT", "UNIT_MULT", "SOURCE_AGENCY",
    }
    for record in records:
        if not isinstance(record, Mapping):
            raise GateError("Packet C metadata series schema is malformed")
        key = record.get("series")
        columns = record.get("schema")
        if not isinstance(key, str) or key not in expected_keys or key in observed_keys:
            raise GateError("Packet C metadata series-key set mismatch")
        observed_keys.add(key)
        if not isinstance(columns, list) or not all(isinstance(x, str) for x in columns):
            raise GateError("Packet C metadata CSV schema is malformed")
        schema = tuple(columns)
        if len(schema) != 32 or len(set(schema)) != 32 or not required.issubset(schema):
            raise GateError("Packet C metadata CSV schema is not the locked 32-column schema")
        if expected_schema is None:
            expected_schema = schema
        elif schema != expected_schema:
            raise GateError("Packet C series CSV schemas differ")
    if observed_keys != expected_keys or expected_schema is None:
        raise GateError("Packet C metadata does not cover all seven exact series")
    if metadata.get("all_series_match_expected_calendar_and_schema") is not True:
        raise GateError("Packet C bounded probe did not match its declared schema")
    return expected_schema


def _normalized_source_rows(
    reader: csv.DictReader, source_lock: Mapping[str, Any],
    *, source_metadata: Mapping[str, Any] | None = None,
) -> Iterable[dict[str, Any]]:
    if is_packet_c_source_lock(source_lock):
        if source_metadata is None:
            raise GateError("Packet C probe metadata is required for its CSV adapter")
        validate_packet_c_probe_metadata(source_lock, source_metadata)
        by_key = {item["key"]: item for item in source_lock["series"]}
        for row in reader:
            try:
                series_key = row["KEY"]
                record = by_key[series_key]
                currency = record["currency"]
                dimensions = {
                    "FREQ": record["frequency"],
                    "CURRENCY": currency,
                    "CURRENCY_DENOM": record["currency_denom"],
                    "EXR_TYPE": record["exr_type"],
                    "EXR_SUFFIX": record["exr_suffix"],
                    "SOURCE_AGENCY": record["source_agency"],
                    "UNIT": record["unit"],
                    "UNIT_MULT": str(record["unit_mult"]),
                    "DECIMALS": str(record["decimals"]),
                }
                if any(row[field] != expected for field, expected in dimensions.items()):
                    raise DataError("ECB CSV row dimensions or units mismatch the Packet C lock")
                allowed = {item["code"] for item in record["allowed_statuses"]}
                if row["OBS_STATUS"] not in allowed:
                    raise DataError("ECB CSV observation status is outside the Packet C lock")
                yield {
                    "date": row["TIME_PERIOD"],
                    "currency": currency,
                    "obs_value": row["OBS_VALUE"],
                    "unit": record["quote_unit"],
                    "status": row["OBS_STATUS"],
                    "available_at": "UNKNOWN",
                }
            except KeyError as exc:
                raise DataError("ECB CSV row key or required dimension is absent") from exc
        return

    field_map = source_lock["csv_field_map"]
    series_to_currency = {v: k for k, v in source_lock["series_by_currency"].items()}
    for row in reader:
        try:
            series_key = row[field_map["series"]]
            currency = series_to_currency[series_key]
            normalized: dict[str, Any] = {
                "date": row[field_map["date"]],
                "currency": currency,
                "obs_value": row[field_map["value"]],
                "unit": row[field_map["unit"]],
                "status": row[field_map["status"]],
            }
            if field_map.get("available_at"):
                normalized["available_at"] = row[field_map["available_at"]]
            yield normalized
        except KeyError as exc:
            raise DataError("CSV field or series key is absent from source lock") from exc


def parse_quote_rows(
    rows: Iterable[Mapping[str, Any]],
    *,
    status_policy: Mapping[str, Sequence[str]],
    unit_by_currency: Mapping[str, str],
) -> QuoteTable:
    valid_statuses = set(status_policy.get("valid", ()))
    missing_statuses = set(status_policy.get("missing", ()))
    if not valid_statuses or valid_statuses.intersection(missing_statuses):
        raise DataError("invalid status policy")
    values: dict[date, dict[str, Decimal]] = {}
    statuses: dict[date, dict[str, str]] = {}
    seen: set[tuple[date, str]] = set()
    row_dates: set[date] = set()
    previous_day_by_currency: dict[str, date] = {}
    for row in rows:
        day = parse_iso_date(row.get("date"), field="date")
        currency = str(row.get("currency", ""))
        if currency not in NON_EUR_CURRENCIES:
            raise DataError("unexpected source currency; EUR is synthetic q=1")
        previous_day = previous_day_by_currency.get(currency)
        if previous_day is not None and day < previous_day:
            raise DataError("input dates are not ordered within currency")
        previous_day_by_currency[currency] = day
        key = (day, currency)
        if key in seen:
            raise DataError("duplicate date/currency observation")
        seen.add(key)
        row_dates.add(day)
        expected_unit = unit_by_currency.get(currency)
        if not expected_unit or row.get("unit") != expected_unit:
            raise DataError("currency or unit identity mismatch")
        status = str(row.get("status", ""))
        if status not in valid_statuses and status not in missing_statuses:
            raise DataError("unknown or mismatched observation status")
        available_at = row.get("available_at", "UNKNOWN")
        if available_at not in (None, "", "UNKNOWN"):
            raise DataError("historical AVAILABLE_AT must remain UNKNOWN")
        statuses.setdefault(day, {})[currency] = status
        if status in missing_statuses:
            if row.get("obs_value") not in (None, "", "NA"):
                raise DataError("missing status row unexpectedly contains a value")
            continue
        value = parse_decimal(row.get("obs_value"), field="OBS_VALUE")
        values.setdefault(day, {})[currency] = value
    return QuoteTable(values=values, statuses=statuses, row_dates=frozenset(row_dates))


def parse_source_csv(
    raw_bytes: bytes, source_lock: Mapping[str, Any],
    source_metadata: Mapping[str, Any] | None = None,
) -> QuoteTable:
    validate_series_identity(source_lock)
    try:
        text = raw_bytes.decode("utf-8-sig", errors="strict")
    except UnicodeDecodeError as exc:
        raise DataError("source CSV is not UTF-8") from exc
    reader = csv.DictReader(text.splitlines())
    if is_packet_c_source_lock(source_lock):
        if source_metadata is None:
            raise GateError("Packet C probe metadata is required for its CSV adapter")
        schema = validate_packet_c_probe_metadata(source_lock, source_metadata)
        if reader.fieldnames != list(schema):
            raise DataError("ECB CSV header differs from the exact Packet C schema")
        rows = _normalized_source_rows(
            reader, source_lock, source_metadata=source_metadata
        )
        status_map = source_unit_status_map(source_lock)
        return parse_quote_rows(
            rows,
            status_policy=status_map["status_policy"],
            unit_by_currency=status_map["unit_by_currency"],
        )

    required_columns = set(source_lock["csv_field_map"].values())
    if reader.fieldnames is None or not required_columns.issubset(set(reader.fieldnames)):
        raise DataError("source CSV schema differs from source lock")
    rows = _normalized_source_rows(reader, source_lock)
    return parse_quote_rows(
        rows,
        status_policy=source_lock["status_policy"],
        unit_by_currency=source_lock["unit_by_currency"],
    )


def validate_observed_date_bounds(table: QuoteTable) -> None:
    lower = date(2009, 11, 1)
    upper = date(2026, 9, 30)
    if any(day < lower or day > upper for day in table.row_dates):
        raise DataError("source snapshot contains dates outside the fixed contract range")


def price_vector(table: QuoteTable, day: date) -> dict[str, Decimal] | None:
    row = table.values.get(day, {})
    if any(currency not in row for currency in NON_EUR_CURRENCIES):
        return None
    vector = {currency: row[currency] for currency in NON_EUR_CURRENCIES}
    vector["EUR"] = Decimal(1)
    return {currency: vector[currency] for currency in CURRENCIES}


def _quote_fraction(value: Any, *, field: str) -> Fraction:
    if isinstance(value, Fraction):
        if value <= 0:
            raise DataError(f"{field}: value must be strictly positive")
        return value
    return Fraction(parse_decimal(value, field=field))


def validate_price_vector(prices: Mapping[str, Any]) -> None:
    if set(prices) != set(CURRENCIES):
        raise DataError("price vector must contain exactly the fixed eight currencies")
    for currency, raw in prices.items():
        _quote_fraction(raw, field=f"q[{currency}]")


def exact_growth_ratios(
    old_prices: Mapping[str, Any], new_prices: Mapping[str, Any]
) -> dict[str, Fraction]:
    validate_price_vector(old_prices)
    validate_price_vector(new_prices)
    return {
        currency: _quote_fraction(old_prices[currency], field=f"q_old[{currency}]")
        / _quote_fraction(new_prices[currency], field=f"q_new[{currency}]")
        for currency in CURRENCIES
    }


def select_extrema(
    old_prices: Mapping[str, Any], new_prices: Mapping[str, Any]
) -> Signal:
    ratios = exact_growth_ratios(old_prices, new_prices)
    high = max(ratios.values())
    low = min(ratios.values())
    winners = [c for c, ratio in ratios.items() if ratio == high]
    losers = [c for c, ratio in ratios.items() if ratio == low]
    if len(winners) != 1 or len(losers) != 1:
        return Signal("TIED_EXTREME", None, None, ratios)
    return Signal("UNIQUE_EXTREMA", winners[0], losers[0], ratios)


def max_directed_pair(
    old_prices: Mapping[str, Any], new_prices: Mapping[str, Any]
) -> tuple[Fraction, tuple[tuple[str, str], ...]]:
    ratios = exact_growth_ratios(old_prices, new_prices)
    returns = {
        (base, quote): ratios[base] / ratios[quote]
        for base in CURRENCIES
        for quote in CURRENCIES
        if base != quote
    }
    maximum = max(returns.values())
    pairs = tuple(pair for pair, ratio in returns.items() if ratio == maximum)
    return maximum, pairs


def cross_quote_vector(
    prices: Mapping[str, Any], numeraire: str
) -> dict[str, Fraction]:
    if numeraire not in CURRENCIES:
        raise DataError("unknown numeraire")
    validate_price_vector(prices)
    denominator = _quote_fraction(prices[numeraire], field=f"q[{numeraire}]")
    return {
        currency: _quote_fraction(prices[currency], field=f"q[{currency}]") / denominator
        for currency in CURRENCIES
    }


def _decimal_ln_ratio(numerator: Decimal, denominator: Decimal) -> Decimal:
    if numerator <= 0 or denominator <= 0:
        raise DataError("log ratio needs strictly positive inputs")
    with localcontext() as ctx:
        ctx.prec = 50
        return (numerator / denominator).ln()


def pair_log_return(
    base: str,
    quote: str,
    old_prices: Mapping[str, Decimal],
    new_prices: Mapping[str, Decimal],
) -> Decimal:
    """Log return of q_quote/q_base; no simple-return or P/L conversion."""
    validate_price_vector(old_prices)
    validate_price_vector(new_prices)
    if base not in CURRENCIES or quote not in CURRENCIES or base == quote:
        raise DataError("invalid directed pair")
    old_pair = (
        _quote_fraction(old_prices[quote], field=f"q_old[{quote}]")
        / _quote_fraction(old_prices[base], field=f"q_old[{base}]")
    )
    new_pair = (
        _quote_fraction(new_prices[quote], field=f"q_new[{quote}]")
        / _quote_fraction(new_prices[base], field=f"q_new[{base}]")
    )
    exact_return_ratio = new_pair / old_pair
    with localcontext() as ctx:
        ctx.prec = 50
        decimal_ratio = Decimal(exact_return_ratio.numerator) / Decimal(exact_return_ratio.denominator)
        return decimal_ratio.ln()


def equal_pair_average_log_strength(
    old_prices: Mapping[str, Decimal], new_prices: Mapping[str, Decimal]
) -> dict[str, Decimal]:
    ratios = exact_growth_ratios(old_prices, new_prices)
    with localcontext() as ctx:
        ctx.prec = 50
        scores = {c: Decimal(r.numerator) / Decimal(r.denominator) for c, r in ratios.items()}
        log_scores = {c: value.ln() for c, value in scores.items()}
        return {
            c: sum((log_scores[c] - log_scores[o] for o in CURRENCIES if o != c), Decimal(0))
            / Decimal(len(CURRENCIES) - 1)
            for c in CURRENCIES
        }


def month_shift(month: str, offset: int) -> str:
    try:
        year_s, month_s = month.split("-")
        ordinal = int(year_s) * 12 + int(month_s) - 1 + offset
        year, month_num = divmod(ordinal, 12)
        if not 1 <= int(month_s) <= 12:
            raise ValueError
        return f"{year:04d}-{month_num + 1:02d}"
    except (ValueError, AttributeError) as exc:
        raise DataError("month must be YYYY-MM") from exc


def month_range(start: str, end: str) -> tuple[str, ...]:
    if start > end:
        raise DataError("month range is reversed")
    result: list[str] = []
    current = start
    while current <= end:
        result.append(current)
        current = month_shift(current, 1)
    return tuple(result)


def _endpoint_reason(
    table: QuoteTable, expected_date: date, endpoint_month: str
) -> str | None:
    vector = price_vector(table, expected_date)
    if vector is not None:
        return None
    dates_in_month = [d for d in table.row_dates if d.strftime("%Y-%m") == endpoint_month]
    if not dates_in_month:
        return f"WHOLE_MISSING_MONTH:{endpoint_month}"
    if expected_date not in table.row_dates:
        return f"MISSING_EXPECTED_ENDPOINT:{endpoint_month}@{expected_date.isoformat()}"
    missing = [c for c in NON_EUR_CURRENCIES if c not in table.values.get(expected_date, {})]
    currency = missing[0] if missing else "UNKNOWN"
    return f"MISSING_CURRENCY:{currency}@{endpoint_month}"


def _score_input_record(table: QuoteTable, day: date, currency: str) -> dict[str, Any]:
    if currency == "EUR":
        return {"date": day.isoformat(), "currency": currency,
                "value": "1", "status": "SYNTHETIC_NUMERAIRE"}
    value = table.values.get(day, {}).get(currency)
    status = table.statuses.get(day, {}).get(currency)
    return {
        "date": day.isoformat(),
        "currency": currency,
        "value": str(value) if value is not None else None,
        "status": status if status is not None else ("PRESENT" if value is not None else "MISSING"),
    }


def formation_score_identities(
    table: QuoteTable, formation_start: date | None, formation_end: date | None
) -> dict[str, dict[str, Any]]:
    """Identify each exact formation score without consulting a target endpoint."""
    identities: dict[str, dict[str, Any]] = {}
    for currency in CURRENCIES:
        if formation_start is None or formation_end is None:
            missing_input_hash = sha256_bytes(canonical_json_bytes({
                "identity_type": "FORMATION_SCORE_INPUTS_UNAVAILABLE",
                "score_spec": SCORE_IDENTITY_SPEC,
                "currency": currency,
                "formation_start": formation_start.isoformat() if formation_start else None,
                "formation_end": formation_end.isoformat() if formation_end else None,
                "reason": "NO_EXPECTED_FORMATION_ENDPOINT",
            }))
            identities[currency] = {
                "status": "UNAVAILABLE",
                "identity_sha256": sha256_bytes(canonical_json_bytes({
                    "identity_type": "FORMATION_SCORE_UNAVAILABLE",
                    "score_spec": SCORE_IDENTITY_SPEC,
                    "currency": currency,
                    "formation_start": formation_start.isoformat() if formation_start else None,
                    "formation_end": formation_end.isoformat() if formation_end else None,
                    "input_identity_sha256": missing_input_hash,
                    "reason": "NO_EXPECTED_FORMATION_ENDPOINT",
                })),
                "input_identity_sha256": missing_input_hash,
                "exact_growth_ratio": None,
                "score_spec": SCORE_IDENTITY_SPEC,
            }
            continue
        start_input = _score_input_record(table, formation_start, currency)
        end_input = _score_input_record(table, formation_end, currency)
        input_hash = sha256_bytes(canonical_json_bytes({
            "identity_type": "FORMATION_SCORE_INPUTS",
            "formation_start": start_input,
            "formation_end": end_input,
        }))
        start_value = start_input["value"]
        end_value = end_input["value"]
        ratio: Fraction | None = None
        if start_value is not None and end_value is not None:
            ratio = Fraction(Decimal(start_value)) / Fraction(Decimal(end_value))
        score_doc = {
            "identity_type": "FORMATION_SCORE",
            "spec_id": SPEC_ID,
            "spec_sha256": SPEC_SHA256,
            "score_spec": SCORE_IDENTITY_SPEC,
            "score_definition": "s_i=ln(q_i(formation_start)/q_i(formation_end)); exact ratio used for ordering",
            "currency": currency,
            "formation_start": formation_start.isoformat(),
            "formation_end": formation_end.isoformat(),
            "input_identity_sha256": input_hash,
            "exact_growth_ratio": ratio,
        }
        identities[currency] = {
            "status": "AVAILABLE" if ratio is not None else "UNAVAILABLE",
            "identity_sha256": sha256_bytes(canonical_json_bytes(score_doc)),
            "input_identity_sha256": input_hash,
            "exact_growth_ratio": ratio,
            "score_spec": SCORE_IDENTITY_SPEC,
        }
    return identities


def build_signal_events(
    target_months: Sequence[str],
    month_end_dates: Mapping[str, str],
    table: QuoteTable,
) -> tuple[SignalEvent, ...]:
    """Create the full scheduled grid; each signal sees only its formation endpoints."""
    events: list[SignalEvent] = []
    previous_target: str | None = None
    for target_month in target_months:
        if previous_target is not None and target_month <= previous_target:
            raise DataError("target months must be strictly ordered")
        previous_target = target_month
        formation_start_month = month_shift(target_month, -2)
        formation_end_month = month_shift(target_month, -1)
        needed_months = (formation_start_month, formation_end_month, target_month)
        dates: list[date | None] = []
        reason: str | None = None
        for index, month in enumerate(needed_months):
            raw_day = month_end_dates.get(month)
            if raw_day is None:
                reason = f"NO_EXPECTED_ENDPOINT:{month}"
                dates.append(None)
                continue
            day = parse_iso_date(raw_day, field=f"month_end_dates[{month}]")
            if day.strftime("%Y-%m") != month:
                raise DataError("calendar endpoint does not belong to its month")
            dates.append(day)
            # Only the two formation endpoints may influence the pre-outcome ledger.
            if index < 2:
                endpoint_problem = _endpoint_reason(table, day, month)
                if endpoint_problem and reason is None:
                    reason = endpoint_problem

        start_day, formation_day, target_day = dates
        score_identities = formation_score_identities(table, start_day, formation_day)
        winner: str | None = None
        loser: str | None = None
        signal_status = "UNAVAILABLE"
        if start_day is not None and formation_day is not None:
            start_prices = price_vector(table, start_day)
            formation_prices = price_vector(table, formation_day)
            if start_prices is not None and formation_prices is not None:
                signal = select_extrema(start_prices, formation_prices)
                signal_status = signal.status
                winner, loser = signal.winner, signal.loser
                if signal.status == "TIED_EXTREME" and reason is None:
                    reason = "TIED_EXTREME"
        if reason is None and (winner is None or loser is None):
            reason = "SIGNAL_UNAVAILABLE"
        status = "READY" if reason is None else "SKIP"
        events.append(
            SignalEvent(
                target_month=target_month,
                formation_start_month=formation_start_month,
                formation_end_month=formation_end_month,
                target_end_month=target_month,
                formation_start_date=start_day.isoformat() if start_day else None,
                formation_end_date=formation_day.isoformat() if formation_day else None,
                target_end_date=target_day.isoformat() if target_day else None,
                winner=winner,
                loser=loser,
                status=status,
                skip_reason=reason,
                score_identities=score_identities,
            )
        )
    return tuple(events)


def event_ledger_payload(events: Sequence[SignalEvent]) -> dict[str, Any]:
    rows = []
    for event in events:
        row = asdict(event)
        row["a"] = event.winner
        row["b"] = event.loser
        rows.append(row)
    return {
        "record_type": "PRE_OUTCOME_EVENT_LEDGER",
        "spec_id": SPEC_ID,
        "data_role": "EXPLORATORY_DISCOVERY",
        "temporal_claim": "REFERENCE_ASSOCIATION_ONLY",
        "events": rows,
    }


def persist_event_ledger(
    events: Sequence[SignalEvent], path: Path,
    *, fault_injector: Callable[[str], None] | None = None,
) -> str:
    payload = canonical_json_bytes(event_ledger_payload(events))
    return atomic_write_verified(path, payload, fault_injector=fault_injector)


def calculate_outcomes_after_ledger(
    events: Sequence[SignalEvent],
    table: QuoteTable,
    *,
    ledger_path: Path,
    expected_ledger_sha256: str,
) -> tuple[Decimal | None, ...]:
    if not ledger_path.is_file():
        raise GateError("event ledger must be persisted before outcome calculation")
    raw_ledger = ledger_path.read_bytes()
    if sha256_bytes(raw_ledger) != expected_ledger_sha256:
        raise GateError("event-ledger identity mismatch")
    expected_payload = canonical_json_bytes(event_ledger_payload(events))
    if raw_ledger != expected_payload:
        raise GateError("event-ledger content does not match the signal events")
    outcomes: list[Decimal | None] = []
    for event in events:
        if event.status != "READY":
            outcomes.append(None)
            continue
        if not event.winner or not event.loser or not event.formation_end_date or not event.target_end_date:
            raise DataError("READY event lacks pair or target endpoints")
        formation_end = parse_iso_date(event.formation_end_date)
        target_end = parse_iso_date(event.target_end_date)
        start_prices = price_vector(table, formation_end)
        end_prices = price_vector(table, target_end)
        if start_prices is None:
            raise DataError("READY event formation endpoint became unavailable")
        if end_prices is None:
            outcomes.append(None)
            continue
        outcomes.append(pair_log_return(event.winner, event.loser, start_prices, end_prices))
    return tuple(outcomes)


def percentile_type7(values: Sequence[Decimal], probability: Decimal) -> Decimal:
    if not values or probability < 0 or probability > 1:
        raise DataError("type-7 percentile requires values and p in [0,1]")
    ordered = sorted(values)
    position = Decimal(len(ordered) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - Decimal(lower)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def circular_resample_grid(
    grid: Sequence[Decimal | None], rng: random.Random
) -> tuple[Decimal | None, ...]:
    if not grid:
        raise DataError("bootstrap grid must retain scheduled calendar slots")
    starts_required = (len(grid) + BOOTSTRAP_BLOCK_LENGTH - 1) // BOOTSTRAP_BLOCK_LENGTH
    sample: list[Decimal | None] = []
    for _ in range(starts_required):
        start = rng.randrange(len(grid))
        sample.extend(
            grid[(start + offset) % len(grid)]
            for offset in range(BOOTSTRAP_BLOCK_LENGTH)
        )
    return tuple(sample[: len(grid)])


def _bootstrap_for_test(
    grid: Sequence[Decimal | None], *, replicates: int, seed: int
) -> BootstrapSummary:
    if replicates <= 0 or not grid:
        raise DataError("bootstrap requires a nonempty grid and positive replicate count")
    rng = random.Random(seed)
    means: list[Decimal] = []
    for _ in range(replicates):
        sample = circular_resample_grid(grid, rng)
        valid = [item for item in sample if item is not None]
        if not valid:
            raise DataError("bootstrap replicate has zero valid observations")
        with localcontext() as ctx:
            ctx.prec = 50
            means.append(sum(valid, Decimal(0)) / Decimal(len(valid)))
    return BootstrapSummary(
        lower_95=percentile_type7(means, Decimal("0.025")),
        upper_95=percentile_type7(means, Decimal("0.975")),
        median=percentile_type7(means, Decimal("0.5")),
        valid_replicates=len(means),
        block_length=BOOTSTRAP_BLOCK_LENGTH,
        seed=seed,
    )


def moving_block_bootstrap(grid: Sequence[Decimal | None]) -> BootstrapSummary:
    """Fixed CSM-002 procedure; no public tuning arguments."""
    return _bootstrap_for_test(
        grid, replicates=BOOTSTRAP_REPLICATES, seed=BOOTSTRAP_SEED
    )


def summarize_metrics(
    outcome_grid: Sequence[Decimal | None], events: Sequence[SignalEvent]
) -> Metrics:
    if len(outcome_grid) != len(events):
        raise DataError("outcome grid no longer matches scheduled calendar grid")
    valid = [value for value in outcome_grid if value is not None]
    skip_reasons: dict[str, int] = {}
    for event, outcome in zip(events, outcome_grid):
        if event.status != "READY":
            key = event.skip_reason or "UNKNOWN_SKIP"
            skip_reasons[key] = skip_reasons.get(key, 0) + 1
        elif outcome is None:
            key = f"TARGET_ENDPOINT_UNAVAILABLE:{event.target_month}"
            skip_reasons[key] = skip_reasons.get(key, 0) + 1
    if not valid:
        mean_bps = median_bps = positive_proportion = None
    else:
        with localcontext() as ctx:
            ctx.prec = 50
            bps = [value * Decimal(10_000) for value in valid]
            mean_bps = sum(bps, Decimal(0)) / Decimal(len(bps))
            median_bps = percentile_type7(bps, Decimal("0.5"))
            positive_proportion = Decimal(sum(value > 0 for value in valid)) / Decimal(len(valid))
    return Metrics(
        mean_bps=mean_bps,
        median_bps=median_bps,
        positive_proportion=positive_proportion,
        eligible_count=len(valid),
        scheduled_count=len(events),
        skip_count=len(events) - len(valid),
        skip_reasons=skip_reasons,
    )


def classify_result(
    *, mean_bps: Decimal, lower_95_bps: Decimal,
    eligible_count: int, scheduled_count: int,
) -> tuple[str, str]:
    if scheduled_count <= 0 or eligible_count < 0 or eligible_count > scheduled_count:
        raise DataError("invalid sample counts")
    coverage = Decimal(eligible_count) / Decimal(scheduled_count)
    if eligible_count < MIN_ELIGIBLE or coverage < MIN_COVERAGE:
        return "INSUFFICIENT_EVIDENCE", "HOLD"
    if mean_bps <= 0:
        return "NOT_SUPPORTED", "DEPRIORITIZE"
    if lower_95_bps <= 0:
        return "INCONCLUSIVE", "HOLD"
    return "PROMISING_EXPLORATORY", "ADVANCE_TO_SEPARATE_ECONOMIC_SCREEN_DESIGN"


def validate_temporal_receipt(receipt: Mapping[str, Any]) -> None:
    if receipt.get("temporal_claim") != "REFERENCE_ASSOCIATION_ONLY":
        raise GateError("reference data cannot support an executable-timing claim")
    if receipt.get("available_at") not in (None, "UNKNOWN"):
        raise GateError("historical AVAILABLE_AT must remain UNKNOWN")
    if receipt.get("executable_claim") is True or receipt.get("executed_at"):
        raise GateError("same-reference executable claim is not supported")
    reference_timestamp = receipt.get("reference_timestamp")
    available_at = receipt.get("available_at")
    if reference_timestamp and available_at and reference_timestamp == available_at:
        raise GateError("same timestamp cannot be asserted as executable availability")


def validate_calendar_document(
    calendar_doc: Mapping[str, Any],
    *, source_lock: Mapping[str, Any] | None = None,
    raw_bytes: bytes | None = None,
) -> dict[str, str]:
    if source_lock is not None and is_packet_c_source_lock(source_lock):
        validate_packet_c_source_lock(source_lock)
        identity = source_lock["calendar"]
        if (calendar_doc.get("calendar_id") != identity.get("id")
                or calendar_doc.get("calendar_version") != identity.get("version")
                or calendar_doc.get("range_start_inclusive") != "2009-11-01"
                or calendar_doc.get("range_end_inclusive") != "2026-09-30"
                or calendar_doc.get("timezone_for_date_labels") != "Europe/Berlin"):
            raise GateError("Packet C expected-calendar identity mismatch")
        dates = calendar_doc.get("expected_open_dates")
        closures = calendar_doc.get("weekday_closures")
        if not isinstance(dates, list) or not isinstance(closures, Mapping):
            raise GateError("Packet C expected-calendar date data is malformed")
        if len(dates) != identity.get("expected_open_day_count"):
            raise GateError("Packet C expected-calendar date count mismatch")
        parsed_dates = [parse_iso_date(value, field="expected_open_dates") for value in dates]
        if any(parsed_dates[i] >= parsed_dates[i + 1] for i in range(len(parsed_dates) - 1)):
            raise GateError("Packet C expected-calendar dates are not unique and ordered")
        lower, upper = date(2009, 11, 1), date(2026, 9, 30)
        if any(day < lower or day > upper or day.weekday() >= 5 for day in parsed_dates):
            raise GateError("Packet C expected-calendar contains an out-of-range or weekend date")
        if any(day in set(parsed_dates) for day in (
            parse_iso_date(value, field="weekday_closures") for value in closures
        )):
            raise GateError("Packet C expected-calendar includes a declared closure")
        date_stream = "\n".join(dates).encode("utf-8")
        if sha256_bytes(date_stream) != identity.get("open_dates_sha256"):
            raise GateError("Packet C open-date hash mismatch")
        month_ends: dict[str, str] = {}
        for value in dates:
            month_ends[value[:7]] = value
        expected_months = month_range(SOURCE_START, SOURCE_END)
        if tuple(month_ends) != expected_months:
            raise GateError("Packet C calendar does not cover the fixed month grid")
        month_stream = "\n".join(
            f"{month}={day}" for month, day in month_ends.items()
        ).encode("utf-8")
        if sha256_bytes(month_stream) != identity.get("month_end_identity_sha256"):
            raise GateError("Packet C month-end identity hash mismatch")
        if calendar_doc.get("last_expected_open_day_by_month") != month_ends:
            raise GateError("Packet C declared month ends differ from its open-date grid")
        if raw_bytes is None or sha256_bytes(raw_bytes) != identity.get("sha256"):
            raise GateError("Packet C expected-calendar file hash mismatch")
        return month_ends

    if calendar_doc.get("spec_id") != SPEC_ID:
        raise GateError("calendar SPEC identity mismatch")
    if calendar_doc.get("calendar_timezone") != "Europe/Berlin":
        raise GateError("calendar timezone identity mismatch")
    endpoints = calendar_doc.get("month_end_dates")
    if not isinstance(endpoints, dict):
        raise GateError("calendar month-end mapping is absent")
    required_months = month_range(SOURCE_START, SOURCE_END)
    if set(endpoints) != set(required_months):
        raise GateError("calendar does not cover the fixed source month grid")
    parsed = [parse_iso_date(endpoints[m], field=f"month_end_dates[{m}]") for m in required_months]
    if any(parsed[i] >= parsed[i + 1] for i in range(len(parsed) - 1)):
        raise GateError("calendar endpoints are not strictly ordered")
    if not calendar_doc.get("official_calendar_source"):
        raise GateError("calendar authority is absent")
    return endpoints


def validate_config(config: Mapping[str, Any]) -> None:
    expected = {
        "config_type": "FROZEN_SPEC_MIRROR",
        "spec_id": SPEC_ID,
        "spec_git_blob_sha1": SPEC_GIT_BLOB_SHA1,
        "spec_sha256": SPEC_SHA256,
        "accepted_pre_freeze_spec_git_blob_sha1": ACCEPTED_SPEC_GIT_BLOB_SHA1,
        "accepted_pre_freeze_spec_sha256": ACCEPTED_SPEC_SHA256,
        "human_decision_id": HUMAN_DECISION_ID,
        "freeze_decision_id": FREEZE_DECISION_ID,
        "freeze_record_commit": FREEZE_RECORD_COMMIT,
        "hypothesis_id": HYPOTHESIS_ID,
        "universe": list(CURRENCIES),
        "target_start": TARGET_START,
        "target_end": TARGET_END,
        "source_start": SOURCE_START,
        "source_end": SOURCE_END,
        "formation_months": 1,
        "target_months": 1,
        "bootstrap": {
            "method": "circular_moving_block_calendar_slots",
            "block_length": BOOTSTRAP_BLOCK_LENGTH,
            "replicates": BOOTSTRAP_REPLICATES,
            "seed": BOOTSTRAP_SEED,
            "percentile": "type7",
        },
        "minimum_eligible": MIN_ELIGIBLE,
        "minimum_coverage": str(MIN_COVERAGE),
        "freeze_status": "FROZEN",
        "market_outcome_access": "CLOSED_UNTIL_INTEGRATOR_GATE_PASS_AND_SEPARATE_X_INSTRUCTION",
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise GateError(f"fixed config mismatch: {key}")
    if any("sweep" in key.lower() or "parameter" in key.lower() for key in config):
        raise GateError("configuration contains a forbidden search parameter")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GateError(f"required JSON artifact unavailable: {path.name}") from exc
    if not isinstance(value, dict):
        raise GateError(f"required JSON artifact is not an object: {path.name}")
    return value


def _read_json_with_bytes(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateError(f"required JSON artifact unavailable: {path.name}") from exc
    if not isinstance(value, dict):
        raise GateError(f"required JSON artifact is not an object: {path.name}")
    return value, raw


def _inject_fault(fault_injector: Callable[[str], None] | None, point: str) -> None:
    if fault_injector is not None:
        fault_injector(point)


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    fd = os.open(path, flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write_verified(
    path: Path, payload: bytes, *, validator: Callable[[bytes], None] | None = None,
    fault_injector: Callable[[str], None] | None = None,
) -> str:
    """Write, flush, fsync, verify, then atomically publish a new immutable file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        raise GateError("artifact path already exists; preserve the attempt")
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.stage-", dir=path.parent)
    temp_path = Path(temp_name)
    promoted = False
    try:
        with os.fdopen(fd, "wb") as stream:
            _inject_fault(fault_injector, "write")
            written = stream.write(payload)
            if written != len(payload):
                raise OSError("short write while staging artifact")
            _inject_fault(fault_injector, "flush")
            stream.flush()
            _inject_fault(fault_injector, "file_fsync")
            os.fsync(stream.fileno())
        raw = temp_path.read_bytes()
        if raw != payload:
            raise GateError("staged artifact bytes differ from requested payload")
        if validator is not None:
            validator(raw)
        _inject_fault(fault_injector, "promotion")
        os.link(temp_path, path)
        promoted = True
        temp_path.unlink()
        _inject_fault(fault_injector, "parent_fsync")
        _fsync_directory(path.parent)
        return sha256_bytes(raw)
    except Exception as exc:
        if promoted:
            try:
                path.unlink(missing_ok=True)
                _fsync_directory(path.parent)
            except OSError:
                pass
        try:
            temp_path.unlink(missing_ok=True)
        except OSError:
            pass
        if isinstance(exc, GateError):
            raise
        raise GateError(f"artifact staging or promotion failed: {exc.__class__.__name__}") from exc


def atomic_capture_bytes(
    payload: bytes, destination: Path, *, expected_sha256: str,
    validator: Callable[[bytes], None],
    fault_injector: Callable[[str], None] | None = None,
) -> str:
    """Safely promote captured bytes only after identity and content validation."""
    def validate(raw: bytes) -> None:
        if sha256_bytes(raw) != expected_sha256:
            raise GateError("staged capture raw-byte hash mismatch")
        validator(raw)
    return atomic_write_verified(
        destination, payload, validator=validate, fault_injector=fault_injector
    )


def _validate_staged_output(stage: Path) -> None:
    entries = list(stage.iterdir())
    if any(not stat.S_ISREG(item.lstat().st_mode) for item in entries):
        raise GateError("staged output must contain regular files only")
    receipt_path = stage / "_completion-pending.json"
    if not receipt_path.is_file() or receipt_path.is_symlink():
        raise GateError("staged output lacks its pending completion manifest")
    try:
        receipt = json.loads(receipt_path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateError("staged success receipt is invalid") from exc
    if not isinstance(receipt, Mapping) or receipt.get("promotion_status") != "READY_TO_PROMOTE":
        raise GateError("staged output completion manifest is not ready")
    success_receipt = receipt.get("success_receipt")
    if not isinstance(success_receipt, Mapping) or success_receipt.get("execution_status") != "SUCCESS":
        raise GateError("staged completion manifest lacks the final success receipt")
    expected = success_receipt.get("output_file_sha256")
    if not isinstance(expected, Mapping) or not expected:
        raise GateError("staged success receipt lacks output hashes")
    actual_files = {item.name for item in entries if item.name != "_completion-pending.json"}
    if actual_files != set(expected):
        raise GateError("staged output file set differs from its receipt")
    for name, digest in expected.items():
        if not isinstance(name, str) or Path(name).name != name:
            raise GateError("staged output contains an unsafe receipt path")
        if sha256_file(stage / name) != digest:
            raise GateError("staged output file hash mismatch")


def _fsync_staged_tree(stage: Path) -> None:
    for path in stage.rglob("*"):
        if path.is_symlink():
            raise GateError("staged output may not contain symbolic links")
        if path.is_file():
            with path.open("rb") as stream:
                os.fsync(stream.fileno())
    for path in sorted((p for p in stage.rglob("*") if p.is_dir()), reverse=True):
        _fsync_directory(path)
    _fsync_directory(stage)


def promote_output_directory(
    stage: Path, destination: Path, *,
    fault_injector: Callable[[str], None] | None = None,
) -> None:
    """Promote a complete staged run as one directory rename, rolling back failures."""
    if stage.parent.resolve() != destination.parent.resolve():
        raise GateError("staging and output must share a filesystem parent")
    if destination.exists() or destination.is_symlink():
        raise GateError("output destination already exists; preserve the attempt")
    _validate_staged_output(stage)
    _fsync_staged_tree(stage)
    _validate_staged_output(stage)
    lock_path = destination.parent / f".{destination.name}.promotion.lock"
    lock_fd: int | None = None
    promoted = False
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        if destination.exists() or destination.is_symlink():
            raise GateError("output destination appeared during promotion")
        _inject_fault(fault_injector, "rename")
        os.rename(stage, destination)
        promoted = True
        _inject_fault(fault_injector, "parent_fsync")
        _fsync_directory(destination.parent)
        pending_path = destination / "_completion-pending.json"
        pending = json.loads(pending_path.read_bytes().decode("utf-8"))
        success_bytes = canonical_json_bytes(pending["success_receipt"])

        # Remove the non-success pending marker and durably record that removal
        # before publishing the final SUCCESS receipt. The receipt is therefore
        # the last fallible commit operation. If its own atomic publication fails,
        # atomic_write_verified removes it before this function reports failure.
        pending_path.unlink()
        _fsync_directory(destination)

        _inject_fault(fault_injector, "success_receipt")
        atomic_write_verified(
            destination / "run-receipt.json", success_bytes,
            fault_injector=(
                (lambda point: _inject_fault(fault_injector, f"success_{point}"))
                if fault_injector is not None else None
            ),
        )
    except Exception as exc:
        if promoted:
            try:
                shutil.rmtree(destination)
                _fsync_directory(destination.parent)
            except OSError:
                pass
        if isinstance(exc, GateError):
            raise
        raise GateError(f"output promotion failed: {exc.__class__.__name__}") from exc
    finally:
        if lock_fd is not None:
            os.close(lock_fd)
            try:
                lock_path.unlink(missing_ok=True)
                _fsync_directory(destination.parent)
            except OSError:
                pass


def _block_network_audit(event: str, args: tuple[Any, ...]) -> None:
    if event.startswith(("socket.connect", "socket.getaddrinfo", "subprocess.Popen", "os.system")):
        raise PermissionError("network and subprocess access are disabled during calculation")


def environment_snapshot() -> dict[str, str]:
    return {
        "python_version": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "executable": sys.executable,
        "module_sha256": sha256_file(Path(__file__)),
        "test_code_sha256": sha256_file(Path(__file__).with_name("test_csm.py")),
        "config_sha256": sha256_file(CONFIG_PATH),
    }


def implementation_file_hashes() -> dict[str, str]:
    root = Path(__file__).parent
    names = (
        "csm.py", "test_csm.py", "config.json", "RUNBOOK.md", "ENVIRONMENT.md",
        "RESULT.md", "TEST_MATRIX.md", "TEST_LOG.txt", "fixtures/toy_cases.json",
    )
    return {name: sha256_file(root / name) for name in names}


def environment_identity_sha256(snapshot: Mapping[str, str] | None = None) -> str:
    return sha256_bytes(canonical_json_bytes(snapshot or environment_snapshot()))


def _write_json_exclusive(
    path: Path, value: Any, *, fault_injector: Callable[[str], None] | None = None,
) -> str:
    payload = canonical_json_bytes(value)
    return atomic_write_verified(path, payload, fault_injector=fault_injector)


def run_locked_calculation(args: argparse.Namespace) -> int:
    """Production path. Gate and capture checks precede data load/output."""
    config = _read_json(CONFIG_PATH)
    validate_config(config)
    source_lock, source_lock_raw = _read_json_with_bytes(Path(args.source_lock))
    probe_metadata_path = Path(args.probe_metadata)
    probe_metadata_bytes = probe_metadata_path.read_bytes()
    try:
        probe_metadata = json.loads(probe_metadata_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateError("Packet C probe metadata is not valid UTF-8 JSON") from exc
    if not isinstance(probe_metadata, dict):
        raise GateError("Packet C probe metadata is not a JSON object")
    probe_metadata_hash = sha256_bytes(probe_metadata_bytes)
    if is_packet_c_source_lock(source_lock):
        validate_packet_c_probe_metadata(source_lock, probe_metadata)
    gate = _read_json(Path(args.gate_receipt))
    expected_file_hashes = implementation_file_hashes()
    gate = validate_gate_receipt(
        gate, source_lock,
        source_lock_raw_bytes=source_lock_raw,
        expected_calendar_sha256=(
            source_lock.get("calendar", {}).get("sha256")
            if is_packet_c_source_lock(source_lock)
            else str(source_lock.get("expected_calendar_sha256", ""))
        ),
        expected_file_hashes=expected_file_hashes,
        expected_environment_sha256=environment_identity_sha256(),
        expected_probe_metadata_sha256=probe_metadata_hash,
    )
    test_log_path = Path(__file__).with_name("TEST_LOG.txt")
    test_path = Path(__file__).with_name("test_csm.py")
    output_dir = Path(args.output_dir)
    if not output_dir.parent.is_dir():
        raise GateError("durable output parent directory must already exist")
    if output_dir.exists() or output_dir.is_symlink():
        raise GateError("output destination already exists; preserve the attempt")
    calendar_path = Path(args.expected_calendar)
    calendar_bytes = calendar_path.read_bytes()
    try:
        calendar_doc = json.loads(calendar_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateError("calendar artifact is not valid UTF-8 JSON") from exc
    if not isinstance(calendar_doc, dict):
        raise GateError("calendar artifact is not a JSON object")
    month_end_dates = validate_calendar_document(
        calendar_doc,
        source_lock=source_lock,
        raw_bytes=calendar_bytes,
    )
    raw_bytes = Path(args.source_csv).read_bytes()
    capture = _read_json(Path(args.capture_manifest))
    validate_capture_manifest(
        capture, raw_bytes, source_lock,
        source_lock_raw_bytes=source_lock_raw,
        expected_metadata_sha256=probe_metadata_hash if is_packet_c_source_lock(source_lock) else None,
    )
    calendar_hash = sha256_bytes(calendar_bytes)
    if gate["expected_calendar_sha256"] != calendar_hash:
        raise GateError("gate calendar identity mismatch")
    if capture["access_ledger_id"] != gate["access_ledger_id"]:
        raise GateError("capture and gate access-ledger identity mismatch")

    stage_dir = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.stage-", dir=output_dir.parent))
    raw_hash = sha256_bytes(raw_bytes)
    source_lock_hash = sha256_bytes(canonical_json_bytes(source_lock))
    source_lock_raw_hash = sha256_bytes(source_lock_raw)
    start_receipt = {
        "run_id": gate["run_id"],
        "data_role": gate["data_role"],
        "execution_status": "IN_PROGRESS",
        "evidence_validity": "PENDING",
        "scientific_status": "NOT_APPLICABLE",
        "access_ledger_id": gate["access_ledger_id"],
        "market_outcome_access_before_gate": False,
        "raw_snapshot_sha256": raw_hash,
        "source_lock_sha256": source_lock_hash,
        "source_lock_raw_sha256": source_lock_raw_hash,
        "probe_metadata_sha256": probe_metadata_hash,
        "calendar_sha256": calendar_hash,
        "d_file_sha256": expected_file_hashes,
        "environment_identity_sha256": environment_identity_sha256(),
    }
    _write_json_exclusive(stage_dir / "attempt-start.json", start_receipt)

    stage = "SOURCE_PARSE"
    ledger_hash: str | None = None
    primary_hash: str | None = None
    try:
        # This hook blocks some accidental calls in this Python process only.
        # It is not an OS sandbox and does not isolate files or other processes.
        sys.addaudithook(_block_network_audit)
        table = parse_source_csv(raw_bytes, source_lock, source_metadata=probe_metadata)
        validate_observed_date_bounds(table)
        target_months = month_range(TARGET_START, TARGET_END)
        events = build_signal_events(target_months, month_end_dates, table)

        stage = "EVENT_LEDGER"
        ledger_path = stage_dir / "event-ledger.json"
        ledger_hash = persist_event_ledger(events, ledger_path)

        # Outcome computation begins only after the event ledger bytes are durable.
        stage = "OUTCOME_CALCULATION"
        outcomes = calculate_outcomes_after_ledger(
            events, table, ledger_path=ledger_path, expected_ledger_sha256=ledger_hash
        )
        metrics = summarize_metrics(outcomes, events)
        primary_payload = {
            "spec_id": SPEC_ID,
            "data_role": "EXPLORATORY_DISCOVERY",
            "inference_status": "PENDING",
            "metrics": asdict(metrics),
            "outcome_grid_log_returns": [str(v) if v is not None else None for v in outcomes],
            "cost_boundary": "UNOBSERVED",
            "temporal_claim": "REFERENCE_ASSOCIATION_ONLY",
            "available_at": "UNKNOWN",
        }
        primary_hash = _write_json_exclusive(stage_dir / "primary-metrics.json", primary_payload)

        stage = "BOOTSTRAP"
        bootstrap = moving_block_bootstrap(outcomes)
        scientific_status, decision = classify_result(
            mean_bps=metrics.mean_bps or Decimal(0),
            lower_95_bps=bootstrap.lower_95 * Decimal(10_000),
            eligible_count=metrics.eligible_count,
            scheduled_count=metrics.scheduled_count,
        )
        inference_hash = _write_json_exclusive(stage_dir / "inference.json", {
            "spec_id": SPEC_ID,
            "scientific_status": scientific_status,
            "decision": decision,
            "bootstrap": asdict(bootstrap),
        })
        runtime = {
            **environment_snapshot(),
            "environment_identity_sha256": environment_identity_sha256(),
            "test_code_sha256": sha256_file(test_path),
            "test_log_sha256": sha256_file(test_log_path),
            "source_lock_sha256": source_lock_hash,
            "source_lock_raw_sha256": source_lock_raw_hash,
            "probe_metadata_sha256": probe_metadata_hash,
            "calendar_sha256": calendar_hash,
            "raw_snapshot_sha256": raw_hash,
            "event_ledger_sha256": ledger_hash,
            "primary_metrics_sha256": primary_hash,
            "inference_sha256": inference_hash,
            "network_access": "NO_NETWORK_CLIENT; PROCESS_AUDIT_HOOK_ONLY_NOT_OS_ISOLATION",
        }
        output_file_hashes = {
            name: sha256_file(stage_dir / name)
            for name in ("attempt-start.json", "event-ledger.json", "primary-metrics.json", "inference.json")
        }
        success_receipt = {
            "run_id": gate["run_id"],
            "data_role": gate["data_role"],
            "execution_status": "SUCCESS",
            "evidence_validity": "VALID",
            "scientific_status": scientific_status,
            "decision": decision,
            "runtime_and_file_snapshot": runtime,
            "output_file_sha256": output_file_hashes,
            "access_ledger_id": gate["access_ledger_id"],
            "market_outcome_access_before_gate": False,
        }
        _write_json_exclusive(stage_dir / "_completion-pending.json", {
            "promotion_status": "READY_TO_PROMOTE",
            "success_receipt": success_receipt,
        })
        promote_output_directory(stage_dir, output_dir)
        print("execution_status=SUCCESS")
        print(f"scientific_status={scientific_status}")
        return 0
    except (GateError, DataError, OSError, ArithmeticError) as exc:
        if stage_dir.exists():
            try:
                _write_json_exclusive(stage_dir / "attempt-status.json", {
                    "run_id": gate["run_id"],
                    "execution_status": "FAILED",
                    "evidence_validity": "PARTIAL",
                    "scientific_status": "NOT_APPLICABLE",
                    "stage": stage,
                    "failure_class": exc.__class__.__name__,
                    "access_ledger_id": gate["access_ledger_id"],
                    "raw_snapshot_sha256": raw_hash,
                    "source_lock_sha256": source_lock_hash,
                    "source_lock_raw_sha256": source_lock_raw_hash,
                    "calendar_sha256": calendar_hash,
                    "event_ledger_sha256": ledger_hash,
                    "primary_metrics_sha256": primary_hash,
                    "output_promoted": False,
                    "do_not_reuse_or_retry_without_new_authorization": True,
                })
            except (GateError, OSError):
                pass
        print(f"execution_status=FAILED stage={stage}", file=sys.stderr)
        print(f"failure_class={exc.__class__.__name__}", file=sys.stderr)
        return 2


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fixed CSM-002 deterministic screen")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="authorized full-history run only")
    run.add_argument("--source-csv", required=True)
    run.add_argument("--source-lock", required=True)
    run.add_argument("--probe-metadata", required=True)
    run.add_argument("--expected-calendar", required=True)
    run.add_argument("--capture-manifest", required=True)
    run.add_argument("--gate-receipt", required=True)
    run.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)
    if args.command == "run":
        try:
            return run_locked_calculation(args)
        except (GateError, DataError, OSError) as exc:
            # Never echo input rows, rates, rankings, or metrics on preflight failure.
            print(f"BLOCKED_OR_INVALID: {exc.__class__.__name__}", file=sys.stderr)
            return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(cli())
