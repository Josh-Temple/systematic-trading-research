# Research Lines Index

This file is a thin routing index for research lines.

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

## Active non-main research branches

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

Important:
- do not infer current research state from this index;
- fresh-read the named main/branch ref before answering line-specific current-state questions;
- if a line is later merged, moved, superseded, or deleted, update this index.

## Routing rules

1. Match the user's research topic to a line here before broad code search.
2. Open the line in the ref named above.
3. Prefer the line-local current projection / specification / decision files over this index.
4. Do not treat a branch name or merge state as proof of completion, verification, or current findings.
5. If no line matches, search the repository rather than inventing a line.
