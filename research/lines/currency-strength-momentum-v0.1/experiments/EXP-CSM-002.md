---
id: EXP-CSM-002
type: Experiment
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PLANNED
execution_status: NOT_RUN
evidence_validity: NOT_APPLICABLE
scientific_status: NOT_APPLICABLE
relations:
  - type: tests_hypothesis
    target: HYP-CSM-002
  - type: uses_specification
    target: SPEC-CSM-002-v01
  - type: uses_dataset
    target: DATA-CSM-002
updated_at: 2026-10-02
---

# Fixed monthly reference-rate Discovery screen — frozen, not run

## State

The science contract is frozen under HDEC-CSM-002-20261001. No experiment run, Result, or Interpretation exists. The Dataset plan is approved for EXPLORATORY_DISCOVERY but has not been captured for this experiment. This record does not authorize data access.

## Frozen design identity

- Hypothesis: HYP-CSM-002, still UNTESTED.
- Accepted pre-freeze SPEC-CSM-002-v01 SHA-256: `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`.
- Frozen SPEC Git blob SHA-1: `7fe114e2fcfa33b0565b51c717455abd8837d5d9`; post-metadata SHA-256: `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`.
- Human decision: HDEC-CSM-002-20261001; repository decision: DEC-CSM-003-FREEZE-20261001.
- Dataset plan: DATA-CSM-002; approved role EXPLORATORY_DISCOVERY. No dataset bytes have been captured for this experiment.
- Universe: AUD/CAD/CHF/EUR/GBP/JPY/NZD/USD; all 56 ordered pairs.
- Formation and target: one calendar month each, on the fixed 2010-01 through 2026-09 target grid.
- Source family: ECB EXR daily reference-rate family; only the retrospective latest-vintage reference-to-reference association is in scope.
- Primary outcome: arithmetic mean of eligible target pair log returns in basis points.
- Inference and sufficiency: circular 12-calendar-slot moving-block bootstrap, 10,000 replicates, seed 20261001, type-7 percentile; at least 120 eligible slots and at least 80% scheduled coverage.
- Search family: one candidate. No outcome-driven horizon, universe, period, subgroup, source, threshold, seed, or block search.

## Run state and access

- Run IDs: none. Result IDs: none.
- Actual full-history capture: not performed. Market outcome calculations: none.
- Integrator read of market history, currency-strength ranking, forward returns, strategy metrics, or performance plots: none.
- Packet C's 2009-11 bounded source-qualification probe and its separately disclosed search-result exposure are recorded in DATA-CSM-002.md. They are not an EXP-CSM-002 outcome.
- During the Integrator's separate ECB documentation follow-up, the current reference-rates page returned individual current observations in the tool output. This exceeded metadata-only scope; the exposure is recorded in GATE.md and remains pending human/E disposition. Values were not transcribed into integration artifacts, compared, calculated, or used.
- E independently reran the 53-test synthetic suite from current D head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`; all passed. Current config blob `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` remains FROZEN and matches the frozen SPEC. The prior 42/42 E suite applies only to old D head `4f739d9cc2b21c138771afec4a728bf2b57060ba`. E independently confirmed the score-identity ledger and tested signature/raw-byte checks, but found D pins stale I/E identities and reproduced a compound save-failure gap. Operational isolation and source-readiness gaps remain.

Execution remains closed. Current E audit `AUDIT-CSM-E-20261001-REAUDIT-01` at PR #38 head `4f683901d01fd6b5ce161c874118a34d40bcac82` is PARTIAL_WITH_GAPS / BLOCKED and is bound to current D head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`. D must resolve current I/E identity binding and the compound promotion/rollback receipt gap, publish new D identities, and obtain another E review. Source readiness, exposure disposition, production key distribution, isolation, durable ledger/destination and named operator remain open. The human acceptance alone does not open the gate.


## Pre-reaudit implementation snapshot — historical note (2026-10-02)

At the time of this snapshot, D PR #34 was at head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779` and E's independent re-audit had not yet completed. E PR #38 head `d1335b29eeb01cdd4b71cd5ded62033b8468e539` audited the prior D head `4f739d9cc2b21c138771afec4a728bf2b57060ba`; preserve that result only as an input-bound historical report. E's completed audit of current D is recorded in the section below. Current source and operational gaps are summarized in DEC-CSM-003-POST-E-REAUDIT-20261002.md and GATE.md. Run state remains PLANNED / NOT_RUN.


## Current E re-audit finding — 2026-10-02

E independently verified the current D synthetic suite (53/53) and synthetic outcome-blind ledger behavior. Its overall status is PARTIAL_WITH_GAPS / BLOCKED. D rejects the exact current I gate and new E audit identity because its identity pins remain old; the synthetic persistence fault test also reproduced a success receipt left after compound promotion/rollback failure. No capture or market-result run is authorized. DATA remains PLANNED / NOT_CAPTURED_FOR_EXPERIMENT.
