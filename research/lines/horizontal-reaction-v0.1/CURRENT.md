---
type: CurrentProjection
research_line_id: RL-HR-001
projection_generated_at: 2026-09-27
derived_from_decisions:
  - DEC-HR-001
  - DEC-HR-002
  - DEC-HR-003
derived_from_interpretations:
  - INT-HR-002
  - INT-HR-003
---

# Current State

## Current scientific status

- **HYP-HR-001 / v0.1 execution-aware strategy:** the frozen execution-aware implementation was not supported on the consumed 2026H1 sample (`RES-HR-001`). The current integrated H1 diagnostic label recorded by `INT-HR-002` is `MULTIPLE_DRIVERS / INCONCLUSIVE`; the supporting source reports conflict remains unresolved in `RES-HR-005` and `DIAG-HR-003`.
- **HYP-HR-002 / unconditional touch:** the preregistered 2026H2 fixed-sample result is `NO_UNCONDITIONAL_TOUCH_SUPPORT` (`RES-HR-006`, `INT-HR-003`). This concerns the defined touch-to-+15-minute price-reaction test; it is not a profitability or universal-absence claim.
- **HYP-HR-003 / confirmation selection effect:** scientific status remains preregistered/frozen and `WAITING_FOR_MATURITY`. There is no Run or Result and no outcome access for this test (`SPEC-HR-003-v01`, `EXP-HR-007`, `DEC-HR-003`). A separate pre-execution code audit now records an unresolved Gamma specification/implementation conflict, so maturity alone is not sufficient to authorize execution.

## Current interpretation

- `INT-HR-002` is the current integrated H1 interpretation and supersedes `INT-HR-001`; it preserves the source discrepancy rather than adjudicating it.
- `INT-HR-003` records the 2026H2 unconditional-touch interpretation under its own hypothesis and frozen sample.
- No scientific interpretation exists yet for the Post-H2 confirmation-selection test.

## Active specification

- `SPEC-HR-001-v01` remains the frozen v0.1 specification. It does not permit same-sample rescue.
- `SPEC-HR-002-v01` governed the completed 2026H2 unconditional-touch test; its dataset is consumed.
- `SPEC-HR-003-v01` is the active preregistration for the next test, currently waiting for 60 structurally eligible sessions and a passing source gate.

## Pre-execution implementation-integrity conflict

A fresh read of the exact historical `run_v01.py` recovered from the persistent Source Pack produced SHA-256 `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`, exactly matching the stored manifest. The executed `build_session_events()` path calculates Gamma from an expanding absolute-Close-change prefix that includes the current candidate bar Close. This conflicts with `SPEC-HR-001-v01`, `SPEC-HR-002-v01`, and the H1 Execution Result description that Gamma uses observations strictly before the candidate minute.

H2 explicitly reused this recovered generator. This projection does not retroactively reclassify H1 or H2, but it does not treat exact frozen-spec implementation fidelity as established while the conflict remains open.

For H3, there is no safe automatic choice between preserving the historical code and changing Gamma to match the frozen prose. In addition, the reviewed sources do not yet specify how the historical same-confirmation-bar ambiguity case maps into H3's required binary `CONFIRMED` / `UNCONFIRMED` groups. See [H3 execution identity precheck](H3_EXECUTION_IDENTITY_PRECHECK_2026-09-27.md).

Until a versioned decision resolves these points, H3 outcome computation is not execution-ready. `DATA-HR-003` remains `FINAL_HOLDOUT / UNUSED`; no H3 outcome was accessed by this audit.

## Consumed data boundaries

- `DATA-HR-001`: the 2026H1 sample is `CONSUMED_HOLDOUT`; do not reuse it for new subset, threshold, parameter, horizon, or rule selection.
- `DATA-HR-002`: the separate 2026H2 unconditional-touch sample is `CONSUMED_HOLDOUT`; do not reuse it for tuning or trading-rule design.
- `DATA-HR-003`: the Post-H2 candidate sample is `FINAL_HOLDOUT`, `UNUSED`, and not yet fully identified or frozen. Preserve that role; do not mark it consumed.

## Current next test

Continue only outcome-blind preparation for `EXP-HR-007`: first-party source/sample identity checks, raw M1/Tick acquisition and hash readback, frozen structural eligibility, and freezing the first 60 eligible sessions. The source-preparation handoff's earliest possible maturity was 2026-10-01, conditional on the next six weekdays passing the structural gate. Even after maturity and source-gate PASS, do not run H3 until the Gamma specification/implementation conflict and binary confirmation-classification ambiguity recorded in `H3_EXECUTION_IDENTITY_PRECHECK_2026-09-27.md` are resolved by a versioned decision.

## Forbidden reuse / rescue

- No same-sample rescue, parameter, threshold, subset, horizon, confirmation-delay, stop, target, or filter search on `DATA-HR-001` or `DATA-HR-002`.
- Do not compute or view `DATA-HR-003` touch outcomes, compare CONFIRMED with UNCONFIRMED outcomes, calculate the primary contrast, or run/view the bootstrap before the 60-session maturity and source-gate conditions pass **and** the recorded H3 implementation/specification conflict is resolved.
- Do not substitute providers, impute missing prices, connect to a broker, or place live trades.

## Invalid / superseded evidence that must not be treated as current

- `RES-HR-002` is source qualification only; D1-D5 were deliberately `NOT_RUN` in that work.
- `RES-HR-003` is a blocked D1-D5 replay attempt with all diagnostics `NOT_RUN`; it is not negative strategy evidence.
- `RES-HR-004` is an exploratory ledger diagnostic on the consumed H1 sample; its same-timestamp midpoint exercise is not formal D5.
- `RES-HR-006-ATTEMPT-1` is the earlier fail-closed H2 source-gate attempt; no touch outcomes were computed and no statistical result label was reached.
- `INT-HR-001` is superseded by `INT-HR-002`; the source discrepancy documented in `RES-HR-005` remains open.

## Projection conflicts

`RES-HR-005` and `DIAG-HR-003` preserve a conflict between the 2026-09-13 Data D1-D5 replay and the 2026-09-23 diagnostic report / Project Brief. They disagree on D2-D5 endpoint counts, estimates, and classification (`EDGE_LOST_BEFORE_ENTRY` versus `MULTIPLE_DRIVERS / INCONCLUSIVE`). Both are exploratory records on the consumed 2026H1 sample. This projection does not resolve that discrepancy.
