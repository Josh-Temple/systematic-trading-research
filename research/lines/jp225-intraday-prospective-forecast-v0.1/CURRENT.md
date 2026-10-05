---
type: CurrentProjection
research_line_id: RL-JP225-PROSPECTIVE-001
projection_generated_at: 2026-10-05
derived_from_decisions: []
derived_from_interpretations: []
---

# Current projection — JP225 prospective forecast Phase 0

- Scientific status: UNTESTED.
- Specification: `SPEC-JP225-FORECAST-001-v01` is PROPOSED_NOT_FROZEN.
- Prospective scored outcome access: CLOSED.
- Scored v0.1 forecast issuance: NOT_AUTHORIZED.
- Exploratory prospective dry runs: PERMITTED if clearly NOT_IN_COHORT.
- Live/paper broker action: NOT_AUTHORIZED.

## Candidate benchmark

- scheduled JPX cash-equity trading days;
- 09:00 JST forecast cutoff / start;
- 15:30 JST endpoint;
- exact XM MT5 `JP225Cash` Bid/Ask midpoint reference;
- B0 / A1 / A2 / A3 comparison family;
- Brier score primary;
- 60 matched valid events;
- challenger reviews after 20 and 40 matched events.

## Fresh-read relationship to existing JP225 research

At main `40c1a04b793622d30e42fc298ef6a138407d46fa`:

- `jp225-ema-timeofday-v0.1` is WAITING_FOR_XM_STAGE1_DATA; exact XM outcomes remain untested.
- exact XM MT5 `JP225Cash` is the current free-source priority.
- Dukascopy `JPN.IDX/JPY` is not accepted as an exact JP225 substitute.
- JPX/J-Quants DataCube is deferred under the no-paid-data policy.
- PR #59's separate DataCube/intraday-momentum line is preserved but quarantined/deferred and must not be treated as outcome-unviewed evidence.

## Earliest operational use

The next scheduled JPX trading day may be used for an exploratory prospective dry run if the forecast can be frozen using only pre-cutoff information.

It must not enter the 60-event scored cohort unless the full source/readiness gate has passed before that event.

If exact XM endpoint quotes are unavailable, preserve the forecast and mark the result unavailable. Do not backfill the same event later from another provider.

## Next action

1. Complete the bounded XM/live-input readiness check without inspecting future outcomes for specification selection.
2. Run deterministic synthetic tests for timing, quote tolerance, scoring, missingness, and future-information rejection.
3. Operate exploratory forecast/review dry runs while readiness remains incomplete.
4. Freeze/activate the scored v0.1 cohort only after explicit human acceptance of the exact specification and readiness PASS.
