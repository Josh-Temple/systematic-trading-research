# B — XM EURJPY Friday exit source readiness (2026-10-08)

## Scope and fresh-read identity

Authority: `docs/TRADING_FIVE_ROLE_EMPIRICAL_WAVE_2026-10-08.md` section B, read from `research/trading-five-role-empirical-wave-20261008` (Git blob `6fe6d079fb2976b8c157f104ad47cc62a1814162`). This is a **source-only, pre-outcome** preparation assessment, **not** XM runtime qualification, scientific support or a formal Packet D independent audit.

Fresh GitHub reads at the start of this B session:
- Repository default: `main`; observed main SHA `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`.
- PR #63: **OPEN / DRAFT**, base `main`, head branch `research/fx-news-sentiment-v0.1`, head SHA `8d3771921fbab88ea56b913f9d6fe8d62236961c`; not merged.
- This B branch starts at the exact observed PR #63 head, not `main`. No direct write to PR #63 head or `main`.
- Read `CURRENT.md`, `SOURCE_CONTRACT.md`, `SPEC-FXNS-001-v01.md`, `PRE_FREEZE_HARDENING_RESULT.md`, existing XM `RESULT.md`, `WINDOWS_RUNBOOK.md`, collector, XM test source, and `TEST_LOG.txt`; also `docs/RESEARCH_PRINCIPLES.md` and the Wave instructions.
- Exact collector Git blob SHA: `72fda266a3c83201c84958c5522380dcf79b56e7`; existing synthetic test Git blob SHA: `e6d510804050a3fa5f5c92d0f8418f7c923656e2`. The preceding XM `RESULT.md` records the collector's exact-byte SHA-256 as `04ec5d1b0a1d92ad82e0d501ec67390e7489cbf3e50e071b30310ed207cd0f5a`; this session did **not** independently recompute that SHA-256 from local bytes.

## Collector and fixed probe review

Existing `collect_mt5_eurjpy_source_probe.py` is `FXNS_EURJPY_SOURCE_PROBE_v0.2`. The six *already fixed*, outcome-independent JST windows are:

| ID | JST window | Purpose |
| --- | --- | --- |
| winter_2026 | 2026-01-15 08:14–08:16 | source/time/schema |
| summer_2026 | 2026-07-15 08:14–08:16 | source/time/schema |
| autumn_2026 | 2026-10-06 08:14–08:16 | source/time/schema |
| winter_friday_2026 | 2026-01-16 08:14–08:16 | Friday exit |
| summer_friday_2026 | 2026-07-17 08:14–08:16 | Friday exit |
| autumn_friday_2026 | 2026-10-02 08:14–08:16 | Friday exit |

For all six, UTC request times map to **23:14–23:16 UTC on the preceding calendar date**. This is independent calendar arithmetic; it does not validate the MT5 SDK's returned timestamp semantics. The existing collector:
- Calls `copy_ticks_range` with aware UTC bounds, `COPY_TICKS_ALL`, and exact symbol `EURJPY`; rejects automatic symbol substitution.
- Preserves original `time`, `time_msc`, `bid`, `ask` and remaining expected tick fields, including zero-row windows; its Bid/Ask row validation rejects nonfinite, nonpositive and crossed quotes.
- Projects allowlisted server identity, terminal build and symbol metadata; records collection time, returned raw timestamp bounds, JST and UTC window definitions, and original row counts.
- Writes `tick_probes_raw.csv`, `metadata.json`, `sha256_manifest.json` into a new directory and disallows overwriting it. Raw and metadata file sizes and SHA-256 are recorded; the manifest is not self-hashed.
- Labels timestamp semantics `UNVERIFIED_PRESERVE_RAW_TIME_AND_TIME_MSC`, commission and other costs UNVERIFIED. It does not issue trades, read order history, calculate return/P&L, or assert SOURCE PASS.

**Important limitations for later independent review:** `first_time/last_time` and `first_time_msc/last_time_msc` report the first/last returned array positions, rather than independently proven chronological extrema. The collector does not explicitly quantify duplicate/out-of-order rows or certify `time` vs `time_msc` consistency, effective market session, or first valid quote in [08:15:00, 08:16:00] JST. These are **review-required**, not evidence of a real observed defect. It would be unsound to infer Friday availability merely because the requested window has Friday in its label. Absent/invalid quotes, holiday or broker closure, and no-quote windows cannot be converted into a Monday rescue or SOURCE PASS.

## Checks performed in this session

- **16/16 read-only checks passed** against freshly fetched GitHub source and test content, using JavaScript source assertions plus independent ISO-8601/JST/UTC calendar arithmetic: version, six window definitions, three correct Friday dates/weekdays, 120-second timing, UTC mapping, expected tick fields, file/hash paths, exact-symbol rejection, presence of source-only API and account allowlist, explicitly unverified state, and coverage in existing synthetic test source. The same review explicitly detected **no dedicated duplicate/ordering test functions**; that finding is a coverage gap, not a PASS for duplicate integrity.
- Existing committed `xm-source/TEST_LOG.txt` records **12/12 XM fake/synthetic tests PASS** on Python 3.12.14, plus **44/44 implementation** and **9/9 source/preservation** tests; these are **historical claims read back**, not newly executed Python tests. They include fake valid/invalid Bid/Ask, zero rows, fixed Friday calendar, UTC conversion, exact symbol, metadata/manifest SHA, and no broker order API. Synthetic close/no-quote economic feasibility and actual returned timestamp semantics are not proven.
- **No Python unit test or MT5 collector was executed in this session.** No Windows terminal, account/server login, raw XM ticks or runtime outputs were accessible to this B execution. Thus no fresh local Python test count, no real terminal hash, and no actual 08:15 quote coverage result are asserted.
- **Code change: NONE.** No reproducible defect was established from actual collector inputs. Adding generalized infrastructure or editing the already adequate runbook would not clear the real gate. Existing raw evidence and tests were not rewritten.

## Single blocking dependency and exact local action

**Blocker: `LOCAL_XM_EXECUTION_REQUIRED` — the intended, already authenticated Windows XM MT5 environment is not accessible to this session.**

The account owner, on that *intended* Windows terminal only, should follow the **existing** `work/xm-source/WINDOWS_RUNBOOK.md` without changing any of the six dates or source rules:

1. In a new empty local folder, place the unmodified `collect_mt5_eurjpy_source_probe.py` v0.2 from PR #63. Install the prerequisites locally using `py -m pip install MetaTrader5 tzdata`.
2. Open the intended XM MT5 terminal and log in **locally**. Run `py collect_mt5_eurjpy_source_probe.py` once. If exact `EURJPY` is unavailable, **stop** at `EXACT_SYMBOL_IDENTITY_REQUIRES_PRE_FREEZE_DECISION`; do not silently switch to a suffixed symbol. If the run fails, preserve its failed directory as a failed attempt; do not relabel it successful.
3. Preserve the entire new directory, **without edits or selective deletion**: `tick_probes_raw.csv`, `metadata.json`, `sha256_manifest.json`. Record the collector file SHA-256 and manifest file SHA-256 locally as additional provenance; compare raw CSV/metadata byte lengths and SHA-256 against the manifest. No invented hashes or coverage values.
4. For independent *source-only* review, determine for **each of the six windows**: file presence, raw row count, null/invalid/nonfinite/crossed Bid/Ask, duplicate and out-of-order `time/time_msc` rows, `time_msc` precision versus `time`, request/returned bounds, actual UTC↔JST and broker/terminal display mapping, first valid Bid/Ask at or after 08:15:00 and through 08:16:00 **inclusive** (never pre-target), and whether the source was in a normal FX session or a Friday/holiday/maintenance closure. Preserve missing or blocked windows as such; do not infer success from any other day.
5. Separately verify exact broker symbol/server/build identity, symbol contract fields, swap interpretation, and **account-applicable** commission/other fees through an authorized non-sensitive source. The collector's swap fields are not full cost qualification; historical trade/order records are not to be fetched for that purpose.

For review, the **non-secret artifact names** are `tick_probes_raw.csv`, `metadata.json` and `sha256_manifest.json`; review needs actual file SHA-256/bytes, six-window counts/coverage with reason codes, time-mapping evidence, and a clear fee-status disposition. **Do not share** passwords, account number, account screenshots, balance/equity, authentication files, order history or private personal details. Any raw tick prices are **source qualification evidence only**, never a basis for direction, returns, performance, trading-rule selection or retrospective score.

## Disposition / scientific boundary

| Dimension | Disposition |
| --- | --- |
| Collector definition and read-only static/calendar checks | `PARTIAL_WITH_GAPS`: existing v0.2 is prepared; limited static checks completed; no new Python or real-MT5 runtime test |
| Real XM EURJPY Bid/Ask, server/time mapping, Friday 08:15 coverage, cost qualification | **`BLOCKED / LOCAL_XM_EXECUTION_REQUIRED`** |
| GDELT source gate (independent) | `PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED` (not changed here) |
| Scientific status / specification | `UNTESTED / PROPOSED_NOT_FROZEN` |
| Human freeze / independent Packet D audit / formal cohort / live or paper orders | **Not granted / not completed / CLOSED / NOT_AUTHORIZED** |

There was **no market-outcome access, real ChatGPT classification, price-direction/P&L/return/win-rate computation, order submission, alternative feed, rule amendment or automatic source promotion**. This report leaves existing `CURRENT.md`, SOURCE_CONTRACT, Specification, prompt/schema, raw evidence, and prior XM documents byte-unchanged.

**Next action (one):** the user conducts **one local, source-only v0.2 collection** on the intended XM Windows MT5 account and preserves all three artifacts for independent qualification; only then reassess actual Friday-source readiness. This B document itself does not unlock formal issuance, scoring or cohort access.
