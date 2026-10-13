---
type: ExploratoryDryRun
research_line_id: RL-USDJPY-OVERNIGHT-001
event_id: DRYRUN-USDJPY-WEEKLY-2026-10-05
created_at: 2026-10-04
status: EXPLORATORY_ONLY_NOT_SCORED_COHORT
scientific_effect: NONE
weekly_spec_status: PROPOSED_NOT_FROZEN
protocol_cutoff_missed: true
---

# Exploratory weekly dry run — 2026-10-05 through 2026-10-09

## 1. Boundary

This is **not** weekly event 1.

The candidate weekly protocol uses a Sunday 20:00 JST information cutoff. This dry run was assembled after 22:58 JST on Sunday 2026-10-04, after that candidate cutoff had already passed.

In addition:

- `SPEC-USDJPY-WEEKLY-001-v01` is not yet frozen;
- source/readiness gates have not passed;
- the Dukascopy reference endpoint route has not yet been qualified for this line.

Therefore:

- do not include this event in the 26-week benchmark;
- do not claim its later outcome as prospective validation;
- do not use its later market outcome to rescue or tune the v0.1 horizon, score, comparator family, thresholds, or promotion rule;
- later scoring is allowed only as an **exploratory pipeline check** and must remain labeled as such.

## 2. Retrieval window

Research retrieval began after approximately `2026-10-04T22:58+09:00`.

The information set is therefore a post-candidate-cutoff exploratory snapshot, not a reconstruction of what was known at exactly 20:00 JST.

No claim is made that every item below was available by the proposed 20:00 cutoff.

## 3. Market snapshot

### USD/JPY

Non-canonical dry-run reference only:

- Monex historical page: 2026-10-02 close `157.853`; high `158.229`; low `156.955`.
- Bloomberg Línea page: approximately `157.85` late on 2026-10-02.

These sources are used only to orient this exploratory dry run.

They do **not** replace the candidate Dukascopy Bid/Ask reference feed required by the proposed specification.

Sources:

- https://stocks.monex.co.jp/USDJPY/historical
- https://www.bloomberglinea.com/english/quote/USDJPY%3ACUR/

### U.S. rates

Official U.S. Treasury daily par yield curve for 2026-10-02:

- 2-year: `4.83%`
- 10-year: `5.28%`

The curve remains at historically elevated long-term yields.

Source:

- https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve

### Fed policy

The Federal Reserve raised the federal-funds target range on 2026-09-16 to:

- `3.75%–4.00%`.

Source:

- https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm

### BOJ policy

The Bank of Japan currently encourages the uncollateralized overnight call rate to remain around:

- `1.25%`.

The interest rate applied to the complementary deposit facility has been 1.25% since 2026-09-24.

Sources:

- https://www.boj.or.jp/en/
- https://www.boj.or.jp/en/mopo/measures/term_cond/yoryo36.htm

## 4. Latest macro/policy observations

### U.S. labor data — yen-positive / USD-negative impulse at the margin

Reuters reported that September U.S. nonfarm payrolls increased by only 29,000 versus an economist forecast around 90,000, with unemployment at 4.2%. The report reduced expectations for another Fed increase at the October meeting.

Interpretation for this dry run:

- weaker labor data reduces near-term Fed-hike pressure;
- that narrows one potential source of additional USD rate support;
- it does not eliminate the already large U.S.–Japan rate differential.

Source:

- https://www.reuters.com/business/us-job-growth-slows-sharply-september-unemployment-rate-rises-42-2026-10-02/

### BOJ — tightening bias exists, but policy path is contested

Reuters reported that several BOJ policymakers discussed the case for faster rate increases at the September meeting, while government representatives pushed for caution.

Interpretation:

- the BOJ side is no longer a simple low-rate / one-way-yen-negative story;
- additional tightening risk can support JPY;
- government resistance and weak domestic-demand concerns can limit that support.

Sources:

- https://www.reuters.com/world/asia-pacific/boj-debated-need-more-rate-hikes-september-meeting-summary-shows-2026-10-01/
- https://www.reuters.com/world/asia-pacific/bojs-policy-pivot-opens-scope-faster-rate-hikes-2026-09-30/

### Intervention risk — material upside cap for USD/JPY

Reuters reported a renewed warning from Japan's top currency diplomat, with emphasis that markets should take the warning on yen weakness seriously and that Japan retains capacity to intervene.

Interpretation:

- this is not a mechanical prediction that intervention will occur;
- it creates asymmetric headline risk if USD/JPY rises rapidly toward recent weak-yen extremes;
- a simple trend-following USD-long weekly narrative should therefore be discounted.

Source:

- https://www.reuters.com/world/asia-pacific/japan-top-fx-diplomat-urges-markets-heed-very-clear-warning-yen-2026-09-28/

### Energy / geopolitical channel — yen-negative counterforce

Reuters has reported oil above roughly $100/bbl amid U.S.–Iran tensions and a global bond selloff.

Interpretation:

- high imported energy costs are adverse for Japan's terms of trade and can pressure JPY;
- high oil can also reinforce inflation/rate pressure in the U.S., supporting Treasury yields and USD;
- risk-off effects can pull the opposite way and therefore this is not a one-direction factor.

Sources:

- https://www.reuters.com/world/africa/dollar-firms-us-iran-tensions-lift-oil-hawkish-fed-bets-build-2026-09-28/
- https://www.reuters.com/commentary/reuters-open-interest/global-markets-view-usa-2026-10-02/

## 5. Known events for 2026-10-05 through 2026-10-09

### Japan

- 2026-10-06: BOJ Governor Kazuo Ueda is scheduled to address the National Securities Convention.
- 2026-10-06: Ministry of Finance 10-year JGB auction.
- 2026-10-08: Ministry of Finance 30-year JGB auction.

Sources:

- https://www.boj.or.jp/about/press/index.htm
- https://www.mof.go.jp/english/policy/jgbs/auction/calendar/2610e.htm

### United States

- 2026-10-07 14:00 ET: minutes of the September 15–16 FOMC meeting are scheduled for release.
- 2026-10-07 15:00 ET: Federal Reserve G.19 Consumer Credit.
- The BLS October calendar lists no national BLS release during October 5–9; the next major listed BLS release is CPI on October 14.

Sources:

- https://www.federalreserve.gov/newsevents/2026-october.htm
- https://www.bls.gov/schedule/2026/10_sched_list.htm

## 6. Repository-research status snapshot

The repository research layer is intentionally **not converted into a directional signal**.

Observed branch states from the current research-line projection:

- Currency Strength Momentum: UNTESTED; no market outcome currently treated as available.
- FX Monetary Policy Alignment: specification frozen, hypothesis UNTESTED, market-outcome gate blocked by upstream dependency.
- USD/JPY Daily Breakout source work: source qualification remains partial.

Therefore this dry run does not claim that any of these lines establishes USD/JPY direction.

## 7. Exploratory full-system-style outlook

This is a manually assembled exploratory analogue of the proposed weekly full-system output.

It is **not WA3**, because WA3 does not yet exist as a frozen, source-qualified forecast system.

### Numerical output

- `p_week_up` (Friday USD/JPY midpoint above Monday 08:00 midpoint): **0.45**
- implied `p_week_non_up`: **0.55**
- exploratory point forecast: **-15 bps** Monday-start-to-Friday-end log return
- confidence: **LOW_TO_MEDIUM**

### Central view

Slight JPY strengthening / USDJPY softening is the modal view, but with low conviction.

The main reason is the combination of:

1. weak U.S. payroll growth reducing urgency for another October Fed hike;
2. a BOJ policy debate that now contains a credible further-tightening side;
3. a scheduled Ueda appearance that can reinforce that side;
4. active Japanese intervention warnings that make rapid USD/JPY upside unusually headline-sensitive.

### Counterevidence

The bearish-USDJPY view is fragile because:

1. U.S. Treasury yields remain very high;
2. the Fed policy rate remains well above the BOJ policy rate;
3. oil/geopolitical stress is unfavorable for Japan's import bill;
4. the Japanese government has signaled caution about overly rapid BOJ tightening;
5. the September FOMC minutes could read more hawkishly than the post-payroll market narrative.

### Scenario map

**Scenario A — mild JPY strengthening / USDJPY down (central):**

- weak U.S. labor data remains the dominant rate-expectation impulse;
- Ueda does not push back against further BOJ normalization;
- intervention risk limits attempts to retest recent weak-yen extremes.

**Scenario B — renewed USDJPY upside:**

- FOMC minutes emphasize inflation and further tightening;
- Treasury yields resume the recent selloff higher;
- Ueda's remarks are interpreted as cautious;
- oil remains high or rises further.

**Scenario C — range / two-way volatility:**

- Ueda and Fed-minutes impulses offset;
- intervention rhetoric caps upside while U.S. yield support limits JPY appreciation.

### Invalidation / surprise conditions

The exploratory mild-down view would be weakened materially by:

- an unambiguously cautious Ueda signal on 2026-10-06;
- a renewed sharp rise in U.S. 2-year/10-year yields;
- a major new oil/geopolitical shock that primarily damages Japan's terms of trade;
- an FOMC-minutes interpretation that restores substantial near-term hike expectations.

It would be strengthened materially by:

- a clearly hawkish Ueda signal;
- additional Japanese official action or stronger intervention signaling;
- a sustained post-payroll decline in U.S. yields.

## 8. What to observe this week

For pipeline learning, preserve without changing the v0.1 scientific choices:

1. Monday 08:00 reference price candidate.
2. Ueda speech text and market timestamp.
3. JGB auction outcomes and rate reaction.
4. U.S. Treasury 2-year and 10-year changes.
5. FOMC minutes publication and immediate rate/FX reaction.
6. any intervention-related official statement.
7. Friday 22:00 candidate endpoint.

If this dry run is scored later, label the score:

`EXPLORATORY_PIPELINE_SCORE_ONLY`

and keep it outside all frozen benchmark counts.
