---
type: Specification
specification_id: SPEC-USDJPY-FORECAST-001-v01
research_line_id: RL-USDJPY-OVERNIGHT-001
status: PROPOSED_NOT_FROZEN
created_at: 2026-10-04
market_outcome_access: CLOSED
---

# SPEC-USDJPY-FORECAST-001-v01 — Phase 0 candidate

## 1. Scientific question

For prospectively generated USD/JPY overnight forecast events, does a frozen AI system using market data, point-in-time fundamentals/news, and status-preserving relevant repository research forecast the sign of the next overnight return better than:

1. a neutral no-change baseline; and
2. an otherwise comparable market-only AI system?

A key secondary question is whether repository research adds forecast value beyond market + fundamentals alone.

This specification evaluates forecast quality only. It does not evaluate a tradable entry/exit rule.

## 2. Event timing

Candidate v0.1 timing:

- timezone: `Asia/Tokyo`;
- observation cutoff: 22:00:00 JST;
- eligible observation weekdays: Monday, Tuesday, Wednesday, Thursday;
- horizon end: 08:00:00 JST on the following calendar day;
- nominal horizon: 10 hours.

Friday observations are excluded because the 08:00 JST next-day endpoint can cross the weekly FX close. Sunday observations are excluded because 22:00 JST precedes the ordinary weekly FX open.

No ex-post exclusion may be added because a day was difficult, volatile, news-heavy, or forecast incorrectly.

Scheduled holidays and major event days remain eligible if the reference-feed quote and required inputs satisfy the predeclared availability rules.

## 3. Reference instrument and outcome semantics

Instrument:

- USD/JPY spot-like best Bid/Ask reference stream from the qualified research/reference feed;
- current candidate feed: Dukascopy USD/JPY historical/live-compatible best Bid/Ask tick semantics, subject to this line's own readiness gate;
- this reference feed is not treated as identical to XM or Matsui execution.

Quote construction:

- `mid = (bid + ask) / 2`.

Start price:

- last valid Bid/Ask tick with timestamp `<= 22:00:00 JST`;
- tick must be no older than 60 seconds before cutoff;
- otherwise the event is `NO_FORECAST_REQUIRED_MARKET_INPUT_MISSING`.

End price:

- first valid Bid/Ask tick with timestamp `>= 08:00:00 JST`;
- tick must occur within 60 seconds after the horizon endpoint;
- otherwise the market result is `MARKET_OUTCOME_UNAVAILABLE`.

Primary realized continuous outcome:

```text
realized_return_bps = 10,000 * ln(end_mid / start_mid)
```

Primary binary outcome for probabilistic scoring:

```text
Y_up = 1 if end_mid > start_mid
Y_up = 0 otherwise
```

An exactly unchanged midpoint therefore counts as non-up for the binary score and retains its exact zero continuous return in the continuous record.

## 4. Forecast outputs

Every scored AI system must emit a structured forecast before outcome access:

- `p_up`: probability that `end_mid > start_mid`;
- `forecast_return_bps`: point forecast of the 10-hour log return in basis points;
- `top_drivers`: bounded explanation of the main pre-cutoff drivers;
- `counterevidence`: bounded explanation of the strongest contrary evidence;
- `source_refs`: identities of the snapshot inputs actually used;
- `forecast_system_version`;
- observable model identifier when available.

Structural validity rules:

- `p_up` must be finite and in `[0.01, 0.99]`;
- `forecast_return_bps` must be finite;
- explanations do not alter numerical scores;
- malformed output is `FORECAST_INVALID`, not a scientific negative result.

## 5. Comparison systems

All systems are scored on the same eligible event when their required inputs are available.

### B0 — neutral no-change baseline

Deterministic:

- `p_up = 0.50`;
- `forecast_return_bps = 0`.

B0 requires no AI call.

### A1 — frozen market-only AI

Permitted input:

- event date / weekday;
- cutoff timestamp;
- current Bid, Ask, Mid;
- deterministic midpoint returns ending at cutoff for 1 hour, 4 hours, and 24 hours;
- deterministic midpoint high-low range in basis points for 4 hours and 24 hours;
- current Bid/Ask spread in basis points;
- explicit missingness flags.

No news, macro/fundamental data, repository research result, or future event schedule may be shown to A1.

### A2 — frozen market + fundamentals/news AI

Receives all A1 inputs plus the frozen v0.1 fundamental/news snapshot contract.

The exact source routes must pass readiness qualification before freeze. The intended bounded categories are:

- current official Fed and BOJ policy settings;
- U.S. 2-year and 10-year Treasury yield observations available by cutoff;
- Japanese 2-year and 10-year government yield observations available by cutoff, if a qualified point-in-time route exists;
- official U.S./Japan macro releases published since the preceding eligible cutoff;
- official central-bank / finance-ministry communications published by cutoff;
- pre-cutoff timestamped USD/JPY-relevant news from the frozen permitted source set;
- scheduled official U.S./Japan releases or central-bank events occurring between cutoff and horizon end, if available from a qualified calendar route.

A source category with no qualified point-in-time route must not be silently substituted.

### A3 — frozen market + fundamentals/news + repository-research AI

Receives all A2 inputs plus a status-preserving research snapshot.

Initial permitted research scope is deliberately narrow:

- current projection of the currency-strength-momentum line;
- current projection of the FX monetary-policy-alignment line;
- any later directly relevant USD/JPY research only if explicitly added before freeze.

For the frozen benchmark, every research input must be pinned to a concrete Git commit/blob/ref set before the first scored event.

The snapshot must preserve labels such as:

- UNTESTED;
- BLOCKED;
- exploratory;
- confirmatory;
- negative/null;
- consumed;
- unused/prospective.

A3 must not receive a prose summary that converts an untested hypothesis into an established predictor.

## 6. Information cutoff and provenance

Only information observable at or before 22:00:00 JST may influence a forecast.

For every material source item, preserve where feasible:

- source identity;
- source URL or immutable identifier;
- published_at;
- observed_at;
- retrieved_at;
- captured value or bounded content snapshot;
- revision/vintage status when relevant;
- retrieval status.

Anything first published after cutoff may be used only in later error attribution.

It must never be inserted into the frozen forecast snapshot.

If a web/search result can change over time, preserve the exact retrieved metadata/snippet/summary used by the forecast system rather than relying on a later re-query.

## 7. Required versus optional inputs

### A1 required

- valid start reference quote;
- all deterministic features computable from the qualified reference history.

If missing: `NO_FORECAST_REQUIRED_MARKET_INPUT_MISSING`.

### A2/A3 required

At minimum, before freeze the source-readiness review must identify which fundamental fields are mandatory.

A required field that cannot be obtained by the cutoff causes that system's event state to be `NO_FORECAST_REQUIRED_INPUT_MISSING`.

No after-the-fact reconstruction is permitted.

Optional source items may be absent only if the frozen input contract explicitly marks them optional.

## 8. Event / observation states

Candidate status vocabulary:

- `FORECAST_ISSUED`;
- `FORECAST_INVALID`;
- `NO_FORECAST_REQUIRED_MARKET_INPUT_MISSING`;
- `NO_FORECAST_REQUIRED_INPUT_MISSING`;
- `SOURCE_RETRIEVAL_FAILED`;
- `NON_ELIGIBLE_SESSION`;
- `MARKET_OUTCOME_UNAVAILABLE`;
- `SCORING_FAILED`.

Observation status is separate from the market result and from scientific interpretation.

## 9. Scoring

### Primary score

For each valid probabilistic forecast:

```text
Brier = (p_up - Y_up)^2
```

Lower is better.

### Primary comparison

A3 versus A1 on the matched set of events where both systems issued structurally valid forecasts and the market outcome is available.

Primary estimand:

```text
mean(Brier_A3 - Brier_A1)
```

Negative values favor A3.

### Baseline sanity comparison

A3 versus B0 on the same matched event set.

### Key secondary comparison

A3 versus A2 on the matched event set.

This isolates the incremental contribution of status-preserving repository research conditional on market + fundamentals/news.

### Secondary continuous metric

Mean absolute error:

```text
MAE_bps = mean(abs(forecast_return_bps - realized_return_bps))
```

Directional accuracy may be reported descriptively but is not the primary metric.

Calibration/reliability analysis is deferred until enough events exist to avoid misleading small-sample bins.

## 10. Evaluation cohort and stopping rule

Frozen v0.1 benchmark cohort:

- minimum: 60 eligible events with valid A3/A1 matched forecasts and available outcomes;
- v0.1 benchmark systems A1/A2/A3 remain unchanged throughout those 60 matched events.

Do not stop early because results look good or bad.

Administrative/safety stop is required if:

- outcome information leaks into a pre-cutoff snapshot;
- forecast records can be rewritten after issuance;
- reference source identity becomes invalid/unverifiable;
- scoring semantics change without a new version;
- a system receives forbidden information;
- trial/event accounting becomes incomplete.

An administrative stop is not a scientific result.

## 11. Daily feedback versus adaptation

Daily:

1. issue/freeze forecasts;
2. score when outcome becomes available;
3. record error attribution;
4. preserve the original forecast unchanged.

Daily error attribution may classify causes such as:

- unexpected post-cutoff event;
- market-price continuation/reversal;
- rate/yield signal mismatch;
- source missingness;
- narrative overconfidence;
- other bounded categories fixed before operation.

Daily attribution does **not** modify frozen v0.1.

### Challenger reviews

At 20 and 40 completed matched events:

- review accumulated errors;
- a challenger change may be proposed;
- the change must get a new version identity;
- evidence used to design it is recorded;
- it is exploratory/adaptive relative to that evidence.

The original A1/A2/A3 v0.1 benchmark continues unchanged to 60 events.

A challenger cannot replace the v0.1 record or be presented as independently confirmed on events used to design it.

## 12. End-of-cohort decision rule

No forecast-skill promotion decision is made before 60 matched v0.1 events.

After 60 events:

### ADVANCE_TO_INDEPENDENT_PROSPECTIVE_REPLICATION

Permitted only if:

- mean Brier(A3) < mean Brier(A1); and
- mean Brier(A3) < mean Brier(B0).

This is a minimum decision gate, not proof of a durable edge.

The next step is another independent prospective period with a frozen successor specification.

### DEPRIORITIZE_FULL_SYSTEM

If A3 fails either minimum comparison, do not rescue v0.1 by changing:

- time window;
- weekday subset;
- event-day filter;
- probability threshold;
- research subset;
- source subset;
- news category;
- market feature lookback

on the same 60-event cohort and call it validated.

Exploratory diagnostics may still be recorded as exploratory.

### Research-value secondary conclusion

A3 versus A2 may answer whether the repository-research layer added incremental value in this cohort.

A negative result is preserved.

## 13. Model, prompt, and source versioning

Each forecast must bind:

- `forecast_system_version`;
- prompt/instruction version;
- observable model identifier;
- input schema version;
- source-set version;
- pinned repository-research refs for A3;
- scoring version.

If a model becomes unavailable and substitution is required:

- do not silently continue under the same system identity;
- create a new forecast-system version;
- preserve the discontinuity.

## 14. Evidence ledger minimum fields

Each event should preserve at least:

- event_id;
- nominal observation date;
- observation cutoff;
- horizon endpoint;
- eligibility state;
- start quote identity;
- input snapshot identity;
- source/provenance records;
- system identity for B0/A1/A2/A3;
- numerical forecast output;
- explanation;
- issued_at;
- immutable forecast hash where feasible;
- outcome quote identity;
- realized outcome;
- score;
- observation status;
- error-attribution record;
- whether the event later influenced a challenger design.

## 15. Source/readiness gate before freeze

Before the first scored forecast, complete a bounded readiness check that does **not** inspect future outcomes under this protocol.

It must establish:

1. exact USD/JPY reference-feed retrieval route;
2. Bid/Ask timestamp semantics;
3. ability to obtain the required pre-cutoff lookback features without future leakage;
4. start/end quote selection implementation;
5. point-in-time routes for mandatory fundamental fields;
6. bounded news retrieval/capture rule;
7. repository-ref pinning mechanism;
8. append-preserving forecast record;
9. deterministic scoring implementation;
10. synthetic tests for cutoff leakage, timestamp edges, missingness, malformed forecasts, and scoring.

Failure of this gate leaves the line PRE-OUTCOME / BLOCKED and does not test the hypothesis.

## 16. Relationship to broker execution

XM and Matsui are outside this forecast-quality specification.

This line does not:

- claim Dukascopy quotes equal either broker;
- model broker fills;
- model broker spread/slippage economics;
- choose position size;
- submit orders.

If forecast evidence later justifies a trading-decision experiment, broker translation becomes a separately preregistered research line or experiment.

## 17. Human freeze boundary

This candidate must not become ACTIVE/FROZEN merely because the file exists.

Human acceptance is required for the exact scientific choices, especially:

- 22:00 → 08:00 JST event;
- Monday–Thursday population;
- midpoint return and binary-up target;
- A1/A2/A3 comparison family;
- Brier primary score;
- 60-event minimum cohort;
- 20/40-event challenger review points;
- end-of-cohort advancement rule.

Until accepted:

- `status = PROPOSED_NOT_FROZEN`;
- prospective outcome access remains CLOSED;
- scored v0.1 forecasting remains NOT_AUTHORIZED.


## 18. Relationship to weekly outlook track

A separate weekly forecast candidate exists at `SPEC-USDJPY-WEEKLY-001-v01`.

For overnight v0.1:

- weekly forecast outputs are not permitted inputs to A1/A2/A3;
- weekly forecast scores do not alter the overnight benchmark;
- overnight forecasts do not rewrite or update the weekly forecast;
- any analysis of weekly/overnight agreement is exploratory unless preregistered later.

A future successor may explicitly test whether a frozen weekly prior improves overnight forecasting, but that is not part of `SPEC-USDJPY-FORECAST-001-v01`.
