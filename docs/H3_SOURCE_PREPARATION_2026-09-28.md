# H3 outcome-blind source preparation — 2026-09-28

Operational result. This is not an H3 Run, Result, sample freeze, or source-gate PASS. GitHub main at the start of work: `373ba83b05ed925c025eb2b97aadefdd762cd80f`; inventory tools merged in PR #20 at `06b54cd2ed685676ef87d37be6591b7526af1c6a`.

## Status

| Field | Value |
|---|---|
| STATUS | PARTIAL_PRE_MATURITY_SOURCE_ACQUIRED |
| PREREGISTRATION_URL | https://docs.google.com/document/d/1GRa035N5FX3F59_wM2T11VFuv3aL85YZghmvaCeTJ0g/edit |
| SOURCE_PREPARATION_HANDOFF | https://docs.google.com/document/d/1QPwXqAcp1fzPm6VXelMLDMyist02-sSSDQ1lkrpsoSg/edit |
| CANDIDATE_SCAN_START | 2026-07-10 UTC |
| LATEST_CANDIDATE_DATE_CHECKED | 2026-09-25 UTC (last completed weekday at acquisition) |
| CALENDAR_CANDIDATE_COUNT | 56 weekdays |
| STRUCTURALLY_ELIGIBLE_COUNT | UNKNOWN; frozen official-hours gate not applied |
| FROZEN_SELECTED_COUNT | 0; no 60-session freeze |
| M1_SOURCE_COVERAGE | 56/56 first-party BID M1 daily responses, basic validation PASS |
| TICK_SOURCE_COVERAGE | 1,344/1,344 first-party BID/ASK Tick hourly responses; 82 empty buckets retained |
| HASH_READBACK_STATUS | PASS for 56 M1 + 1,344 Tick raw payloads from persisted Drive ZIPs; archive SHA-256 also matched |
| SOURCE_GATE | NOT_EVALUATED; structural minutes, H2 fixed-prefix continuity and full source gate remain open |
| OUTCOME_COMPUTED | NO |
| CONFIRMATION_OUTCOME_COMPARISON | NO |
| BOOTSTRAP_RUN | NO |
| PROTOCOL_CHANGED / PARAMETER_SEARCH / SAMPLE_RESELECTION | NO / NO / NO |
| CURRENT_STATE | WAITING_FOR_MATURITY |
| NEXT_ACTION | Resolve the accepted official trading-minute convention from frozen sources; apply it without touch/outcome access, continue candidate acquisition and freeze only the first 60 structurally eligible sessions, then complete the source gate. |

## Source identity and limits

- M1 route: `https://jetta.dukascopy.com/v1/candles/minute/XAU-USD/BID/{YYYY}/{M}/{D}`. Raw response bytes and per-day URL, local retrieval time, size, SHA-256, decoded row count, first/last UTC timestamp and fields are in the M1 archive.
- Tick route: `https://jetta.dukascopy.com/v1/ticks/XAU-USD/{YYYY}/{M}/{D}/{H}`. All 24 hours were requested for each candidate weekday independent of touch/confirmation. Raw empty buckets were retained. Per-hour UTC timestamp, quote count, BID/ASK and spread validity, duplicates, reversals, size and SHA-256 are in the nine Tick archives.
- M1 basic checks: 56/56 PASS for finite and ordered OHLC, ordered minute timestamps, UTC-day bounds and source decoding. Tick basic checks: 1,344/1,344 PASS; duplicate/reversed timestamp, invalid quote and nonpositive spread counts are zero. These checks do not replace the frozen official-hours structural gate.
- 2026-09-07 contains 1,229 M1 rows and an observed interval without bars after 18:28 through 21:59 UTC. Other sampled Monday–Thursday responses have 1,380 rows. Whether the missing interval is an official market closure or makes the session structurally ineligible has **not** been determined. No date was excluded or selected on this basis.
- An interrupted first Tick pass left the original retrieval timestamp unrecorded for 1,120 responses. Those original times remain UNKNOWN. A later first-party re-fetch matched stored byte count and SHA-256 for all 1,120; the new retrieval times are in the separate verification receipts. The other 224 responses retain their initial retrieval timestamps.
- The exact legacy `run_v01.py` SHA-256 `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd` was independently rechecked. The frozen H2 135-file prefix was **not** read back or concatenated in this preparation; Gamma/event generation was not run.
- Four truncated Drive uploads were detected by full ZIP readback and deleted only after verified replacement archives existed. They are not part of the valid source set.

## Persisted source and verification

- [M1 raw responses and manifest](https://drive.google.com/file/d/1h2Vhik3yz-UR05l-F_a0RQMYNkEKP71X/view): ZIP SHA-256 `32aa265060e302adb4f407a5ba6c31bb9406566a9424d6cfe269c7aaedd3a41d`; 56/56 per-file readback.
- [Tick re-fetch receipts and machine-readable archive index](https://drive.google.com/file/d/1c6VjfTX-HUgMioVJ_w_DIeaHPZWgfJjg/view): ZIP SHA-256 `92b4d848b383348bdb5291954c4a9f5b84371c56d20c3510ced8d972bcb65cd8`; 1,120/1,120 exact matches.

| Tick archive | Dates (UTC) | Hours | ZIP SHA-256 |
|---|---|---:|---|
| [Part 01](https://drive.google.com/file/d/1JSRJkk9w3NvHmsOfaqS2fa2J2fbtdI3e/view) | 2026-07-10–2026-07-21 | 192 | `38b46ba5ce099d64ad29029e13af596a7054df98b9a5e0ec0b865cfc680928c2` |
| [Part 02A](https://drive.google.com/file/d/1pEWVN8qXgy7gHt6NqNYz4mBo1NDmtb-d/view) | 2026-07-22–2026-07-27 | 96 | `84ffb426d9b73eeeaa284c0735365bcea46620d2507be71d613fff323d712ea1` |
| [Part 02B](https://drive.google.com/file/d/1tfwtBRF_foXoVcApFuQ3njIWIFBhaBUq/view) | 2026-07-28–2026-07-31 | 96 | `163bd59913c76d2b8b76d743f19c3e859930be6e5fd6b3d36a04f239c6d56aa5` |
| [Part 03](https://drive.google.com/file/d/1QPjMa-XG-Ss6zD8ydZbRDMsQjqsrpVNm/view) | 2026-08-03–2026-08-12 | 192 | `97c9aaa4270b267233c0f23dd5a2c554299687ea5300e706943741a8e001e767` |
| [Part 04](https://drive.google.com/file/d/1juAlC3Bwb6lwqPMiiBy9GZf7ri341NJ1/view) | 2026-08-13–2026-08-24 | 192 | `a27ec9e3c6dbcb07182f4127d6faadd5460fd09ae5a714859936624a9369cac6` |
| [Part 05A](https://drive.google.com/file/d/17V7b1JaQCvWDEDDErJt37kq9k5EnaVew/view) | 2026-08-25–2026-08-28 | 96 | `17caa4b92f0c0f243dd5dec4a94c99d8bba17028b995d051c1f58e5676e9aec4` |
| [Part 05B](https://drive.google.com/file/d/189N2HioiLXD1qgxUOPm5UrW16kUg1fF4/view) | 2026-08-31–2026-09-03 | 96 | `7ab34dd1e8a34a936083b0aa46ebe7e71576c456153bf0cfca279f4e3c1f93da` |
| [Part 06](https://drive.google.com/file/d/1mm1Ylr0PyFlbRK3yU135gaHuWAPuLb8D/view) | 2026-09-04–2026-09-15 | 192 | `c141da75efce11adca37de8811483120ff2cd231cf95f6d6aa9840051f479a92` |
| [Part 07](https://drive.google.com/file/d/1zIHc5UGoF4qXZLGvDIqFce4D2UeeHSzg/view) | 2026-09-16–2026-09-25 | 192 | `5ce2fcafd11b73eaa2ea080ba07c2637821224c0f174f313c96377417890458f` |

All nine archived Tick ZIPs were downloaded after upload. ZIP integrity, 56 unique daily manifests and 1,344 unique raw hourly members were checked, and every member SHA-256 matched its manifest. Total valid archived Tick ZIP bytes: 49,079,800.

## Closed boundary

At this date, only 56 Monday–Friday candidates had fully elapsed since 2026-07-10. Even if all passed the structural gate, fewer than 60 sessions exist. `DATA-HR-003` remains `FINAL_HOLDOUT / UNUSED`; no H3 Run or Result is created. No touch outcome, CONFIRMED-vs-UNCONFIRMED outcome comparison, primary contrast or bootstrap has been computed or viewed. A future session must fresh-read the current preregistration, source-preparation handoff, `DEC-HR-004`, dataset record, and repository main before progressing.
