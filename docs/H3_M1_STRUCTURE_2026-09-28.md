# H3 outcome-blind M1 structural check — 2026-09-28

This follows [H3 source preparation](H3_SOURCE_PREPARATION_2026-09-28.md). It is a structural check on already acquired BID M1 responses, not an H3 sample freeze, Run, Result, or full source-gate PASS.

## Basis and result

The [H1 frozen `sample_freeze.json`](https://drive.google.com/file/d/1k69iHCQwQ2GMQahPFYHTY1bQKrdz4daR/view) records 1,380 expected M1 minutes on summer Monday–Thursday, 1,260 on summer Friday, and excludes 2026-05-25 (a summer Monday with 1,229 bars) for exactly 151 missing expected minutes. The earlier [Stage A sealed result](https://docs.google.com/document/d/1OAd1WPSBhf98wfG5IkEqb4nS11rV0MpfIsfTTFXrKr0/edit) explicitly records the accepted summer interpretation: Monday–Thursday 00:00–20:59 and 22:00–23:59 UTC; Friday 00:00–20:59 UTC. It cites the [Dukascopy XAU/USD trading-hours table](https://www.dukascopy.com/swiss/english/forex/forex-trading-accounts/link/), which shows the summer daily break at 21:00–22:00 GMT and Friday close at 21:00 GMT. The H1 structural records corroborate the same minute counts and the shortened-day exclusion.

`classify_m1_structure.py` read each unchanged response from the [persisted M1 source archive](https://drive.google.com/file/d/1h2Vhik3yz-UR05l-F_a0RQMYNkEKP71X/view), checked its size and SHA-256 against the original inventory, decoded M1 using the byte-identified legacy decoder, and compared the complete minute set and OHLC basic validity. Its scope is only 2026-07-10 through 2026-09-25 UTC.

| Field | Value |
|---|---|
| Calendar weekday candidates | 56 |
| Structurally eligible under documented summer minute set | 55 |
| Excluded | 2026-09-07: 1,229 rows; expected 1,380; missing 151; extra 0; duplicate 0 |
| Other 55 dates | Exact expected minutes, no extras or duplicates, basic OHLC PASS |
| Classification status | DOCUMENTED_SUMMER_MINUTE_SET_PASS |
| H3 frozen selected sessions | 0; fewer than 60 eligible dates have elapsed |
| Tick and fixed H2 prefix source gate | NOT_EVALUATED |
| Outcome and group comparison | NOT_COMPUTED |
| Current state | WAITING_FOR_MATURITY |

The 2026-09-07 missing interval includes 18:29–20:59 UTC, matching 151 required minutes. The calendar continues chronologically after that exclusion; no date is substituted by discretion. The original [per-day check v1](https://drive.google.com/file/d/1aknkzRaRP2k6giF_mHa7khHya_o7VkG2/view) marked provenance pending; the [v2 record](https://drive.google.com/file/d/1-kLYOuNMA4kzBtVtPYs69-vS9bFCqRSx/view) adds the explicit prior seal and provider references without changing any date classifications or raw hashes. Its downloaded readback SHA-256 is `7744c0a9af6c01374854c152131826869f92368e4185e83a50fb7a800af9e3d1`. Do not use this 55-date count as a full source-gate PASS or inspect H3 outcomes before the first 60 structurally eligible sessions and the full source gate are fixed.

Next: acquire subsequent fully elapsed UTC candidates, then complete the Tick source gate before any H3 outcome access. The [135-file H2 prefix raw identity](H3_H2_PREFIX_IDENTITY_2026-09-28.md) has been separately verified. `DATA-HR-003` remains `FINAL_HOLDOUT / UNUSED`.
