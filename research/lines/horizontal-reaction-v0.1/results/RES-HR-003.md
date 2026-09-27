---
id: RES-HR-003
type: Result
research_line_id: RL-HR-001
run_id: RUN-HR-003
observed_at: UNKNOWN
execution_status: BLOCKED
evidence_validity: VALID
scientific_status: NOT_APPLICABLE
headline_metrics:
  selected_session_count: 60
  authoritative_trade_population: 2685
  source_identity_status: BLOCKED_BEFORE_REPLAY
  d1: NOT_RUN
  d2: NOT_RUN
  d3: NOT_RUN
  d4: NOT_RUN
  d5: NOT_RUN
  headline_recomputation: NOT_PERFORMED
  access_error: ERR_BLOCKED_BY_CLIENT
artifact_refs:
  - https://docs.google.com/document/d/1dbHCFmZOF2dYP7dcVmhJu1fKuY4U1jdf7RJHkZ94jX4/edit
diagnostic_refs:
  - DIAG-HR-001
relations:
  - type: produced_by_run
    target: RUN-HR-003
---

# Blocked D1-D5 replay result

## Observation

The primary source records failure to retrieve the required first-party raw source series through the specified Official Dukascopy Historical Data Export / JETTA route, with `ERR_BLOCKED_BY_CLIENT`. It records the fixed 60-session list and 2,685-trade population, but the data required for D1-D5 replay were not available to this attempt.

## Status scope

- `execution_status: BLOCKED` records the failed access/replay attempt.
- `evidence_validity: VALID` applies to the persisted record of that blocked attempt.
- `scientific_status: NOT_APPLICABLE` means this blocked attempt produced no scientific outcome. It is not a strategy-level inconclusive or negative finding.

D1-D5 are all `NOT_RUN`. No substitute data were used and no mechanism was assessed.

## Source

[Horizontal Reaction Strategy v0.1 — D1-D5 Diagnostic Replay Result (Chat Branch)](https://docs.google.com/document/d/1dbHCFmZOF2dYP7dcVmhJu1fKuY4U1jdf7RJHkZ94jX4/edit).
