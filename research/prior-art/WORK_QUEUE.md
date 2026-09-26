# Prior-Art Work Queue

Updated: 2026-09-27

## Purpose

Long-running WORK sessions are used primarily for breadth-oriented evidence gathering, repetitive inspection, and focused verification tasks that do not require changing the canonical design.

Canonical design decisions, cross-repository synthesis, and schema changes remain outside the WORK role until evidence has been reviewed.

## Current state

Completed deep reviews:

- Trading Second Brain
- zestoles/quant
- Epsilon Quant Research
- DVC
- RD-Agent

Completed WORK:

- WORK-PA-001 — 21-candidate prior-art scan
- WORK-PA-002 — DVC reproducibility boundary review

Current priority:

1. Freqtrade — next focused engine/diagnostic review
2. Cross-repository synthesis / Phase 1 exit review after Freqtrade
3. Qlib or Kedro only if a material evidence gap remains

## WORK-PA-001 — Broad prior-art candidate scout

Status: COMPLETE

Result:
- `research/prior-art/CANDIDATE_SCAN.md`
- 21 candidates screened

## WORK-PA-002 — DVC reproducibility boundary review

Status: COMPLETE

Result:
- `research/prior-art/dvc.md`
- Commit supplied by WORK: `6c11602d2dadd6941f1290c78b1094342c29ad7d`
- Review status: PARTIAL

Key verified findings:

- Issue #11058 reproduced independently on DVC 3.67.1.
- Output could be generated from old code while `dvc.lock` recorded the post-edit code hash.
- A subsequent `dvc repro` skipped the stage as unchanged.
- Frozen-stage + `--force` behavior also reproduced a dependency-hash update without command re-execution.
- DVC strongly records declared pipeline definition and observed post-run dependency/output state.
- DVC lock metadata does not by itself guarantee that recorded dependency identity is the exact identity that caused the output.

## WORK-PA-003 — Freqtrade lookahead-diagnostic boundary review

Status: READY

### Goal

Deep-review `freqtrade/freqtrade` to determine what its lookahead-analysis and related backtest diagnostics actually detect, what they can miss, and whether passing the diagnostic can be mistaken for proof of no temporal leakage.

### Required fresh reads

Before starting, fresh-read:

- current project main
- `docs/ROADMAP.md`
- `docs/RESEARCH_PRINCIPLES.md`
- `research/prior-art/README.md`
- `research/prior-art/TEMPLATE.md`
- `research/prior-art/CANDIDATE_SCAN.md`
- completed prior-art reviews including `dvc.md`

### Target repository

`freqtrade/freqtrade`

### Core questions

Evaluate separately:

1. What exact classes of lookahead bias does `lookahead-analysis` test?
2. What assumptions does the test make about indicators, signals, resampling, informative pairs, and dataframe construction?
3. Can a strategy pass lookahead-analysis while still containing temporal leakage?
4. What known blind spots are documented or reported?
5. What tests exist for the diagnostic itself?
6. How are higher-timeframe / informative-candle boundaries handled?
7. What differences are expected between backtest, dry-run, and live behavior?
8. Which simulation assumptions are explicitly not guaranteed to match live execution?
9. How are data timing, incomplete candles, pairlists, fills, and fees handled?
10. Does the tool record diagnostic limitations or only PASS/FAIL output?

### Leads from candidate scan

Start from, but independently verify:

- official `lookahead-analysis` documentation
- Issue #12507 — reported missed higher-timeframe leakage
- Issue #12894 — reported signal mismatch after passing lookahead analysis

For each issue:

- inspect maintainer response
- inspect related PR/fix/tests
- determine current status
- independently reproduce a minimal case if feasible
- otherwise mark NOT_REPRODUCED

### Comparison target

Test these emerging principles:

- diagnostic PASS is not proof of problem absence
- computation correctness and evidence correctness require separate tests
- temporal data semantics must be explicit research assumptions
- scientific guarantee boundaries should be stored with the diagnostic result

### Output

Create only:

`research/prior-art/freqtrade.md`

Use `TEMPLATE.md` and add a section:

`Diagnostic Guarantee Matrix`

Rows:

- direct future-column access
- full-dataframe aggregation leakage
- shifted features
- higher-timeframe/informative-pair leakage
- incomplete candle usage
- dynamic pairlist effects
- backtest/live signal parity
- fill/execution parity
- cost parity
- stateful/external side effects

Classify each:

- STRONG
- PARTIAL
- NOT GUARANTEED
- NOT VERIFIED

### End report

Report:

- path
- commit SHA
- Review status
- whether #12507 was reproduced
- whether #12894 was reproduced
- strongest confirmed diagnostic guarantee
- most important blind spot
- any evidence that contradicts current provisional principles

## Later WORK candidates

After WORK-PA-003:

- provenance-field comparison across DVC / zestoles / Epsilon
- failure-pattern catalogue
- DVC vs DataLad vs Kedro provenance boundary comparison
- NautilusTrader / hftbacktest execution-semantics review
- Qlib experiment-recorder review

Do not independently change canonical schema or scientific rules.
