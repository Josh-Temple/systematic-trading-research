# H3 outcome-blind M1 structural check — 2026-09-28

This follows [H3 source preparation](H3_SOURCE_PREPARATION_2026-09-28.md). It is a structural check on already acquired BID M1 responses, not an H3 sample freeze, Run, Result, or full source-gate PASS.

## Basis and result

The [H1 frozen `sample_freeze.json`](https://drive.google.com/file/d/1k69iHCQwQ2GMQahPFYHTY1bQKrdz4daR/view) records 1,380 expected M1 minutes on summer Monday–Thursday, 1,260 on summer Friday, and excludes 2026-05-25 (a summer Monday with 1,229 bars) for exactly 151 missing expected minutes. The H1 evaluation freeze calls for the same accepted trading-hours convention, but the frozen JSON does not enumerate each expected minute. The minute set here is explicitly **reconstructed** from those counts and the observed continuous source intervals: Monday–Thursday 00:00–20:59 and 22:00–23:59 UTC; Friday 00:00–20:59 UTC. Exact schedule provenance remains open for the formal gate.

`classify_m1_structure.py` read each unchanged response from the [persisted M1 source archive](https://drive.google.com/file/d/1h2Vhik3yz-UR05l-F_a0RQMYNkEKP71X/view), checked its size and SHA-256 against the original inventory, decoded M1 using the byte-identified legacy decoder, and compared the complete minute set and OHLC basic validity. Its scope is only 2026-07-10 through 2026-09-25 UTC.

| Field | Value |
|---|---|
| Calendar weekday candidates | 56 |
| Pass under reconstructed summer minute set | 55 |
| Excluded under that set | 2026-09-07: 1,229 rows; expected 1,380; missing 151; extra 0; duplicate 0 |
| Other 55 dates | Exact expected minutes, no extras or duplicates, basic OHLC PASS |
| Classification status | RECONSTRUCTED_SCHEDULE_PENDING_PROVENANCE |
| H3 frozen selected sessions | 0; fewer than 60 eligible dates have elapsed |
| Tick and fixed H2 prefix source gate | NOT_EVALUATED |
| Outcome and group comparison | NOT_COMPUTED |
| Current state | WAITING_FOR_MATURITY |

The 2026-09-07 missing interval includes 18:29–20:59 UTC, matching 151 required minutes under this reconstruction. The calendar continues chronologically after that exclusion; no date is substituted by discretion. The [machine-readable per-day check](https://drive.google.com/file/d/1aknkzRaRP2k6giF_mHa7khHya_o7VkG2/view) is saved separately with the source inventory SHA-256 and each raw SHA-256; its downloaded readback SHA-256 is `c7eeee3fec92f93854e5263c62c99291ef4f1b6c424d02d297bb3b11db2e5a40`. Do not use this 55-date count as a formal source-gate PASS or inspect H3 outcomes before the first 60 structurally eligible sessions and the full source gate are fixed.

Next: establish an explicit authoritative minute-set reference for the accepted convention, acquire subsequent fully elapsed UTC candidates, then verify the 135-file H2 prefix and complete Tick source gate before any H3 outcome access. `DATA-HR-003` remains `FINAL_HOLDOUT / UNUSED`.
