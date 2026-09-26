---
id: EXP-HR-001
type: Experiment
research_line_id: RL-HR-001
created_at: 2026-09-11
experiment_kind: CONFIRMATORY
tests_hypothesis: HYP-HR-001
uses_specification: SPEC-HR-001-v01
planned_dataset_uses:
  - dataset_id: DATA-HR-001
    role_at_freeze: UNUSED_EVALUATION_AT_FREEZE
relations:
  - type: tests_hypothesis
    target: HYP-HR-001
  - type: uses_specification
    target: SPEC-HR-001-v01
  - type: uses_dataset
    target: DATA-HR-001
---

# 2026H1 execution-aware candidate screen

## Question

Does the frozen v0.1 confirmation-entry strategy retain positive expectancy under a spread-aware executable BID/ASK proxy on a sample selected before outcome access?

## Sample construction

- Eligibility window: 2026-01-02 through 2026-06-30 UTC.
- Selection: first 60 structurally eligible UTC trading weekdays.
- Selected count: 60.
- Selected dates finish on 2026-04-10.
- No start-date, end-date, or sample-size change after outcome access.

## Execution semantics

- Confirming M1 close becomes usable only after the bar completes.
- LONG entry: first ASK tick at or after confirmation-bar close.
- SHORT entry: first BID tick at or after confirmation-bar close.
- LONG stop/target monitored on BID.
- SHORT stop/target monitored on ASK.
- Time stop uses first executable closing-side tick at or after entry +15 minutes.
- One open position maximum.

## Candidate-screen classification

PROMISING_FOR_FURTHER_VALIDATION only if the result has nontrivial trade count, expectancy > 0R, profit factor > 1, is not dominated by a tiny set of winners, and drawdown is operationally interpretable.

EXPLANATORY_REACTION_WITHOUT_TRADABLE_EDGE if reaction remains visible but executable expectancy <= 0 or PF <= 1.

INCONCLUSIVE if sample/evidence is insufficient without relaxing rules.

## Source

Evaluation freeze:
https://docs.google.com/document/d/1RrBrev2MqsAeeXDSI3CXDiBk2Mn6z0d_m77hEjnSqOo/edit
