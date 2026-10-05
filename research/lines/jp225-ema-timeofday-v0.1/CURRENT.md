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

## No-PC continuation update — 2026-10-04

While Windows/XM Stage 1 is unavailable, one separate pre-registered proxy candidate was tested on previously unused 2017 OANDA-derived JP225 midpoint M1 data: EMA5/EMA200 cross followed by five complete M1 bars of persistent EMA ordering before entry.

Result: **PERSIST5_PROXY_NOT_SUPPORTED_2017**. Valid n=1,204 across 253 Asia/Tokyo dates; mean +15m gross points=-0.287292; day-cluster 95% interval=[-1.671920,+1.127615]. The same-year unfiltered comparator mean was -0.144020. Per the frozen stop rule, 2016 was not accessed and no persistence-length/time-window rescue is allowed.

## Source research update — 2026-10-04

A bounded official-source review identified JPX/OSE J-Quants DataCube historical derivatives one-minute OHLC and transaction-tick data as a materially better **futures proxy/source candidate** than the consumed OANDA midpoint data. It is **not** an XM replacement: the tick product is executed-price history rather than XM BID/ASK, one-minute data is trade-based, and futures contract/roll semantics differ. Do not use this source to unlock Packet C or the 2026 XM holdout. See [JPX OSE source-route review](work/source-research/JPX_OSE_SOURCE_ROUTE_2026-10-04.md).

## Next action

Exact XM work remains waiting for a future Windows opportunity. When available, run the revised [Stage 1 Windows runbook](work/source-qualification/STAGE1_WINDOWS_RUNBOOK.md) and provide the immutable raw ZIP. Until then, do not relax the XM source gate or promote proxy results to XM conclusions. Stage 1 source review -> frozen signal-only manifest -> event-adjacent Stage 2 ticks -> Packet A execution PASS -> pinned independent Discovery gate -> one-shot 2025 result. See [Stage 2 plan](work/source-qualification/STAGE2_PLAN.md).

Repository integration state: PR #54 (pre-XM hardening) and PR #55 (2017 persistence negative result) are merged on `main`; the separate US-lead negative line is also on `main` via PR #56. These merges do not change the scientific gate: exact XM source qualification remains incomplete, Packet C is locked, and the 2026 holdout remains untouched. No broker substitute, credentials, live orders or holdout acquisition is authorized.


## Free-source policy update — 2026-10-05

Research-owner policy: **do not use a separate paid market-data service for now**.

Source routing is now:

- exact XM MT5 JP225Cash: **PRIMARY / FREE-SOURCE PRIORITY**;
- Dukascopy JPN.IDX/JPY: **REJECTED_AS_JP225_PROXY** because Dukascopy documents it as Japan 200+ Index, not Nikkei 225;
- JPX/J-Quants DataCube: **DEFERRED_NO_PAID_DATA**;
- consumed OANDA midpoint data: **NO_FURTHER_RESCUE_MINING**.

This does not change the frozen EMA specification or scientific status. Exact XM remains UNTESTED and WAITING_FOR_XM_STAGE1_DATA.

See:

- work/source-research/FREE_SOURCE_ROUTE_DECISION_2026-10-05.md
- work/source-research/DUKASCOPY_JPN_IDX_SOURCE_QUALIFICATION_2026-10-05.md
- work/packets/PACKET_FREE_XM_STAGE1_READINESS.md
