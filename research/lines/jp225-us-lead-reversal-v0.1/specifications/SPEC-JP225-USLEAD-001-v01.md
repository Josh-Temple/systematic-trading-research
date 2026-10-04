---
id: SPEC-JP225-USLEAD-001-v01
type: HistoricalProxyDiscoverySpecification
hypothesis_id: HYP-JP225-USLEAD-001
created_at: 2026-10-04
status: FROZEN_BEFORE_2015_OUTCOME_ACCESS
xm_execution_evidence: false
---

# JP225 US-Lead Opening Reversal — 2015 proxy discovery

## 1. Purpose

Test one literature-motivated cross-market timing rule on a previously unread public proxy year.

No parameter search is permitted.

## 2. Discovery data

Use only calendar-year 2015 files from public repository `FutureSharks/financial-data`:

- OANDA-derived midpoint `SPX500_USD` M1;
- OANDA-derived midpoint `JP225_USD` M1.

Preserve monthly Git blob SHAs.

No 2014 price outcome may be accessed unless 2015 passes and an exact 2014 replication specification is committed first.

## 3. U.S. regular-session return

For each New York trading date:

- entry quote = OPEN of exact 09:30 America/New_York M1 bar;
- exit quote = CLOSE of exact 15:59 America/New_York M1 bar;
- U.S. return = exit / entry - 1.

Both exact bars must exist.

No interpolation or nearest-bar substitution.

### Mapping to Japanese date

For a Japanese calendar date D:

1. take D-1 calendar day;
2. if Saturday/Sunday, roll backward to Friday;
3. require an available U.S. session return on exactly that resulting New York calendar date;
4. if unavailable, exclude the Japanese date.

This intentionally excludes a Japanese day whose expected preceding U.S. weekday was a U.S. market holiday rather than carrying an older session forward.

## 4. Japanese opening window

JPX's 2015 Nikkei 225 futures day session began at 09:00 JST.

For each eligible Japan date:

- JP entry = OPEN of exact 09:00 Asia/Tokyo M1 bar;
- JP exit = OPEN of exact 09:30 Asia/Tokyo M1 bar.

Both exact bars must exist.

No interpolation.

## 5. Direction

If U.S. regular-session return > 0:
- direction = SHORT.

If U.S. regular-session return < 0:
- direction = LONG.

If exactly zero:
- no event.

Directional JP gross return:

- LONG: exit / entry - 1
- SHORT: entry / exit - 1

Also report signed index points:
- LONG: exit - entry
- SHORT: entry - exit

## 6. Primary metric

Mean directional JP return in basis points.

Supporting:
- median bps;
- mean points;
- median points;
- win rate;
- event count;
- distinct Japan dates;
- day bootstrap 95% CI;
- U.S.-return / JP-first-30m raw correlation;
- unconditional long 09:00–09:30 descriptive mean.

## 7. Bootstrap

One event maximum per Japan date.

- resample Japan event dates with replacement;
- 10,000 replications;
- seed 2255001;
- RNG = 32-bit LCG:
  - x0 = seed unsigned 32-bit
  - x[n+1] = (1664525*x[n] + 1013904223) mod 2^32
  - U = x / 2^32
- linear percentile interpolation at position (N-1)*q;
- q = 0.025 and 0.975.

## 8. Discovery support rule

Classify `USLEAD_PROXY_SUPPORTED_2015` only if all hold:

1. >= 180 valid events;
2. mean directional bps > 0;
3. bootstrap 95% lower bound > 0.

Otherwise:
- `INSUFFICIENT_PROXY_EVENTS`, or
- `USLEAD_PROXY_NOT_SUPPORTED_2015`.

## 9. Comparator / descriptive only

Report:
- unconditional LONG 09:00–09:30 JST gross return;
- raw correlation between U.S. regular-session return and JP 09:00–09:30 raw long return.

These cannot rescue a failed strategy rule.

## 10. Forbidden rescue

After reading 2015 outcomes, do not change or search:

- U.S. return threshold;
- absolute-return threshold;
- 09:00/09:30 times;
- horizon;
- weekday;
- direction rule;
- overnight sign filter;
- volatility/VIX filter;
- EMA or other technical filter;
- SL/TP;
- long-only/short-only;
- transaction-cost assumptions.

If discovery fails, stop this v0.1 candidate.

If discovery passes, commit an exact 2014 replication specification before accessing 2014 outcomes.

## 11. Interpretation boundary

The source is midpoint CFD proxy data.

A positive historical result would not establish XM JP225Cash net profitability.

Actual broker BID/ASK spread, execution, current session structure, and modern-regime replication remain separate requirements.
