---
id: DATA-HR-001
type: Dataset
research_line_id: RL-HR-001
created_at: 2026-09-11
provider: Dukascopy first-party historical data
instrument: XAU/USD
time_range: 2026-01-02/2026-06-30 eligibility window; first 60 eligible sessions selected
granularity:
  signal: M1
  execution: raw BID/ASK Tick
role: CONSUMED_HOLDOUT
consumption_status: CONSUMED
may_influence_future_search: false
identity_evidence:
  m1_sha256_manifest: 7568d8ef1922c22e47d6bcacb2de555dcabb57c64f61ddf3f028bc4312a17325
  tick_sha256_manifest: 5e8558790024f78f8f9c5359bb85b6d8f46291ebd7dd8afca41ac35a362959ef
relations: []
---

# 2026H1 Horizontal Reaction evaluation dataset

## Frozen role

At freeze time, this was an evaluation period selected before v0.1 outcome computation.

The selection rule was the first 60 structurally eligible UTC trading weekdays in ascending order beginning 2026-01-02, within the fixed window ending 2026-06-30.

The actual 60 selected sessions finish on 2026-04-10.

After outcome access, this sample is a **CONSUMED_HOLDOUT** for Knowledge Base purposes.

It must not be reset to unused.

## Series

Signal:
- XAUUSD BID M1 UTC.

Execution proxy:
- XAUUSD raw BID and ASK ticks UTC.
- LONG entry ASK / exit BID.
- SHORT entry BID / exit ASK.

## Source restrictions

Frozen evaluation rules prohibited:

- alternate provider,
- broker-history substitution,
- repair/interpolation,
- synthetic rows,
- outcome-based substitution.

## Current reuse boundary

Allowed:

- reproduction of already-fixed calculations,
- correction of clear data/calculation errors,
- integration of existing results,
- interpretation-boundary checks.

Forbidden:

- new subset selection,
- new threshold selection,
- new parameter search,
- new time-window selection,
- new rule selection.

## Sources

Evaluation freeze:
https://docs.google.com/document/d/1RrBrev2MqsAeeXDSI3CXDiBk2Mn6z0d_m77hEjnSqOo/edit

Execution result:
https://docs.google.com/document/d/17Etkil26A1xv8SqEzZW3t44FHz9TNxNWrzWm6O_WyTI/edit
