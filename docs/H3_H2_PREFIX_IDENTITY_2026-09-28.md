# H3 fixed H2 generator prefix — source identity check, 2026-09-28

This outcome-blind check follows [DEC-HR-004](../research/lines/horizontal-reaction-v0.1/decisions/DEC-HR-004.md) and the [H3 implementation audit](../research/lines/horizontal-reaction-v0.1/H3_IMPLEMENTATION_IDENTITY_AUDIT_2026-09-28.md). It does not run the generator or complete the H3 source gate.

The frozen [H2 135-file generator-input CSV](https://drive.google.com/file/d/1Zu0xNyLfSABItcAgZqKtxmaAi-nzEWvR/view) was read back with SHA-256 `1232af3b557a9559ca22f03e7c21ff748d467794cdaec5b32ddd9c0b437fcec3`, matching the package's `SHA256SUMS_20260923.txt`. It lists 75 pre-touch context files and 60 selected H2 sessions in date order, 2025-12-31 through 2026-07-09.

`verify_h2_prefix.py` requested each listed Dukascopy first-party BID M1 route and stored the exact response once. All 135 raw byte sizes and SHA-256 values match the frozen per-file identities. The [source identity archive](https://drive.google.com/file/d/19R8whOpps1W8YwTafDI6OuDzZeDOrqKN/view) contains the 135 responses, frozen CSV and verification manifest. After upload, its downloaded ZIP had SHA-256 `1a4f1b7449230c374b4ade3df1f93e574712faae6ae87577127f08e59d84ffe2`; ZIP integrity and all 135 member hashes passed readback.

| Field | Value |
|---|---|
| Fixed-prefix raw identity | PASS_135_EXACT_RAW_MATCH |
| Context / selected H2 files | 75 / 60 |
| First / last date | 2025-12-31 / 2026-07-09 UTC |
| H3 post-prefix append | Not run; acquired later M1 files remain separate |
| Generator events / Gamma / outcomes | Not computed |
| H3 selected sample / full source gate | Not frozen / NOT_EVALUATED |
| Current state | WAITING_FOR_MATURITY |

For H3, preserve this exact ordered prefix and append later valid first-party BID M1 files chronologically before filtering selected sessions. Do not reset expanding Gamma at 2026-07-10. The source bytes match; no H3 generator output or temporal-leakage resolution is implied. The [summer M1 structural check](H3_M1_STRUCTURE_2026-09-28.md) is separately limited to the 56 later weekday candidates. `DATA-HR-003` remains `FINAL_HOLDOUT / UNUSED`.
