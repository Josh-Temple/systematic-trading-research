---
type: PreCutoffPreliminaryAssessment
event_id: XPF-JP225-20261009
research_line_id: RL-JP225-PROSPECTIVE-001
observed_at: 2026-10-09T07:50:37+09:00
formal_forecast_issued: false
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
model_identifier: GPT-6
---

# JP225 — 2026-10-09 pre-cutoff quantitative assessment

**This is a preliminary, pre-08:00 JST frozen snapshot, NOT an issued forecast.** The eventual issuance timestamp must be truthful and at/after 08:00. Do not re-infer these numbers from post-cutoff information.

Target: JP225 09:00→15:30 JST **intraday** move, not close versus the prior day. Subjective exploratory, **NOT calibrated** and **NO_TRADE**.

## Fixed probabilities and forecasts

| System | p(up) | Predicted log return |
| --- | ---: | ---: |
| B0 neutral | 0.50 | 0 bps |
| A1 (public-futures proxy only; exact XM unavailable) | 0.48 | -4 bps |
| A2 (cross-market and news) | 0.44 | -10 bps |
| A3 (A2 plus status-preserving repository) | 0.46 | -7 bps |

**A3: mildly bearish / low conviction.**

## Facts available before 08:00 JST (all source publication times checked)

1. 2026-10-09 06:00 JST Osaka Nikkei 225 Dec futures night close **68,390**, **-710** vs previous futures settlement, **-652.11** below yesterday's Nikkei cash close **69,042.11**; Kabutan publication **06:03 JST**.
2. 2026-10-09 04:13 JST CME Nikkei futures about **68,360**, **-740 / -1.08%** vs Osaka daytime settlement; published **04:23 JST**, data explicitly delayed 10 min.
3. U.S. Oct 8 NY close (OANDA summary published **06:20 JST**): **Nasdaq 27,193.34** (-345.35; ~-1.25%); **Dow 51,231.64** (+51.77); **U.S. 10y yield 5.22%** (-0.06 pp); **WTI 91.49 USD** (+3.21 USD). Downside pressure more pronounced in technology than in the Dow.
4. Reuters report published **05:11 JST**: U.S. semiconductor shares weaker; SOX **-3.68%**. Some Reuters early transmission index closing figures differ from OANDA's 06:20 figure; do not conflate exact price levels.
5. USDJPY NY close around **157.88** (OANDA 06:20; -0.20 JPY vs prior); Kyodo published 06:34 quotes **157.83–157.93**. Moderate yen strengthening; still relatively weak in absolute yen terms.
6. JPX official calendar: **Friday 2026-10-09 is a cash trading day**; **Monday 2026-10-12 is Sports Day, cash-market holiday**, distinct from derivatives holiday trading.
7. The yesterday cash-index close 69,042.11 is prior-session context. **No 2026-10-09 09:00 or 15:30 market outcome was accessed, anticipated as fact, or used.**

## Interpretation before cutoff

**A1 proxy-only:** Adverse futures gap suggests a lower *open*, not necessarily continued 09:00→15:30 decline. Exact 08:00 XM JP225Cash Bid/Ask and deterministic 1h/4h/24h market features not retrieved. Therefore p(up)=0.48, -4 bps is explicitly a proxy-only subjective heuristic, **not a valid exact-XM target-only estimator**.

**A2:** Nasdaq and SOX weakness, oil rally and small JPY appreciation add risk-off pressure, but the overnight move may be incorporated into the cash open; Dow gains and lower U.S. yields temper extrapolation. Hence 0.44, -10 bps with uncertainty.

**A3:** Fresh-read `main` SHA `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3` preserves JP225 EMA `UNTESTED / WAITING_FOR_XM_STAGE1_DATA`, 2017 OANDA proxy `PERSIST5_PROXY_NOT_SUPPORTED_2017`, and US-lead reversal `STOPPED / USLEAD_PROXY_NOT_SUPPORTED_2015`. None supports a validated intraday continuation or reversal edge. A3 moderates the unsupported extrapolation (0.46, -7 bps); **not a learned coefficient, performance optimization, or claim of skill**.

## Counterevidence / limitations

- Futures pressure may be mostly priced into 09:00 open; a rebound is possible. Overnight futures are not 09:00→15:30 outcomes.
- Dow marginally rose and U.S. yields fell, unlike the technology sector.
- Overnight USDJPY near 158 is weak-yen context despite a small yen appreciation.
- Friday before a cash-market holiday is contextual only; no validated weekday adjustment was applied.
- No exact XM source, no formal scored event, no trade. This model did **not** fit weights to Oct 6 or Oct 8 outcomes.

## Timestamped pre-cutoff sources

- https://www.jpx.co.jp/calendar/202610.html
- https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html
- https://minkabu.jp/news/4632451 (06:03)
- https://fx.minkabu.jp/news/381162 (04:23)
- https://www.oanda.jp/lab-education/market_news/mn_1038097_202610090620/ (06:20)
- https://www.newsweekjapan.jp/articles/-/336421 (05:11)
- https://www.oanda.jp/lab-education/market_news/kn_2026100901000920/ (06:34)
- https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-ema-timeofday-v0.1/CURRENT.md
- https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-us-lead-reversal-v0.1/CURRENT.md

## Research decision

Preserve `PROPOSED_NOT_FROZEN / UNTESTED / SCORED_COHORT_CLOSED`. Future issuance must transcribe **0.48/-4, 0.44/-10, 0.46/-7** without new inference; any late issuance must be called late.
