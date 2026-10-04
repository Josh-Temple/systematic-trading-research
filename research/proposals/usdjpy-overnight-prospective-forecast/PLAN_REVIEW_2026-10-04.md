# USD/JPY Overnight Prospective Forecast — Plan Review

Date: 2026-10-04 JST  
Status: **DRAFT_NOT_FROZEN**  
Scientific effect: **NONE**  
Market outcome access caused by this document: **NONE**  
Live trading authority: **NONE**

## 1. Purpose

This document records the reviewed plan for a prospective USD/JPY forecasting experiment.

The intended question is not simply:

> Can an AI guess whether USD/JPY will rise by tomorrow morning?

The intended research question is:

> Can a preregistered forecasting process that combines market information, real-time fundamentals, news, and appropriately status-labeled prior research produce prospectively measured forecast quality that is better than simple frozen baselines?

The experiment should collect future, timestamped forecast evidence rather than repeatedly reinterpret historical outcomes.

This proposal is not a trading rule, not a profitability claim, and not permission to place broker orders.

## 2. Why this is worth pursuing

The repository currently has substantial retrospective and pre-outcome research infrastructure, but future observations that did not exist at protocol freeze are especially valuable because they reduce several forms of data snooping and historical outcome contamination.

A recurring forecast loop can create such evidence if the information cutoff, forecast target, scoring, and versioning are fixed before outcomes are observed.

The useful loop is:

```text
information cutoff
→ input snapshot
→ forecast
→ immutable forecast record
→ future outcome
→ deterministic scoring
→ error attribution
→ periodic review
→ separately versioned challenger
```

The useful loop is **not**:

```text
forecast
→ outcome
→ rewrite reasoning/rules
→ forecast again
```

## 3. Governing repository principles

This proposal must remain consistent with `docs/RESEARCH_PRINCIPLES.md`.

In particular:

- observation / fact, hypothesis, specification, data, experiment, result, interpretation, and decision remain distinct;
- negative and null results are preserved;
- provenance is retained;
- confirmatory conditions are fixed before outcomes;
- research history is append-preserving;
- exploratory observations are not promoted to confirmatory evidence without unused/prospective evidence;
- deterministic computation is separated from AI reasoning where feasible;
- AI free-form answers are not themselves evidence of a market edge;
- live broker orders and automated position sizing remain outside this proposal.

## 4. Main issues found in the first draft plan

### 4.1 “Tomorrow morning” is underspecified

The protocol must fix:

- forecast observation time;
- forecast end time;
- timezone;
- reference instrument;
- reference price series;
- Bid / Ask / Mid semantics;
- eligible weekdays;
- holiday / market-closure handling;
- quote-missing handling.

A phrase such as “tomorrow morning” is not reproducible enough.

### 4.2 Daily feedback can become adaptive overfitting

Daily scoring is acceptable.

Daily rule modification is not the default.

If the system changes input weights, prompt logic, forecast thresholds, source selection, scenario boundaries, or other rules after each outcome, the observed sample becomes development data for the next version.

Therefore:

- daily loop = forecast → freeze → score → error classification;
- protocol/model changes occur only at predefined review points;
- every changed version receives a new identity;
- prior versions remain in the ledger;
- a new version must be evaluated on observations that did not determine that version.

### 4.3 Forecast logic and explanation text must be separated

The experiment should not treat a fluent market narrative as evidence.

Where computation is deterministic, it should be implemented deterministically.

The system should separate at least:

1. source acquisition / normalization;
2. deterministic market and macro features;
3. model/AI forecast output;
4. explanatory narrative;
5. deterministic scoring;
6. later interpretation.

The explanation may help diagnose decisions, but it must not retroactively redefine the forecast.

### 4.4 Real-time fundamentals require point-in-time provenance

Fundamental and news inputs can silently change after the forecast cutoff.

For each material input, preserve where feasible:

- source identity;
- published_at;
- observed_at;
- retrieved_at;
- value or captured content;
- revision / vintage status when relevant;
- retrieval failure state.

Information first released after the cutoff may be used for later error attribution, but must never be inserted into the frozen forecast snapshot as though it was known earlier.

### 4.5 Prior research must retain evidence status

Prior repository findings must not be flattened into an undifferentiated “research knowledge” prompt.

Inputs should preserve status such as:

- observed fact;
- hypothesis;
- frozen specification;
- exploratory result;
- confirmatory result;
- negative/null;
- blocked;
- consumed sample;
- unused/prospective;
- untested.

A hypothesis whose outcome remains unopened must not be summarized to the forecaster as an established predictor.

### 4.6 Forecast quality and trading profitability are different experiments

This proposal should first test forecast quality.

It should not immediately turn forecast probabilities into broker orders.

A later “forecast → trading decision rule” would require its own preregistration, including:

- entry timing;
- execution feed;
- transaction costs;
- position sizing;
- abstention rule;
- risk limits;
- economic kill condition.

A forecast may be statistically informative but economically unusable after costs.

### 4.7 Baselines must be strong enough to matter

An AI forecast is not useful merely because its raw directional accuracy exceeds 50%.

The protocol should compare against frozen baselines.

Minimum candidate baseline family:

- no-change / unconditional-base-rate baseline;
- simple market-only deterministic baseline;
- AI market-only forecast;
- AI market + fundamentals + status-labeled repository research forecast.

The exact baseline definitions must be frozen before the first scored observation.

This allows a direct incremental-value question:

> Do fundamentals and prior research improve forecast quality beyond market-only information?

### 4.8 Calendar and regime semantics must be explicit

Sunday/Monday, holiday sessions, major scheduled events, and U.S. daylight-saving transitions may create materially different observation conditions.

The protocol must decide in advance whether these are:

- included in one population;
- stratified only for later descriptive analysis;
- or excluded by a predeclared eligibility rule.

Do not inspect outcomes first and then create an exclusion rule.

### 4.9 Missing data needs a fail-closed state

If required inputs cannot be obtained by the cutoff, the system must not reconstruct the forecast after the fact.

Possible states should distinguish:

- FORECAST_ISSUED;
- NO_FORECAST_REQUIRED_INPUT_MISSING;
- MARKET_OUTCOME_UNAVAILABLE;
- SOURCE_RETRIEVAL_FAILED;
- NON_ELIGIBLE_SESSION.

Exact labels can be finalized in Phase 0.

Missing-data status and market outcome must remain separate.

### 4.10 Model and prompt drift must be tracked

If the AI model, prompt, tool availability, source routing, or retrieval method changes, that may change the forecasting system.

At minimum, store where observable:

- model identifier;
- prompt / instruction version;
- input schema version;
- source-set version;
- scoring version;
- forecast-system version.

Do not silently pool materially different system versions.

## 5. Recommended experimental structure

### 5.1 Frozen benchmark

Maintain one forecast system that is unchanged for a predefined evaluation window.

Its role is to provide a stable prospective benchmark.

### 5.2 Adaptive challenger

A second system may be improved from past errors, but only under explicit version boundaries.

A challenger update should record:

- evidence used to motivate the change;
- what changed;
- what did not change;
- predicted improvement;
- plausible failure mode;
- effective start date;
- version identifier.

The changed challenger must earn evidence on later observations.

### 5.3 Daily process

A candidate daily sequence:

1. Determine whether the session is eligible.
2. At the fixed information cutoff, retrieve only permitted point-in-time inputs.
3. Persist source/input snapshot and provenance.
4. Generate forecasts from each frozen comparison system.
5. Persist forecast probabilities / numerical output and explanation separately.
6. Lock the event.
7. At the fixed horizon, retrieve the outcome from the preregistered reference feed.
8. Compute scores deterministically.
9. Record error attribution without rewriting the original forecast.
10. Make no protocol change during the daily scoring action.

## 6. Forecast target — current recommendation

The primary target should preferably be a continuous price change / return over a fixed horizon rather than relying only on a three-class UP / FLAT / DOWN definition.

Reason:

A FLAT class requires an arbitrary boundary, which can become another tuning parameter.

Candidate structure, **not yet frozen**:

- observation time: fixed JST time;
- horizon end: fixed next-morning JST time;
- primary outcome: reference USD/JPY return over that interval;
- secondary output: probabilistic directional / magnitude categories if useful.

Before activation, the exact reference price semantics must be fixed.

## 7. Scoring — current recommendation

Do not use only hit rate.

Candidate metrics, **not yet frozen**, include:

- continuous forecast error for a numerical-return forecast;
- Brier score for probabilistic categorical forecasts;
- log loss where appropriate and numerically safe;
- directional accuracy as a secondary descriptive metric;
- calibration / reliability after enough observations;
- coverage / no-forecast rate;
- comparison with every frozen baseline.

The exact primary metric and promotion/kill criteria must be frozen before prospective scoring begins.

## 8. Source architecture

The experiment should avoid creating unnecessary source infrastructure.

Relevant existing work should be reused only after a fresh read of its current branch / canonical state.

Current related work observed during this 2026-10-04 review includes:

- `research/fx-monetary-policy-alignment-v0.1`
- `research/fx-daily-breakout-20261003`

Important boundary:

These branches are not automatically canonical `main` evidence merely because they exist.

The USD/JPY Daily Breakout source-qualification work has already developed a useful conceptual separation between:

- research/reference feed;
- broker-specific execution translation.

That separation is likely reusable here, subject to fresh qualification for this forecast protocol.

The forecast experiment should not claim Dukascopy, XM, and Matsui prices/fills are interchangeable unless separately established.

## 9. Relationship to the monetary-policy research line

The FX monetary-policy-alignment work may provide structured research context, but its scientific status must be respected.

At the time of this review, the branch records a frozen specification while the market-outcome gate remains blocked by an upstream dependency.

Therefore this proposal must not tell the forecast system that monetary-policy alignment is already a proven USD/JPY predictor.

It may be supplied only with its correct status and content boundary.

## 10. Phase 0 before any live forecast scoring

Do not automate daily scored forecasts until the following are frozen.

### 10.1 Forecast event identity

Fix:

- instrument;
- observation time;
- horizon end;
- timezone;
- eligible calendar;
- reference feed;
- price-side semantics.

### 10.2 Input contract

Fix:

- required market fields;
- permitted fundamental fields;
- permitted news/source classes;
- prior-research retrieval rule;
- point-in-time cutoff;
- missing-input behavior.

### 10.3 Comparison systems

Fix the baseline and AI variants to be scored in parallel.

Avoid adding new variants after seeing which initial system performs poorly unless they enter as a new version/family with full trial accounting.

### 10.4 Metrics

Fix:

- primary score;
- secondary diagnostics;
- minimum evaluation duration or event count;
- review cadence;
- stopping / kill conditions;
- version-promotion rule.

### 10.5 Update rule

Fix when changes are permitted.

Recommended principle:

- score daily;
- review periodically;
- change only by explicit version;
- evaluate the changed version only on future observations.

### 10.6 Evidence ledger

Every event should preserve at least:

- event_id;
- observation timestamp;
- horizon;
- eligibility;
- input snapshot identity;
- data provenance;
- forecast-system version;
- forecast outputs;
- confidence / probabilities;
- explanation;
- outcome identity;
- score;
- observation status;
- error attribution;
- whether this event influenced a later version.

## 11. What this proposal does not establish

This document does **not** establish that:

- USD/JPY is predictably directional overnight;
- fundamentals add predictive value;
- repository research adds predictive value;
- AI outperforms a simple baseline;
- forecast quality converts to positive trading expectancy;
- any current XM or Matsui execution rule is profitable;
- any broker should receive an order.

All such claims require later evidence.

## 12. Recommended next action

Create a bounded Phase 0 specification for the USD/JPY prospective forecast line.

The next work product should resolve only the pre-outcome scientific contract:

1. event timing and eligibility;
2. reference feed and price semantics;
3. input/source schema and information cutoff;
4. comparison systems;
5. scoring metrics;
6. minimum evaluation window / stopping rule;
7. update/version rule;
8. missing-data states;
9. evidence ledger.

After human review and freeze, begin prospective shadow forecasting.

Do not start with live capital.

## 13. Promotion boundary

Only after prospective evidence exists should the project decide whether to create a separate trading-decision experiment.

Any such promotion must preserve the distinction between:

- forecast quality;
- economic value after costs;
- execution feasibility;
- live-risk authorization.

Status remains **DRAFT_NOT_FROZEN** until a separate human-reviewed specification explicitly freezes the Phase 0 contract.
