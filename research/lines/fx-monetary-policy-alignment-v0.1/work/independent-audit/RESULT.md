---
id: AUDIT-FXMP-E-20261004-01
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: PENDING_CI
execution_status: NOT_RUN
evidence_validity: NOT_APPLICABLE
scientific_status: NOT_APPLICABLE
tests_hypothesis: NOT_APPLICABLE
relations:
  - type: derived_from
    target: DIAG-FXMP-SOURCE-001
  - type: derived_from
    target: DIAG-FXMP-IMPLEMENTATION-001
---

# Packet E — independent pre-outcome audit

## Audit input

Exact implementation/source head under audit:

`d1a8d41d74eac78d420c6776971af3cc1be37931`

This audit branch was created directly from that exact head.

## Independence rule

The audit does not reuse the implementation's test functions as its oracle.

It:
- freshly reads the exact source lock, proposed spec and implementation;
- uses an independently written synthetic oracle;
- compares implementation outputs against the oracle;
- statically checks the implementation for network/subprocess/dataframe-style dependencies;
- verifies fixed source hashes and currency-to-BIS-area mapping;
- independently checks outcome-field invariance.

No FX prices, price rankings, target returns, P/L, Sharpe or performance plots are read.

## Provisional boundary

Even if the independent synthetic audit passes, this does not open market-outcome access. Final inference code/audit, durable-source disposition, and explicit human freeze are separate gates.
