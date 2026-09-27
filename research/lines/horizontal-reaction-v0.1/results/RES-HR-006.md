---
id: RES-HR-006
type: Result
research_line_id: RL-HR-001
run_id: RUN-HR-006
observed_at: UNKNOWN
execution_status: SUCCESS
evidence_validity: VALID
scientific_status: NOT_SUPPORTED
headline_metrics:
  selected_session_count: 60
  touch_population_count: 4788
  primary_event_count: 4786
  unavailable_event_count: 2
  bootstrap_seed: 20260913
  bootstrap_replications: 10000
  primary_mean_bps: -1.379343686609
  primary_median_bps: -0.648618177805
  primary_positive_rate: 0.469494358546
  primary_clustered_95ci_bps: [-1.908681505831, -0.862084588075]
  long_n: 2518
  long_mean_bps: -1.750279865969
  long_clustered_95ci_bps: [-2.490788225849, -0.961713552948]
  short_n: 2268
  short_mean_bps: -0.967519480423
  short_clustered_95ci_bps: [-1.803396853327, -0.121842806434]
  classification: NO_UNCONDITIONAL_TOUCH_SUPPORT
  independent_recomputation: PASS_EXACT_MATCH
artifact_refs:
  - https://docs.google.com/document/d/1V65WyLaecRTPPMtZZTb5Q-5rPLnYN9RLq-fyORXTwWM/edit
  - https://docs.google.com/document/d/1j_tpgHdw6CdXbe7rNwC2PTxxZUB1MOKs85Z4QQ-xDFM/edit
diagnostic_refs: []
relations:
  - type: produced_by_run
    target: RUN-HR-006
  - type: contradicts
    target: HYP-HR-002
---

# Completed 2026H2 unconditional-touch replication result

## Observation

The final source reports a completed run with source identity PASS for fixed 60-session M1 and raw Tick coverage, 4,788 generated first-touch events, 4,786 primary events, and 2 unavailable outcomes.

Using the frozen seed `20260913` and 10,000 session-clustered bootstrap replications, it reports:

- primary mean: -1.379343686609 bps;
- median: -0.648618177805 bps;
- positive rate: 46.9494358546%;
- clustered 95% interval: [-1.908681505831, -0.862084588075] bps.

The result reports exact-match independent recomputation of event count, mean, and clustered interval.

## Scientific result

Under the frozen classification rule, the result is `NO_UNCONDITIONAL_TOUCH_SUPPORT` for HYP-HR-002 in this fixed sample. It does not establish universal absence of horizontal reaction, causality, a profitable opposite-direction strategy, or a trading rule.

The LONG and SHORT subgroup summaries are descriptive only and do not override the primary result.

## Status and authority boundary

This is confirmatory relative to the Gold Trade Lab 2026H2 preregistration. The source explicitly says Studio Lab canonical status was not modified.

The earlier fail-closed attempt (RES-HR-006-ATTEMPT-1) remains a separate historical execution result. Its blocked status is not the scientific result.

## Sources

- [Frozen preregistration](https://docs.google.com/document/d/1kYvZ7tQ2m8ZynEjzVPZoy-k-cqsU6sWTqF4b_QeIkvo/edit)
- [Completed Result v3](https://docs.google.com/document/d/1V65WyLaecRTPPMtZZTb5Q-5rPLnYN9RLq-fyORXTwWM/edit)
- [Reproducibility code and result v3](https://docs.google.com/document/d/1j_tpgHdw6CdXbe7rNwC2PTxxZUB1MOKs85Z4QQ-xDFM/edit)
