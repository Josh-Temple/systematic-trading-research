---
id: RL-JP225-EMA-001
type: ResearchLine
created_at: 2026-10-03
status: SOURCE_QUALIFICATION_REQUIRED
relations: []
---

# JP225 M1 EMA5/EMA200 Time-of-Day v0.1

## Purpose

Test whether a simple M1 EMA(5)/EMA(200) crossover on XM `JP225Cash` predicts same-direction short-horizon movement after observed BID/ASK spread, and whether the effect is concentrated in a small set of time windows fixed before outcome inspection.

## Scientific framing

The line separates three questions:

1. **Signal:** does EMA(5)/EMA(200) crossover contain same-direction information at +15 minutes?
2. **Timing:** is any signal stronger during predeclared opening/closing windows?
3. **Incremental value:** does EMA(5) add useful information compared with the simpler price/EMA(200) crossover comparator?

## Data roles

- **Discovery:** 2025-01-01 through 2025-12-31.
- **Warm-up:** target starts at 2024-12-01 and must provide at least 1,000 valid quoted M1 bars before the first evaluated event.
- **Unused holdout:** 2026-01-01 through 2026-09-30.
- **Prospective:** only after a successful holdout and a new explicit decision.

If the exact XM history cannot cover these roles, do not slide dates after seeing outcomes.

## Core restrictions

- EMA spans fixed at 5 and 200.
- M1 only.
- No stop loss or take profit.
- Primary horizon +15 minutes.
- +5 and +30 minutes descriptive only.
- No parameter search.
- No time-window search beyond the predeclared windows.
- No live/paper orders or broker automation.

## Next action

Qualify XM MT5 `JP225Cash` historical bars/ticks, timestamp semantics, and instrument identity. In parallel, implement the frozen calculation against synthetic fixtures only.
