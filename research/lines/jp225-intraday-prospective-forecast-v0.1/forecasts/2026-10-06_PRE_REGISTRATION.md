---
type: ProspectiveEventPreRegistration
event_id: XPF-JP225-20261006
research_line_id: RL-JP225-PROSPECTIVE-001
registered_at: 2026-10-06T01:53:00+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
forecast_status: PENDING
---

# JP225 prospective dry run — 2026-10-06 pre-registration

## Event identity

- event_id: `XPF-JP225-20261006`
- date: 2026-10-06
- timezone: Asia/Tokyo
- eligibility: scheduled JPX cash-equity trading day
- forecast cutoff / target start: 2026-10-06 09:00:00 JST
- target end: 2026-10-06 15:30:00 JST
- cohort status: `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`
- scored v0.1 cohort effect: NONE

## Eligibility evidence captured before cutoff

Official JPX calendar:
- https://www.jpx.co.jp/calendar/202610.html
- 2026-10-06 is not marked as a market holiday.

Official JPX cash-equity trading hours:
- https://www.jpx.co.jp/equities/trading/domestic/01.html
- morning: 09:00-11:30 JST
- afternoon: 12:30-15:30 JST

These sources define the session/calendar only. They are not substitutes for exact XM `JP225Cash` prices.

## Forecast contract

At or immediately after the 09:00 cutoff, using only information available at or before 09:00:

- B0 neutral baseline;
- A1 JP225-market-only;
- A2 market + cross-market/fundamentals/news;
- A3 A2 + status-preserving pinned repository research.

Each AI forecast must record:

- p_up;
- forecast_return_bps;
- top_drivers;
- counterevidence;
- invalidation_conditions;
- source_refs;
- information_cutoff;
- issued_at;
- forecast_system_version;
- model identifier when observable;
- canonical hash where feasible.

## Fail-closed rules

- The forecast must not use information first available after 09:00:00 JST.
- The forecast must not be rewritten after issuance.
- Exact XM `JP225Cash` absence must be recorded; no other provider may be represented as the formal XM source.
- If public/non-XM data are used to exercise the exploratory workflow, they must be explicitly labeled exploratory context.
- The 15:30 result must not influence the forecast.
- This event can never later be promoted into the frozen 60-event v0.1 cohort.

## Outcome/review contract

After 15:30:

- retrieve exact XM start/end quotes only if the qualified route is actually available;
- otherwise mark `MARKET_OUTCOME_UNAVAILABLE`;
- preserve the forecast regardless of invalidation;
- keep factual score/error separate from interpretation;
- record bounded error attribution;
- do not modify the v0.1 candidate from this one event.

## Trading boundary

No broker order, position sizing, paper order, or live-capital action is authorized by this dry run.
