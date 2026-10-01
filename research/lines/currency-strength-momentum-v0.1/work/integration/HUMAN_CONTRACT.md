---
id: HCON-CSM-I1-20261001
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: NOT_APPROVED
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
---

# Human contract — acceptance receipt status

## Decision status

**NOT_APPROVED.** No human freeze receipt or exact-byte acceptance was present in the fresh-read proposal artifacts. The current instruction authorizes execution of Packet I; it does not accept the proposed science contract.

- Proposed SPEC: SPEC-CSM-002-v01
- Proposal ref: e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff
- Git blob SHA-1: a073e77dec14337ee20609ed6136e50a8c1e76e2
- File SHA-256: e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90
- freeze_status: PROPOSED_NOT_FROZEN
- human decision ID: NOT_RECORDED
- acceptance time: NOT_RECORDED
- accepted specification SHA-256: null
- original human brief: NOT_AVAILABLE_IN_THE_REVIEWED_REPOSITORY_ARTIFACTS

The PR #31 description summarizes the proposal. It is not the missing original brief or an acceptance receipt. Approval has not been inferred from the existence of the proposal, worker results, D tests, or the instruction to run Packet I.

## Exact contract offered for decision

Accepting this document means accepting the exact bytes of SPEC-CSM-002-v01 identified above. The suggested study asks whether the previous calendar month's synchronous spot appreciation of the strongest currency minus the weakest, among AUD/CAD/CHF/EUR/GBP/JPY/NZD/USD, has a positive mean over the next calendar month's synchronous ECB reference-to-reference spot log return for target months 2010-01 through 2026-09.

The proposed contract fixes:

| Dimension | Exact proposed choice |
|---|---|
| Universe | AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD; all 56 ordered pairs; no filters |
| Formation / target | One calendar month formation followed by one calendar month target |
| Target period | 2010-01 through 2026-09 inclusive; source boundary 2009-11-01 through 2026-09-30 |
| Source | Seven ECB EXR daily series D.CCY.EUR.SP00.A; EUR is the synthetic numeraire |
| Outcome / claim | Synchronous reference-to-reference pair log return. Retrospective latest-vintage association only; no causal availability, executable entry, or net profitability claim |
| Primary statistic | Arithmetic mean of eligible target log returns in basis points |
| Dependence interval | Circular moving-block bootstrap over the full calendar-slot grid; block length 12; 10,000 replicates; seed 20261001; type-7 percentile; two-sided 95% interval |
| Baseline | Uniform mean over all 56 ordered log-return pairs is analytically zero; no sampled random-pair backtest |
| Data sufficiency | At least 120 eligible target months and at least 80% scheduled coverage |
| Decision rule | If insufficient, HOLD; if mean ≤ 0, NOT_SUPPORTED / DEPRIORITIZE; if mean > 0 with lower interval ≤ 0, INCONCLUSIVE / HOLD; if mean > 0 with lower interval > 0, PROMISING_EXPLORATORY / ADVANCE_TO_SEPARATE_ECONOMIC_SCREEN_DESIGN |
| Search / costs | One empirical candidate; no horizon, universe, subperiod, seed, block-length or filter search. Cost, carry and financing stay UNOBSERVED. |

The interval and thresholds are proposed research-design rules, not evidence that the screen is adequately powered or economically profitable.

## Decision request

Please explicitly accept or decline SPEC-CSM-002-v01 at SHA-256 e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90. If accepted, the receipt must identify the decision, the exact SHA-256, the decision date, and the accepting human. If changes are requested, create and review a new specification version; do not edit this proposed version in place.

Freezing the research contract would **not** authorize market data access. Packet E's independent audit, source and data-access blockers, the Integrator's all-PASS gate, and a separate X instruction would still be required.

