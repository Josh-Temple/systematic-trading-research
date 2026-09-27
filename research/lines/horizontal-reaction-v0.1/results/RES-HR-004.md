---
id: RES-HR-004
type: Result
research_line_id: RL-HR-001
run_id: RUN-HR-004
observed_at: UNKNOWN
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: EXPLORATORY
headline_metrics:
  population: 2685
  sessions: 60
  rows: 2685
  columns: 33
  reported_duplicate_trade_ids: 0
  reported_duplicate_event_ids: 0
  reported_missing_cells: 0
  reported_ledger_calculation_mismatches: 0
  reported_same_timestamp_midpoint_mean_R: -0.0413
  reported_spread_aware_mean_R: -0.2016
  reported_same_timestamp_accounting_spread_drag_R: 0.1603
  formal_d5: NOT_ESTABLISHED
  confirmatory_evidence: NO
  parameter_tuning: NO
  strategy_rule_change: NO
artifact_refs:
  - https://docs.google.com/document/d/1PfMQ9_rENQU6MttmH2A3CmGYk41G5SlFIPVFNv48bHo/edit
diagnostic_refs:
  - DIAG-HR-002
relations:
  - type: produced_by_run
    target: RUN-HR-004
  - type: derived_from
    target: DATA-HR-001
---

# Independent exploratory Data diagnostic result

## Observation

The primary source reports that the fixed 2,685-trade population was not changed, no extra trade exclusions were added, and no strategy-rule or parameter changes were made. It reports ledger quality checks with no duplicates, missing cells, or calculation mismatches.

It reports a same-timestamp midpoint mean of `-0.0413R`, spread-aware mean of `-0.2016R`, and approximate accounting spread drag of `0.1603R`. This comparison uses the actual spread-aware exits and is not formal D5.

## Status scope

`execution_status: SUCCESS` refers to the diagnostic analysis as reported by its source; migration did not rerun it. `evidence_validity: PARTIAL` reflects that the report is retrievable but the executed 35-code-cell notebook was not located as a retrievable artifact. `scientific_status: EXPLORATORY` preserves the source's explicit non-confirmatory status.

## Boundary

The source does not establish the cause of the negative trade-path result, touch-level reaction, future profitability, or a tradable rule. All observations use consumed 2026H1 data. The same-timestamp midpoint comparison must not be relabeled as formal D5.

## Source

[Horizontal Reaction Strategy v0.1 — Data Exploratory Diagnostic Result — 2026H1 v1](https://docs.google.com/document/d/1PfMQ9_rENQU6MttmH2A3CmGYk41G5SlFIPVFNv48bHo/edit).
