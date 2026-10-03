---
id: PKT-JP225-EMA-B
type: WorkInstruction
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-03
status: PRE_OUTCOME_PACKET
---

# Packet B — Outcome-blind deterministic implementation

Implement the frozen specification without reading actual JP225 history.

Required: EMA recursion, EMA cross, price/EMA200 comparator, timezone flags, BID/ASK mapping, +5/+15/+30 horizons, unavailable-quote states, overlap diagnostics, day-cluster bootstrap seed 2255200, discovery gate, holdout gate.

Synthetic tests must cover EMA recursion; equality boundary; long/short cross; no fabricated missing bars; Tokyo window boundaries; U.S. DST conversion; long ASK/BID execution; short BID/ASK execution; missing entry/target quotes; exact/first-after-target quotes; deterministic bootstrap; advancement tie-break; holdout locked without advancement.

No actual JP225, proxy-index, XM historical, or holdout data may be loaded. Implementation success is computational evidence only.
