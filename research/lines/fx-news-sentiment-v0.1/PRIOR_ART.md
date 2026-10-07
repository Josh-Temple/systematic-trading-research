# Prior art — FX News Sentiment with ChatGPT v0.1

Status: PRE-OUTCOME DESIGN EVIDENCE
Date reviewed: 2026-10-07

## 1. Direct FX evidence

### Ballinari & Maly — FX sentiment analysis with large language models

Source:
- Swiss National Bank Working Paper 2025/11
- https://www.snb.ch/en/publications/research/working-papers/2025/working_paper_2025_11

Relevant design:

- G10 currency sentiment is classified at article level.
- The model distinguishes forward-looking from backward-looking sentiment.
- Daily currency sentiment aggregates appreciation and depreciation counts as:
  `S_i,t = log(1 + CountAppreciation_i,t) - log(1 + CountDepreciation_i,t)`.
- Their portfolio is long positive-sentiment currencies and short negative-sentiment currencies with zero-cost weighting.
- Their EUR/JPY illustration takes no position when the two currency signals share a sign, goes long when the EUR signal exceeds the JPY signal and signs differ, and short in the converse case.
- Portfolio weights for day t to t+1 use articles published on day t.
- Reported trading returns are before transaction fees.
- The strongest results require domain fine-tuning; raw Llama can perform materially worse.

Implication for this line:

This is the primary mechanism prior. It supports testing language-model extraction of forward-looking FX sentiment. It does **not** establish that ChatGPT Plus zero-shot classification will work, nor that the proposed 08:00 JST adaptation is equivalent to the paper.

## 2. General LLM news interpretation evidence

### Lopez-Lira & Tang — Can ChatGPT forecast stock price movements?

Publication:
- Journal of Financial Economics, 2026
- DOI: 10.1016/j.jfineco.2026.104335
- arXiv: https://arxiv.org/abs/2304.07619

Relevant result:

GPT-4 classifications of firm news predict subsequent U.S.-equity return drift in a post-training-cutoff sample. Transaction-cost sensitivity materially affects economic value.

Implication:

LLM text interpretation can carry forward-looking market information in some settings, but the evidence is cross-market and cannot be treated as validation of an FX EURJPY rule.

## 3. Adverse evidence on autonomous LLM investors

### FINSABER

Sources:
- Paper: https://arxiv.org/abs/2505.07078
- Repository: https://github.com/waylonli/FINSABER
- Documentation: https://waylonli.github.io/FINSABER/

Relevant findings/design changes:

- reported LLM-agent advantages weaken materially under two-decade, broader-universe evaluation;
- survivorship, look-ahead and data-snooping controls materially change conclusions;
- transaction costs and risk-adjusted performance are required;
- current FINSABER execution defaults to `next_open` for date-level text where intraday availability is uncertain;
- source timing and order-fill timing are treated as separate contracts;
- LLM call cost can be treated as an economic cost.

Implication:

Do not use same-day prices when article availability is only date-level. Freeze publication-time requirements before scoring. Measure costs explicitly.

### Profit Mirage / information leakage research

Source:
- https://arxiv.org/abs/2510.07920

Reported result:

Several financial LLM agents show large performance decay after the backbone model's training/release cutoff and retain evidence of memorized historical patterns.

Implication:

Historical ChatGPT backtests are weak evidence unless model-training contamination is controlled. This line therefore prioritizes prospective events.

## 4. GitHub / implementation lessons

### TradingAgents / FinMem family

These projects demonstrate practical multi-agent and memory-based financial workflows, but their original short-window backtests do not satisfy the robustness standard required here. Their architectural complexity is not adopted as evidence of edge.

### Look-Ahead-Bench

Repository:
- https://github.com/benstaf/lookaheadbench

Relevant principle:

Evaluate end-to-end financial agents across genuinely unseen periods and document training-cutoff assumptions, prompts and inference settings.

## 5. Design principles extracted

The common principles used by v0.1 are:

1. Use the LLM for a narrow semantic task, not unrestricted portfolio discretion.
2. Separate source availability time from order time.
3. Preserve every input/output with point-in-time provenance.
4. Prefer genuinely prospective data when the model may know historical outcomes.
5. Include Bid/Ask and any account-specific trading cost before profitability claims.
6. Keep NO_TRADE in the event ledger rather than dropping difficult days.
7. Freeze prompt, aggregation, pair rule, horizon and stopping conditions before prospective scoring.
8. Treat model/version changes as research-state changes, not silent implementation details.
9. Do not tune provider, prompt, timing, thresholds or pair on the same scored cohort.
