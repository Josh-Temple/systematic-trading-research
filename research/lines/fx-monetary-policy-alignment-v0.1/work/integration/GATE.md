---
id: GATE-FXMP-I2-20261004
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: BLOCKED
market_outcome_access: false
relations:
  - type: uses_specification
    target: SPEC-FXMP-001-v02
  - type: derived_from
    target: DEC-FXMP-003-FREEZE-20261004
  - type: depends_on
    target: RL-CSM-001
---

# FXMP final outcome-access gate — BLOCKED / CLOSED

## Current decision

- Science contract: **FROZEN**.
- FXMP source qualification: **PASS for retrospective latest-vintage scope**.
- Deterministic policy-feature implementation: **PASS**.
- Independent source/feature audit: **PASS**.
- Inference implementation: **PASS**.
- Independent inference audit: **PASS**.
- Market outcome access: **false**.
- HYP-FXMP-001: **UNTESTED**.

The gate is blocked by the upstream price-selection/outcome dependency, not by an FXMP scientific-contract failure.

## Frozen FXMP identities

- accepted pre-freeze SHA-256: `dfcdc8e6d240539fca1afdc5bafd3202bd0e0648fdc1c13c7224917fd7a66040`
- frozen SPEC Git blob: `eb79d2c4dbd4e4b13ffbd70aed325a1e39c50c6c`
- frozen SPEC SHA-256: `6087910862dfc710f5fe64f16cd0067a399487e3de12e20f930f50024419b741`
- deterministic BIS predictor slice SHA-256: `2cf878dbd0b8a98c05db741dc40a14d0b62a7cb6c178f86121937b0d41eb7eee`
- raw BIS archive SHA-256: `707f39206f7c4bc1001ea7f67b182d20e9b2d59fcf6542d0dd566a19f61d7f15`

## Upstream CSM dependency fresh-read

Fresh read from CSM integration head `6bd9ddc5bc53c37aee3b0d82d1ac2c00c00fd73c`:

- `SPEC-CSM-002-v01`: FROZEN
- frozen CSM SPEC Git blob: `7fe114e2fcfa33b0565b51c717455abd8837d5d9`
- frozen CSM SPEC SHA-256: `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`
- CSM Packet I I1: `PARTIAL_WITH_GAPS`
- CSM I2: `BLOCKED`
- CSM gate: `CLOSED`
- CSM `market_outcome_access=false`
- CSM HYP-CSM-002: `UNTESTED`
- DATA-CSM-002: `PLANNED / NOT_CAPTURED_FOR_EXPERIMENT`
- EXP-CSM-002: `PLANNED / NOT_RUN`

Current CSM gate blockers include:
- stale current I2/E receipt identity pins;
- reproduced compound persistence failure that can leave a success receipt after reported promotion failure;
- independent E result remains PARTIAL_WITH_GAPS / BLOCKED;
- full-history source coverage, missing/status distribution, publication timing/vintage and external calendar authority unresolved;
- production trust root/key distribution unresolved;
- OS isolation, filesystem allowlist, durable destination/access ledger unresolved;
- named outcome-access operator unresolved;
- human exposure dispositions unresolved.

## Why FXMP cannot proceed to outcomes

SPEC-FXMP-001-v02 requires the price-selected pair identities and target outcomes to come from the frozen CSM contract.

Because CSM I2 does not authorize source capture/outcome computation, FXMP may not:
- generate or consume CSM market-outcome data;
- calculate ALIGNED vs OPPOSED target returns;
- run the frozen bootstrap on market outcomes;
- emit D, confidence interval, group return summaries, P/L or Sharpe.

Opening FXMP while CSM is closed would bypass the upstream safety/research gate and violate the frozen dependency.

## Gate condition matrix

| Condition | Status | Evidence |
|---|---|---|
| Exact human acceptance | PASS | HCON-FXMP-I1-20261004 |
| Frozen FXMP science body | PASS | integrity run 37159665711; body unchanged |
| BIS source identity and durable predictor slice | PASS | locked raw/slice hashes; Git-preserved slice |
| Policy semantic guards | PASS | source lock + synthetic/independent audit |
| Feature outcome-blindness | PASS | synthetic CI + independent audit |
| Fixed inference implementation | PASS | combined 22-test CI + independent inference audit |
| CSM frozen dependency identity | PASS | fresh-read exact frozen CSM SPEC |
| CSM outcome-access gate | **BLOCKED** | CSM I2 CLOSED; market_outcome_access=false |
| FXMP final outcome access | **BLOCKED** | upstream dependency unavailable |

## Required condition for reconsideration

Do not reconsider FXMP outcome access until the CSM line independently records a current, valid I2 PASS/OPEN state for the same frozen CSM contract and required event/outcome artifacts can be produced without violating its gate.

At reconsideration, fresh-read:
1. current CSM integration head and gate;
2. frozen CSM SPEC identity;
3. CSM D/E/source/operations evidence;
4. FXMP frozen SPEC identity;
5. BIS predictor-slice identity;
6. current FXMP CI/audit status.

No result-driven FXMP specification change is allowed while waiting for the upstream gate.

## No-result receipt

No HYP-FXMP-001 market outcome, ALIGNED-vs-OPPOSED return difference, bootstrap interval, P/L, Sharpe, broker action or live/paper trade was computed in this integration step.
