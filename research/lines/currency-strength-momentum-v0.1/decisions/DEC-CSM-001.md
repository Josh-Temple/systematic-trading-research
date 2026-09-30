---
id: DEC-CSM-001
type: Decision
research_line_id: RL-CSM-001
created_at: 2026-10-01
based_on:
  - HYP-CSM-001
  - SPEC-CSM-001-v01
decision: ADVANCE_TO_BOUNDED_EXPLORATORY_SCREEN
reason: Published FX momentum evidence supports a bounded monthly test, while direct intraday prior evidence is negative and does not answer the monthly question.
effect_on_current_state:
  hypothesis_HYP-CSM-001: UNTESTED_V0_1
  dataset_DATA-CSM-001: PLANNED_SOURCE_QUALIFICATION
next_allowed_actions:
  - ECB source qualification
  - immutable source capture
  - deterministic implementation of SPEC-CSM-001-v01
  - one execution of EXP-CSM-001
forbidden_actions:
  - lookback sweep before recording v0.1
  - holding-period sweep before recording v0.1
  - universe selection from outcomes
  - factor-filter rescue
  - intraday parameter search
relations:
  - type: derived_from
    target: HYP-CSM-001
  - type: derived_from
    target: SPEC-CSM-001-v01
---

# Decision — advance to one bounded monthly Discovery screen

The research question is sufficiently grounded to justify a low-cost empirical test.

The next action is not strategy optimization. It is source qualification followed by one deterministic execution of the frozen 1-month / 1-month strongest-minus-weakest specification.

A positive gross ECB-reference-rate result will not be called a tradeable edge. A negative result will not be rescued on the same outcome set by trying additional horizons or filters.
