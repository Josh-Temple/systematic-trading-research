---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261006
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-06T22:19:56+09:00
formal_score_status: UNAVAILABLE_EXACT_XM_MISSING
---

# JP225 2026-10-06 public-proxy review

## Boundary

This file is a diagnostic comparison against the official Nikkei 225 cash index. It is **not** the formal XM `JP225Cash` outcome and cannot enter the future scored cohort.

The formal review remains `MARKET_OUTCOME_UNAVAILABLE` because the qualified exact-XM 09:00/15:30 Bid/Ask route is not available.

## Public cash-index outcome

Official Nikkei 225:

- 09:00 open: 69,954.61
- close: 70,683.98
- high: 70,798.62 at 15:17
- low: 69,813.16 at 09:02
- close versus previous close: +737.12 / +1.05%
- 09:00→close log return: approximately **+103.72 bps**
- proxy binary outcome: **UP**

## Frozen forecasts versus public proxy

| System | P(up) | Return forecast | Proxy Brier | Proxy absolute error |
| --- | ---: | ---: | ---: | ---: |
| B0 | 0.50 | 0 bps | 0.2500 | 103.72 bps |
| A1 | 0.53 | +4 bps | 0.2209 | 99.72 bps |
| A2 | 0.58 | +13 bps | 0.1764 | 90.72 bps |
| A3 | 0.56 | +9 bps | 0.1936 | 94.72 bps |

These values are **nonformal diagnostics only**.

## Result / interpretation separation

### Result

- A1/A2/A3 all assigned greater-than-0.50 probability to the direction that occurred in the public proxy.
- A2 had the lowest proxy Brier among the three AI forecasts for this single event.
- All three return forecasts materially understated the public cash-index move.
- A3 was directionally correct in the public proxy but less favorable than A2 on both the single-event proxy Brier and absolute-return error.

### Interpretation

The positive pre-cutoff market context was directionally informative on this day, while the A3 repository layer did not add value relative to A2 in this one public-proxy observation. That is not evidence that A2 is generally superior to A3: one exploratory event, a late issuance, non-XM inputs, and a non-XM outcome proxy are insufficient for that conclusion.

The midday pullback was real, but the market resumed upward movement into the afternoon and reached the daily high at 15:17. Therefore the morning profit-taking risk described in the forecast was transient rather than session-dominant.

## Decision

- no specification change;
- no probability-rule change;
- no source-set change;
- no cohort admission;
- exact-XM readiness remains the blocking issue for formal scoring.

## Public source

Official Nikkei 225 daily summary:
https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261006&idx=nk225
