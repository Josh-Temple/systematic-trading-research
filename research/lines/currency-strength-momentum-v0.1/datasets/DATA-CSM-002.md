---
id: DATA-CSM-002
type: Dataset
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PLANNED_NOT_FROZEN
dataset_role: EXPLORATORY_DISCOVERY
capture_status: NOT_CAPTURED_FOR_EXPERIMENT
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
---

# ECB EXR monthly reference association dataset — planned only

## Planned identity

- Source family: ECB EXR daily, seven fixed keys D.CCY.EUR.SP00.A for AUD/CAD/CHF/GBP/JPY/NZD/USD; EUR is the synthetic numeraire.
- Candidate source-lock: CSM-SOURCE-LOCK-ECB-001, Git blob SHA-1 81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf, SHA-256 ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71.
- Candidate calendar: ECB_TARGET_LONG_TERM_2002_RULE, 4,331 expected open dates and 203 monthly endpoints; file SHA-256 6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4.
- Proposed source boundary: 2009-11-01 through 2026-09-30.
- Proposed target months: 2010-01 through 2026-09.
- Proposed role: EXPLORATORY_DISCOVERY only. This role has not been human-approved. No future confirmation sample is designated or accessed.

## Qualification versus experiment data

Packet C executed a fixed November 2009 source-qualification probe for the seven series. Its receipt reports 21 expected dates per series, status A, the 32-column CSV schema, and byte-exact raw response hashes. The response schema contains OBS_VALUE. C reports that its metadata probe did not extract, compare, calculate with, or emit OBS_VALUE values, and the raw probe CSV snapshots remain in local scratch rather than this repository. This bounded probe is a source-qualification artifact; it is not the full Experiment dataset, a market-result receipt, or evidence of target-period coverage.

Separately, C disclosed that an ECB converter search result and a FRED series search result incidentally displayed individual current observations during source discovery. According to C's Result, those values were not recorded, reproduced, cross-compared, or used. The Integrator did not retrieve the snippets or raw probe CSVs and does not repeat any observation values. The disclosure remains unresolved for evidence-validity and outcome-access purposes; no claim that the discovery sample is wholly unexposed is made.

## Known gaps

- Full-history coverage and actual missing/duplicate/status distribution: UNKNOWN until a separately authorized capture and machine preflight.
- Historical setting/publication time, date-specific availability, method continuity and original/latest-vintage history: UNKNOWN.
- Revision and republication availability: UNKNOWN.
- Reference rates are not executable BID/ASK quotes. Spread, slippage, commission, carry, financing and realized trading costs: UNOBSERVED.
- Public raw capture is only supported as a cited, byte-preserved ECB export under the C report's documented reuse assessment; the durable destination and access-control arrangement are not assigned.
- Any later source, calendar, transport, unit, status or vintage change requires a fresh source identity and downstream audit.

No full-history dataset, rankings, returns or performance metrics have been generated for this proposed record.

