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
py -m pip install MetaTrader5 tzdata
py collect_mt5_eurjpy_source_probe.py
```

Default output directory:

`fxns_eurjpy_mt5_source_probe`

The script accepts only the exact candidate symbol `EURJPY`. If that symbol is unavailable, it fails and reports only the names of EURJPY-like symbols. Do **not** edit the script to substitute one automatically. A suffix or alternate symbol name requires a pre-freeze source-identity decision.

## Fixed probe scope

Six fixed 2-minute windows around 08:15 JST are fixed only for source/timestamp qualification:

- 2026-01-15 08:14–08:16 JST
- 2026-07-15 08:14–08:16 JST
- 2026-10-06 08:14–08:16 JST
- 2026-01-16 08:14–08:16 JST — Friday exit source probe
- 2026-07-17 08:14–08:16 JST — Friday exit source probe
- 2026-10-02 08:14–08:16 JST — Friday exit source probe

Collector version: `FXNS_EURJPY_SOURCE_PROBE_v0.2`.
Friday purpose: `FRIDAY_EXIT_FEASIBILITY`; other probes: `SOURCE_TIME_SCHEMA`.
Selected only by calendar: winter, summer and recent complete period, all before
2026-10-07. January 16 directly follows existing January 15 Thursday. No prices,
spreads or results informed selection. These dates must not change after outputs.
`tzdata` supplies Asia/Tokyo timezone data on Windows. Request datetimes are UTC-aware;
raw returned time/time_msc are preserved without declaring their meaning verified.

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


## Thursday → Friday amendment boundary

Friday is exit-only at 08:15 JST; Thursday exits Friday, never rolls to Monday.
v0.2 now includes the three preselected Friday probes. They are source qualification
only, never strategy evaluation. Independent review must verify valid Bid/Ask at or
after 08:15 through 08:16 inclusive, time mapping versus terminal display, server
identity and costs. Missing quotes never extend exit to Monday. Empty windows are
preserved as zero rows, not proof of feasibility; API/schema/invalid-quote failures
stop collection. A partial failed directory is not a successful collection.
Status remains LOCAL_XM_EXECUTION_REQUIRED.


## Preservation and review handoff

Keep all three files unchanged; never edit raw CSV or metadata. ZIP the entire output
folder for independent source review if needed. Do not include credential files,
account screenshots, account number, balance/equity or personal information. The
collector calls account_info only to project the allowlisted server field; the SDK
returns an account object, but the collector does not access, serialize or calculate
its financial/identity fields. There is no trade-history access.

Do not rerun into the same folder: it fails rather than overwrite evidence. Preserve
failed folders separately; do not choose dates or retained attempts using quote
quality. Successful collection is not SOURCE PASS. Swap metadata is preserved only;
commission remains UNVERIFIED_NOT_INFERRED_FROM_ACCOUNT_HISTORY and other costs
UNVERIFIED_NOT_CALCULATED. Source review must qualify account-specific costs separately.
If EURJPY is unavailable, EXACT_SYMBOL_IDENTITY_REQUIRES_PRE_FREEZE_DECISION stops;
EURJPY-like names may be displayed, but no suffix is automatically adopted.
