# XM JP225 Stage 1 — Windows runbook

This is the lightest path to unblock the exact XM research.

## What it collects

- `JP225Cash` M1 from 2024-11-29 through the end of 2025;
- four fixed small BID/ASK tick probe windows in 2025;
- terminal/server/symbol metadata needed for source qualification;
- SHA-256 identities.

It does **not** collect the 2026 holdout and does not calculate signals or performance.

## Before running

Use a Windows PC with:

1. XM MetaTrader 5 installed;
2. the intended XM account already logged in;
3. `JP225Cash` visible in Market Watch if available.

No account password or API key is placed in the script.

## Commands

Open PowerShell or Command Prompt in the directory containing the script.

```powershell
py -m pip install MetaTrader5
py collect_mt5_jp225_stage1.py
```

If `py` is unavailable, use `python` instead.

Expected output directory:

`jp225_mt5_stage1`

Expected files:

- `m1_warmup_2025_raw.csv`
- `tick_probes_raw.csv`
- `metadata.json`
- `sha256_manifest.json`

## After the run

Zip the `jp225_mt5_stage1` folder and provide that ZIP to the research session.

Do not edit the CSV or JSON files before zipping them.

## What happens next

The research side will:

1. verify file hashes and source metadata;
2. determine actual available M1/tick coverage;
3. resolve timestamp semantics conservatively;
4. run the already-tested EMA calculation on 2025 only if source qualification passes;
5. create an event-time manifest;
6. request only the BID/ASK tick windows needed around those 2025 events.

This staged path avoids downloading a full year of unnecessary tick history.

The 2026 holdout stays untouched unless the frozen 2025 discovery gate advances exactly one candidate.
