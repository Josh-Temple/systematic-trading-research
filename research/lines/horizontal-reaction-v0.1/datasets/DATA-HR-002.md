---
id: DATA-HR-002
type: Dataset
research_line_id: RL-HR-001
created_at: 2026-09-13
provider: Dukascopy first-party historical data
instrument: XAU/USD
time_range: 2026-04-13/2026-07-09 selected sessions; eligibility window 2026-04-13/2026-08-31 UTC
granularity:
  signal: M1
  path: raw BID/ASK Tick
role: CONSUMED_HOLDOUT
consumption_status: CONSUMED
may_influence_future_search: false
identity_evidence:
  result_reported_status: PASS_FIXED_60_SESSION_M1_AND_RAW_TICK_COVERAGE
  selected_sessions_reference: https://docs.google.com/spreadsheets/d/1fuebVQ5nr2vvU0YQWbtrabtHHyZ-EldHbXhcZYDOJLs/edit
  source_gate_reference: https://docs.google.com/document/d/1V65WyLaecRTPPMtZZTb5Q-5rPLnYN9RLq-fyORXTwWM/edit
  july_expected_m1_hashes_reference: https://docs.google.com/document/d/1ZatYdOTzwQoQiSZZzGl28Bpl44e7g4D9lJds8ZGxFgg/edit
  july_tick_per_file_hashes_in_migrated_result_text: UNVERIFIED
relations: []
---

# 2026H2 unconditional-touch replication dataset

## Identity and role

This is a distinct 2026H2 selected-session dataset for HYP-HR-002. The completed Result v3 reports source identity as `PASS_FIXED_60_SESSION_M1_AND_RAW_TICK_COVERAGE`. The pre-outcome reproducibility sheet records the selected session list and source-gate state at the earlier blocked attempt. The July source-recovery handoff lists the six selected July M1 expected hashes and defines a 146-hour July Tick recovery scope.

At preregistration, the 60-session sample was an unused evaluation sample for this hypothesis. After the completed result was accessed, this dataset is `CONSUMED_HOLDOUT` and must not be reset to unused.

## Selected sessions

The frozen 60 selected UTC dates are listed in the linked reproducibility sheet and in the completed Result v3. They span 2026-04-13 through 2026-07-09. No date selection or replacement after outcome access is reported.

## Provenance boundary

The final source reports fixed 60-session M1 and raw Tick coverage passed. Exact per-file Tick hashes for the final recovery were not restated in the Result v3 text retrieved for this migration; that field remains `UNVERIFIED` here. This records a migration visibility limit and does not overwrite the source's reported overall PASS.

## Sources

- [Horizontal Reaction — 2026H2 Unconditional Touch Replication Preregistration — 2026H2 v1](https://docs.google.com/document/d/1kYvZ7tQ2m8ZynEjzVPZoy-k-cqsU6sWTqF4b_QeIkvo/edit)
- [Horizontal Reaction — 2026H2 Unconditional Touch Replication Reproducibility Artifact v1](https://docs.google.com/spreadsheets/d/1fuebVQ5nr2vvU0YQWbtrabtHHyZ-EldHbXhcZYDOJLs/edit)
- [Horizontal Reaction — 2026H2 Unconditional Touch Replication Result v3](https://docs.google.com/document/d/1V65WyLaecRTPPMtZZTb5Q-5rPLnYN9RLq-fyORXTwWM/edit)
