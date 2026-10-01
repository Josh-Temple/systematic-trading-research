---
id: HCON-CSM-I1-20261001
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: ACCEPTED
human_decision_id: HDEC-CSM-002-20261001
accepted_at: 2026-10-01T21:35:55+09:00
accepting_human: Current human user; repository-linked GitHub login Josh-Temple
accepted_spec_sha256: e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90
frozen_spec_sha256: a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
  - type: derived_from
    target: DEC-CSM-003-FREEZE-20261001
---

# Human contract — exact acceptance receipt

## Decision receipt

**ACCEPTED** — the current human user explicitly accepted the exact pre-freeze bytes of SPEC-CSM-002-v01 identified by SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90` and replied: **「承認します 進めて下さい」**.

- Human decision ID: `HDEC-CSM-002-20261001`.
- Acceptance time: `2026-10-01T21:35:55+09:00`.
- Acceptance source: direct reply in this conversation to the request naming the exact SHA-256.
- Accepted proposal ref: `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`.
- Accepted file Git blob SHA-1: `a073e77dec14337ee20609ed6136e50a8c1e76e2`.
- Accepted file SHA-256: `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`.
- Frozen file Git blob SHA-1: `7fe114e2fcfa33b0565b51c717455abd8837d5d9`.
- Frozen file SHA-256: `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`.
- Repository-linked GitHub login shown for the current integration PR: `Josh-Temple`; this is an account reference, not a claim about legal identity.

## Exact contract accepted

The accepted design asks whether, among AUD/CAD/CHF/EUR/GBP/JPY/NZD/USD, the currency with the strongest previous-calendar-month synchronous spot appreciation minus the weakest has a positive mean synchronous ECB reference-to-reference spot log return over the next calendar month, for target months 2010-01 through 2026-09. It tests retrospective latest-vintage reference association only, not returns that could have been earned with public information.

| Dimension | Accepted choice |
|---|---|
| Universe | AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD; all 56 ordered pairs; no filters |
| Formation / target | One calendar month formation followed by one calendar month target |
| Target period | 2010-01 through 2026-09 inclusive; source boundary 2009-11-01 through 2026-09-30 |
| Source | Seven ECB EXR daily series D.CCY.EUR.SP00.A; EUR is the synthetic numeraire |
| Outcome / claim | Synchronous reference-to-reference pair log return; retrospective latest-vintage association only; no causal availability, executable entry, or net profitability claim |
| Primary statistic | Arithmetic mean of eligible target log returns in basis points |
| Dependence interval | Circular moving-block bootstrap over the full calendar-slot grid; block length 12; 10,000 replicates; seed 20261001; type-7 percentile; two-sided 95% interval |
| Baseline | Uniform mean over all 56 ordered log-return pairs is analytically zero; no sampled random-pair backtest |
| Data sufficiency | At least 120 eligible target months and at least 80% scheduled coverage |
| Decision rule | Insufficient: HOLD; mean ≤ 0: NOT_SUPPORTED / DEPRIORITIZE; mean > 0 with lower interval ≤ 0: INCONCLUSIVE / HOLD; mean > 0 with lower interval > 0: PROMISING_EXPLORATORY / ADVANCE_TO_SEPARATE_ECONOMIC_SCREEN_DESIGN |
| Search / costs | One empirical candidate; no horizon, universe, subperiod, seed, block-length or filter search. Cost, carry and financing stay UNOBSERVED. |

The interval and thresholds are fixed design rules. Their acceptance is not evidence that the screen is adequately powered or economically profitable.

## Approval-to-freeze byte transition

| Field | Before acceptance / freeze | Frozen file |
|---|---|---|
| `status` | `HUMAN_BOUNDARY` | `ACTIVE` |
| `freeze_status` | `PROPOSED_NOT_FROZEN` | `FROZEN` |
| `frozen_at` | absent | `2026-10-01T21:35:55+09:00` |
| `human_decision_ref` | absent | `DEC-CSM-003-FREEZE-20261001` |

Only the SPEC frontmatter changed when recording the freeze. The accepted contract body remains byte-for-byte unchanged. The accepted pre-freeze digest and frozen post-metadata digest are both retained above. The original human brief that preceded the proposal was not available in the reviewed repository artifacts.

## Execution boundary

This receipt accepts and freezes the science contract. It does not authorize market-data capture or analysis. The source full-history/vintage readiness, D's post-freeze configuration identity, independent E audit, data-exposure disposition, durable destination/access ledger, and trusted receipt/process-isolation conditions remain open. The I2 gate is CLOSED, no market outcome has been computed, and no run instruction is issued to X.
