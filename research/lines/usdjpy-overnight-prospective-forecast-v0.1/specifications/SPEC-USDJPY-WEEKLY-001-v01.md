---
type: Specification
specification_id: SPEC-USDJPY-WEEKLY-001-v01
research_line_id: RL-USDJPY-OVERNIGHT-001
status: PROPOSED_NOT_FROZEN
created_at: 2026-10-04
market_outcome_access: CLOSED
---

# SPEC-USDJPY-WEEKLY-001-v01 — Weekly outlook Phase 0 candidate

## 1. Scientific question

For prospectively generated weekly USD/JPY outlook events, does a frozen AI system using market data, point-in-time fundamentals/news, and status-preserving relevant repository research forecast the sign of the following trading week's return better than:

1. a neutral no-change baseline; and
2. an otherwise comparable market-only AI system?

A key secondary question is whether repository research adds forecast value beyond market + fundamentals/news alone.

This specification evaluates weekly forecast quality only. It does not define a trading rule.

## 2. Forecast timing

Candidate v0.1 weekly timing:

- timezone: `Asia/Tokyo`;
- forecast cutoff: Sunday 20:00:00 JST;
- forecast target begins: Monday 08:00:00 JST;
- forecast target ends: Friday 22:00:00 JST.

The weekly forecast is therefore issued before the ordinary FX week opens.

The target interval starts after forecast issuance.

This intentionally excludes the Sunday/Monday opening gap from the primary return target.

The gap may later be recorded as a descriptive diagnostic, but it must not be substituted into the primary target after outcomes are observed.

## 3. Eligible weeks

A nominal week is eligible if:

- the Sunday 20:00 JST forecast cutoff occurs normally;
- the qualified reference feed provides a valid Monday 08:00 start quote under the rule below;
- the required forecast inputs were available by the Sunday cutoff;
- the Friday 22:00 endpoint is observable under the rule below.

Japanese, U.S., or other scheduled holidays do not by themselves exclude a week.

Major central-bank meetings, elections, CPI/payroll releases, intervention risk, geopolitical events, and other high-volatility conditions also do not justify ex-post exclusion.

If the reference market does not supply the required quote or a mandatory source route fails under the frozen rule, the event receives the relevant missing/unavailable status rather than being reconstructed later.

## 4. Reference instrument and weekly outcome

Instrument:

- USD/JPY spot-like best Bid/Ask reference stream from the qualified research/reference feed;
- current candidate: Dukascopy USD/JPY best Bid/Ask tick semantics, subject to this line's source/readiness gate;
- the reference feed is not treated as broker execution for XM or Matsui.

Quote construction:

```text
mid = (bid + ask) / 2
```

Weekly start price:

- first valid Bid/Ask tick with timestamp `>= Monday 08:00:00 JST`;
- tick must occur within 60 seconds after the target start;
- otherwise `WEEKLY_MARKET_START_UNAVAILABLE`.

Weekly end price:

- first valid Bid/Ask tick with timestamp `>= Friday 22:00:00 JST`;
- tick must occur within 60 seconds after the target end;
- otherwise `WEEKLY_MARKET_END_UNAVAILABLE`.

Primary realized continuous outcome:

```text
weekly_realized_return_bps = 10,000 * ln(friday_end_mid / monday_start_mid)
```

Primary binary outcome:

```text
Y_week_up = 1 if friday_end_mid > monday_start_mid
Y_week_up = 0 otherwise
```

An unchanged midpoint counts as non-up for the binary score and remains exactly zero in the continuous return record.

## 5. Forecast outputs

Every scored weekly AI system must emit before the Sunday cutoff:

- `p_week_up`: probability that Friday end midpoint exceeds Monday start midpoint;
- `forecast_week_return_bps`: point forecast for the Monday–Friday log return;
- `weekly_base_case`: concise central scenario;
- `risk_scenarios`: bounded alternative scenarios and invalidation conditions;
- `scheduled_catalysts`: known future events between Monday start and Friday end that were observable by the Sunday cutoff;
- `top_drivers`;
- `counterevidence`;
- `source_refs`;
- `forecast_system_version`;
- observable model identifier where available.

Structural validity:

- `p_week_up` must be finite and in `[0.01, 0.99]`;
- `forecast_week_return_bps` must be finite;
- narrative/scenario fields do not change the numerical score;
- malformed output is `WEEKLY_FORECAST_INVALID`, not a scientific negative result.

## 6. Weekly comparison systems

### WB0 — neutral no-change baseline

Deterministic:

- `p_week_up = 0.50`;
- `forecast_week_return_bps = 0`.

### WA1 — frozen weekly market-only AI

Permitted inputs:

- forecast date and cutoff timestamp;
- latest valid reference Bid/Ask/Mid from the prior Friday session;
- deterministic midpoint returns ending at the prior Friday reference point for 1 trading day, 5 trading days, and 20 trading days;
- deterministic high-low range in basis points over 5 and 20 trading days;
- latest Bid/Ask spread at the prior Friday reference point;
- explicit missingness flags.

WA1 receives no macro/fundamental data, news, repository research, or forward event schedule.

### WA2 — frozen weekly market + fundamentals/news AI

Receives all WA1 inputs plus the frozen weekly point-in-time fundamental/news contract.

Intended bounded categories, subject to source qualification:

- current official Fed and BOJ policy settings;
- latest U.S. 2-year and 10-year Treasury yield observations available by Sunday cutoff;
- latest Japanese 2-year and 10-year government yield observations available by Sunday cutoff where a qualified route exists;
- official U.S./Japan macro releases published since the preceding weekly cutoff;
- official central-bank / finance-ministry communications published by cutoff;
- timestamped USD/JPY-relevant news published by the Sunday cutoff from the frozen permitted source set;
- scheduled official U.S./Japan macro releases and central-bank events for Monday–Friday, if available from a qualified point-in-time calendar route;
- known market-closure/holiday schedule relevant to source availability.

No unqualified source category may be silently substituted.

### WA3 — frozen weekly market + fundamentals/news + repository research AI

Receives all WA2 inputs plus a status-preserving repository research snapshot pinned before the first scored weekly event.

Initial scope is narrow:

- currency-strength-momentum current projection;
- FX monetary-policy-alignment current projection;
- directly relevant USD/JPY line(s) only if explicitly admitted before freeze.

Every research item must preserve its state, including where applicable:

- UNTESTED;
- BLOCKED;
- exploratory;
- confirmatory;
- negative/null;
- consumed;
- unused/prospective.

An untested or blocked research hypothesis must not be rendered to WA3 as established predictive evidence.

## 7. Information cutoff

Only information observable at or before Sunday 20:00:00 JST may influence the weekly forecast.

For material inputs preserve where feasible:

- source identity;
- source URL / immutable identifier;
- published_at;
- observed_at;
- retrieved_at;
- captured value/content;
- revision/vintage status;
- retrieval status.

Any information first published after the Sunday cutoff may be used only for later error attribution.

It must not be inserted into the frozen weekly snapshot.

## 8. Scheduled future events

Because a weekly outlook is intended to reason about the upcoming week, events scheduled in advance may be supplied if their schedule was observable by the Sunday cutoff.

Examples include:

- CPI;
- payrolls/employment;
- GDP;
- retail sales;
- Fed/BOJ decisions;
- scheduled speeches;
- auctions or official releases where relevant.

The system may reason about uncertainty surrounding the event.

It may not use the later released result until after the weekly forecast is frozen.

If a scheduled event is later cancelled, delayed, or rescheduled, that becomes outcome-period information and may be recorded in error attribution.

## 9. Weekly scoring

### Primary probabilistic score

```text
Weekly_Brier = (p_week_up - Y_week_up)^2
```

Lower is better.

### Primary weekly comparison

WA3 versus WA1 on matched valid weekly events.

Primary estimand:

```text
mean(Weekly_Brier_WA3 - Weekly_Brier_WA1)
```

Negative values favor WA3.

### Baseline sanity

WA3 versus WB0 on the same matched weeks.

### Research incremental comparison

WA3 versus WA2 on the same matched weeks.

This isolates the incremental contribution of the status-preserving repository research layer conditional on market + fundamentals/news.

### Secondary continuous metric

```text
Weekly_MAE_bps =
mean(abs(forecast_week_return_bps - weekly_realized_return_bps))
```

Directional accuracy is descriptive, not primary.

## 10. Frozen weekly cohort

Initial frozen weekly benchmark:

- 26 matched valid weekly events;
- WA1/WA2/WA3 remain unchanged throughout the 26-week benchmark cohort.

Do not stop early because performance looks favorable or unfavorable.

Twenty-six weeks is a bounded initial prospective cohort, not a claim of universal statistical power.

Administrative/safety stop is required if:

- post-cutoff information leaks into the forecast snapshot;
- forecast artifacts can be rewritten after issuance;
- reference source identity becomes invalid/unverifiable;
- scoring semantics change without a new version;
- a system receives forbidden data;
- event accounting becomes incomplete.

An administrative stop is not a scientific result.

## 11. Weekly feedback and adaptation

After each completed eligible week:

1. retrieve and bind the Friday endpoint;
2. compute deterministic scores;
3. preserve the original Sunday forecast unchanged;
4. record error attribution;
5. record major post-cutoff information that plausibly explains forecast error without rewriting the original inputs.

Weekly feedback does not alter the frozen v0.1 benchmark.

### Challenger reviews

At 9 and 18 completed matched weekly events:

- accumulated errors may be reviewed;
- a challenger may be proposed;
- the challenger receives a new version identity;
- evidence used to design the challenger is recorded;
- that challenger remains adaptive/exploratory relative to the events used to design it.

WA1/WA2/WA3 v0.1 continue unchanged through event 26.

## 12. End-of-cohort rule

No weekly forecast-skill promotion decision occurs before 26 matched events.

### ADVANCE_WEEKLY_TO_INDEPENDENT_PROSPECTIVE_REPLICATION

Permitted only if:

- mean Brier(WA3) < mean Brier(WA1); and
- mean Brier(WA3) < mean Brier(WB0).

This is only a minimum gate for a new prospective replication.

It does not establish durable market edge or trading profitability.

### DEPRIORITIZE_WEEKLY_FULL_SYSTEM

If WA3 fails either minimum comparison, do not rescue v0.1 by changing on the same 26 weeks:

- weekly start/end times;
- holiday subset;
- event-day subset;
- news categories;
- research subset;
- source subset;
- market lookback;
- probability threshold.

Post-hoc diagnostics may be preserved as exploratory evidence.

## 13. Relationship to the overnight track

The weekly and overnight tracks are scientifically separate in v0.1.

The weekly forecast output is **not** a permitted input to the frozen overnight A1/A2/A3 systems.

The overnight forecasts are **not** permitted to rewrite, update, or replace the Sunday weekly forecast.

After sufficient paired observations exist, the repository may descriptively examine:

- agreement between weekly and overnight direction;
- disagreement cases;
- whether errors cluster in particular combinations.

Such analysis is exploratory unless preregistered in a later prospective specification.

A later successor may explicitly test whether a frozen weekly forecast improves an overnight forecast, but that is outside v0.1.

## 14. Weekly event states

Candidate states:

- `WEEKLY_FORECAST_ISSUED`;
- `WEEKLY_FORECAST_INVALID`;
- `WEEKLY_NO_FORECAST_REQUIRED_INPUT_MISSING`;
- `WEEKLY_SOURCE_RETRIEVAL_FAILED`;
- `WEEKLY_MARKET_START_UNAVAILABLE`;
- `WEEKLY_MARKET_END_UNAVAILABLE`;
- `WEEKLY_SCORING_FAILED`.

Execution/observation status remains distinct from market result and scientific interpretation.

## 15. Evidence ledger

Each weekly event should preserve at least:

- weekly_event_id;
- Sunday forecast cutoff;
- Monday target start;
- Friday target end;
- eligibility state;
- forecast input snapshot identity;
- point-in-time source/provenance records;
- scheduled catalyst snapshot;
- WB0/WA1/WA2/WA3 system identities;
- numerical outputs;
- scenario/narrative outputs;
- issued_at;
- immutable forecast hash where feasible;
- Monday start quote identity;
- Friday end quote identity;
- realized weekly return;
- Brier / MAE scores;
- observation status;
- error attribution;
- whether the event influenced a later challenger.

## 16. Source/readiness gate

Before the first scored weekly event, prove without using target-period outcomes to choose scientific conditions:

1. reference-feed route and timestamp semantics;
2. Friday historical lookback feature construction;
3. Monday 08:00 and Friday 22:00 endpoint selection;
4. point-in-time official rate/yield routes;
5. weekly economic-calendar capture route;
6. bounded Sunday news capture route;
7. repository-ref pinning;
8. append-preserving weekly artifact storage;
9. deterministic weekly scoring;
10. synthetic tests for cutoff leakage, DST/calendar edges, missing data, malformed outputs, and score calculation.

Failure leaves the weekly track PRE-OUTCOME / BLOCKED.

## 17. Broker boundary

This specification does not:

- claim the reference price equals XM or Matsui execution;
- model broker spreads/fills;
- define entries/exits;
- size positions;
- authorize paper/live orders.

Economic translation requires a separate preregistered experiment after forecast evidence exists.

## 18. Human freeze boundary

Human acceptance is required for the exact weekly choices, especially:

- Sunday 20:00 JST forecast cutoff;
- Monday 08:00 → Friday 22:00 JST target interval;
- midpoint return and binary-up target;
- WB0/WA1/WA2/WA3 comparison family;
- Brier primary score;
- 26-week cohort;
- 9/18-week challenger review points;
- isolation from overnight forecasts;
- end-of-cohort advancement rule.

Until explicitly accepted:

- `status = PROPOSED_NOT_FROZEN`;
- weekly prospective outcome access remains CLOSED;
- scored weekly forecasting remains NOT_AUTHORIZED.
