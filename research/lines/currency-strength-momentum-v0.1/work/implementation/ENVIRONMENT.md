# Implementation environment and guarantee boundaries

## Recorded environment

- Python: 3.12.14 in this preparation session.
- Runtime dependency: Python standard library only.
- Verification: `unittest` and `py_compile`.
- Packet C metadata read: exact artifacts at branch `work/csm-source-qualification-20261001`, head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`.
- The integration test verifies Packet C Git blob identities for the source lock, probe schema metadata, and expected calendar. It generates synthetic CSV rows from the declared schema. It does not read probe response CSVs, extract `OBS_VALUE`, or request full history.
- The module contains no HTTP client. The authorized calculation path installs a Python audit hook blocking socket connection, DNS lookup, shell, and subprocess events.
- Runtime receipts record SHA-256 identities for code, config, tests, test log, source lock, probe metadata, expected calendar, raw snapshot, event ledger, and calculation artifacts.

## What tests establish

Synthetic tests cover exact decimal ratio ordering and ties, quote inversion and pair return direction, 56 ordered-pair equivalence, numeraire invariance, complete-network pair-average ranking, calendar-slot preservation, missing-data fail-closed behavior, prefix/future-suffix invariance, temporal receipt boundaries, fixed circular bootstrap behavior, type-7 percentiles, and decision thresholds.

The Packet C integration test checks the exact source-lock mapping, seven ECB series identities and dimensions, ordered 32-column CSV schema, accepted status, units and decimal scales, official calendar file/date/month-end hashes, and all 203 monthly endpoints. Its test rows are generated synthetic values, not ECB observations.

## What tests do not establish

- Packet C's `PARTIAL_WITH_GAPS` status is retained. Its bounded probe qualifies one fixed month’s route/schema/calendar identity only. It does not establish full-history coverage, historical publication time, revision/vintage access, or availability on every expected date.
- Packet C reported an incidental search-result observation exposure. Packet D did not retrieve, repeat, reproduce, or use those values; the disclosure still requires Integrator review before any outcome access.
- No full-history data coverage, market ranking, forward return, performance metric, or strategy result was calculated by Packet D.
- The official expected calendar identity was hash-checked, but D's tests do not independently adjudicate the authority or legal scope of the ECB/TARGET calendar rule.
- No historical `AVAILABLE_AT` or executable quote/fill timing was established. The result boundary remains `REFERENCE_ASSOCIATION_ONLY`.
- Synthetic formula tests do not prove data integrity, market accessibility, profitability, robustness, or independent confirmation.
- JSON receipt checks validate required fields and byte identities but do not cryptographically authenticate a human, auditor, or Integrator. File permissions and process isolation remain external controls.
- Python audit hooks reduce accidental network use from this process; they are not an operating-system sandbox and do not prevent a separate process from reading files.

## Runtime output boundary

The authorized runner writes machine-readable files under a new output directory. The event ledger includes calendar slots, pair identities, dates, and skip reasons but excludes target outcomes. It is written and hashed before outcome calculation. Later metrics and inference files contain market-derived outputs and must remain access-controlled. A stopped or invalid attempt is operational evidence, not a scientific rejection.
