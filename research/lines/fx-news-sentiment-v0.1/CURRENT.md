---
type: CurrentProjection
research_line_id: RL-FXNS-001
projection_generated_at: 2026-10-07
derived_from_decisions: []
derived_from_interpretations: []
---

# Current projection — FX News Sentiment with ChatGPT v0.1

## Current state

- Scientific status: UNTESTED.
- Specification: PROPOSED_NOT_FROZEN.
- Historical market-outcome search for tuning: NOT_AUTHORIZED.
- Formal prospective cohort: CLOSED.
- Exploratory source/prompt dry runs: PERMITTED only without using subsequent market outcomes to modify the candidate rule.
- Live or paper broker order submission: NOT_AUTHORIZED.

## Candidate question

Can a fixed ChatGPT prompt classify pre-cutoff FX news into forward-looking EUR and JPY sentiment such that the deterministic EURJPY rule in this line produces positive prospective executable returns after measured Bid/Ask costs?

## Candidate implementation

- ChatGPT is a bounded classifier, not the trading-rule author.
- A deterministic program aggregates classifications and creates LONG / SHORT / NO_TRADE.
- A separate deterministic program reads qualified XM EURJPY Bid/Ask observations after the forecast is frozen and computes the shadow result.
- Issued classification/signal records are append-only and never overwritten.

## Evidence state

Relevant external evidence is mixed:

1. SNB Working Paper 2025/11 reports useful FX sentiment classification and trading performance from a **fine-tuned** Llama 3.1 model, including a EUR/JPY pair illustration.
2. Lopez-Lira and Tang report that GPT-4 news interpretation predicts subsequent U.S.-equity return drift, supporting LLM text interpretation as a plausible signal-extraction task, but not this FX rule.
3. FINSABER's long-horizon evaluation finds that broad LLM trading-agent advantages often disappear under longer, broader and bias-aware tests.
4. Recent leakage research reports large post-cutoff performance decay in several financial LLM agents.

Therefore v0.1 adopts the narrow text-classification use case and rejects autonomous free-form LLM trading as the default.

## Current blockers

- exact permitted news-source set is not frozen;
- point-in-time article availability and publication timestamps are not qualified;
- public/private preservation rules for article input text are not fixed;
- ChatGPT prompt/output schema is not frozen;
- observable model-identity handling across product updates is not fixed;
- exact XM EURJPY Bid/Ask timestamp/cost route is not qualified for this line;
- deterministic implementation and synthetic tests do not yet exist.

## Next action

Execute Packets A-C outcome-blind:

1. complete literature / GitHub prior-art record;
2. qualify the news and XM source contracts;
3. freeze the ChatGPT classification prompt and deterministic rule;
4. implement and test the pipeline with synthetic fixtures only;
5. obtain independent pre-outcome audit.

Only then request human freeze for a prospective shadow cohort.
