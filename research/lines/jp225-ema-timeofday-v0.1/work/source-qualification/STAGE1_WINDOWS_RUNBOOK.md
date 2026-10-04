# XM JP225 Stage 1 — Windows runbook v0.2

Use Windows with the intended XM MT5 terminal already installed and logged in. No password or account number is requested by these scripts.

Download **the complete source-qualification directory from the pre-XM hardening branch**, not the old PR #45 script alone. At minimum, keep `collect_mt5_jp225_stage1.py`, `stage1_contract.py` and `validate_stage1.py` together.

In PowerShell in that directory:

```powershell
py -m pip install MetaTrader5
py collect_mt5_jp225_stage1.py
py validate_stage1.py jp225_mt5_stage1 --out stage1_validation.json
```

The collector accepts only `JP225Cash`; it does not substitute similar symbols. It reads warm-up + 2025 M1 and four small fixed 2025 tick probes. No EMA, signals, returns, account equity, credentials, or 2026 history are collected. Stage 1 performs no trading.

The four raw files in `jp225_mt5_stage1` must remain unchanged:

- `metadata.json`
- `m1_warmup_2025_raw.csv`
- `tick_probes_raw.csv`
- `sha256_manifest.json`

A **PARTIAL_WITH_GAPS** result is expected before independent time/BID/coverage review. It is not a trading failure. Do not mark the metadata PASS yourself or edit its timestamps. Zip the raw folder and provide the ZIP to the research session. `stage1_validation.json` may be included beside it.

If collector/validator says **FAIL**, retain the partial directory locally and report the failure code. Do not rerun into the same directory, delete unexpected rows, paste quote values, or upload unreviewed failed market files. Boundary violations must be reviewed first. The validator prints no detailed price data and no holdout counts.

After raw integrity review, the research session may ask for a minimal redacted chart-time/source identity check at the fixed 2025 probes. Exclude account numbers, names and local paths. An unresolved timezone, M1 price identity or truncated history keeps source qualification partial.

Stage 1 alone cannot authorize Packet C. Next comes a separately frozen signal-only event manifest, local event-adjacent Stage 2 tick collection, Packet A execution qualification, and a pinned independent Discovery gate. See `STAGE2_PLAN.md`. 2026 stays locked.
