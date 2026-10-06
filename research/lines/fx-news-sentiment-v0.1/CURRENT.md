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
- Outcome-blind deterministic core: SYNTHETIC_CORE_PASS.
- Synthetic test result: 24/24 PASS on Python 3.13.5.
- Market outcome access during implementation: NONE.

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

The deterministic outcome-blind core now implements:

- headline cutoff validation;
- exact-URL deduplication;
- fixed sentiment enums;
- SNB-style appreciation/depreciation score aggregation;
- EURJPY LONG / SHORT / NO_TRADE selection;
- signal-freeze timing guard;
- exact quote validation and first-quote-at/after-target selection;
- 60-second quote tolerance;
- spread-aware LONG/SHORT return arithmetic;
- midpoint gross comparator;
- visible model-identity change guard;
- canonical JSON SHA-256.

The first synthetic test run exposed six implementation errors caused by Python `str Enum` normalization. Those code defects were corrected without changing the scientific rule, and the complete 24-test suite then passed.

## Evidence state

1. SNB Working Paper 2025/11 provides the direct FX sentiment mechanism prior, but uses fine-tuned Llama and full-text providers.
2. Lopez-Lira & Tang provide peer-reviewed headline-based GPT evidence in U.S. equities.
3. FX headline sentiment work using ChatGPT 3.5 provides direct task-level support, but not a prospective retail trading validation.
4. FINSABER and leakage research are adverse evidence against broad autonomous LLM-trader claims.

Therefore v0.1 intentionally narrows ChatGPT to semantic classification and relies on prospective evidence.

## Remaining blockers

- exact GDELT query/field contract not frozen;
- GDELT runtime source qualification incomplete;
- near-duplicate headline and MAXRECORDS fail-closed rules not frozen;
- ChatGPT prompt/output schema not frozen;
- observable model-identity policy not frozen;
- exact XM EURJPY Bid/Ask timestamp and account-cost route not qualified;
- live GDELT/XM adapters and formal cohort runner not implemented;
- independent pre-outcome audit not yet run;
- human freeze not granted.

## Next action

Complete Packet B source/prompt/XM qualification. The deterministic Packet C core can then be extended only as required by the qualified schemas, followed by an independent pre-outcome audit. No formal EURJPY market outcome should be opened before explicit human freeze.
