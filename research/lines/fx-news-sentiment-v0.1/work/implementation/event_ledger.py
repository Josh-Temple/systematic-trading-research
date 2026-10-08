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
    retained = dedupe_headlines(raw_records)
    retained_ids = [r["record_id"] for r in retained]
    try:
        parsed = validate_batch(raw_outputs, retained_ids)
        eur, jpy = daily_scores(parsed)
        action = pair_action(eur, jpy)
    except (ValueError, TypeError, KeyError) as exc:
        raise EventBlocked("OUTPUT_PARSE_OR_SCORE_BLOCKED: " + str(exc)) from exc
    hashes = _candidate_hashes()
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


def write_blocked_receipt(*, event_id: str, reason: str, directory: Path):
    """Append-only synthetic failed-preflight receipt; never an issued event."""
    if not re.fullmatch(r"SYNTHETIC-FXNS-[0-9]{8}", event_id):
        raise EventBlocked("INVALID_SYNTHETIC_EVENT_ID")
    _required_text(reason, "BLOCK_REASON")
    receipt = {"event_id": event_id, "record_type": "BLOCKED_SYNTHETIC_PREFLIGHT",
               "formal_cohort_status": COHORT_STATE, "decision": None,
               "is_no_trade": None, "market_outcome": "UNAVAILABLE_NOT_REQUESTED",
               "blocked_reason": reason, "version": SPEC_VERSION}
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
    if event.get("record_type") != "SYNTHETIC_ONLY_NOT_FORMAL" or event.get("formal_cohort_status") != "CLOSED":
        raise EventBlocked("FORMAL_RECORD_WRITE_FORBIDDEN")
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
    if record.get("record_type") not in {"SYNTHETIC_ONLY_NOT_FORMAL", "BLOCKED_SYNTHETIC_PREFLIGHT"}:
        raise EventBlocked("NON_SYNTHETIC_RECORD")
    return record
