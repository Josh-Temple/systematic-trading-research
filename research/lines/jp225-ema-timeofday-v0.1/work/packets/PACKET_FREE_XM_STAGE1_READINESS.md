# Work Packet — Free-Source XM Stage 1 Readiness

Role: **Exact XM Source Acquisition / Qualification Worker**

Research line:

research/lines/jp225-ema-timeofday-v0.1/

Source policy:

**NO SEPARATE PAID MARKET-DATA SERVICE**

## Purpose

Bring the existing exact-XM research line from WAITING_FOR_XM_STAGE1_DATA to the strongest source-qualification state permitted by a local XM MT5 session, without calculating strategy outcomes and without accessing 2026 data.

This packet does not authorize a substitute broker or instrument.

## Required fresh reads

Before execution, fresh-read current GitHub main and at minimum:

- CURRENT.md
- RESEARCH_LINE.md
- frozen specification and integration/SPEC_FREEZE.json
- work/source-qualification/STAGE1_WINDOWS_RUNBOOK.md
- work/source-qualification/STAGE2_PLAN.md
- collect_mt5_jp225_stage1.py
- validate_stage1.py
- stage1_contract.py
- this packet
- work/source-research/FREE_SOURCE_ROUTE_DECISION_2026-10-05.md

Do not use past chat SHA/status as current truth.

## Hard boundaries

Do not:

- access 2026 market data;
- calculate EMA signals;
- calculate forward returns;
- calculate direction counts;
- calculate correlation/regression;
- calculate P/L;
- alter EMA5/EMA200;
- search new windows or filters;
- substitute another JP225-like symbol if JP225Cash is absent;
- use Dukascopy JPN.IDX/JPY as a JP225 substitute;
- purchase DataCube or any other historical-data service.

## Local execution

Use Windows with the intended XM MT5 terminal installed and logged in.

Run the existing Stage 1 collector and validator exactly as defined by the current runbook.

Treat all raw Stage 1 market files as local research inputs.

Preferred communication back to cloud/GitHub:

- validation receipt;
- SHA-256 identities;
- non-sensitive terminal/server/symbol metadata;
- row/coverage counts;
- failure codes;
- source-review receipt.

Do not paste or manually summarize market price values into chat.

If an independent source review genuinely requires raw bytes, stop and explicitly document why before transferring them.

## Expected Stage 1 result

PARTIAL_WITH_GAPS is acceptable and expected until timestamp/BID/source semantics and coverage are independently reviewed.

A collector failure is a source result, not a trading result.

If exact JP225Cash is unavailable or history is insufficient:

- preserve the failure;
- do not substitute another symbol;
- do not shift dates;
- classify the source gap explicitly.

## Advancement boundary

Stage 1 PASS alone does not authorize 2025 outcome calculation.

Required sequence remains:

1. Stage 1 source qualification PASS;
2. frozen signal-only 2025 event manifest;
3. manifest hash pinned before event-adjacent tick acquisition;
4. minimal Stage 2 BID/ASK tick collection;
5. Packet A execution qualification PASS;
6. pinned independent 2025 Discovery gate;
7. one-shot Discovery.

2026 remains locked throughout this packet.

## Completion output

Report:

- exact GitHub ref used;
- XM server identity at non-sensitive granularity;
- exact symbol result;
- M1/tick coverage status;
- Stage 1 validator classification;
- remaining gaps;
- hashes of safe receipts/artifacts;
- confirmation that no strategy outcomes or 2026 data were accessed.

Do not claim a market edge.
