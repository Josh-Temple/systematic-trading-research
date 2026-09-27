---
id: SPEC-HR-002-v01
type: Specification
research_line_id: RL-HR-001
version: v0.1
created_at: 2026-09-13
frozen_at: 2026-09-13
freeze_status: FROZEN
tests_hypothesis: HYP-HR-002
data_roles_allowed:
  - UNUSED_EVALUATION_AT_FREEZE
outcome_definition: Mean direction-aware first-touch to +15 completed minutes return in bps over all eligible first-touch events, regardless of later confirmation or trade entry
metrics:
  - eligible_touch_event_count
  - unavailable_event_count
  - mean_direction_aware_bps
  - session_clustered_95_percent_interval
  - median_direction_aware_bps
  - positive_rate
  - LONG_descriptive_summary
  - SHORT_descriptive_summary
  - session_level_counts_and_means
stopping_or_kill_conditions:
  - fewer_than_60_structurally_eligible_sessions
  - independence_review_hold
  - source_identity_or_completeness_gate_failure
  - touch_population_definition_hold
  - required_data_gap_requiring_imputation_or_substitution
relations:
  - type: tests_hypothesis
    target: HYP-HR-002
---

# Unconditional Touch Replication — frozen 2026H2 specification

## Source

[Horizontal Reaction — Unconditional Touch Replication Preregistration — 2026H2 v1](https://docs.google.com/document/d/1kYvZ7tQ2m8ZynEjzVPZoy-k-cqsU6sWTqF4b_QeIkvo/edit), frozen by Gold Trade Lab 2026-09-13 JST. This is a proposed confirmatory test relative to that preregistration; it was not registered as Studio Lab canonical.

## Sample

- Calendar eligibility window: 2026-04-13 through 2026-08-31 UTC.
- Select the first 60 structurally eligible UTC trading weekdays in ascending order from 2026-04-13.
- Do not choose or replace dates based on touch outcomes.
- The selected 60-session list is recorded in the [Reproducibility Artifact v1, Selected Sessions tab](https://docs.google.com/spreadsheets/d/1fuebVQ5nr2vvU0YQWbtrabtHHyZ-EldHbXhcZYDOJLs/edit); the completed Result v3 repeats the fixed list. The listed sessions end 2026-07-09.

## Source and signal construction

- Provider: Dukascopy first-party historical data only.
- Signal: XAU/USD BID M1 UTC.
- Path and endpoint quotes: XAU/USD raw BID/ASK ticks UTC.
- Reuse the v0.1 pre-touch rules without modification: immediately preceding 60 observed M1 bars; support/resistance from their Low/High extremes; gamma from absolute consecutive M1 Close changes available strictly before the candidate time; the frozen zone bounds; approach from above for LONG support and below for SHORT resistance; existing fresh-approach / interaction-reset logic.
- The primary population includes every eligible first-touch event, regardless of later confirmation, confirmation latency, signal, executable entry, position blocking, or trade outcome. Do not apply the old matched 2,685-trade restriction.

## Outcome and inference

- For each eligible touch, calculate the existing D4-compatible direction-aware touch-to-+15-completed-minute return in bps using the frozen touch-price and quote-side convention.
- Record unavailable endpoints and reasons; do not impute, shift, or substitute providers.
- Primary statistic: event count, unavailable count, mean bps, and 95% session-clustered bootstrap interval.
- Bootstrap 10,000 replications, seed `20260913`; resample the 60 sessions as clusters with replacement and pool eligible events.
- Secondary descriptions: median, positive rate, LONG/SHORT summaries, and session-level counts/means. Secondary results do not override the primary interpretation.

## Frozen classification

- `REPLICATION_SUPPORTED`: primary mean > 0 and clustered 95% interval lower bound > 0.
- `NO_UNCONDITIONAL_TOUCH_SUPPORT`: primary mean <= 0 and interval upper bound <= 0.
- `INCONCLUSIVE`: interval includes 0.

## Forbidden on this sample

No changes to lookback, gamma, zone, approach, touch de-clustering, period, horizon, confirmation delay, stop, target, filters, or event inclusion. No parameter search, touch-entry strategy design, outcome-driven session changes, provider substitution, or same-sample rescue.

## Boundary

A positive touch-to-+15m mean would concern price reaction only, not tradability. The test makes no causal claim against a non-touch control and does not establish executable profitability.
