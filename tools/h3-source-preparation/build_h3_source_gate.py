#!/usr/bin/env python3
"""Build the outcome-blind H3 source/maturity gate from persisted artifacts.

This program never generates touches, confirmation groups, returns, contrasts,
or bootstrap output. It validates:

- exact legacy generator identity;
- the frozen H2 135-file M1 prefix;
- post-H2 M1 raw identities;
- the frozen structural-session classification;
- full-day Tick identities and retrieval evidence;
- one continuous H2 -> H3 M1 history with no Gamma reset.

A 60-session freeze packet is emitted only when the first 60 structurally
eligible sessions exist and every component gate passes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


EXPECTED_GENERATOR_SHA256 = "9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd"
EXPECTED_H2_PREFIX_MANIFEST_SHA256 = "1232af3b557a9559ca22f03e7c21ff748d467794cdaec5b32ddd9c0b437fcec3"
BOOTSTRAP_SEED = 20260913
BOOTSTRAP_REPLICATIONS = 10_000
CANDIDATE_START = "2026-07-10"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return sha256_bytes(raw)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def decode_m1(payload: dict) -> list[dict]:
    """Exact delta decoder semantics used by the recovered legacy generator."""
    mult = float(payload.get("multiplier") or 1)
    scale = 1 if mult >= 1 else 10 ** abs(math.floor(math.log10(mult)))
    stamp = int(payload.get("timestamp") or 0)
    shift = int(payload.get("shift") or 1)
    values = {
        key: payload.get(key) or []
        for key in ("times", "opens", "highs", "lows", "closes")
    }
    if len({len(value) for value in values.values()}) != 1:
        raise ValueError("inconsistent_m1_lengths")

    o, h, l, c = (
        float(payload.get(key) or 0)
        for key in ("open", "high", "low", "close")
    )
    rows = []
    for i, delta in enumerate(values["times"]):
        stamp += shift * int(delta)
        o = math.floor((o + float(values["opens"][i]) * mult) * scale + 0.5) / scale
        h = math.floor((h + float(values["highs"][i]) * mult) * scale + 0.5) / scale
        l = math.floor((l + float(values["lows"][i]) * mult) * scale + 0.5) / scale
        c = math.floor((c + float(values["closes"][i]) * mult) * scale + 0.5) / scale
        rows.append({"ts": stamp, "o": o, "h": h, "l": l, "c": c})
    return rows


def verify_generator(path: Path) -> dict[str, Any]:
    digest = sha256_file(path)
    return {
        "sha256": digest,
        "expected_sha256": EXPECTED_GENERATOR_SHA256,
        "identity": "PASS" if digest == EXPECTED_GENERATOR_SHA256 else "HOLD_MISMATCH",
    }


def verify_h2_prefix(root: Path) -> dict[str, Any]:
    identity_path = root / "h2_prefix_source_identity.json"
    require(identity_path.is_file(), "h2_prefix_identity_missing")
    identity = load_json(identity_path)

    require(
        identity.get("frozen_manifest_sha256") == EXPECTED_H2_PREFIX_MANIFEST_SHA256,
        "h2_prefix_manifest_identity_mismatch",
    )
    require(identity.get("record_count") == 135, "h2_prefix_record_count_mismatch")
    require(
        identity.get("identity") == "PASS_135_EXACT_RAW_MATCH",
        "h2_prefix_not_pass",
    )

    records = identity.get("records") or []
    require(len(records) == 135, "h2_prefix_records_missing")
    dates = [r.get("date") for r in records]
    require(
        dates == sorted(dates) and len(set(dates)) == 135,
        "h2_prefix_order_or_duplicate",
    )
    require(dates[-1] == "2026-07-09", "h2_prefix_end_mismatch")

    failures = []
    for record in records:
        path = root / record["relative_path"]
        if not path.is_file():
            failures.append({"date": record["date"], "reason": "missing_raw"})
            continue
        raw = path.read_bytes()
        digest = sha256_bytes(raw)
        if (
            len(raw) != record["byte_count"]
            or digest != record["sha256"]
            or record.get("identity") != "PASS"
        ):
            failures.append(
                {"date": record["date"], "reason": "raw_identity_mismatch"}
            )

    return {
        "record_count": len(records),
        "first_date": dates[0],
        "last_date": dates[-1],
        "identity_file_sha256": sha256_file(identity_path),
        "records": records,
        "failures": failures,
        "status": "PASS" if not failures else "HOLD",
    }


def verify_m1_inventory(root: Path) -> dict[str, Any]:
    manifest_path = root / "m1_source_manifest.json"
    require(manifest_path.is_file(), "m1_source_manifest_missing")
    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw)

    require(
        manifest.get("candidate_start") == CANDIDATE_START,
        "m1_candidate_start_mismatch",
    )
    require(manifest.get("outcome_computed") is False, "m1_manifest_outcome_flag")
    require(
        manifest.get("confirmation_outcome_comparison") is False,
        "m1_manifest_confirmation_outcome_flag",
    )
    require(manifest.get("bootstrap_run") is False, "m1_manifest_bootstrap_flag")

    records = manifest.get("records") or []
    dates = [r.get("date") for r in records]
    require(
        dates == sorted(dates) and len(set(dates)) == len(dates),
        "m1_manifest_order_or_duplicate",
    )

    failures = []
    for record in records:
        path = root / record["relative_path"]
        if not path.is_file():
            failures.append({"date": record["date"], "reason": "missing_raw"})
            continue
        raw = path.read_bytes()
        if (
            len(raw) != record["byte_count"]
            or sha256_bytes(raw) != record["sha256"]
        ):
            failures.append(
                {"date": record["date"], "reason": "raw_identity_mismatch"}
            )
        if (
            record.get("basic_validation") != "PASS"
            or record.get("status") != "SOURCE_RECORDED"
        ):
            failures.append(
                {"date": record["date"], "reason": "basic_validation_not_pass"}
            )

    return {
        "manifest": manifest,
        "manifest_sha256": sha256_bytes(manifest_raw),
        "records": records,
        "dates": dates,
        "failures": failures,
        "status": "PASS" if not failures else "HOLD",
    }


def verify_structural_manifest(path: Path, m1: dict[str, Any]) -> dict[str, Any]:
    require(path.is_file(), "structural_manifest_missing")
    raw = path.read_bytes()
    manifest = json.loads(raw)

    require(
        manifest.get("input_manifest_sha256") == m1["manifest_sha256"],
        "structural_manifest_input_identity_mismatch",
    )
    require(
        manifest.get("classification_status") == "DOCUMENTED_SUMMER_MINUTE_SET_PASS",
        "structural_classification_status_mismatch",
    )
    require(manifest.get("outcome_computed") is False, "structural_outcome_flag")

    records = manifest.get("records") or []
    require(
        [r.get("date") for r in records] == m1["dates"],
        "structural_dates_mismatch",
    )

    eligible = [r["date"] for r in records if r.get("eligible") is True]
    ineligible = [r for r in records if r.get("eligible") is not True]
    require(
        len(eligible) == manifest.get("structurally_eligible_count"),
        "structural_count_mismatch",
    )

    return {
        "manifest_sha256": sha256_bytes(raw),
        "eligible_dates": eligible,
        "ineligible_records": ineligible,
        "status": "PASS",
    }


def load_verification_receipts(
    root: Path,
) -> dict[tuple[str, int], dict[str, Any]]:
    receipts: dict[tuple[str, int], dict[str, Any]] = {}
    receipt_root = root / "tick_retrieval_verification"
    if not receipt_root.exists():
        return receipts

    for path in sorted(receipt_root.glob("*.json")):
        receipt = load_json(path)
        key = (receipt.get("date"), int(receipt.get("hour")))
        require(key not in receipts, f"duplicate_tick_verification_receipt:{key}")
        receipts[key] = receipt
    return receipts


def verify_ticks(
    root: Path,
    verification_root: Path,
    candidate_dates: list[str],
) -> dict[str, Any]:
    receipts = load_verification_receipts(verification_root)
    failures = []
    records_by_date: dict[str, list[dict[str, Any]]] = {}
    original_timestamp_count = 0
    verified_timestamp_count = 0
    empty_bucket_count = 0

    for day in candidate_dates:
        manifest_path = root / f"tick_source_manifest_{day}.json"
        if not manifest_path.is_file():
            failures.append({"date": day, "reason": "daily_manifest_missing"})
            continue

        manifest = load_json(manifest_path)
        if (
            manifest.get("date") != day
            or manifest.get("hours_requested") != 24
            or manifest.get("outcome_computed") is not False
            or manifest.get("confirmation_outcome_comparison") is not False
            or manifest.get("bootstrap_run") is not False
        ):
            failures.append(
                {"date": day, "reason": "daily_manifest_contract_mismatch"}
            )

        records = manifest.get("records") or []
        records_by_date[day] = records
        if (
            len(records) != 24
            or sorted(r.get("hour") for r in records) != list(range(24))
        ):
            failures.append(
                {"date": day, "reason": "not_exactly_24_hour_records"}
            )
            continue

        for record in records:
            hour = int(record["hour"])
            if record.get("date") != day:
                failures.append(
                    {"date": day, "hour": hour, "reason": "record_date_mismatch"}
                )
                continue

            path = root / record["relative_path"]
            if not path.is_file():
                failures.append(
                    {"date": day, "hour": hour, "reason": "raw_missing"}
                )
                continue

            raw = path.read_bytes()
            digest = sha256_bytes(raw)
            if len(raw) != record["byte_count"] or digest != record["sha256"]:
                failures.append(
                    {"date": day, "hour": hour, "reason": "raw_identity_mismatch"}
                )
            if (
                record.get("json_and_quote_validation") != "PASS"
                or record.get("status") != "SOURCE_RECORDED"
            ):
                failures.append(
                    {"date": day, "hour": hour, "reason": "tick_validation_not_pass"}
                )

            if record.get("quote_count") == 0:
                empty_bucket_count += 1

            if record.get("retrieved_at_utc"):
                original_timestamp_count += 1
                continue

            receipt = receipts.get((day, hour))
            if not receipt:
                failures.append(
                    {
                        "date": day,
                        "hour": hour,
                        "reason": "missing_retrieval_timestamp_and_receipt",
                    }
                )
                continue

            if (
                receipt.get("status") != "EXACT_MATCH"
                or receipt.get("stored_sha256") != digest
                or receipt.get("verified_response_sha256") != digest
                or int(receipt.get("verified_response_bytes")) != len(raw)
                or not receipt.get("verified_retrieval_at_utc")
            ):
                failures.append(
                    {
                        "date": day,
                        "hour": hour,
                        "reason": "verification_receipt_mismatch",
                    }
                )
            else:
                verified_timestamp_count += 1

    return {
        "candidate_dates": len(candidate_dates),
        "hour_records_expected": len(candidate_dates) * 24,
        "hour_records_found": sum(len(v) for v in records_by_date.values()),
        "original_retrieval_timestamp_count": original_timestamp_count,
        "exact_refetch_receipt_count": verified_timestamp_count,
        "verification_receipt_total": len(receipts),
        "empty_bucket_count": empty_bucket_count,
        "records_by_date": records_by_date,
        "failures": failures,
        "status": "PASS" if not failures else "HOLD",
    }


def verify_combined_m1_continuity(
    h2_root: Path,
    m1_root: Path,
    h2_records: list[dict[str, Any]],
    post_records: list[dict[str, Any]],
) -> dict[str, Any]:
    entries: list[tuple[str, Path, str]] = []

    for record in h2_records:
        entries.append(
            (
                record["date"],
                h2_root / record["relative_path"],
                record["sha256"],
            )
        )
    for record in post_records:
        entries.append(
            (
                record["date"],
                m1_root / record["relative_path"],
                record["sha256"],
            )
        )

    dates = [day for day, _, _ in entries]
    require(dates == sorted(dates), "combined_m1_dates_not_sorted")
    require(len(set(dates)) == len(dates), "combined_m1_duplicate_date")
    require(
        dates[134] == "2026-07-09" and dates[135] == "2026-07-10",
        "h2_h3_prefix_boundary_mismatch",
    )

    last_ts = None
    row_count = 0
    failures = []

    for day, path, _ in entries:
        rows = decode_m1(json.loads(path.read_bytes()))
        for row in rows:
            if not (
                math.isfinite(row["o"])
                and math.isfinite(row["h"])
                and math.isfinite(row["l"])
                and math.isfinite(row["c"])
                and row["h"] >= row["l"]
                and row["l"] <= row["o"] <= row["h"]
                and row["l"] <= row["c"] <= row["h"]
            ):
                failures.append(
                    {"date": day, "reason": "invalid_combined_m1_ohlc"}
                )
                break
            ts = row["ts"]
            if last_ts is not None and ts <= last_ts:
                failures.append(
                    {
                        "date": day,
                        "reason": "global_m1_not_strictly_increasing",
                        "timestamp": ts,
                    }
                )
                break
            last_ts = ts
            row_count += 1
        if failures:
            break

    chain = [{"date": day, "sha256": digest} for day, _, digest in entries]

    return {
        "file_count": len(entries),
        "first_date": dates[0],
        "prefix_last_date": dates[134],
        "post_prefix_first_date": dates[135],
        "latest_date": dates[-1],
        "decoded_row_count": row_count,
        "gamma_history_reset": False,
        "source_chain_sha256": canonical_sha256(chain),
        "failures": failures,
        "status": "PASS" if not failures else "HOLD",
    }


def gate_state(
    *,
    eligible_count: int,
    all_components_pass: bool,
) -> tuple[str, str, str]:
    if not all_components_pass:
        return "HOLD", "HALTED_FAIL_CLOSED", "HALTED_FAIL_CLOSED"
    if eligible_count < 60:
        return (
            "NOT_EVALUATED_PENDING_MATURITY",
            "WAITING_FOR_MATURITY",
            "ACQUIRE_NEXT_FULLY_COMPLETED_UTC_CANDIDATE_OUTCOME_BLIND",
        )
    return (
        "PASS",
        "READY_FOR_FROZEN_H3_RUN",
        "RUN_EXISTING_POST_H2_PREREGISTRATION_ONCE",
    )


def build(args: argparse.Namespace) -> dict[str, Any]:
    generator = verify_generator(args.legacy_generator)
    h2 = verify_h2_prefix(args.h2_prefix_root)
    m1 = verify_m1_inventory(args.m1_root)
    structural = verify_structural_manifest(args.structural_manifest, m1)
    ticks = verify_ticks(
        args.tick_root,
        args.tick_verification_root,
        m1["dates"],
    )
    continuity = verify_combined_m1_continuity(
        args.h2_prefix_root,
        args.m1_root,
        h2["records"],
        m1["records"],
    )

    component_status = {
        "legacy_generator_identity": generator["identity"],
        "h2_prefix_identity": h2["status"],
        "post_h2_m1_identity": m1["status"],
        "m1_structural_gate": structural["status"],
        "tick_identity": ticks["status"],
        "h2_to_h3_m1_continuity": continuity["status"],
    }

    eligible = structural["eligible_dates"]
    maturity = len(eligible) >= 60
    selected = eligible[:60] if maturity else []
    all_components_pass = all(
        value == "PASS" for value in component_status.values()
    )
    source_gate, current_state, next_action = gate_state(
        eligible_count=len(eligible),
        all_components_pass=all_components_pass,
    )

    freeze_packet = None
    if maturity and all_components_pass:
        selected_set = set(selected)
        selected_m1 = [
            {"date": record["date"], "sha256": record["sha256"]}
            for record in m1["records"]
            if record["date"] in selected_set
        ]
        selected_ticks = []
        for day in selected:
            manifest_path = args.tick_root / f"tick_source_manifest_{day}.json"
            selected_ticks.append(
                {
                    "date": day,
                    "manifest_sha256": sha256_file(manifest_path),
                    "hour_sha256": [
                        record["sha256"]
                        for record in ticks["records_by_date"][day]
                    ],
                }
            )

        freeze_packet = {
            "status": "FROZEN_BEFORE_H3_OUTCOME_ACCESS",
            "specification": "SPEC-HR-003-v01",
            "decision": "DEC-HR-004",
            "candidate_start": CANDIDATE_START,
            "selected_session_count": 60,
            "selected_dates": selected,
            "selected_dates_sha256": sha256_bytes(
                ("\n".join(selected) + "\n").encode("utf-8")
            ),
            "legacy_generator_sha256": generator["sha256"],
            "generator_history_source_chain_sha256": continuity[
                "source_chain_sha256"
            ],
            "generator_history_file_count": continuity["file_count"],
            "h2_prefix_identity_file_sha256": h2["identity_file_sha256"],
            "h2_prefix_record_count": h2["record_count"],
            "post_h2_m1_manifest_sha256": m1["manifest_sha256"],
            "structural_manifest_sha256": structural["manifest_sha256"],
            "selected_m1_raw_sha256": selected_m1,
            "selected_tick_identity": selected_ticks,
            "bootstrap_seed": BOOTSTRAP_SEED,
            "bootstrap_replications": BOOTSTRAP_REPLICATIONS,
            "outcome_computed": False,
            "confirmation_outcome_comparison": False,
            "bootstrap_run": False,
            "protocol_changed": False,
            "parameter_search": False,
            "sample_reselection": False,
        }
        freeze_packet["freeze_packet_sha256"] = canonical_sha256(
            freeze_packet
        )

    return {
        "scope": "H3_OUTCOME_BLIND_FULL_SOURCE_AND_MATURITY_GATE",
        "status": current_state,
        "source_gate": source_gate,
        "candidate_start": CANDIDATE_START,
        "latest_candidate_date_checked": m1["manifest"].get(
            "latest_candidate_date_checked"
        ),
        "calendar_candidate_count": len(m1["dates"]),
        "structurally_eligible_count": len(eligible),
        "eligible_chronological_prefix": eligible,
        "structurally_ineligible_records": structural["ineligible_records"],
        "frozen_selected_count": len(selected),
        "frozen_selected_dates": selected,
        "sessions_remaining_to_maturity": max(0, 60 - len(eligible)),
        "component_status": component_status,
        "generator_identity": generator,
        "h2_prefix": {
            key: h2[key]
            for key in (
                "record_count",
                "first_date",
                "last_date",
                "identity_file_sha256",
                "failures",
                "status",
            )
        },
        "m1": {
            "manifest_sha256": m1["manifest_sha256"],
            "record_count": len(m1["records"]),
            "failures": m1["failures"],
            "status": m1["status"],
        },
        "ticks": {
            key: ticks[key]
            for key in (
                "candidate_dates",
                "hour_records_expected",
                "hour_records_found",
                "original_retrieval_timestamp_count",
                "exact_refetch_receipt_count",
                "verification_receipt_total",
                "empty_bucket_count",
                "failures",
                "status",
            )
        },
        "combined_m1_continuity": continuity,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "bootstrap_replications": BOOTSTRAP_REPLICATIONS,
        "outcome_computed": False,
        "confirmation_outcome_comparison": False,
        "bootstrap_run": False,
        "protocol_changed": False,
        "parameter_search": False,
        "sample_reselection": False,
        "next_action": next_action,
        "freeze_packet": freeze_packet,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m1-root", type=Path, required=True)
    parser.add_argument("--h2-prefix-root", type=Path, required=True)
    parser.add_argument("--tick-root", type=Path, required=True)
    parser.add_argument("--tick-verification-root", type=Path, required=True)
    parser.add_argument("--structural-manifest", type=Path, required=True)
    parser.add_argument("--legacy-generator", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = build(args)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "source_gate": result["source_gate"],
                "eligible": result["structurally_eligible_count"],
                "frozen_selected_count": result["frozen_selected_count"],
                "sessions_remaining_to_maturity": result[
                    "sessions_remaining_to_maturity"
                ],
                "output": str(args.output),
            }
        )
    )


if __name__ == "__main__":
    main()
