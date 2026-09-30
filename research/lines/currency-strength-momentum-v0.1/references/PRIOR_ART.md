# Prior art — Currency Strength Momentum v0.1

Reviewed: 2026-10-01

## Published evidence

### Menkhoff, Sarno, Schmeling, Schrimpf (2012)

"Currency Momentum Strategies", Journal of Financial Economics 106(3), 660-684.
DOI: 10.1016/j.jfineco.2012.06.009

Relevant design:

- currencies are ranked by lagged returns;
- winner-minus-loser currency portfolios are formed monthly;
- formation and holding periods include 1, 3, 6, 9, and 12 months;
- the study reports positive cross-sectional momentum spreads;
- transaction costs materially reduce the returns.

Use here:

This supports cross-sectional currency momentum as a legitimate research hypothesis. It does not establish that a single strongest-minus-weakest pair among eight majors is profitable now.

### Moskowitz, Ooi, Pedersen (2012)

"Time Series Momentum", Journal of Financial Economics 104(2), 228-250.
DOI: 10.1016/j.jfineco.2011.11.003

Relevant point:

Return persistence was reported across multiple asset classes, including currencies, primarily over 1-12 month horizons.

Boundary:

Time-series momentum is not identical to the cross-sectional strongest-minus-weakest test.

### Huang et al. (2020)

"Time series momentum: Is it there?", Journal of Financial Economics 135(3), 774-794.
DOI: 10.1016/j.jfineco.2019.08.004

Relevant counterpoint:

The paper argues that evidence for time-series momentum predictability is weaker than pooled results may suggest and that strategy profitability need not imply the proposed predictability mechanism.

Use here:

Do not treat generic momentum literature as proof of this exact FX mechanism.

### Zhang (2022)

"Dissecting currency momentum", Journal of Financial Economics 144(1), 154-173.
DOI: 10.1016/j.jfineco.2021.05.035

Relevant point:

The paper reports that cross-sectional and time-series currency momentum are largely explained by momentum in carry and dollar factors, while idiosyncratic currency returns contain little momentum.

Use here:

If v0.1 shows positive continuation, the next scientific question is whether that continuation survives factor decomposition. Factor controls are deliberately not added to the first bounded screen.

## GitHub prior example

Repository:
nateemma/fx-strategy-framework

Current default-branch review on 2026-10-01 found:

- a reusable cross-sectional momentum implementation that ranks trailing per-currency returns and forms long/short baskets;
- a documented intraday FX assessment that tested currency-strength ranking first;
- commit b723aa48c3a08bc63d11bbaa2233245a80871233 records the 1h / two-year / seven-major currency-strength continuation premise as rejected, with negative rank-IC and cost-dominated reversion;
- commit 74d3c0f8da65a35b8a95955fbf0606ebaa0d9e5c fixes a lookahead bug caused by backward-filling future volatility forecasts.

Transferable lessons:

1. Do not infer monthly behavior from intraday behavior.
2. Cost-free signal evidence and executable economics are separate questions.
3. Cross-sectional ranking must be tested with point-in-time transformations.
4. A diagnostic or framework can still contain a concrete lookahead bug; causal checks and code review remain necessary.
5. Preserve negative results rather than adding filters until something becomes positive.

## v0.1 design consequence

The first test stays deliberately small:

- eight fixed major currencies;
- one-month formation;
- one-month forward horizon;
- spot-price phenomenon only;
- one frozen definition;
- no parameter sweep;
- no factor or execution rescue.

A positive result can only justify a second, separately frozen test. A negative result is a terminal result for this exact v0.1 specification.
