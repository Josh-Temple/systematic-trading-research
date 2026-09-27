---
id: SPEC-HR-003-v01
type: Specification
research_line_id: RL-HR-001
version: v0.1
created_at: 2026-09-23
frozen_at: 2026-09-23
freeze_status: FROZEN
tests_hypothesis: HYP-HR-003
data_roles_allowed:
  - FINAL_HOLDOUT
outcome_definition: Difference in mean direction-aware touch-to-+15-completed-minute bps between CONFIRMED and UNCONFIRMED events in the frozen first-60-eligible-session sample
metrics:
  - eligible_touch_event_count
  - confirmed_count_and_rate
  - unconfirmed_count
  - unavailable_count_and_reason
  - confirmed_mean_and_median_bps
  - unconfirmed_mean_and_median_bps
  - primary_contrast_bps
  - session_clustered_95_percent_interval
  - secondary_descriptive_metrics
stopping_or_kill_conditions:
  - fewer_than_60_structurally_eligible_sessions
  - source_identity_gate_failure
  - sample_independence_review_hold
  - prior analysis of exact sample discovered before outcome computation
  - minimum source or sample completeness failure
relations:
  - type: tests_hypothesis
    target: HYP-HR-003
---

# Confirmation Selection Effect — Post-H2 frozen specification

## Source

[Horizontal Reaction — Confirmation Selection Effect Preregistration — Post-H2 v1](https://docs.google.com/document/d/1GRa035N5FX3F59_wM2T11VFuv3aL85YZghmvaCeTJ0g/edit), frozen 2026-09-23 before outcome access. The source-preparation state is documented in [Confirmation Selection Effect Source Preparation Handoff v1](https://docs.google.com/document/d/1QPwXqAcp1fzPm6VXelMLDMyist02-sSSDQ1lkrpsoSg/edit), latest retrieved revision `ANLCKQl7GEONhGA6zeB6JVcxlC2p-3TWmWIb_bk3Q_ztIeCaHDt7jNrYaz14mQrnpGeF8wkbSuXU377S5mDS1k1eM7MX45WSDr5gUI54BwA`.

## Sample and source

- Candidate start: 2026-07-10 UTC, after the consumed 2026H2 unconditional-touch sample ending 2026-07-09.
- Scan weekdays in ascending order; freeze the first 60 structurally eligible UTC trading weekdays.
- As of the source-preparation handoff (2026-09-23), 54 Monday-Friday calendar dates had elapsed. Earliest possible maturity was 2026-10-01 if the next six weekdays all pass the frozen structural gate; maturity is not guaranteed.
- Signal: Dukascopy first-party XAU/USD BID M1 UTC.
- Outcome/path: Dukascopy first-party raw BID/ASK Tick UTC.
- No alternate provider, broker history, midpoint-only replacement, chart export, interpolation, synthetic quote, or reconstructed price.

## Population, classification, and outcome

- Use the unchanged exact pre-confirmation first-touch generator and existing fresh-approach logic.
- Include every eligible touch whether or not it later confirms, signals, enters, is blocked by a position, or produces a trade.
- Classify each eligible touch under the original v0.1 confirmation rule as `CONFIRMED` or `UNCONFIRMED`. Execution availability and trade status do not change classification.
- Use the existing D4 direction-aware touch-to-+15-completed-minute bps outcome and quote-side convention.
- Required unavailable endpoints are counted with reasons and not imputed.

## Primary estimand and inference

`PRIMARY_CONTRAST = mean(outcome | CONFIRMED) - mean(outcome | UNCONFIRMED)`.

Use a 60-session cluster bootstrap with 10,000 replications and frozen seed `20260913`. Primary output is the 95% percentile interval for the contrast.

Frozen labels:

- `CONFIRMATION_SELECTION_EFFECT_SUPPORTED`: lower bound > 0.
- `NO_CONFIRMATION_SELECTION_EFFECT_SUPPORT`: upper bound <= 0.
- `INCONCLUSIVE`: neither condition, or minimum source/sample completeness fails.

## Maturity, source gate, and outcome-access boundary

The source-preparation handoff reports `WAITING_FOR_MATURITY`. Until the 60th structurally eligible session is frozen and the source gate passes, do not compute or view touch outcomes, compare CONFIRMED vs UNCONFIRMED outcomes, calculate the primary contrast, or run/view bootstrap output.

Before outcomes, permitted work is limited to source/sample identity checks, first-party acquisition and hash manifests, structural eligibility, freezing the 60-session list, and outcome-blind calculation-code preparation.

The selection outcome, group comparison, and bootstrap are forbidden until both maturity and source-gate conditions pass.

## Forbidden rescue

No session substitution, post-outcome date exclusion, threshold/horizon/confirmation change, subset search, parameter sweep, imputation, provider substitution, broker access, or live trading action.
