---
id: PKT-JP225-EMA-C
type: WorkInstruction
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-03
status: OUTCOME_PACKET_CONDITIONAL
---

# Packet C — 2025 discovery execution

## Preconditions

Packet A signal+execution source PASS; Packet B tests PASS; exact code SHA and raw source hashes recorded; specification unchanged.

## Allowed outcome access

Only 2025-01-01 through 2025-12-31.

2026 holdout may not be summarized, plotted, signaled, counted, or scored.

## Required outputs

EMA5/EMA200 and price/EMA200 comparator; +15m primary; +5/+30 descriptive; ALL/TOKYO_OPEN_30/TOKYO_CLOSE_30; descriptive night/US-open flags; side breakdown; overlap; spread distribution; unavailable-quote counts.

Apply the frozen advancement rule exactly.

Write exactly one terminal discovery decision: `NO_ADVANCEMENT` or `ADVANCE_TO_HOLDOUT: <one exact candidate>`.
