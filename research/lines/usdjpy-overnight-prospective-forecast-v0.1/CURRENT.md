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


## Operational preparation status

- Exploratory weekly dry run for 2026-10-05 through 2026-10-09: RECORDED / NOT_IN_COHORT.
- Dry-run full-system-style view: p_week_up 0.45, point forecast -15 bps, LOW_TO_MEDIUM confidence; this is not WA3 and has no scientific promotion effect.
- Deterministic helper implementation: COMPLETE_FOR_CANDIDATE.
- Synthetic helper tests: 19/19 PASS; no market data used.
- Fed / BOJ / U.S. Treasury / official calendar source routes: partially qualified for the fundamental layer.
- Dukascopy reference-feed bounded raw sample: BLOCKED_PENDING_RETRIEVAL.
- Durable news snapshot contract: PARTIAL / NOT_FROZEN.
- Formal scored start: BLOCKED.
- Earliest clean weekly cohort candidate remains Sunday 2026-10-11 cutoff, only if human freeze and all readiness gates pass first.

See:

- `work/EXPLORATORY_WEEKLY_DRY_RUN_2026-10-04.md`
- `work/SOURCE_READINESS_2026-10-04.md`
- `work/SOURCE_READINESS_UPDATE_2026-10-04_IMPLEMENTATION.md`
- `work/implementation/forecast_core.py`
- `work/implementation/test_forecast_core.py`
- `work/packets/PACKET_SOURCE_DUKASCOPY_REFERENCE_GATE.md`


## Live Market State Journal

- **Protocol:** `OBS-USDJPY-LIVE-STATE-001-v01`
- **Status:** ACTIVE_OBSERVATIONAL.
- **Scientific effect:** NONE.
- **Scored forecast authority:** NONE.
- **Default checkpoints:** 08:30, 15:00, 21:30 JST.
- **Additional checkpoints:** EVENT_DRIVEN / MANUAL.
- **History rule:** append-only; corrections are new entries.
- **Benchmark boundary:** journal entries cannot overwrite forecasts, cannot retroactively supply post-cutoff information, and cannot replace canonical scored-input snapshots.
- **Challenger role:** journal observations may motivate separately versioned exploratory challengers.
- **Initial entry:** `observations/entries/20261005T011400+0900_MANUAL.json`.
- **Initial state:** weekend market closed; pre-open baseline only; noncanonical prior-Friday price context explicitly labeled.
- **Validator:** 12/12 synthetic tests PASS.

See:

- `observations/LIVE_MARKET_STATE_JOURNAL_v0.1.md`
- `observations/README.md`
- `observations/STATE_ENTRY_TEMPLATE_v0.1.json`
- `decisions/HDEC-USDJPY-LIVE-JOURNAL-001_2026-10-05.md`
- `work/implementation/live_state_journal.py`


## Latest live observation

- **State:** `STATE-USDJPY-20261008T075200+0900-MANUAL`
- **Observed:** 2026-10-08 07:52 JST.
- **USD/JPY:** NY close 158.04-158.14; 05:48 quote 158.07-158.09; exact qualified 07:52 quote unavailable.
- **FOMC minutes:** most participants saw another hike this year as likely appropriate, but views on the path remained divided.
- **U.S. rates:** 10Y retreated toward ~5.28-5.29% after a strong 10-year auction; 2Y ~4.762%.
- **Oil:** Brent settled ~100.20 / WTI ~88.28 after IEA reserve-release news.
- **Forecast relation:** `p_up=0.55 / +6 bps / SLIGHT_USDJPY_UP` is under pressure and currently appears more likely to finish directionally wrong.
- **Final result:** PENDING until 08:00; no formal score without the qualified reference feed.
- **Working state:** NEUTRAL_TO_SLIGHT_USDJPY_DOWN into endpoint, LOW_TO_MEDIUM confidence.
- **Scientific effect:** NONE; journal only.

## Latest overnight forecast event

- **Event:** `XPF-EVENT-USDJPY-20261006-220000`
- **Status:** NO_FORECAST_ISSUED_CUTOFF_PASSED.
- **Reason:** at 22:18, post-cutoff information was already available; issuing a 22:00 forecast would violate prospective/outcome-blind timing.
- **Forecast values:** NOT_APPLICABLE.
- **Benchmark effect:** NONE.
- **Operational interpretation:** MISSED_CUTOFF_NEGATIVE_OPERATIONAL_RESULT.

## Latest exploratory overnight evaluation

- **Evaluation:** `XEV-USDJPY-20261005-215400`
- **Forecast:** `p_up=0.53 / +4 bps / SLIGHT_USDJPY_UP`.
- **Status:** INDICATIVE_DIRECTIONAL_MISS_FORMAL_SCORE_UNAVAILABLE.
- **Indicative public-price return:** roughly -13 to -19 bps using 158.10-158.20 near-start and ~157.90 near-end observations.
- **Indicative point-forecast error:** roughly 17 to 23 bps.
- **Illustrative only if Y_up=0 is later confirmed:** Brier 0.2809 vs neutral 0.2500, delta +0.0309.
- **Research lesson:** elevated U.S. yields did not translate into sustained USDJPY upside; preserve this as a challenger diagnostic, not a reason to rewrite v0.1.
- **Benchmark effect:** NONE_NOT_IN_COHORT.
## Latest exploratory overnight forecast

- **Forecast:** `XPF-USDJPY-20261007-214634`
- **Status:** EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT.
- **Issued:** 2026-10-07 21:46:34 JST.
- **Information cutoff:** 2026-10-07 21:46:34 JST.
- **Nominal target:** 22:00 JST → 08:00 JST.
- **p_up:** 0.55.
- **Point forecast:** +6 bps.
- **Direction:** SLIGHT_USDJPY_UP.
- **Confidence:** LOW.
- **Main support:** elevated U.S. long yields, oil back above $100, broad-dollar firmness, USDJPY resilience after the afternoon dip.
- **Main counterevidence:** 158.5 resistance, higher JGB yields, intervention sensitivity near 159, and FOMC-minutes event risk.
- **Protocol deviation:** issued 13m26s before nominal cutoff and qualified reference feed remains unavailable; not eligible for frozen benchmark.
- **Post-cutoff FOMC/credit results:** forbidden as forecast inputs; may be used only in later error attribution.
