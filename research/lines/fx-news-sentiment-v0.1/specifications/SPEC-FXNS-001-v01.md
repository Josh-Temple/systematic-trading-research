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

Does a fixed ChatGPT classification of point-in-time FX **headlines** produce a deterministic EURJPY signal with positive prospective executable value after qualified trading costs?

This tests one workflow, not "ChatGPT trading" in general.

## 2. Prior-art relationship

EUR/JPY is chosen before any prospective outcome because the primary SNB FX-sentiment paper explicitly illustrates this pair under a sentiment-difference rule.

The candidate adapts rather than replicates that paper:
- SNB uses full-text provider content and a fine-tuned Llama;
- v0.1 proposes GDELT title/headline metadata and an off-the-shelf ChatGPT product model.

That substitution must be judged prospectively.

## 3. Event schedule

- timezone: Asia/Tokyo;
- eligible issuance days: Monday through Thursday;
- information cutoff: 08:00:00 JST;
- classification/signal must freeze before 08:15:00 JST;
- shadow entry target: 08:15:00 JST;
- shadow exit target: 08:15:00 JST on the next eligible calendar day;
- Friday issuance excluded to avoid a structurally different weekend horizon.

Late issuance: `LATE_ISSUANCE_NO_SCORE`.

## 4. News input

Preferred candidate source: GDELT Article List / DOC API.

Candidate window:
- GDELT DOC records in the exact 24-hour window ending at the current cutoff; Monday is also 24 hours, not since the previous issuance;
- GDELT seen timestamp, not inferred publisher time, controls eligibility;
- English-language query;
- candidate query / MAXRECORDS / deduplication are locked for qualification in `work/SOURCE_QUALIFICATION_RESULT.md`, but runtime completeness and boundary semantics remain unqualified.

For each input record preserve at least:

- event-local ID;
- GDELT seen timestamp;
- title;
- URL;
- source domain/outlet if supplied;
- retrieval timestamp;
- raw-response artifact SHA-256;
- query/version identity.

Underlying publisher article body is not part of v0.1 model input.

If the frozen query reaches an unresolved output cap or response completeness cannot be established, the event fails closed.

## 5. ChatGPT classification

Input to ChatGPT is the frozen headline record only.

For EUR and JPY separately emit one enum:

- `APPRECIATION`;
- `DEPRECIATION`;
- `UNCHANGED`;
- `NOT_MENTIONED`;
- `INSUFFICIENT`.

Classify the headline's forward implication after availability. Do not turn a purely retrospective price-move description into a forward signal.

Preserve:

- prompt version/hash;
- visible model identifier, if available;
- observable thinking/configuration label;
- issued_at;
- raw structured response;
- validation status.

If the visible product model identity changes during a formal cohort, stop administratively and version the protocol. Unobservable underlying model updates remain an explicit limitation.

## 6. Daily score

For currency i:

`S_i = log(1 + N_appreciation_i) - log(1 + N_depreciation_i)`.

UNCHANGED / NOT_MENTIONED / INSUFFICIENT contribute zero.

## 7. Pair action

Define `sgn(0)=0`.

- LONG EURJPY if `S_EUR > S_JPY` and `sgn(S_EUR) != sgn(S_JPY)`;
- SHORT EURJPY if `S_EUR < S_JPY` and `sgn(S_EUR) != sgn(S_JPY)`;
- NO_TRADE otherwise.

No magnitude/confidence threshold is permitted.

## 8. Executable shadow return

Reference candidate: exact XM MT5 EURJPY Bid/Ask from a qualified account/server route.

Entry within 60 seconds after 08:15:
- LONG: Ask;
- SHORT: Bid.

Exit on the next eligible event day within 60 seconds after 08:15:
- LONG: Bid;
- SHORT: Ask.

Missing exact quote => `MARKET_OUTCOME_UNAVAILABLE`; no provider rescue.

Executable log return, bps:
- LONG: `10000 * ln(exit_bid / entry_ask)`;
- SHORT: `10000 * ln(entry_bid / exit_ask)`;
- NO_TRADE: 0.

Commission/swap/other fees must be qualified separately. Until all relevant costs are known, claims are "spread-aware", not "fully net profitable".

## 9. Ledger and metrics

Keep every eligible event, including NO_TRADE.

Primary:
- mean executable return bps per eligible event, with NO_TRADE = 0.

Secondary:
- executed-trade expectancy;
- LONG/SHORT/NO_TRADE counts;
- win rate;
- midpoint gross vs Bid/Ask executable difference;
- maximum cumulative drawdown in one-unit bps;
- event bootstrap 95% interval.

## 10. Cohort

Recommended for human freeze:
- 60 eligible issuance events;
- no early scientific stop for good/bad performance.

Administrative stop for:
- pre-freeze outcome leakage;
- prompt/rule/source/model-policy mutation;
- mutable issued records;
- unqualified time semantics;
- incomplete/truncated input corpus;
- execution-source integrity failure.

Administrative stop is not a market result.

## 11. Candidate advance rule

Before any formal outcome, human freeze must accept the exact rule.

Recommended minimum:
1. mean event executable return > 0;
2. event-bootstrap 95% lower bound > 0;
3. cost accounting complete enough for the stated economic claim;
4. no unresolved integrity violation affecting the cohort.

Failure cannot be rescued on the same cohort by changing query terms, source, prompt, pair, cutoff, horizon, neutral treatment or threshold.

## 12. Historical-data boundary

Do not inspect historical EURJPY outcomes to choose:
- GDELT query terms;
- 08:00 cutoff / 08:15 entry;
- EURJPY;
- prompt;
- sentiment threshold;
- holding horizon.

Synthetic data may test mechanics only.

## 13. Independence from other research lines

Do not combine price-based `currency-strength-momentum-v0.1`, JP225 research, technical indicators or accumulated Trading results with v0.1 inputs.

Any combined model is a new hypothesis with a new unused/prospective cohort.

## 14. Broker boundary

No order submission, automatic position sizing or live capital action.

Matsui FX portability is a later independent execution question. A positive XM-reference shadow result would not establish Matsui profitability.

## 15. Human freeze

Status remains `PROPOSED_NOT_FROZEN`.

Formal prospective scoring requires:
- GDELT source qualification PASS;
- prompt/output freeze;
- XM quote/cost qualification;
- deterministic implementation + synthetic tests PASS;
- independent pre-outcome audit PASS;
- explicit human acceptance of final query, prompt, model policy, timing, cohort size, cost boundary and advance rule.

### Pre-freeze amendment — 2026-10-07

The initial draft contemplated publisher full-text inputs from a frozen provider allowlist. Source preflight found that the historical DailyFX route is no longer current and that current provider preservation restrictions undermine an auditable public pipeline. Before any formal outcome, the candidate was narrowed to GDELT title/headline metadata. This amendment is pre-outcome and does not consume a sample.

### Packet B pre-freeze clarification — 2026-10-07

Only DOC API `artlist` is the selected candidate route; the separate GAL dataset
and its mixed `date` semantics are not interchangeable. A runtime query returned
HTTP 200 and raw bytes were hashed, but SOURCE PASS is not granted.
Prompt and strict output schema are exact-byte hashed approval candidates, not frozen.
Qualification raw snapshots are not formal events and cannot be backfilled.
GDELT observation and pipeline retrieval timestamps are distinct. Point-in-time
acquisition proof and endpoint behavior remain blockers before formal issuance.
The next-eligible-day Thursday-to-Monday exit versus weekend-avoidance rationale
must be resolved before human freeze; this update does not change the exit rule.
