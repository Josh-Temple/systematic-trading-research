---
type: PreCutoffPreliminaryAssessment
event_id: XPF-JP225-20261013
research_line_id: RL-JP225-PROSPECTIVE-001
observed_at: 2026-10-13T07:55:49+09:00
formal_forecast_issued: false
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
model_identifier: GPT-6
---

# JP225 2026-10-13 pre-08:00 preliminary quantitative snapshot

This snapshot is recorded BEFORE the **2026-10-13 08:00 JST information cutoff**. It fixes all B0/A1/A2/A3 numbers and explanations in advance. Formal immutable JSON may only be issued **at or after 08:00**, with truthful issuance time and any late-issuance deviation. Transcribe the fixed values **without post-cutoff re-inference**. No XM prices have been acquired. This is **exploratory and subjective**, not statistically estimated or formal trading guidance.

**Target: exactly 2026-10-13 09:00→15:30 JST intraday change**, *NOT prior close→today's close* and NOT the overnight futures gap. Scheduled JPX cash day after Monday October 12 Sports Day.

## Pre-cutoff frozen candidate estimates (no model retraining)

| System | P(09:00→15:30 goes up) | Forecast log-return |
| --- | ---: | ---: |
| B0 neutral comparator | 0.50 | 0 bps |
| A1 proxy-only target-market context; exact XM unavailable | **0.49** | **-2 bps** |
| A2 plus cross-market, FX, news | **0.47** | **-6 bps** |
| A3 plus repository state, preserving unsupported hypotheses | **0.48** | **-4 bps** |

**A3 headline: almost neutral / very weak bearish tilt, low confidence; NO_TRADE.** 0.48 means subjective 48% probability of a positive move in the fixed 09:00→15:30 interval; it does **not** imply 52% validated downside accuracy.

## Available-at/before-07:55:49 JST source observations

1. **Official JPX cash calendar**: Oct 12 cash holiday, Oct 13 Tuesday regular cash session. https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html
2. **JPX/QUICK futures display captured via web search during this pre-cutoff session**: Nikkei 225 future Dec-2026, trading-date Oct 13 **06:00 JST 68,380**, shown at **-1,090** vs reference settlement. The same page shows 04:10 overnight low 68,340, timestamp 04:10. **This is OSE futures not the target, not exact XM, and the dynamic page provides no immutable point-in-time raw receipt.** https://port.jpx.co.jp/jpxhp/main/index.aspx?F=future
3. **Independent time-stamped market report 06:23 JST**: CME225 yen-denominated futures **68,380**, -1,090 vs Osaka prior day session. https://www.traders.co.jp/news/article/1_2206428 . **CME futures and Osaka futures are distinct instruments**, though quoted levels happen to match. Do not treat as independently confirmed identical instrument readings.
4. **Source-quality conflict:** Kabutan's dynamically cached Nikkei 225 *mini* page displayed **68,995 at 06:00** for Dec-2026 contract, while JPX's displayed mini Dec-2026 was **68,350 at 06:00**. No common version/capture provenance resolves the **645-point contradiction**. Consequently **do not qualify either as exact current spot/JP225Cash input**, and discount precise futures price in forecast sign/magnitude. https://s.kabutan.jp/futures/%E6%97%A5%E7%B5%8C225%E5%85%88%E7%89%A9%E3%83%9F%E3%83%8B/ . The large gap is discussed qualitatively only and no exact-XM feature inferred.
5. **U.S. close for Mon Oct 12**, as reported **2026-10-13 06:20 JST**: Dow **51,850.55** (+195.60), Nasdaq composite **27,245.90** (-120.27, roughly -0.44%), USDJPY **158.61** (+0.30 yen), WTI Nov crude **USD 93.74** (+USD 1.89). U.S. 10yr Treasury market CLOSED for the Columbus Day holiday; no fresh traded bond-close yield can be asserted. https://www.traderswebfx.jp/news/article/1214941 . AP separately reports Dow +0.4%, Nasdaq -0.4%, S&P -0.1%, energy firm; do not rely on later timestamps without verification.
6. **Reuters market recap published 2026-10-13 06:49 JST**: Nasdaq declined, dollar index strong, USDJPY about **158.66**; U.S. bond market holiday; coverage suggests caution around geopolitical risk and future U.S. inflation data. https://www.newsweekjapan.jp/articles/-/336644
7. **Early session observable dated report (03:16 JST)**: CME Nikkei futures **68,490 at 03:06 JST**, versus Osaka daytime settlement -980, confirming prior to cutoff a large negative futures gap at that hour; old snapshot, **not** the 07:55 spot. https://fx.minkabu.jp/news/381327
8. **No Oct 13 Japanese cash opening/closing index, 09:00–15:30 price path, late news, formal XM prices, same-day P/L or trade outcomes** were accessed as forecast inputs.

## Frozen interpretation by system

**A1**: Marked `exact_xm_input_status=UNAVAILABLE`: missing 08:00 exact-XM JP225Cash Bid/Ask tick, 1h/4h/24h lookback and official reproducible target-only market features. Public overnight futures show opening downside risk, but opening gap does NOT by itself imply negative **post-open** return. Moreover cached OSE mini snapshots conflict. Subjective proxy-only A1 almost neutral: **P(up)=0.49; return -2bps**. It is not source-compliant A1 evidence.

**A2**: U.S. Nasdaq modestly declined despite positive Dow; higher oil and geopolitical caution are headwinds; weak absolute JPY around 158.6 could benefit exporters; the initial gap may already be fully reflected in cash 09:00 opening. The first cash trading session after holiday adds uncertainty rather than justified directional parameter adjustment. Slight bearish tilt **P(up)=0.47; -6bps**. No deterministic model mapping these covariates to return; figures are subjective diagnostic values only.

**A3**: GitHub main SHA `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3` freshly read. JP225 exact-XM EMA hypothesis remains **UNTESTED / WAITING_FOR_XM_STAGE1_DATA**, 2017 persistent-EMA proxy **PERSIST5_PROXY_NOT_SUPPORTED_2017**; US lead reversal proxy remains **STOPPED / USLEAD_PROXY_NOT_SUPPORTED_2015**. These negative/unverified results cannot justify trading continuation or mean-reversion and cannot imply better forecast skill. Therefore retain cautious near-neutral estimate **P(up)=0.48; -4bps**, smaller in magnitude than A2 because repository provides no validated boost to a gap-continuation hypothesis; this is descriptive judgment, **not** a tuned weighting coefficient.

## Counterevidence / outcome-blind limitations

- Dow +0.38% with Nasdaq -0.44% is mixed; an across-market one-direction narrative would be misleading.
- WTI strength hurts some sectors but favors energy. USDJPY about 158.6 can support Japanese exporters.
- Previous trading-day close vs future settlement are distinct, contract/expiry differ, and both must not be substituted for a 09:00→15:30 cash or exact-XM move.
- **Conflicting mini-futures 06:00 web representations** demonstrate a data-quality problem; neither is used as a numerically qualified signal.
- After a negative overnight gap, either intraday continuation or bounce is feasible. Historical exploratory Oct 6/8/9 outcomes were NOT used to tune today's values or optimize any specification.
- Model probabilities are **uncalibrated**. No reference quotes; scientific status UNTESTED; formal cohort CLOSED; NO_TRADE.

## Fixed source references

- https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html
- https://port.jpx.co.jp/jpxhp/main/index.aspx?F=future (dynamic, not a frozen versioned raw feed)
- https://www.traders.co.jp/news/article/1_2206428 (06:23 JST)
- https://www.traderswebfx.jp/news/article/1214941 (06:20 JST)
- https://www.newsweekjapan.jp/articles/-/336644 (06:49 JST)
- https://fx.minkabu.jp/news/381327 (03:16 JST)
- https://s.kabutan.jp/futures/%E6%97%A5%E7%B5%8C225%E5%85%88%E7%89%A9%E3%83%9F%E3%83%8B/ (contradictory dynamic source)
- https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-ema-timeofday-v0.1/CURRENT.md
- https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-us-lead-reversal-v0.1/CURRENT.md

## Pre-cutoff decision

Candidate specification unchanged: `PROPOSED_NOT_FROZEN`. Cohort `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`; exact XM missing; future formal XM outcome unavailable unless qualified exact route provided by owner, currently not requested. The numerical B0/A1/A2/A3 predictions above are frozen now and **must not change with post-08:00 information**.
