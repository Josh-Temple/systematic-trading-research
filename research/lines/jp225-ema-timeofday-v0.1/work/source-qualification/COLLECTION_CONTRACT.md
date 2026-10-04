# XM Stage 1 acquisition contract v0.2 — 2026-10-04 correction

This replaces the unsafe padded full-history acquisition contract; its earlier text/code remains in Git history at PR #45 head `48ede9665b91b308310fee47b97bcfa81c66cdae`. Scientific parameters and sample roles are unchanged.

- Exact symbol only: `JP225Cash`; no aliases or substitutions.
- `copy_rates_range`: request UTC-aware datetimes, 2024-11-29 00:00:00 to **2025-12-31 23:59:00 inclusive**. Official API documentation explicitly defines the end as inclusive. Do not request 2026-01-01.
- Four fixed 2025 tick probes in `stage1_contract.py`. They cover Tokyo opening/closing regions in winter, spring, summer and autumn for source verification, not performance ranking.
- Before saving any market row, inspect raw `time` (and tick `time_msc`). Any row outside the requested research acquisition domain, especially >=2026-01-01, fails. Do not silently drop it. Do not print its prices or a holdout count. A failed partial directory cannot be used for research.
- Raw CSV schemas must exactly match the MT5 M1/tick fields. No imputation, sorting or deduplication during collection.
- Metadata uses positive field allowlists: terminal build/maxbars; account server only; exact symbol/digits/point/tick size/contract size/volume min/step/chart mode. No login, name, password, balances, margin, currency, local paths or raw error messages.
- Old `collect_mt5_jp225.py` is disabled before MT5 import/connection. It no longer offers early holdout acquisition.
- New output directory only; never overwrite a prior collection.

## Outputs

`metadata.json`, `m1_warmup_2025_raw.csv`, `tick_probes_raw.csv`, `sha256_manifest.json`.

Keep these immutable. Source review is a **separate** `source_review.json`, bound to all three original file hashes and the exact server. It is not generated as PASS by the collector.

## Timestamp/source identity

Official MetaTrader Python docs state UTC request/return semantics. This is a documented request convention, not proof of the specific XM feed. The earlier report's forum conflict has not been independently reacquired as authoritative evidence in this audit. Do not assert that returned raw time is server-local or UTC from clock resemblance.

For qualification, record fixed 2025 winter/summer anchors linking raw API `time` / `time_msc`, terminal chart display time, independently known UTC/JST, server offset and DST evidence. Confirm M1 timestamp represents bar OPEN; signal close is +60s. Confirm chart mode BID and actual chart/BID-tick bar identity at the fixed probes. Use metadata/raw values solely for source qualification; no EMA or forward-return inspection.

Stage 1 validator supports only a review establishing **UTC_RAW_SECONDS** and **BID_M1_BAR_OPEN**. A feed requiring a server-local/DST decoder stays PARTIAL_WITH_GAPS until a separately reviewed outcome-blind decoder exists. No implicit offset correction is permitted. Raw-domain boundary checks alone do not establish calendar-domain identity.

Coverage evidence must address full calendar 2025, 1,000 warm-up bars before the first evaluated event, truncation by terminal Max. bars in chart, trading sessions/holidays, and missing-minute classification. Missing minutes are reported, never imputed or assumed all legitimate.

No order placement is present. This script uses the user's already logged-in terminal solely to read historical data. Do not provide credentials to ChatGPT or commit broker raw data by default.
