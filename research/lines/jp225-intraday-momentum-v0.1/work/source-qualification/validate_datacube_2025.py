#!/usr/bin/env python3
"""Outcome-blind local validator for JPX DataCube 2025 Nikkei 225 mini ticks.

This program reads local CSV/ZIP files, reports source identity and coverage
metadata, and never writes or prints row-level market values. It does not
calculate returns, differences, signs, correlations, regression, or P&L.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, TextIO


EXPECTED_HEADER = (
    "trade_date",
    "execution_date",
    "index_type",
    "security_code",
    "time",
    "trade_price",
    "price_type",
    "trade_volume",
    "no",
    "contract_month",
    "sco_category",
)
EXPECTED_MONTHS = tuple(f"2025-{month:02d}" for month in range(1, 13))
BOUNDARIES = {
    "09:30:00": 9 * 60 * 60 * 1000 + 30 * 60 * 1000,
    "15:00:00": 15 * 60 * 60 * 1000,
    "15:30:00": 15 * 60 * 60 * 1000 + 30 * 60 * 1000,
}
WINDOW_WIDTH_MS = 60_000
EXPECTED_PRODUCT_INDEX = "19"
EXPECTED_CONTRACTS_2025 = ("202503", "202506", "202509", "202512", "202603")
CALENDAR_PATH = Path(__file__).with_name("TSE_2025_EXPECTED_CONTRACTS.csv")
OUTCOME_BLINDNESS_STATUS = "COMPROMISED_BY_EXTERNAL_2025_QUOTE_SNIPPET"


def expected_contract_for(day: str) -> str | None:
    """Return the frozen quarterly front month for a 2025 execution date."""
    if "2025-01-01" <= day <= "2025-03-13":
        return "202503"
    if "2025-03-14" <= day <= "2025-06-12":
        return "202506"
    if "2025-06-13" <= day <= "2025-09-11":
        return "202509"
    if "2025-09-12" <= day <= "2025-12-11":
        return "202512"
    if "2025-12-12" <= day <= "2025-12-31":
        return "202603"
    return None


def load_calendar(path: Path = CALENDAR_PATH) -> dict[str, str]:
    calendar: dict[str, str] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["execution_date", "expected_front_contract_month"]:
            raise ValueError("CALENDAR_SCHEMA_MISMATCH")
        for row in reader:
            day = row["execution_date"]
            contract = row["expected_front_contract_month"]
            date.fromisoformat(day)
            if day[:4] != "2025" or contract != expected_contract_for(day):
                raise ValueError("CALENDAR_VALUE_OUT_OF_SCOPE")
            if day in calendar:
                raise ValueError("CALENDAR_DUPLICATE_DATE")
            calendar[day] = contract
    if not calendar:
        raise ValueError("CALENDAR_EMPTY")
    return calendar


def parse_date(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    try:
        if len(value) == 8 and value.isdigit():
            return date(int(value[:4]), int(value[4:6]), int(value[6:8])).isoformat()
        return date.fromisoformat(value).isoformat()
    except ValueError:
        return None


def parse_time_ms(value: str | None) -> int | None:
    if value is None:
        return None
    digits = value.strip()
    if not digits.isdigit() or len(digits) > 9:
        return None
    digits = digits.zfill(9)
    hour, minute, second, millis = (
        int(digits[0:2]),
        int(digits[2:4]),
        int(digits[4:6]),
        int(digits[6:9]),
    )
    if hour > 23 or minute > 59 or second > 59 or millis > 999:
        return None
    return ((hour * 60 + minute) * 60 + second) * 1000 + millis


def positive_finite(value: str | None) -> bool:
    if value is None:
        return False
    try:
        number = Decimal(value.strip())
    except (InvalidOperation, ValueError):
        return False
    return number.is_finite() and number > 0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def input_files(raw_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in raw_dir.rglob("*")
        if path.is_file() and (path.suffix.lower() == ".csv" or path.suffix.lower() == ".zip")
    )


def csv_streams(path: Path) -> Iterable[tuple[str, TextIO, Any]]:
    """Yield CSV text streams, without extracting an archive to disk."""
    if path.suffix.lower() == ".csv":
        stream = path.open("r", encoding="utf-8-sig", newline="")
        yield path.name, stream, None
        return
    archive = zipfile.ZipFile(path, "r")
    members = sorted(
        name for name in archive.namelist()
        if name.lower().endswith(".csv") and not name.endswith("/")
    )
    if not members:
        archive.close()
        raise ValueError("ARCHIVE_HAS_NO_CSV")
    for name in members:
        binary = archive.open(name, "r")
        import io
        stream = io.TextIOWrapper(binary, encoding="utf-8-sig", newline="")
        yield name, stream, archive


def _create_diagnostics_db(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA journal_mode=OFF;
        PRAGMA synchronous=OFF;
        CREATE TABLE sequence_keys (
            trade_date TEXT NOT NULL,
            security_code TEXT NOT NULL,
            seq_no TEXT NOT NULL,
            occurrences INTEGER NOT NULL,
            PRIMARY KEY (trade_date, security_code, seq_no)
        );
        CREATE TABLE timestamp_groups (
            trade_date TEXT NOT NULL,
            execution_date TEXT NOT NULL,
            security_code TEXT NOT NULL,
            time_value TEXT NOT NULL,
            row_count INTEGER NOT NULL,
            missing_seq_count INTEGER NOT NULL,
            PRIMARY KEY (trade_date, execution_date, security_code, time_value)
        );
        CREATE TABLE timestamp_sequence_keys (
            trade_date TEXT NOT NULL,
            execution_date TEXT NOT NULL,
            security_code TEXT NOT NULL,
            time_value TEXT NOT NULL,
            seq_no TEXT NOT NULL,
            PRIMARY KEY (trade_date, execution_date, security_code, time_value, seq_no)
        );
        """
    )


def _update_sequence_diagnostics(
    db: sqlite3.Connection,
    trade_day: str | None,
    execution_day: str | None,
    security_code: str,
    raw_time: str,
    sequence: str,
) -> None:
    if trade_day is None or execution_day is None:
        return
    db.execute(
        """INSERT INTO timestamp_groups VALUES (?, ?, ?, ?, 1, ?)
        ON CONFLICT(trade_date, execution_date, security_code, time_value)
        DO UPDATE SET row_count=row_count+1,
                      missing_seq_count=missing_seq_count+excluded.missing_seq_count""",
        (trade_day, execution_day, security_code, raw_time, int(not sequence)),
    )
    if sequence:
        db.execute(
            "INSERT OR IGNORE INTO timestamp_sequence_keys VALUES (?, ?, ?, ?, ?)",
            (trade_day, execution_day, security_code, raw_time, sequence),
        )
        db.execute(
            """INSERT INTO sequence_keys VALUES (?, ?, ?, 1)
            ON CONFLICT(trade_date, security_code, seq_no)
            DO UPDATE SET occurrences=occurrences+1""",
            (trade_day, security_code, sequence),
        )


def _file_diagnostics(db: sqlite3.Connection) -> dict[str, int]:
    duplicate_sequences = db.execute(
        "SELECT COUNT(*) FROM sequence_keys WHERE occurrences > 1"
    ).fetchone()[0]
    same_timestamp_groups = db.execute(
        "SELECT COUNT(*) FROM timestamp_groups WHERE row_count > 1"
    ).fetchone()[0]
    ambiguous_timestamp_groups = db.execute(
        """
        SELECT COUNT(*) FROM timestamp_groups g
        LEFT JOIN (
            SELECT trade_date, execution_date, security_code, time_value,
                   COUNT(*) AS distinct_sequence_count
            FROM timestamp_sequence_keys
            GROUP BY trade_date, execution_date, security_code, time_value
        ) s USING (trade_date, execution_date, security_code, time_value)
        WHERE g.row_count > 1 AND
              (g.missing_seq_count > 0 OR COALESCE(s.distinct_sequence_count, 0) < g.row_count)
        """
    ).fetchone()[0]
    return {
        "duplicate_sequence_groups": int(duplicate_sequences),
        "same_millisecond_timestamp_groups": int(same_timestamp_groups),
        "ambiguous_same_timestamp_groups": int(ambiguous_timestamp_groups),
    }


def _open_csv_members(path: Path) -> list[tuple[str, TextIO, Any]]:
    try:
        return list(csv_streams(path))
    except (OSError, zipfile.BadZipFile, RuntimeError, UnicodeDecodeError, ValueError):
        raise ValueError("FILE_OPEN_FAILED") from None


def _read_file(
    path: Path,
    raw_dir: Path,
    calendar: dict[str, str],
    db: sqlite3.Connection,
) -> tuple[dict[str, Any], dict[str, Any]]:
    relative_name = path.relative_to(raw_dir).as_posix()
    file_record: dict[str, Any] = {
        "filename": relative_name,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "csv_members": [],
        "row_count": 0,
        "header_sha256": None,
        "schema_match": False,
        "schema_status": "NOT_READ",
        "execution_date_min": None,
        "execution_date_max": None,
        "trade_date_min": None,
        "trade_date_max": None,
        "index_type_values": [],
        "contract_month_counts": {},
        "sco_category_counts": {},
        "purchase_month_inferred_from_trade_date": None,
        "status_code": "OK",
    }
    state: dict[str, Any] = {
        "expected_contracts_seen": set(),
        "expected_contract_dates_seen": set(),
        "out_of_scope_date_rows": 0,
        "malformed_date_rows": 0,
        "invalid_time_rows": 0,
        "missing_sequence_rows": 0,
        "invalid_sequence_rows": 0,
        "nonmonotonic_sequence_transitions": 0,
        "index_values": set(),
        "contract_counts": Counter(),
        "sco_counts": Counter(),
        "trade_dates": set(),
        "execution_dates": set(),
        "boundary_candidates": defaultdict(lambda: {"row_count": 0, "sequence_values": set(), "missing_sequence_rows": 0}),
        "boundary_seen_product_contract": set(),
        "boundary_seen_nonstrategy": set(),
    }
    last_sequence_by_key: dict[tuple[str, str], int] = {}
    try:
        members = _open_csv_members(path)
    except ValueError:
        file_record["status_code"] = "FILE_OPEN_FAILED"
        return file_record, state
    if not members:
        file_record["status_code"] = "NO_CSV_MEMBER"
        return file_record, state
    open_archives = {archive for _, _, archive in members if archive is not None}
    for member_name, stream, archive in members:
        member_record: dict[str, Any] = {"member_name": member_name}
        try:
            reader = csv.DictReader(stream)
            header = tuple(reader.fieldnames or ())
            header_text = "\x1f".join(header).encode("utf-8")
            file_record["header_sha256"] = hashlib.sha256(header_text).hexdigest()
            schema_match = header == EXPECTED_HEADER
            file_record["schema_match"] = file_record["schema_match"] or schema_match
            member_record["schema_match"] = schema_match
            member_record["header_field_count"] = len(header)
            if not schema_match:
                file_record["schema_status"] = "SCHEMA_MISMATCH"
                member_record["schema_status"] = "SCHEMA_MISMATCH"
                file_record["status_code"] = "SCHEMA_MISMATCH"
                for row in reader:
                    file_record["row_count"] += 1
                file_record["csv_members"].append(member_record)
                continue
            file_record["schema_status"] = "MATCH"
            for row in reader:
                file_record["row_count"] += 1
                state["row_count"] = state.get("row_count", 0) + 1
                trade_day = parse_date(row.get("trade_date"))
                execution_day = parse_date(row.get("execution_date"))
                if trade_day is None or execution_day is None:
                    state["malformed_date_rows"] += 1
                else:
                    state["trade_dates"].add(trade_day)
                    state["execution_dates"].add(execution_day)
                    if trade_day[:4] != "2025" or execution_day[:4] != "2025":
                        state["out_of_scope_date_rows"] += 1
                index_type = (row.get("index_type") or "").strip()
                if index_type:
                    state["index_values"].add(index_type)
                    file_record.setdefault("_index_counts", Counter())[index_type] += 1
                contract = (row.get("contract_month") or "").strip()
                if contract:
                    state["contract_counts"][contract] += 1
                    file_record.setdefault("_contract_counts", Counter())[contract] += 1
                    if index_type == EXPECTED_PRODUCT_INDEX and contract in EXPECTED_CONTRACTS_2025:
                        state["expected_contracts_seen"].add(contract)
                sco = (row.get("sco_category") or "").strip()
                if sco:
                    state["sco_counts"][sco] += 1
                    file_record.setdefault("_sco_counts", Counter())[sco] += 1

                security = (row.get("security_code") or "").strip()
                sequence = (row.get("no") or "").strip()
                normalized_sequence = str(int(sequence)) if sequence.isdigit() else sequence
                _update_sequence_diagnostics(
                    db, trade_day, execution_day, security,
                    (row.get("time") or "").strip().zfill(9), normalized_sequence,
                )
                if not sequence:
                    state["missing_sequence_rows"] += 1
                elif not sequence.isdigit():
                    state["invalid_sequence_rows"] += 1
                elif trade_day is not None:
                    sequence_key = (trade_day, security)
                    number = int(sequence)
                    previous = last_sequence_by_key.get(sequence_key)
                    if previous is not None and number < previous:
                        state["nonmonotonic_sequence_transitions"] += 1
                    last_sequence_by_key[sequence_key] = number

                time_ms = parse_time_ms(row.get("time"))
                if time_ms is None:
                    state["invalid_time_rows"] += 1
                    continue
                if trade_day is None or execution_day is None:
                    continue
                if trade_day[:4] != "2025" or execution_day[:4] != "2025":
                    continue
                expected_contract = calendar.get(execution_day)
                if expected_contract is None:
                    continue
                if (
                    index_type == EXPECTED_PRODUCT_INDEX
                    and contract == expected_contract
                    and trade_day == execution_day
                ):
                    state["expected_contract_dates_seen"].add(execution_day)
                    state["boundary_seen_product_contract"].add(execution_day)
                if (
                    index_type != EXPECTED_PRODUCT_INDEX
                    or contract != expected_contract
                    or trade_day != execution_day
                ):
                    continue
                state["boundary_seen_product_contract"].add(execution_day)
                sco_category = sco
                if sco_category != "0":
                    continue
                state["boundary_seen_nonstrategy"].add(execution_day)
                if not positive_finite(row.get("trade_price")) or not positive_finite(row.get("trade_volume")):
                    continue
                if not sequence or not sequence.isdigit():
                    continue
                for boundary, start_ms in BOUNDARIES.items():
                    if start_ms <= time_ms <= start_ms + WINDOW_WIDTH_MS:
                        key = (execution_day, boundary, security, time_ms)
                        candidate = state["boundary_candidates"][key]
                        candidate["row_count"] += 1
                        candidate["sequence_values"].add(normalized_sequence)
        except (csv.Error, UnicodeDecodeError, OSError):
            file_record["status_code"] = "CSV_READ_FAILED"
        finally:
            stream.close()
        file_record["csv_members"].append(member_record)
    for archive in open_archives:
        archive.close()

    if state["trade_dates"]:
        file_record["trade_date_min"] = min(state["trade_dates"])
        file_record["trade_date_max"] = max(state["trade_dates"])
    if state["execution_dates"]:
        file_record["execution_date_min"] = min(state["execution_dates"])
        file_record["execution_date_max"] = max(state["execution_dates"])
    trade_months = sorted({day[:7] for day in state["trade_dates"]})
    if len(trade_months) == 1:
        file_record["purchase_month_inferred_from_trade_date"] = trade_months[0]
    elif len(trade_months) > 1:
        file_record["status_code"] = "MULTIPLE_TRADE_MONTHS_IN_FILE"
    file_record["index_type_values"] = sorted(state["index_values"])
    file_record["contract_month_counts"] = dict(sorted(state["contract_counts"].items()))
    file_record["sco_category_counts"] = dict(sorted(state["sco_counts"].items()))
    file_record.pop("_index_counts", None)
    file_record.pop("_contract_counts", None)
    file_record.pop("_sco_counts", None)
    return file_record, state


def _load_attestations(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _timezone_status(attestations: dict[str, Any]) -> dict[str, Any]:
    timezone_note = attestations.get("timezone_semantics", {})
    if (
        isinstance(timezone_note, dict)
        and timezone_note.get("status") == "CONFIRMED"
        and timezone_note.get("timezone") == "JST"
        and str(timezone_note.get("source_url", "")).startswith("https://")
        and timezone_note.get("checked_at")
        and timezone_note.get("reviewer")
    ):
        return {
            "status": "ATTESTED_JST",
            "source_url": timezone_note["source_url"],
            "checked_at": timezone_note["checked_at"],
            "reviewer": timezone_note["reviewer"],
        }
    return {"status": "UNCONFIRMED", "source_url": None, "checked_at": None, "reviewer": None}


def build_receipt(
    raw_dir: Path,
    calendar_path: Path = CALENDAR_PATH,
    attestations_path: Path | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    raw_dir = raw_dir.resolve()
    calendar = load_calendar(calendar_path)
    files = input_files(raw_dir)
    with tempfile.TemporaryDirectory(prefix="jpx-source-qualification-") as temp_dir:
        db = sqlite3.connect(str(Path(temp_dir) / "diagnostics.sqlite3"))
        _create_diagnostics_db(db)
        file_records: list[dict[str, Any]] = []
        file_states: list[dict[str, Any]] = []
        for path in files:
            file_record, state = _read_file(path, raw_dir, calendar, db)
            file_records.append(file_record)
            file_states.append(state)
        db.commit()
        diagnostics = _file_diagnostics(db)
        db.close()

    all_trade_dates = set().union(*(state["trade_dates"] for state in file_states)) if file_states else set()
    all_execution_dates = set().union(*(state["execution_dates"] for state in file_states)) if file_states else set()
    all_index_values = set().union(*(state["index_values"] for state in file_states)) if file_states else set()
    all_contracts_seen = set().union(*(state["expected_contracts_seen"] for state in file_states)) if file_states else set()
    all_expected_contract_dates_seen = set().union(
        *(state["expected_contract_dates_seen"] for state in file_states)
    ) if file_states else set()
    contract_counts: Counter[str] = Counter()
    sco_counts: Counter[str] = Counter()
    boundary_candidates: dict[tuple[str, str, str, int], dict[str, Any]] = {}
    for state in file_states:
        contract_counts.update(state["contract_counts"])
        sco_counts.update(state["sco_counts"])
        for key, value in state["boundary_candidates"].items():
            target = boundary_candidates.setdefault(
                key, {"row_count": 0, "sequence_values": set()}
            )
            target["row_count"] += value["row_count"]
            target["sequence_values"].update(value["sequence_values"])

    months_to_files: dict[str, list[str]] = defaultdict(list)
    for record in file_records:
        month = record["purchase_month_inferred_from_trade_date"]
        if month:
            months_to_files[month].append(record["filename"])
    months_seen = sorted(months_to_files)
    month_file_identity_complete = (
        tuple(months_seen) == EXPECTED_MONTHS
        and all(len(months_to_files[month]) == 1 for month in EXPECTED_MONTHS)
        and len(file_records) == 12
    )
    expected_contracts_missing = sorted(set(EXPECTED_CONTRACTS_2025) - all_contracts_seen)

    boundary_results: dict[str, Any] = {}
    candidate_rows_per_boundary = Counter()
    available_dates_per_boundary: dict[str, set[str]] = {key: set() for key in BOUNDARIES}
    ambiguous_dates_per_boundary: dict[str, set[str]] = {key: set() for key in BOUNDARIES}
    for (day, boundary, _security, _time_ms), candidate in boundary_candidates.items():
        candidate_rows_per_boundary[boundary] += candidate["row_count"]
        unambiguous = (
            len(candidate["sequence_values"]) == candidate["row_count"]
        )
        if unambiguous:
            available_dates_per_boundary[boundary].add(day)
        else:
            ambiguous_dates_per_boundary[boundary].add(day)
    for boundary in BOUNDARIES:
        unavailable = []
        for day in sorted(calendar):
            if day in available_dates_per_boundary[boundary]:
                continue
            reason = (
                "AMBIGUOUS_SEQUENCE_ONLY_IN_WINDOW"
                if day in ambiguous_dates_per_boundary[boundary]
                else "NO_QUALIFYING_ROW_IN_WINDOW"
            )
            unavailable.append({"execution_date": day, "reason": reason})
        boundary_results[boundary] = {
            "window_end_inclusive": "boundary + 00:01:00.000",
            "expected_trade_dates": len(calendar),
            "dates_with_qualifying_rows": len(available_dates_per_boundary[boundary]),
            "qualifying_row_count": int(candidate_rows_per_boundary[boundary]),
            "unavailable_dates": unavailable,
        }

    schema_ok = bool(file_records) and all(
        record["schema_match"] and record["status_code"] == "OK"
        for record in file_records
    )
    date_scope_ok = all(
        state["out_of_scope_date_rows"] == 0 and state["malformed_date_rows"] == 0
        for state in file_states
    )
    product_ok = all_index_values == {EXPECTED_PRODUCT_INDEX}
    sequence_ok = (
        diagnostics["duplicate_sequence_groups"] == 0
        and diagnostics["ambiguous_same_timestamp_groups"] == 0
        and sum(s["missing_sequence_rows"] for s in file_states) == 0
        and sum(s["invalid_sequence_rows"] for s in file_states) == 0
        and sum(s["nonmonotonic_sequence_transitions"] for s in file_states) == 0
    )
    timezone_status = _timezone_status(_load_attestations(attestations_path))
    coverage_evaluated = bool(calendar) and all(
        boundary in boundary_results for boundary in BOUNDARIES
    )
    systemic_ambiguity = not (
        month_file_identity_complete
        and schema_ok
        and date_scope_ok
        and product_ok
        and sequence_ok
        and not expected_contracts_missing
        and all(state["invalid_time_rows"] == 0 for state in file_states)
    )
    attestations = _load_attestations(attestations_path)
    license_status = attestations.get(
        "license_publication_boundary", "WAITING_FOR_JPX_LICENSE_CLARIFICATION"
    )
    independent_review = attestations.get("independent_review", "NOT_REVIEWED")
    final_pass = all(
        (
            OUTCOME_BLINDNESS_STATUS == "INTACT",
            month_file_identity_complete,
            schema_ok,
            date_scope_ok,
            product_ok,
            timezone_status["status"] == "ATTESTED_JST",
            sequence_ok,
            coverage_evaluated,
            not systemic_ambiguity,
            license_status == "RESOLVED",
            independent_review == "PASS",
        )
    )
    created = generated_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    aggregate_exec_dates = [day for day in all_execution_dates if day[:4] == "2025"]
    aggregate_trade_dates = [day for day in all_trade_dates if day[:4] == "2025"]
    return {
        "receipt_type": "JPX_DATACUBE_2025_SOURCE_QUALIFICATION",
        "receipt_version": 1,
        "generated_at_utc": created,
        "scope": {
            "provider": "JPX Market Innovation & Research / J-Quants DataCube",
            "dataset_family": "Financial Derivatives Information",
            "data_type": "Tick",
            "product": "Nikkei 225 mini",
            "expected_calendar_year": 2025,
            "research_line_outcome_access_status": OUTCOME_BLINDNESS_STATUS,
            "external_2025_market_quote_snippet_exposed": True,
            "target_datacube_2025_files_accessed": False,
            "quote_values_recorded_or_used": False,
            "2026_market_data_accessed": False,
            "raw_files_processed_locally": True,
        },
        "files": file_records,
        "file_completeness": {
            "expected_purchase_months": list(EXPECTED_MONTHS),
            "months_inferred_from_trade_date": months_seen,
            "month_to_filenames": dict(sorted(months_to_files.items())),
            "expected_month_count": 12,
            "raw_market_file_count": len(file_records),
            "all_twelve_month_files_present": month_file_identity_complete,
        },
        "schema_validation": {
            "expected_column_count": len(EXPECTED_HEADER),
            "header_fingerprint_recorded": True,
            "all_files_match_official_schema": schema_ok,
            "header_names_emitted": False,
        },
        "row_metadata": {
            "row_count": sum(int(record["row_count"]) for record in file_records),
            "execution_date_min": min(aggregate_exec_dates) if aggregate_exec_dates else None,
            "execution_date_max": max(aggregate_exec_dates) if aggregate_exec_dates else None,
            "trade_date_min": min(aggregate_trade_dates) if aggregate_trade_dates else None,
            "trade_date_max": max(aggregate_trade_dates) if aggregate_trade_dates else None,
            "index_type_values": sorted(all_index_values),
            "contract_month_counts": dict(sorted(contract_counts.items())),
            "expected_front_contract_months": list(EXPECTED_CONTRACTS_2025),
            "expected_front_contract_months_missing": expected_contracts_missing,
            "expected_front_contract_dates_present": len(all_expected_contract_dates_seen),
            "expected_front_contract_dates_unavailable": [
                day for day in sorted(calendar) if day not in all_expected_contract_dates_seen
            ],
            "sco_category_counts": dict(sorted(sco_counts.items())),
            "out_of_scope_date_rows_rejected": sum(
                s["out_of_scope_date_rows"] for s in file_states
            ),
            "malformed_date_rows": sum(s["malformed_date_rows"] for s in file_states),
        },
        "sequence_diagnostics": {
            **diagnostics,
            "missing_sequence_rows": sum(s["missing_sequence_rows"] for s in file_states),
            "invalid_sequence_rows": sum(s["invalid_sequence_rows"] for s in file_states),
            "nonmonotonic_sequence_transitions": sum(
                s["nonmonotonic_sequence_transitions"] for s in file_states
            ),
            "nonconsecutive_values_are_not_treated_as_missing": True,
        },
        "boundary_coverage": boundary_results,
        "semantics": {
            "displayed_clock_timezone": timezone_status,
            "sequence_rule": "JPX No is execution order ascending within trade_date/security_code; raw uniqueness is checked above.",
            "sequence_semantics_source": "https://dc.jpx-jquants.com/ja/spec/dataspec/fin_derivatives/tick/futures",
        },
        "gate_checks": {
            "outcome_blindness_integrity_preserved": OUTCOME_BLINDNESS_STATUS == "INTACT",
            "all_twelve_expected_month_files_present": month_file_identity_complete,
            "sha256_recorded_for_every_input_file": len(file_records) == len(files),
            "schema_matches": schema_ok,
            "index_type_matches_nikkei_225_mini_19": product_ok,
            "no_2024_or_2026_execution_or_trade_dates": date_scope_ok,
            "timezone_semantics_confirmed": timezone_status["status"] == "ATTESTED_JST",
            "sequence_semantics_and_sample_order_validated": sequence_ok,
            "required_boundary_coverage_evaluated": coverage_evaluated,
            "systemic_ambiguity": systemic_ambiguity,
            "license_publication_boundary": license_status,
            "independent_review": independent_review,
            "packet_a_pass": final_pass,
        },
        "outcome_blind_guards": {
            "row_level_values_emitted": False,
            "numeric_outcomes_calculated": False,
            "market_direction_calculated": False,
            "statistical_relationships_calculated": False,
            "strategy_performance_calculated": False,
            "extreme_dates_searched": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--calendar", type=Path, default=CALENDAR_PATH)
    parser.add_argument("--attestations", type=Path)
    args = parser.parse_args()
    if not args.raw_dir.is_dir():
        parser.error("--raw-dir must be a local directory")
    output = args.output or args.raw_dir / "SOURCE_QUALIFICATION_RECEIPT.json"
    receipt = build_receipt(
        args.raw_dir,
        calendar_path=args.calendar,
        attestations_path=args.attestations,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"receipt_written={output}")
    print(f"packet_a_pass={receipt['gate_checks']['packet_a_pass']}")
    return 0 if receipt["gate_checks"]["packet_a_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
