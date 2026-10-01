# Implementation environment and guarantee boundaries

## Recorded environment

- Python: 3.12.14 in this preparation session.
- Runtime dependency: Python standard library only.
- Verification: `unittest` and `py_compile`.
- Network/source access during implementation: none for market data; the module contains no HTTP client. The authorized run path installs a Python audit hook blocking socket connection, DNS lookup, shell, and subprocess events.
- Input/output identities: SHA-256 is recorded for code, fixed config, source lock, expected calendar, raw snapshot, event ledger, and metrics. Python version, implementation, platform, and file hashes form an environment identity.

The production runner's current environment hash is intentionally not frozen here. A future gate must be generated against the exact execution environment and current code/test/config bytes.

## What tests establish

Synthetic tests cover exact decimal ratio ordering and ties, quote inversion and pair return direction, 56 ordered pair equivalence, numeraire invariance, complete-network pair-average ranking, calendar-slot preservation, missing-data fail-closed behavior, prefix/future-suffix invariance, receipt temporal boundaries, fixed circular bootstrap behavior, type-7 percentiles, and decision thresholds.

## What tests do not establish

- No official ECB series, response format, quote unit, observation-status code, publication history, revisions, or source license was requalified here.
- No official TARGET holiday calendar was retrieved or hashed. The code consumes an externally qualified calendar and never infers month ends from available prices.
- No historical `AVAILABLE_AT` or executable quote/fill timing was established. The result boundary remains `REFERENCE_ASSOCIATION_ONLY`.
- No full-history data coverage, market ranking, forward return, performance metric, or strategy result was calculated.
- Synthetic formula tests do not prove data integrity, market accessibility, profitability, robustness, or independent confirmation.
- The JSON receipt checks required fields and byte identities but does not cryptographically authenticate the named human, auditor, or Integrator. File permissions and process isolation remain external controls.
- Python audit hooks reduce accidental network use from this process; they are not an operating-system sandbox and do not prevent a separate process from reading files.

## Runtime output boundary

The authorized runner writes machine-readable files under a new output directory. The event ledger includes calendar slots, pair identities, dates, and skip reasons but excludes target outcomes. It is written and hashed before the outcome calculation. The later metrics file includes market-derived output and must remain access-controlled. A stopped/invalid attempt is operational evidence, not a scientific rejection.
