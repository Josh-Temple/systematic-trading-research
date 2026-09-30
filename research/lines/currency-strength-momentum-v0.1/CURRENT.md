---
type: CurrentProjection
research_line_id: RL-CSM-001
projection_generated_at: 2026-10-01
derived_from_decisions:
  - DEC-CSM-001
derived_from_interpretations: []
---

# Current State

## Current scientific status

- HYP-CSM-001 is UNTESTED.
- No market outcome for this research line has been calculated in this repository.
- The line is approved only for a bounded exploratory monthly screen.

## Frozen v0.1 question

Among AUD, CAD, CHF, EUR, GBP, JPY, NZD, and USD:

1. rank prior-calendar-month spot strength;
2. long the strongest currency against the weakest;
3. measure the next-calendar-month spot return.

The formation period and forward horizon are both one month.

## Important identity

Under the common-numeraire return definition, strongest-minus-weakest is mathematically the same selection as the currency pair with the maximum prior-month return.

Therefore v0.1 tests extreme cross-sectional FX momentum. It does not test a separate proprietary "currency strength indicator" mechanism.

## Evidence state

Published literature supports currency momentum as a real research question, but later work suggests much of the effect may reflect carry and dollar-factor momentum.

A relevant public GitHub project reports negative 1-hour currency-strength continuation and cost-dominated short-horizon reversion. That is adverse prior evidence for intraday versions, not a result for this monthly specification.

## Data state

DATA-CSM-001 is PLANNED_SOURCE_QUALIFICATION.

Primary candidate source: official ECB daily euro reference rates through the frozen cutoff 2026-09-30.

No provider substitution is authorized inside v0.1.

## Next action

1. Acquire and validate the exact ECB series.
2. Preserve source identity and hash.
3. Implement the frozen transformation and deterministic identity checks.
4. Execute EXP-CSM-001 once.
5. Save Result, Interpretation, Decision, and update this projection.

## Boundaries

Do not add:

- RSI / MACD / ADX
- trend-entry timing
- volatility-adjusted strength
- multi-horizon averaging
- carry filters
- regime filters
- alternative lookbacks

before the v0.1 result is durably recorded.
