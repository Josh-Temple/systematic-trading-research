# Packet A — Source qualification

Role: independent source qualifier.

1. Fresh-read current main, this line's SPEC and SOURCE_CONTRACT.
2. Do not access 2026 data.
3. Resolve exact JPX DataCube Nikkei 225 mini dataset/product identity and license/storage boundary.
4. Validate timestamp and contract-code semantics without calculating price outcomes.
5. Produce a bound source receipt with raw-file hashes and coverage-only diagnostics.
6. PASS only if source semantics are adequate for the frozen point mapping.

Output must distinguish PASS, PARTIAL_WITH_GAPS and FAIL.


## Current pre-purchase status — 2026-10-04

Public metadata now identifies the monthly series route future_tick_19_YYYYMM and twelve period selections in work/source-qualification/DATACUBE_2025_PURCHASE_MANIFEST.json. The local-only validator, synthetic tests, runbook, and completion checklist are linked from that directory.

Current classification: PARTIAL_WITH_GAPS / WAITING_FOR_JPX_LICENSE_CLARIFICATION / OUTCOME_BLINDNESS_COMPROMISED. Product metadata review is not source PASS. No raw DataCube target files were acquired. The current DataCube FAQ does not expressly resolve whether source hashes, schema, and coverage metadata may be published by this unaffiliated individual project. Inquiry draft is prepared and unsent.

A JPX public search result exposed a 2025 futures quote snippet during this Work run. No values were recorded or used and no outcome calculations were performed. See work/source-qualification/OUTCOME_ACCESS_INCIDENT_2026-10-04.md. Do not describe this research line as outcome-unviewed, and do not run the 2025 confirmation pending owner disposition.
