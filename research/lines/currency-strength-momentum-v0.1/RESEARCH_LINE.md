---
id: RL-CSM-001
type: ResearchLine
created_at: 2026-10-01
status: DISCOVERY_READY
relations: []
---

# Currency Strength Momentum v0.1

## Purpose

Test the specific FX idea: among eight major currencies, rank recent currency strength, then hold the strongest currency long against the weakest currency for the next month.

This line treats the idea as a form of cross-sectional currency momentum, not as a proprietary "currency strength indicator" effect.

## Universe

Frozen for v0.1:

- AUD
- CAD
- CHF
- EUR
- GBP
- JPY
- NZD
- USD

The universe comes from the user-specified major-currency concept and is not selected from observed outcomes.

## Core identity

Under the v0.1 definition, currency strength is a common-numeraire return ranking.

For currency i with log value v_i in a common numeraire:

s_i(t) = v_i(t) - v_i(t-1)

The strongest-minus-weakest selected pair is therefore also the currency pair with the largest prior-period return because:

pair_return(i,j) = s_i - s_j

This equivalence is part of the specification and must be checked deterministically in code. A positive result would be evidence about extreme cross-sectional momentum, not evidence that a separate "strength meter" mechanism exists.

## Research boundary

v0.1 is a bounded exploratory / Discovery screen.

It does not establish:

- tradeable net profitability,
- live broker execution quality,
- independence from carry or dollar factors,
- robustness to other lookbacks or holding periods,
- intraday persistence,
- parameter optimality.

No parameter sweep is permitted in v0.1.

## Current next action

Qualify and acquire the frozen ECB daily reference-rate source through 2026-09-30, preserve raw/source identity, then execute EXP-CSM-001 exactly once.

If source acquisition or identity cannot be established cleanly, record the operational block and do not substitute a different provider silently.
