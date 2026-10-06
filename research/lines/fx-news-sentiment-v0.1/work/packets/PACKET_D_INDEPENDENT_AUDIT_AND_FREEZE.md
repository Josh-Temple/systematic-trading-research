# Packet D — Independent pre-outcome audit and human freeze packet

## Goal

Independently determine whether the proposed v0.1 can safely enter a prospective shadow cohort.

## Audit

Fresh-read repository state and independently verify:

- specification completeness;
- source qualification;
- prompt hash and output schema;
- information cutoff;
- exact pair rule and zero semantics;
- XM quote/cost semantics;
- append-only records;
- synthetic-test coverage;
- no outcome-bearing data in design/implementation paths;
- no silent dependence on currency-strength or other research results.

## Human decision packet

If the audit passes, present the user with only the unresolved scientific choices that truly require human acceptance, including:

- final source allowlist;
- exact prompt/model identity policy;
- 60-event cohort size or justified alternative;
- advancement/rejection rule;
- cost claim boundary.

Do not show prospective market outcomes before freeze.

## Outcomes

- `PASS_READY_FOR_HUMAN_FREEZE`;
- `PARTIAL_WITH_GAPS`;
- `BLOCKED`.

Only explicit human freeze after a PASS opens the formal cohort.
