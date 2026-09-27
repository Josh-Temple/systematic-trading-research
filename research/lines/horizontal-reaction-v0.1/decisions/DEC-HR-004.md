---
id: DEC-HR-004
type: Decision
research_line_id: RL-HR-001
created_at: 2026-09-28
based_on:
  - SPEC-HR-001-v01
  - SPEC-HR-003-v01
  - RUN-HR-006
decision: FREEZE_H3_IMPLEMENTATION_IDENTITY_OUTCOME_BLIND
reason: H3 explicitly inherits the exact H2 pre-confirmation first-touch generator unchanged. The recovered generator and H2 input identity make that external reference byte-identifiable. Preserve the legacy implementation rather than silently converting H3 into a corrected specification, while keeping the temporal-information mismatch explicit as an interpretation limitation.
effect_on_current_state:
  experiment_EXP-HR-007: WAITING_FOR_MATURITY
  dataset_DATA-HR-003: FINAL_HOLDOUT_UNCONSUMED
  implementation_identity: FROZEN
next_allowed_actions:
  - continue outcome-blind source and structural preparation
  - use exact run_v01.py SHA-256 9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd
  - preserve the exact H2 generator-input prefix through 2026-07-09 and append later first-party BID M1 source chronologically without reset
  - after maturity and source-gate PASS, classify confirmation before execution-ambiguity filtering
  - run the frozen H3 preregistration once only after all existing gates pass
forbidden_actions:
  - patch Gamma to strict-before semantics inside SPEC-HR-003-v01
  - reset or re-origin Gamma history at 2026-07-10
  - select generator history using DATA-HR-003 touch, confirmation, or return outcomes
  - map same-confirmation-bar events to UNCONFIRMED merely because the legacy execution list removes them
  - compute or view H3 touch outcomes, group contrasts, or bootstrap before maturity and source-gate PASS
  - use any H3 outcome to revise this implementation identity
relations:
  - type: derived_from
    target: SPEC-HR-003-v01
  - type: derived_from
    target: RUN-HR-006
---

# Decision — freeze H3 legacy implementation identity before outcome access

## Scope

This decision resolves the three implementation-identity blockers recorded in
`H3_IMPLEMENTATION_IDENTITY_AUDIT_2026-09-28.md` without accessing or computing
`DATA-HR-003` outcomes.

It does not change the H3 sample, event horizon, confirmation threshold, outcome,
bootstrap seed, decision rule, or source provider. It does not authorize an H3 run.
`EXP-HR-007` remains `WAITING_FOR_MATURITY`.

## 1. Gamma semantics

`SPEC-HR-001-v01` says candidate-minute calculations use observations strictly
before the candidate minute. The exact historical H1/H2 generator used by the H2
replication does not satisfy that prose: its expanding Gamma prefix includes the
Close change ending at the candidate bar.

H3, however, explicitly freezes the **exact pre-confirmation first-touch generator
used by the 2026H2 replication** and says to use it unchanged.

For H3 v0.1, implementation identity therefore follows the recovered legacy
generator bytes:

- file: `run_v01.py`
- SHA-256:
  `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`
- Gamma implementation:
  `abs_change_prefix[global_i] / (global_i - 1)`

No strict-before Gamma correction is made inside this frozen H3 experiment.

The prose/code mismatch remains a real limitation. Any eventual H3 result is
evidence about the selection behavior of this legacy generator, not evidence that
the event definition is free of temporal leakage or is directly implementable in
real time. A strict-before Gamma version would be a new specification/version and
would require its own unused evaluation sample.

## 2. Generator-history origin

Because legacy Gamma is expanding-history, reproducing H3 requires a fixed history
origin.

The exact H2 generator-input identity is the frozen prefix:

- 135 M1 files;
- first context date: 2025-12-31;
- last H2 selected session: 2026-07-09;
- 75 pre-touch context files plus 60 H2 selected sessions.

For H3 source preparation, this exact H2 prefix is retained unchanged. Starting
after 2026-07-09, every valid first-party Dukascopy BID M1 source file acquired for
the chronological candidate scan is appended in timestamp order **before**
selected-session filtering. The cumulative Gamma state is not reset at
2026-07-10.

A date may still fail the frozen structural/source gate. Missing or invalid source
is not imputed. History inclusion is never chosen using touch identity,
confirmation status, +15-minute return, group contrast, or any other H3 outcome.

This is an implementation-continuation rule required by the already frozen
reference to the exact H2 generator; it is not a new parameter search.

## 3. Same-confirmation-bar classification

The recovered generator has two distinct layers:

1. a pending interaction mechanically satisfies the v0.1 confirmation condition
   and is appended to the internal confirmation-event list;
2. after that, confirmations sharing one confirmation-bar timestamp are removed
   from the clean execution-event list as
   `both_confirmations_same_bar` execution ambiguity.

H3 is not an execution replay. Its preregistration says:

- every eligible touch must be classified `CONFIRMED` or `UNCONFIRMED`;
- primary classification follows the original confirmation rule;
- execution availability, open-position constraint, and whether a trade occurred
  do not change primary classification.

Therefore, for H3 classification, a touch is `CONFIRMED` when its pending
interaction mechanically satisfies the original confirmation close condition,
including when another touch confirms on the same confirmation bar. The later
execution-ambiguity filter is not used to turn such a touch into
`UNCONFIRMED`.

The same-confirmation-bar occurrence may be recorded separately for auditability,
but it does not change the binary H3 classification.

## 4. Remaining gates

This decision resolves implementation identity only.

Before any H3 outcome access, the existing frozen gates still apply:

- first 60 structurally eligible sessions must be frozen;
- first-party M1/Tick source identity must pass;
- exact sample/source hashes must be persisted and read back;
- no prior analysis of the exact H3 outcome may be discovered;
- bootstrap seed remains `20260913`, 10,000 replications;
- no touch-to-+15m outcome, group comparison, primary contrast, or bootstrap may
  be computed or viewed before the gates pass.

`DATA-HR-003` remains `FINAL_HOLDOUT / UNUSED`.
