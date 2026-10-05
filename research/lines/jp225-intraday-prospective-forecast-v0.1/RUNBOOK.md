# JP225 prospective forecast — manual chat runbook

Status: ACTIVE_FOR_EXPLORATORY_DRY_RUNS_ONLY

This runbook deliberately uses no ChatGPT scheduled task and no scheduled GitHub workflow.

## Morning forecast invocation

On an eligible JPX trading day, invoke the forecast from ChatGPT at or immediately after 08:00 JST.

Recommended user message:

`JP225の今日の予想を実行して`

The operator must then:

1. fresh-read this branch and the event pre-registration;
2. verify the event date against the official JPX calendar;
3. freeze an information cutoff of exactly 08:00:00 JST;
4. retrieve only sources available by that cutoff;
5. produce B0/A1/A2/A3;
6. preserve exact-XM missingness rather than substituting another provider;
7. mark every output `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`;
8. validate the JSON record;
9. append a new forecast artifact without overwriting prior records.

If the invocation occurs materially after 08:00, public sources that cannot demonstrate their pre-08:00 state must not be treated as canonical pre-cutoff input. Record the limitation as a protocol deviation rather than reconstructing it silently.

## Afternoon review invocation

After 15:30 JST, use:

`JP225の今日の結果確認を実行して`

The operator must:

1. fresh-read the exact issued forecast artifacts first;
2. never alter those forecast files;
3. retrieve exact XM `JP225Cash` start/end quotes only if the qualified route is genuinely available;
4. otherwise set `MARKET_OUTCOME_UNAVAILABLE` or `SOURCE_RETRIEVAL_FAILED`;
5. compute Brier/MAE only when the required exact-XM outcome exists;
6. record facts separately from interpretation;
7. record error attribution without changing the candidate specification;
8. append a review artifact and validate it.

## Scientific boundary

A dry run is workflow evidence, not forecast-skill evidence.

No individual dry run can:

- enter the later 60-event scored cohort;
- justify a rule change;
- rescue a missing XM outcome with another provider;
- modify existing EMA/reversal research;
- authorize trading.

## Current event

The first pre-registered dry-run event is:

- `XPF-JP225-20261006`
- 2026-10-06
- information cutoff / intended issuance: 08:00 JST
- target start: 09:00 JST
- endpoint: 15:30 JST
- status before forecast: PENDING

For 2026-10-06 specifically, the timing-change request arrived before 08:00 but repository implementation occurred after 08:00. Any forecast issued for that date after implementation must include a `LATE_ISSUANCE_AFTER_0800` protocol deviation and remain `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`.
