---
type: ResearchLine
research_line_id: RL-FXNS-001
status: PROPOSED_NOT_FROZEN
created_at: 2026-10-07
---

# FX News Sentiment with ChatGPT v0.1

## Purpose

Test a bounded, prospectively timestamped workflow in which ChatGPT classifies forward-looking FX **headlines** and a deterministic rule converts those classifications into a EUR/JPY shadow-trading signal.

The line is designed for ChatGPT Plus plus a retail FX environment, without a paid LLM API or paid news feed. It is not an autonomous trading agent and does not authorize live orders.

## Evidence basis

The primary FX mechanism prior is Ballinari and Maly (SNB Working Paper 2025/11): a fine-tuned Llama 3.1 classifies forward-looking G10 sentiment, aggregates appreciation/depreciation counts, and feeds next-day currency portfolios; their EUR/JPY illustration uses relative, opposite-sign sentiment.

This v0.1 is **not** a direct replication:
- the SNB study uses full-text provider content and a fine-tuned model;
- DailyFX, one of its sources, closed in 2024;
- current FXStreet / Investing.com preservation terms make them poor fits for a public auditable pipeline;
- v0.1 therefore proposes title/headline metadata from GDELT and an off-the-shelf ChatGPT product model.

That substitution is exactly what the prospective experiment tests.

## Candidate v0.1 adaptation

- pair: EUR/JPY only;
- LLM role: headline classification only;
- preferred news route: GDELT Article List / title metadata, pending runtime qualification;
- candidate news window: 24 hours ending at 08:00 JST;
- information cutoff: 08:00 JST;
- intended shadow entry: 08:15 JST;
- intended shadow exit: 08:15 JST on the next normal FX weekday (Thursday → Friday; Friday exit-only);
- eligible issuance days: Monday through Thursday;
- reference/execution research feed: exact XM MT5 EURJPY Bid/Ask, subject to qualification;
- live trading: forbidden in v0.1.

The 15-minute delay is deliberate: it avoids pretending that a model output produced after 08:00 could have been executed at 08:00.

## Signal family

For each frozen GDELT headline record, ChatGPT classifies EUR and JPY independently as:

- APPRECIATION;
- DEPRECIATION;
- UNCHANGED;
- NOT_MENTIONED;
- INSUFFICIENT.

For each currency and event date:

`S_i = log(1 + N_appreciation) - log(1 + N_depreciation)`.

Candidate pair action:

- LONG EURJPY when `S_EUR > S_JPY` and the signs differ;
- SHORT EURJPY when `S_EUR < S_JPY` and the signs differ;
- NO_TRADE otherwise.

Exact zero/sign semantics are fixed in the proposed specification and must remain unchanged once frozen.

## Scientific boundary

v0.1 tests one concrete ChatGPT-assisted headline workflow. It does not establish:

- general LLM trading skill;
- validity for other pairs;
- equivalence to the fine-tuned SNB model;
- profitability on Matsui FX;
- robustness to another source/query;
- optimality of the 08:00/08:15 timing;
- value of adding technical indicators, price-based currency strength, macro filters, or repository research.

No historical EURJPY parameter search is authorized.

## Current next action

Finish GDELT runtime/query qualification, freeze the headline input contract and ChatGPT prompt, qualify XM EURJPY Bid/Ask/cost semantics, then implement deterministic aggregation/quote selection with synthetic tests. Formal prospective scoring remains closed until independent audit and explicit human freeze.


## Pre-freeze hardening update — 2026-10-07

The amended specification governs Thursday → Friday exit, distinct issuance/exit
days, strict open 24-hour news boundaries and MAXRECORDS fail-closed disposition.
See `work/PRE_FREEZE_HARDENING_RESULT.md` for current verification. Earlier runtime/history
statements describe the previous review; this update supersedes its schedule blocker.
Scientific UNTESTED; specification PROPOSED_NOT_FROZEN; GDELT PARTIAL_WITH_GAPS
(SOURCE_QUALIFICATION_BLOCKED for formal use); prompt FREEZE_READY_CANDIDATE;
XM LOCAL_XM_EXECUTION_REQUIRED; formal cohort CLOSED. No SOURCE PASS or freeze.
