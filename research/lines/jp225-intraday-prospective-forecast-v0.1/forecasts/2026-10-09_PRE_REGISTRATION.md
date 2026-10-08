---
type: ProspectiveEventPreRegistration
event_id: XPF-JP225-20261009
research_line_id: RL-JP225-PROSPECTIVE-001
registered_at: 2026-10-09T07:49:42+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
forecast_status: PENDING
---

# JP225 prospective dry run pre-registration — 2026-10-09

## Event and locked candidate protocol

- Information cutoff: **2026-10-09 08:00:00 JST**.
- Intended forecast issuance: at or immediately after 08:00 JST, with truthful actual timestamp.
- Target return window: **2026-10-09 09:00:00 to 15:30:00 JST**.
- Formal reference: qualified exact XM MT5 `JP225Cash` Bid/Ask midpoint; **not acquired in this run at user's request**.
- Exploratory-only status: `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`; scored cohort `CLOSED`; specification `PROPOSED_NOT_FROZEN`; scientific `UNTESTED`; `NO_TRADE`.
- Candidate family: B0 neutral 0.50/0 bps; A1 target-market-only; A2 plus market/fundamental/cross-market/news; A3 plus status-preserving repository evidence.
- 2026-10-09 is a scheduled Friday trading day under the JPX 2026 October calendar. 2026-10-12 is Sports Day and a *cash-market* holiday (separate derivatives holiday trading is not cash-market eligibility).
- Official JPX calendar: https://www.jpx.co.jp/calendar/202610.html
- Official JPX annual holiday list: https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html

## Anti-leakage boundary

Only market/economic information **published or observably available no later than 08:00 JST** may inform the forecast. Unverifiable timestamp/live pages must be quarantined. Preserve known provider, scope, and publication timing in a separate 07:xx pre-cutoff assessment. Do not use post-08:00 outcomes, live market prices, later reports, or the 09:00 opening to update probabilities.

The prior 2026-10-06 and 2026-10-08 exploratory outcomes are **not** training observations and cannot be used to optimize coefficients or weights.

## Source and review plan

- Preserve exact-XM input missingness; publicly reported cash/futures values may be *proxy-only exploratory context* but not exact A1 or formal outcomes.
- Preserve forecast records as append-only with actual issuance timestamps and canonical SHA-256; late issuance, if any, must be explicitly flagged.
- After 15:30: without qualified XM prices, formal review is `MARKET_OUTCOME_UNAVAILABLE` and formal score remains empty. Any public Nikkei cash-index comparison must be separately labeled `PUBLIC_PROXY_REVIEW`.
- Do not trade, change the candidate spec, merge PR #62, or schedule automation based on this event.

## Registration evidence

- GitHub repo: Josh-Temple/systematic-trading-research.
- PR #62: open/draft at fresh read; initial head `04c1ed0d98597236a28d7dd455e1de07fe0b092b`.
- This file fixes the event before cutoff but **does not** itself constitute a completed pre-cutoff quantitative forecast.
