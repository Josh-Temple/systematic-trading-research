# Research Lines Index

This file is a thin routing index for research lines and proposals.

It does not summarize current findings, experiment status, or decisions. For those, open the selected line in its current ref and follow the line-local files.

## Main-branch lines

### horizontal-reaction-v0.1

- scope root: `research/lines/horizontal-reaction-v0.1/`
- current projection: `research/lines/horizontal-reaction-v0.1/CURRENT.md`
- line definition: `research/lines/horizontal-reaction-v0.1/LINE.md`

Use for questions about the Horizontal Reaction research line.

### jp225-ema-timeofday-v0.1

- scope root: `research/lines/jp225-ema-timeofday-v0.1/`
- current projection: `research/lines/jp225-ema-timeofday-v0.1/CURRENT.md`
- line definition: `research/lines/jp225-ema-timeofday-v0.1/RESEARCH_LINE.md`

Use for the exact XM MT5 `JP225Cash` M1 EMA5/EMA200 research line and its explicitly separate historical proxy evidence. Fresh-read the line-local CURRENT/specification/audit before acting.

### jp225-us-lead-reversal-v0.1

- scope root: `research/lines/jp225-us-lead-reversal-v0.1/`
- current projection: `research/lines/jp225-us-lead-reversal-v0.1/CURRENT.md`

Use for the literature-motivated prior-U.S.-session / Japanese-opening reversal proxy research line. The 2015 OANDA midpoint proxy discovery is negative and stopped; it is not XM execution evidence.

## Branch-only research lines

Routing checked on 2026-10-08 against GitHub main `d7532c33a841a0d8c21d1288f39230e47c413894`, open PR metadata and branch trees. This date is a routing snapshot, not a statement of research freshness. Re-read the selected ref before acting.

### jp225-intraday-prospective-forecast-v0.1

- branch: `research/jp225-intraday-prospective-forecast-v0.1`
- scope root on that branch: `research/lines/jp225-intraday-prospective-forecast-v0.1/`
- current projection: `research/lines/jp225-intraday-prospective-forecast-v0.1/CURRENT.md`
- specification: `research/lines/jp225-intraday-prospective-forecast-v0.1/specifications/SPEC-JP225-FORECAST-001-v01.md`

Use for the prospective 09:00→15:30 JST JP225 forecast/review experiment. It is scientifically separate from the EMA and intraday-momentum strategy lines. Until source/readiness passes, dry runs are NOT_IN_COHORT and exact-XM outcome gaps must fail closed.

### currency-strength-momentum-v0.1

- branch: `research/currency-strength-momentum-v0.1`
- scope root on that branch: `research/lines/currency-strength-momentum-v0.1/`
- current projection on that branch: `research/lines/currency-strength-momentum-v0.1/CURRENT.md`
- line definition on that branch: `research/lines/currency-strength-momentum-v0.1/RESEARCH_LINE.md`

Use for questions about the FX currency-strength / strongest-versus-weakest momentum research line.

The architecture and packet work have separate branches. For the pre-outcome architecture follow [PR #31](https://github.com/Josh-Temple/systematic-trading-research/pull/31); for packet reconciliation follow [PR #37](https://github.com/Josh-Temple/systematic-trading-research/pull/37). Neither an open PR nor this route establishes outcome access authority.

### Other branch-only lines

| Topic / scope root | Ref to read | Entry point |
| --- | --- | --- |
| FX news headlines and bounded ChatGPT sentiment — `research/lines/fx-news-sentiment-v0.1/` | `research/fx-news-sentiment-v0.1` | [CURRENT](https://github.com/Josh-Temple/systematic-trading-research/blob/research/fx-news-sentiment-v0.1/research/lines/fx-news-sentiment-v0.1/CURRENT.md), [PR #63](https://github.com/Josh-Temple/systematic-trading-research/pull/63) |
| USDJPY overnight and weekly prospective forecasts — `research/lines/usdjpy-overnight-prospective-forecast-v0.1/` | `research/usdjpy-overnight-prospective-forecast-v0.1` | [CURRENT](https://github.com/Josh-Temple/systematic-trading-research/blob/research/usdjpy-overnight-prospective-forecast-v0.1/research/lines/usdjpy-overnight-prospective-forecast-v0.1/CURRENT.md), [PR #57](https://github.com/Josh-Temple/systematic-trading-research/pull/57) |
| JP225 intraday prospective forecasts — `research/lines/jp225-intraday-prospective-forecast-v0.1/` | `research/jp225-intraday-prospective-forecast-v0.1` | [CURRENT](https://github.com/Josh-Temple/systematic-trading-research/blob/research/jp225-intraday-prospective-forecast-v0.1/research/lines/jp225-intraday-prospective-forecast-v0.1/CURRENT.md), [PR #62](https://github.com/Josh-Temple/systematic-trading-research/pull/62) |
| Relative monetary-policy stance — `research/lines/fx-monetary-policy-alignment-v0.1/` | `research/fx-monetary-policy-alignment-v0.1` | [CURRENT](https://github.com/Josh-Temple/systematic-trading-research/blob/research/fx-monetary-policy-alignment-v0.1/research/lines/fx-monetary-policy-alignment-v0.1/CURRENT.md), [PR #43](https://github.com/Josh-Temple/systematic-trading-research/pull/43) |

### Deferred source route

`research/lines/jp225-intraday-momentum-v0.1/` is preserved on `research/jp225-intraday-momentum-v0.1` via [closed, unmerged PR #59](https://github.com/Josh-Temple/systematic-trading-research/pull/59). Follow its [CURRENT](https://github.com/Josh-Temple/systematic-trading-research/blob/research/jp225-intraday-momentum-v0.1/research/lines/jp225-intraday-momentum-v0.1/CURRENT.md) for its incident and source boundaries. The main-branch [free-source route decision](jp225-ema-timeofday-v0.1/work/source-research/FREE_SOURCE_ROUTE_DECISION_2026-10-05.md) takes precedence for source acquisition policy. This is separate from the exact-XM EMA and prospective-forecast lines.

## Branch-only proposals

| Topic / scope root | Ref to read | Entry point |
| --- | --- | --- |
| USDJPY daily breakout — `research/proposals/fx-daily-breakout-20261003/` | `research/fx-daily-breakout-20261003` | [README](https://github.com/Josh-Temple/systematic-trading-research/blob/research/fx-daily-breakout-20261003/research/proposals/fx-daily-breakout-20261003/README.md), [PR #40](https://github.com/Josh-Temple/systematic-trading-research/pull/40) |
| Multi-asset ETF trend feasibility — `research/proposals/multi-asset-trend-20261002/` | `research/multi-asset-trend-feasibility-20261002` | [README](https://github.com/Josh-Temple/systematic-trading-research/blob/research/multi-asset-trend-feasibility-20261002/research/proposals/multi-asset-trend-20261002/README.md), [PR #39](https://github.com/Josh-Temple/systematic-trading-research/pull/39) |

Important:
- do not infer current research state from this index;
- fresh-read the named main/branch ref before answering line-specific current-state questions;
- if a line is later merged, moved, superseded, or deleted, update this index.

## Synthetic research pilot

`research/pilots/autonomous-research-v0.1/` is a separate evaluator-integrity pilot on main. Use the pilot-local protocols and official-run status; it is not a market research line and does not consume Horizontal Reaction holdout data.

## Routing rules

1. Match the user's research topic to a line here before broad code search.
2. Open the line in the ref named above.
3. Prefer the line-local current projection / specification / decision files over this index.
4. Do not treat a branch name or merge state as proof of completion, verification, or current findings.
5. If no line matches, search the repository rather than inventing a line.
