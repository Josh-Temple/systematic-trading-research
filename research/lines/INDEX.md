# Research Lines Index

This file is a thin routing index for research lines.

It does not summarize current findings, experiment status, or decisions. For those, open the selected line in its current ref and follow the line-local files.

## Main-branch lines

### horizontal-reaction-v0.1

- scope root: `research/lines/horizontal-reaction-v0.1/`
- current projection: `research/lines/horizontal-reaction-v0.1/CURRENT.md`
- line definition: `research/lines/horizontal-reaction-v0.1/LINE.md`

Use for questions about the Horizontal Reaction research line.

## Active non-main research branches

### currency-strength-momentum-v0.1

- branch: `research/currency-strength-momentum-v0.1`
- scope root on that branch: `research/lines/currency-strength-momentum-v0.1/`
- current projection on that branch: `research/lines/currency-strength-momentum-v0.1/CURRENT.md`
- line definition on that branch: `research/lines/currency-strength-momentum-v0.1/RESEARCH_LINE.md`

Use for questions about the FX currency-strength / strongest-versus-weakest momentum research line.

### jp225-ema-timeofday-v0.1

- branch: `research/jp225-ema-timeofday-20261003`
- scope root on that branch: `research/lines/jp225-ema-timeofday-v0.1/`
- current projection on that branch: `research/lines/jp225-ema-timeofday-v0.1/CURRENT.md`
- line definition on that branch: `research/lines/jp225-ema-timeofday-v0.1/RESEARCH_LINE.md`

Use for the XM JP225Cash M1 EMA5/EMA200 crossover and time-of-day research line.


### jp225-us-lead-reversal-v0.1

- branch: `research/jp225-us-lead-reversal-20261004`
- scope root on that branch: `research/lines/jp225-us-lead-reversal-v0.1/`
- current projection on that branch: `research/lines/jp225-us-lead-reversal-v0.1/CURRENT.md`

Use for the literature-motivated prior-U.S.-session / Japanese-opening reversal proxy research line. The 2015 OANDA midpoint proxy discovery is negative and the line is stopped; it is not XM execution evidence.

Important:
- non-main lines are not currently canonical on `main`;
- do not infer current research state from this index;
- fresh-read the named branch before answering line-specific current-state questions;
- if a branch is merged, moved, superseded, or deleted, update this index.

## Routing rules

1. Match the user's research topic to a line here before broad code search.
2. Open the line in the ref named above.
3. Prefer the line-local current projection / specification / decision files over this index.
4. Do not treat a branch name as proof of completion, verification, or current findings.
5. If no line matches, search the repository rather than inventing a line.

JP225 combined pre-XM audit/hardening review branch: `work/jp225-pre-xm-hardening`.
Its line-local CURRENT and `work/integration/INDEPENDENT_AUDIT.md` are the combined draft projection; the architecture-only branch above does not include these later corrections. Neither is merged main authority yet.
