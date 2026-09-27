---
type: CurrentProjection
research_line_id: RL-HR-001
projection_generated_at: 2026-09-28
derived_from_decisions:
  - DEC-HR-001
  - DEC-HR-002
  - DEC-HR-003
  - DEC-HR-004
derived_from_interpretations:
  - INT-HR-002
  - INT-HR-003
---

# Current State

## Current scientific status

- **HYP-HR-001 / v0.1 execution-aware strategy:** the frozen execution-aware implementation was not supported on the consumed 2026H1 sample (`RES-HR-001`). The current integrated H1 diagnostic label recorded by `INT-HR-002` is `MULTIPLE_DRIVERS / INCONCLUSIVE`; the supporting source reports conflict remains unresolved in `RES-HR-005` and `DIAG-HR-003`.
- **HYP-HR-002 / unconditional touch:** the preregistered 2026H2 fixed-sample result is `NO_UNCONDITIONAL_TOUCH_SUPPORT` (`RES-HR-006`, `INT-HR-003`). This concerns the defined touch-to-+15-minute price-reaction test; it is not a profitability or universal-absence claim.
- **HYP-HR-003 / confirmation selection effect:** preregistered and frozen, and still `WAITING_FOR_MATURITY`. There is no Run or Result and no outcome access for this test (`SPEC-HR-003-v01`, `EXP-HR-007`, `DEC-HR-003`). `DEC-HR-004` freezes the implementation reference outcome-blind to the exact recovered H2 legacy generator while preserving the Gamma temporal-information mismatch as an explicit interpretation limitation.

## Current interpretation

- `INT-HR-002` is the current integrated H1 interpretation and supersedes `INT-HR-001`; it preserves the source discrepancy rather than adjudicating it.
- `INT-HR-003` records the 2026H2 unconditional-touch interpretation under its own hypothesis and frozen sample.
- No scientific interpretation exists yet for the Post-H2 confirmation-selection test.

## Active specification

- `SPEC-HR-001-v01` remains the frozen v0.1 specification. It does not permit same-sample rescue.
- `SPEC-HR-002-v01` governed the completed 2026H2 unconditional-touch test; its dataset is consumed.
- `SPEC-HR-003-v01` is the active preregistration for the next test, currently waiting for 60 structurally eligible sessions and a passing source gate. `DEC-HR-004` does not rewrite that frozen specification; it resolves its external implementation reference to exact `run_v01.py` SHA-256 `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`.

## Consumed data boundaries

- `DATA-HR-001`: the 2026H1 sample is `CONSUMED_HOLDOUT`; do not reuse it for new subset, threshold, parameter, horizon, or rule selection.
- `DATA-HR-002`: the separate 2026H2 unconditional-touch sample is `CONSUMED_HOLDOUT`; do not reuse it for tuning or trading-rule design.
- `DATA-HR-003`: the Post-H2 candidate sample is `FINAL_HOLDOUT`, `UNUSED`, and not yet fully identified or frozen. Preserve that role; do not mark it consumed.

## Current next test

Continue only outcome-blind preparation for `EXP-HR-007`: first-party source/sample identity checks, raw M1/Tick acquisition and hash readback, frozen structural eligibility, and freezing the first 60 eligible sessions. For generator state, retain the exact H2 135-file M1 prefix through 2026-07-09 and append later first-party BID M1 source chronologically without resetting expanding Gamma. For H3 binary classification, apply the original confirmation condition before the legacy same-confirmation-bar execution-ambiguity filter. The source-preparation handoff's earliest possible maturity was 2026-10-01, conditional on the next six weekdays passing the structural gate. Run the existing preregistration once only after all 60 sessions are frozen and every source gate passes.

## Forbidden reuse / rescue

- No same-sample rescue, parameter, threshold, subset, horizon, confirmation-delay, stop, target, or filter search on `DATA-HR-001` or `DATA-HR-002`.
- Do not compute or view `DATA-HR-003` touch outcomes, compare CONFIRMED with UNCONFIRMED outcomes, calculate the primary contrast, or run/view the bootstrap before both the 60-session maturity and source-gate conditions pass.
- Do not substitute providers, impute missing prices, connect to a broker, or place live trades.

## Invalid / superseded evidence that must not be treated as current

- `RES-HR-002` is source qualification only; D1-D5 were deliberately `NOT_RUN` in that work.
- `RES-HR-003` is a blocked D1-D5 replay attempt with all diagnostics `NOT_RUN`; it is not negative strategy evidence.
- `RES-HR-004` is an exploratory ledger diagnostic on the consumed H1 sample; its same-timestamp midpoint exercise is not formal D5.
- `RES-HR-006-ATTEMPT-1` is the earlier fail-closed H2 source-gate attempt; no touch outcomes were computed and no statistical result label was reached.
- `INT-HR-001` is superseded by `INT-HR-002`; the source discrepancy documented in `RES-HR-005` remains open.

## Projection conflicts

`RES-HR-005` and `DIAG-HR-003` preserve a conflict between the 2026-09-13 Data D1-D5 replay and the 2026-09-23 diagnostic report / Project Brief. They disagree on D2-D5 endpoint counts, estimates, and classification (`EDGE_LOST_BEFORE_ENTRY` versus `MULTIPLE_DRIVERS / INCONCLUSIVE`). Both are exploratory records on the consumed 2026H1 sample. This projection does not resolve that discrepancy.


## H3 implementation identity boundary

`DEC-HR-004` resolves the pre-outcome implementation blockers operationally without erasing the underlying prose/code conflict:

- H3 uses the exact recovered legacy H2 generator bytes, including candidate-bar-dependent expanding Gamma.
- The exact H2 generator input through 2026-07-09 is the fixed prefix; later valid first-party BID M1 source is appended chronologically before selected-session filtering, with no history reset.
- Same-confirmation-bar dual confirmations remain `CONFIRMED` for H3's confirmation classification because the later clean-list removal is an execution-ambiguity filter.
- Any eventual H3 result must not be described as evidence that the generator is temporal-leakage-free or directly live-executable.

These points do not open `DATA-HR-003`; maturity and source gates remain controlling.
