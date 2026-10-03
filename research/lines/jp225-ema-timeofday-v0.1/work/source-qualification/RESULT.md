---
id: RESULT-JP225-EMA-A-PRECHECK-20261003
type: WorkResult
packet_id: PKT-JP225-EMA-A
research_line_id: RL-JP225-EMA-001
status: PARTIAL_WITH_GAPS
scientific_status: NOT_APPLICABLE
market_outcome_access: false
---

# Packet A — Source qualification precheck

## Status

**PARTIAL_WITH_GAPS**

The public/documentation layer is sufficient to define a bounded acquisition path, but the exact XM MT5 account/server history has not been accessed in this session. Therefore source qualification is not PASS.

No EMA event, forward return, spread-conditioned result, discovery result, or holdout result was calculated.

## Established before account-specific access

### XM product surface

Current broker-facing XMTrading material identifies:

- cash symbol: `JP225Cash`;
- MT5 availability;
- variable spread;
- a broad weekday trading/quote schedule;
- server clock convention described as GMT+2 in standard time and GMT+3 in daylight-saving time.

These public materials are supporting evidence only. The connected MT5 terminal remains authoritative for the exact account/server instrument.

### MetaTrader history capability

Official MQL5 documentation provides:

- `copy_rates_range` / `CopyRates` for historical bars;
- `copy_ticks_range` / `CopyTicksRange` for BID/ASK tick history;
- symbol properties including tick size and contract size.

### Timestamp conflict preserved

MetaTrader5 Python documentation currently states that tick/bar history is stored and returned in UTC. A recent MQL5 forum moderation response states that returned data are broker-server time and reports the UTC wording as a documentation problem.

Because these statements conflict, v0.1 does not resolve timestamp identity by assumption.

The acquisition tool therefore preserves raw integer timestamps and terminal/server metadata. Qualification requires a readback check against the actual XM terminal/server convention before any time-of-day outcome is computed.

## Still required for PASS

1. Exact connected account server name.
2. Exact symbol returned by the terminal.
3. Terminal/package version.
4. Symbol digits, point, tick size, contract size, volume minimum/step.
5. Actual M1 coverage covering warm-up and calendar 2025.
6. Actual BID/ASK tick coverage sufficient for executable entry/exit mapping.
7. Raw timestamp-domain resolution for that server/history.
8. M1 bar identity check versus chart or independently reconstructed BID bars.
9. Missing/duplicate/out-of-order diagnostics.
10. SHA-256 of raw files and metadata.

## Prepared acquisition path

`collect_mt5_jp225.py` is an outcome-blind raw collector. It requires an already installed and logged-in local MT5 terminal and never accepts or stores account credentials.

It writes:

- terminal/account/symbol metadata;
- raw M1 history;
- raw BID/ASK tick history;
- SHA-256 manifest.

It does not calculate EMA, signals, events, forward returns, P/L, or performance summaries.

## Gate

Packet C remains locked.

Source state is not a negative trading result.
