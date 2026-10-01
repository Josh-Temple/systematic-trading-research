---
id: DATA-CSM-002
type: Dataset
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PLANNED
dataset_role: EXPLORATORY_DISCOVERY
capture_status: NOT_CAPTURED_FOR_EXPERIMENT
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
---

# ECB EXR monthly reference association dataset — planned, not captured

## Planned identity

- Science contract: SPEC-CSM-002-v01, frozen post-metadata SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`; accepted pre-freeze SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`.
- Source family: ECB EXR daily, seven fixed keys D.CCY.EUR.SP00.A for AUD/CAD/CHF/GBP/JPY/NZD/USD; EUR is the synthetic numeraire.
- Candidate source-lock: CSM-SOURCE-LOCK-ECB-001, Git blob SHA-1 `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf`, SHA-256 `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71`. This qualifies only the bounded route/schema example, not full-history coverage or historical vintage.
- Candidate expected calendar: ECB_TARGET_LONG_TERM_2002_RULE, 4,331 expected open dates and 203 monthly endpoints; file SHA-256 `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4`.
- Source boundary: 2009-11-01 through 2026-09-30. Target months: 2010-01 through 2026-09.
- Approved dataset role: EXPLORATORY_DISCOVERY only. No future confirmation sample is designated or accessed.

## Qualification versus experiment data

Packet C executed a fixed November 2009 source-qualification probe for the seven series. Its receipt reports 21 expected dates per series, status A, the 32-column CSV schema, and byte-exact raw response hashes. The response schema contains OBS_VALUE. C reports that its metadata probe did not extract, compare, calculate with, or emit OBS_VALUE values. The raw probe CSV snapshots remain in local scratch rather than this repository. This bounded probe is a source-qualification artifact; it is not the full Experiment dataset, a market-result receipt, or evidence of target-period coverage.

C separately disclosed that an ECB converter search result and a FRED series search result incidentally displayed individual current observations during source discovery. According to C's Result, those values were not recorded, reproduced, cross-compared, or used. This Integrator did not retrieve those snippets or raw probe CSVs and does not reproduce any observation values. That incident remains unresolved for evidence-validity and outcome-access purposes.

During a separate Integrator documentation review, the official public ECB current reference-rates page returned a daily table containing individual current observations in the tool output. This exceeded the metadata-only scope. No individual value was transcribed into an integration artifact, quoted, compared, calculated, or used. This is a separate exposure incident; human and independent E disposition is pending.

## Known gaps

- Full-history coverage and actual missing/duplicate/status distribution: UNKNOWN; no full-history capture or machine preflight has occurred.
- Historical setting/publication time, date-specific availability, method continuity, and original/latest-vintage history: UNKNOWN. The accepted claim is limited to retrospective latest-vintage reference association, not causal availability or executable entry.
- Revision and republication availability across the sample: UNKNOWN.
- Reference rates are not executable BID/ASK quotes. Spread, slippage, commission, carry, financing, and realized trading costs: UNOBSERVED.
- Public raw capture is only supported as a cited, byte-preserved ECB export under the C report's documented reuse assessment; the durable destination and access-control arrangement are not assigned.
- Any later source, calendar, transport, unit, status, or vintage change requires a fresh source identity and downstream audit.

No full-history dataset, rankings, returns, or performance metrics have been generated for this planned record. The human freeze does not authorize a capture or analysis.
