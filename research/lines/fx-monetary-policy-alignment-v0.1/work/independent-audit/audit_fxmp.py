#!/usr/bin/env python3
"""Independent pre-outcome audit for RL-FXMP-001.

The audit intentionally uses an independently written oracle for synthetic
cases. It does not read FX prices, CSM rankings, target returns, or P/L.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from decimal import Decimal
from pathlib import Path

LINE = Path(__file__).resolve().parents[2]
IMPL = LINE / "work" / "implementation" / "policy_feature.py"
LOCK = LINE / "work" / "source-qualification" / "SOURCE_LOCK.json"
SPEC = LINE / "specifications" / "SPEC-FXMP-001-v01.md"

EXPECTED_ARCHIVE_SHA256 = "707f39206f7c4bc1001ea7f67b182d20e9b2d59fcf6542d0dd566a19f61d7f15"
EXPECTED_SLICE_SHA256 = "2cf878dbd0b8a98c05db741dc40a14d0b62a7cb6c178f86121937b0d41eb7eee"
EXPECTED_MAPPING = {
    "AUD": "AU",
    "CAD": "CA",
    "CHF": "CH",
    "EUR": "XM",
    "GBP": "GB",
    "JPY": "JP",
    "NZD": "NZ",
    "USD": "US",
}


def month_index(month: str) -> int:
    y, m = month.split("-")
    return int(y) * 12 + int(m) - 1


def oracle_guard(currency: str, old: str, new: str, lock: dict) -> str | None:
    if currency not in EXPECTED_MAPPING:
        return "POLICY_SOURCE_INVALID"
    oi = month_index(old)
    ni = month_index(new)
    if oi >= ni:
        return "POLICY_SOURCE_INVALID"
    area = EXPECTED_MAPPING[currency]
    guards = lock["monthly_feature_guards"]
    for start, end in guards.get("unavailable_month_ranges", {}).get(area, []):
        if oi <= month_index(end) and ni >= month_index(start):
            return "POLICY_RATE_UNAVAILABLE"
    switch = guards.get("instrument_switch_months", {}).get(area)
    if switch is not None and oi < month_index(switch) <= ni:
        return "POLICY_INSTRUMENT_BREAK_CROSSED"
    return None


def oracle_change(currency: str, old: str, new: str, values: dict, lock: dict):
    reason = oracle_guard(currency, old, new, lock)
    if reason:
        return None, reason
    if (currency, old) not in values or (currency, new) not in values:
        return None, "POLICY_SOURCE_MISSING"
    try:
        a = Decimal(str(values[(currency, old)]))
        b = Decimal(str(values[(currency, new)]))
    except Exception:
        return None, "POLICY_SOURCE_INVALID"
    if not a.is_finite() or not b.is_finite():
        return None, "POLICY_SOURCE_INVALID"
    return b - a, None


def oracle_record(event: dict, values: dict, lock: dict) -> dict:
    pa, ra = oracle_change(event["a"], event["policy_old_month"], event["policy_new_month"], values, lock)
    pb, rb = oracle_change(event["b"], event["policy_old_month"], event["policy_new_month"], values, lock)
    reasons = sorted(set(r for r in (ra, rb) if r))
    if reasons:
        return {
            "status": "UNAVAILABLE",
            "reason_codes": reasons,
            "classification": None,
        }
    z = pa - pb
    label = "ALIGNED" if z > 0 else "OPPOSED" if z < 0 else "NEUTRAL"
    return {
        "status": "AVAILABLE",
        "reason_codes": [],
        "classification": label,
        "p_a": format(pa, "f"),
        "p_b": format(pb, "f"),
        "z": format(z, "f"),
    }


def import_impl():
    spec = importlib.util.spec_from_file_location("fxmp_policy_feature_audited", IMPL)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load implementation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def audit_static_boundary():
    tree = ast.parse(IMPL.read_text(encoding="utf-8"))
    forbidden_modules = {"urllib", "requests", "httpx", "socket", "subprocess", "pandas", "numpy"}
    imports = set()
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
    bad_imports = sorted(imports & forbidden_modules)
    if bad_imports:
        raise AssertionError(f"forbidden implementation imports: {bad_imports}")
    bad_calls = sorted(set(calls) & {"open", "urlopen", "request", "post", "run", "Popen"})
    if bad_calls:
        raise AssertionError(f"forbidden implementation calls: {bad_calls}")
    return {"imports": sorted(imports), "forbidden_imports": [], "forbidden_calls": []}


def main():
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    spec_text = SPEC.read_text(encoding="utf-8")
    impl = import_impl()

    assert_equal(lock["source"]["archive_sha256"], EXPECTED_ARCHIVE_SHA256, "archive sha")
    assert_equal(lock["predictor_slice"]["deterministic_slice_sha256"], EXPECTED_SLICE_SHA256, "slice sha")
    assert_equal(lock["currency_to_ref_area"], EXPECTED_MAPPING, "currency mapping")
    assert "PROPOSED_NOT_FROZEN" in spec_text
    assert "D = mean(y_k | ALIGNED) - mean(y_k | OPPOSED)" in spec_text
    assert "r_i(k-1) - r_i(k-4)" in spec_text

    static = audit_static_boundary()

    cases = [
        {
            "name": "aligned",
            "event": {"event_id":"c1","a":"AUD","b":"CAD","policy_old_month":"2020-01","policy_new_month":"2020-04"},
            "values": {("AUD","2020-01"):"0.75",("AUD","2020-04"):"1.00",("CAD","2020-01"):"1.75",("CAD","2020-04"):"1.75"},
        },
        {
            "name": "opposed",
            "event": {"event_id":"c2","a":"AUD","b":"CAD","policy_old_month":"2020-01","policy_new_month":"2020-04"},
            "values": {("AUD","2020-01"):"1.00",("AUD","2020-04"):"0.75",("CAD","2020-01"):"1.75",("CAD","2020-04"):"1.75"},
        },
        {
            "name": "neutral",
            "event": {"event_id":"c3","a":"AUD","b":"CAD","policy_old_month":"2020-01","policy_new_month":"2020-04"},
            "values": {("AUD","2020-01"):"1.00",("AUD","2020-04"):"1.25",("CAD","2020-01"):"1.50",("CAD","2020-04"):"1.75"},
        },
        {
            "name": "ch_break",
            "event": {"event_id":"c4","a":"CHF","b":"USD","policy_old_month":"2019-03","policy_new_month":"2019-06"},
            "values": {("CHF","2019-03"):"-0.75",("CHF","2019-06"):"-0.75",("USD","2019-03"):"2.40",("USD","2019-06"):"2.40"},
        },
        {
            "name": "xm_break",
            "event": {"event_id":"c5","a":"EUR","b":"USD","policy_old_month":"2024-06","policy_new_month":"2024-09"},
            "values": {("EUR","2024-06"):"4.25",("EUR","2024-09"):"3.50",("USD","2024-06"):"5.375",("USD","2024-09"):"5.125"},
        },
        {
            "name": "jp_no_policy",
            "event": {"event_id":"c6","a":"JPY","b":"USD","policy_old_month":"2013-03","policy_new_month":"2013-06"},
            "values": {("JPY","2013-03"):"0.1",("JPY","2013-06"):"0.1",("USD","2013-03"):"0.125",("USD","2013-06"):"0.125"},
        },
        {
            "name": "missing",
            "event": {"event_id":"c7","a":"NZD","b":"USD","policy_old_month":"2020-01","policy_new_month":"2020-04"},
            "values": {("NZD","2020-01"):"1.0",("USD","2020-01"):"1.5",("USD","2020-04"):"1.0"},
        },
        {
            "name": "invalid",
            "event": {"event_id":"c8","a":"GBP","b":"USD","policy_old_month":"2020-01","policy_new_month":"2020-04"},
            "values": {("GBP","2020-01"):"0.75",("GBP","2020-04"):"NaN",("USD","2020-01"):"1.5",("USD","2020-04"):"1.0"},
        },
    ]

    case_results = []
    for case in cases:
        expected = oracle_record(case["event"], case["values"], lock)
        actual_full = impl.build_feature_record(case["event"], case["values"], lock)
        actual = {k: actual_full.get(k) for k in expected}
        assert_equal(actual, expected, case["name"])
        case_results.append({"name": case["name"], "status": "PASS"})

    invariant_event = {
        "event_id": "inv1",
        "a": "AUD",
        "b": "CAD",
        "policy_old_month": "2020-01",
        "policy_new_month": "2020-04",
        "future_return": "999",
        "target_price": "12345",
    }
    invariant_values = {
        ("AUD","2020-01"):"1.00",("AUD","2020-04"):"1.25",
        ("CAD","2020-01"):"1.50",("CAD","2020-04"):"1.50",
    }
    variants = []
    for v1, v2 in [("999","12345"),("-999","0"),("0","-500")]:
        e = dict(invariant_event)
        e["future_return"] = v1
        e["target_price"] = v2
        variants.append(e)
    stripped = dict(invariant_event)
    stripped.pop("future_return")
    stripped.pop("target_price")
    variants.append(stripped)
    hashes = {
        hashlib.sha256(impl.canonical_ledger_bytes(impl.build_feature_ledger([e], invariant_values, lock))).hexdigest()
        for e in variants
    }
    assert_equal(len(hashes), 1, "outcome invariance")

    report = {
        "audit_id": "AUDIT-FXMP-E-20261004-01",
        "audited_head": "d1a8d41d74eac78d420c6776971af3cc1be37931",
        "source_archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "predictor_slice_sha256": EXPECTED_SLICE_SHA256,
        "static_boundary": static,
        "independent_oracle_cases": case_results,
        "outcome_field_invariance": "PASS",
        "market_outcome_accessed": False,
        "result": "PASS_WITH_RECORDED_GAPS",
        "recorded_gaps": [
            "Predictor raw bytes are identified by hash but the recorded Actions artifact is temporary.",
            "OBS_STATUS=A and OBS_CONF=F official codelist meanings are not yet locked in the source receipt.",
            "Point-in-time historical vintage availability remains unverified; the claim is retrospective latest-vintage only.",
            "Final inference implementation and its synthetic audit are not yet present.",
            "Scientific choices 3-month lookback and 24/24 group minima remain unfrozen."
        ],
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
