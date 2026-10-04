---
id: DEC-CSM-004-METADATA-SOURCE-READINESS-20261004
type: Decision
research_line_id: RL-CSM-001
created_at: 2026-10-04
status: ACTIVE
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
  - type: derived_from
    target: DEC-CSM-003-POST-E-REAUDIT-20261004
---

# Metadata-only full-history source-readiness authorization

## Decision

Authorize one **metadata-only source-readiness run** for the seven fixed ECB EXR series over the already frozen source interval.

This is not Packet X and does not open I2.

Purpose: resolve source coverage/status/schema/calendar readiness without exposing or analysing market values.

## Fixed scope

Series:
- D.AUD.EUR.SP00.A
- D.CAD.EUR.SP00.A
- D.CHF.EUR.SP00.A
- D.GBP.EUR.SP00.A
- D.JPY.EUR.SP00.A
- D.NZD.EUR.SP00.A
- D.USD.EUR.SP00.A

Period:
- 2009-11-01 through 2026-09-30

Provider/transport:
- official ECB EXR SDMX REST API
- exact route family already locked by Packet C

## Allowed processing

An isolated GitHub Actions runner may receive the full official CSV response bytes only to compute source-readiness metadata.

The script may:
- hash raw response bytes;
- verify HTTP/content type;
- parse the locked schema;
- read TIME_PERIOD and OBS_STATUS;
- compare TIME_PERIOD to the locked expected calendar;
- count rows/dates, duplicates, missing expected dates, unexpected dates and status codes;
- test whether OBS_VALUE is blank/nonblank and numeric/nonfinite as a boolean validity check;
- verify fixed dimension/unit/source-agency metadata;
- record first/last dates and hashes of date lists;
- emit only metadata/counts/hashes.

## Forbidden processing/output

The script must not:
- print, persist, upload or commit any OBS_VALUE;
- compute returns, ratios, rankings, selected pairs or target outcomes;
- compute descriptive price statistics;
- retain raw CSV as an Actions artifact;
- make parameter/subperiod choices;
- expose any observation value in error messages.

Raw full-history responses are ephemeral runner inputs and are discarded when the job ends.

Only a derived metadata receipt with no observation values may be committed later after independent review.

## Fail-closed rule

Any unexpected schema, dimension, source agency, status, duplicate, out-of-range date, nonnumeric/blank value, or calendar discrepancy is recorded as a source-readiness gap. It is not silently repaired.

## Scientific boundary

The frozen SPEC remains unchanged.

This decision only permits evidence needed to decide whether the fixed source can later be captured under I2. It does not authorize market-outcome access.
