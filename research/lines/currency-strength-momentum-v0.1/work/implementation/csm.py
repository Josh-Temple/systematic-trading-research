"""Outcome-blind deterministic core for the proposed CSM-002 screen.

The module has no network client and accepts only a source-lock-described CSV
adapter. The research contract remains proposed, so a market run cannot pass
the gate until a later freeze and Integrator receipt authorize it.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import random
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SPEC_ID = "SPEC-CSM-002-v01"
SPEC_GIT_BLOB_SHA1 = "a073e77dec14337ee20609ed6136e50a8c1e76e2"
SPEC_SHA256 = "e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90"
HYPOTHESIS_ID = "HYP-CSM-002"
CURRENCIES = ("AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "USD")
NON_EUR_CURRENCIES = tuple(c for c in CURRENCIES if c != "EUR")
EXPECTED_SERIES_BY_CURRENCY = {
    c: f"D.{c}.EUR.SP00.A" for c in NON_EUR_CURRENCIES
}
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


def validate_series_identity(source_lock: Mapping[str, Any]) -> None:
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


def validate_gate_receipt(
    receipt: Mapping[str, Any], source_lock: Mapping[str, Any],
    *, expected_file_hashes: Mapping[str, str] | None = None,
    expected_environment_sha256: str | None = None,
) -> None:
    """Fail closed; no current receipt can pass against this proposed contract."""
    validate_series_identity(source_lock)
    if receipt.get("gate_status") != "PASS":
        raise GateError("market-outcome gate is not PASS")
    if receipt.get("human_freeze_status") != "FROZEN":
        raise GateError("human has not frozen the exact research contract")
    if receipt.get("market_outcome_access_authorized") is not True:
        raise GateError("market-outcome access is not explicitly authorized")
    if receipt.get("data_role") != "EXPLORATORY_DISCOVERY":
        raise GateError("dataset role mismatch")
    if receipt.get("spec_id") != SPEC_ID:
        raise GateError("gate SPEC identity mismatch")
    if receipt.get("spec_git_blob_sha1") != SPEC_GIT_BLOB_SHA1:
        raise GateError("gate SPEC bytes differ from implementation target")
    if receipt.get("hypothesis_id") != HYPOTHESIS_ID:
        raise GateError("gate hypothesis identity mismatch")
    if receipt.get("source_lock_id") != source_lock.get("id"):
        raise GateError("gate source-lock identity mismatch")
    required_text = (
        "human_contract_decision_id",
        "spec_sha256",
        "source_transport",
        "source_lock_sha256",
        "unit_status_map_sha256",
        "expected_calendar_sha256",
        "raw_capture_process_id",
        "access_ledger_id",
        "code_commit",
        "synthetic_test_log_sha256",
        "environment_identity_sha256",
        "independent_audit_id",
        "integrator_gate_id",
        "run_id",
        "outcome_access_owner",
    )
    for field in required_text:
        value = receipt.get(field)
        if not isinstance(value, str) or not value.strip():
            raise GateError(f"gate receipt missing {field}")
    for field in ("spec_sha256", "source_lock_sha256", "unit_status_map_sha256", "expected_calendar_sha256",
                  "synthetic_test_log_sha256", "environment_identity_sha256"):
        value = receipt[field]
        if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value.lower()):
            raise GateError(f"gate receipt has invalid {field}")
    if receipt.get("spec_sha256") != SPEC_SHA256:
        raise GateError("gate SPEC SHA-256 differs from proposed exact bytes")
    if receipt.get("source_series_keys") != list(EXPECTED_SERIES_BY_CURRENCY.values()):
        raise GateError("gate series keys mismatch")
    if receipt.get("source_transport") != source_lock.get("source_transport"):
        raise GateError("gate source transport does not match source lock")
    if receipt.get("source_lock_sha256") != sha256_bytes(canonical_json_bytes(source_lock)):
        raise GateError("gate source-lock content identity mismatch")
    status_unit_hash = sha256_bytes(canonical_json_bytes({
        "unit_by_currency": source_lock.get("unit_by_currency"),
        "status_policy": source_lock.get("status_policy"),
    }))
    if receipt.get("unit_status_map_sha256") != status_unit_hash:
        raise GateError("gate unit/status identity mismatch")
    expected_time_range = {
        "source_start": SOURCE_START,
        "source_end": SOURCE_END,
        "target_start": TARGET_START,
        "target_end": TARGET_END,
    }
    if receipt.get("time_range") != expected_time_range:
        raise GateError("gate time-range identity mismatch")
    if expected_file_hashes is not None and receipt.get("code_file_hashes") != dict(expected_file_hashes):
        raise GateError("gate code/config/test identity mismatch")
    if (expected_environment_sha256 is not None
            and receipt.get("environment_identity_sha256") != expected_environment_sha256):
        raise GateError("gate environment identity mismatch")
    if receipt.get("full_history_run_authorized") is not True:
        raise GateError("full-history execution is not explicitly authorized")


def validate_capture_manifest(
    manifest: Mapping[str, Any], raw_bytes: bytes, source_lock: Mapping[str, Any]
) -> None:
    if manifest.get("capture_status") != "CAPTURED":
        raise GateError("raw-capture preflight is not complete")
    if manifest.get("source_lock_id") != source_lock.get("id"):
        raise GateError("raw-capture source identity mismatch")
    if manifest.get("source_lock_sha256") != sha256_bytes(canonical_json_bytes(source_lock)):
        raise GateError("raw-capture source-lock content identity mismatch")
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


def _normalized_source_rows(
    reader: csv.DictReader, source_lock: Mapping[str, Any]
) -> Iterable[dict[str, Any]]:
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
    previous_day: date | None = None
    for row in rows:
        day = parse_iso_date(row.get("date"), field="date")
        if previous_day is not None and day < previous_day:
            raise DataError("input dates are not ordered")
        previous_day = day
        currency = str(row.get("currency", ""))
        if currency not in NON_EUR_CURRENCIES:
            raise DataError("unexpected source currency; EUR is synthetic q=1")
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


def parse_source_csv(raw_bytes: bytes, source_lock: Mapping[str, Any]) -> QuoteTable:
    validate_series_identity(source_lock)
    try:
        text = raw_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise DataError("source CSV is not UTF-8") from exc
    reader = csv.DictReader(text.splitlines())
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
        for month in needed_months:
            raw_day = month_end_dates.get(month)
            if raw_day is None:
                reason = f"NO_EXPECTED_ENDPOINT:{month}"
                dates.append(None)
                continue
            day = parse_iso_date(raw_day, field=f"month_end_dates[{month}]")
            if day.strftime("%Y-%m") != month:
                raise DataError("calendar endpoint does not belong to its month")
            dates.append(day)
            endpoint_problem = _endpoint_reason(table, day, month)
            if endpoint_problem and reason is None:
                reason = endpoint_problem

        start_day, formation_day, target_day = dates
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
            )
        )
    return tuple(events)


def event_ledger_payload(events: Sequence[SignalEvent]) -> dict[str, Any]:
    return {
        "record_type": "PRE_OUTCOME_EVENT_LEDGER",
        "spec_id": SPEC_ID,
        "data_role": "EXPLORATORY_DISCOVERY",
        "temporal_claim": "REFERENCE_ASSOCIATION_ONLY",
        "events": [asdict(event) for event in events],
    }


def persist_event_ledger(events: Sequence[SignalEvent], path: Path) -> str:
    payload = canonical_json_bytes(event_ledger_payload(events))
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(payload)
    except FileExistsError as exc:
        raise GateError("event-ledger path already exists; preserve the attempt") from exc
    return sha256_bytes(payload)


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
        if start_prices is None or end_prices is None:
            raise DataError("READY event target became unavailable")
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
    for event in events:
        if event.status != "READY":
            key = event.skip_reason or "UNKNOWN_SKIP"
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


def validate_calendar_document(calendar_doc: Mapping[str, Any]) -> None:
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


def validate_config(config: Mapping[str, Any]) -> None:
    expected = {
        "spec_id": SPEC_ID,
        "spec_git_blob_sha1": SPEC_GIT_BLOB_SHA1,
        "spec_sha256": SPEC_SHA256,
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
        "freeze_status": "PROPOSED_NOT_FROZEN",
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


def _block_network_audit(event: str, args: tuple[Any, ...]) -> None:
    if event.startswith(("socket.connect", "socket.getaddrinfo", "subprocess.Popen", "os.system")):
        raise PermissionError("network and subprocess access are disabled during calculation")


def environment_snapshot() -> dict[str, str]:
    return {
        "python_version": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "module_sha256": sha256_file(Path(__file__)),
        "config_sha256": sha256_file(CONFIG_PATH),
    }


def environment_identity_sha256(snapshot: Mapping[str, str] | None = None) -> str:
    return sha256_bytes(canonical_json_bytes(snapshot or environment_snapshot()))


def _write_json_exclusive(path: Path, value: Any) -> str:
    payload = canonical_json_bytes(value)
    try:
        with path.open("xb") as stream:
            stream.write(payload)
    except FileExistsError as exc:
        raise GateError("output file already exists; do not reuse an attempt directory") from exc
    return sha256_bytes(payload)


def run_locked_calculation(args: argparse.Namespace) -> int:
    """Production path. Gate and capture checks precede data load/output."""
    config = _read_json(CONFIG_PATH)
    validate_config(config)
    source_lock = _read_json(Path(args.source_lock))
    gate = _read_json(Path(args.gate_receipt))
    test_log_path = Path(__file__).with_name("TEST_LOG.txt")
    test_path = Path(__file__).with_name("test_csm.py")
    expected_file_hashes = {
        "csm.py": sha256_file(Path(__file__)),
        "config.json": sha256_file(CONFIG_PATH),
        "test_csm.py": sha256_file(test_path),
    }
    validate_gate_receipt(
        gate, source_lock,
        expected_file_hashes=expected_file_hashes,
        expected_environment_sha256=environment_identity_sha256(),
    )
    if sha256_file(test_log_path) != gate.get("synthetic_test_log_sha256"):
        raise GateError("synthetic test-log identity mismatch")
    calendar_path = Path(args.expected_calendar)
    calendar_bytes = calendar_path.read_bytes()
    try:
        calendar_doc = json.loads(calendar_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateError("calendar artifact is not valid UTF-8 JSON") from exc
    if not isinstance(calendar_doc, dict):
        raise GateError("calendar artifact is not a JSON object")
    validate_calendar_document(calendar_doc)
    raw_bytes = Path(args.normalized_csv).read_bytes()
    capture = _read_json(Path(args.capture_manifest))
    validate_capture_manifest(capture, raw_bytes, source_lock)
    calendar_hash = sha256_bytes(calendar_bytes)
    if gate["expected_calendar_sha256"] != calendar_hash:
        raise GateError("gate calendar identity mismatch")
    if capture["access_ledger_id"] != gate["access_ledger_id"]:
        raise GateError("capture and gate access-ledger identity mismatch")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    raw_hash = sha256_bytes(raw_bytes)
    source_lock_hash = sha256_bytes(canonical_json_bytes(source_lock))
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
        "source_lock_file_sha256": sha256_file(Path(args.source_lock)),
        "calendar_sha256": calendar_hash,
        "code_sha256": expected_file_hashes["csm.py"],
        "config_sha256": expected_file_hashes["config.json"],
        "test_code_sha256": expected_file_hashes["test_csm.py"],
        "test_log_sha256": sha256_file(test_log_path),
    }
    _write_json_exclusive(output_dir / "attempt-start.json", start_receipt)

    stage = "SOURCE_PARSE"
    ledger_hash: str | None = None
    primary_hash: str | None = None
    try:
        sys.addaudithook(_block_network_audit)
        table = parse_source_csv(raw_bytes, source_lock)
        validate_observed_date_bounds(table)
        target_months = month_range(TARGET_START, TARGET_END)
        events = build_signal_events(target_months, calendar_doc["month_end_dates"], table)

        stage = "EVENT_LEDGER"
        ledger_path = output_dir / "event-ledger.json"
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
        primary_hash = _write_json_exclusive(output_dir / "primary-metrics.json", primary_payload)

        stage = "BOOTSTRAP"
        bootstrap = moving_block_bootstrap(outcomes)
        scientific_status, decision = classify_result(
            mean_bps=metrics.mean_bps or Decimal(0),
            lower_95_bps=bootstrap.lower_95 * Decimal(10_000),
            eligible_count=metrics.eligible_count,
            scheduled_count=metrics.scheduled_count,
        )
        inference_hash = _write_json_exclusive(output_dir / "inference.json", {
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
            "source_lock_file_sha256": sha256_file(Path(args.source_lock)),
            "calendar_sha256": calendar_hash,
            "raw_snapshot_sha256": raw_hash,
            "event_ledger_sha256": ledger_hash,
            "primary_metrics_sha256": primary_hash,
            "inference_sha256": inference_hash,
            "network_access": "DISABLED_BY_PROCESS_AUDIT_HOOK",
        }
        _write_json_exclusive(output_dir / "run-receipt.json", {
            "run_id": gate["run_id"],
            "data_role": gate["data_role"],
            "execution_status": "SUCCESS",
            "evidence_validity": "VALID",
            "scientific_status": scientific_status,
            "decision": decision,
            "runtime_and_file_snapshot": runtime,
            "access_ledger_id": gate["access_ledger_id"],
            "market_outcome_access_before_gate": False,
        })
        print("execution_status=SUCCESS")
        print(f"scientific_status={scientific_status}")
        return 0
    except (GateError, DataError, OSError, ArithmeticError) as exc:
        _write_json_exclusive(output_dir / "attempt-status.json", {
            "run_id": gate["run_id"],
            "execution_status": "FAILED",
            "evidence_validity": "PARTIAL",
            "scientific_status": "NOT_APPLICABLE",
            "stage": stage,
            "failure_class": exc.__class__.__name__,
            "access_ledger_id": gate["access_ledger_id"],
            "raw_snapshot_sha256": raw_hash,
            "source_lock_sha256": source_lock_hash,
            "calendar_sha256": calendar_hash,
            "event_ledger_sha256": ledger_hash,
            "primary_metrics_sha256": primary_hash,
            "do_not_reuse_or_retry_without_new_authorization": True,
        })
        print(f"execution_status=FAILED stage={stage}", file=sys.stderr)
        print(f"failure_class={exc.__class__.__name__}", file=sys.stderr)
        return 2


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fixed CSM-002 deterministic screen")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="authorized full-history run only")
    run.add_argument("--normalized-csv", required=True)
    run.add_argument("--source-lock", required=True)
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
