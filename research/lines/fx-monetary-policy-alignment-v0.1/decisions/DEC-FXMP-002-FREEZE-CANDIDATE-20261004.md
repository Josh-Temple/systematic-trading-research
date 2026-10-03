---
id: DEC-FXMP-002-FREEZE-CANDIDATE-20261004
type: Decision
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: HUMAN_BOUNDARY
relations:
  - type: derived_from
    target: DIAG-FXMP-SOURCE-001
  - type: derived_from
    target: REF-FXMP-SCI-001
  - type: derived_from
    target: AUDIT-FXMP-E-20261004-01
  - type: derived_from
    target: AUDIT-FXMP-INFERENCE-20261004-01
---

# Exact freeze candidate decision — awaiting human acceptance

## Decision

**READY_FOR_EXPLICIT_HUMAN_FREEZE / MARKET OUTCOME ACCESS REMAINS CLOSED**

The pre-outcome research design is sufficiently specified and independently audited to present one exact freeze candidate to the human user.

Candidate specification:

- file: `specifications/SPEC-FXMP-001-v02.md`
- Git blob SHA-1: `f19f611648253e7fad23fa53b6c229addc1d6711`
- bytes: `12201`
- SHA-256: `dfcdc8e6d240539fca1afdc5bafd3202bd0e0648fdc1c13c7224917fd7a66040`
- identity workflow: `FXMP freeze candidate identity`
- identity run: `37158290046`

## Scientific choices proposed for freeze

1. Existing frozen CSM pair-selection/output contract remains unchanged.
2. BIS WS_CBPOL monthly end-of-period policy rates are the only policy source.
3. Policy momentum lookback is exactly three calendar months: `r(k-1)-r(k-4)`.
4. ALIGNED / NEUTRAL / OPPOSED use the sign of the selected-pair relative policy change with no epsilon threshold.
5. CHF June 2019 and EUR September 2024 policy-instrument switch windows fail closed.
6. JPY April 2013 through September 2016 policy-rate-unavailable windows fail closed.
7. Primary estimand is `mean(y|ALIGNED)-mean(y|OPPOSED)`.
8. Minimum eligible primary-group counts are 24 ALIGNED and 24 OPPOSED.
9. Dependence interval is a 12-calendar-slot circular moving-block bootstrap with 10,000 replicates, Python `random.Random`, seed 20261004, type-7 95% interval.
10. Any bootstrap replicate lacking either primary group fails inference without retry.
11. This run remains retrospective latest-vintage EXPLORATORY_DISCOVERY only.
12. A positive result requires a separately frozen unused/prospective test before any tradable-edge claim.

## Why these choices are admissible now

They were fixed before HYP-FXMP-001 market outcomes were accessed.

- Source identity and predictor slice are locked and the deterministic slice is preserved in Git.
- Policy-instrument discontinuities were discovered and handled before outcome access.
- Feature implementation passed synthetic CI and independent audit.
- Inference implementation passed synthetic CI and independent audit.
- The three-month lookback and 24/24 floor are explicit bounded design choices, not values selected from FXMP outcome performance.

The literature does not establish that three months or 24/24 are uniquely optimal. Their scientific value here is that they define one bounded, preregistered candidate and prevent outcome-driven rescue.

## Human action required

The human user must explicitly accept the exact SHA-256:

`dfcdc8e6d240539fca1afdc5bafd3202bd0e0648fdc1c13c7224917fd7a66040`

A generic instruction to continue is not treated as acceptance of these exact bytes unless it is given after this identity is presented.

## After acceptance

Acceptance authorizes only the science freeze.

The Integrator must then:
- create an exact human acceptance receipt;
- change only freeze metadata in SPEC-FXMP-001-v02;
- preserve both pre-freeze and frozen hashes;
- bind source/implementation/audit identities;
- re-check the CSM frozen dependency;
- keep market-outcome access closed until a separate final gate passes.

No outcome run is authorized by this Decision.
