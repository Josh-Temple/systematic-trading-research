---
type: CurrentProjection
research_line_id: RL-JP225-EMA-001
projection_generated_at: 2026-10-04
derived_from_decisions:
  - DEC-JP225-EMA-001
  - DEC-JP225-PROXY-20261004
  - work/integration/INDEPENDENT_AUDIT.md
---

# Current State

Operational state: **WAITING_FOR_XM_STAGE1_DATA**.

## Exact XM research

- HYP-JP225-EMA-001: **UNTESTED**; XM outcomes accessed: **NO**.
- Original specification bytes fixed by [SPEC_FREEZE.json](work/integration/SPEC_FREEZE.json); its historical draft header is retained.
- Packet A source: **PARTIAL_WITH_GAPS**. Exact server/time/BID M1/coverage unverified.
- Packet B + collector/validators/Stage 2/one-shot runner: **SYNTHETIC_TESTS_PASS**. No claim of market edge.
- Packet C 2025 Discovery: **LOCKED / NOT_EXECUTED** until exact signal+execution source and pinned independent gate PASS.
- XM 2026-01-01 through 2026-09-30: **UNTOUCHED / LOCKED**. No loader invocation or outcome/count/plot.

Core unchanged: exact XM MT5 JP225Cash, M1 EMA5/200, 2025 discovery, +15m BID/ASK primary, ALL / 08:45–09:15 / 15:15–15:45 JST selectable only. +5/+30, night/US open and price/EMA200 remain descriptive/comparator. No rescue search.

## Proxy evidence — separate and consumed

OANDA-derived midpoint candles are not XM execution data. 2020 partial-year close-window observation was selected post hoc. Frozen 2019 single-candidate replication failed (99 valid/65 dates, mean +0.9303 gross points); 2018 ALL slope test failed (4958/305, mean +0.2374). One-bar EMA200 slope is structurally redundant.

Original negative files and source receipts remain unchanged. Independent raw replay reproduced counts/daily sums and classification; original exact bootstrap RNG provenance remains incomplete. See [independent audit](work/integration/INDEPENDENT_AUDIT.md) and [procedural deviation](work/integration/PROCEDURAL_DEVIATION.md). Overall audit **PARTIAL_WITH_GAPS**, not blanket scientific PASS. Do not optimize consumed proxy samples or promote them to XM results.

## Next action

Run the revised [Stage 1 Windows runbook](work/source-qualification/STAGE1_WINDOWS_RUNBOOK.md) and provide the immutable raw ZIP. Use this integration branch's complete scripts, not old PR #45. Stage 1 source review -> frozen signal-only manifest -> event-adjacent Stage 2 ticks -> Packet A execution PASS -> pinned independent Discovery gate -> one-shot 2025 result. See [Stage 2 plan](work/source-qualification/STAGE2_PLAN.md).

All JP225 PRs remain draft pending complete review. Main has not yet adopted this projection. No broker substitute, credentials, live orders or holdout acquisition is authorized.
