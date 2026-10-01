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
- D's 42 synthetic/component tests are implementation checks, not an experiment result. At current PR #34 head `4f739d9cc2b21c138771afec4a728bf2b57060ba`, config blob `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` matches the frozen SPEC identity; E independently reran the suite (42/42). E still found the event ledger lacks SPEC-required formation score identities, and gate-authentication, source-lock raw-byte, save-failure, and isolation gaps remain.

Execution remains closed. E audit `AUDIT-CSM-E-20261002` is PARTIAL_WITH_GAPS with recommendation BLOCKED. Before any I2 reconsideration: D must fix the event-ledger score identity and gate/capture safeguards, then publish new code/test/config identities; E must audit changed inputs; source readiness, exposure disposition, isolation, durable ledger/destination and named operator must be resolved; and every I2 condition must PASS. The human acceptance alone does not open the gate.
