# Prior Repository Review — Freqtrade lookahead diagnostic boundary

## Metadata

- Repository: `freqtrade/freqtrade` — https://github.com/freqtrade/freqtrade
- Review date: 2026-09-27 JST
- Reviewed default branch: `5284e4d2721f313488dddf8a1e8c2652314c5cc7` (main observed at start). Local component check: installed Freqtrade **2026.8**, not that main commit.
- Purpose: strategy execution/backtesting and diagnostics for lookahead and recursive indicator behavior.
- Maturity: long-running project; 2025 changes to comparison and order override, 2026 API and pricing-side changes are visible. This review is scoped to diagnostic guarantees, not an audit of all trading features.

## 1. What problem is this repository solving?

**FACT:** Backtests supply the entire historical dataframe to `populate_*`; a strategy can accidentally use future data. `lookahead-analysis` reruns shortened backtests around baseline trades, compares signal/trade timing and indicator dataframes, and reports differences; `recursive-analysis` separately probes indicator sensitivity to startup history. [Code](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead.py), [docs](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/lookahead-analysis.md).

**INTERPRETATION:** The diagnostic tests an observable difference under selected counterfactual reruns; it is not static proof that every value was available at signal time.

## 2. Canonical source of truth

Strategy code, configuration, historical candles and pair selection determine a backtest; its output and the diagnostic table/CSV are generated observations. `has_bias: No` describes differences detected on checked trades under overridden settings, not a canonical certificate of temporal validity. [Output/overrides](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead_helpers.py).

## 3. Current repository structure

Relevant paths: `freqtrade/optimize/analysis/lookahead.py`, `lookahead_helpers.py`, `recursive.py`, `freqtrade/strategy/strategy_helper.py` (informative merge), `freqtrade/optimize/backtesting.py`; tests in `tests/optimize/test_lookahead_analysis.py`, `tests/strategy/test_strategy_helpers.py`, and `tests/strategy/strats/lookahead_bias/`. Documentation in `docs/lookahead-analysis.md`, `recursive-analysis.md`, `backtesting.md`, `strategy-customization.md`. Links in §20.

## 4. Knowledge / data model

The diagnostic's `Analysis` stores checked trade count, differing entry/exit count, differing indicator names and `has_bias`. CSV carries filename, strategy and these counts; it does not carry a catalog of tested signal branches, informative source timestamps, dataset/code hash, environment, or proof of live parity. Too few trades and checking errors have distinct table presentation, but are not ordinary `No`. [Analysis](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead.py), [CSV](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead_helpers.py).

## 5. Research lifecycle

User defines strategy, downloads historical candles, backtests, checks lookahead/recursive behavior, then may forward-test in dry mode. These helpers do not decide whether a hypothesis is valid, preserve preregistration, or establish execution economics. [Strategy docs](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/strategy-customization.md).

## 6. Experiment reproducibility

### What the diagnostic actually computes

**FACT:** `start()` builds a full baseline, requires minimum trades, iterates baseline trade rows until target count, skips forced exits, reruns for each entry/exit with a single-pair selection and shortened timerange, checks whether entry/exit timestamps remain in resulting trades and compares the overlapping full versus cut dataframe columns. It marks `has_bias` when a compared indicator or checked entry/exit differs. The full and cut runs use the same backtesting engine. [Implementation](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead.py).

**FACT:** Configuration overrides disable cache/protections, expand max open trades/wallet, fix stake and force market orders by default. Custom price callbacks associated with limit orders are therefore outside the default route. [Helpers](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead_helpers.py), [docs](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/lookahead-analysis.md).

### Diagnostic Guarantee Matrix

The classifications refer to what **lookahead-analysis passing** establishes, not whether Freqtrade offers another safe helper. `PARTIAL` means an observed difference can be caught under checked paths, not comprehensive detection.

| Property | Assessment | Evidence / boundary |
| --- | --- | --- |
| Direct future-column access | **PARTIAL** | `iloc[-1]`/future column can change on cut data and appear as signal/indicator difference, but only checked trade paths and dataframe columns are examined. [Code](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead.py). |
| Full-dataframe aggregation leakage | **PARTIAL** | `.mean()` without rolling commonly changes with cutoff, and overlapping columns are compared; a branch never exercised or unchanged value is missed. [Code](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead.py), [examples](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/lookahead-analysis.md). |
| Shifted features | **PARTIAL** | Negative `shift` is exercised by upstream regression strategy (`shift(-10)`), but this test does not establish universal coverage. Positive shift looks backward in the same frame, though timing/merge context still matters. [Test strategy](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/tests/strategy/strats/lookahead_bias/strategy_test_v3_with_lookahead_bias.py), [test](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/tests/optimize/test_lookahead_analysis.py). |
| Higher-timeframe / informative-pair leakage | **NOT GUARANTEED** | `merge_informative_pair` shifts the informative candle to its availability boundary; raw `merge_asof` on open timestamps need not. Diagnostic compares values, not source availability timestamps. Component reproduction below. [Merge helper](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/strategy/strategy_helper.py). |
| Incomplete candle usage | **NOT GUARANTEED** | Default helpers aim at closed candles; custom external/merged data can contain unfinalized candle fields and comparison has no availability-time assertion. No full live-feed experiment here. [Merge helper](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/strategy/strategy_helper.py), [#12507](https://github.com/freqtrade/freqtrade/issues/12507). |
| Dynamic pairlist effects | **NOT GUARANTEED** | Slice uses a single pair and assumes behavior matches full pairlist; dynamic backtest pairlists can use current market state and lack historical reproducibility. [Docs](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/lookahead-analysis.md), [backtesting](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/backtesting.md). |
| Backtest / dry-run / live signal parity | **NOT GUARANTEED** | All lookahead reruns are backtests; live fetch/history length and callbacks differ. `recursive-analysis` tests another slice of indicator variance, not full parity. [Code](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead.py), [recursive docs](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/recursive-analysis.md). |
| Fill / execution parity | **NOT GUARANTEED** | Market-order override changes path; backtest assumes fills within OHLC range without slippage and candle ordering/price rules. No order-book/liquidity proof. [Helpers](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead_helpers.py), [assumptions](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/backtesting.md#assumptions-made-by-backtesting). |
| Cost parity | **NOT GUARANTEED** | Backtest includes modeled/default or overridden fees; live fee tiers, spread, slippage and funding/context are not verified by comparison of two backtests. [Backtest docs](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/backtesting.md). |
| Stateful / external side effects | **NOT GUARANTEED** | Reruns create new engine/strategy processing and change pairlist/settings; stateful callbacks, time-dependent data or external effects may differ or stay identically wrong. The diagnostic neither traces external reads nor establishes deterministic replay. [Code](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead.py). |

### Independent component experiment

**FACT — REPRODUCED at component level, Freqtrade 2026.8:** Constructed four 15-minute rows at 00:00–00:45 and one 1-hour row timestamped by its 00:00 **open**, with final `close=999` (only known by 01:00). Plain `pandas.merge_asof(..., direction='backward')` made `999` visible at **all four** rows. Freqtrade's `merge_informative_pair(..., '15m', '1h')` gave `NaN` at 00:00/00:15/00:30 and first placed 999 at the 00:45 candle, whose signal is acted on after 01:00. Passed identical leaked dataframe prefix to the installed `LookaheadAnalysis.analyze_indicators` as full and cut indicator stores: `false_indicators=[]`. This demonstrates that column equality alone has no temporal availability check.

**LIMITATION:** This was a component test with a deliberately identical cut dataframe, **not** a complete `lookahead-analysis` CLI backtest. It does not independently establish whether #12507's precise strategy/data path would yield `has_bias: No` on main. Its stronger conclusion is a logical boundary: when the same unavailable value is present on both compared sides, equality cannot flag it. The helper itself did enforce the safe merge timing in this case.

### Reproducibility scope

Historical data, strategy revision/configuration, fees, pairlist and timerange must be identified to repeat an experiment. The diagnostic CSV does not itself pin those inputs. Same-frame `shift(-n)`, full-frame aggregation and indicator comparison are relevant, but no universal temporal type/availability check exists in the inspected code. Freqtrade's `recursive-analysis` probes history-length effects; its docs caution that output is indicator variance, not full backtest or live signal verification.

## 7. Negative / failed research

Too few trades produces a failed test display; errors likewise differ from `No`. The implementation keeps counters and CSV, but does not provide a first-class preserved negative scientific hypothesis or complete diagnostic failure ledger. [Helpers/tests](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/tests/optimize/test_lookahead_analysis.py).

## 8. Current knowledge vs history

Version control and exported backtest files can retain historical observations. No built-in current-valid scientific conclusion versus superseded result relation was established for the diagnostic. A fresh result should not silently supersede historical context without strategy/data/config identity.

## 9. AI / agent role

No AI judgment is part of the inspected lookahead algorithm. An agent can call CLI/API and receive `No`, but that output is bounded by sampled trades and simulation configuration; AI should not promote it to universal absence proof.

## 10. Deterministic execution boundary

The engine computes indicators and orders according to code/data and fixed backtest assumptions. The diagnostic reruns the engine rather than reading strategy syntax. If both baseline and shortened runs contain the same semantically invalid source value, deterministic agreement is possible; if a model/external service changes between runs, differences need not be temporal leakage.

## 11. Human-facing interface

CLI/freqUI table reports `has_bias`, checked trade count and differing columns. CSV exports these values but not per-branch coverage or temporal source-availability assertions. Docs explicitly warn that untriggered signals can yield false negatives, pairlist dependence false positives, and default market-order override excludes custom pricing callbacks. [Docs](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/lookahead-analysis.md).

## 12. AI-facing retrieval

Structured CSV/API output exists, but it gives observed comparisons rather than a comprehensive machine-readable guarantee statement. No dedicated MCP/provenance retrieval guarantee was verified in inspected paths.

## 13. Issues / discussions findings

| Issue | Reporter claim | Maintainer response / status | Fix, tests, current behavior | Independent status |
| --- | --- | --- | --- | --- |
| [#12507](https://github.com/freqtrade/freqtrade/issues/12507) | In Freqtrade 2025.10, raw `merge_asof` of 1h body into 15m exposes unclosed 1h close while diagnostic says `No`. | [xmatthias](https://github.com/freqtrade/freqtrade/issues/12507#issuecomment-3518197487) explained candle-open timestamps, recommended `merge_informative_pair`; cautioned that unchecked trade paths can show `No`. Closed as question, not accepted core fix. | Main helper shifts 1h open time by 1h minus 15m; [helper test](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/tests/strategy/test_strategy_helpers.py) asserts first 3 rows empty, then prior 1h candle. No issue-specific merged fix/regression test identified. | **NOT_REPRODUCED** as end-to-end diagnostic; component timing/equality **REPRODUCED** (above). |
| [#12894](https://github.com/freqtrade/freqtrade/issues/12894) | Freqtrade 2026.1 5m/30m strategy reportedly had dry-run signal mismatch despite `has_bias: No`; reporter asserted 644 backtest candles matched own script. | [xmatthias](https://github.com/freqtrade/freqtrade/issues/12894#issuecomment-3989559137) requested actual reduced strategy and evidence; [closed for inactivity](https://github.com/freqtrade/freqtrade/issues/12894#issuecomment-4028994466). Attachment claimed in text was not present to maintainer. | No issue-linked verified fix/regression test identified. Main diagnostic still only runs backtests; separate recursive tool checks indicator history sensitivity. Exact reporter root cause remains unknown. | **NOT_TESTED** exact case: strategy/config/dry-run signal series unavailable; no basis to call it reproduced. |

**LIMITATION:** PR search by issue number found no reliable issue-linked fixes; this is not proof that no related changes exist. Both reporter claims are separated from established behavior.

## 14. Commit-history findings

**FACT:** [PR #12126](https://github.com/freqtrade/freqtrade/pull/12126) merged in 2025, replacing only-last-row indicator comparison with full overlapping dataframe comparison; current source uses `DataFrame.compare`. [PR #12229](https://github.com/freqtrade/freqtrade/pull/12229) merged later to force market orders and reduce false positives; [implementation commit](https://github.com/freqtrade/freqtrade/commit/a2c3729254728ebc1520bd48945ccc6f6f3c9657) explicitly acknowledges possible false negatives in pricing callbacks. [2026 pricing-side correction](https://github.com/freqtrade/freqtrade/commit/0fe47b35186e2eb4545f127a3a5c647469a83cdc) and [API endpoint](https://github.com/freqtrade/freqtrade/commit/86f4353cc6eff5ebd0a4e5e6d05ae4dcb9ac7ae0) show continued behavior/interface changes. No motive beyond documented PR/commit descriptions is inferred.

## 15. Failure cases / abandoned approaches

Last-row-only comparison was superseded by full overlapping-row comparison. Default limit/custom-price path was intentionally disabled to reduce false positives, trading coverage for stability. No proof that #12507 or #12894 received a dedicated fix. Inactive issue closure is not validation of reporter's hypothesis.

## 16. Strengths

Real backtest reruns expose many noncausal vectorized indicators without relying on regex/static code inspection; full dataframe comparison improves sensitivity; too-few-trades path avoids an ordinary green `No`; safe informative merge helper plus timestamp tests address a concrete class of HTF timing errors.

## 17. Limitations

Coverage follows sampled trades, pairs, time ranges and overridden execution path. No assertion on when source information became available. No proof of dry/live signal parity, order fills, fee/cost realism, external state or all signal branches. Component test and source support a blind spot; no full CLI reproduction of either Issue. Tool version 2026.8 is behind inspected main.

## 18. Transferable lessons

| Class | Lesson and evidence |
| --- | --- |
| STRONG_COMMON_PRINCIPLE | Record what was checked and what was not; baseline/cut equality only attests to a sampled comparison, as source and tests show. |
| STRONG_COMMON_PRINCIPLE | Treat availability timestamps and candle-close semantics as experiment specifications; raw merge and helper produced different as-of values at the same signal row in an independent component test. |
| PLAUSIBLE_PATTERN | Keep a diagnostic result with dataset/strategy/config identity, checked branches, overrides and untested paths; Freqtrade CSV omits several of these. |
| PROJECT_SPECIFIC | Freqtrade's forced market orders/wallet and single-pair reruns solve particular comparison artifacts while changing the execution path. |
| DO_NOT_COPY | Interpret `has_bias: No` as a certificate of no temporal leakage or live execution parity; the comparison does not check source availability or live execution. |

**INTERPRETATION:** The evidence supports, rather than refutes, the provisional separation of diagnostic PASS, temporal semantics, computation/evidence correctness and live parity. Importantly, the safe informative merge helper and tests are affirmative counterweights: tool-level design can prevent a specific leakage class even when the diagnostic alone cannot prove absence. No evidence contradicting the five stated provisional principles was found.

## 19. Questions for cross-repository synthesis

Can event-time/availability-time of every informative feature be recorded and checked? What minimal branch/pair/candle coverage is useful for a diagnostic certificate? How should baseline/cut agreement be paired with a live/dry signal capture and fill/cost comparison? Can recursive indicator differences be linked to historical sample identity without claiming full parity?

## 20. Sources reviewed

- Project main fresh read at `24741a4f1022e703cac048181e54c5a54d88feac`: [README](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/README.md), [ROADMAP](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/docs/ROADMAP.md), [principles](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/docs/RESEARCH_PRINCIPLES.md), [prior-art README](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/README.md), [template](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/TEMPLATE.md), [queue](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/WORK_QUEUE.md), [candidate scan](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/CANDIDATE_SCAN.md), completed reviews [Trading Second Brain](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/trading-second-brain.md), [zestoles/quant](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/zestoles-quant.md), [Epsilon](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/epsilon-quant-research.md), [DVC](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/dvc.md), [RD-Agent](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/rd-agent.md). [Synthesis v0.1](https://github.com/Josh-Temple/systematic-trading-research/blob/24741a4f1022e703cac048181e54c5a54d88feac/research/prior-art/SYNTHESIS_V0.1.md) also read, unchanged.
- Freqtrade pinned current code: [diagnostic](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead.py), [helpers](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/optimize/analysis/lookahead_helpers.py), [safe informative merge](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/freqtrade/strategy/strategy_helper.py), [diagnostic tests](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/tests/optimize/test_lookahead_analysis.py), [merge tests](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/tests/strategy/test_strategy_helpers.py); [lookahead](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/lookahead-analysis.md), [recursive](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/recursive-analysis.md), [backtesting](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/backtesting.md), [strategy](https://github.com/freqtrade/freqtrade/blob/5284e4d2721f313488dddf8a1e8c2652314c5cc7/docs/strategy-customization.md). Issues, maintainer responses, PRs and commits in §§13–14.

## Review status

**PARTIAL.** Current implementation and tests inspected; temporal merge and diagnostic column-comparison blind spot independently checked at component level. Neither issue's full strategy-level behavior was independently reproduced; live/dry execution and costs were not run. The report limits claims accordingly.
