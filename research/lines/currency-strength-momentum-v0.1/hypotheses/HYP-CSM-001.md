---
id: HYP-CSM-001
type: Hypothesis
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: UNTESTED_V0_1
relations: []
---

# Strongest-minus-weakest major-currency continuation

## Statement

Among AUD, CAD, CHF, EUR, GBP, JPY, NZD, and USD, the currency with the strongest spot appreciation over the immediately preceding calendar month, held long against the weakest currency, has a positive spot return over the next calendar month on average.

## Mechanism class

Cross-sectional currency momentum / relative-strength continuation.

## Prior basis

The hypothesis is motivated by published evidence on cross-sectional currency momentum, especially Menkhoff, Sarno, Schmeling, and Schrimpf (2012), while recognizing later evidence that much currency momentum may reflect momentum in common carry and dollar factors rather than idiosyncratic currency persistence.

## Counterevidence already known

A separate public GitHub research project, nateemma/fx-strategy-framework, reports that a 1-hour / two-year / major-currency currency-strength momentum screen produced negative rank information coefficients and was rejected as an intraday continuation premise (commit b723aa48c3a08bc63d11bbaa2233245a80871233).

That result is relevant negative prior evidence but does not test this monthly v0.1 hypothesis.

## Boundary

This hypothesis does not assert:

- positive performance at intraday horizons,
- positive excess returns after financing, spreads, commissions, or slippage,
- independence from carry or dollar factors,
- profitability of any indicator implementation that uses volatility normalization, multiple horizons, smoothing, or discretionary filters.
