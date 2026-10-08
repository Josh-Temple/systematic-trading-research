"""Offline arithmetic only. No market history, signals, API, or brokerage access.

Run beside instruments.csv: python3 cost_feasibility.py > feasibility.json
Snapshot prices are sizing illustrations, not orders or return forecasts.
"""

import csv
import json
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path


def main():
    source = Path(__file__).with_name("instruments.csv")
    with source.open(encoding="utf-8", newline="") as handle:
        products = list(csv.DictReader(handle))
    if len(products) != 5 or len({r["code"] for r in products}) != 5:
        raise ValueError("Expected five unique candidate products")
    for row in products:
        expected = Decimal(row["close_jpy"]) * Decimal(row["lot_units"])
        if expected != Decimal(row["lot_notional_jpy"]):
            raise ValueError(f"Inconsistent lot notional: {row['code']}")
        if row["close_date"] != "2026-10-02":
            raise ValueError("Mixed snapshot dates")
    plans = {"Light": Decimal("1650"), "Standard": Decimal("3300")}
    scenarios = []
    for capital in map(Decimal, ("100000", "300000", "1000000", "3000000")):
        budget = capital / len(products)
        positions = []
        for row in products:
            lot_value = Decimal(row["lot_notional_jpy"])
            lots = (budget / lot_value).to_integral_value(rounding=ROUND_FLOOR)
            positions.append({
                "code": row["code"],
                "lots": int(lots),
                "units": int(lots * Decimal(row["lot_units"])),
                "notional_jpy": int(lots * lot_value),
            })
        invested = sum(p["notional_jpy"] for p in positions)
        cash = int(capital) - invested
        scenarios.append({
            "capital_jpy": int(capital),
            "all_five_sleeves_active_illustration": positions,
            "invested_jpy": invested,
            "rounding_cash_jpy": cash,
            "rounding_cash_pct": float(Decimal(cash) / capital * 100),
            "annual_data_cost_pct": {
                plan: float(fee * 12 / capital * 100)
                for plan, fee in plans.items()
            },
        })
    output = {
        "status": "ILLUSTRATIVE_FEASIBILITY_NOT_STRATEGY_RESULT",
        "price_snapshot_date": "2026-10-02",
        "currency": "JPY",
        "assumptions": [
            "Five equal capital sleeves; all active for lot-rounding illustration only",
            "Floor to whole trading lots; residual stays cash",
            "No transaction fees or execution price changes in lot-sizing illustration",
            "No actual user's capital or trade instruction inferred",
            "Twelve monthly subscriptions at currently published prices; no add-ons",
        ],
        "minimum_capital_one_lot_in_each_20pct_sleeve_jpy": int(
            max(Decimal(p["lot_notional_jpy"]) for p in products) * len(products)
        ),
        "annual_data_cost_jpy": {
            plan: int(fee * 12) for plan, fee in plans.items()
        },
        "scenarios": scenarios,
        "does_not_estimate": ["strategy_returns", "bid_ask_spread", "drawdown", "tax", "suitability"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
