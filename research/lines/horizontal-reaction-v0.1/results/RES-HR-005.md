---
id: RES-HR-005
type: Result
research_line_id: RL-HR-001
run_id: RUN-HR-005
observed_at: UNKNOWN
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: EXPLORATORY
headline_metrics:
  current_integrated_report:
    d1_n: 2685
    d1_touch_to_entry_mean_R: 0.331
    d4_n: 2683
    d4_touch_to_15m_mean_R: 0.125
    d2_n: 2683
    d2_entry_to_15m_mean_R: -0.205
    d2_session_clustered_95_ci_R: [-0.304, -0.114]
    d3_n: 1402
    d3_population: 1404
    d3_entry_to_15m_mean_R: -1.034
    stopped_trades_recross_entry_within_15m_pct: 54.7
    same_exit_timestamp_midpoint_gross_mean_R: -0.0413
    same_exit_timestamp_bid_ask_net_mean_R: -0.2016
    same_exit_timestamp_spread_drag_mean_R: 0.1603
    formal_d5_n: 2683
    formal_d5_midpoint_mean_bps: -0.708
    formal_d5_midpoint_95_ci_bps: [-1.896, 0.299]
    formal_d5_spread_drag_mean_bps: 1.782
    formal_d5_spread_drag_95_ci_bps: [1.658, 1.928]
    current_classification_in_project_brief: MULTIPLE_DRIVERS / INCONCLUSIVE
  earlier_2026_09_13_data_replay_source:
    d1_n: 2685
    d1_mean_R: 0.3307
    d2_n: 2685
    d2_mean_R: -0.2011
    d3_n: 1404
    d3_mean_R: -1.0260
    d4_n: 2685
    d4_mean_R: 0.1281
    d5_n: 2685
    d5_spread_drag_mean_bps: 1.783
    classification: EDGE_LOST_BEFORE_ENTRY
  source_discrepancy: PRESENT_UNRESOLVED
artifact_refs:
  - https://drive.google.com/file/d/1ODFl8jxY676iMfrRAPlMyqHSFjfAeUTD/view
  - https://docs.google.com/document/d/1MreVcFJUz5sDu2w9-qdIAX7D2lGZ5aKeDoQZozZLHE4/edit
  - https://docs.google.com/document/d/1GMuRnL6ZPa_OR2tVY85dQujjk0EmgdJeOBsdbLytBnE/edit
diagnostic_refs:
  - DIAG-HR-003
relations:
  - type: produced_by_run
    target: RUN-HR-005
  - type: derived_from
    target: DATA-HR-001
---

# Successful exploratory D1-D5 diagnostic result — source discrepancy preserved

## Current integrated report (2026-09-23 report and Project Brief)

The report gives:

- D1 touch-to-entry: n=2,685; mean +0.331R.
- D2 entry-to-15-minute, no barrier: n=2,683; mean -0.205R; session-clustered 95% CI [-0.304, -0.114].
- D3 stopped-trade +15-minute counterfactual: n=1,402 of 1,404; mean -1.034R; 54.7% of stopped trades recrossed entry within 15 minutes.
- D4 touch-to-15-minute, no barrier: n=2,683; mean +0.125R.
- Formal D5: n=2,683; matched midpoint mean -0.708 bps; 95% CI [-1.896, 0.299]; spread drag +1.782 bps; 95% CI [+1.658, +1.928].

The same report separately gives a same-actual-exit timestamp midpoint mean of -0.0413R, BID/ASK net mean -0.2016R, and difference +0.1603R. It explicitly distinguishes that comparison from formal D5.

The report's current integrated classification, repeated in the Project Brief, is `MULTIPLE_DRIVERS / INCONCLUSIVE`. It describes post-entry path deterioration and spread cost together, and does not make a single-driver causal claim.

## Earlier source record (2026-09-13)

The separate [Data D1-D5 Exploratory Diagnostic Replay](https://docs.google.com/document/d/1MreVcFJUz5sDu2w9-qdIAX7D2lGZ5aKeDoQZozZLHE4/edit) reports:

- D2 n=2,685, mean -0.2011R;
- D3 n=1,404, mean -1.0260R;
- D4 n=2,685, mean +0.1281R;
- D5 n=2,685, spread drag +1.783 bps;
- classification `A = EDGE_LOST_BEFORE_ENTRY`.

This conflicts with the 2026-09-23 report on endpoint availability, several estimates, and integrated classification. The source documents do not state in the retrieved text that one invalidates or replaces the other. Both remain exploratory historical records; this Result preserves the discrepancy instead of adjudicating it.

## Evidence and boundary

The report says the same fixed 2,685-trade population was used and the source pack plus five-hour Tick Correction v2 were read with recorded hashes. It also states that two D2/D4/D5 endpoints and two D3 endpoints could not be identified and were not imputed.

This result is exploratory on a consumed sample. It is not confirmatory evidence, does not establish causality or future profitability, and does not authorize any new parameter, filter, or rule.

## Sources

- [HR_v01_2026H1_diagnostic_report_ja.md](https://drive.google.com/file/d/1ODFl8jxY676iMfrRAPlMyqHSFjfAeUTD/view)
- [Horizontal Reaction Strategy v0.1 — Data D1-D5 Exploratory Diagnostic Replay — 2026H1 v1](https://docs.google.com/document/d/1MreVcFJUz5sDu2w9-qdIAX7D2lGZ5aKeDoQZozZLHE4/edit)
- [PILOT-TRADING-001 Project Brief — GOLD Decision Research Lab](https://docs.google.com/document/d/1GMuRnL6ZPa_OR2tVY85dQujjk0EmgdJeOBsdbLytBnE/edit)
