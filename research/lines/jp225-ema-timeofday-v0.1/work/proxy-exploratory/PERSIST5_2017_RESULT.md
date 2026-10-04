---
id: RESULT-JP225-PROXY-PERSIST5-2017
type: HistoricalProxyResult
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-04
status: COMPLETE
classification: PERSIST5_PROXY_NOT_SUPPORTED_2017
xm_execution_evidence: false
---

# EMA5/EMA200 cross + 5-bar persistence — 2017 result

## Pre-outcome freeze

The candidate was frozen before 2017 price outcomes were accessed.

Chronology:
- no-PC continuation decision commit: `08f912aafdfad162da8d979d5c6c5123c7fef6d7`
- initial persistence specification commit: `63a445a8af7717bd8382badedca001ace0f99645`
- exact-minute eligibility clarification, still before price-content access: `2c35a1092de8dbd5e4b1044033502f319c0d93f6`
- first 2017 outcome-bearing monthly receipt: `cc2b954b9d8614199f22022002b7c8106ff7d93d`

Directory/blob identities were listed only after the specification was frozen. The calculation did not inspect 2016.

## Source

Public OANDA-derived JP225 midpoint M1 files from `FutureSharks/financial-data`.

2017 monthly Git blob SHAs:

- Jan `14ce4981687674bec3c11bf89c69344be5695cda`
- Feb `da02ce3b0061076fe94b5ed93bd4c9018c2a013c`
- Mar `0712053cde39eab5d7454148264e2d792dd4b432`
- Apr `22719c4b5667138bbee29ecd052d86969ecbc705`
- May `b9a74bcb88587beceb4bebf4b7b1f5d2a7068f7d`
- Jun `8c335255d58caccdf69b3afe1b50d916d0e0c2f0`
- Jul `704470966f2b942b7c03f1726544e123467a0ec6`
- Aug `8c76d558e762511518e776eee700c97c9c4188e1`
- Sep `5d8122d0bd5b359622e341424b470e21ee301e35`
- Oct `47fcea36313d0904e9c0e45c36378e4b9c0489f0`
- Nov `f8eec27cfd5a8091e76b6f948a82f08e1b518feb`
- Dec `1385dee3c144f5e7a519082ca056eaa4b1c5f11d`

Combined source rows: **248,798**.

Observed timestamp coverage:
- first: 2017-01-02 23:00 UTC
- last: 2017-12-29 21:59 UTC

Monthly source-to-result receipts are preserved under `2017-persist5/month_XX.json`.

## Frozen mechanics

- M1 close
- recursive EMA(5), EMA(200)
- first 1,000 chronological source rows as warm-up
- base cross requires an exact preceding one-minute bar
- after cross, next five exact one-minute bars must all preserve the crossed EMA ordering
- entry at exact bar OPEN six minutes after the cross-bar open
- exit at exact OPEN 15 minutes after entry
- no imputation or nearest-bar substitution
- ALL times only
- midpoint gross points only
- day-cluster bootstrap by Asia/Tokyo entry date
- 10,000 replications
- seed 2255200
- explicitly specified 32-bit LCG and linear percentile interpolation

## Primary persistence result

Base EMA5/EMA200 crosses: **4,094**.

Classification before outcome:
- persistence ordering failed: **894**
- exact confirmation minute missing: **1,704**
- five-bar persistence confirmed: **1,496**

Confirmed-event resolution:
- exact entry missing: **109**
- exact +15m target missing: **183**
- valid outcomes: **1,204**

Valid sample:
- distinct Asia/Tokyo dates: **253**
- long: **594**
- short: **610**
- mean +15m gross points: **-0.287292**
- median: **-1.35**
- win rate: **44.77%**
- day-cluster bootstrap 95% interval: **[-1.671920, +1.127615]**

Frozen support criterion required:
1. >=500 valid outcomes
2. >=150 dates
3. mean >0
4. 95% lower bound >0

Criteria 1 and 2 pass. Criteria 3 and 4 fail.

**Classification: PERSIST5_PROXY_NOT_SUPPORTED_2017.**

## Unfiltered comparator

Same exact-minute base crossover, without the five-bar persistence wait:

- events: **4,094**
- valid outcomes: **2,776**
- entry missing: **643**
- target missing: **675**
- dates: **288**
- mean +15m gross points: **-0.144020**
- median: **0**
- win rate: **45.61%**
- day-cluster bootstrap 95% interval: **[-0.730975, +0.472003]**

The persistence modification does not improve the observed gross continuation result in 2017.

## Integrity checks

Independent annual receipt checks:

- base crosses = persistence-failed + confirmation-gap + confirmed:
  - 4,094 = 894 + 1,704 + 1,496
- confirmed = entry-missing + target-missing + valid:
  - 1,496 = 109 + 183 + 1,204
- comparator events = entry-missing + target-missing + valid:
  - 4,094 = 643 + 675 + 2,776
- every valid persistence event has entry exactly six minutes after the cross bar open
- every valid exit is exactly 15 minutes after entry
- every valid comparator entry is exactly one minute after the cross bar open
- no duplicate persistence event IDs were found

## Interpretation

### FACT

The five-bar persistence requirement reduces the event population substantially, but the remaining sample has negative average +15-minute gross movement.

The raw unfiltered comparator is also negative on the same year.

### INTERPRETATION

Waiting five complete minutes for the EMA ordering to persist does not rescue the short-horizon continuation hypothesis in this historical midpoint proxy.

The result is adverse before any spread, slippage, commission, or XM markup is charged.

The high number of confirmation gaps also shows that exact-minute persistence tests are sensitive to the historical proxy's sparse-minute coverage. Missing minutes were treated as unavailable evidence, not filled.

This does not establish the result for current XM JP225Cash.

## Decision

Per the pre-registered stop rule:

- **do not access 2016 for this candidate**
- do not try alternative persistence lengths
- do not add time windows
- do not change EMA lengths
- do not add SL/TP or side filters

The candidate stops as a negative proxy result.

Exact XM v0.1 remains UNTESTED and WAITING_FOR_XM_STAGE1_DATA.
