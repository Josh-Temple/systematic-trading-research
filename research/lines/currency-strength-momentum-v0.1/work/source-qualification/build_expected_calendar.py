#!/usr/bin/env python3
"""Build the expected TARGET operating-day date grid for the fixed CSM source range.

This file generates calendar dates only; it never requests or reads market data.
"""
from datetime import date, timedelta
from pathlib import Path
import hashlib, json

START = date(2009, 11, 1)
END = date(2026, 9, 30)


def easter_sunday(year: int) -> date:
    # Gregorian computus (Meeus/Jones/Butcher).
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def target_closure_dates(year: int) -> dict[date, str]:
    easter = easter_sunday(year)
    return {
        date(year, 1, 1): "NEW_YEAR",
        easter - timedelta(days=2): "GOOD_FRIDAY",
        easter + timedelta(days=1): "EASTER_MONDAY",
        date(year, 5, 1): "LABOUR_DAY",
        date(year, 12, 25): "CHRISTMAS_DAY",
        date(year, 12, 26): "26_DECEMBER",
    }


def build() -> dict:
    weekday_closures = {}
    for year in range(START.year, END.year + 1):
        for day, reason in target_closure_dates(year).items():
            if START <= day <= END and day.weekday() < 5:
                weekday_closures[day.isoformat()] = reason

    open_dates = []
    day = START
    while day <= END:
        if day.weekday() < 5 and day.isoformat() not in weekday_closures:
            open_dates.append(day.isoformat())
        day += timedelta(days=1)

    month_ends = {}
    for iso_day in open_dates:
        month = iso_day[:7]
        month_ends[month] = iso_day

    date_stream = "\n".join(open_dates).encode("utf-8")
    month_stream = "\n".join(f"{m}={d}" for m, d in month_ends.items()).encode("utf-8")
    return {
        "calendar_id": "ECB_TARGET_LONG_TERM_2002_RULE",
        "calendar_version": "1.0",
        "date_basis": "local operating-day labels; no intraday timestamps",
        "timezone_for_date_labels": "Europe/Berlin",
        "range_start_inclusive": START.isoformat(),
        "range_end_inclusive": END.isoformat(),
        "rule": "Monday-Friday excluding New Year's Day, Good Friday, Easter Monday, 1 May, Christmas Day, and 26 December. Weekend dates are already closed.",
        "official_rule_scope": "ECB decision dated 2000-12-14 says this common calendar applies from 2002 until further notice; the current T2/ECB framework confirms TARGET operating-day use. This is the expected calendar, not proof that every series published on every expected day.",
        "expected_open_day_count": len(open_dates),
        "expected_open_dates_sha256": hashlib.sha256(date_stream).hexdigest(),
        "expected_month_end_identity_sha256": hashlib.sha256(month_stream).hexdigest(),
        "weekday_closures": dict(sorted(weekday_closures.items())),
        "expected_open_dates": open_dates,
        "last_expected_open_day_by_month": month_ends,
    }


if __name__ == "__main__":
    obj = build()
    target = Path(__file__).with_name("expected-calendar.json")
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    target.write_bytes(raw)
    print(json.dumps({
        "path": target.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "expected_open_day_count": obj["expected_open_day_count"],
        "first_open_day": obj["expected_open_dates"][0],
        "last_open_day": obj["expected_open_dates"][-1],
        "month_count": len(obj["last_expected_open_day_by_month"]),
        "probe_month_expected_days": [d for d in obj["expected_open_dates"] if d.startswith("2009-11-")],
    }, ensure_ascii=False, separators=(",", ":")))
