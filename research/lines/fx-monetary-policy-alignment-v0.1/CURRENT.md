---
type: CurrentProjection
research_line_id: RL-FXMP-001
projection_generated_at: 2026-10-04
derived_from_decisions:
  - DEC-FXMP-001-PREOUTCOME-20261003
  - DEC-FXMP-002-FREEZE-CANDIDATE-20261004
  - DEC-FXMP-003-FREEZE-20261004
derived_from_interpretations: []
---

# Current projection — frozen science contract, blocked upstream outcome gate

- **HYP-FXMP-001:** UNTESTED.
- **SPEC-FXMP-001-v02:** ACTIVE / FROZEN.
- **Human acceptance:** HDEC-FXMP-001-20261004 at `2026-10-04T07:47:20+09:00`.
- **Accepted pre-freeze identity:** Git blob `f19f611648253e7fad23fa53b6c229addc1d6711`; 12,201 bytes; SHA-256 `dfcdc8e6d240539fca1afdc5bafd3202bd0e0648fdc1c13c7224917fd7a66040`.
- **Frozen identity:** Git blob `eb79d2c4dbd4e4b13ffbd70aed325a1e39c50c6c`; 12,260 bytes; SHA-256 `6087910862dfc710f5fe64f16cd0067a399487e3de12e20f930f50024419b741`.
- **Freeze integrity:** workflow run `37159665711` PASS; scientific body verified unchanged.
- **Market outcome access:** CLOSED / false.
- **Final FXMP gate:** BLOCKED by upstream CSM I2, not by FXMP contract failure.
- **CSM dependency:** frozen CSM SPEC blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`; current CSM I2 is BLOCKED/CLOSED.
- **BIS raw source:** SHA-256 `707f39206f7c4bc1001ea7f67b182d20e9b2d59fcf6542d0dd566a19f61d7f15`.
- **Durable BIS predictor slice:** Git blob `1dc3057e1d370d9c56c721b9caa6d26e7cd5dfba`; SHA-256 `2cf878dbd0b8a98c05db741dc40a14d0b62a7cb6c178f86121937b0d41eb7eee`.
- **Source scope:** qualified for retrospective latest-vintage association; historical point-in-time vintage is not claimed.
- **Semantic guards:** CHF 2019-06 and EUR 2024-09 instrument switches; JPY 2013-04 through 2016-09 policy-rate-unavailable interval; fail closed.
- **Feature implementation:** PASS; outcome-field invariance PASS; independent source/feature audit PASS.
- **Inference implementation:** combined feature+inference synthetic CI 22/22 PASS; independent inference audit PASS.
- **Frozen inference:** three-month policy lookback; 24/24 minimum primary groups; circular 12-slot moving-block bootstrap; 10,000 replicates; seed 20261004; type-7 95% interval.
- **Next admissible action:** remediate and independently reopen the upstream CSM I2 gate under its own frozen contract, then fresh-read/re-evaluate FXMP gate.
- **Not admissible:** HYP-FXMP-001 market-outcome computation, ALIGNED-vs-OPPOSED return result, P/L, Sharpe, broker/live/paper action.
