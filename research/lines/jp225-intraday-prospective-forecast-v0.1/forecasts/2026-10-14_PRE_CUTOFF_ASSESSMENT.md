---
type: PreCutoffPreliminaryAssessment
event_id: XPF-JP225-20261014
research_line_id: RL-JP225-PROSPECTIVE-001
observed_at: 2026-10-14T07:53:41+09:00
formal_forecast_issued: false
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
model_identifier: GPT-6
---

# JP225 2026-10-14 pre-cutoff quantitative assessment

## Temporal control

This numerical candidate snapshot was drafted using only evidence explicitly timestamped before **2026-10-14 08:00 JST**, and committed before that cutoff. Subsequent official issue after 08:00 must reproduce the values without new inference, and record actual issue/commit times truthfully. If GitHub issuance occurs after 09:00, record explicit lateness and do not disguise it. Market outcome was not accessed for this forecast; no XM MT5 price retrieval.

**Research target: Nikkei-type session 09:00→15:30 JST return of qualified exact XM JP225Cash (Bid/Ask midpoint), NOT the October 13 close to October 14 close, and NOT the overnight futures gap.** All public market data are **proxy-only context**, not qualified exact-XM input. Scientific status `UNTESTED`, protocol `PROPOSED_NOT_FROZEN`, cohort `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`, formal 60-event cohort `CLOSED`, action `NO_TRADE`.

## Frozen provisional numbers (all subjective / uncalibrated)

| System | P(up, 09:00→15:30) | Forecast log return |
| --- | ---: | ---: |
| B0 neutral benchmark | 0.50 | 0 bps |
| A1 public target-market futures proxy only | **0.52** | **+3 bps** |
| A2 market / macro / FX / public reports | **0.49** | **-2 bps** |
| A3 with existing repository research status | **0.50** | **0 bps** |

**Headline A3: no demonstrated direction; neutral; very low conviction and NO_TRADE.** The above are deliberately tentative explorations, NOT estimated coefficients, market-proven probabilities, or previous-event fitted outputs. B0 is always neutral; A3 happens to match B0 this session and is not a claim of equal validated skill.

## Facts verifiably published before 08:00 JST on 2026-10-14

1. **Osaka Exchange Nikkei 225 December-2026 futures**, 06:00 JST overnight close **68,100**, **+140 points versus the previous futures settlement**, published 06:03 JST by Kabutan. December mini overnight close **68,110**, +150. Public cash index previous close (Oct 13) **67,777.52**; main future +322.48 over that *different instrument* reference. This is overnight **opening context**, not the target intraday return, and exact futures-vs-cash spread is not an XM predictor. https://minkabu.jp/news/4634620
2. Matsui Securities reprints same **06:03 JST** notice confirming **68,100** overnight Dec-future and +140 vs futures previous settlement; **not independent price discovery** as article identical. https://finance.matsui.co.jp/news/626797/index
3. A **05:32 JST** published New York market report: U.S. Oct 13 Dow **51,670.10** (**-180.45, -0.35%**), S&P 500 **7,805.45** (**-1.79, -0.02%**), Nasdaq composite **27,204.38** (**-41.52, -0.15%**). U.S. tech and memory-related shares were weak. The same report includes **CME Nikkei futures 68,235** observed around 05:20 JST, +275 versus Osaka previous session; a different market/time to Osaka's **06:00** futures close of 68,100, so **not** an inconsistent quote for the same instrument/time. https://minkabu.jp/news/4634615
4. **06:21 JST** timestamped NY market digest covering Oct 13 close: USDJPY **158.33** (prior-day change -0.28 yen), U.S. 10-year yield **5.21%** (-0.03 percentage points), WTI Nov crude **$94.14** (+$0.40), Dow 51,670.10, Nasdaq 27,204.38. Published on Myforex at 06:21 and cross-presented on the associated dated digest site. This reports a somewhat firmer yen and elevated crude, but their effects on the post-opening JP225 return are not calibrated. https://www.myforex.com/ja/news/dzh261014050.html
5. A 06:22 JST Fisco published recap also reported U.S. Dow and Nasdaq declines and relative weakness in semiconductor shares, with energy-sector strength. It is same prior-night U.S. session, not an independent 08:00 Japanese signal. https://www.zaikei.co.jp/article/20261014/873307.html
6. JPX regular calendar: Wednesday October 14 is a scheduled Japan cash-equity trading day. Monday October 12 was a holiday; the cash session reopened Oct 13. https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html
7. **Excluded:** dynamic JPX future webpage lacking point-in-time frozen raw version; fresh 08:00 XM quote and exact 1h/4h/24h lookbacks (unavailable); any 09:00 opening price, 15:30 close, today's intraday outcomes, or market reports after 08:00. Do not silently fill these gaps.

## Hypothesis/interpretation by system, pre-cutoff only

**A1:** Overnight OSE and CME futures showed positive *opening* context versus their reference futures settlements; the OSE Dec future was > prior cash close. However opening gaps can be entirely incorporated into the 09:00 opening. Without exact XM 08:00 features and with public data as proxy only, use a **very weak upward lean**, `p_up=0.52`, `return=+3bps`. This is **not** a valid fully sourced exact-XM-only A1 model.

**A2:** U.S. equities fell, notably memory/tech; oil rose; the yen strengthened somewhat to about 158.33 while remaining relatively weak in absolute terms. This could offset the positive Japan overnight futures opening signal. The U.S. broad S&P 500 was almost flat, so a uniform risk-off assertion is unwarranted. Net mild bearish/near-neutral `p_up=0.49`, `return=-2bps`. Numerical coefficients are not estimated and no statistically supported edge exists.

**A3:** Source-pinned main commit `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3` has JP225 EMA `UNTESTED / WAITING_FOR_XM_STAGE1_DATA`, OANDA persistence `PERSIST5_PROXY_NOT_SUPPORTED_2017`, and US-lead reversal `STOPPED / USLEAD_PROXY_NOT_SUPPORTED_2015`. These results **do not** establish bullish, bearish or reversal skill; no supported strategy provides reason to amplify a small A2 tilt. Exploratory uncertainty-aware near-neutral A3 `p_up=0.50`, `return=0bps`. It is not a trained regularization operation and conveys no evidence of improvement.

## Counterevidence, source discipline and scientific decisions

- Although futures overnight closes were modestly positive, they do not determine the **09:00→15:30** direction.
- Previous Japanese day saw a large decline, but that observed Oct 13 result was **not** used to fit/tune any model or create a day-after-loss rebound hypothesis.
- Small U.S. equity falls with nearly flat S&P, lower U.S. long yield, moderately firmer yen, higher oil, and mixed sectors do not provide a validated sign for JP225 post-opening cash change.
- Distinguish OSE vs CME venues/timestamps, futures settlements vs Japanese cash close, and public indices vs XM quotes. No broker replacement permitted.
- There are **zero qualified exact-XM JP225Cash observations** for today's cutoff; all A1/A2/A3 values are subjective research dry-run outputs.
- No trading, parameter optimization, feature selection, outcome-backfill, historical holdout inspection or respecification.

## Source references and immutable repository context

- https://minkabu.jp/news/4634620 (06:03 JST Osaka close)
- https://finance.matsui.co.jp/news/626797/index (06:03 JST reprint, not independent)
- https://minkabu.jp/news/4634615 (05:32 JST U.S. close and CME context)
- https://www.myforex.com/ja/news/dzh261014050.html (06:21 JST U.S./FX/yields/WTI)
- https://www.zaikei.co.jp/article/20261014/873307.html (06:22 JST Fisco U.S. recap)
- https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html (official calendar)
- https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-ema-timeofday-v0.1/CURRENT.md
- https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-us-lead-reversal-v0.1/CURRENT.md

## Custody note on preceding pre-registration

The October 14 `PRE_REGISTRATION.md` front matter states an indicative `registered_at=07:52:00`, but the actual GitHub commit `c91afbb0f3d07699498d6fd9409a9c6eadff4ff4` occurred at **07:52:53 JST**. This note corrects the provenance **without overwriting the earlier file**. The actual GitHub commit time is authoritative for pre-registration.

## Freeze decision

**Fix B0 0.50 / 0bps; A1 0.52 / +3bps; A2 0.49 / -2bps; A3 0.50 / 0bps**, without changing these values after 08:00. Future formal issuance must report actual issue timestamp and SHA-256; remain `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT` and `NO_TRADE`.
