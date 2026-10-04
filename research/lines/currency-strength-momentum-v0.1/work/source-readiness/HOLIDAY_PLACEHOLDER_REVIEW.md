---
id: CSM-SOURCE-HOLIDAY-PLACEHOLDER-20261004
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-04
status: REVIEWED
scientific_status: NOT_APPLICABLE
market_outcome_access: false
relations:
  - type: derived_from
    target: CSM-SOURCE-READINESS-20261004-01
---

# ECB EXR holiday-placeholder review

## Finding

The first metadata-only full-history run returned, for each of the seven fixed ECB EXR series:

- 4,331 rows with `OBS_STATUS=A`;
- zero missing expected TARGET-open dates;
- ten additional rows with `OBS_STATUS=H`;
- those ten H rows had blank observation values;
- the same ten dates appeared for every series.

No observation values were emitted or reviewed.

Safe metadata receipt:
- workflow run: `37167323298`
- receipt SHA-256: `5734c0ed874d9c5362210e75e27c6a337e437e7eef7daae9aca902b682a24835`

## Dates

The ten additional H-status dates are:

- 2009-12-25
- 2010-01-01
- 2010-04-02
- 2010-04-05
- 2011-04-22
- 2011-04-25
- 2011-12-26
- 2012-04-06
- 2012-04-09
- 2012-05-01

Each is excluded by the independently locked TARGET closing-day rule.

## Official status meaning

ECB observation-status documentation defines `H` as a missing value due to a holiday or weekend.

The long-term TARGET calendar closes, in addition to weekends, on:
- 1 January;
- Good Friday;
- Easter Monday;
- 1 May;
- 25 December;
- 26 December.

Therefore these rows are not evidence of a missing expected open-day exchange-rate observation. They are explicit holiday placeholders carried in the API output.

## Readiness rule

For this fixed source-readiness check:

- `A` rows are candidate market observations and must occur exactly on expected TARGET-open dates, with a valid positive numeric value.
- `H` rows are permitted only when:
  - the date is not in the locked expected-open calendar;
  - the observation value is blank;
  - the date is an independently expected TARGET-closed date.
- H rows are excluded from the observation-date coverage set.
- Any H row on an expected-open date, or any H row with a nonblank value, fails closed.
- Any status other than A or reviewed H fails closed.

This is a source-parsing qualification, not a scientific-result change.

## Boundary

No exchange-rate value is reproduced or used.

The frozen `SPEC-CSM-002-v01` is unchanged.
