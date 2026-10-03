---
id: SPEC-FXMP-001-v01
type: Specification
research_line_id: RL-FXMP-001
created_at: 2026-10-03
status: PROPOSED
freeze_status: PROPOSED_NOT_FROZEN
tests_hypothesis: HYP-FXMP-001
data_roles_allowed:
  - EXPLORATORY_DISCOVERY
relations:
  - type: tests_hypothesis
    target: HYP-FXMP-001
---

# Proposed break-aware policy-alignment screen

This file incorporates source-semantic corrections found before any FX outcome access. It is not frozen.

## 1. Price side

If later bound to the existing frozen CSM design, preserve its fixed universe, price selection, target grid, price source, calendar and next-month spot outcome exactly. Do not rerank pairs using policy data.

For each target month k, let:
- a = price-selected strongest currency;
- b = price-selected weakest currency;
- y_k = the already-defined next-month selected-pair spot log return.

The policy feature must be built and persisted before y_k is joined or calculated.

## 2. Policy source

Source family only:

- provider: Bank for International Settlements
- dataflow: `BIS,WS_CBPOL,1.0`
- frequency: monthly
- unit: per cent per year
- collection: end of period
- monthly semantics: value of the last business day of the reference month, derived from the BIS daily series
- series:
  - AUD: `M.AU`
  - CAD: `M.CA`
  - CHF: `M.CH`
  - EUR: `M.XM`
  - GBP: `M.GB`
  - JPY: `M.JP`
  - NZD: `M.NZ`
  - USD: `M.US`

Source substitution is forbidden after freeze.

## 3. Proposed policy feature

Let r_i(m) be the BIS monthly end-of-period policy-rate observation for currency area i in calendar month m.

For target month k:

`p_i(k) = r_i(k-1) - r_i(k-4)`

and for the price-selected pair:

`z_k = p_a(k) - p_b(k)`.

Classification:

- ALIGNED: z_k > 0
- NEUTRAL: z_k = 0
- OPPOSED: z_k < 0

No epsilon threshold, no rate-level ranking, no imputation, no substitute national rate.

The three-month lookback is a proposed scientific choice, not yet human-frozen.

## 4. Source-break rule

The BIS series are deliberately long, spliced policy-rate series. A numerical change must not be interpreted as a monetary-policy move when the comparison crosses a documented change in the identity of the rate being represented.

For either selected currency, if the interval used to compute p_i crosses a documented BIS policy-instrument identity change or contains a documented period in which no policy rate is adopted, classify the policy feature as unavailable and do not calculate z_k.

Required reason codes:

- `POLICY_RATE_UNAVAILABLE`
- `POLICY_INSTRUMENT_BREAK_CROSSED`
- `POLICY_SOURCE_MISSING`
- `POLICY_SOURCE_INVALID`

No rollback to a different month and no replacement with a corridor midpoint, money-market rate, bond yield, OIS or another provider is permitted.

Known in-sample semantic hazards from the BIS 18 Jun 2026 documentation include:

- Switzerland: midpoint of the SNB target range through 12 Jun 2019; SNB policy rate from 13 Jun 2019.
- Euro area: main refinancing operation rate through 17 Sep 2024; deposit facility rate from 18 Sep 2024.
- Japan: no policy rate adopted from 4 Apr 2013 through 20 Sep 2016; additional regime/instrument changes occur before and after that interval.

Australia, Canada, New Zealand, United Kingdom and United States have no documented main-policy-instrument identity change inside the proposed 2010-2026 test interval in the reviewed BIS documentation.

## 5. Timing boundary

This first historical test is retrospective latest-vintage association only.

It does not claim that:
- today's BIS historical series was identically available in real time;
- a policy decision effective on the same calendar boundary was tradable before the FX reference observation;
- publication timestamps are known merely from monthly dates.

Before any stronger causal/executable claim, exact announcement/effective/publication timing must be separately qualified.

## 6. Primary estimand

`D = mean(y_k | ALIGNED) - mean(y_k | OPPOSED)`.

Primary hypothesis: D > 0.

NEUTRAL is descriptive and is not pooled with either primary group.

## 7. Proposed inference

Candidate method, still requiring freeze:

- preserve the full calendar-slot grid;
- circular moving-block bootstrap;
- block length 12 calendar slots;
- 10,000 replicates;
- fixed seed chosen and recorded before outcome access;
- resample slots, then recompute the ALIGNED-minus-OPPOSED difference inside each replicate;
- if any replicate has no eligible ALIGNED or OPPOSED observations, inference fails closed.

Operational minimum proposed before outcome access:
- >=24 eligible ALIGNED slots;
- >=24 eligible OPPOSED slots.

These are operational minima, not a statistical power guarantee.

## 8. Decision rule proposal

After source lock, deterministic implementation, independent audit and explicit human freeze:

- invalid source / failed inference / insufficient group counts: HOLD or NOT_APPLICABLE as appropriate;
- D <= 0: NOT_SUPPORTED / DEPRIORITIZE this exact hypothesis;
- D > 0 and lower 95% interval <= 0: INCONCLUSIVE / HOLD;
- D > 0 and lower 95% interval > 0: PROMISING_EXPLORATORY / advance only to a separately designed unused/prospective economic test.

No historical result authorizes a live rule.

## 9. Forbidden search

No result-driven changes to:
- policy lookback;
- currency universe;
- price formation/holding horizon;
- break handling;
- ALIGNED/OPPOSED threshold;
- subperiod;
- side;
- bootstrap block length/seed;
- source/provider.

Any later economic-momentum, Taylor-rule, OIS, sovereign-yield or text-based monetary-policy model is a separate preregistered research line.
