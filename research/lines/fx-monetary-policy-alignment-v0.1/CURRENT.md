---
type: CurrentProjection
research_line_id: RL-FXMP-001
projection_generated_at: 2026-10-03
derived_from_decisions:
  - DEC-FXMP-001-PREOUTCOME-20261003
derived_from_interpretations: []
---

# Current projection — pre-outcome, source-qualified only in part

- **HYP-FXMP-001:** UNTESTED.
- **SPEC-FXMP-001-v01:** PROPOSED_NOT_FROZEN.
- **Market outcome access:** CLOSED.
- **BIS source family:** predictor source identity locked to official BIS bulk archive SHA-256 `707f39206f7c4bc1001ea7f67b182d20e9b2d59fcf6542d0dd566a19f61d7f15`; deterministic 8-area slice SHA-256 `2cf878dbd0b8a98c05db741dc40a14d0b62a7cb6c178f86121937b0d41eb7eee`. Durable raw-byte preservation remains open.
- **Critical source semantics:** instrument/regime breaks exist; Japan has a documented 2013-2016 no-policy-rate interval.
- **Design correction:** break-crossing or unavailable policy windows fail closed.
- **Literature:** supports a bounded incremental-information test but not a mechanical "rate up -> currency up" interpretation.
- **Open human choices:** proposed 3-month lookback and 24/24 group-count minima.
- **Outcome-blind implementation:** PASS at PR head `9e9791676b53d70a7f01ecfac42f139f9ce803b8`; CI run `37130507077`, 12/12 synthetic tests passed.
- **Next action:** independent pre-outcome audit, durable predictor-source preservation, and human freeze of the still-open scientific choices.
- **Existing CSM:** unchanged; its market outcome gate remains closed and no CSM result was accessed for this work.
