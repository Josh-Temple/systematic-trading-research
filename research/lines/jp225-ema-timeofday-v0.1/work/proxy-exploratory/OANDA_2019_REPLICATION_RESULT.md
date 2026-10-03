---
id: RESULT-JP225-PROXY-OANDA-2019-REPLICATION
type: HistoricalReplicationResult
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-04
status: COMPLETE
classification: HISTORICAL_PROXY_NOT_REPLICATED
xm_execution_evidence: false
---

# OANDA JP225 historical-close replication — 2019

## Frozen question

Before 2019 outcome access, `OANDA_2019_REPLICATION_SPEC.md` fixed one primary question:

Does the post-hoc 2020 proxy observation for EMA(5)/EMA(200) crossovers during 14:45–15:15 JST reproduce in the separate 2019 OANDA JP225 M1 history at a +15-minute gross horizon?

No 2019 hourly, weekday, EMA, horizon, stop/target, or alternate-window search was permitted.

## Source identity

External repository: `FutureSharks/financial-data`

External repository commit read during the work:

`7ba1d404aa8b0e1c0f71321acebadcbfb9bcca8d`

The repository README identifies JP225 among its OANDA-sourced 2005–2020 instruments.

The repository's `oanda_prices.py`:
- requests month boundaries as UTC UNIX timestamps;
- asks OANDA for M1 candles;
- expands `candle['mid']`, therefore these are midpoint candle values rather than executable BID/ASK;
- converts returned UNIX seconds to pandas timestamps.

2019 blob identities:

- Jan `80895e23081fc27de8c99024df0c926e15e90163`
- Feb `0d537b37b4b35edef0e7bc3dae0d7751f436b986`
- Mar `f404162c4b0e7a876410dd986ed661373ddfbb39`
- Apr `a048ad915c812c12193e2f45a4112c2b7ebd975d`
- May `ed28957678adac00a80c2b0b6eb3cdadc4e33bb9`
- Jun `ecdca2722429d8a70392653b839d40accb19801a`
- Jul `a5ef30d9c84d1ed0b81348fd3b5713c5d9359300`
- Aug `5914448601142a85bc73a826d5dbc3a00753285c`
- Sep `2a8b3ba266475c31cdec70887d92a53f44ff8d85`
- Oct `bb5d7cbe7510abbff564c3f8d7d668446490747d`
- Nov `de602bf010073e8bf4ae48c2605a40d41738b711`
- Dec `880d6d0be48c6f3cddd4022b613e478e50ad04bd`

Combined row count: **250,276**.

Observed timestamp coverage: **2019-01-01 23:00 UTC through 2019-12-31 21:59 UTC**.

Monthly source-to-event partial receipts are preserved under `work/proxy-exploratory/2019/month_XX.json`.

## Frozen mechanics

- M1 close series
- recursive EMA(5) and EMA(200)
- first 1,000 chronological source rows as warm-up
- signal close = source bar timestamp + 1 minute
- gross proxy entry = exact next-minute bar OPEN
- gross proxy exit = exact OPEN 15 minutes after signal close
- missing exact timestamps are not imputed
- sign = +1 long / -1 short
- primary window = 14:45 <= Asia/Tokyo < 15:15
- date-cluster bootstrap by Asia/Tokyo date
- 10,000 replications
- seed 2255200

## Primary EMA5/EMA200 result

- crossover events in primary window: **161**
- valid exact-bar outcomes: **99**
- unavailable exact entry/target outcomes: **62**
- distinct Asia/Tokyo dates with valid outcomes: **65**
- mean gross +15m directional points: **+0.9303**
- win rate: **53.54%**
- day-cluster bootstrap 95% interval: **[-2.9103, +5.0836]**

Frozen replication criterion required:
1. >=50 valid events
2. >=30 dates
3. mean >0
4. 95% lower bound >0

Criteria 1–3 pass. Criterion 4 fails.

**Classification: HISTORICAL_PROXY_NOT_REPLICATED.**

## Predeclared baselines

### All eligible EMA5/EMA200 crossovers

- events: 5,126
- valid: 3,503
- missing: 1,623
- dates: 293
- mean gross points: **-0.1788**
- win rate: **46.62%**
- day-cluster 95% interval: **[-0.8706, +0.5566]**

### Tokyo-open 08:45–09:15 JST

- events: 226
- valid: 205
- missing: 21
- dates: 114
- mean gross points: **-3.1566**
- win rate: **44.88%**
- day-cluster 95% interval: **[-7.5435, +1.8286]**

Neither baseline supports a stable positive gross continuation effect.

## Price/EMA200 comparator in primary window

- events: 365
- valid: 245
- missing: 120
- dates: 109
- mean gross points: **-0.4004**
- win rate: **46.94%**
- day-cluster 95% interval: **[-2.2357, +1.4757]**

The positive 2020 close-window comparator observation also does not reproduce in 2019.

## Interpretation

### Fact

The strong positive 2020 partial-year close-window observation does not replicate in the frozen 2019 historical test.

### Interpretation

The 2020 close-window result is more consistent with a sample-specific/regime-specific observation than a stable property that should be promoted to an XM trading rule.

The broad EMA crossover result is approximately zero before any spread or slippage is charged. This is adverse evidence for the idea that simply exploiting XM's narrow spread will be sufficient to create an edge.

### Limitations

- OANDA midpoint proxy, not XM JP225Cash
- no executable spread
- historical market structure differs from current JPX hours
- high exact-target missingness is preserved rather than imputed
- historical replication is weaker evidence than prospective or broker-specific validation

## Stop decision

Per the frozen specification, do not run 2018 as another replication of the **14:45–15:15 close-window candidate** after this failure.

The original XM line remains scientifically UNTESTED because the exact XM source gate is still open.
