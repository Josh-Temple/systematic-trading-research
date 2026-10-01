---
id: RESULT-CSM-B-001
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PARTIAL_WITH_GAPS
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: NOT_APPLICABLE
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
---

# GitHub prior-art / failure review (Packet B)

## 要約

Nate EmmaのFX framework、pmorissette/bt、Freqtradeの3実装をコード・テスト・履歴まで確認した。追加screenとしてQuantConnect/LeanのForex instrument・fee・brokerage実装も調べた。

確認したのは各repoが実装・テスト・報告として何を保証するかであり、市場edgeの有無ではない。Nate Emmaのperformance numbers、paper-accountの報告値、Freqtrade Issue #12894は独立再現していない。記録された失敗は第三者報告・コード変更として扱い、independent reproductionと区別した。

## Authority / fresh-read receipt

- 作業開始時のmain SHA: 1bba695ea252863c3b7366b8b910aa36e211c325。
- 指定Packetは同一mainの子commit 36240da15fc83120d12d081c227f3e0dd8badaaaにあり、PR #31のopen draft headだった。PR headのparentは作業開始mainと一致する。
- proposal_refとmain_shaを分けた。mainにはline planが存在しない。worker branchは指定proposal headから作成し、PR #31をbaseにstackする。
- mainのREADME、docs/RESEARCH_PRINCIPLES.md、schema/v0.1/README.md、research/prior-art/README.md、freqtrade.md、SYNTHESIS_V0.2.mdを読んだ。proposal refのline README、ARCHITECTURE_REVIEW_2026-10-01.md、SPEC-CSM-002-v01.md、DEC-CSM-002.md、GITHUB_PRIOR_ART_2026-10-01.md、work/README.md、Packet本文も読んだ。
- 先行reviewは探索の手がかりに留め、各repoのfresh default ref・source・tests・commit/issue記録で再確認した。提案仕様と市場gateは変更していない。

## 実行境界

閲覧したのはGitHub上の公開README、source、tests、commits、PRs、issuesのみ。市場価格データを取得せず、strategy return、current ranking、Sharpe、pair selectionを計算していない。Nate Emma、bt、Freqtradeのrepository test suiteも実行していない。private account statement、credentials、H3、DATA-HR-003、Autonomous Pilot、Web/MCPは閲覧・変更していない。

このPacket用に標準ライブラリだけの合成invariant checksを4件実行した。これらは外部repository codeの実行・独立replicationではない。記録済みthird-party performanceは閲覧したが、すべてsource-reportedとして扱う。

## 完了matrix

| # | Packet項目 | Status | 確認内容・残る範囲 |
|---|---|---|---|
| 1 | Nate Emma current code / tests | PASS | README、momentum strategy/features/basket、simulator、spot quote、financing、関連testsを確認。市場データなし、repo suite未実行。 |
| 2 | intraday negative、bfill修正、monthly verdict | PASS | exact commits、current code/tests、保存済みverdictを照合。未保存のthrowaway scriptとraw inputsは確認できず、成績は再現していない。 |
| 3 | backtest/live/paper、FX-only/account、financing history | PASS | public README/docs/codeと該当commitを照合。paperとreal-moneyを分離し、NAVの混合・修正履歴を確認。private statementやgitignored forward logsの独立照合はしていない。 |
| 4 | bt momentum, lag, costs, PR #572, holding cost fixes | PASS | current master source/tests、PR/commit diffとhistoryを確認。suite未実行。equity-oriented cost defaultsをFXへ転用しない点を記録。 |
| 5 | Freqtrade current default, lookahead, HTF, Issues #12507/#12894 | GAP | develop source/tests/docsとissue履歴を確認。current helper regression testsあり。Issue #12894とfull CLI behaviorは再現していない。 |
| 6 | 追加repo screen / 3+実装比較 | PASS | QuantConnect/LeanのForex quote, fee, fill/slippage, tests, relevant historyをscreen。これはexecution modelの先行例で、currency momentumの結果ではない。 |
| 7 | synthetic independent checks | GAP | 4/4 generic toy invariants passed。外部source codeをtestしていないためsource-level independent reproductionはNOT_REPRODUCED。 |
| 8 | 共通原則、repo固有、模倣しない点、test checklist | PASS | FAILURE_TEST_CHECKLIST.mdを作成。 |
| | 総合 | PARTIAL_WITH_GAPS | Freqtrade end-to-end reproduction、Nateの未保存計算、paper account raw recordの独立検証は未完。strategy outcomeでなく証拠取得・再現範囲のgap。 |

## Repository findings

### 1. nateemma/fx-strategy-framework

Fresh default main SHA: bb6a431f05d03fcdd765e2f4af3382f32d6a2ab5.

- READMEはpoint-in-time data、backtest、walk-forward、lookahead diagnosticsを持つFX strategy frameworkと説明する。live-related statusはIBKR paper accountであり、real-money permissionは別gateとしている。
- strategies/features/momentum.pyはlookback前との単純price returnを計算する。strategies/momentum.pyはsignalからlong/short weightsを作り、defaultは63-day lookbackとtop-3/bottom-3。これは8通貨から単一max/min pairを選ぶ仕様ではない。
- strategies/features/basket.pyはlongとshortを別々に等ウェイト化する。warmup、符号、dollar-neutrality、少数valid names、causalityをtestしている。
- forex/backtest/portfolio.pyはweightsを1行shiftして次行のspot/carryに適用する。transaction costはweight turnoverに対して計算、carryは年率値を252で割る。optional financingはheld positionのsideに応じたspreadを引く。testsにはlong/short charge、weight lag、financing無しとの一致がある。
- forex/data/prices.pyは価格を「1 foreign currency unitあたりのUSD」にそろえて通貨ごとのinversionを適用し、panelをforward-fillする。これは提案仕様のECB currency-per-EUR sourceと同じdata lineageではない。
- forex/backtest/financing.pyは2026-08-16に取得したとするIBKR published tier scheduleを定数化し、FRED rate seriesをas-of joinして日次holding costを計算する。これは別のbroker economicsモデルであり、reference-rate screenのcost sourceではない。
- current strategies/carrymom.pyはspot momentumでなく、carry signal/rate differentialのlookback changeをrankする。carry-momentumの結果をprice-momentumの結果と混ぜない。
- Commit b723aa48c3a08bc63d11bbaa2233245a80871233はassessment planを更新し、1h・2y・7 majorsのcost-blind rank-ICがnegativeでmomentum premiseをrejectしたと記録する。diffはdoc更新で、raw output/data/reproduction artifactは含まれない。これは月次reference-rate screenのnegative resultではない。
- Commit 74d3c0f8da65a35b8a95955fbf0606ebaa0d9e5cはHAR volatility forecast warmupのfuture-fill bfillを除き、causal EWMA fallbackへ変更した。対象はML volatility overlayでありmomentum featureではない。current testsにはsynthetic-view truncation causality checkがあるが、このcommit用の明示的warmup regression testは見つからなかった。
- project_fx_momentum_verdict.mdはdaily 1971–2026のG10 currency basket、daily/monthly cadence、turnover cost、同sample hyperoptの結果を報告する。top/bottom basketはsingle-pair max/minと別物。著者がmonthly diagnostic scriptをtemporary /tmpへ置き、保存しなかったと記す。数値はsource-reportedであり、このsessionの再計算ではない。
- 後続のcarry_momはrate-differential change predictorであり、過去のprice-momentum評価と直ちに矛盾するものではない。
- Commit 17f1a22...はFX-only reportingを追加。以前のNAVはFXと複数ETF sleeveを混ぜていた。Commit f90d394...はsettled FX spotがpositionsでなくcashに記録される点を修正し、FX legs/P&Lを更新した。current snapshot_nav.pyは両seriesを分ける。
- docs/scheduled-paper-track.mdはpath-change outageの履歴を記し、manual rebalanceでもfreshness checkがhealthyに見える制約を明記する。nav.csvとtrack.logはgitignored。public GitHub記録はpaper forward trackを示すが、raw persistent statement/ledgerはこのreviewでは利用できない。
- docs/financing-spread-findings.mdは初期account interest measurementをsimulatedとして説明し、後にIBKR published scheduleと一致したと報告する。commit f15e798...はその著者報告を記録するが、broker statementを独立確認したものではない。READMEはcarry_cot_mom returnをpre-financingと明記する。これらの数値は今回の提案戦略と無関係。

### 2. pmorissette/bt

Fresh default master SHA: 4c4ad3621ed9d9b78b73610ae69e49746acd4169.

- SelectMomentumはStatTotalReturnとSelectNを組み合わせ、[now - lookback - lag, now - lag]のtotal returnでtop-Nを選ぶ。default lagはzero。これはrow-dateの意味は決めるが、closeの公表時刻や実際に注文できる時刻までは定義しない。
- defaultはtop-N selectorで、single strongest-minus-weakest FX tradeそのものではない。testsはsimple return、lag、history不足、nonfinite weightsを扱う。
- Backtestのdefault transaction costはzero。flat commission callbackとnonlinear CostModelはoptional。generic CostModelはvolumeとvolatilityを要し、docsのexampleはliquid US equity向けhalf-spreadを置く。FXのspread/carry calibrationには使えない。
- CouponPayingSecurityのcost_long/cost_shortはholding-cost経路であり、完全なFX rollover modelではない。Commit 497e75...はcost inputのindex alignment検査を追加し、long/short両方向の回帰testを加えた。
- Commits 7d8785...と2be1fb...はfinite holding cost checksとnested/paper strategyの事前検証を追加。de4655...はtransaction cost計算をposition state変更より前に移した。current testsはこれらのfailure behaviorを確認する。
- Commit a74f8a...はnonfinite multi-period momentum weightsを正規化/再balance前に拒否し、position stateが変わらないことをtestする。
- PR #572は8053f4f...としてmerge済み。動的strategy subtreeがcommission callbackを引き継がず、static経路だけfeeを請求していたregressionを修正した。current testはdynamic経路とpaper copyを比較する。PR本文は328 tests等の成功を報告するが、このsessionでは実行していない。
- 移転できる原則は、costが各経路で適用されるかと、入力indexが揃っているかをtestすること。FXにequity cost valuesをコピーしない。

### 3. freqtrade/freqtrade

Fresh default branchはdevelop、SHA f6a7b767a31720b2f34059dd7b166b28abef3f09。repository metadata上のdefaultはdevelop。main branch lookupは404だった。

- current lookahead codeはfullとtruncated backtestのmatching rowsでdataframeを比較する。Commit 5e5137edc134e5e03b508a66b3594f21d80e2c1eはlast-row-onlyからfull-dataframe comparisonへ変更した履歴。
- official docsはtriggerされたentry/exitごとにsingle-pair verification runを行い、indicator値やsignal dateの変化を比較すると説明する。defaultでmarket ordersを強制し、custom limit-price callbackは対象外。untriggered signalは見逃す可能性、single-pairとcross-pair rankingの違いなどを明記している。
- current merge_informative_pairはinformative merge keyをinformative timeframe minus base timeframeだけ後ろへずらす。15m/1h testは初めの3行にhourly candleがなく、その後4行でprior hourly openを維持することを確認する。open-time stampの場合、hourly closeは00:45の15m candle close boundaryで利用可能になる。
- Issue #12507の投稿者はraw merge_asof(direction=backward)で未完了higher-timeframe candleのopen timestampを使い、lookahead analysisがpassしたと報告。maintainerはavailability shiftとmerge_informative_pair / @informativeを案内し、未triggered signalのfalse negativeも説明した。報告対象はraw merge pathでありcurrent helperのregressionではない。
- Issue #12894はlookahead passにもかかわらずdry-run/backtest signalsが異なると報告する。maintainerがstrategy reproduction等を求め、inactiveのためclose。未検証でありこのsessionでも再現していない。
- 前回のfreqtrade component reproductionは、以前のreviewがinstalled 2026.8上で行ったもの。このPacketの新規再現ではない。本sessionはcurrent develop source/tests/docs/issuesを読んだが、Freqtrade CLIは実行していない。
- lookahead-analysisのpassは「設定されたrerunで検査された範囲に差が見つからなかった」を意味する。point-in-time availability、cross-pair equivalence、dry-run/live parity、fill realism全般の証明ではない。

### 4. QuantConnect/Lean — 追加実装screen

Fresh default master SHA: 41c6e603e5671ca7b5d3de0cbe13b3c4b109bba4.

- Forex security、broker fee model、testsがある成熟execution engineとして選定した。4つ目のimplementation familyとしてprice/fee/fill semanticsをscreenする目的で、momentum outcomeのsourceではない。
- BasicTemplateForexAlgorithmはForex dataをQuoteBarsとして説明。current Forex.cs constructor pathはImmediateFillModel、InteractiveBrokersFeeModel、NullSlippageModel、Null margin-interest modelを設定する（brokerage configurationによる変更可能性を含む）。FXCM brokerage/fee codeにはorder supportとquote-currency handlingが別途ある。
- FxcmFeeModel.csはfee schedule source dateを2015と記している。file history上のlisted changesは2018年まで。現行のbroker quoteではなく、dated static configurationの例。
- current tests/regression algorithmsはForex order validation、resolution feeds、currency conversionを扱う。このscreenでは該当するcross-sectional currency strength strategyを確認していない。venue-specific bid/ask、financing、publication、fill evidenceはfresh qualificationが必要。

## Independent synthetic checks

Python 3.12.14で実行。scriptはwork/github-prior-art/toy_checks/run_toy_checks.py、outputはwork/github-prior-art/toy_checks/TOY_CHECK_OUTPUT.txt。

- trailing-return prefix invariance under suffix perturbation: PASS
- max-minus-min cross-sectional pair identity on synthetic values: PASS
- one-row weight lag and turnover-cost path: PASS
- 15m/1h open-time availability-key alignment: PASS

合計4/4。synthetic inputsのみ。外部repo code、provider calendar、market data、strategy performanceは検証していない。

## 独立知見に昇格しなかったclaim

- Nate Emmaのintraday/monthly performanceとaccount financing numbersはauthor-reportedのまま。
- monthly throwaway scriptと元データはrepoにないため、公開artifactだけでは数値を再現できない。
- Freqtrade Issue #12894は未再現。issue closeはresolution evidenceではない。
- Issue #12507はraw merge failureのuser reportとmaintainer guidanceを示す。current helperが誤っている証拠にはしない。
- 以前のcomponent reproductionはそのreviewへ帰属し、このtaskの新規再現ではない。
- Leanのdated FXCM fee scheduleは設定上の注意でありcurrent economicsではない。
- このどのartifactも提案中CSM仕様のmarket outcome evidenceではない。

## Deliverables

- work/github-prior-art/RESULT.md
- work/github-prior-art/REPOSITORY_MATRIX.csv
- work/github-prior-art/FAILURE_TEST_CHECKLIST.md
- work/github-prior-art/toy_checks/run_toy_checks.py
- work/github-prior-art/toy_checks/TOY_CHECK_OUTPUT.txt

Hashesとexact remote readbackはcompletion receiptとPR filesで確認する。変更pathはすべてPacket write allowlist内。
