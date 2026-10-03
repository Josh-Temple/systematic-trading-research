# XM MT5 JP225Cash collection contract

## Purpose

Acquire the exact broker history required for source qualification without calculating trading outcomes.

## Environment

Run on a PC where the user's XM MetaTrader 5 terminal is already installed and logged in.

The collector does not contain account number, password, API token, or server credentials.

## Acquisition scope

Default raw acquisition uses a boundary-padded superset:

- requested start: 2024-11-29 00:00:00 in the API request time convention;
- requested end: 2026-10-02 00:00:00 in the API request time convention.

The scientific windows remain unchanged:

- warm-up: at least 1,000 valid M1 bars before the first 2025 event;
- discovery: 2025-01-01 through 2025-12-31 after timestamp semantics are resolved;
- holdout: 2026-01-01 through 2026-09-30.

Extra boundary bytes are acquisition context only and cannot be used to alter the scientific dates.

## Required files

- `metadata.json`
- `m1_raw.csv`
- `ticks_raw.csv`
- `sha256_manifest.json`

## Required metadata

- MetaTrader5 package/terminal version;
- account server only (no login/password);
- exact symbol;
- symbol description/path if available;
- digits/point/tick size/contract size;
- min/max/step volume;
- first/last available exported M1 timestamp;
- first/last available exported tick timestamp;
- raw row counts;
- collector version/commit.

## Timestamp rule

Preserve raw `time` and `time_msc` integers exactly.

Do not convert the research windows to Tokyo time or label returned history as UTC until the actual XM history convention is independently resolved.

Current documentation evidence is conflicting, so timestamp resolution is a source-qualification task, not an implementation default.

## Privacy

Do not commit the user's account number, name, email, credentials, or terminal data directory. Only the broker server string needed for provenance may be retained.

Raw broker history may be large. Do not commit it to Git by default; store it as an external artifact and commit only identity/hash metadata unless repository policy explicitly changes.
