---
type: CurrentProjection
research_line_id: RL-USDJPY-OVERNIGHT-001
projection_generated_at: 2026-10-04
derived_from_decisions: []
derived_from_interpretations: []
---

# Current projection — dual-horizon Phase 0 candidate awaiting human freeze

- **Scientific status:** UNTESTED.
- **Overnight specification:** `SPEC-USDJPY-FORECAST-001-v01` is PROPOSED_NOT_FROZEN.
- **Weekly specification:** `SPEC-USDJPY-WEEKLY-001-v01` is PROPOSED_NOT_FROZEN.
- **Prospective outcome access:** CLOSED for both horizons.
- **Scored forecast issuance:** NOT_AUTHORIZED for both horizons.
- **Live/paper broker action:** NOT_AUTHORIZED.

## Overnight candidate

- Monday–Thursday at 22:00 JST → 08:00 JST next calendar day.
- Candidate reference outcome: qualified USD/JPY best Bid/Ask midpoint-to-midpoint log return.
- Candidate benchmark cohort: 60 matched valid events.
- Primary comparison: A3 full system versus A1 market-only.
- Baseline sanity: A3 versus B0 neutral.
- Research-layer comparison: A3 versus A2 market + fundamentals/news.
- Challenger reviews: after matched events 20 and 40; frozen v0.1 continues unchanged to 60.

## Weekly candidate

- Sunday 20:00 JST forecast cutoff.
- Target interval: Monday 08:00 JST → Friday 22:00 JST.
- Candidate reference outcome: qualified USD/JPY best Bid/Ask midpoint-to-midpoint weekly log return.
- Candidate benchmark cohort: 26 matched valid weeks.
- Primary comparison: WA3 full weekly system versus WA1 weekly market-only.
- Baseline sanity: WA3 versus WB0 neutral.
- Research-layer comparison: WA3 versus WA2 weekly market + fundamentals/news.
- Challenger reviews: after matched weeks 9 and 18; frozen v0.1 continues unchanged to 26.

## Cross-horizon isolation

- weekly forecast output is not a permitted input to overnight A1/A2/A3 v0.1;
- overnight forecasts do not rewrite the Sunday weekly forecast;
- future agreement/disagreement analysis is exploratory unless separately preregistered.

## Related fresh-read research state

These refs were inspected during Phase 0 design and are not automatically promoted to evidence for this line:

- `research/currency-strength-momentum-v0.1` at observed branch head `4b0a6e54f7186308c2e9b1e14a6605fae018c42e`: HYP-CSM-001 UNTESTED; current projection says no market outcome has been calculated.
- `research/fx-monetary-policy-alignment-v0.1` at observed branch head `c87756ba807cc39fd52476e8fc60c78e4f9f0831`: specification frozen, hypothesis UNTESTED, market-outcome gate blocked by an upstream dependency.
- `research/fx-daily-breakout-20261003` at observed branch head `7d51437181c338428134ec6adcd658de38e4faaf`: USD/JPY reference-feed architecture is only partially qualified and requires bounded source retrieval before outcome use.

## Next admissible action

Human review of each exact Phase 0 candidate plus source/readiness qualification.

Until both requirements pass for a horizon:

- do not issue a scored forecast for that horizon;
- do not inspect future outcomes under that protocol for specification selection;
- do not call any current research hypothesis a proven predictor;
- do not create a trading decision rule from the proposal.
