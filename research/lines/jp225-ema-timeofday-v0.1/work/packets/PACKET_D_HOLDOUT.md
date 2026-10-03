---
id: PKT-JP225-EMA-D
type: WorkInstruction
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-03
status: HOLDOUT_PACKET_LOCKED
---

# Packet D — 2026 untouched holdout

Requires a durable Packet C decision naming exactly one advanced candidate. NO_ADVANCEMENT keeps this packet locked.

Allowed outcome: only selected candidate, primary +15m EMA5/EMA200, 2026-01-01 through 2026-09-30.

Decision states:

- `SUPPORTED_IN_HOLDOUT`
- `NOT_SUPPORTED_IN_HOLDOUT`
- `INSUFFICIENT_HOLDOUT_EVENTS`
- `SOURCE_OR_EXECUTION_BLOCKED`

Secondary horizons, alternate windows, EMA parameters, and rescue filters cannot change the primary verdict. A positive historical holdout does not authorize live trading; prospective/shadow validation requires a new decision.
