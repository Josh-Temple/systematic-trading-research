---
id: EXP-CSM-002
type: Experiment
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PLANNED_NOT_FROZEN
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
---

# Fixed monthly reference-rate Discovery screen — planned only

## State

This Experiment record is created from the current proposal and reconciled A–D worker evidence. It is **PLANNED_NOT_FROZEN**. No experimental run exists. No result or Interpretation is created. This record does not authorize data access.

## Proposed design identity

- Hypothesis: HYP-CSM-002, currently UNTESTED.
- Proposed contract: SPEC-CSM-002-v01 at proposal ref e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff, Git blob SHA-1 a073e77dec14337ee20609ed6136e50a8c1e76e2, SHA-256 e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90.
- Proposed dataset: DATA-CSM-002, role EXPLORATORY_DISCOVERY if the human approves the exact contract.
- Universe: AUD/CAD/CHF/EUR/GBP/JPY/NZD/USD; all 56 ordered pairs.
- Formation and target: one calendar month each, on the fixed 2010-01 through 2026-09 target grid.
- Source: ECB EXR daily reference-rate family; the only claim contemplated is retrospective reference-to-reference association.
- Primary outcome: arithmetic mean of eligible target pair log returns in basis points.
- Inference and sufficiency: the fixed circular 12-calendar-slot moving-block bootstrap, 10,000 replicates, seed 20261001, type-7 percentile; at least 120 eligible slots and at least 80% scheduled coverage.
- Search family: one candidate. No outcome-driven horizon, universe, period, subgroup, source, threshold, seed, or block search.

## Run state and access

- Run IDs: none.
- Result IDs: none.
- Actual full-history capture: not performed.
- Integrator market outcome access: false.
- The C 2009-11 bounded source qualification probe and its separately disclosed search-result exposure are recorded in DATA-CSM-002.md. They are not an EXP-CSM-002 outcome.
- The worker-reported 42 D tests use synthetic inputs and are not an experimental result.
- Execution remains unavailable until exact human acceptance, source/data readiness, an E audit, an all-PASS I gate, and a separate X instruction.

