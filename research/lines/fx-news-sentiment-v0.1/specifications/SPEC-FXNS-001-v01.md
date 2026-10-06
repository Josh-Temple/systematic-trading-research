---
type: Specification
specification_id: SPEC-FXNS-001-v01
research_line_id: RL-FXNS-001
status: PROPOSED_NOT_FROZEN
created_at: 2026-10-07
market_outcome_access: CLOSED_FOR_FORMAL_COHORT
---

# SPEC-FXNS-001-v01 — candidate prospective shadow protocol

## 1. Scientific question

Does a fixed ChatGPT classification of point-in-time FX news produce a deterministic EURJPY signal with positive prospective executable value after qualified trading costs?

This is a test of one workflow, not of "ChatGPT trading" in general.

## 2. Why EUR/JPY

EUR/JPY is chosen before this line sees any prospective outcome because the primary prior-art paper explicitly illustrates this pair under its sentiment-difference rule. It is not selected from this repository's historical EURJPY outcomes.

## 3. Event schedule

Candidate schedule:

- timezone: Asia/Tokyo;
- eligible issuance days: Monday through Thursday;
- news information cutoff: 08:00:00 JST;
- intended classification/signal freeze: after cutoff and before 08:15:00 JST;
- shadow entry target: 08:15:00 JST;
- shadow exit target: 08:15:00 JST on the next eligible calendar day;
- Friday issuance excluded in v0.1 to avoid a structurally different weekend holding horizon.

If the signal is not frozen before the entry target, the event is `LATE_ISSUANCE_NO_SCORE`.

## 4. News input window and source contract

Candidate input window:

- articles with qualified publication timestamps in (previous event cutoff, current event cutoff];
- only sources on the frozen source allowlist;
- only content demonstrably available by the cutoff.

The source allowlist is unresolved until Packet B. Formal scoring cannot begin before it is frozen.

For each article preserve:

- source/provider;
- canonical URL or source ID;
- title;
- publication timestamp with timezone;
- retrieval timestamp;
- exact text span/input shown to ChatGPT where legally permitted;
- otherwise a private snapshot reference plus cryptographic hash;
- extraction status and any truncation.

Date-only items are not eligible for the formal same-day input set.

## 5. ChatGPT classification contract

ChatGPT receives article text plus no post-cutoff prices or outcomes.

For EUR and JPY separately it must emit one enum:

- `APPRECIATION`;
- `DEPRECIATION`;
- `UNCHANGED`;
- `NOT_MENTIONED`;
- `INSUFFICIENT`.

The task is explicitly forward-looking: classify the article's implication for the currency after publication, not describe a move that has already happened.

The frozen record must include:

- prompt version/hash;
- model identifier visible in the product, if available;
- thinking-effort/configuration label observable to the operator;
- issued_at;
- raw structured response;
- validation status.

If the named product model changes during a formal cohort, stop that cohort administratively and open a new protocol version. Unobservable underlying weight changes remain a limitation and must not be falsely claimed as controlled.

## 6. Daily currency score

For currency i:

`S_i = log(1 + N_appreciation_i) - log(1 + N_depreciation_i)`.

`UNCHANGED`, `NOT_MENTIONED`, and `INSUFFICIENT` contribute zero to both counts.

If no eligible article produces APPRECIATION or DEPRECIATION for either currency, both scores are zero.

## 7. Pair action

Define `sgn(0)=0`.

- LONG EURJPY if `S_EUR > S_JPY` and `sgn(S_EUR) != sgn(S_JPY)`;
- SHORT EURJPY if `S_EUR < S_JPY` and `sgn(S_EUR) != sgn(S_JPY)`;
- NO_TRADE otherwise.

No magnitude threshold is permitted in v0.1.

## 8. Reference and executable shadow return

Formal reference feed candidate:

- exact XM MT5 EURJPY Bid/Ask from a qualified user account/server route.

Entry:

- LONG: Ask at first valid quote at/after 08:15:00 JST within 60 seconds;
- SHORT: Bid at first valid quote at/after 08:15:00 JST within 60 seconds.

Exit on next eligible event day:

- LONG: Bid at first valid quote at/after 08:15:00 JST within 60 seconds;
- SHORT: Ask at first valid quote at/after 08:15:00 JST within 60 seconds.

If the exact quote is unavailable within tolerance, result is `MARKET_OUTCOME_UNAVAILABLE`; do not replace it with another provider.

Primary executable log return in basis points:

- LONG: `10000 * ln(exit_bid / entry_ask)`;
- SHORT: `10000 * ln(entry_bid / exit_ask)`;
- NO_TRADE: 0.

Any account commission/swap/other fee must be independently qualified. Until complete costs are known, the result is "spread-aware" rather than "fully net profitable".

## 9. Event ledger and primary metric

Every eligible issuance day remains in the ledger, including NO_TRADE.

Primary metric:

`mean_event_executable_return_bps` across all eligible scored events, with NO_TRADE = 0.

This prevents the system from improving the headline result merely by dropping low-confidence or difficult days after the fact.

Secondary:

- mean return per executed shadow trade;
- number and rate of LONG / SHORT / NO_TRADE;
- win rate on executed trades;
- midpoint gross versus Bid/Ask executable return;
- maximum cumulative drawdown in bps under one-unit notional;
- session/event bootstrap interval for the mean.

## 10. Candidate cohort and stopping rule

Before human freeze, the cohort size remains proposed.

Recommended v0.1 cohort for human acceptance:

- 60 eligible issuance events;
- no early scientific stop for favorable or unfavorable results.

Administrative stop:

- outcome leakage before signal freeze;
- changed prompt/rule/source set/model identity policy;
- mutable issued records;
- unqualified timestamp semantics;
- source input that cannot prove pre-cutoff availability.

Administrative stop is not a negative market result.

## 11. Candidate advancement / rejection rule

Before the first formal outcome, human freeze must decide the exact rule.

Recommended minimum:

Advance only if, over the fixed cohort:

1. primary mean event executable return > 0;
2. event-bootstrap 95% lower bound > 0;
3. observed spread/cost accounting is complete enough for the economic claim being made;
4. no unresolved integrity violation affects the cohort.

Otherwise do not rescue the cohort by changing provider, prompt, pair, cutoff, horizon, neutral treatment, or threshold and calling the revision validated.

## 12. Historical-data boundary

No historical EURJPY outcome may be searched to choose:

- cutoff;
- 15-minute processing delay;
- source provider;
- pair;
- prompt;
- sentiment threshold;
- holding period.

Historical/synthetic data may be used only for pipeline mechanics where market outcomes cannot influence scientific choices.

## 13. Relationship to currency-strength research

This line is independent of `currency-strength-momentum-v0.1`.

Do not combine price-based currency strength with news sentiment in v0.1. Any later combined model is a separate hypothesis and requires a new unused/prospective cohort.

## 14. Broker boundary

No order submission, automatic position sizing, or live-capital action is authorized by this specification.

Matsui FX portability is a later execution-replication question. A positive XM-reference shadow result does not establish Matsui net profitability.

## 15. Human freeze

This specification is currently `PROPOSED_NOT_FROZEN`.

Formal prospective outcome scoring begins only after:

- source qualification PASS;
- deterministic implementation and synthetic tests PASS;
- independent pre-outcome audit;
- explicit human acceptance of the final source set, prompt, timing, cohort size, cost contract and advancement rule.
