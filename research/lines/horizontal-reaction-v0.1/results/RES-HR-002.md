---
id: RES-HR-002
type: Result
research_line_id: RL-HR-001
run_id: RUN-HR-002
observed_at: UNKNOWN
execution_status: SUCCESS
evidence_validity: VALID
scientific_status: NOT_APPLICABLE
headline_metrics:
  selected_m1_per_file_identity: MATCH_60_OF_60
  raw_m1_files_reported_valid: 129
  tick_per_file_identity: MATCH_1366_OF_1366
  authoritative_trade_population: 2685
  original_tick_execution_scope_hours: 1366
  fresh_d1_d5_manifest_scope_hours: 1321
  original_only_hours: 50
  manifest_only_hours: 5
  archive_packaging: DIFFERENT
  aggregate_sha_algorithm: UNKNOWN
artifact_refs:
  - https://docs.google.com/document/d/1MAYi0VwMhQo9zQIO6LGa0tidIlra4ITykwbU1wIplWc/edit
  - https://drive.google.com/file/d/1uCcOwyaWloeMSgDEhW9IfXlxAEgpbH8I/view
diagnostic_refs: []
relations:
  - type: produced_by_run
    target: RUN-HR-002
  - type: derived_from
    target: DATA-HR-001
---

# Source Pack recovery result

## Observation

The primary source reports that the persistent Source Pack was recovered and read back; selected M1 and Tick underlying file identities matched their prior per-file SHA-256 manifests despite different archive packaging. The authoritative 2,685-trade population was retained. It records 1,366 original execution-scope Tick hours and a 1,321-hour fresh D1-D5 manifest scope, differing by 50 original-only and 5 manifest-only hours.

## Result status scope

`scientific_status: NOT_APPLICABLE` records that source qualification produced no scientific hypothesis outcome. It neither supports nor rejects HYP-HR-001.

## Evidence boundary

The aggregate-SHA canonicalization/packaging algorithm is unspecified. This result does not claim aggregate archive equivalence. D1-D5 were deliberately `NOT_RUN` in this recovery work; blocked or unrun diagnostics are not negative strategy evidence.

## Source

[Horizontal Reaction Strategy v0.1 — 2026H1 Source Pack Recovery Result (Chat Branch)](https://docs.google.com/document/d/1MAYi0VwMhQo9zQIO6LGa0tidIlra4ITykwbU1wIplWc/edit) (revision `ANLCKQn7pswb5Zm-YxTA13Ed6lfF_q654JOeNsIn7WmbvnXlw8Yc1EdxKrCnZltBeDpbd72AXtZH9YhuBphdoCvgV-EROEwDfP83YxWoGU0`).
