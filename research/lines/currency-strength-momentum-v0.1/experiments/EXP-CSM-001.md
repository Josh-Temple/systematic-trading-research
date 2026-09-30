---
id: EXP-CSM-001
type: Experiment
research_line_id: RL-CSM-001
created_at: 2026-10-01
experiment_kind: EXPLORATORY_DISCOVERY
tests_hypothesis: HYP-CSM-001
uses_specification: SPEC-CSM-001-v01
planned_dataset_uses:
  - dataset_id: DATA-CSM-001
    role_at_freeze: EXPLORATORY_DISCOVERY
relations:
  - type: tests_hypothesis
    target: HYP-CSM-001
  - type: uses_specification
    target: SPEC-CSM-001-v01
  - type: uses_dataset
    target: DATA-CSM-001
---

# Monthly strongest-minus-weakest screen

## Question

Does the prior-calendar-month strongest-minus-weakest pair among the frozen eight-currency universe have positive next-calendar-month spot continuation?

## Comparison target

The primary null is no positive continuation in the selected pair.

A separate "best pair momentum" comparator is not treated as an independent strategy because, under the frozen common-numeraire definition, strongest-minus-weakest selection is mathematically identical to selecting the pair with the largest prior-month return.

## Why monthly

The primary horizon is monthly because the published currency-momentum literature uses monthly formation/holding portfolios, while a relevant public implementation reports rejection of currency-strength continuation at a 1-hour horizon.

The v0.1 experiment therefore does not mix intraday and medium-horizon evidence.

## Execution sequence

1. Qualify DATA-CSM-001 source identity and coverage.
2. Persist the raw source or an immutable source snapshot plus retrieval metadata/hash.
3. Generate month-end observations without interpolation.
4. Compute strength scores and selected pair.
5. Assert the strongest-minus-weakest / maximum-pair-return identity.
6. Freeze the event ledger before calculating forward outcomes if the implementation separates these steps.
7. Calculate forward outcomes and predeclared metrics once.
8. Save code identity, source identity, event ledger, and result.
9. Classify only under the predeclared Discovery decision rule.

## Not part of this experiment

- carry or dollar-factor regression
- interest-rate differential returns
- executable BID/ASK backtest
- broker rollover / financing
- transaction-cost optimization
- alternative formation/holding periods
- volatility-adjusted strength
- multi-horizon strength
- technical-entry timing
- intraday execution

Those questions may be considered only after the v0.1 result is recorded.
