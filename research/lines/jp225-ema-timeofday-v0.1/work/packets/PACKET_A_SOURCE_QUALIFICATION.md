---
id: PKT-JP225-EMA-A
type: WorkInstruction
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-03
status: PRE_OUTCOME_PACKET
---

# Packet A — XM JP225Cash source qualification

## Objective

Determine whether exact XM MT5 `JP225Cash` history can support the frozen v0.1 test.

## Required fresh reads

Current main HEAD; docs/RESEARCH_PRINCIPLES.md; this line's README, CURRENT, decision, hypothesis, specification; current XM MT5 symbol specification available in the user environment.

## Forbidden

Do not calculate EMA crosses, event counts, forward returns, spread-conditioned outcomes, best periods, or 2025/2026 performance.

## Required checks

1. Exact symbol identity and account server.
2. MT5 terminal build and export method.
3. M1 coverage from warm-up through 2025.
4. Tick coverage for BID/ASK mapping.
5. Timestamp/server timezone and DST semantics.
6. Missing/duplicate/out-of-order timestamps.
7. Whether chart M1 is BID-based and whether exported bars match.
8. Digits/tick size/contract size where exposed.
9. Raw preservation and SHA-256.
10. Whether 2026 bytes can be preserved without outcome summaries if acquired early.

PASS only if signal and execution series can be interpreted without invented semantics.

Bars without BID/ASK ticks => `SIGNAL_ONLY_SOURCE`, insufficient for practical net-edge conclusion.

No provider substitution inside this packet.
