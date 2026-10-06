# XM EURJPY collector preparation result — 2026-10-07

Status: COLLECTOR_READY_NOT_RUN
Scientific status: NOT_APPLICABLE
Market outcome access: NONE

Prepared an outcome-blind Windows/MT5 source probe by adapting the established JP225 source-qualification pattern.

Properties:

- exact candidate symbol `EURJPY` only;
- no automatic symbol substitution;
- three fixed 2-minute seasonal tick probes;
- Bid/Ask schema validation;
- non-sensitive metadata allowlist;
- raw file + SHA-256 manifest;
- no signal, return, P/L, or order logic;
- commission left explicitly unverified;
- swap fields preserved but not interpreted as net economic cost.

Local syntax validation:

- Python `py_compile`: PASS
- collector SHA-256: `5745c2dc75061b3b7249b5fdbced20c52ad6eecabd6d61799ee9f68a0a621c03`

The collector was **not run against MT5** in the Chat environment. Exact XM source qualification therefore remains incomplete.
