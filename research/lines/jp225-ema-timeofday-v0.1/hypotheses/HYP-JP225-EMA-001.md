---
id: HYP-JP225-EMA-001
type: Hypothesis
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-03
status: UNTESTED
---

# EMA crossover continuation with time-of-day concentration

## Primary hypothesis

After an M1 EMA(5)/EMA(200) crossover on XM `JP225Cash`, the quote-executable signed return 15 minutes after the signal is positive on average.

## Time-of-day hypothesis

Any usable effect may be concentrated around market-structure transitions rather than uniform through the day.

The only windows eligible for discovery selection in v0.1 are:

- **ALL**
- **TOKYO_OPEN_30**: signal close time >= 08:45 and < 09:15 Asia/Tokyo
- **TOKYO_CLOSE_30**: signal close time >= 15:15 and < 15:45 Asia/Tokyo

These are fixed before outcome inspection because current JPX Nikkei 225 futures hours place the day-session open at 08:45 and close at 15:45, and published one-minute Nikkei 225 futures research reports materially different first- and last-30-minute behavior.

## Descriptive-only time flags

- OSE_NIGHT_OPEN_30: 17:00–17:30 Asia/Tokyo
- US_CASH_OPEN_60: 09:30–10:30 America/New_York, using IANA timezone rules
- OTHER

They cannot be promoted to the v0.1 discovery winner.

## Comparator

EMA(5) may add no incremental value over a simpler close-price crossing of EMA(200). A price/EMA200 crossover is therefore measured under the same horizons and quote rules.

## Falsification boundary

The practical idea is not supported if the source/execution semantics cannot be qualified, no discovery candidate meets the advancement rule, or the selected candidate fails untouched holdout. Source failure is operational evidence, not a negative market result.
