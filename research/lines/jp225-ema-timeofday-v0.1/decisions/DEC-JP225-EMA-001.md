---
id: DEC-JP225-EMA-001
type: Decision
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-03
status: ACTIVE_PRE_OUTCOME_DECISION
---

# Initial architecture decision

## Decision

Proceed with a bounded two-stage test of the user-proposed JP225 M1 EMA(5)/EMA(200) crossover.

## Fixed choices

- Target instrument: XM MT5 `JP225Cash`.
- Discovery: calendar 2025.
- Holdout: 2026-01-01 through 2026-09-30.
- Primary horizon: +15 minutes.
- Secondary: +5/+30 descriptive only.
- Discovery candidates: ALL, Tokyo first 30 minutes, Tokyo last 30 minutes.
- No TP/SL in v0.1.
- Price/EMA200 cross is comparator.
- Observed BID/ASK execution is required for economic conclusions.

## Why no stop/target optimization first

A fixed-horizon event study tests whether the signal has directional information after spread. If absent, exit tuning would create a large rescue search space.

## Why XM data controls

The practical claim concerns XM short-term tradability. A different broker/index can inform market structure but cannot establish actual XM signal or spread economics.

## Why not Dukascopy as default proxy

Its official JPN.IDX/JPY product is described as Japan 200+ Index. Exact equivalence is not established.

## Boundary

This decision authorizes source qualification and outcome-blind code only. 2025 outcome calculation waits for both gates; 2026 holdout remains locked until a discovery winner is recorded.
