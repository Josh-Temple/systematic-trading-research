---
id: EXP-HR-002
type: Experiment
research_line_id: RL-HR-001
created_at: 2026-09-27
experiment_kind: SOURCE_QUALIFICATION
tests_hypothesis: UNKNOWN
uses_specification: SPEC-HR-001-v01
planned_dataset_uses:
  - dataset_id: DATA-HR-001
    role_at_freeze: CONSUMED_HOLDOUT
relations:
  - type: uses_specification
    target: SPEC-HR-001-v01
  - type: uses_dataset
    target: DATA-HR-001
---

# 2026H1 persistent Source Pack recovery and identity validation

## Purpose

Migrate the source-pack recovery and identity-validation work. This is source qualification, not a new trading test, and it did not execute D1-D5.

## Fact / source basis

Primary source: [Horizontal Reaction Strategy v0.1 — 2026H1 Source Pack Recovery Result (Chat Branch)](https://docs.google.com/document/d/1MAYi0VwMhQo9zQIO6LGa0tidIlra4ITykwbU1wIplWc/edit), Drive document ID `1MAYi0VwMhQo9zQIO6LGa0tidIlra4ITykwbU1wIplWc`, revision `ANLCKQn7pswb5Zm-YxTA13Ed6lfF_q654JOeNsIn7WmbvnXlw8Yc1EdxKrCnZltBeDpbd72AXtZH9YhuBphdoCvgV-EROEwDfP83YxWoGU0`.

The source reports:

- `SOURCE_PACK_STATUS=COMPLETE`
- `SOURCE_IDENTITY_STATUS=CONTENT_MATCH_PACKAGING_DIFFERENT`
- original raw data found, reused, and reacquired from the same first-party Dukascopy JETTA route
- selected M1 per-file identities matched 60/60; all 129 raw M1 files were reported valid
- Tick per-file identities matched 1,366/1,366; one Tick hour was reacquired and matched the prior hash
- authoritative population remained 2,685 trades
- no missing source scope was reported for the recovery work
- source-pack archive SHA-256: `e243b306f2eaf67485d334cdf17497f260b30f705e5d67cd5937377d3106f491`
- the original execution scope was 1,366 Tick UTC hours; the fresh D1-D5 manifest scope was 1,321 hours, with 50 original-only and 5 manifest-only hours

The source explicitly states that underlying raw-file content identities matched although the archive packaging differed. It also states that the prior aggregate-SHA canonicalization/packaging algorithm is unspecified.

## Migration interpretation

DATA-HR-001 remains the scientific sample. No new Dataset entity is created because this source describes recovered packaging and matching per-file identities, not a materially different dataset identity.

## Boundary / what this does not establish

D1-D5 were deliberately not run in this work (`D1_D5_RUN=NO`; each D1-D5 item is `NOT_RUN`). This source qualification establishes neither a new trading result nor a new interpretation of HYP-HR-001. It does not establish how the prior aggregate SHA was produced.

## Schema friction / UNKNOWN

The v0.1 Experiment entity requires `tests_hypothesis`, but this source-qualification task does not test a trading hypothesis. The field is retained as `UNKNOWN` rather than falsely linking HYP-HR-001. The source does not specify the run start/completion timestamps or result observation timestamp; these remain `UNKNOWN` in the associated Run and Result.

## Related artifacts

- DATA-HR-001
- SPEC-HR-001-v01
- RUN-HR-002
- RES-HR-002
