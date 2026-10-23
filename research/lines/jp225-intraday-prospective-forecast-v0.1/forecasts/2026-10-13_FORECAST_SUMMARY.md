---
type: ProspectiveForecastSummary
event_id: XPF-JP225-20261013
research_line_id: RL-JP225-PROSPECTIVE-001
pre_registered_at: 2026-10-13T07:55:04+09:00
pre_cutoff_assessment_at: 2026-10-13T07:55:49+09:00
information_cutoff: 2026-10-13T08:00:00+09:00
issued_at: 2026-10-13T08:00:01+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# JP225 2026-10-13 exploratory forecast summary

**Target:** scheduled JPX cash day 09:00 to 15:30 JST intraday change, not previous close to today close. **Information cutoff:** 08:00 JST on Oct 13.

An assessment was recorded at 07:55:49 JST, GitHub-committed at 07:56:35 JST (pre-cutoff), and all numerical probabilities/return forecasts were fixed before the cutoff at https://github.com/Josh-Temple/systematic-trading-research/blob/5804cc24264bf4a72746515bf74042fb3ef52b53/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-13_PRE_CUTOFF_ASSESSMENT.md. Formal JSONs begin their single atomic issue at 2026-10-13T08:00:01+09:00 JST (actual Git commit is the authoritative publication timestamp); no post-cutoff inputs or reinference.

| System | Frozen P(up) | Frozen return |
| --- | ---: | ---: |
| B0 neutral | 0.50 | 0 bps |
| A1 public-futures proxy only | 0.49 | -2 bps |
| A2 cross-market | 0.47 | -6 bps |
| A3 status-preserving repo | **0.48** | **-4 bps** |

**A3: essentially neutral with a mild bearish tilt, very low conviction. No trade.** These are subjective exploratory numbers, NOT validated or statistically calibrated probabilities.

## Scientific and input boundaries

- `SPEC-JP225-FORECAST-001-v01` `PROPOSED_NOT_FROZEN`; scientific `UNTESTED`, scored cohort `CLOSED`, status `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`.
- No actual XM `JP225Cash` Bid/Ask retrieved under owner's XM deferral. A1 uses proxy-only market context, **not qualified exact-XM target market data**.
- A 06:00 OSE Dec 2026 futures snapshot was around 68,380, down 1,090 versus a futures settlement; a 06:23 CME225 report also 68,380 but on a distinct instrument. Other 06:00 public mini future sources conflicted by 645 points (68,995 vs 68,350). Conflicts were explicitly quarantined; no formal price features or raw-feed qualification.
- Oct 12 U.S. equity close: mixed (Nasdaq down about 0.44%, Dow up about 0.38%), WTI higher and USDJPY near 158.6. This is mostly opening context, **not proven 09:00-15:30 forecast edge**.
- Pre-cutoff repository statuses of JP225 EMA and US-lead reversal were copied as negative/unverified evidence, not treated as proven strategies.
- No historical-outcome model optimization, changing parameters, merging this draft PR, actual trading, or formal market P/L.
- For formal after-close review, missing qualified XM exact 09:00/15:30 data implies `MARKET_OUTCOME_UNAVAILABLE`, null quotes and returns, and empty `scores={}`. Public Nikkei cash-index diagnostics after 15:30 must be kept in separately named proxy review.

## Canonical SHA-256 integrity (JSON content excluding canonical_sha256)

| JSON record | Canonical SHA-256 |
| --- | --- |
| `2026-10-13_A1_forecast.json` | `e14ea4f17f3ad169a8a9a9f9ad396e28e08d9bed03cf0d28b356f1a0cbeede6d` |
| `2026-10-13_A2_forecast.json` | `d6915802ab7f6055d2bc360644d9046cd8b722d940c1cf2480c2d59e997a0e9c` |
| `2026-10-13_A3_forecast.json` | `8063b37175e25a902626bc7827a2b10a5de38c54a10dc4040573a9d6fd6d9059` |

GitHub Actions outcome must be checked on the final commit; **passing synthetic tests is not formal scientific validation**. Preserve Oct 6 legacy hash mismatch warnings rather than misreporting them as pass.

## Frozen evidence

- https://github.com/Josh-Temple/systematic-trading-research/blob/5804cc24264bf4a72746515bf74042fb3ef52b53/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-13_PRE_CUTOFF_ASSESSMENT.md
- Official holiday calendar: https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html
- OSE/JPX dynamic pre-cutoff future page: https://port.jpx.co.jp/jpxhp/main/index.aspx?F=future
- Timestamped 06:23 CME futures report: https://www.traders.co.jp/news/article/1_2206428
- Timestamped 06:20 NY market close and FX: https://www.traderswebfx.jp/news/article/1214941
- Timestamped 06:49 Reuters NY market summary: https://www.newsweekjapan.jp/articles/-/336644
- Contradictory public futures snapshot: https://s.kabutan.jp/futures/%E6%97%A5%E7%B5%8C225%E5%85%88%E7%89%A9%E3%83%9F%E3%83%8B/

No news, price or market information acquired after the 08:00 cutoff was used to set or modify this event.
