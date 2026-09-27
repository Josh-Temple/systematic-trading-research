---
id: EXP-HR-005
type: Experiment
research_line_id: RL-HR-001
created_at: 2026-09-27
experiment_kind: DIAGNOSTIC
tests_hypothesis: NOT_APPLICABLE
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

# Successful exploratory D1-D5 diagnostic and integrated 2026H1 decomposition

## Purpose

Represent the completed D1-D5 diagnostic over the fixed, consumed 2026H1 sample and preserve the conflict between source reports without changing the sample, rules, or interpretation.

## Sources read

1. [Horizontal Reaction Strategy v0.1 — Data D1-D5 Exploratory Diagnostic Replay — 2026H1 v1](https://docs.google.com/document/d/1MreVcFJUz5sDu2w9-qdIAX7D2lGZ5aKeDoQZozZLHE4/edit), Drive document ID `1MreVcFJUz5sDu2w9-qdIAX7D2lGZ5aKeDoQZozZLHE4`. This source reports a full 2,685-event diagnostic and classifies it `A = EDGE_LOST_BEFORE_ENTRY`.
2. [HR_v01_2026H1_diagnostic_report_ja.md](https://drive.google.com/file/d/1ODFl8jxY676iMfrRAPlMyqHSFjfAeUTD/view), Drive file ID `1ODFl8jxY676iMfrRAPlMyqHSFjfAeUTD`, created 2026-09-23. It reports two unavailable +15-minute endpoints and the integrated classification `MULTIPLE_DRIVERS / INCONCLUSIVE`.
3. [PILOT-TRADING-001 Project Brief — GOLD Decision Research Lab](https://docs.google.com/document/d/1GMuRnL6ZPa_OR2tVY85dQujjk0EmgdJeOBsdbLytBnE/edit), Drive document ID `1GMuRnL6ZPa_OR2tVY85dQujjk0EmgdJeOBsdbLytBnE`, revision `ANLCKQmLpomUActZBEIn8CGcrIS8GCZz6tcEQTb1S3TbV-Rbi5YBVIiQVCtzT622W5QeuUjN8nVrvmGhdEOtFcSNofMlb8oIm80bqmFtDZs`. Its H1 section gives the same D1-D5 values/classification as the 2026-09-23 report and labels `MULTIPLE_DRIVERS / INCONCLUSIVE` as the current classification.

## Fact / source basis

The 2026-09-23 report describes a diagnostic on the fixed 60 sessions and 2,685-trade population using the exact archived source pack plus a separately persisted five-hour Tick Correction v2. It reports a missing raw endpoint for two D2/D4/D5 observations and two D3 observations; no proxy quotes were inserted.

The earlier 2026-09-13 Data replay document reports a complete 2,685-observation scope and different values/classification. The two source records are retained separately in RES-HR-005. This migration does not silently reconcile them or claim the later report explicitly invalidated the earlier record.

## Boundary / what this does not establish

Both sources classify their work as exploratory/diagnostic on consumed 2026H1 data. Neither establishes future profitability, causality, or a profitable alternative rule. No sample selection, parameter tuning, exclusions, or strategy-rule changes were made in this migration.

## Schema friction / UNKNOWN

This diagnostic decomposes a prior result rather than directly testing HYP-HR-001, so `tests_hypothesis` is `NOT_APPLICABLE`. Exact run start/end times, code commit, and environment identity are not captured in the source record. The two diagnostic source records disagree on endpoint availability, multiple D1-D5 values, and classification; no v0.1 field models competing source versions directly, so the discrepancy is preserved in Result and Diagnostic narrative.

## Related artifacts

- DATA-HR-001
- SPEC-HR-001-v01
- EXP-HR-003
- RUN-HR-005
- RES-HR-005
- DIAG-HR-003
- INT-HR-002
