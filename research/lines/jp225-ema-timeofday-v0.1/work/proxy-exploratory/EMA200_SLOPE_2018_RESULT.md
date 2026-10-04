---
id: RESULT-JP225-PROXY-EMA200-SLOPE-2018
type: HistoricalProxyResult
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-04
status: COMPLETE
classification: SLOPE_FILTER_PROXY_NOT_SUPPORTED_2018
xm_execution_evidence: false
---

# EMA5/EMA200 cross + aligned EMA200 slope — 2018 result

## Frozen test

The specification `EMA200_SLOPE_2018_SPEC.md` was committed before 2018 JP225 outcomes were accessed.

The only added condition was:

- long EMA5/EMA200 cross: current EMA200 > prior EMA200
- short EMA5/EMA200 cross: current EMA200 < prior EMA200

No time window, alternative slope lookback, threshold, EMA variant, exit variant, or side-specific rule was searched.

## Source

Public OANDA-derived midpoint JP225 M1 data from `FutureSharks/financial-data`.

2018 source blobs:

- Jan `ded62a1624fdea8c253a0ad0a1fe14cf8c1e8140`
- Feb `d210af7b47d9975b6069ea9dc9ecbb3e355e2e0a`
- Mar `ba1d75d04574e89dffa85c9dff22f2b403e2bf3d`
- Apr `aa2b7c449240e82c1e1cfbcff826d053a7c629a6`
- May `359dfeacd2f6801a776cc354112ffee175470d27`
- Jun `f55b8a88810dda15fa759464090b2273dfbce96b`
- Jul `108c909d7b3d348d1667e4d184458f2109083be4`
- Aug `d31498b049e23d6715002f1cfb1850404fda4444`
- Sep `551b974b4e9ec09930e05e552b50db516615e450`
- Oct `13fc4312c2e72ad54f231d2195b531eec42528b8`
- Nov `c086218e49726f846d31da07d912a98be156b638`
- Dec `0f7a5eae5e62e656d2e8dc7defe088b89ac911d3`

Rows: **300,680**.

Observed timestamp coverage: **2018-01-01 23:00 UTC through 2018-12-31 21:59 UTC**.

Monthly partial receipts are preserved under `work/proxy-exploratory/2018-slope/month_XX.json`.

## Result

### Intended slope-filter signal

- events: **5,940**
- valid exact-bar outcomes: **4,958**
- missing exact entry/target outcomes: **982**
- distinct Asia/Tokyo dates: **305**
- mean gross +15m directional points: **+0.2374**
- win rate: **48.87%**
- day-cluster bootstrap 95% interval: **[-0.3830, +0.8841]**

Frozen support required:
1. >=500 valid outcomes
2. >=150 dates
3. mean >0
4. 95% lower bound >0

Condition 4 fails.

**Classification: SLOPE_FILTER_PROXY_NOT_SUPPORTED_2018.**

### Unfiltered EMA5/EMA200 comparator

The unfiltered result is exactly identical:

- events: **5,940**
- valid: **4,958**
- missing: **982**
- dates: **305**
- mean: **+0.2374**
- win rate: **48.87%**
- 95% interval: **[-0.3830, +0.8841]**

This exact identity prompted a deterministic algebra check.

## Structural finding

The intended one-step EMA200 slope filter is not merely ineffective; under the standard EMA recursion it is logically redundant with an EMA fast/slow crossover when both EMAs use the same input and the fast alpha is larger than the slow alpha.

See `EMA200_SLOPE_REDUNDANCY_PROOF.md`.

Therefore the equality of filtered/unfiltered events is expected by construction and should not be interpreted as a market coincidence.

## Economic interpretation

The broad 2018 gross proxy expectancy is approximately zero **before** spread, slippage, commission, or XM-specific markup.

Its mean of +0.2374 index points is also the maximum average round-trip cost budget that could be absorbed before mean expectancy reaches zero in this proxy.

Because XM spreads are variable and exact historical XM BID/ASK is unavailable here, this does not calculate XM net expectancy. It is nevertheless adverse evidence for expecting a broad 24-hour 5/200 cross to become strongly profitable solely because JP225Cash feels inexpensive to trade.

## Stop decision

Do not rescue this result with a longer EMA200 slope lookback or slope magnitude threshold on the same development path. Those are new parameters and require a separately motivated specification plus unused data.

The exact XM broker-specific test remains open.
