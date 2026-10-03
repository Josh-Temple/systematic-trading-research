---
id: REF-FXMP-SCI-001
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-03
status: PARTIAL_WITH_GAPS
execution_status: SUCCESS
evidence_validity: VALID_FOR_REVIEW_SCOPE
scientific_status: NOT_APPLICABLE
tests_hypothesis: NOT_APPLICABLE
relations:
  - type: supports
    target: HYP-FXMP-001
---

# Packet B — monetary policy, fundamentals and FX prior-art review

## Scope

Dated pre-outcome literature review. No FX market outcome for HYP-FXMP-001 was calculated.

The review separates:
- macro fundamentals;
- policy-rule fundamentals;
- policy-rate/interest differentials;
- monetary-policy surprises/shocks;
- economic momentum;
- price momentum/carry;
- state dependence.

It does not treat these as interchangeable.

## Executive synthesis

The literature supports a narrow empirical test of monetary-policy information in FX, but strongly rejects a simplistic interpretation that "higher or rising policy rates mechanically imply currency appreciation".

Three points are especially relevant:

1. Exchange rates can be linked to fundamentals even when changes are hard to forecast.
2. Policy information is richer than the observed policy-rate level/change: inflation, activity, expectations, surprises and regime state can matter.
3. The sign and strength of interest-rate/currency relations can change across regimes and with carry positioning.

Therefore HYP-FXMP-001 is scientifically reasonable only as a bounded incremental-information screen.

## Evidence

### Engel & West — Exchange Rates and Fundamentals

NBER Working Paper 10723 / later JPE publication.  
https://www.nber.org/papers/w10723

They show that a present-value exchange-rate model can produce near-random-walk exchange-rate behavior even when exchange rates and fundamentals are linked. This cautions against equating weak direct predictability with irrelevance of fundamentals.

Relevance: supports the broader motivation, not the exact policy-rate feature.

### Andersen, Bollerslev, Diebold & Vega (2003) — Micro Effects of Macro Announcements

American Economic Review 93(1), 38–62.  
https://www.aeaweb.org/articles?id=10.1257/000282803321455151

Using real-time expectations, realizations and high-frequency FX quotes, the paper reports conditional-mean exchange-rate jumps around macro announcement surprises.

Relevance: the "surprise" relative to expectations matters; a monthly policy-rate change is not equivalent to a monetary-policy surprise.

### Molodtsova & Papell — Taylor Rule Exchange Rate Forecasting During the Financial Crisis

NBER Working Paper 18330 / NBER ISOM 2012 chapter.  
https://www.nber.org/papers/w18330

The study reports that some Taylor-rule specifications outperform a random walk in selected out-of-sample windows and outperform simpler interest-differential, monetary and PPP models in their euro/dollar design.

Relevance: policy stance may be useful, but observed interest differentials alone can omit information in inflation/activity responses.

### Engel, Lee, Liu, Liu & Wu — UIP Puzzle, Exchange Rate Forecasting, and Taylor Rules

NBER Working Paper 24059 / later journal publication.  
https://www.nber.org/papers/w24059

The authors cast doubt on broad Taylor-rule out-of-sample forecasting claims. In a related in-sample result, US inflation is significant while the interest-rate differential is not.

Relevance: strong counterweight to treating a policy-rate differential as the complete fundamental state.

### Dahlquist & Hasseltoft (2020) — Economic momentum and currency returns

Journal of Financial Economics 136(1), 152–167.  
https://www.sciencedirect.com/science/article/pii/S0304405X19302211

Past trends in activity and inflation fundamentals predict currency returns in their design. The paper reports an annualized Sharpe ratio of 0.70 for its economic-momentum strategy, and predictive content distinct from standard carry, momentum and value strategies.

Relevance: direct prior that fundamental trends can contain incremental currency information. Their predictors, horizons, portfolios and payoff are not the proposed BIS policy-rate alignment feature.

### Calomiris & Mamaysky (2019) — Monetary Policy and Exchange Rate Returns: Time-Varying Risk Regimes

NBER Working Paper 25714.  
https://www.nber.org/papers/w25714

A text-derived global central-bank stance measure predicts exchange-rate returns in their design. The reported relation between developed-market carry and future currency returns changes sign between pre- and post-crisis subperiods.

Relevance: policy information may matter, but state/regime dependence is material and the measure is not a simple policy-rate change.

### Schmitt-Grohé & Uribe (2022) — Permanent versus transitory monetary shocks

Journal of International Economics 135, 103560.  
https://www.sciencedirect.com/science/article/pii/S0022199621001409

The paper finds different, even opposite, exchange-rate implications for permanent and transitory monetary shocks in its model/empirical setting.

Relevance: an observed rate increase is not a homogeneous structural shock. HYP-FXMP-001 must remain predictive/descriptive rather than causal.

### Hutchinson et al. (2022) — Are carry, momentum and value still there in currencies?

International Review of Financial Analysis 83, 102245.  
https://www.sciencedirect.com/science/article/pii/S1057521922002058

The authors report substantial post-publication deterioration in traditional currency predictability, including carry/momentum/value, with their out-of-sample average Sharpe falling relative to in-sample evidence.

Relevance: adverse prior against assuming stable historical FX anomalies; any positive result still requires unused/prospective confirmation.

### Bartram, Grinblatt & Xu (2025) — Monetary Policy Predicts Currency Movements

NBER Working Paper 33423.  
https://www.nber.org/papers/w33423

The paper reports that a measure of relative central-bank monetary restrictiveness predicts raw and risk-adjusted currency returns. Importantly, its restrictiveness measure is derived from archived point-in-time monetary data and macro controls, not the observed policy-rate change alone.

Relevance: supportive contemporary prior for monetary-policy information, while showing that the richer policy state differs materially from HYP-FXMP-001.

### BIS Bulletin 124 (2026) — monetary-policy transmission and carry trades

https://www.bis.org/publications/bulletin-124-monetary-policy-transmission-exchange-rates-role-currency-carry-trades

The bulletin reports that carry positioning can amplify exchange-rate responses to monetary-policy tightening, implying state-dependent transmission.

Relevance: motivates explicit interpretation limits; a policy-rate relation need not be invariant across positioning regimes.

## What the literature supports

- Fundamentals and monetary-policy information can matter for FX.
- Relative/cross-country information is natural for currencies.
- Trend/change measures can contain information beyond price momentum in some designs.
- A narrow pre-outcome incremental-information test is justified.

## What the literature does not establish

- that three months is the uniquely correct policy-rate lookback;
- that BIS policy-rate changes are the best monetary-policy proxy;
- that policy-rate change and monetary-policy surprise are equivalent;
- that policy-rate alignment has a stable sign in 2010-2026;
- that a historical association would survive transaction costs;
- that a positive association would be causal;
- that policy rates subsume inflation/activity/expectations.

## Design implications before freeze

1. Keep HYP-FXMP-001 separate from broader "fundamentals" claims.
2. Do not add inflation, activity, OIS, sovereign yields or text sentiment after viewing HYP-FXMP-001 outcomes.
3. Preserve the break-aware BIS source rule.
4. Label the first test EXPLORATORY_DISCOVERY.
5. Require a new unused/prospective test before any tradable-edge conclusion.
6. Treat the proposed three-month lookback and minimum group counts as explicit pre-outcome human choices rather than literature-established constants.

## Review gaps

- This was a targeted primary-source review, not a formal exhaustive systematic review.
- Some evidence is from working papers rather than final journal versions.
- The exact HYP-FXMP-001 statistic has not been identified in the reviewed literature.
- No point-in-time BIS policy-rate replication paper for this exact eight-currency construction was found.

Status remains PARTIAL_WITH_GAPS despite sufficient evidence to guide the pre-outcome design.
