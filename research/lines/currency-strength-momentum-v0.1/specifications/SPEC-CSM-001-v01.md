---
id: SPEC-CSM-001-v01
type: Specification
research_line_id: RL-CSM-001
version: v0.1
created_at: 2026-10-01
frozen_at: 2026-10-01
freeze_status: FROZEN
tests_hypothesis: HYP-CSM-001
data_roles_allowed:
  - EXPLORATORY_DISCOVERY
outcome_definition: next-calendar-month spot log return of the prior-month strongest-minus-weakest currency pair
metrics:
  - event_count
  - mean_forward_return_bps
  - median_forward_return_bps
  - positive_rate
  - calendar_year_cluster_bootstrap_95pct_ci
  - unavailable_month_count
stopping_or_kill_conditions:
  - no_lookback_search
  - no_holding_period_search
  - no_universe_search
  - no_regime_filter_search
  - no_factor_filter_search
relations:
  - type: tests_hypothesis
    target: HYP-CSM-001
---

# Currency Strength Momentum v0.1 — Frozen Discovery Specification

## Universe

Exactly eight currencies:

AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD.

No currency is added or removed after outcome access.

## Source semantics

Primary source candidate: ECB Exchange Rates (EXR), daily euro foreign exchange reference rates.

Expected series for the seven non-EUR currencies:

EXR.D.AUD.EUR.SP00.A
EXR.D.CAD.EUR.SP00.A
EXR.D.CHF.EUR.SP00.A
EXR.D.GBP.EUR.SP00.A
EXR.D.JPY.EUR.SP00.A
EXR.D.NZD.EUR.SP00.A
EXR.D.USD.EUR.SP00.A

EUR is the common numeraire and is assigned log value 0.

Acquisition boundary:

- start: 1999-01-04
- end: 2026-09-30
- use only observations present in the official source
- do not interpolate missing dates
- use the last available ECB observation in each calendar month as that month-end observation

ECB reference rates are informational reference rates, not executable BID/ASK quotes. Therefore v0.1 is a phenomenon screen only.

## Common-numeraire representation

Let q_i(t) be ECB units of currency i per 1 EUR at month-end t.

For non-EUR currency i:

v_i(t) = -ln(q_i(t))

For EUR:

v_EUR(t) = 0

The prior-month strength score is:

s_i(t) = v_i(t) - v_i(t-1)

Cross-sectional demeaning may be calculated as a diagnostic assertion only; it must not change the ranking.

## Pair selection

At each eligible month-end t:

- strongest = currency with max s_i(t)
- weakest = currency with min s_i(t)
- direction = long strongest / short weakest

If the strongest or weakest rank is not unique because of an exact tie, mark that event unavailable. Do not add a discretionary tie-break.

Deterministic identity check:

max_i,j [s_i(t) - s_j(t)] must equal s_strongest(t) - s_weakest(t).

This confirms that the "currency strength" selection is exactly the best prior-month pair under this definition.

## Forward outcome

For the next month t+1:

y(t+1) =
[v_strongest(t+1) - v_strongest(t)]
-
[v_weakest(t+1) - v_weakest(t)]

Positive y = continuation.
Negative y = reversal.

Events are monthly and non-overlapping.

## Inference

Report:

- number of eligible monthly events
- mean forward return in basis points
- median forward return in basis points
- positive-rate
- calendar-year cluster bootstrap 95% interval for the mean

Bootstrap:

- resample calendar-year clusters with replacement
- 10,000 replications
- seed = 20261001

This is exploratory evidence, not confirmatory evidence.

## Predeclared decision rule

- mean forward return <= 0: DEPRIORITIZE monthly continuation in this exact v0.1 form.
- mean > 0 but the cluster-bootstrap 95% interval includes 0: HOLD as weak / inconclusive Discovery evidence.
- mean > 0 and the 95% interval is entirely above 0: ADVANCE only to a separate execution-aware and factor-decomposition design.

Even an ADVANCE result does not establish a tradeable edge because this source has no executable spread, commission, slippage, financing, or broker-specific rollover.

## Forbidden rescue

After outcome access, do not rescue v0.1 by changing:

- 1-month formation period
- 1-month forward horizon
- the eight-currency universe
- ranking definition
- volatility normalization
- smoothing
- time-of-month
- side filters
- carry filters
- trend filters
- regime filters

Any such change is a new hypothesis/specification and requires new evidence boundaries.
