---
id: RES-HR-001
type: Result
research_line_id: RL-HR-001
run_id: RUN-HR-001
observed_at: 2026-09-11
execution_status: SUCCESS
evidence_validity: VALID
scientific_status: NOT_SUPPORTED
headline_metrics:
  trades: 2685
  mean_R: -0.201598
  median_R: -1.001100
  win_rate: 0.347486
  profit_factor: 0.660341
  max_consecutive_losses: 20
  max_drawdown_R: 542.166368
artifact_refs:
  - https://docs.google.com/document/d/17Etkil26A1xv8SqEzZW3t44FHz9TNxNWrzWm6O_WyTI/edit
diagnostic_refs: []
relations:
  - type: produced_by_run
    target: RUN-HR-001
  - type: contradicts
    target: HYP-HR-001
---

# 2026H1 v0.1 execution result

## Observation

The frozen v0.1 execution-aware proxy produced:

- 2,685 evaluable trades
- mean expectancy: -0.201598R/trade
- median: -1.001100R
- win rate: 34.7486%
- Profit Factor: 0.660341
- maximum consecutive losses: 20
- maximum drawdown: 542.166368R
- target hits: 303
- stop hits: 1,404
- time stops: 978

The primary result is spread-aware through historical BID/ASK quote sides.

No additional live slippage, commission, financing, latency, broker markup, or venue-specific execution effect was established.

## Scientific result

The frozen v0.1 implementation is **not supported as a tradable execution-aware candidate on this consumed sample**.

This result does not prove that all horizontal-reaction phenomena are absent.

## Boundary

The result does not establish:

- future profitability,
- live fillability,
- optimal parameters,
- causality,
- broker-specific net performance.

It does not authorize parameter rescue on the same 2026H1 sample.

## Source

https://docs.google.com/document/d/17Etkil26A1xv8SqEzZW3t44FHz9TNxNWrzWm6O_WyTI/edit
