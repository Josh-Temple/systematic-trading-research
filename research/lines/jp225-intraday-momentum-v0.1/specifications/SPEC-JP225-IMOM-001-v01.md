---
id: SPEC-JP225-IMOM-001-v01
type: StrategyExperimentSpecification
research_line_id: RL-JP225-IMOM-001
created_at: 2026-10-04
status: FROZEN_PRE_OUTCOME
market_outcome_access: false
---

# JP225 / Nikkei 225 Intraday Momentum — Specification v0.1

## 1. Purpose

Test a single literature-motivated same-day intraday momentum relation on official OSE Nikkei 225 mini transaction data without parameter search.

This is a confirmatory historical test on a sample not used in the cited Japan study, followed by a separately locked 2026 holdout only if 2025 advances.

## 2. Instrument

OSE Nikkei 225 mini.

Use only quarterly contract months: March, June, September, December.

Contract selection for each eligible TSE date is calendar-deterministic:

1. compute the nearest quarterly contract whose official last trading day is not before that date;
2. call that the front quarterly contract for the date;
3. a date is eligible only if the same contract was also the front quarterly contract on the previous eligible TSE date.

This excludes the first eligible day after a front-quarter roll and avoids cross-contract early returns.

Do not choose contracts from realized volume, return, spread, or model performance.

## 3. Calendar

Use TSE cash-market business days only.

OSE holiday-trading sessions when the TSE cash market is closed are excluded.

For v0.1 the relevant 2025 TSE cash hours are:

- open 09:00 JST;
- close 15:30 JST.

OSE Nikkei 225 mini trades through these timestamps.

## 4. Source

Primary intended source: official JPX/OSE J-Quants DataCube Nikkei 225 mini transaction ticks.

Required before outcome calculation:

- exact DataCube product/dataset identity;
- acquisition date;
- contract codes;
- timestamp timezone and encoding;
- transaction-price field semantics;
- source file hashes;
- coverage report for required one-minute windows;
- license/storage decision.

Trade ticks are not BID/ASK quotes.

## 5. Point-price mapping

For each required clock boundary, use the **first valid transaction at or after the boundary and no later than boundary + 60 seconds**.

Required boundaries:

- previous eligible TSE date 15:30:00 JST;
- current date 09:30:00 JST;
- current date 15:00:00 JST;
- current date 15:30:00 JST.

No interpolation, nearest-neighbor outside the 60-second window, forward fill, midpoint reconstruction, or synthetic quote is allowed.

If a required boundary has no valid transaction, that date is unavailable and produces no outcome.

If multiple trades share an indistinguishable timestamp and source ordering cannot establish a unique first trade, the point is unavailable unless source qualification proves a deterministic source ordering rule.

## 6. Predictor

For eligible date t:

`early_return_t = P_t(09:30) / P_prev(15:30) - 1`

Both prices must be from the same quarterly front contract.

The predictor is known by 09:31 JST at the latest under the allowed +60-second mapping.

## 7. Target

`late_return_t = P_t(15:30) / P_t(15:00) - 1`

This is the final 30 minutes of the current TSE cash session, measured using the same OSE futures contract.

## 8. Primary predictability statistic

Estimate by OLS across eligible dates:

`late_return_t = alpha + beta * early_return_t + error_t`

Primary direction: `beta > 0`.

Inference is a deterministic paired-day bootstrap:

- resampling unit: eligible date pair `(early_return_t, late_return_t)`;
- replications: 10,000;
- seed: 2252025;
- RNG: 32-bit LCG:
  - x0 = seed unsigned 32-bit;
  - x[n+1] = (1664525*x[n] + 1013904223) mod 2^32;
  - U = x / 2^32;
- each replication samples N dates with replacement;
- recompute OLS beta with intercept;
- percentile interval: linear interpolation at positions `(Nboot-1)*0.025` and `(Nboot-1)*0.975`.

If a replication has zero predictor variance, that replication is invalid. More than 1% invalid replications => test status `BOOTSTRAP_DEGENERATE`, no advancement.

## 9. Frozen simple trading translation

No threshold is optimized.

- early_return > 0: LONG;
- early_return < 0: SHORT;
- early_return = 0: NO TRADE.

Gross signed return:

- LONG: `late_return`;
- SHORT: `-late_return`.

Also report signed points using the mapped transaction prices.

This is **gross transaction-price evidence only**. DataCube does not supply a qualified executable BID/ASK model for this line.

For the sign-translation gross mean, use the same 10,000-replication date bootstrap and seed 2252026.

## 10. 2025 confirmation sample

Calendar period: 2025-01-01 through 2025-12-31.

Run once after source and implementation gates pass.

Advancement requires all:

1. at least 180 eligible paired dates;
2. OLS beta > 0;
3. beta bootstrap 95% lower bound > 0;
4. sign-translation gross mean return > 0;
5. sign-translation bootstrap 95% lower bound > 0.

If any fails: `IMOM_NOT_SUPPORTED_2025`.

If data count is below 180: `INSUFFICIENT_2025_EVENTS`.

No secondary analysis may rescue a failed primary decision.

## 11. 2026 holdout

Period: 2026-01-01 through 2026-09-30.

2026 raw market data must not be acquired, parsed, summarized or counted before a durable 2025 advancement receipt is written.

Holdout support requires all:

1. at least 120 eligible paired dates;
2. OLS beta > 0;
3. beta bootstrap 95% lower bound > 0;
4. sign-translation gross mean > 0;
5. sign-translation bootstrap 95% lower bound > 0.

Otherwise classify either `INSUFFICIENT_2026_HOLDOUT_EVENTS` or `IMOM_NOT_SUPPORTED_2026_HOLDOUT`.

## 12. Required descriptive outputs

These do not alter advancement:

- eligible/unavailable day counts and reasons;
- beta point estimate and bootstrap interval;
- alpha;
- Pearson correlation;
- sign-strategy event count;
- long/short/no-trade counts;
- gross mean/median return;
- gross mean/median points;
- win rate;
- break-even additional round-trip cost when gross mean is positive;
- contract-month counts;
- excluded roll-transition dates.

No weekday, month, volatility, VIX, direction-only, magnitude-threshold, second-to-last-half-hour, BOJ-event, stop-loss, take-profit or alternate-time subgroup may be selected from 2025 outcomes.

## 13. Forbidden rescue

After any 2025 outcome is read, do not alter:

- early or late clock boundaries;
- +60-second mapping window;
- quarterly-contract rule;
- calendar eligibility;
- return sign rule;
- return threshold;
- sample dates;
- bootstrap seed/algorithm;
- minimum event counts;
- predictor/target definition;
- side selection;
- volatility/volume/news/event filters.

A failed v0.1 stops.

## 14. Relationship to prior JP225 lines

A result here:

- does not validate XM `JP225Cash`;
- does not alter the EMA5/EMA200 specification;
- does not reopen consumed OANDA proxy samples;
- does not rescue the stopped U.S.-lead reversal line.

## 15. Live boundary

No broker order, leverage, capital allocation or position sizing is authorized.

A positive result would justify a separate executable-economics study with its own preregistration.
