---
id: DEC-FXMP-003-FREEZE-20261004
type: Decision
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: ACTIVE
relations:
  - type: derived_from
    target: DEC-FXMP-002-FREEZE-CANDIDATE-20261004
  - type: uses_specification
    target: SPEC-FXMP-001-v02
---

# Science contract frozen after exact human acceptance

## Decision

**SPEC-FXMP-001-v02 is FROZEN.**

Human acceptance:
- decision id: `HDEC-FXMP-001-20261004`
- acceptance time: `2026-10-04T07:47:20+09:00`
- accepted pre-freeze SHA-256: `dfcdc8e6d240539fca1afdc5bafd3202bd0e0648fdc1c13c7224917fd7a66040`
- accepted pre-freeze Git blob: `f19f611648253e7fad23fa53b6c229addc1d6711`

Frozen identity:
- Git blob SHA-1: `eb79d2c4dbd4e4b13ffbd70aed325a1e39c50c6c`
- bytes: `12260`
- SHA-256: `6087910862dfc710f5fe64f16cd0067a399487e3de12e20f930f50024419b741`
- freeze integrity run: `37159665711`
- scientific body unchanged: **verified true**

The frozen contract fixes the three-month BIS policy-rate feature, semantic break guards, ALIGNED/NEUTRAL/OPPOSED classification, primary estimand, 24/24 operational minimum, 12-slot circular moving-block bootstrap, 10,000 replicates, seed 20261004, type-7 interval and no-rescue rule.

## Boundary

This decision freezes the scientific contract only.

It does not open market-outcome access. A separate gate record governs access.
