---
type: CurrentProjection
research_line_id: RL-JP225-EMA-001
projection_generated_at: 2026-10-03
derived_from_decisions:
  - DEC-JP225-EMA-001
derived_from_interpretations: []
---

# Current State

## Scientific status

- HYP-JP225-EMA-001: **UNTESTED**
- Market outcomes accessed by this line: **NO**
- Current phase: **PRE_OUTCOME / SOURCE QUALIFICATION + OUTCOME-BLIND IMPLEMENTATION**

## Frozen core

Primary signal: M1 EMA(5) crossing EMA(200).

Primary outcome: signed executable +15-minute return in JP225 index points using observed BID/ASK quotes.

Primary candidate windows for discovery selection:

1. ALL eligible times
2. TOKYO_OPEN_30: 08:45–09:15 JST
3. TOKYO_CLOSE_30: 15:15–15:45 JST

Other predeclared windows are descriptive diagnostics only.

## Data state

Preferred source: XM MT5 `JP225Cash`.

Required: BID-based M1 bars or equivalent raw BID ticks, BID/ASK ticks for executable entry/exit, explicit instrument/server/timezone metadata, and warm-up + discovery coverage.

Current result: **NOT YET QUALIFIED**.

Dukascopy `JPN.IDX/JPY` is not an authorized exact substitute because its official product description is "Japan 200+ Index".

## Gate

Do not inspect 2026 holdout outcomes unless the 2025 discovery stage selects exactly one predeclared candidate under the frozen advancement rule.

## Next actions

1. Packet A — XM source qualification.
2. Packet B — deterministic implementation and synthetic tests.
3. Packet C — 2025 discovery execution only after A and B pass.
4. Packet D — 2026 holdout only if Packet C advances one exact window.
