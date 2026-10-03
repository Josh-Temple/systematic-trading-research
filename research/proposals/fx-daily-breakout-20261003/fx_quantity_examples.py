"""Offline USD/JPY arithmetic examples. No signals, accounts or order access.

Cost inputs are hypothetical reserves, not broker quotes. The distance is a
mid-price movement; spread belongs in unit_cost exactly once. Never feed an
already spread-inclusive executable-price distance and add spread again.
"""
from decimal import Decimal, ROUND_FLOOR
import json

def quantity(*, budget, distance, unit_cost, fixed_cost, equity, price,
             leverage_cap, minimum, step):
    args = [budget, distance, unit_cost, fixed_cost, equity, price,
            leverage_cap, minimum, step]
    if any(v is None for v in args):
        return {"status": "BLOCKED", "reason": "UNKNOWN_INPUT"}
    b, d, c, f, e, p, lev, low, tick = map(lambda v: Decimal(str(v)), args)
    if any(not v.is_finite() for v in (b, d, c, f, e, p, lev, low, tick)):
        raise ValueError("Inputs must be finite")
    if min(b, d, e, p, lev, low, tick) <= 0 or min(c, f) < 0:
        raise ValueError("Positive sizes and nonnegative costs required")
    if low != low.to_integral_value() or tick != tick.to_integral_value() or low % tick:
        raise ValueError("Integer currency units and minimum aligned to step required")
    if b <= f:
        return {"status": "SKIP", "reason": "FIXED_COST_EXCEEDS_BUDGET"}
    risk_limit = (b - f) / (d + c)
    exposure_limit = e * lev / p
    q = (min(risk_limit, exposure_limit) / tick).to_integral_value(rounding=ROUND_FLOOR) * tick
    if q < low:
        return {"status": "SKIP", "reason": "MINIMUM_SIZE_EXCEEDS_LIMITS", "rounded_units": format(q, 'f')}
    return {"status": "ARITHMETIC_ONLY", "units": format(q, 'f'),
            "reserved_loss_jpy": format(q * (d + c) + f, 'f'),
            "notional_jpy": format(q * p, 'f'), "effective_leverage": format(q * p / e, 'f')}

def examples():
    out = []
    for budget in (50, 25):
        for distance in ('0.30', '0.50', '1.00'):
            for broker, minimum, step in [('Matsui', 1, 1), ('XM_Micro_MT5', 100, 10)]:
                inputs = dict(budget=budget, distance=distance, unit_cost='0.02',
                              fixed_cost=0, equity=10000, price=150,
                              leverage_cap=2, minimum=minimum, step=step)
                out.append({'broker': broker, 'hypothetical_inputs': inputs,
                            'result': quantity(**inputs)})
    return {'scope': 'HYPOTHETICAL_ARITHMETIC_ONLY', 'market_outcomes_computed': False,
            'assumptions': '150 JPY/USD and 0.02 JPY/unit cost reserve are illustrative, not observed. Leverage cap 2 is a draft guardrail, not account setting. No margin calculation.',
            'cases': out}

if __name__ == '__main__':
    print(json.dumps(examples(), ensure_ascii=False, indent=2))
