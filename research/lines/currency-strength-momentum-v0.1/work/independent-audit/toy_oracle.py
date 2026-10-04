#!/usr/bin/env python3
"""Independent synthetic audit checks for CSM-002. No market observations are read."""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib
import json
import math
import random
import shutil
import sys
import tempfile
from datetime import datetime
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Mapping

AUDIT_ID = "AUDIT-CSM-E-20261004-REAUDIT-02"
I_HEAD = "6bd9ddc5bc53c37aee3b0d82d1ac2c00c00fd73c"
I_GATE_BLOB = "bfa515df80fb855749d8df1e5ce9d657b8f3f495"
I_GATE_SHA256 = None  # computed from exact supplied bytes
I_GATE_MD_BLOB = "62e8399821d7e8c168672f93c1dbc7155deca4b2"
I_GATE_MD_SHA256 = None  # computed from exact supplied bytes
D_HEAD = "3695f0a8ed085669ec3644826889f9fc953a6808"
OLD_E_ID = "AUDIT-CSM-E-20261002"
NOW = datetime.fromisoformat("2026-10-02T07:00:00+09:00")
FROZEN_SPEC_BLOB = "7fe114e2fcfa33b0565b51c717455abd8837d5d9"
FROZEN_SPEC_SHA256 = "a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2"
EXPECTED_D_SHA256 = {
    "csm.py": "f57c859dd137bb49f23a23ddf2760681bc3ca14aa23cf82e03e2f35bc5b54535",
    "test_csm.py": "899332a9e51018d6140a201105eccdad8154d075af1a32354776621976185bf2",
    "config.json": "9235142b336080ccd87c731d95fe266f64402c202e0de3b7e372521747cccfe1",
    "RUNBOOK.md": "bba147d4da072507ba255cb15a93a9fe0e76fda7df822fe4cfcf626501b91fb7",
    "ENVIRONMENT.md": "8290c920ea74a05ef759281bcba2792f446f7cc53774f319bf9a57ec5e1e7d8f",
    "RESULT.md": "3c48c47f87634346ac4c02ff1c73a32f640b50d429f2e303d5668bb7c2eff0ea",
    "TEST_MATRIX.md": "d5dfa2c76dcaf2c803755d0a03aac803550ce793ad84c7d35257ec899971e0ca",
    "TEST_LOG.txt": "8b6f5f9c2c6527c9c1b6535ba5fdbdcd6394b2259ce947949a52720734cf3b3b",
    "fixtures/toy_cases.json": "08e0cb95402f5110bcfac494e590cb2d57fd033dde2e5d79a038454526c39f6c",
}

# Deliberately synthetic test key copied from D's public test fixture, never production trust.
TEST_RSA_N = int(
    "f12c454cafaa2a3cc5d755f9db98ca193944475b5ed676efb0facd2a0ebcce35272e6721d8ac76a15a136b01e41fd481b3926cdc95f48f27680cd57a2fe9ae13f0bc79d31d616b1cbb5b028c86f69aecf93ad84efc426ff3b77245d9e38ed6868069f84adddb175a1eddb99983da0a8ba8975d047e8fb50390f6a09c723bd84b855d65995738c247bddc199af39ae49324305be07cc587ba074bbe6f72af3cb516734036a8e20998589cb37256cc32ccd5275d0a3dedb3ef320d334ae9dd8e6d78391021f0f58288a74a625c32e66f4023710a378c068ddcd1bd59976ef2722bb662cd4a4241ac21a47f134568a5157eeee81d4b3ccbf39e8a4ded3def126833", 16)
TEST_RSA_D = int(
    "4bf6a04b53c75aef72776d96ba22e9814166eebcea65cde7988c9ec3c1099a3fe6bbf873123edc4cdd44e17f227e1e1ece53702398be03bb2b4c638f4d7922c218211d94301c67b310964d7abae6010d64413331c9c61962202587b7e633af0185801b5b657ee55f96fa4ac3fe6256d0ff84d1a121461d83668d3030a6d08fc3394dc7a94ed00c9bfaecd94c8ce147c3c154d534b7163f36b2ca8f929ff20ca69ace7d6197c527a4cb5fc773ae19668945df5a1436cea37b561c560566d360737f660c73921e06c46a5bfed26936be53dc751dbfe2a911f88eeb1bc1847754e759899e84280df1cfa055a555e60c20dab7d60dd25b662790b50443f017946a7d", 16)
TEST_KEYS: dict[str, dict[str, Any]] = {
    "integrator-test-key-001": {
        "role": "integrator", "principal_id": "integrator-principal-001",
        "n_hex": format(TEST_RSA_N, "x"), "e": 65537, "revoked": False,
        "valid_from": "2026-01-01T00:00:00Z", "valid_until": "2027-01-01T00:00:00Z",
    },
    "auditor-test-key-001": {
        "role": "independent_auditor", "principal_id": "auditor-principal-001",
        "n_hex": format(TEST_RSA_N, "x"), "e": 65537, "revoked": False,
        "valid_from": "2026-01-01T00:00:00Z", "valid_until": "2027-01-01T00:00:00Z",
    },
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


def rejects(call: Callable[[], Any], phrase: str) -> None:
    try:
        call()
    except Exception as exc:
        if phrase not in str(exc):
            raise AssertionError(f"expected {phrase!r}, got {type(exc).__name__}: {exc}") from exc
    else:
        raise AssertionError(f"expected rejection containing {phrase!r}")


def sign_envelope(csm: Any, payload: Mapping[str, Any], key_id: str,
                  issued_at: str = "2026-10-02T06:00:00+09:00",
                  expires_at: str = "2026-10-02T18:00:00+09:00") -> dict[str, Any]:
    signature_doc = {
        "key_id": key_id,
        "algorithm": "RSASSA-PKCS1-v1_5-SHA256",
        "issued_at": issued_at,
        "expires_at": expires_at,
    }
    message = csm.canonical_json_bytes({"payload": payload, **signature_doc})
    digest_info = csm.RSA_SHA256_DIGEST_INFO_PREFIX + hashlib.sha256(message).digest()
    size = (TEST_RSA_N.bit_length() + 7) // 8
    padding_len = size - len(digest_info) - 3
    encoded = b"\x00\x01" + b"\xff" * padding_len + b"\x00" + digest_info
    signature = pow(int.from_bytes(encoded, "big"), TEST_RSA_D, TEST_RSA_N).to_bytes(size, "big")
    return {"payload": dict(payload), "signature": {
        **signature_doc, "signature_b64": base64.b64encode(signature).decode("ascii")
    }}


def synthetic_lock(csm: Any) -> dict[str, Any]:
    non_eur = [x for x in csm.CURRENCIES if x != "EUR"]
    return {
        "id": "SYNTHETIC-LOCK-ONLY",
        "spec_id": csm.SPEC_ID,
        "source_transport": "SYNTHETIC_FIXTURE_ONLY",
        "series_by_currency": dict(csm.EXPECTED_SERIES_BY_CURRENCY),
        "csv_field_map": {"date": "TIME_PERIOD", "series": "SERIES_KEY", "value": "OBS_VALUE",
                          "unit": "UNIT", "status": "OBS_STATUS"},
        "unit_by_currency": {x: "units_per_EUR" for x in non_eur},
        "status_policy": {"valid": ["A"], "missing": ["M"]},
        "fixture_status": "SYNTHETIC",
    }


def test_math_and_outcome_blindness(csm: Any) -> None:
    currencies = tuple(csm.CURRENCIES)
    old = {c: Decimal("1") for c in currencies}
    new = {c: Decimal(v) for c, v in {
        "AUD": "1.20", "CAD": "0.94", "CHF": "1.08", "EUR": "1.00",
        "GBP": "0.91", "JPY": "1.31", "NZD": "0.87", "USD": "0.98",
    }.items()}
    ratios = {c: Fraction(old[c]) / Fraction(new[c]) for c in currencies}
    a = max(currencies, key=ratios.__getitem__)
    b = min(currencies, key=ratios.__getitem__)
    selected = csm.select_extrema(old, new)
    check((selected.winner, selected.loser) == (a, b), "extrema differ from independent exact-ratio oracle")
    all_pairs = {(x, y): ratios[x] / ratios[y] for x in currencies for y in currencies if x != y}
    high = max(all_pairs.values())
    max_pairs = tuple(pair for pair, value in all_pairs.items() if value == high)
    check(len(all_pairs) == 56 and max_pairs == ((a, b),), "all-56 directed-pair identity failed")

    old_cross = {c: Fraction(old[c]) / Fraction(old["CAD"]) for c in currencies}
    new_cross = {c: Fraction(new[c]) / Fraction(new["CAD"]) for c in currencies}
    transformed = {c: old_cross[c] / new_cross[c] for c in currencies}
    check((max(currencies, key=transformed.__getitem__), min(currencies, key=transformed.__getitem__)) == (a, b),
          "common-numeraire change altered the selected pair")
    check(csm.select_extrema(old_cross, new_cross).winner == a and csm.select_extrema(old_cross, new_cross).loser == b,
          "D implementation differs under synthetic numeraire change")

    # Pair price is q_b/q_a; return is log(new pair / old pair), not a simple-return difference.
    old_pair = Fraction(old[b]) / Fraction(old[a])
    new_pair = Fraction(new[b]) / Fraction(new[a])
    exact_pair_ratio = new_pair / old_pair
    with localcontext() as ctx:
        ctx.prec = 50
        independent_log = (Decimal(exact_pair_ratio.numerator) / Decimal(exact_pair_ratio.denominator)).ln()
    d_log = csm.pair_log_return(a, b, old, new)
    check(abs(independent_log - d_log) < Decimal("1e-45"), "pair quote orientation/log return mismatch")
    check(abs(independent_log - (Decimal(exact_pair_ratio.numerator) / Decimal(exact_pair_ratio.denominator) - 1)) > Decimal("1e-6"),
          "toy case failed to distinguish log from simple return")

    tied = dict(new)
    tied["AUD"] = Decimal("0.8")
    tied["GBP"] = Decimal("0.8")
    check(csm.select_extrema(old, tied).status == "TIED_EXTREME", "exact tie was not retained")
    eur_winner = {c: Decimal("1.1") + Decimal(i) / Decimal(100) for i, c in enumerate(currencies)}
    eur_winner["EUR"] = Decimal("1")
    eur_loser = {c: Decimal("0.7") + Decimal(i) / Decimal(100) for i, c in enumerate(currencies)}
    eur_loser["EUR"] = Decimal("1")
    check(csm.select_extrema(old, eur_winner).winner == "EUR", "EUR winner case failed")
    check(csm.select_extrema(old, eur_loser).loser == "EUR", "EUR loser case failed")
    usd_winner = {c: Decimal("0.8") + Decimal(i) / Decimal(100) for i, c in enumerate(currencies)}
    usd_winner["USD"] = Decimal("0.5")
    usd_loser = {c: Decimal("0.8") + Decimal(i) / Decimal(100) for i, c in enumerate(currencies)}
    usd_loser["USD"] = Decimal("2")
    check(csm.select_extrema(old, usd_winner).winner == "USD", "USD winner case failed")
    check(csm.select_extrema(old, usd_loser).loser == "USD", "USD loser case failed")

    # The uniform mean over all directed pairs is zero by exact antisymmetry.
    with localcontext() as ctx:
        ctx.prec = 50
        score = {c: (Decimal(new[c].numerator) / Decimal(new[c].denominator)).ln()
                 if isinstance(new[c], Fraction) else new[c].ln() for c in currencies}
        cancellations = [(score[y] - score[x]) + (score[x] - score[y])
                         for i, x in enumerate(currencies) for y in currencies[i + 1:]]
    check(len(cancellations) == 28 and all(value == 0 for value in cancellations),
          "uniform 56-direction log-return baseline is not zero")


def test_ledger_target_invariance(csm: Any) -> None:
    calendar = {
        "2019-11": "2019-11-29", "2019-12": "2019-12-31", "2020-01": "2020-01-31",
        "2020-02": "2020-02-28", "2020-03": "2020-03-31",
    }
    values: dict[Any, dict[str, Decimal]] = {}
    for index, month in enumerate(sorted(calendar)):
        day = csm.parse_iso_date(calendar[month])
        values[day] = {currency: Decimal("1") + Decimal(index + 1) * Decimal(pos + 2) / Decimal(1000)
                       for pos, currency in enumerate(csm.CURRENCIES)}
        values[day]["EUR"] = Decimal("1")
    dates = frozenset(values)
    table = csm.QuoteTable(values, {}, dates)
    events = csm.build_signal_events(("2020-01",), calendar, table)
    baseline = csm.canonical_json_bytes(csm.event_ledger_payload(events))
    row = csm.event_ledger_payload(events)["events"][0]
    check(set(row["score_identities"]) == set(csm.CURRENCIES), "ledger lacks all currency score identities")
    target_day = csm.parse_iso_date(calendar["2020-01"])
    changed_values = {day: dict(prices) for day, prices in values.items()}
    changed_values[target_day]["AUD"] = Decimal("9000")
    changed_values[target_day]["USD"] = Decimal("0.0001")
    changed_table = csm.QuoteTable(changed_values, {}, dates)
    changed_events = csm.build_signal_events(("2020-01",), calendar, changed_table)
    check(csm.canonical_json_bytes(csm.event_ledger_payload(changed_events)) == baseline,
          "target value changed pre-outcome ledger bytes")
    missing_values = {day: prices for day, prices in values.items() if day != target_day}
    missing_table = csm.QuoteTable(missing_values, {}, frozenset(missing_values))
    missing_events = csm.build_signal_events(("2020-01",), calendar, missing_table)
    check(csm.canonical_json_bytes(csm.event_ledger_payload(missing_events)) == baseline,
          "target availability changed pre-outcome ledger bytes")
    with tempfile.TemporaryDirectory() as td:
        absent = Path(td) / "not-yet-persisted.json"
        rejects(lambda: csm.calculate_outcomes_after_ledger(events, table, ledger_path=absent,
                                                            expected_ledger_sha256="0" * 64),
                "persisted before outcome")


def test_signature_controls(csm: Any) -> None:
    valid = sign_envelope(csm, {"signer_principal_id": "integrator-principal-001"},
                          "integrator-test-key-001")
    got = csm._verify_signed_envelope(valid, TEST_KEYS, required_role="integrator", now=NOW)
    check(got["signer_principal_id"] == "integrator-principal-001", "valid signed envelope rejected")
    rejects(lambda: csm._verify_signed_envelope(valid, TEST_KEYS, required_role="independent_auditor", now=NOW),
            "role is not trusted")
    wrong_principal = sign_envelope(csm, {"signer_principal_id": "attacker-principal-001"},
                                    "integrator-test-key-001")
    rejects(lambda: csm._verify_signed_envelope(wrong_principal, TEST_KEYS, required_role="integrator", now=NOW),
            "principal does not match")
    expired = sign_envelope(csm, {"signer_principal_id": "integrator-principal-001"},
                            "integrator-test-key-001", expires_at="2026-10-02T06:30:00+09:00")
    rejects(lambda: csm._verify_signed_envelope(expired, TEST_KEYS, required_role="integrator", now=NOW),
            "expired")
    unknown = json.loads(json.dumps(valid))
    unknown["signature"]["key_id"] = "unknown-key-001"
    rejects(lambda: csm._verify_signed_envelope(unknown, TEST_KEYS, required_role="integrator", now=NOW),
            "not in the trusted key store")
    revoked = dict(TEST_KEYS)
    revoked["integrator-test-key-001"] = {**TEST_KEYS["integrator-test-key-001"], "revoked": True}
    rejects(lambda: csm._verify_signed_envelope(valid, revoked, required_role="integrator", now=NOW),
            "role is not trusted")


def actual_i_identity(gate: Mapping[str, Any], gate_raw: bytes, gate_md_raw: bytes) -> dict[str, Any]:
    return {
        "pr_number": 37,
        "head_sha": I_HEAD,
        "gate_blob_sha1": I_GATE_BLOB,
        "gate_sha256": hashlib.sha256(gate_raw).hexdigest(),
        "gate_markdown_blob_sha1": I_GATE_MD_BLOB,
        "gate_markdown_sha256": hashlib.sha256(gate_md_raw).hexdigest(),
        "gate_status": gate["gate_status"],
        "market_outcome_access": gate["market_outcome_access"],
    }


def synthetic_e_identity() -> dict[str, Any]:
    return {
        "audit_id": "AUDIT-CSM-E-SYNTH-DYNAMIC-001",
        "pr_number": 38,
        "head_sha": "e" * 40,
        "result_blob_sha1": "5" * 40,
        "result_sha256": "6" * 64,
        "matrix_blob_sha1": "7" * 40,
        "matrix_sha256": "8" * 64,
        "status": "PASS",
        "recommendation": "ALLOW_I2",
    }


def valid_gate_payload(
    csm: Any,
    lock: Mapping[str, Any],
    raw_lock: bytes,
    current_i: Mapping[str, Any],
    file_hashes: Mapping[str, str],
    *,
    audit_identity: Mapping[str, Any] | None = None,
    environment_sha256: str = "c" * 64,
    calendar_sha256: str = "a" * 64,
) -> dict[str, Any]:
    audit_identity = dict(audit_identity or synthetic_e_identity())
    audit_payload = {
        **audit_identity,
        "signer_principal_id": "auditor-principal-001",
        "audited_d_file_hashes": dict(file_hashes),
        "audited_environment_identity_sha256": environment_sha256,
        "audited_spec_sha256": csm.SPEC_SHA256,
        "audited_source_lock_raw_sha256": csm.sha256_bytes(raw_lock),
        "audited_calendar_sha256": calendar_sha256,
    }
    audit_envelope = sign_envelope(csm, audit_payload, "auditor-test-key-001")
    return {
        "gate_id": "I2-CSM-002-TEST-001",
        "integrator_principal_id": "integrator-principal-001",
        "signer_principal_id": "integrator-principal-001",
        "gate_status": "PASS",
        "human_freeze_status": "FROZEN",
        "market_outcome_access_authorized": True,
        "data_role": "EXPLORATORY_DISCOVERY",
        "spec_id": csm.SPEC_ID,
        "spec_git_blob_sha1": csm.SPEC_GIT_BLOB_SHA1,
        "spec_sha256": csm.SPEC_SHA256,
        "hypothesis_id": csm.HYPOTHESIS_ID,
        "human_contract_decision_id": csm.HUMAN_DECISION_ID,
        "source_lock_id": csm.source_lock_id(lock),
        "source_transport": csm.source_transport(lock),
        "source_lock_sha256": csm.sha256_bytes(csm.canonical_json_bytes(lock)),
        "source_lock_raw_sha256": csm.sha256_bytes(raw_lock),
        "unit_status_map_sha256": csm.sha256_bytes(
            csm.canonical_json_bytes(csm.source_unit_status_map(lock))
        ),
        "expected_calendar_sha256": calendar_sha256,
        "source_series_keys": list(csm.EXPECTED_SERIES_BY_CURRENCY.values()),
        "time_range": {
            "source_start": csm.SOURCE_START,
            "source_end": csm.SOURCE_END,
            "target_start": csm.TARGET_START,
            "target_end": csm.TARGET_END,
        },
        "raw_capture_process_id": "capture-process-0001",
        "access_ledger_id": "access-ledger-0001",
        "run_id": "csm-run-0001",
        "outcome_access_operator_id": "operator-account-0001",
        "outcome_access_operator_name": "Jordan Rivera",
        "code_file_hashes": dict(file_hashes),
        "synthetic_test_log_sha256": file_hashes["TEST_LOG.txt"],
        "environment_identity_sha256": environment_sha256,
        "current_i2_gate_identity": dict(current_i),
        "independent_audit_identity": audit_identity,
        "independent_audit_attestation": audit_envelope,
        "independent_audit_envelope_sha256": csm.sha256_bytes(
            csm.canonical_json_bytes(audit_envelope)
        ),
        "full_history_run_authorized": True,
    }


def validate_synthetic_gate(
    csm: Any,
    payload: Mapping[str, Any],
    lock: Mapping[str, Any],
    raw_lock: bytes,
    file_hashes: Mapping[str, str],
    *,
    expected_error: str | None = None,
) -> None:
    receipt = sign_envelope(csm, payload, "integrator-test-key-001")
    call = lambda: csm.validate_gate_receipt(
        receipt,
        lock,
        source_lock_raw_bytes=raw_lock,
        trusted_keys=TEST_KEYS,
        expected_file_hashes=file_hashes,
        expected_environment_sha256="c" * 64,
        expected_probe_metadata_sha256=None,
        expected_calendar_sha256="a" * 64,
        now=NOW,
        allow_synthetic_test_fixtures=True,
    )
    if expected_error is None:
        accepted = call()
        check(accepted["gate_status"] == "PASS", "valid dynamic signed gate was rejected")
    else:
        rejects(call, expected_error)


def test_raw_lock_and_dynamic_identity(
    csm: Any,
    gate_doc: Mapping[str, Any],
    gate_raw: bytes,
    gate_md_raw: bytes,
) -> None:
    lock = synthetic_lock(csm)
    canonical = csm.canonical_json_bytes(lock)
    file_hashes = dict(EXPECTED_D_SHA256)

    # Semantically equal but byte-different source-lock must still fail raw-byte binding.
    changed_raw = b" \n" + canonical
    pass_i = actual_i_identity(gate_doc, gate_raw, gate_md_raw)
    pass_i["gate_status"] = "PASS"
    pass_i["market_outcome_access"] = True
    payload = valid_gate_payload(csm, lock, canonical, pass_i, file_hashes)
    receipt = sign_envelope(csm, payload, "integrator-test-key-001")
    rejects(lambda: csm.validate_gate_receipt(
        receipt,
        lock,
        source_lock_raw_bytes=changed_raw,
        trusted_keys=TEST_KEYS,
        expected_file_hashes=file_hashes,
        expected_environment_sha256="c" * 64,
        expected_probe_metadata_sha256=None,
        expected_calendar_sha256="a" * 64,
        now=NOW,
        allow_synthetic_test_fixtures=True,
    ), "raw-byte identity mismatch")

    # Exact current I is CLOSED and must not authorize even with valid synthetic signatures.
    current_i = actual_i_identity(gate_doc, gate_raw, gate_md_raw)
    check(current_i["gate_status"] == "CLOSED" and current_i["market_outcome_access"] is False,
          "fresh current I2 gate is not CLOSED")
    current_payload = valid_gate_payload(csm, lock, canonical, current_i, file_hashes)
    validate_synthetic_gate(
        csm, current_payload, lock, canonical, file_hashes,
        expected_error="current I2 gate is not PASS",
    )

    # Non-circularity: rotate immutable I/E identities without changing D code.
    rotated_i = dict(pass_i)
    rotated_i["head_sha"] = "c" * 40
    rotated_i["gate_blob_sha1"] = "d" * 40
    rotated_i["gate_sha256"] = "e" * 64
    rotated_i["gate_markdown_blob_sha1"] = "f" * 40
    rotated_i["gate_markdown_sha256"] = "1" * 64
    rotated_e = synthetic_e_identity()
    rotated_e["audit_id"] = "AUDIT-CSM-E-SYNTH-ROTATED"
    rotated_e["head_sha"] = "2" * 40
    rotated_payload = valid_gate_payload(
        csm, lock, canonical, rotated_i, file_hashes, audit_identity=rotated_e
    )
    validate_synthetic_gate(csm, rotated_payload, lock, canonical, file_hashes)

    # Stale/wrong E evidence against different D bytes must fail closed.
    bad_payload = valid_gate_payload(csm, lock, canonical, rotated_i, file_hashes)
    bad_e = json.loads(json.dumps(bad_payload["independent_audit_attestation"]))
    bad_e_payload = bad_e["payload"]
    bad_e_payload["audited_d_file_hashes"]["csm.py"] = "0" * 64
    bad_e = sign_envelope(csm, bad_e_payload, "auditor-test-key-001")
    bad_payload["independent_audit_attestation"] = bad_e
    bad_payload["independent_audit_envelope_sha256"] = csm.sha256_bytes(
        csm.canonical_json_bytes(bad_e)
    )
    validate_synthetic_gate(
        csm, bad_payload, lock, canonical, file_hashes,
        expected_error="does not bind the current D file hashes",
    )



def stage_success_tree(csm: Any, parent: Path, name: str) -> tuple[Path, Path]:
    stage = parent / f".{name}.stage"
    destination = parent / name
    stage.mkdir()
    names = ("attempt-start.json", "event-ledger.json", "primary-metrics.json", "inference.json")
    hashes = {}
    for index, filename in enumerate(names):
        content = f"synthetic-{index}".encode()
        (stage / filename).write_bytes(content)
        hashes[filename] = csm.sha256_bytes(content)
    pending = {"promotion_status": "READY_TO_PROMOTE", "success_receipt": {
        "execution_status": "SUCCESS", "output_file_sha256": hashes,
    }}
    (stage / "_completion-pending.json").write_bytes(csm.canonical_json_bytes(pending))
    return stage, destination


def test_failure_cleanup(csm: Any) -> list[str]:
    observed_gaps: list[str] = []
    write_points = ("write", "flush", "file_fsync", "promotion", "parent_fsync")
    for point in write_points:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "artifact.json"
            def fail(name: str, target_point: str = point) -> None:
                if name == target_point:
                    raise OSError("synthetic fault")
            rejects(lambda: csm.atomic_write_verified(target, b"synthetic", fault_injector=fail),
                    "artifact staging or promotion failed")
            check(not target.exists(), f"atomic file remains after {point} fault")

    promotion_points = ("rename", "parent_fsync", "success_receipt", "success_write", "success_flush",
                        "success_file_fsync", "success_promotion", "success_parent_fsync")
    for point in promotion_points:
        with tempfile.TemporaryDirectory() as td:
            stage, destination = stage_success_tree(csm, Path(td), "final")
            def fail(name: str, target_point: str = point) -> None:
                if name == target_point:
                    raise OSError("synthetic fault")
            phrase = ("artifact staging or promotion failed"
                      if point in {"success_write", "success_flush", "success_file_fsync",
                                   "success_promotion", "success_parent_fsync"}
                      else "output promotion failed")
            rejects(lambda: csm.promote_output_directory(stage, destination, fault_injector=fail), phrase)
            check(not destination.exists(), f"final output remains after {point} fault")

    # A single final directory-fsync fault rolls back the published directory.
    with tempfile.TemporaryDirectory() as td:
        stage, destination = stage_success_tree(csm, Path(td), "final")
        original_fsync = csm._fsync_directory
        count = {"destination": 0}
        def fail_final(path: Path) -> None:
            if path == destination:
                count["destination"] += 1
                if count["destination"] == 2:
                    raise OSError("synthetic final directory fsync fault")
            original_fsync(path)
        csm._fsync_directory = fail_final
        try:
            rejects(lambda: csm.promote_output_directory(stage, destination), "failed")
            check(not destination.exists(), "single final directory-fsync fault left final output")
        finally:
            csm._fsync_directory = original_fsync

    # If rollback deletion itself fails after the final fsync, cleanup errors are suppressed.
    with tempfile.TemporaryDirectory() as td:
        stage, destination = stage_success_tree(csm, Path(td), "final")
        original_fsync = csm._fsync_directory
        original_rmtree = csm.shutil.rmtree
        count = {"destination": 0}
        def fail_final(path: Path) -> None:
            if path == destination:
                count["destination"] += 1
                if count["destination"] == 2:
                    raise OSError("synthetic final directory fsync fault")
            original_fsync(path)
        def fail_cleanup(path: Any, *args: Any, **kwargs: Any) -> Any:
            if Path(path) == destination:
                raise OSError("synthetic rollback deletion fault")
            return original_rmtree(path, *args, **kwargs)
        csm._fsync_directory = fail_final
        csm.shutil.rmtree = fail_cleanup
        try:
            rejects(lambda: csm.promote_output_directory(stage, destination), "failed")
            check(not (destination / "run-receipt.json").exists(),
                  "compound failure left a SUCCESS receipt after D hardening")
        finally:
            csm._fsync_directory = original_fsync
            csm.shutil.rmtree = original_rmtree
            if destination.exists():
                original_rmtree(destination)
    return observed_gaps


def test_bootstrap(csm: Any) -> None:
    block, reps, seed = 12, 10_000, 20_261_001
    grid = tuple(None if i in (4, 17) else Decimal(i - 17) / Decimal(13) for i in range(36))
    rng = random.Random(seed)
    means: list[Decimal] = []
    with localcontext() as ctx:
        ctx.prec = 50
        nblocks = math.ceil(len(grid) / block)
        for _ in range(reps):
            sample: list[Decimal | None] = []
            for _ in range(nblocks):
                start = rng.randrange(len(grid))
                sample.extend(grid[(start + offset) % len(grid)] for offset in range(block))
            valid = [value for value in sample[:len(grid)] if value is not None]
            check(bool(valid), "independent bootstrap generated an empty replicate")
            means.append(sum(valid, Decimal(0)) / Decimal(len(valid)))
        ordered = sorted(means)
    def p7(probability: Decimal) -> Decimal:
        with localcontext() as ctx:
            ctx.prec = 28
            h = Decimal(len(ordered) - 1) * probability
            low = int(h)
            high = min(low + 1, len(ordered) - 1)
            return ordered[low] + (ordered[high] - ordered[low]) * (h - Decimal(low))
    oracle = (p7(Decimal("0.025")), p7(Decimal("0.975")), p7(Decimal("0.5")))
    result = csm.moving_block_bootstrap(grid)
    check((result.lower_95, result.upper_95, result.median) == oracle,
          "D fixed circular moving-block bootstrap differs from independent implementation")
    check((result.block_length, result.valid_replicates, result.seed) == (block, reps, seed),
          "D bootstrap constants differ from frozen specification")
    check(csm.classify_result(mean_bps=Decimal(0), lower_95_bps=Decimal(-1),
                              eligible_count=120, scheduled_count=150) == ("NOT_SUPPORTED", "DEPRIORITIZE"),
          "frozen nonpositive-mean decision boundary differs")
    check(csm.classify_result(mean_bps=Decimal(1), lower_95_bps=Decimal(0),
                              eligible_count=120, scheduled_count=150) == ("INCONCLUSIVE", "HOLD"),
          "frozen interval boundary differs")


def test_packet_c_metadata(csm: Any, lock_path: Path, probe_path: Path, calendar_path: Path) -> None:
    lock_raw, probe_raw, calendar_raw = lock_path.read_bytes(), probe_path.read_bytes(), calendar_path.read_bytes()
    expected = {
        lock_path: "ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71",
        probe_path: "1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533",
        calendar_path: "6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4",
    }
    for path, digest in expected.items():
        check(hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"metadata bytes mismatch for {path.name}")
    lock = json.loads(lock_raw.decode())
    probe = json.loads(probe_raw.decode())
    calendar = json.loads(calendar_raw.decode())
    csm.validate_packet_c_source_lock(lock)
    csm.validate_packet_c_probe_metadata(lock, probe)
    csm.validate_calendar_document(calendar, source_lock=lock, raw_bytes=calendar_raw)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d-root", type=Path, required=True, help="directory containing the exact D files")
    parser.add_argument("--i-gate-json", type=Path, required=True, help="exact current I gate.json bytes")
    parser.add_argument("--i-gate-md", type=Path, required=True, help="exact current I GATE.md bytes")
    parser.add_argument("--frozen-spec", type=Path, required=True, help="exact frozen SPEC bytes")
    parser.add_argument("--source-lock", type=Path, required=True, help="permitted C metadata only")
    parser.add_argument("--probe-metadata", type=Path, required=True, help="permitted C metadata only")
    parser.add_argument("--expected-calendar", type=Path, required=True, help="permitted C metadata only")
    args = parser.parse_args()
    for relative, expected_hash in EXPECTED_D_SHA256.items():
        raw = (args.d_root / relative).read_bytes()
        check(hashlib.sha256(raw).hexdigest() == expected_hash, f"D artifact identity mismatch: {relative}")
    gate_raw = args.i_gate_json.read_bytes()
    gate_md_raw = args.i_gate_md.read_bytes()
    frozen_spec_raw = args.frozen_spec.read_bytes()
    check(git_blob_sha1(gate_raw) == I_GATE_BLOB, "current I gate.json Git blob mismatch")
    check(git_blob_sha1(gate_md_raw) == I_GATE_MD_BLOB, "current I GATE.md Git blob mismatch")
    current_i_gate_sha256 = hashlib.sha256(gate_raw).hexdigest()
    current_i_gate_md_sha256 = hashlib.sha256(gate_md_raw).hexdigest()
    check(git_blob_sha1(frozen_spec_raw) == FROZEN_SPEC_BLOB
          and hashlib.sha256(frozen_spec_raw).hexdigest() == FROZEN_SPEC_SHA256,
          "frozen SPEC identity mismatch")
    sys.path.insert(0, str(args.d_root.resolve()))
    importlib.invalidate_caches()
    csm = importlib.import_module("csm")
    gate_doc = json.loads(args.i_gate_json.read_bytes().decode())
    checks: list[tuple[str, Callable[[], Any]]] = [
        ("synthetic formula, 56-pair, quote, tie, numeraire, and baseline oracle", lambda: test_math_and_outcome_blindness(csm)),
        ("formation score ledger target-value and availability invariance", lambda: test_ledger_target_invariance(csm)),
        ("trusted key, role, principal, signature, revocation, and expiry checks", lambda: test_signature_controls(csm)),
        ("raw source-lock bytes and dynamic signed I/E binding", lambda: test_raw_lock_and_dynamic_identity(csm, gate_doc, gate_raw, gate_md_raw)),
        ("fault-injected atomic persistence and promotion", lambda: test_failure_cleanup(csm)),
        ("independent fixed circular bootstrap and decision boundaries", lambda: test_bootstrap(csm)),
        ("exact permitted C metadata identity and internal validation", lambda: test_packet_c_metadata(csm, args.source_lock, args.probe_metadata, args.expected_calendar)),
    ]
    gaps: list[str] = []
    for name, fn in checks:
        result = fn()
        if name.startswith("fault-injected"):
            gaps.extend(result)
        print("PASS:", name)
    for gap in gaps:
        print("GAP_REPRODUCED:", gap)
    print("AUDIT_ID:", AUDIT_ID)
    print("BOUND_D_HEAD:", D_HEAD)
    print("BOUND_I_HEAD:", I_HEAD)
    print("CURRENT_I_GATE_STATE:", gate_doc["gate_status"], gate_doc["market_outcome_access"])
    print("CURRENT_I_GATE_SHA256:", current_i_gate_sha256)
    print("CURRENT_I_GATE_MD_SHA256:", current_i_gate_md_sha256)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
