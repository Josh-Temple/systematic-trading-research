---
type: ResearchLine
research_line_id: RL-USDJPY-OVERNIGHT-001
status: PROPOSED_NOT_FROZEN
created_at: 2026-10-04
---

# USD/JPY Prospective Forecast v0.1 — Overnight + Weekly

## Purpose

Build prospectively timestamped USD/JPY forecast experiments that test whether frozen AI forecasting systems add forecast value beyond simple baselines when supplied with:

1. market information;
2. point-in-time fundamentals and news;
3. status-preserving relevant repository research.

The line currently contains two scientifically separate scored-forecast horizons plus one non-scored observation stream:

- **Overnight:** Monday–Thursday 22:00 JST → next-day 08:00 JST.
- **Weekly:** Sunday 20:00 JST forecast → Monday 08:00 through Friday 22:00 JST target interval.
- **Live Market State Journal:** append-only observational checkpoints at 08:30, 15:00, 21:30 JST plus event-driven/manual updates.

The line is designed to collect future evidence. It is not a live-trading strategy and grants no broker execution authority.

## Primary research questions

### Overnight

On a preregistered set of overnight forecast events, does the full frozen forecasting system produce lower probabilistic forecast error than the frozen market-only AI comparison and the neutral no-change baseline?

### Weekly

On a preregistered set of weekly outlook events, does the full frozen weekly forecasting system produce lower probabilistic forecast error than the frozen weekly market-only AI comparison and neutral no-change baseline?

## Secondary research question

At each horizon, conditional on the same market and fundamental/news inputs, does adding status-preserving repository research reduce forecast error relative to the market + fundamentals/news AI system?

## Cross-horizon boundary

The overnight and weekly tracks are separate v0.1 experiments.

- weekly forecast outputs are not inputs to the frozen overnight benchmark;
- overnight outputs do not rewrite or update the frozen weekly forecast;
- agreement/disagreement analysis is exploratory unless preregistered later;
- a later prospective version may explicitly test whether a weekly prior improves nightly forecasts.

## Live observation stream

`OBS-USDJPY-LIVE-STATE-001-v01` is ACTIVE_OBSERVATIONAL.

It may update as market conditions change and may be used for:

- point-in-time situation awareness;
- change tracking;
- error-context reconstruction;
- challenger idea generation.

It is not itself scored and cannot rewrite frozen forecasts or replace canonical forecast source snapshots.

## Scientific boundaries

- No market outcome may be used to choose v0.1 scientific conditions before freeze.
- Daily/weekly scoring must not rewrite the frozen v0.1 benchmark systems.
- Adaptive improvements are tracked as separate challenger versions.
- Explanation quality is not itself evidence of forecast skill.
- Forecast quality and trading profitability are separate experiments.
- No order submission, automatic position sizing, or live-capital action is authorized.
- Negative/null results are preserved and do not trigger same-sample rule rescue.

## Current state

The line is **PROPOSED_NOT_FROZEN**.

See:

- `CURRENT.md`
- `specifications/SPEC-USDJPY-FORECAST-001-v01.md`
- `specifications/SPEC-USDJPY-WEEKLY-001-v01.md`
- `work/HUMAN_REVIEW_PACKET_2026-10-04.md`
- `work/HUMAN_REVIEW_PACKET_WEEKLY_2026-10-04.md`

No scored prospective event at either horizon is authorized until its exact specification is explicitly accepted and the relevant source/readiness gates pass.
