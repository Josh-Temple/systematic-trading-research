# XM EURJPY source probe — Windows runbook

Status: PRE-FREEZE / SOURCE QUALIFICATION ONLY

This collector does not place an order and does not calculate a return, signal, P/L, win rate, or strategy result.

## Environment

Use Windows with the intended XM MT5 terminal already installed and logged in.

Do not provide ChatGPT with:

- password;
- account number;
- local credential files;
- account balance/equity;
- personal identity data.

## Run

Place `collect_mt5_eurjpy_source_probe.py` in an empty local folder.

PowerShell:

```powershell
py -m pip install MetaTrader5
py collect_mt5_eurjpy_source_probe.py
```

Default output directory:

`fxns_eurjpy_mt5_source_probe`

The script accepts only the exact candidate symbol `EURJPY`. If that symbol is unavailable, it fails and reports only the names of EURJPY-like symbols. Do **not** edit the script to substitute one automatically. A suffix or alternate symbol name requires a pre-freeze source-identity decision.

## Fixed probe scope

Three 2-minute windows around 08:15 JST are fixed only for source/timestamp qualification:

- 2026-01-15 08:14–08:16 JST
- 2026-07-15 08:14–08:16 JST
- 2026-10-06 08:14–08:16 JST

These windows are not used to choose a trading rule or estimate profitability.

## Outputs

Keep locally and unchanged:

- `tick_probes_raw.csv`
- `metadata.json`
- `sha256_manifest.json`

The collector preserves only allowlisted terminal/server/symbol metadata. It does not store account number, name, balance, equity, password, or local paths.

## Review boundary

A successful collection is **not** SOURCE PASS by itself.

Independent review must confirm:

- exact symbol identity;
- server identity;
- raw `time` / `time_msc` semantics versus UTC/JST/terminal display;
- BID/ASK validity;
- 08:15 quote-selection feasibility;
- swap metadata interpretation;
- commission/other fee status.

Commission is explicitly left `UNVERIFIED_NOT_INFERRED_FROM_ACCOUNT_HISTORY`; do not inspect trade history merely to infer it.

Raw probe prices should remain source-qualification material. Do not use them to tune the signal, cutoff, pair, or holding period.
