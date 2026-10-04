---
id: HYP-JP225-USLEAD-001
type: Hypothesis
created_at: 2026-10-04
status: ACTIVE_PROXY_DISCOVERY
---

# HYP-JP225-USLEAD-001

## Hypothesis

The sign of the previous completed U.S. regular-session S&P 500 return predicts a short-term **opposite-direction** move in the first 30 minutes of the next eligible Japanese day session.

Operational proxy rule:

- previous U.S. regular-session return > 0 -> SHORT JP225 from 09:00 to 09:30 JST;
- previous U.S. regular-session return < 0 -> LONG JP225 from 09:00 to 09:30 JST;
- return = 0 -> no event.

## Motivation

Iwanaga (2026), using one-minute Nikkei 225 futures and S&P 500 data from 2001–2024, reports a negative relationship between the previous day's S&P 500 return and the first 30-minute Nikkei 225 futures return, alongside a positive relation near the close.

This research line tests only the opening-reversal sign rule in a separate public midpoint proxy dataset.

It does not assume the result transfers to XM JP225Cash.
