# Human Review Packet — USD/JPY Overnight Prospective Forecast v0.1

Date: 2026-10-04 JST  
Status: HUMAN_BOUNDARY / PRE-FREEZE  
Outcome access: CLOSED

## Purpose

Reduce the remaining human decision to one bounded acceptance of the Phase 0 scientific contract.

No market outcome has been used to choose the candidate below.

## Candidate package

Specification:

- `specifications/SPEC-USDJPY-FORECAST-001-v01.md`

Proposed choices:

1. **Event:** Monday–Thursday, 22:00 JST → next-day 08:00 JST.
2. **Reference price:** qualified USD/JPY best Bid/Ask midpoint.
3. **Primary realized outcome:** 10-hour midpoint log return.
4. **Primary probabilistic target:** probability that end midpoint is above start midpoint.
5. **Systems:** neutral baseline B0, market-only A1, market+fundamentals/news A2, market+fundamentals/news+status-preserving research A3.
6. **Primary score:** Brier score.
7. **Primary comparison:** A3 versus A1.
8. **Baseline sanity:** A3 versus B0.
9. **Research incremental comparison:** A3 versus A2.
10. **Frozen benchmark duration:** 60 matched valid events.
11. **Adaptation:** daily scoring/error attribution; challenger proposals allowed after event 20 and 40; original v0.1 remains unchanged through event 60.
12. **Promotion:** only consider independent prospective replication if A3 mean Brier is lower than both A1 and B0 after 60 matched events.
13. **Trading:** no broker orders, no automatic position sizing, no claim of profitability.

## Why these choices

### 22:00 → 08:00 JST

This directly operationalizes the original intent of an evening forecast for the following morning while capturing a substantial U.S.-session interval.

Friday and Sunday are excluded to avoid embedding the weekly close/open into the same population.

### Binary probability + continuous return

The binary probability provides a proper probabilistic score without introducing an arbitrary “flat” band.

The continuous return is retained so forecast magnitude can be evaluated separately.

### Brier score

Brier score directly evaluates probability quality and penalizes overconfidence.

Directional accuracy remains secondary.

### 60 events

This is long enough to prevent a handful of nights from determining the conclusion while still being operationally feasible for an initial prospective cohort.

It is not claimed to provide universal statistical power.

### Frozen benchmark + adaptive challenger

This preserves a stable prospective benchmark while allowing the daily feedback loop to generate future improvements without rewriting the original experiment.

## Remaining non-human readiness work

Even after acceptance, scored forecasts must not start until:

- reference-feed retrieval is qualified for this protocol;
- mandatory fundamental source routes are fixed;
- news retrieval/capture rules are fixed;
- prompts and source-set versions are persisted;
- append-only forecast storage works;
- deterministic scoring is implemented and synthetic-tested;
- cutoff leakage tests pass.

Those are readiness gates, not reasons to alter the scientific question after results.

## Acceptance effect

An explicit human acceptance of this exact packet may be recorded as the authority to:

1. change the candidate specification status to ACTIVE/FROZEN without changing its scientific body;
2. preserve the accepted pre-freeze file identity;
3. proceed to source/readiness implementation while market outcomes remain closed;
4. open scored prospective forecasting only after readiness gates pass.

Acceptance does **not** authorize live or paper broker trading.
