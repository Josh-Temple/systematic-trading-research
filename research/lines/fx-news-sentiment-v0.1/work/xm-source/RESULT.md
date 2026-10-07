# XM EURJPY Friday exit collector preparation — 2026-10-07

Fresh-read baseline: PR #63 head `885f4e5b357d8eca4edebe7b836e27a7615f1fac`, OPEN/DRAFT.
Read current projection, specification, pre-freeze report, collector/runbook/result
and cross-references. Schedule consistent: Mon–Thu issuance, next weekday 08:15 JST
exit, Thursday→Friday, Friday exit-only, no Monday rescue, formal cohort CLOSED.
Previous report's missing-Friday statement describes v0.1; v0.2 supersedes it.

Scientific status: UNTESTED
Specification: PROPOSED_NOT_FROZEN
XM collector: FRIDAY_EXIT_PROBE_READY_NOT_RUN
XM source qualification: LOCAL_XM_EXECUTION_REQUIRED
Market outcome access: NONE
Formal cohort: CLOSED

## Current collector identity

Version: `FXNS_EURJPY_SOURCE_PROBE_v0.2`
Current collector exact-byte SHA-256: `04ec5d1b0a1d92ad82e0d501ec67390e7489cbf3e50e071b30310ed207cd0f5a`
Previous v0.1 hash was `5745c2dc75061b3b7249b5fdbced20c52ad6eecabd6d61799ee9f68a0a621c03`;
that is historical, not the current hash.

## Change and selection basis

Existing January 15 / July 15 / October 6 probes unchanged. Added January 16,
July 17, October 2 Friday windows 08:14–08:16 JST solely by calendar/season:
winter, summer, recent complete period. All precede October 7; January 15 Thursday
and January 16 Friday are adjacent. No prices or spreads used for selection.
Each probe records purpose, intended weekday, JST/UTC request bounds, row count
and original first/last time/time_msc. Friday purpose FRIDAY_EXIT_FEASIBILITY.
Raw CSV contains original values, no returns, signals, order or liquidity judgment.

Exact EURJPY only, no substitution. Fail-closed symbol error has explicit pre-freeze
decision code and may show EURJPY-like names only. Price validation now also rejects
NaN/infinity (implementation integrity repair, no change to economic criteria).
Empty arrays are preserved as zero rows for independent review, not SOURCE PASS.
UTC-aware requests and UNVERIFIED_PRESERVE_RAW_TIME_AND_TIME_MSC remain distinct.
No account history/financial field access. account_info's SDK object is projected
only to server; balance/equity etc are neither accessed nor saved. Swap remains
metadata; commission and other costs stay unverified. No automatic feasibility flag.

## Tests (all fake/synthetic, no actual MetaTrader5 import/terminal connection)

- collector py_compile PASS
- 12 XM unit tests PASS: calendar, adjacent Thursday/Friday, old windows, UTC,
  schema/invalid and nonfinite Bid/Ask, raw epochs, allowlist field access,
  six-window fake-MT5 serialization/manifest SHA, overwrite rejection, exact-symbol
  failure/suffix rejection, AST source-only API allowlist/no price division
- existing implementation 44 tests PASS + source/preservation 9 PASS
- total 65/65 PASS; TEST_LOG.txt records runtime and commands
- git diff --check PASS

An initial test incorrectly interpreted pathlib '/' joins as price division; fixed
that assertion to allow file-path joins. No scientific rule change resulted.

## Remaining blockers and next local step

Actual exact symbol/server, raw-time mapping, Friday boundary quotes, swap and
commission/other account costs are unqualified. A six-window collection alone
cannot prove every future holiday/session's availability. No SOURCE PASS, freeze or
cohort opening. GDELT, formal runner and independent audit gates remain unchanged.

Use WINDOWS_RUNBOOK.md on intended Windows XM terminal: start/login locally,
run collector in an empty folder, preserve tick_probes_raw.csv, metadata.json and
sha256_manifest.json unchanged, then provide them for independent source review.
Do not provide password/account number/balance/equity. Do not substitute feeds or
calculate strategy outcomes. Real MT5 execution was not performed in this task.
