---
type: ResearchLine
research_line_id: RL-USDJPY-OVERNIGHT-001
status: PROPOSED_NOT_FROZEN
created_at: 2026-10-04
---

# USD/JPY Overnight Prospective Forecast v0.1

## Purpose

Build a prospective, timestamped USD/JPY forecast experiment that can answer whether a fixed AI forecasting process adds forecast value beyond simple baselines when supplied with:

1. market information;
2. point-in-time fundamentals and news;
3. status-preserving relevant repository research.

The line is designed to collect future evidence. It is not a live-trading strategy and grants no broker execution authority.

## Primary research question

On a preregistered set of overnight forecast events, does the full frozen forecasting system produce lower probabilistic forecast error than the frozen market-only AI comparison and the neutral no-change baseline?

## Secondary research question

Conditional on the same market and fundamental inputs, does adding status-preserving repository research reduce forecast error relative to the market + fundamentals AI system?

## Scientific boundaries

- No market outcome may be used to choose v0.1 scientific conditions before freeze.
- Daily scoring must not rewrite the frozen v0.1 benchmark systems.
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
- `work/HUMAN_REVIEW_PACKET_2026-10-04.md`

No scored prospective event is authorized until the specification is explicitly accepted and the source/readiness gates pass.
