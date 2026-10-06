from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Iterable, Mapping, Sequence


class Sentiment(str, Enum):
    APPRECIATION = "APPRECIATION"
    DEPRECIATION = "DEPRECIATION"
    UNCHANGED = "UNCHANGED"
    NOT_MENTIONED = "NOT_MENTIONED"
    INSUFFICIENT = "INSUFFICIENT"


class Action(str, Enum):
    LONG = "LONG_EURJPY"
    SHORT = "SHORT_EURJPY"
    NO_TRADE = "NO_TRADE"


@dataclass(frozen=True)
class Quote:
    timestamp: datetime
    bid: float
    ask: float

    def __post_init__(self) -> None:
        if self.timestamp.tzinfo is None:
            raise ValueError("quote timestamp must be timezone-aware")
        if not (math.isfinite(self.bid) and math.isfinite(self.ask)):
            raise ValueError("quote prices must be finite")
        if self.bid <= 0 or self.ask <= 0:
            raise ValueError("quote prices must be positive")
        if self.bid > self.ask:
            raise ValueError("bid must not exceed ask")


def parse_iso_aware(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return dt


def validate_headline_record(record: Mapping[str, object], cutoff: datetime) -> None:
    if cutoff.tzinfo is None:
        raise ValueError("cutoff must be timezone-aware")
    for key in ("record_id", "gdelt_seen_at", "source_domain", "title", "url"):
        if not isinstance(record.get(key), str) or not str(record[key]).strip():
            raise ValueError(f"missing or invalid {key}")
    seen = parse_iso_aware(str(record["gdelt_seen_at"]))
    if seen > cutoff:
        raise ValueError("post-cutoff headline is forbidden")


def dedupe_exact_url(records: Sequence[Mapping[str, object]]) -> list[Mapping[str, object]]:
    """Deduplicate exact URLs only. Near-duplicate title policy remains a source-contract decision."""
    out: list[Mapping[str, object]] = []
    seen: set[str] = set()
    for record in records:
        url = str(record.get("url", "")).strip()
        if not url:
            raise ValueError("record missing url")
        if url not in seen:
            seen.add(url)
            out.append(record)
    return out


def validate_classification(row: Mapping[str, object]) -> None:
    if not isinstance(row.get("record_id"), str) or not str(row["record_id"]).strip():
        raise ValueError("missing record_id")
    for currency in ("EUR", "JPY"):
        try:
            Sentiment(str(row[currency]))
        except (KeyError, ValueError) as exc:
            raise ValueError(f"invalid {currency} sentiment") from exc


def _as_sentiment(raw: Sentiment | str) -> Sentiment:
    return raw if isinstance(raw, Sentiment) else Sentiment(raw)


def _as_action(raw: Action | str) -> Action:
    return raw if isinstance(raw, Action) else Action(raw)


def currency_score(values: Iterable[Sentiment | str]) -> float:
    app = 0
    dep = 0
    for raw in values:
        value = _as_sentiment(raw)
        if value is Sentiment.APPRECIATION:
            app += 1
        elif value is Sentiment.DEPRECIATION:
            dep += 1
    return math.log1p(app) - math.log1p(dep)


def daily_scores(classifications: Sequence[Mapping[str, object]]) -> tuple[float, float]:
    eur: list[Sentiment] = []
    jpy: list[Sentiment] = []
    seen_ids: set[str] = set()
    for row in classifications:
        validate_classification(row)
        rid = str(row["record_id"])
        if rid in seen_ids:
            raise ValueError("duplicate classification record_id")
        seen_ids.add(rid)
        eur.append(_as_sentiment(str(row["EUR"])))
        jpy.append(_as_sentiment(str(row["JPY"])))
    return currency_score(eur), currency_score(jpy)


def sign(value: float, atol: float = 1e-15) -> int:
    if abs(value) <= atol:
        return 0
    return 1 if value > 0 else -1


def pair_action(s_eur: float, s_jpy: float) -> Action:
    se = sign(s_eur)
    sj = sign(s_jpy)
    if se == sj:
        return Action.NO_TRADE
    if s_eur > s_jpy:
        return Action.LONG
    if s_eur < s_jpy:
        return Action.SHORT
    return Action.NO_TRADE


def validate_signal_timing(cutoff: datetime, issued_at: datetime, entry_target: datetime) -> None:
    for name, value in (("cutoff", cutoff), ("issued_at", issued_at), ("entry_target", entry_target)):
        if value.tzinfo is None:
            raise ValueError(f"{name} must be timezone-aware")
    if issued_at < cutoff:
        raise ValueError("issued_at cannot precede information cutoff")
    if issued_at >= entry_target:
        raise ValueError("late issuance is not scoreable")


def select_quote_at_or_after(
    quotes: Sequence[Quote], target: datetime, max_delay_seconds: int = 60
) -> Quote:
    if target.tzinfo is None:
        raise ValueError("target must be timezone-aware")
    if max_delay_seconds < 0:
        raise ValueError("max_delay_seconds must be nonnegative")
    eligible = [q for q in quotes if q.timestamp >= target]
    if not eligible:
        raise ValueError("no quote at or after target")
    quote = min(eligible, key=lambda q: q.timestamp)
    if quote.timestamp - target > timedelta(seconds=max_delay_seconds):
        raise ValueError("nearest quote exceeds tolerance")
    return quote


def executable_return_bps(action: Action | str, entry: Quote | None, exit_: Quote | None) -> float:
    act = _as_action(action)
    if act is Action.NO_TRADE:
        return 0.0
    if entry is None or exit_ is None:
        raise ValueError("entry and exit quotes required for a trade")
    if act is Action.LONG:
        return 10_000.0 * math.log(exit_.bid / entry.ask)
    return 10_000.0 * math.log(entry.bid / exit_.ask)


def midpoint_return_bps(action: Action | str, entry: Quote | None, exit_: Quote | None) -> float:
    act = _as_action(action)
    if act is Action.NO_TRADE:
        return 0.0
    if entry is None or exit_ is None:
        raise ValueError("entry and exit quotes required for a trade")
    entry_mid = (entry.bid + entry.ask) / 2.0
    exit_mid = (exit_.bid + exit_.ask) / 2.0
    raw = 10_000.0 * math.log(exit_mid / entry_mid)
    return raw if act is Action.LONG else -raw


def validate_model_identity(expected: str, observed: str) -> None:
    if not expected or not observed:
        raise ValueError("model identity must be non-empty")
    if expected != observed:
        raise ValueError("model identity changed; cohort must stop/version")


def canonical_json_bytes(record: Mapping[str, object]) -> bytes:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha256(record: Mapping[str, object]) -> str:
    return hashlib.sha256(canonical_json_bytes(record)).hexdigest()
