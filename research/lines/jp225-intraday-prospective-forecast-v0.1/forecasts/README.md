# Forecast records

This directory is append-preserving storage for JP225 prospective forecast/review records.

## Naming

Use one immutable forecast artifact per system and event, for example:

- `YYYY-MM-DD_A1_forecast.json`
- `YYYY-MM-DD_A2_forecast.json`
- `YYYY-MM-DD_A3_forecast.json`
- `YYYY-MM-DD_review.json`

Dry-run records must include:

- `cohort_status = EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`;
- information cutoff and issued_at;
- system/version identity;
- numerical forecast;
- source refs;
- canonical forecast hash where feasible.

Formal v0.1 records are not permitted until the source/readiness gate passes and the exact specification is explicitly frozen.

Issued forecast files must not be replaced to correct a forecast. Corrections or annotations are new artifacts.
