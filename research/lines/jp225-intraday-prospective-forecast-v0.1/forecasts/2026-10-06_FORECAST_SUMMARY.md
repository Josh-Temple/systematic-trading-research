---
type: ProspectiveForecastSummary
event_id: XPF-JP225-20261006
research_line_id: RL-JP225-PROSPECTIVE-001
information_cutoff: 2026-10-06T08:00:00+09:00
issued_at: 2026-10-06T08:22:44+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# JP225 prospective dry run — 2026-10-06

## Protocol status

This is a late-issued exploratory dry run. The human timing decision was made before 08:00 JST, but the forecast was not issued until 08:22:44 JST.

Protocol deviations:

- `LATE_ISSUANCE_AFTER_0800`
- `EXACT_XM_0800_INPUT_UNAVAILABLE`
- `PUBLIC_NON_XM_MARKET_CONTEXT_USED_FOR_EXPLORATORY_DRY_RUN`

Only information demonstrably available at or before 08:00 JST was admitted. No post-08:00 market information was used in the forecast.

Target remains exact XM MT5 `JP225Cash` midpoint change from 09:00 JST to 15:30 JST. Exact XM input was unavailable at issuance, so public futures/market data are exploratory context only and must not be treated as a formal substitute.

## Forecasts

| System | P(up) | Forecast return |
| --- | ---: | ---: |
| B0 | 0.50 | 0 bps |
| A1 | 0.53 | +4 bps |
| A2 | 0.58 | +13 bps |
| A3 | 0.56 | +9 bps |

A3 headline direction: **mildly bullish / low conviction**.

## Pre-cutoff factual inputs used

- Osaka Nikkei 225 futures night session ended at 70,180 at 06:00 JST, +90 versus prior settlement and 233.14 points above the prior cash close.
- A public Nikkei futures feed showed a last trade around 70,192.5 at 07:58 JST.
- USDJPY was around 157.99 at 06:10 JST.
- WTI was about -2.17% at 05:55 JST.
- U.S. stocks closed higher; Nasdaq was +1.05%, with technology leadership, while U.S. 10-year yields remained around the 5.30% area.
- The official Japanese statistical-release calendar showed no major Japanese government-statistics release on 2026-10-06 before the 15:30 endpoint.
- A market calendar listed a BOJ governor appearance at 15:35 JST, after the target endpoint.

## Interpretation

Positive overnight futures, U.S. technology strength, a weak yen and lower oil create a modest positive prior. Confidence is capped because much of the overnight futures strength can be incorporated into the 09:00 opening level, while the prior cash session had already risen 2.40% and high long-term yields leave a profit-taking / valuation headwind.

A3 is deliberately less bullish than A2. The repository does not contain validated exact-XM evidence justifying stronger confidence: the EMA line remains UNTESTED / WAITING_FOR_XM_STAGE1_DATA, and the separate U.S.-lead opening-reversal proxy line is STOPPED / NOT_SUPPORTED.

## Review boundary

The forecast is immutable after issuance. After 15:30, review the exact issued records first. Use exact XM start/end quotes only if the qualified route is genuinely available; otherwise record `MARKET_OUTCOME_UNAVAILABLE` and do not substitute another provider.

No trade or position sizing is authorized.
