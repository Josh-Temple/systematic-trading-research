---
type: Specification
specification_id: SPEC-JP225-FORECAST-001-v01
research_line_id: RL-JP225-PROSPECTIVE-001
status: PROPOSED_NOT_FROZEN
created_at: 2026-10-05
market_outcome_access: CLOSED
---

# SPEC-JP225-FORECAST-001-v01 — Phase 0 candidate

## 1. Scientific question

For prospectively generated JP225 intraday forecast events, does a frozen AI system using target-market data, point-in-time cross-market/fundamentals/news, and status-preserving relevant repository research forecast the sign of the same-day return better than:

1. a neutral no-change baseline; and
2. an otherwise comparable JP225-market-only AI system?

A secondary question is whether the repository-research layer adds forecast value beyond market + cross-market/fundamentals/news alone.

This specification evaluates forecast quality only. It does not evaluate a tradable entry/exit rule.

## 2. Event timing and eligibility

Candidate v0.1 timing:

- timezone: `Asia/Tokyo`;
- forecast cutoff: 09:00:00 JST;
- target start: 09:00:00 JST;
- target end: 15:30:00 JST on the same calendar day;
- eligible date: scheduled JPX cash-equity trading day, subject to the exact-XM quote availability rules below.

JPX cash-equity trading hours are used only to define the intended Japanese daytime session. The research outcome itself remains exact XM MT5 `JP225Cash`, not a substituted JPX, futures, OANDA, or Dukascopy series.

No ex-post exclusion may be added because a day was difficult, volatile, news-heavy, or forecast incorrectly.

## 3. Reference instrument and outcome semantics

Instrument:

- exact XM MT5 `JP225Cash`;
- best Bid/Ask tick semantics from the qualified XM source route;
- source identity, server identity, timezone mapping, and timestamp semantics must pass the line's readiness gate before formal scoring begins.

Quote construction:

- `mid = (bid + ask) / 2`.

Start price:

- last valid Bid/Ask tick with mapped timestamp `<= 09:00:00 JST`;
- tick must be no older than 60 seconds before cutoff;
- otherwise the event is `NO_FORECAST_REQUIRED_MARKET_INPUT_MISSING`.

End price:

- first valid Bid/Ask tick with mapped timestamp `>= 15:30:00 JST`;
- tick must occur within 60 seconds after the endpoint;
- otherwise the market result is `MARKET_OUTCOME_UNAVAILABLE`.

Primary realized continuous outcome:

    realized_return_bps = 10,000 * ln(end_mid / start_mid)

Primary binary outcome:

    Y_up = 1 if end_mid > start_mid
    Y_up = 0 otherwise

An exactly unchanged midpoint counts as non-up for the binary score and retains zero continuous return.

No alternative provider may be used to rescue a missing formal outcome for the same event.

## 4. Forecast outputs

Every scored AI system must emit before outcome access:

- `p_up`;
- `forecast_return_bps`;
- `top_drivers`;
- `counterevidence`;
- `invalidation_conditions`;
- `source_refs`;
- `forecast_system_version`;
- observable model identifier when available.

Structural rules:

- `p_up` finite in [0.01, 0.99];
- return forecast finite;
- explanations do not alter numerical scores;
- malformed output is `FORECAST_INVALID`, not a scientific negative result.

A separate action field may state `NO_TRADE`, but action choice does not remove the market forecast from scoring.

## 5. Comparison systems

### B0 — neutral baseline

- `p_up = 0.50`;
- `forecast_return_bps = 0`.

### A1 — frozen JP225-market-only AI

Permitted input:

- event date / weekday;
- cutoff timestamp;
- current XM JP225Cash Bid, Ask, Mid;
- deterministic JP225Cash midpoint returns ending at cutoff for 1 hour, 4 hours, and 24 hours;
- deterministic JP225Cash midpoint high-low range in basis points for 4 hours and 24 hours;
- current Bid/Ask spread in basis points;
- explicit missingness flags.

No news, macro/fundamental data, other markets, repository results, or future-event schedule may be shown to A1.

### A2 — frozen market + cross-market/fundamentals/news AI

Receives all A1 inputs plus a frozen point-in-time snapshot. Before formal freeze, the source contract must identify exact required/optional fields and qualified routes. Candidate categories are bounded to:

- USD/JPY state at cutoff;
- prior U.S. equity-session information and other cross-market items only where a qualified point-in-time route is frozen;
- current BOJ and Fed policy settings;
- qualified Japan/U.S. sovereign-yield observations available by cutoff;
- official macro releases published by cutoff;
- official central-bank / finance-ministry communications published by cutoff;
- pre-cutoff timestamped JP225-relevant news from the frozen permitted source set;
- scheduled official Japan/U.S. releases or central-bank events between cutoff and 15:30, if available from a qualified calendar route.

A category without a qualified point-in-time route must not be silently substituted or reconstructed later.

### A3 — A2 + status-preserving repository research AI

Receives all A2 inputs plus a repository snapshot pinned before the first scored event.

Initial permitted scope:

- `research/lines/jp225-ema-timeofday-v0.1/CURRENT.md`;
- `research/lines/jp225-us-lead-reversal-v0.1/CURRENT.md`;
- later directly relevant JP225 research only if explicitly added before formal freeze.

The quarantined/deferred PR #59 DataCube line must not be represented as clean outcome-unviewed evidence.

The snapshot must preserve labels including UNTESTED, BLOCKED, exploratory, negative/null, proxy-only, consumed, quarantined, and deferred. A3 must not convert an untested or proxy result into an established predictor.

## 6. Information cutoff and provenance

Only information observable at or before 09:00:00 JST may influence a forecast.

For every material item preserve where feasible:

- source identity;
- URL or immutable identifier;
- `published_at`;
- `observed_at`;
- `retrieved_at`;
- bounded content/value snapshot actually used;
- revision/vintage status when relevant;
- retrieval status.

Post-cutoff information may be used only in later error attribution.

Forecast records are append-preserving. Corrections are new records; an issued forecast is never overwritten.

## 7. Event / observation states

- `FORECAST_ISSUED`;
- `FORECAST_INVALID`;
- `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`;
- `NO_FORECAST_REQUIRED_MARKET_INPUT_MISSING`;
- `NO_FORECAST_REQUIRED_INPUT_MISSING`;
- `SOURCE_RETRIEVAL_FAILED`;
- `NON_ELIGIBLE_SESSION`;
- `MARKET_OUTCOME_UNAVAILABLE`;
- `SCORING_FAILED`.

Observation status is separate from market result and scientific interpretation.

## 8. Scoring

Primary per-forecast score:

    Brier = (p_up - Y_up)^2

Lower is better.

Primary comparison on matched events:

    mean(Brier_A3 - Brier_A1)

Negative values favor A3.

Baseline sanity comparison: A3 versus B0.
Key secondary comparison: A3 versus A2.

Secondary continuous metric:

    MAE_bps = mean(abs(forecast_return_bps - realized_return_bps))

Directional accuracy is descriptive, not primary.

## 9. Evaluation cohort and stopping rule

Frozen v0.1 benchmark:

- 60 eligible events with valid A3/A1 matched forecasts and available exact-XM outcomes;
- A1/A2/A3 remain unchanged throughout those 60 matched events.

Do not stop early because results look good or bad.

Administrative stop is required for outcome leakage, mutable issued records, invalid source identity/time mapping, changed scoring semantics, forbidden inputs, or incomplete event accounting. Administrative stop is not a scientific result.

## 10. Daily forecast-review loop

For each eligible date:

1. gather and freeze the pre-cutoff input snapshots;
2. issue and hash B0/A1/A2/A3 outputs;
3. preserve the issued forecast unchanged;
4. after 15:30, obtain the qualified outcome if available;
5. compute deterministic scores;
6. record factual forecast error separately from interpretation;
7. record bounded error attribution and next observation without modifying v0.1.

Candidate attribution categories before operation:

- target-market continuation/reversal;
- USD/JPY / cross-market mismatch;
- rate/yield signal mismatch;
- unexpected post-cutoff event;
- source missingness;
- narrative overconfidence;
- other, with free-text detail but no retroactive rule change.

## 11. Challenger reviews

After 20 and 40 completed matched events:

- review accumulated errors;
- a challenger may be proposed under a new version;
- preserve evidence used to design it;
- mark it adaptive/exploratory relative to that evidence.

The original v0.1 benchmark continues unchanged to 60 events.

## 12. End-of-cohort decision

`ADVANCE_TO_INDEPENDENT_PROSPECTIVE_REPLICATION` is permitted only if:

- mean Brier(A3) < mean Brier(A1); and
- mean Brier(A3) < mean Brier(B0).

This is a minimum gate, not proof of a durable trading edge.

If A3 fails either comparison, do not rescue the same cohort by changing time window, weekday subset, probability threshold, source subset, news category, market-feature lookback, or repository subset and call it validated.

A3 versus A2 may support a separate conclusion about incremental repository-research value.

## 13. Source/readiness gate

Before the first scored forecast, establish without using future outcomes for selection:

1. exact XM MT5 `JP225Cash` symbol/server identity;
2. Bid/Ask tick timestamp semantics;
3. XM server-time ↔ UTC/JST mapping including DST handling if applicable;
4. ability to obtain pre-cutoff 1h/4h/24h features without future leakage;
5. deterministic 09:00 and 15:30 quote selection;
6. required A2 source routes and point-in-time capture rules;
7. A3 repository-ref pinning;
8. append-preserving forecast storage;
9. deterministic scoring;
10. synthetic tests for cutoff leakage, timestamp edges, missingness, malformed forecasts, scoring, and non-trading-day handling.

Failure leaves the scored cohort CLOSED. It does not test the forecasting hypothesis.

## 14. Exploratory prospective dry runs before readiness PASS

Dry runs are permitted to exercise the human/AI forecast-review workflow before the source gate passes if:

- every record is labeled `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`;
- no dry-run event later enters the frozen 60-event cohort;
- missing exact XM start/end data are not repaired with another provider;
- dry-run results do not change the v0.1 scientific conditions;
- any improvement idea becomes a separate candidate/challenger record.

## 15. Broker boundary

This line does not submit orders, choose position size, or claim forecast skill equals trading profitability.

XM is the exact reference/execution environment identity for this forecast outcome, but any later live trading decision rule must be separately specified and evaluated.

## 16. Human freeze boundary

The user has approved proceeding with the JP225 forecast-review research line. Formal activation of the scored v0.1 cohort still requires explicit acceptance of the completed exact specification after readiness fields are pinned.

Until then:

- status remains `PROPOSED_NOT_FROZEN`;
- scored cohort access remains CLOSED;
- exploratory prospective dry runs are allowed under Section 14.
