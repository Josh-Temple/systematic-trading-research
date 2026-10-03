---
id: SPEC-FXMP-001-v02
type: Specification
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: ACTIVE
freeze_status: FROZEN
frozen_at: 2026-10-04T07:47:20+09:00
human_decision_ref: HDEC-FXMP-001-20261004
tests_hypothesis: HYP-FXMP-001
data_roles_allowed:
  - EXPLORATORY_DISCOVERY
relations:
  - type: tests_hypothesis
    target: HYP-FXMP-001
  - type: supersedes
    target: SPEC-FXMP-001-v01
---

# Exact freeze candidate — price momentum × monetary-policy alignment

This is the complete pre-outcome freeze candidate. It does not authorize market-outcome access.

## 1. Scientific question and claim boundary

Question:

> For the fixed AUD/CAD/CHF/EUR/GBP/JPY/NZD/USD universe, is the following-calendar-month spot return of the price-momentum-selected strongest-versus-weakest pair higher when the selected strongest currency has experienced a more restrictive three-calendar-month policy-rate change than the selected weakest currency, compared with the opposite policy-rate ordering?

This is a **retrospective latest-vintage exploratory association**.

It is not:
- a causal monetary-policy estimate;
- a complete model of FX fundamentals;
- a monetary-policy-surprise study;
- an executable-entry or net-profitability claim;
- independent confirmation of the existing currency-strength study.

## 2. Dependency on the frozen price-selection contract

This line does not redefine price momentum.

It binds to the frozen currency-strength contract:

- research line: `RL-CSM-001`
- specification: `SPEC-CSM-002-v01`
- current frozen Git blob SHA-1: `7fe114e2fcfa33b0565b51c717455abd8837d5d9`
- frozen specification SHA-256 already recorded by that line: `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`
- universe: AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD
- target months: 2010-01 through 2026-09 inclusive
- price formation: previous calendar month
- outcome: the same next-calendar-month synchronous ECB reference-to-reference selected-pair spot log return `y_k`.

For each target month k, `a` and `b` must come from the CSM outcome-blind event ledger:
- `a`: price-selected strongest currency;
- `b`: price-selected weakest currency.

This FXMP line may not rerank pairs, change the price horizon, alter the price source, or rescue a CSM skip.

If the CSM slot is unavailable or tied under its frozen contract, the corresponding FXMP slot is unavailable.

## 3. Policy predictor source — exact identity

Provider: Bank for International Settlements.

Dataflow: `BIS,WS_CBPOL,1.0`.

Frequency: monthly.

Unit: per cent per year.

Collection: end of period. BIS monthly values are derived from the daily series and correspond to the value on the last business day of the reference month.

Currency -> BIS monthly key:

- AUD -> `M.AU`
- CAD -> `M.CA`
- CHF -> `M.CH`
- EUR -> `M.XM`
- GBP -> `M.GB`
- JPY -> `M.JP`
- NZD -> `M.NZ`
- USD -> `M.US`

Source lock: `FXMP-SOURCE-LOCK-BIS-CBPOL-001`.

Raw official BIS flat archive identity:
- URL: `https://data.bis.org/static/bulk/WS_CBPOL_csv_flat.zip`
- bytes: 4,134,512
- SHA-256: `707f39206f7c4bc1001ea7f67b182d20e9b2d59fcf6542d0dd566a19f61d7f15`
- CSV member SHA-256: `0ba9441232f120b4237121494e57d5faf4a087615528f411b8ecc3e1750a4ff9`

Deterministic predictor slice:
- period: 2009-09 through 2026-08
- rows: 1,592
- path: `research/lines/fx-monetary-policy-alignment-v0.1/datasets/bis_cbpol_monthly_8ccy_2009-09_2026-08.csv`
- Git blob SHA-1: `1dc3057e1d370d9c56c721b9caa6d26e7cd5dfba`
- bytes: 34,192
- SHA-256: `2cf878dbd0b8a98c05db741dc40a14d0b62a7cb6c178f86121937b0d41eb7eee`

Present rows in the locked slice have:
- `OBS_STATUS=A`: normal value; no break in period;
- `OBS_CONF=F`: free, for publication.

No provider or series substitution is permitted after freeze.

## 4. Fixed policy feature

For target month k, let `r_i(m)` be the locked BIS monthly end-of-period policy rate for currency i.

The fixed lookback is exactly **three calendar months**:

`p_i(k) = r_i(k-1) - r_i(k-4)`.

For the already price-selected pair:

`z_k = p_a(k) - p_b(k)`.

Classification:

- `ALIGNED` if `z_k > 0`;
- `NEUTRAL` if `z_k = 0`;
- `OPPOSED` if `z_k < 0`.

Exact decimal arithmetic is used for policy-rate differences.

No epsilon threshold, smoothing, policy-rate level rank, alternate lookback, or carry substitution is permitted.

The three-month choice is fixed now as one bounded candidate. It is not claimed to be literature-optimal.

## 5. Policy-source semantic guards

The BIS long series contains policy-instrument changes. A numeric difference must not be interpreted as policy momentum across a documented instrument-identity break.

Month-label guards are fixed as follows:

### Switzerland

Instrument switch month: `2019-06`.

Any `p_CHF(k)` interval with:
- old month before 2019-06; and
- new month at or after 2019-06

is unavailable with reason:
`POLICY_INSTRUMENT_BREAK_CROSSED`.

### Euro area

Instrument switch month: `2024-09`.

Any `p_EUR(k)` interval with:
- old month before 2024-09; and
- new month at or after 2024-09

is unavailable with reason:
`POLICY_INSTRUMENT_BREAK_CROSSED`.

### Japan

Conservative unavailable monthly interval:
`2013-04` through `2016-09` inclusive.

Any `p_JPY(k)` interval overlapping that range is unavailable with reason:
`POLICY_RATE_UNAVAILABLE`.

### Other source failures

- missing required endpoint -> `POLICY_SOURCE_MISSING`
- invalid/nonfinite endpoint, invalid currency mapping, invalid month order -> `POLICY_SOURCE_INVALID`

If either selected currency is unavailable, the entire FXMP slot is policy-feature unavailable.

No rollback, carry-forward, interpolation, alternate rate, corridor midpoint reconstruction, bond yield, OIS, or alternate provider is allowed.

## 6. Temporal and outcome-blind boundary

For each target month k:

1. obtain the CSM formation-only pair identity `a,b`;
2. use only policy months through `k-1`;
3. calculate `p_a,p_b,z` and classification;
4. persist and hash the FXMP feature ledger;
5. only after successful persistence may the target outcome `y_k` be joined/calculated under the later outcome gate.

The feature builder must not receive target-month FX values.

Mutating or removing synthetic future-return / target-price fields must leave feature-ledger bytes unchanged.

Current synthetic and independent audits have verified this behavior.

## 7. Primary estimand

Primary estimand:

`D = mean(y_k | ALIGNED) - mean(y_k | OPPOSED)`.

Primary hypothesis:

`D > 0`.

NEUTRAL slots are descriptive only and are not pooled into either primary group.

The test asks whether the fixed policy feature contains incremental information conditional on the already-selected price pair.

## 8. Full target grid and minimum evidence

Preserve the full 201 scheduled CSM target-month slots from 2010-01 through 2026-09.

A slot may remain on the grid with no FXMP outcome contribution because of:
- CSM unavailable/tied slot;
- policy-feature unavailable;
- missing target outcome under the CSM contract.

Do not compress the calendar grid after skips.

Before inference:
- eligible ALIGNED outcome count must be at least **24**;
- eligible OPPOSED outcome count must be at least **24**.

If either group has fewer than 24:
- status: `INSUFFICIENT_EVIDENCE`;
- decision: `HOLD`;
- do not run the bootstrap.

The 24/24 rule is an operational minimum, not a power guarantee.

## 9. Fixed dependence interval

Use a circular moving-block bootstrap on the full calendar-slot grid.

Fixed configuration:

- block length: **12 calendar slots**
- replicates: **10,000**
- PRNG: Python stdlib `random.Random`
- seed: **20261004**
- target statistic inside each replicate: ALIGNED mean minus OPPOSED mean
- percentile interval: two-sided 95%
- percentile method: type-7 linear interpolation
- report 2.5%, 50%, 97.5% bootstrap percentiles

Algorithm:

1. Let N be the number of scheduled calendar slots; under the frozen CSM target grid N=201.
2. For each replicate, initialize an empty resampled index list.
3. Draw `ceil(N/12)` independent start indices using `randrange(N)`.
4. For each start, append 12 consecutive grid indices modulo N.
5. Truncate the concatenated list to N indices.
6. Within those resampled slots, collect valid ALIGNED and OPPOSED y values.
7. If either primary group is empty in any replicate, inference is `FAILED`. Do not retry with a different seed, block length, or replicate count.
8. Compute D for each successful replicate.
9. Sort the 10,000 replicate D values.
10. Type-7 percentile at p uses `h=(B-1)*p`, linear interpolation between floor(h) and ceil(h).

No iid month assumption or pair-level sample-size multiplication is allowed.

## 10. Primary decision rule

After valid source, feature ledger, target join and inference:

- source/identity/persistence/inference failure -> operational STOP; no scientific conclusion
- group minimum not met -> `INSUFFICIENT_EVIDENCE / HOLD`
- `D <= 0` -> `NOT_SUPPORTED / DEPRIORITIZE`
- `D > 0` and lower 95% interval `<= 0` -> `INCONCLUSIVE / HOLD`
- `D > 0` and lower 95% interval `> 0` -> `PROMISING_EXPLORATORY / ADVANCE_TO_SEPARATE_UNUSED_OR_PROSPECTIVE_TEST_DESIGN`

A negative D does not establish a profitable reversal rule.

A positive D does not establish net profitability or causality.

## 11. Allowed descriptive outputs

Allowed after the outcome gate opens:

- D and its fixed bootstrap interval;
- eligible ALIGNED and OPPOSED counts;
- NEUTRAL count;
- unavailable/skip counts by preregistered reason;
- group mean, median and positive-return proportion for ALIGNED / NEUTRAL / OPPOSED;
- source/break coverage counts.

Not allowed from this exploratory run:

- best currency;
- best year/decade;
- policy lookback comparison;
- alternate threshold;
- subperiod selection;
- side-specific rescue;
- volatility filter;
- carry filter;
- OIS/bond-yield substitution;
- Sharpe or leveraged P/L;
- broker execution claim.

## 12. Cost and execution boundary

Spread, slippage, commission, financing, rollover and realised carry are UNOBSERVED in this test.

No broker symbol, order, position size, leverage or live/paper trade is part of the experiment.

## 13. Search and stopping rule

This research family contains one empirical policy-alignment candidate under this specification.

Do not search:
- 1/2/6/12-month policy lookbacks;
- alternate policy-rate definitions;
- different currencies;
- different CSM horizon;
- different target dates;
- alternate break handling;
- thresholded z;
- alternate bootstrap block/seed;
- favourable subperiods.

If this exact candidate is not supported, do not rescue it on the same sample.

Any broader economic-momentum, Taylor-rule, OIS, sovereign-yield, news or text-policy model must be a separately preregistered line.

## 14. Implementation and audit state before freeze

Feature implementation:
- synthetic CI passed;
- future/outcome-field invariance passed;
- independent source/feature audit `AUDIT-FXMP-E-20261004-01` passed with recorded non-scientific limitations.

Inference implementation:
- combined feature + inference CI run `37157939932`: 22/22 tests passed;
- independent inference audit `AUDIT-FXMP-INFERENCE-20261004-01` passed.

No market outcome has been accessed or computed for HYP-FXMP-001.

## 15. Human freeze boundary

This file remains `HUMAN_BOUNDARY / PROPOSED_NOT_FROZEN` until the human user explicitly accepts the exact pre-freeze bytes identified by SHA-256.

Acceptance of this file authorizes only the science freeze.

It does **not** automatically open market-outcome access.

After acceptance, a separate integration receipt must:
- record the accepted SHA-256;
- change only freeze metadata;
- bind exact source / implementation / audit identities;
- confirm the existing CSM dependency is still frozen and unchanged;
- keep outcome access closed until final gate checks pass.

## 16. Confirmation boundary

This 2010-01 through 2026-09 study overlaps prior published FX momentum and monetary-policy literature and is exploratory.

If the result is promising, the next scientific step is a separately frozen unused or prospective test. The same historical sample may not be used to select a new policy lookback, threshold, macro-variable combination or regime filter and then presented as confirmation.
