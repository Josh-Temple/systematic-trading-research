---
id: EXP-HR-004
type: Experiment
research_line_id: RL-HR-001
created_at: 2026-09-27
experiment_kind: DIAGNOSTIC
tests_hypothesis: UNKNOWN
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

# Independent exploratory Data diagnostic on the fixed 2026H1 population

## Purpose

Represent the independent exploratory diagnostic report on the already-consumed 2,685-trade 2026H1 population. This is not a confirmatory test and does not change the strategy rules or sample.

## Fact / source basis

Primary source: [Horizontal Reaction Strategy v0.1 — Data Exploratory Diagnostic Result — 2026H1 v1](https://docs.google.com/document/d/1PfMQ9_rENQU6MttmH2A3CmGYk41G5SlFIPVFNv48bHo/edit), Drive document ID `1PfMQ9_rENQU6MttmH2A3CmGYk41G5SlFIPVFNv48bHo`.

The source says that a separate ChatGPT Data session analyzed the fixed population using the reported persistent Source Pack `trade_event_artifact.json`; this migration only preserves that report and did not rerun its analysis. The reported population was 2,685 trades over 60 UTC sessions, 2026-01-02 through 2026-04-10.

The report records: population unchanged; no additional trade exclusions; no parameter tuning; no strategy-rule change; confirmatory evidence = NO.

## Content

The source reports ledger-level quality checks with no duplicate IDs, fully duplicated rows, missing cells, or reported mismatches for event ordering, execution sides, risk, target, or return calculation. It reports negative expectancy across all rolling windows and the examined existing subgroups.

The same-timestamp midpoint comparison reports mean `-0.0413R` versus spread-aware BID/ASK mean `-0.2016R`, with approximately `0.1603R` mean accounting spread drag. The source explicitly says this is **not formal D5**, because actual exit timestamps depend on spread-aware stop/target triggering.

The source's interpretation is limited to the implemented v0.1 trade path: it describes broad negative outcomes and stop hits as an aggregate-loss component, while stating that the ledger-only analysis cannot distinguish absence of touch reaction from confirmation decay, exit geometry, or cost erosion.

## Boundary / what this does not establish

This remains an exploratory diagnostic over a consumed sample. It does not establish future profitability, touch-level reaction, reaction decay, D2/D3/D4 raw-path counterfactuals, formal matched D5, live commission/slippage economics, or a new rule. Exploratory subgroup observations are not rules.

The source reports that the executed 35-code-cell notebook was not located as a retrievable Drive artifact. It was not reconstructed here. It also records that a separate D1-D5 Result v2 was BLOCKED / NOT_RUN at the time that report was preserved; that statement is historical and does not describe later diagnostics.

## Schema friction / UNKNOWN

The v0.1 Experiment entity requires `tests_hypothesis`, but this descriptive diagnostic does not test HYP-HR-001. The field is `UNKNOWN`. Exact run timestamps, code commit, environment, raw notebook artifact, and independently reproducible code identity are not available from the source and remain unknown or unverified.

## Related artifacts

- HYP-HR-001
- SPEC-HR-001-v01
- DATA-HR-001
- RUN-HR-004
- RES-HR-004
- DIAG-HR-002
