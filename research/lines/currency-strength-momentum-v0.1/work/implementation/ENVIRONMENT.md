# CSM-002 implementation environment

## Verified software environment

- Python 3.12.14, CPython on Linux, using the Python standard library.
- Test runner: `unittest`; syntax check: `py_compile`.
- No external Python package, network client, plotting library, or exchange-rate download tool is used by the implementation or tests.
- Gate signatures use a small standard-library RSA/SHA-256 verifier. Production trust keys are read only from the fixed root-owned trust-store path `/etc/csm-002/trusted-keys.json`; no production key is included, generated, or assigned by this D work. Tests use a synthetic private key fixture that is never available to the production CLI.

## Input boundary for the verified suite

The suite reads the exact Packet C source-lock, probe-metadata, and expected-calendar metadata artifacts at PR #35 head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`, verifies their Git blob and SHA-256 identities, and generates its own metadata-shaped synthetic CSV rows. It does not fetch or read Packet C probe-response CSVs or market observations. All price-like test values and all calculations are synthetic.

The source-lock file is read into one byte buffer and parsed from that buffer. Gate and capture receipt checks bind both its canonicalized object hash and its raw-byte SHA-256. Tests alter whitespace while preserving JSON meaning and confirm the signed raw-byte mismatch is rejected.

## What tests establish

- Exact-ratio score identities bind each currency's formation inputs and the fixed score calculation specification.
- The pre-outcome event ledger records `a`, `b`, formation endpoints, every currency's score identity, and pre-outcome skip reasons. Changing or removing the synthetic target endpoint does not change ledger bytes.
- Signed E and I2 test envelopes are accepted only with trusted test keys and matching role, identity, expiry, code/config/test/environment, source-lock, calendar, and metadata hashes. Unknown keys, placeholders, absent/expired receipts, identity mismatch, and invalid signatures fail closed.
- Capture and output staging is checked before promotion. Fault injection covers writes, flush, file fsync, raw-byte validation, rename, directory promotion, and final success-receipt creation.
- The full fixed formula, calendar, bootstrap, threshold, Packet C metadata integration, and closed-gate no-read suite remains in place.

## What tests do not establish

- Current I2 remains CLOSED and the exact current E audit remains PARTIAL_WITH_GAPS / BLOCKED. The test-only gate overrides and test keys are not real authorization.
- A root-owned local trust-store file is an interface, not proof that a production trust root has been distributed. Platform/security staff must provision and fingerprint the E and Integrator public keys and maintain revocation/validity records.
- A Python audit hook is process-local defense against selected accidental actions. It is not OS-level file/process isolation, does not enforce a filesystem allowlist, and cannot stop another process from reading a file.
- D has not provisioned or verified a durable allowlisted runner, durable output storage, persistent append-only access/attempt ledger, or named outcome-access operator. Those owners and checks are listed in `RUNBOOK.md` and remain external GAPs.
- Packet C remains `PARTIAL_WITH_GAPS`; bounded metadata does not establish full-history coverage, missing/status distribution, historical publication timing, or revision/vintage availability. External calendar authority and disclosed observation-exposure disposition are also unresolved.
- No market history, outcome, ranking, return, P/L, Sharpe, or performance plot was read or calculated.
