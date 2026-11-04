# Human Review Packet — USD/JPY Weekly Prospective Outlook v0.1

Date: 2026-10-04 JST  
Status: HUMAN_BOUNDARY / PRE-FREEZE  
Outcome access: CLOSED

## Purpose

Provide a bounded human decision for adding a separate weekly prospective forecast horizon to the same research line.

This packet does not alter the overnight candidate's event definition.

## Candidate specification

- `specifications/SPEC-USDJPY-WEEKLY-001-v01.md`

## Proposed choices

1. **Forecast cutoff:** Sunday 20:00 JST.
2. **Target interval:** Monday 08:00 JST → Friday 22:00 JST.
3. **Reference price:** qualified USD/JPY best Bid/Ask midpoint.
4. **Primary realized outcome:** Monday-to-Friday midpoint log return.
5. **Primary probabilistic target:** probability Friday endpoint is above Monday start.
6. **Systems:** WB0 neutral baseline, WA1 market-only, WA2 market+fundamentals/news, WA3 market+fundamentals/news+status-preserving repository research.
7. **Primary score:** Brier score.
8. **Primary comparison:** WA3 versus WA1.
9. **Baseline sanity:** WA3 versus WB0.
10. **Research incremental comparison:** WA3 versus WA2.
11. **Frozen benchmark duration:** 26 matched valid weeks.
12. **Adaptation:** weekly scoring/error attribution; challenger proposals after weeks 9 and 18; original v0.1 remains unchanged through week 26.
13. **Cross-horizon boundary:** weekly outputs do not feed the frozen overnight benchmark; overnight outputs do not rewrite the weekly forecast.
14. **Trading:** no broker orders, position sizing, or profitability claim.

## Why the target begins Monday 08:00

A Sunday forecast should predict an interval that begins after the forecast is frozen.

Starting Monday 08:00:

- avoids defining part of the target before the forecast cutoff;
- avoids making the weekly open gap the main outcome;
- provides a fixed JST boundary after the ordinary FX weekly open under both U.S. DST states.

The opening gap may be recorded descriptively but cannot replace the primary target.

## Why scheduled next-week events are permitted

The objective is a genuine weekly outlook.

If the date/time of CPI, payrolls, a central-bank decision, or another official event is known by Sunday 20:00, that schedule is legitimate pre-forecast information.

The later event result is not.

## Why weekly and overnight forecasts remain separate

Feeding the Sunday weekly view into the nightly benchmark would make it difficult to determine whether forecast value came from:

- current nightly information;
- the weekly prior;
- or interaction between them.

v0.1 therefore estimates the two horizons independently.

A later prospective version can test a weekly-prior input explicitly.

## Why 26 weekly events

Twenty-six events provide a bounded roughly half-year prospective pilot that spans more than a handful of macro weeks.

It is not claimed to provide universal statistical power.

The outcome is a gate for an independent replication, not a final edge claim.

## Remaining readiness work

Even after human acceptance, weekly scored forecasts must remain closed until:

- reference-feed start/end semantics are verified;
- Sunday point-in-time fundamental/news capture routes are qualified;
- next-week official calendar capture is qualified;
- prompt/source-set versions are persisted;
- append-preserving weekly forecast storage works;
- deterministic Brier/MAE scoring is implemented;
- leakage/missingness/calendar synthetic tests pass.

## Acceptance effect

Explicit acceptance of this exact weekly packet permits:

1. freezing the weekly scientific body without substantive changes;
2. recording the accepted pre-freeze identity;
3. source/readiness implementation while weekly outcomes remain closed;
4. scored weekly forecasting only after the readiness gate passes.

Acceptance does not authorize broker trading.
