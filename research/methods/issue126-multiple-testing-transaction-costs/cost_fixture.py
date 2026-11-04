"""Issue #126: synthetic-only cost accounting and outcome-blind selection.

No broker, market loader, forecasting, or live execution entrypoint.
Price and quantity produce synthetic quote-currency PnL; fees use same unit.
"""
from dataclasses import dataclass
from datetime import datetime
from math import isfinite


class EvidenceHold(ValueError):
    """Missing, inconsistent or non-synthetic evidence."""


def valid_number(name, value, *, positive=False, signed=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EvidenceHold(f"{name}: numeric required")
    try:
        value = float(value)
    except (OverflowError, ValueError) as exc:
        raise EvidenceHold(f"{name}: unrepresentable") from exc
    if not isfinite(value) or (not signed and value < 0) or (positive and value == 0):
        raise EvidenceHold(f"{name}: invalid or nonfinite")
    return value


@dataclass(frozen=True)
class RoundTrip:
    side: int
    quantity: float
    entry_mid: float
    exit_mid: float
    entry_half_spread: float = 0
    exit_half_spread: float = 0
    entry_slippage: float = 0
    exit_slippage: float = 0
    entry_impact: float = 0
    exit_impact: float = 0
    entry_fee: float = 0
    exit_fee: float = 0
    funding_charge: float = 0


def roundtrip_pnl(t: RoundTrip):
    """Full two-sided synthetic fill, all costs adverse and nonnegative.

    Midpoint-to-midpoint gross and prices of spread/slippage/impact are
    disjoint cost components. Never add them to already-executed bid/ask
    prices: that would double count. No partial fills or FX conversion.
    """
    if type(t.side) is not int or t.side not in (-1, 1):
        raise EvidenceHold("side: integer +1 or -1 required")
    qty = valid_number("quantity", t.quantity)
    entry = valid_number("entry_mid", t.entry_mid, positive=True)
    exit_ = valid_number("exit_mid", t.exit_mid, positive=True)
    prices = ("entry_half_spread", "exit_half_spread", "entry_slippage",
              "exit_slippage", "entry_impact", "exit_impact")
    p = {k: valid_number(k, getattr(t, k)) for k in prices}
    entry_fee = valid_number("entry_fee", t.entry_fee)
    exit_fee = valid_number("exit_fee", t.exit_fee)
    funding = valid_number("funding_charge", t.funding_charge)
    if qty == 0 and (entry_fee or exit_fee or funding):
        raise EvidenceHold("flat path cannot have fill fees or funding")
    gross = t.side * qty * (exit_ - entry)
    spread = qty * (p["entry_half_spread"] + p["exit_half_spread"])
    slippage = qty * (p["entry_slippage"] + p["exit_slippage"])
    impact = qty * (p["entry_impact"] + p["exit_impact"])
    fees = entry_fee + exit_fee
    cost = spread + slippage + impact + fees + funding
    net = gross - cost
    if not all(isfinite(x) for x in (gross, spread, slippage, impact, fees, funding, cost, net)):
        raise EvidenceHold("arithmetic overflow")
    return {"gross": gross, "spread": spread, "slippage": slippage,
            "impact": impact, "fees": fees, "funding": funding,
            "total_cost": cost, "net": net}


def validate_synthetic_bars(rows):
    if not rows:
        raise EvidenceHold("empty series")
    last = None
    for stamp, price in rows:
        try:
            dt = datetime.fromisoformat(stamp)
        except (TypeError, ValueError) as exc:
            raise EvidenceHold("invalid timestamp") from exc
        if dt.tzinfo is None or dt.utcoffset() is None:
            raise EvidenceHold("timestamp must be timezone-aware")
        if last is not None and dt <= last:
            raise EvidenceHold("duplicate or non-increasing timestamp")
        last = dt
        valid_number("price", price, positive=True)


@dataclass(frozen=True)
class SelectionManifest:
    source_kind: str
    selection_sample_id: str
    evaluation_sample_id: str
    candidate_ids: tuple[str, ...]


def select_training_winner(training_scores, manifest: SelectionManifest):
    """No evaluation outcomes enter this interface, even as a parameter."""
    if manifest.source_kind != "SYNTHETIC":
        raise EvidenceHold("non-synthetic provenance")
    if (not manifest.selection_sample_id or not manifest.evaluation_sample_id
            or manifest.selection_sample_id == manifest.evaluation_sample_id):
        raise EvidenceHold("invalid sample identity")
    ids = manifest.candidate_ids
    if (not ids or len(ids) != len(set(ids))
            or any(not isinstance(i, str) or not i for i in ids)):
        raise EvidenceHold("invalid candidate registry")
    if set(training_scores) != set(ids):
        raise EvidenceHold("missing or extra candidate")
    scores = {i: valid_number(f"training_score:{i}", training_scores[i], signed=True) for i in ids}
    return max(ids, key=lambda i: scores[i])  # ties: manifest order
