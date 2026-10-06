---
type: ResearchLine
research_line_id: RL-FXNS-001
status: PROPOSED_NOT_FROZEN
created_at: 2026-10-07
---

# FX News Sentiment with ChatGPT v0.1

## Purpose

Test a bounded, prospectively timestamped workflow in which ChatGPT classifies forward-looking FX-news sentiment and a deterministic rule converts those classifications into a EUR/JPY shadow-trading signal.

The line is designed for a user who can operate ChatGPT Plus and retail FX accounts without paid API infrastructure. It is not an autonomous trading agent and does not authorize live orders.

## Why this line

The strongest directly relevant prior evidence found so far is Ballinari and Maly (Swiss National Bank Working Paper 2025/11), which fine-tunes Llama 3.1 for G10 FX sentiment and constructs next-day currency portfolios from forward-looking article classifications. Their EUR/JPY illustration enters only when EUR and JPY sentiment scores differ in sign.

This line does **not** claim that an off-the-shelf ChatGPT model reproduces their fine-tuned model. v0.1 is a new prospective test of that operationally cheaper substitution.

## Candidate v0.1 adaptation

- pair: EUR/JPY only;
- model role: text classification only;
- candidate news window: 24 hours ending at 08:00 JST;
- information cutoff: 08:00 JST;
- intended shadow entry: 08:15 JST;
- intended shadow exit: 08:15 JST on the next eligible event day;
- eligible issuance days: Monday through Thursday when the qualified XM EURJPY quote route is available;
- news-source set: unresolved until source qualification;
- reference/execution research feed: exact XM MT5 EURJPY Bid/Ask, subject to qualification;
- live trading: forbidden in v0.1.

The 15-minute delay between information cutoff and shadow entry is deliberate. It makes the workflow executable by a human/ChatGPT process without pretending that a classification produced after the cutoff could have been traded at the cutoff price.

## Signal family

For each source article, ChatGPT classifies EUR and JPY independently as:

- APPRECIATION;
- DEPRECIATION;
- UNCHANGED;
- NOT_MENTIONED / INSUFFICIENT.

For each currency and event date, aggregate the forward-looking classifications using the SNB-style score:

`S_i = log(1 + N_appreciation) - log(1 + N_depreciation)`.

Pair action candidate:

- LONG EURJPY when `S_EUR > S_JPY` and the two scores do not have the same sign;
- SHORT EURJPY when `S_EUR < S_JPY` and the two scores do not have the same sign;
- NO_TRADE otherwise.

Exact zero/sign semantics are frozen in the specification before any scored prospective event.

## Scientific boundary

v0.1 tests whether this exact ChatGPT-assisted news-classification workflow has prospective predictive/economic value on EURJPY under its frozen source, timing, model, prompt, and execution assumptions.

It does not establish:

- general LLM trading skill;
- validity for other pairs;
- equivalence to the fine-tuned SNB model;
- profitability on Matsui FX;
- robustness to another news provider;
- optimality of the 08:00/08:15 timing;
- value of adding price indicators, macro filters, or repository research.

No historical parameter search is authorized.

## Current next action

Complete source qualification and prompt/input-contract design without inspecting prospective outcomes for rule selection. Then implement deterministic aggregation, quote selection, cost accounting, append-only records, and synthetic tests. Formal prospective scoring remains closed until explicit human freeze.
