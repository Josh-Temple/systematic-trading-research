---
type: CurrentProjection
research_line_id: RL-USDJPY-OVERNIGHT-001
projection_generated_at: 2026-10-04
derived_from_decisions: []
derived_from_interpretations: []
---

# Current projection — Phase 0 candidate awaiting human freeze

- **Scientific status:** UNTESTED.
- **Specification:** `SPEC-USDJPY-FORECAST-001-v01` is PROPOSED_NOT_FROZEN.
- **Prospective outcome access:** CLOSED.
- **Scored forecast issuance:** NOT_AUTHORIZED.
- **Live/paper broker action:** NOT_AUTHORIZED.
- **Candidate event:** Monday–Thursday at 22:00 JST, horizon to 08:00 JST next calendar day.
- **Candidate reference outcome:** Dukascopy USD/JPY best Bid/Ask ticks; midpoint-to-midpoint log return, subject to a line-specific source/readiness gate.
- **Candidate minimum evaluation cohort:** 60 eligible frozen-v0.1 events.
- **Daily behavior:** snapshot → forecast → immutable record → outcome → deterministic score → error attribution.
- **Update behavior:** frozen v0.1 systems remain unchanged through the cohort; adaptive improvements may exist only as separately versioned challengers.
- **Primary candidate comparison:** full market + fundamentals + status-preserving research AI versus market-only AI.
- **Baseline sanity comparison:** full AI versus neutral `p_up=0.50`, zero-return baseline.
- **Key secondary comparison:** full AI versus market + fundamentals AI.

## Related fresh-read research state

These refs were inspected while drafting Phase 0 and are not automatically promoted to evidence for this line:

- `research/currency-strength-momentum-v0.1` at observed branch head `4b0a6e54f7186308c2e9b1e14a6605fae018c42e`: current projection says HYP-CSM-001 is UNTESTED and no market outcome has been calculated.
- `research/fx-monetary-policy-alignment-v0.1` at observed branch head `c87756ba807cc39fd52476e8fc60c78e4f9f0831`: specification frozen, hypothesis UNTESTED, market-outcome gate blocked by an upstream dependency.
- `research/fx-daily-breakout-20261003` at observed branch head `7d51437181c338428134ec6adcd658de38e4faaf`: USD/JPY reference-feed architecture is only partially qualified and requires bounded source retrieval before outcome use.

## Next admissible action

Human review of the exact Phase 0 candidate plus source/readiness qualification.

Until both are complete:

- do not issue a scored v0.1 forecast;
- do not inspect future outcomes under this protocol;
- do not call any current research hypothesis a proven predictor;
- do not create a trading decision rule from this proposal.
