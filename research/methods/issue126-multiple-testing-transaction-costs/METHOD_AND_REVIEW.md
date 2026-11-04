# Issue #126 — Multiple-testing research and synthetic transaction-cost checks

Status: **SYNTHETIC_ONLY / NOT_FROZEN / NO_MARKET_DATA / REVIEW_REQUIRED**  
Scope: independent methodology study. **No modification to FXNS PR #125, CSM, FXMP, Horizontal Reaction, or JP225 contracts.**

## 1. Primary-method comparison

| Method | Question | Applicability and risks |
| --- | --- | --- |
| White (2000), Reality Check | After searching many models, does the best one have predictive superiority over a benchmark? | Requires the complete comparison family, consistent losses, and a defensible joint bootstrap preserving time dependence. Can be conservative with many poor alternatives. |
| Hansen (2005), SPA | Does an alternative forecast significantly outperform the benchmark? | Studentization and sample-dependent null can improve power over Reality Check; still needs valid loss differentials, candidate family and resampling assumptions. |
| Bailey et al. (2017), CSCV/PBO | How frequently does the in-sample winner degrade when evaluated out of sample across combinatorial partitions? | Needs comparable candidate scores, defensible partitions and no information leakage. Estimated PBO is **not** a significance p-value or the probability of future trading losses. |
| Harvey, Liu & Zhu (2014), multiple-testing finance | How should extensive factor discovery affect evidential thresholds? | Historical factor-mining evidence is relevant, but their illustrative thresholds are **not** universal thresholds for this study. |

**Decision:** No single procedure is adopted as a universal pass/fail test. Before any real-data study, independently freeze the attempted candidate family (including discarded choices), benchmark, outcome, source, partitions, bootstrap/dependence assumptions, missingness and interpretation rules. Consumed and unused holdout status must remain unchanged.

Primary sources:
- White (2000), *A Reality Check for Data Snooping*: https://doi.org/10.1111/1468-0262.00152
- Hansen (2005), *A Test for Superior Predictive Ability*: https://doi.org/10.1198/073500105000000063
- Bailey, Borwein, López de Prado & Zhu (2017), *The Probability of Backtest Overfitting*: https://escholarship.org/uc/item/4w1110bb
- Harvey, Liu & Zhu, *...and the Cross-Section of Expected Returns*: https://www.nber.org/papers/w20592

## 2. Defined synthetic accounting convention

`cost_fixture.py` implements only a fully filled, two-sided synthetic round trip. It is not a broker interface or a realistic execution-cost estimator.

Price inputs are **midpoints**. Side is +1 for long and -1 for short. Quantity multiplied by price gives synthetic quote-currency PnL. Each half-spread, adverse slippage and adverse impact is a **price-unit** adjustment per fill. Entry/exit fees and holding charges use the same **PnL currency**:

```text
gross = side * quantity * (exit_mid - entry_mid)
spread = quantity * (entry_half_spread + exit_half_spread)
slippage = quantity * (entry_slippage + exit_slippage)
impact = quantity * (entry_impact + exit_impact)
fees = entry_fee + exit_fee
net = gross - spread - slippage - impact - fees - funding_charge
```

**Do not pass already executed bid/ask prices into this midpoint accounting convention**: adding half-spreads again would double-count. The choice of reference price and its relation to execution price must be documented. Costs are uncalibrated, not applicable to actual FX or JP225 trading.

Excluded (must be a separate implementation and review): partial/missed fills, rejected orders, multiple currencies and conversion, funding credits, tick/lot/precision rules, open positions, fees in another currency, venue-specific charges, stale quotes, and real impact modeling.

References:
- SEC, bid-ask spread: https://www.sec.gov/answers/spread.htm
- SEC, effective spread / execution-price conventions: https://www.sec.gov/reports/report-practice-preferencing
- Frazzini, Israel & Moskowitz, *Trading Costs* (2018): https://www.aqr.com/insights/research/working-paper/trading-costs (institutional-equity data, **not** calibration for retail FX or JP225)

## 3. Local deterministic tests

Run from this directory, standard-library Python only:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_cost_fixture.py
```

At creation, the author-controlled local test run passed **9 unittest test methods** (2026-11-04). This is **not** an independently executed CI result; current GitHub commit needs its own reproducibility check.

Tests cover:
1. Zero cost leaves net PnL equal to gross.
2. Both entry and exit adjustments, with a hand-checkable arithmetic fixture.
3. Increasing any nonnegative fixed-fill cost cannot raise net PnL.
4. Long/short direction and zero-turnover behavior; no fabricated fill fees.
5. Invalid side/price/cost, NaN, infinity and arithmetic overflow fail closed.
6. Missing timezone, duplicate/out-of-order synthetic timestamps and invalid prices fail closed.
7. Candidate choice accepts only training scores and frozen candidate order as a tie breaker.
8. Missing/extra candidates, non-synthetic source labels and reused split IDs fail closed.
9. A seeded iid zero-signal illustration shows selection inflation in sample with independent evaluation draws.

The earlier Issue #126 NumPy example is **not** an exact replay of this standard-library fixture. These tests do **not** calculate White RC, Hansen SPA, CSCV/PBO, Sharpe, live costs or a market trading edge.

## 4. Critical internal review (not third-party independent acceptance)

- **Provenance:** split IDs and `source_kind='SYNTHETIC'` are declarative. A caller can mislabel contaminated scores. The code cannot independently attest raw source digests, dataset identity or candidate attempt history. **NOT VERIFIED**.
- **Leakage:** excluding evaluation outcomes from the selection function is useful, but an upstream feature-builder could already leak future information into training scores. This test does not prove full temporal isolation. **NOT VERIFIED**.
- **Search history:** the function checks the declared list only; discarded variants or adaptive reruns might be absent. An immutable attempt ledger is required. **NOT VERIFIED**.
- **Dependence:** iid normal fixtures do not reflect autocorrelated, heteroskedastic or nonstationary market returns. No inferential extrapolation is warranted. **NOT APPLICABLE** to real-data testing.
- **Price/quantity semantics:** binary floats, implicit quote currency, fixed quantity and always-complete fills are insufficient for real clearing/cash accounting. **NOT QUALIFIED**.
- **Independence:** code, expected values, and tests were authored by the same assistant. A genuinely independent reviewer and implementation remain necessary. **NOT RUN**.
- **Automation:** publishing a PR, passing local tests, or reaching green CI is not scientific acceptance.

## 5. Next gates

A. Independent method and arithmetic review against both costs and timestamp fixtures.  
B. Design a host-verified, immutable, outcome-blind data/split/attempt manifest (source hash, candidate fingerprints, trials rejected as well as accepted, test role and temporal cutoffs).  
C. A later, explicit human research-design decision would be required to freeze any multiple-testing method and construct **new synthetic** time-series experiments.  
D. No market outcomes, no cost calibration from live quotes, no frozen study changes, no broker orders.

**Current result:** `SYNTHETIC_TESTS_PASS_LOCAL / DESIGN_PARTIAL / INDEPENDENT_REVIEW_NOT_RUN / NO_MARKET_DATA / NO_TRADING`.
