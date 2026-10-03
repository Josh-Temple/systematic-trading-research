---
type: CurrentProjection
research_line_id: RL-FXMP-001
projection_generated_at: 2026-10-04
derived_from_decisions:
  - DEC-FXMP-001-PREOUTCOME-20261003
  - DEC-FXMP-002-FREEZE-CANDIDATE-20261004
derived_from_interpretations: []
---

# Current projection — exact freeze candidate awaiting human acceptance

- **HYP-FXMP-001:** UNTESTED.
- **SPEC-FXMP-001-v02:** HUMAN_BOUNDARY / PROPOSED_NOT_FROZEN.
- **Exact candidate identity:** Git blob `f19f611648253e7fad23fa53b6c229addc1d6711`; 12,201 bytes; SHA-256 `dfcdc8e6d240539fca1afdc5bafd3202bd0e0648fdc1c13c7224917fd7a66040`.
- **Market outcome access:** CLOSED.
- **CSM dependency:** current frozen CSM specification remains blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`; this FXMP line does not alter it.
- **BIS predictor source:** raw archive SHA-256 `707f39206f7c4bc1001ea7f67b182d20e9b2d59fcf6542d0dd566a19f61d7f15`.
- **Durable predictor slice:** Git blob `1dc3057e1d370d9c56c721b9caa6d26e7cd5dfba`; SHA-256 `2cf878dbd0b8a98c05db741dc40a14d0b62a7cb6c178f86121937b0d41eb7eee`.
- **Source qualification:** valid for retrospective latest-vintage scope; point-in-time historical vintage remains unverified and is not claimed.
- **Semantic guards:** CHF 2019-06 and EUR 2024-09 instrument switches; JPY 2013-04 through 2016-09 policy-rate-unavailable interval; fail closed.
- **Feature implementation:** synthetic tests and independent audit PASS; outcome-field invariance PASS.
- **Inference implementation:** combined feature+inference CI 22/22 PASS; independent inference audit PASS.
- **Candidate fixed inference:** 3-month policy lookback, 24/24 minimum primary groups, circular 12-slot moving-block bootstrap, 10,000 replicates, seed 20261004, type-7 95% interval.
- **Next admissible action:** explicit human acceptance of the exact SPEC-FXMP-001-v02 SHA-256 above.
- **Not admissible yet:** market-outcome calculation, ALIGNED-vs-OPPOSED return comparison, P/L, Sharpe, broker/live action.
