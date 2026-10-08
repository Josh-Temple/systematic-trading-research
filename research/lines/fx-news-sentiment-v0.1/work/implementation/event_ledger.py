"""Outcome-blind, synthetic-only prospective event ledger prototype.

There is intentionally NO switch that enables formal issuance or outcome joining.
Source evidence and timestamps in the synthetic path are fixtures, not approvals.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit

from fxns import (canonical_json_bytes, canonical_sha256, daily_scores, dedupe_headlines,
                  event_schedule, pair_action, parse_iso_aware, validate_event_timing,
                  validate_formal_source, validate_model_identity, validate_news_window)
from prompt_contract import validate_batch

SPEC_VERSION = "SPEC-FXNS-001-v01"
COHORT_STATE = "CLOSED"  # No user-supplied flag or environment variable can open it.
MAXRECORDS = 250
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class EventBlocked(ValueError):
    """An attempted event failed closed; no formal event or result exists."""


def issue_formal_event(*_args, **_kwargs):
    raise EventBlocked("FORMAL_COHORT_CLOSED_NO_ISSUANCE")


def associate_market_outcome(*_args, **_kwargs):
    raise EventBlocked("FORMAL_COHORT_CLOSED_NO_OUTCOME_JOIN")


@dataclass(frozen=True)
class SyntheticSourceEvidence:
    # Independently reviewed evidence is an EXTERNAL prerequisite; the synthetic
    # fixture can check its shape but cannot certify reviewer/source authenticity.
    source_status: str
    acquisition_status: str
    independent_review_ref: str
    independent_review_sha256: str
    raw_ref: str
    raw_sha256: str
    metadata_ref: str
    metadata_sha256: str
    query_version: str
    retrieved_at: str


def _required_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise EventBlocked(f"MISSING_{label}")
    return value


def _sha(value, label):
    if not isinstance(value, str) or not SHA256.fullmatch(value):
        raise EventBlocked(f"INVALID_{label}_SHA256")
    return value


def _time(value, label):
    try:
        return parse_iso_aware(_required_text(value, label))
    except (TypeError, ValueError) as exc:
        raise EventBlocked(f"INVALID_{label}_TIME") from exc


def _candidate_hashes():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "PROMPT_MANIFEST_v0.1.json").read_bytes())
    if manifest.get("status") != "FREEZE_READY_CANDIDATE_NOT_HUMAN_FROZEN":
        raise EventBlocked("UNEXPECTED_PROMPT_STATUS")
    hashes = manifest["files"]
    for name in ("PROMPT_v0.1.txt", "OUTPUT_SCHEMA_v0.1.json"):
        expected = _sha(hashes.get(name), name)
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        if actual != expected:
            raise EventBlocked("PROMPT_SCHEMA_HASH_MISMATCH")
    return {"prompt_sha256": hashes["PROMPT_v0.1.txt"],
            "schema_sha256": hashes["OUTPUT_SCHEMA_v0.1.json"]}


def _fixture_source(evidence: SyntheticSourceEvidence, cutoff: datetime):
    if not isinstance(evidence, SyntheticSourceEvidence):
        raise EventBlocked("SOURCE_EVIDENCE_MISSING")
    if evidence.source_status != "PASS" or evidence.acquisition_status != "PASS":
        raise EventBlocked("SOURCE_QUALIFICATION_BLOCKED")
    _required_text(evidence.independent_review_ref, "INDEPENDENT_REVIEW_REF")
    _sha(evidence.independent_review_sha256, "INDEPENDENT_REVIEW")
    _required_text(evidence.query_version, "QUERY_VERSION")
    for label in ("raw", "metadata"):
        ref = _required_text(getattr(evidence, label + "_ref"), label.upper() + "_REF")
        if not ref.startswith("synthetic://"):
            raise EventBlocked("REAL_SOURCE_NOT_ACCEPTED_IN_SYNTHETIC_PATH")
        _sha(getattr(evidence, label + "_sha256"), label.upper())
    obtained = _time(evidence.retrieved_at, "RETRIEVED_AT")
    if obtained > cutoff:
        raise EventBlocked("POST_CUTOFF_ACQUISITION")
    # No count/fixture property can promote an unreviewed external source to PASS.
    return obtained


def build_synthetic_event(*, event_date: date, issued_at: str, raw_records: list[dict],
                          raw_count: int, raw_outputs: list[str],
                          source: SyntheticSourceEvidence, expected_model: str,
                          visible_model: str, expected_config: str, visible_config: str,
                          version: str = SPEC_VERSION, unavailable_dates=()):
    """Pure synthetic review; does NOT issue formal events, score market outcomes or fetch data."""
    if version != SPEC_VERSION:
        raise EventBlocked("VERSION_MISMATCH")
    if not isinstance(event_date, date) or isinstance(event_date, datetime):
        raise EventBlocked("INVALID_EVENT_DATE")
    try:
        cutoff, entry, exit_ = event_schedule(event_date, unavailable_dates)
        issued = _time(issued_at, "ISSUED_AT")
        validate_event_timing(cutoff, issued, entry, exit_)
    except (ValueError, TypeError) as exc:
        raise EventBlocked(str(exc)) from exc
    obtained = _fixture_source(source, cutoff)
    for name, value in (("EXPECTED_MODEL", expected_model), ("VISIBLE_MODEL", visible_model),
                        ("EXPECTED_CONFIG", expected_config), ("VISIBLE_CONFIG", visible_config)):
        _required_text(value, name)
    try:
        validate_model_identity(expected_model, visible_model)
        if expected_config != visible_config:
            raise EventBlocked("MODEL_CONFIG_CHANGED")
    except ValueError as exc:
        raise EventBlocked(str(exc)) from exc
    if not isinstance(raw_records, list) or not isinstance(raw_outputs, list):
        raise EventBlocked("INVALID_INPUT_TYPE")
    if type(raw_count) is not int or raw_count != len(raw_records):
        raise EventBlocked("RAW_COUNT_MISMATCH")
    if raw_count == 0:
        raise EventBlocked("EMPTY_INPUT_SOURCE_UNVERIFIED")
    if raw_count >= MAXRECORDS:
        raise EventBlocked("INPUT_CORPUS_COMPLETENESS_UNVERIFIED")
    # This helper is the last cap check; its flags come from EXPLICIT fixture evidence.
    try:
        validate_formal_source({"article_count": raw_count,
                                "completeness": "UNVERIFIED_EVEN_BELOW_CAP"},
                               source_qualified=source.source_status == "PASS",
                               acquisition_proven=source.acquisition_status == "PASS")
    except ValueError as exc:
        raise EventBlocked(str(exc)) from exc
    raw_ids = []
    for record in raw_records:
        if not isinstance(record, dict):
            raise EventBlocked("INVALID_HEADLINE_RECORD")
        if not str(record.get("title", "")).startswith("SYNTHETIC:"):
            raise EventBlocked("REAL_HEADLINE_NOT_ACCEPTED_IN_SYNTHETIC_PATH")
        try:
            host = urlsplit(str(record.get("url", ""))).hostname
        except ValueError as exc:
            raise EventBlocked("INVALID_SYNTHETIC_URL") from exc
        if not host or not host.endswith(".invalid"):
            raise EventBlocked("REAL_URL_NOT_ACCEPTED_IN_SYNTHETIC_PATH")
        try:
            validate_news_window(record, cutoff)
            if _time(record["gdelt_seen_at"], "GDELT_SEEN_AT") > obtained:
                raise EventBlocked("NEWS_AFTER_PIPELINE_RETRIEVAL")
        except ValueError as exc:
            raise EventBlocked(str(exc)) from exc
        raw_ids.append(record["record_id"])
    if len(raw_ids) != len(set(raw_ids)):
        raise EventBlocked("DUPLICATE_RAW_RECORD_ID")
    hashes = _candidate_hashes()
    retained = dedupe_headlines(raw_records)
    retained_ids = [r["record_id"] for r in retained]
    try:
        parsed = validate_batch(raw_outputs, retained_ids)
        eur, jpy = daily_scores(parsed)
        action = pair_action(eur, jpy)
    except (ValueError, TypeError, KeyError) as exc:
        raise EventBlocked("OUTPUT_PARSE_OR_SCORE_BLOCKED: " + str(exc)) from exc
    event_id = "SYNTHETIC-FXNS-" + event_date.strftime("%Y%m%d")
    return {
        "event_id": event_id, "version": version,
        "formal_cohort_status": COHORT_STATE, "record_type": "SYNTHETIC_ONLY_NOT_FORMAL",
        "frozen_at": issued.isoformat(), "information_cutoff": cutoff.isoformat(),
        "entry_target": entry.isoformat(), "exit_target": exit_.isoformat(),
        "source": {**source.__dict__, "raw_count": raw_count,
                   "retained_count": len(retained), "synthetic_fixture_only": True},
        "prompt_and_schema": hashes,
        "model": {"expected_visible_identity": expected_model, "observed_visible_identity": visible_model,
                  "expected_config": expected_config, "observed_config": visible_config},
        "input_record_ids": retained_ids,
        "input_snapshot_sha256": canonical_sha256({"records": retained, "retrieved_at": source.retrieved_at}),
        "classification_raw": list(raw_outputs), "classification_parsed": parsed,
        "decision": action.value, "is_no_trade": action.value == "NO_TRADE",
        "synthetic_scores": {"EUR": eur, "JPY": jpy},
        "market_outcome": "UNAVAILABLE_NOT_REQUESTED", "blocked_reason": None,
    }



_SYNTHETIC_EVENT_KEYS = frozenset({
    "event_id", "version", "formal_cohort_status", "record_type",
    "frozen_at", "information_cutoff", "entry_target", "exit_target",
    "source", "prompt_and_schema", "model", "input_record_ids",
    "input_snapshot_sha256", "classification_raw", "classification_parsed",
    "decision", "is_no_trade", "synthetic_scores", "market_outcome",
    "blocked_reason",
})
_BLOCKED_RECEIPT_KEYS = frozenset({
    "event_id", "record_type", "formal_cohort_status", "decision",
    "is_no_trade", "market_outcome", "blocked_reason", "version",
})
_SYNTHETIC_SOURCE_KEYS = frozenset({
    "source_status", "acquisition_status", "independent_review_ref",
    "independent_review_sha256", "raw_ref", "raw_sha256", "metadata_ref",
    "metadata_sha256", "query_version", "retrieved_at", "raw_count",
    "retained_count", "synthetic_fixture_only",
})
_SYNTHETIC_MODEL_KEYS = frozenset({
    "expected_visible_identity", "observed_visible_identity",
    "expected_config", "observed_config",
})


def _validate_synthetic_record(record: dict, *, allow_blocked: bool = False):
    """Check *untrusted* writer/verifier input; a record hash alone is not provenance.

    The guard is deliberately synthetic-only. It neither verifies a real source
    nor provides an authorization path to formal issuance or outcome joining.
    """
    if not isinstance(record, dict):
        raise EventBlocked("INVALID_SYNTHETIC_RECORD")
    if record.get("version") != SPEC_VERSION or record.get("formal_cohort_status") != COHORT_STATE:
        raise EventBlocked("SYNTHETIC_VERSION_OR_COHORT_MISMATCH")
    event_id = record.get("event_id")
    if not isinstance(event_id, str) or not re.fullmatch(r"SYNTHETIC-FXNS-[0-9]{8}", event_id):
        raise EventBlocked("INVALID_SYNTHETIC_EVENT_ID")
    if record.get("market_outcome") != "UNAVAILABLE_NOT_REQUESTED":
        raise EventBlocked("SYNTHETIC_MARKET_OUTCOME_FORBIDDEN")

    if record.get("record_type") == "BLOCKED_SYNTHETIC_PREFLIGHT":
        if not allow_blocked or set(record) != _BLOCKED_RECEIPT_KEYS:
            raise EventBlocked("INVALID_BLOCKED_SYNTHETIC_RECEIPT")
        if record.get("decision") is not None or record.get("is_no_trade") is not None:
            raise EventBlocked("BLOCKED_RECEIPT_CANNOT_BE_A_DECISION")
        _required_text(record.get("blocked_reason"), "BLOCK_REASON")
        return

    if record.get("record_type") != "SYNTHETIC_ONLY_NOT_FORMAL" or set(record) != _SYNTHETIC_EVENT_KEYS:
        raise EventBlocked("INVALID_SYNTHETIC_EVENT_SHAPE")
    if record.get("blocked_reason") is not None:
        raise EventBlocked("SYNTHETIC_EVENT_MUST_NOT_BE_BLOCKED")

    source = record.get("source")
    if not isinstance(source, dict) or set(source) != _SYNTHETIC_SOURCE_KEYS:
        raise EventBlocked("INVALID_SYNTHETIC_SOURCE_SHAPE")
    if source.get("synthetic_fixture_only") is not True:
        raise EventBlocked("REAL_SOURCE_NOT_ACCEPTED_IN_SYNTHETIC_PATH")
    if source.get("source_status") != "PASS" or source.get("acquisition_status") != "PASS":
        raise EventBlocked("SOURCE_QUALIFICATION_BLOCKED")
    for name in ("raw", "metadata", "independent_review"):
        ref = _required_text(source.get(name + "_ref"), name.upper() + "_REF")
        if not ref.startswith("synthetic://"):
            raise EventBlocked("REAL_SOURCE_NOT_ACCEPTED_IN_SYNTHETIC_PATH")
        _sha(source.get(name + "_sha256"), name.upper())
    if not str(source.get("query_version", "")).startswith("synthetic-"):
        raise EventBlocked("NON_SYNTHETIC_QUERY_VERSION")
    if (type(source.get("raw_count")) is not int
            or not 0 < source["raw_count"] < MAXRECORDS
            or type(source.get("retained_count")) is not int
            or not 0 < source["retained_count"] <= source["raw_count"]):
        raise EventBlocked("INVALID_SYNTHETIC_RECORD_COUNTS")

    model = record.get("model")
    if not isinstance(model, dict) or set(model) != _SYNTHETIC_MODEL_KEYS:
        raise EventBlocked("INVALID_SYNTHETIC_MODEL")
    for name in _SYNTHETIC_MODEL_KEYS:
        if not str(model.get(name, "")).startswith("synthetic-"):
            raise EventBlocked("REAL_MODEL_IDENTITY_NOT_ACCEPTED_IN_SYNTHETIC_PATH")
    if (model["expected_visible_identity"] != model["observed_visible_identity"]
            or model["expected_config"] != model["observed_config"]):
        raise EventBlocked("MODEL_IDENTITY_OR_CONFIG_CHANGED")

    if record.get("prompt_and_schema") != _candidate_hashes():
        raise EventBlocked("PROMPT_SCHEMA_HASH_MISMATCH")
    ids = record.get("input_record_ids")
    if (not isinstance(ids, list) or len(ids) != source["retained_count"]
            or not all(isinstance(r, str) and r.startswith("synthetic-") for r in ids)
            or len(set(ids)) != len(ids)):
        raise EventBlocked("INVALID_SYNTHETIC_INPUT_IDENTITIES")
    _sha(record.get("input_snapshot_sha256"), "INPUT_SNAPSHOT")
    if (not isinstance(record.get("classification_raw"), list)
            or len(record["classification_raw"]) != len(ids)
            or not all(isinstance(item, str) for item in record["classification_raw"])):
        raise EventBlocked("INVALID_SYNTHETIC_CLASSIFICATION_RAW")
    parsed = record.get("classification_parsed")
    if (not isinstance(parsed, list) or len(parsed) != len(ids)
            or any(not isinstance(row, dict) for row in parsed)
            or [row.get("record_id") for row in parsed] != ids):
        raise EventBlocked("INVALID_SYNTHETIC_CLASSIFICATION_PARSED")
    if not isinstance(record.get("synthetic_scores"), dict) or set(record["synthetic_scores"]) != {"EUR", "JPY"}:
        raise EventBlocked("INVALID_SYNTHETIC_SCORES")
    if record.get("decision") not in ("LONG_EURJPY", "SHORT_EURJPY", "NO_TRADE"):
        raise EventBlocked("INVALID_SYNTHETIC_DECISION")
    if type(record.get("is_no_trade")) is not bool or record["is_no_trade"] != (record["decision"] == "NO_TRADE"):
        raise EventBlocked("INCONSISTENT_NO_TRADE")
    cutoff = _time(record.get("information_cutoff"), "INFORMATION_CUTOFF")
    frozen_at = _time(record.get("frozen_at"), "FROZEN_AT")
    entry = _time(record.get("entry_target"), "ENTRY_TARGET")
    exit_ = _time(record.get("exit_target"), "EXIT_TARGET")
    retrieved_at = _time(source.get("retrieved_at"), "RETRIEVED_AT")
    if not (retrieved_at <= cutoff <= frozen_at < entry < exit_):
        raise EventBlocked("INVALID_SYNTHETIC_EVENT_TIMELINE")
    if cutoff.date().strftime("%Y%m%d") != event_id.rsplit("-", 1)[-1]:
        raise EventBlocked("SYNTHETIC_EVENT_DATE_MISMATCH")

def write_blocked_receipt(*, event_id: str, reason: str, directory: Path):
    """Append-only synthetic failed-preflight receipt; never an issued event."""
    if not re.fullmatch(r"SYNTHETIC-FXNS-[0-9]{8}", event_id):
        raise EventBlocked("INVALID_SYNTHETIC_EVENT_ID")
    _required_text(reason, "BLOCK_REASON")
    receipt = {"event_id": event_id, "record_type": "BLOCKED_SYNTHETIC_PREFLIGHT",
               "formal_cohort_status": COHORT_STATE, "decision": None,
               "is_no_trade": None, "market_outcome": "UNAVAILABLE_NOT_REQUESTED",
               "blocked_reason": reason, "version": SPEC_VERSION}
    _validate_synthetic_record(receipt, allow_blocked=True)
    target_dir = Path(directory)
    target_dir.mkdir(parents=True, exist_ok=True)
    file = target_dir / (event_id + ".blocked.json")
    with file.open("xb") as handle:
        handle.write(canonical_json_bytes({"record": receipt,
                                           "record_sha256": canonical_sha256(receipt)}) + b"\n")
        handle.flush()
        os.fsync(handle.fileno())
    return file


def write_synthetic_event(event: dict, directory: Path):
    """Append one immutable event file by exclusive create, then verify byte/hash readback."""
    _validate_synthetic_record(event)
    event_id = event.get("event_id")
    if not isinstance(event_id, str) or not re.fullmatch(r"SYNTHETIC-FXNS-[0-9]{8}", event_id):
        raise EventBlocked("INVALID_SYNTHETIC_EVENT_ID")
    target_dir = Path(directory)
    target_dir.mkdir(parents=True, exist_ok=True)
    payload = {"record": event, "record_sha256": canonical_sha256(event)}
    raw = canonical_json_bytes(payload) + b"\n"
    file = target_dir / (event_id + ".json")
    # O_EXCL makes an existing event immutable to this writer, even if NO_TRADE.
    with file.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    if file.read_bytes() != raw:
        raise EventBlocked("LEDGER_READBACK_MISMATCH")
    return file, hashlib.sha256(raw).hexdigest()


def verify_synthetic_event(file: Path):
    raw = Path(file).read_bytes()
    if not raw.endswith(b"\n"):
        raise EventBlocked("LEDGER_INCOMPLETE_RECORD")
    payload = json.loads(raw)
    record = payload["record"]
    if payload.get("record_sha256") != canonical_sha256(record):
        raise EventBlocked("LEDGER_TAMPER_DETECTED")
    _validate_synthetic_record(record, allow_blocked=True)
    return record
