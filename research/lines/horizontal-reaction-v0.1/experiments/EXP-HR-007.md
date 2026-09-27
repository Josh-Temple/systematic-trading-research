---
id: EXP-HR-007
type: Experiment
research_line_id: RL-HR-001
created_at: 2026-09-23
status: WAITING_FOR_MATURITY
experiment_kind: CONFIRMATORY
tests_hypothesis: HYP-HR-003
uses_specification: SPEC-HR-003-v01
planned_dataset_uses:
  - dataset_id: DATA-HR-003
    role_at_freeze: FINAL_HOLDOUT
relations:
  - type: tests_hypothesis
    target: HYP-HR-003
  - type: uses_specification
    target: SPEC-HR-003-v01
  - type: uses_dataset
    target: DATA-HR-003
---

# Post-H2 Confirmation Selection Effect test

## Purpose

Test the frozen HYP-HR-003 on the first 60 structurally eligible UTC trading weekdays from 2026-07-10, using all eligible first-touch events and the frozen confirmed/unconfirmed classification.

## Current state

`WAITING_FOR_MATURITY`. The latest retrieved source-preparation handoff reports 54 Monday-Friday calendar dates through 2026-09-23 and earliest possible maturity on 2026-10-01 if all next six weekdays pass the structural gate. No 60-session sample or source-gate PASS was present in the retrieved sources for this migration.

## Current authorized preparation

- exact source/sample identity checks;
- first-party M1/Tick acquisition and hash manifest;
- structural eligibility;
- freezing the first 60 eligible sessions;
- outcome-blind calculation preparation.

## Strict hold

Until 60 eligible sessions are frozen and source gate PASS, do not compute or inspect touch outcomes, CONFIRMED-vs-UNCONFIRMED outcomes, the primary contrast, or bootstrap output. No run or Result entity is created by this preregistration migration.

## Sources

- Frozen preregistration: https://docs.google.com/document/d/1GRa035N5FX3F59_wM2T11VFuv3aL85YZghmvaCeTJ0g/edit
- Source preparation handoff: https://docs.google.com/document/d/1QPwXqAcp1fzPm6VXelMLDMyist02-sSSDQ1lkrpsoSg/edit
