"""Independent synthetic oracle for the frozen CSM-002 contract.

This file uses hand-authored toy values only. It has no network, file, or market-data
input path and prints assertions only, never synthetic return magnitudes.
"""
from datetime import date, timedelta
from decimal import Decimal, localcontext
from fractions import Fraction
from math import ceil
import argparse
import hashlib
import json
import random

CURRENCIES = ("AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "USD")
BLOCK = 12
REPLICATES = 10_000
SEED = 20_261_001


def q_vector(overrides=None):
    values = {ccy: Decimal("1") for ccy in CURRENCIES}
    values.update({key: Decimal(str(value)) for key, value in (overrides or {}).items()})
    return values


def growth_ratios(old, new):
    return {ccy: Fraction(old[ccy]) / Fraction(new[ccy]) for ccy in CURRENCIES}


def choose_extremes(old, new):
    growth = growth_ratios(old, new)
    high = max(growth.values())
    low = min(growth.values())
    winners = [ccy for ccy in CURRENCIES if growth[ccy] == high]
    losers = [ccy for ccy in CURRENCIES if growth[ccy] == low]
    if len(winners) != 1 or len(losers) != 1:
        return None, None
    return winners[0], losers[0]


def pair_quote(prices, base, quote):
    return Fraction(prices[quote]) / Fraction(prices[base])


def pair_log_return(start, end, base, quote):
    ratio = pair_quote(end, base, quote) / pair_quote(start, base, quote)
    with localcontext() as ctx:
        ctx.prec = 50
        return (Decimal(ratio.numerator) / Decimal(ratio.denominator)).ln()


def transform_numeraire(prices, numeraire):
    ref = Fraction(prices[numeraire])
    return {ccy: Fraction(prices[ccy]) / ref for ccy in CURRENCIES}


def type7(values, probability):
    ordered = sorted(values)
    if not ordered or not Decimal(0) <= probability <= Decimal(1):
        raise ValueError("invalid type-7 input")
    h = Decimal(len(ordered) - 1) * probability
    lo = int(h)
    hi = min(lo + 1, len(ordered) - 1)
    frac = h - Decimal(lo)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * frac


def circular_sample(grid, rng):
    if not grid:
        raise ValueError("empty grid")
    sample = []
    for _ in range(ceil(len(grid) / BLOCK)):
        start = rng.randrange(len(grid))
        sample.extend(grid[(start + j) % len(grid)] for j in range(BLOCK))
    return tuple(sample[:len(grid)])


def bootstrap(grid):
    rng = random.Random(SEED)
    means = []
    for _ in range(REPLICATES):
        valid = [item for item in circular_sample(grid, rng) if item is not None]
        if not valid:
            raise ValueError("zero-valid replicate")
        with localcontext() as ctx:
            ctx.prec = 50
            means.append(sum(valid, Decimal(0)) / Decimal(len(valid)))
    return (
        type7(means, Decimal("0.025")),
        type7(means, Decimal("0.975")),
        type7(means, Decimal("0.5")),
        len(means),
    )


def classify(mean_bps, lower_bps, eligible, scheduled):
    if scheduled <= 0 or eligible < 0 or eligible > scheduled:
        raise ValueError("invalid counts")
    if eligible < 120 or Decimal(eligible) / Decimal(scheduled) < Decimal("0.80"):
        return "INSUFFICIENT_EVIDENCE", "HOLD"
    if mean_bps <= 0:
        return "NOT_SUPPORTED", "DEPRIORITIZE"
    if lower_bps <= 0:
        return "INCONCLUSIVE", "HOLD"
    return "PROMISING_EXPLORATORY", "ADVANCE_TO_SEPARATE_ECONOMIC_SCREEN_DESIGN"


def month_shift(month, offset):
    year, mon = map(int, month.split("-"))
    ordinal = year * 12 + mon - 1 + offset
    new_year, zero_mon = divmod(ordinal, 12)
    return f"{new_year:04d}-{zero_mon + 1:02d}"


def month_range(start, end):
    out = []
    cur = start
    while cur <= end:
        out.append(cur)
        cur = month_shift(cur, 1)
    return out


def check_pair_algebra_and_numeraire():
    old = q_vector()
    formation = q_vector({
        "AUD": "0.90", "CAD": "1.20", "CHF": "1.10", "EUR": "1.00",
        "GBP": "0.80", "JPY": "1.40", "NZD": "0.95", "USD": "0.70",
    })
    growth = growth_ratios(old, formation)
    winner, loser = choose_extremes(old, formation)
    assert winner == "USD" and loser == "JPY"
    directed = {
        (a, b): growth[a] / growth[b]
        for a in CURRENCIES for b in CURRENCIES if a != b
    }
    maximum = max(directed.values())
    winners = [pair for pair, value in directed.items() if value == maximum]
    assert len(directed) == 56
    assert winners == [(winner, loser)]
    assert maximum == growth[winner] / growth[loser]

    target = q_vector({"USD": "0.60", "JPY": "1.60", "EUR": "1.02"})
    y = pair_log_return(formation, target, winner, loser)
    with localcontext() as ctx:
        ctx.prec = 50
        score_y = (
            -(target[winner] / formation[winner]).ln()
            + (target[loser] / formation[loser]).ln()
        )
        assert abs(y - score_y) < Decimal("1e-45")

    base_simple = Fraction(formation[winner]) / Fraction(target[winner]) - 1
    quote_simple = Fraction(formation[loser]) / Fraction(target[loser]) - 1
    pair_simple = (
        pair_quote(target, winner, loser) / pair_quote(formation, winner, loser) - 1
    )
    assert pair_simple == (1 + base_simple) / (1 + quote_simple) - 1
    assert pair_simple != base_simple - quote_simple

    old_cross = transform_numeraire(old, "CAD")
    formation_cross = transform_numeraire(formation, "CAD")
    cross_growth = growth_ratios(old_cross, formation_cross)
    assert choose_extremes(old_cross, formation_cross) == (winner, loser)
    assert all(
        cross_growth[c] == growth[c] / growth["CAD"] for c in CURRENCIES
    )


def check_eur_usd_direction_and_exact_ties():
    old = q_vector()
    eur_wins = q_vector({
        "AUD": "1.10", "CAD": "1.20", "CHF": "1.30", "GBP": "1.40",
        "JPY": "1.50", "NZD": "1.60", "USD": "2.00",
    })
    assert choose_extremes(old, eur_wins) == ("EUR", "USD")
    later = q_vector({"USD": "2.20"})
    eur_usd = pair_quote(eur_wins, "EUR", "USD")
    later_eur_usd = pair_quote(later, "EUR", "USD")
    assert later_eur_usd > eur_usd
    assert pair_log_return(eur_wins, later, "EUR", "USD") > 0

    usd_wins = q_vector({
        "AUD": "1.20", "CAD": "1.10", "CHF": "1.08", "GBP": "1.04",
        "JPY": "1.03", "NZD": "1.02", "USD": "0.50",
    })
    assert choose_extremes(old, usd_wins)[0] == "USD"

    tied = q_vector({"AUD": "0.50", "CAD": "0.500"})
    assert choose_extremes(old, tied) == (None, None)


def check_calendar_slots_and_causality():
    months = month_range("2010-01", "2026-09")
    assert len(months) == 201
    assert months[0] == "2010-01" and months[-1] == "2026-09"
    target = "2020-03"
    required = (month_shift(target, -2), month_shift(target, -1), target)
    assert required == ("2020-01", "2020-02", "2020-03")
    available_endpoints = {"2020-01", "2020-03"}
    assert any(month not in available_endpoints for month in required)
    scheduled_targets = ("2020-01", "2020-02", "2020-03")
    assert len(scheduled_targets) == 3
    expected_february_endpoint = date.fromisoformat("2020-02-28")
    observed_neighbor = date.fromisoformat("2020-02-27")
    assert expected_february_endpoint != observed_neighbor

    old = q_vector()
    formation = q_vector({"AUD": "0.8", "USD": "1.4", "JPY": "1.2"})
    before = choose_extremes(old, formation)
    wildly_changed_future = q_vector({"AUD": "100", "USD": "0.001", "JPY": "50"})
    after = choose_extremes(old, formation)
    assert before == after
    assert wildly_changed_future != formation


def check_bootstrap_and_decision_boundaries():
    values = [Decimal(1), Decimal(2), Decimal(4), Decimal(8)]
    assert type7(values, Decimal("0.5")) == Decimal(3)
    assert type7(values, Decimal("0.25")) == Decimal("1.75")

    grid14 = tuple(None if i == 4 else Decimal(i) for i in range(14))
    rng = random.Random(SEED)
    starts = [rng.randrange(len(grid14)) for _ in range(ceil(len(grid14) / BLOCK))]
    assert starts == [3, 5]
    sample = circular_sample(grid14, random.Random(SEED))
    assert len(sample) == len(grid14)
    assert sample.count(None) == 1

    grid = tuple(
        None if i in (4, 17) else Decimal(i - 10) / Decimal(10)
        for i in range(24)
    )
    result1 = bootstrap(grid)
    result2 = bootstrap(grid)
    assert result1 == result2
    assert result1[3] == REPLICATES
    try:
        bootstrap((None,) * 24)
    except ValueError as exc:
        assert "zero-valid" in str(exc)
    else:
        raise AssertionError("all-missing bootstrap must fail closed")

    assert classify(Decimal(10), Decimal(5), 119, 150) == ("INSUFFICIENT_EVIDENCE", "HOLD")
    assert classify(Decimal(10), Decimal(5), 120, 151) == ("INSUFFICIENT_EVIDENCE", "HOLD")
    assert classify(Decimal(0), Decimal(-1), 120, 150) == ("NOT_SUPPORTED", "DEPRIORITIZE")
    assert classify(Decimal(1), Decimal(0), 120, 150) == ("INCONCLUSIVE", "HOLD")
    assert classify(Decimal(1), Decimal("0.01"), 120, 150) == (
        "PROMISING_EXPLORATORY", "ADVANCE_TO_SEPARATE_ECONOMIC_SCREEN_DESIGN"
    )


def easter_sunday(year):
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def check_calendar_file(path, source_lock_path):
    raw = path.read_bytes()
    doc = json.loads(raw.decode("utf-8"))
    lock = json.loads(source_lock_path.read_text(encoding="utf-8"))
    identity = lock["calendar"]
    assert doc["calendar_id"] == identity["id"]
    assert doc["range_start_inclusive"] == identity["range_start_inclusive"]
    assert doc["range_end_inclusive"] == identity["range_end_inclusive"]
    lower = date.fromisoformat(doc["range_start_inclusive"])
    upper = date.fromisoformat(doc["range_end_inclusive"])
    closures = set()
    for year in range(lower.year, upper.year + 1):
        easter = easter_sunday(year)
        closures.update({
            date(year, 1, 1), easter - timedelta(days=2), easter + timedelta(days=1),
            date(year, 5, 1), date(year, 12, 25), date(year, 12, 26),
        })
    expected = []
    day = lower
    while day <= upper:
        if day.weekday() < 5 and day not in closures:
            expected.append(day.isoformat())
        day += timedelta(days=1)
    declared = doc["expected_open_dates"]
    assert declared == expected
    assert len(declared) == doc["expected_open_day_count"]
    assert hashlib.sha256(raw).hexdigest() == identity["sha256"]
    date_stream = chr(10).join(declared).encode("utf-8")
    assert hashlib.sha256(date_stream).hexdigest() == doc["expected_open_dates_sha256"] == identity["open_dates_sha256"]
    month_ends = {}
    for value in declared:
        month_ends[value[:7]] = value
    assert month_ends == doc["last_expected_open_day_by_month"]
    month_stream = chr(10).join(f"{month}={day}" for month, day in month_ends.items()).encode("utf-8")
    assert hashlib.sha256(month_stream).hexdigest() == doc["expected_month_end_identity_sha256"] == identity["month_end_identity_sha256"]
    assert len(declared) == identity["expected_open_day_count"]
    assert len(month_ends) == 203


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--calendar", type=lambda value: __import__("pathlib").Path(value))
    parser.add_argument("--source-lock", type=lambda value: __import__("pathlib").Path(value))
    args = parser.parse_args()
    checks = (
        ("exact common-numeraire / all-56-pair identity and log-return algebra", check_pair_algebra_and_numeraire),
        ("EUR/USD orientation, winner/loser, and exact tie behavior", check_eur_usd_direction_and_exact_ties),
        ("fixed monthly slots, missing endpoint, and future-suffix isolation", check_calendar_slots_and_causality),
        ("circular bootstrap, type-7, missing slot, and decision boundaries", check_bootstrap_and_decision_boundaries),
    )
    if args.calendar and args.source_lock:
        checks = checks + (("TARGET weekday/holiday calendar reconstruction and hash integrity", lambda: check_calendar_file(args.calendar, args.source_lock)),)
    elif args.calendar or args.source_lock:
        raise SystemExit("pass both --calendar and --source-lock together")
    for label, check in checks:
        check()
        print("PASS", label)
    print(f"RESULT: {len(checks)}/{len(checks)} independent synthetic/metadata checks passed")
    print("INPUTS: hand-authored synthetic constants and the pinned calendar metadata only; no market observations")


if __name__ == "__main__":
    main()
