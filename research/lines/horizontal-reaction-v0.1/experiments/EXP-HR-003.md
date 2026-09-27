---
id: EXP-HR-003
type: Experiment
research_line_id: RL-HR-001
created_at: 2026-09-27
experiment_kind: DIAGNOSTIC
tests_hypothesis: NOT_APPLICABLE
uses_specification: SPEC-HR-001-v01
planned_dataset_uses:
  - dataset_id: DATA-HR-001
    role_at_freeze: CONSUMED_HOLDOUT
relations:
  - type: uses_specification
    target: SPEC-HR-001-v01
  - type: uses_dataset
    target: DATA-HR-001
---

# Blocked 2026H1 D1-D5 replay attempt

## Purpose

Record the D1-D5 replay attempt that stopped before replay because the required first-party raw source data could not be reacquired through the specified route.

## Fact / source basis

Primary source: [Horizontal Reaction Strategy v0.1 — D1-D5 Diagnostic Replay Result (Chat Branch)](https://docs.google.com/document/d/1dbHCFmZOF2dYP7dcVmhJu1fKuY4U1jdf7RJHkZ94jX4/edit), Drive document ID `1dbHCFmZOF2dYP7dcVmhJu1fKuY4U1jdf7RJHkZ94jX4`. The exact source revision was not captured.

The source reports a fixed 60-session list and the original 2,685-trade population. It states that the needed raw BID/ASK path and reconstructive values were unavailable in the existing result/ledger, and that reacquisition through the specified Official Dukascopy Historical Data Export / JETTA route was blocked with `ERR_BLOCKED_BY_CLIENT`.

## Boundary / what this does not establish

The source reports:

- `SOURCE_IDENTITY_STATUS=BLOCKED_BEFORE_REPLAY`
- D1, D2, D3, D4, and D5 each `NOT_RUN`
- `HEADLINE_RECOMPUTATION=NOT_PERFORMED`
- no substitute package, provider, midpoint/M1 close, synthetic spread, estimate, or interpolation was used
- alternative explanations were `NOT_ASSESSED`

This is a blocked execution and source-access record. It is not a negative scientific result and establishes no explanation for the 2026H1 strategy result.

## Schema friction / UNKNOWN

This Experiment does not directly test a scientific hypothesis, so `tests_hypothesis` is `NOT_APPLICABLE` under the pilot-refined v0.1 schema. Run start/completion timestamps, exact code identity, environment, and exact source revision are not provided by the primary source and remain unknown.

## Related artifacts

- HYP-HR-001
- SPEC-HR-001-v01
- DATA-HR-001
- RUN-HR-003
- RES-HR-003
- DIAG-HR-001
