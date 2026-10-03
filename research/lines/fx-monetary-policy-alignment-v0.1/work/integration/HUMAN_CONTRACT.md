---
id: HCON-FXMP-I1-20261004
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: ACCEPTED
human_decision_id: HDEC-FXMP-001-20261004
accepted_at: 2026-10-04T07:47:20+09:00
accepting_human: Current human user; repository-linked GitHub login Josh-Temple
accepted_spec_sha256: dfcdc8e6d240539fca1afdc5bafd3202bd0e0648fdc1c13c7224917fd7a66040
accepted_spec_git_blob_sha1: f19f611648253e7fad23fa53b6c229addc1d6711
accepted_spec_bytes: 12201
frozen_spec_sha256: 6087910862dfc710f5fe64f16cd0067a399487e3de12e20f930f50024419b741
frozen_spec_git_blob_sha1: eb79d2c4dbd4e4b13ffbd70aed325a1e39c50c6c
frozen_spec_bytes: 12260
relations:
  - type: uses_specification
    target: SPEC-FXMP-001-v02
  - type: derived_from
    target: DEC-FXMP-002-FREEZE-CANDIDATE-20261004
---

# Human contract — exact FXMP science freeze acceptance

## Decision receipt

**ACCEPTED** — the current human user explicitly accepted the exact pre-freeze bytes of `SPEC-FXMP-001-v02` identified by SHA-256:

`dfcdc8e6d240539fca1afdc5bafd3202bd0e0648fdc1c13c7224917fd7a66040`

The user replied in this conversation:

**「承認します。進めて下さい」**

Acceptance time: `2026-10-04T07:47:20+09:00`.

Accepted pre-freeze identity:

- Git blob SHA-1: `f19f611648253e7fad23fa53b6c229addc1d6711`
- bytes: `12,201`
- SHA-256: `dfcdc8e6d240539fca1afdc5bafd3202bd0e0648fdc1c13c7224917fd7a66040`
- identity workflow run: `37158352342`
- PR at acceptance boundary: `#43`
- PR head before freeze metadata update: `06c2d7dbc9bfd89c4c4990a1effbf49fd77da6e6`

## Accepted scientific choices

The accepted contract fixes, before market-outcome access:

- dependency on the frozen `SPEC-CSM-002-v01` price-selection/outcome contract;
- BIS `WS_CBPOL` monthly end-of-period policy rates as the only policy predictor source;
- exact three-calendar-month policy-rate change `r(k-1)-r(k-4)`;
- sign-only ALIGNED / NEUTRAL / OPPOSED classification with no epsilon threshold;
- conservative CHF/EUR instrument-switch and JPY no-policy-rate fail-closed guards;
- primary estimand `mean(y|ALIGNED)-mean(y|OPPOSED)`;
- minimum 24 eligible ALIGNED and 24 eligible OPPOSED slots;
- full calendar-slot grid;
- circular 12-slot moving-block bootstrap;
- 10,000 replicates;
- Python `random.Random` seed `20261004`;
- type-7 two-sided 95% percentile interval;
- empty primary group in any bootstrap replicate => inference failure without retry;
- retrospective latest-vintage EXPLORATORY_DISCOVERY claim only;
- no rescue tuning on the same historical sample;
- a separate unused/prospective test before any tradable-edge claim.

## Freeze transition boundary

Only specification frontmatter may change when recording the freeze:

| Field | Accepted pre-freeze value | Frozen value |
|---|---|---|
| `status` | `HUMAN_BOUNDARY` | `ACTIVE` |
| `freeze_status` | `PROPOSED_NOT_FROZEN` | `FROZEN` |
| `frozen_at` | absent | `2026-10-04T07:47:20+09:00` |
| `human_decision_ref` | absent | `HDEC-FXMP-001-20261004` |

The scientific body must remain unchanged.

The frozen post-metadata Git blob and SHA-256 will be appended to repository records after exact CI identity verification.

## Execution boundary

This receipt authorizes the **science freeze only**.

It does not authorize market-outcome access, CSM outcome generation, FXMP return comparison, P/L, Sharpe, broker actions, paper trading, or live trading.

A separate final integration gate must be evaluated after the frozen-file identity is verified.


## Frozen identity verification

The accepted scientific body was frozen by metadata-only transition and independently verified in GitHub Actions.

- frozen Git blob SHA-1: `eb79d2c4dbd4e4b13ffbd70aed325a1e39c50c6c`
- frozen bytes: `12260`
- frozen SHA-256: `6087910862dfc710f5fe64f16cd0067a399487e3de12e20f930f50024419b741`
- freeze integrity workflow run: `37159665711`
- verification result: **SUCCESS**
- scientific body unchanged from accepted pre-freeze bytes: **true**

The verified transition is exactly:

- `status: HUMAN_BOUNDARY -> ACTIVE`
- `freeze_status: PROPOSED_NOT_FROZEN -> FROZEN`
- add `frozen_at: 2026-10-04T07:47:20+09:00`
- add `human_decision_ref: HDEC-FXMP-001-20261004`

No scientific-body edit occurred during freeze.
