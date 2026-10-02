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
updated_at: 2026-10-02
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

## Historical E audit update against pre-correction D — 2026-10-02

Packet E at PR #38 head `d1335b29eeb01cdd4b71cd5ded62033b8468e539` completed with status PARTIAL_WITH_GAPS and recommendation BLOCKED. E read only C's source-lock, probe-metadata and expected-calendar artifacts; it did not read C's RESULT, raw probe CSV, OBS_VALUE values or full-history market data. E verified the declared calendar sequence and hashes internally, but did not independently retrieve an external calendar authority. Full-history coverage, actual missing/status distribution, historical publication time and revision/vintage availability remain UNKNOWN.

E also confirmed that the current I2 gate remains closed and made no market-result calculation. C's search-result exposure and the Integrator's separate ECB page exposure remain pending human disposition; no individual values are repeated here. The durable output destination, access/attempt ledger, named operator, trusted isolation controls and gate receipt authentication are still unassigned or unauthenticated. DATA-CSM-002 remains PLANNED and NOT_CAPTURED_FOR_EXPERIMENT.



## D correction record before the completed E re-audit — 2026-10-02

D PR #34 is open/draft/unmerged at exact head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`. The unchanged config remains FROZEN and pins the accepted frozen SPEC. D reports 53/53 synthetic tests and changes to outcome-blind score identities, signed fail-closed receipts, raw-byte source-lock verification, and atomic staged output. Packet I read the exact current D deliverable identities; it did not rerun D's tests. At the time of this earlier note, the former E audit at PR #38 head `d1335b29eeb01cdd4b71cd5ded62033b8468e539` was a PARTIAL_WITH_GAPS / BLOCKED historical audit of D head `4f739d9cc2b21c138771afec4a728bf2b57060ba`. The clean independent re-audit has since completed at E head `4f683901d01fd6b5ce161c874118a34d40bcac82` against current D head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`; see the current update below.

D's code-level changes do not resolve the remaining source and operational gaps: full-history coverage, actual missing/status distribution, historical publication time, revision/vintage access, and external calendar authority remain unknown or unverified. Production trust-key provisioning, OS-level isolation, filesystem allowlist, durable destination/access-attempt ledger, named operator, and human dispositions of both exposure disclosures remain open. D's runbook/test log still reference the pre-refresh I2 and E identities; E's completed re-audit confirms the current D gate binding rejects the refreshed I/E identities. D must refresh them using a non-circular design.

DATA-CSM-002 remains PLANNED and NOT_CAPTURED_FOR_EXPERIMENT. No full-history capture, market-outcome calculation, ranking, return, or performance metric was accessed or generated by this refresh; no instruction was issued to X.


## Current independent E re-audit — 2026-10-02

E PR #38 head `4f683901d01fd6b5ce161c874118a34d40bcac82` completed audit `AUDIT-CSM-E-20261001-REAUDIT-01` against D PR #34 head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`. The result is PARTIAL_WITH_GAPS / BLOCKED. E independently reran D's 53-test synthetic suite and confirmed outcome-blind score identities, tested signature/identity controls and raw source-lock-byte binding. It also found D rejects the refreshed current I/E identities and reproduced a compound promotion/rollback failure that leaves a success receipt in the destination.

The current D and E artifact identities and full findings are in GATE.md and the E result/matrix. External source and operational gaps remain: external calendar authority, full-history coverage, status/missing distribution, historical timing/vintage, production trust keys, OS isolation, filesystem allowlist, durable destination/access ledger, named operator and human exposure dispositions. B path/base and original-brief traceability remain separate gaps.

DATA-CSM-002 remains PLANNED and NOT_CAPTURED_FOR_EXPERIMENT. The E audit used only the three permitted C metadata files and synthetic values; it did not read C RESULT, raw probe CSV, OBS_VALUE, market history or results. No experiment capture or outcome calculation occurred.
