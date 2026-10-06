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
- Specification: `SPEC-FXNS-001-v01` is PROPOSED_NOT_FROZEN.
- Historical market-outcome search for tuning: NOT_AUTHORIZED.
- Formal prospective cohort: CLOSED.
- Live or paper broker order submission: NOT_AUTHORIZED.

## Candidate question

Can a fixed ChatGPT prompt classify point-in-time FX headlines into forward-looking EUR and JPY sentiment such that a deterministic EURJPY rule produces positive prospective executable returns after qualified costs?

## Current source direction

Preflight completed on 2026-10-07 without viewing EURJPY outcomes.

- Historical DailyFX route: not current; IG states DailyFX closed in 2024.
- Investing.com: not selected for a canonical reproducible input under current preservation terms.
- FXStreet: not selected without permission under current copying/AI-use restrictions.
- GDELT: preferred v0.1 candidate because its released datasets are open for unrestricted reuse and its article-list data provide title/URL plus point-in-time observation metadata.

The candidate is therefore **GDELT headline/title classification**, not publisher full-text ingestion.

GDELT is not yet SOURCE PASS: exact query, runtime response fields, record-limit behavior, deduplication, raw-response hashing and attribution still need qualification.

## Candidate implementation

- GDELT provides the frozen point-in-time headline corpus.
- ChatGPT is a bounded classifier, not the trade-rule author.
- Deterministic code aggregates labels and creates LONG / SHORT / NO_TRADE.
- Separate deterministic code reads qualified XM EURJPY Bid/Ask only after the signal is frozen.
- Issued input/classification/signal records are append-only.

## Evidence state

1. SNB Working Paper 2025/11 provides the direct FX sentiment mechanism prior, but uses fine-tuned Llama and full-text providers.
2. Lopez-Lira & Tang provide peer-reviewed headline-based GPT evidence in U.S. equities.
3. FX headline sentiment work using ChatGPT 3.5 provides direct task-level support, but not a prospective retail trading validation.
4. FINSABER and leakage research are adverse evidence against broad autonomous LLM-trader claims.

Therefore v0.1 intentionally narrows ChatGPT to semantic classification and relies on prospective evidence.

## Remaining blockers

- exact GDELT query/field contract not frozen;
- runtime source qualification incomplete;
- ChatGPT prompt/output schema not frozen;
- observable model-identity handling not frozen;
- exact XM EURJPY Bid/Ask timestamp and account-cost route not qualified;
- deterministic implementation/synthetic tests not yet present;
- independent pre-outcome audit not yet run.

## Next action

Complete Packet B source/prompt qualification, then Packet C outcome-blind implementation. After an independent PASS, present the final unresolved choices for human freeze. No formal market outcome should be opened before that boundary.
