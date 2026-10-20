---
id: REF-CSM-GIT-002
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PARTIAL_SOURCE_AND_HISTORY_REVIEW
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: NOT_APPLICABLE
relations: []
---

# GitHub prior art / failure result

source/commit/PRを読んだ結果。external backtest、broker、live/paperの独立実行はしていない。記載performanceはauthor-reported。本lineのmarket outcomeは計算しない。

## nateemma/fx-strategy-framework

Default mainをfresh read: `bb6a431f05d03fcdd765e2f4af3382f32d6a2ab5`。

確認: strategies/momentum.py、tests/test_momentum_strategy.py、docs/archive/legacy-memory/project_fx_momentum_verdict.md、100件のcommit履歴から関連message、issues一覧（その取得では項目なし）、以下のexact commit diff。

- [momentum implementation](https://github.com/nateemma/fx-strategy-framework/blob/bb6a431f05d03fcdd765e2f4af3382f32d6a2ab5/strategies/momentum.py): trailing spot return→basket weights、vol-target overlayは別class。defaults63/3/3とsearch spaceがある。parameter sweepを本計画へ移植しない。
- [tests](https://github.com/nateemma/fx-strategy-framework/blob/bb6a431f05d03fcdd765e2f4af3382f32d6a2ab5/tests/test_momentum_strategy.py): synthetic winner/loser符号、warmup、少数valid names、prefix causal check、finite result。
- [intraday negative commit](https://github.com/nateemma/fx-strategy-framework/commit/b723aa48c3a08bc63d11bbaa2233245a80871233): doc diffが1h/2y/7 majorsのcontinuation拒否・reversion cost問題を記録。raw experiment artifact/independent replayは未確認。月次の否定結果ではない。
- [removed bfill](https://github.com/nateemma/fx-strategy-framework/commit/74d3c0f8da65a35b8a95955fbf0606ebaa0d9e5c): future HAR forecastsによるwarmup backfillをcausal EWMA fallbackへ置換。これはML volatility overlayのbug修正であり、intraday negativeや全momentum codeの無漏洩証明ではない。
- [monthly verdict](https://github.com/nateemma/fx-strategy-framework/blob/bb6a431f05d03fcdd765e2f4af3382f32d6a2ab5/docs/archive/legacy-memory/project_fx_momentum_verdict.md): daily/monthly G10 basketを弱いとしてbenched、daily-rebalanceを前提としたhyperoptがmonthly objectiveとずれたと報告。throwaway script未保存の記載があるためauditability gap。1/1 single-pairと同一でない。
- 最新履歴は後にcarry-momentumをblendへ採用した記録も含む。**carry differential change**はprice momentumと別signal。「momentum rejected」と「momentum deployed」を同じ仮説の矛盾と即断しない。
- `f90d3946583072b4f543c7a671216e6d0961ce8b`、`a92e53fd8819e708c55b8ed5f41c26e5f9fc151c`、`f15e798f450dd5626e712d71cd17a1463c939c9b` のmessageでは、account全体とFX-only performance、interest posting reset、financing spread、paperでの利息近似を再点検したと報告。message確認に留まり現行code/statement照合はBのtask。headline pre-financing性能をnetへ流用しない。

**INTERPRETATION:** negative保持、費用を段階化、prefix testsは有用。捨てたscript、parameter sweepによる同sample進行、cash/forward/retail financingの混同は模倣しない。1 repoの結果を科学的truthへ昇格しない。

## pmorissette/bt

Default master: `4c4ad3621ed9d9b78b73610ae69e49746acd4169`。

[Cost_Models docs](https://github.com/pmorissette/bt/blob/4c4ad3621ed9d9b78b73610ae69e49746acd4169/docs/source/Cost_Models.md)、最近50commit、[PR572](https://github.com/pmorissette/bt/pull/572)、[commission fix](https://github.com/pmorissette/bt/commit/9563951b152c22db23b94ebeb17bf21ccabfc803)、[holding-date fix](https://github.com/pmorissette/bt/commit/497e75eecf5d1adeb4a40e78a612ec239a2c9aa3) のdiff/code/testを確認。

**FACT:** default zero cost。configured commissionsがdynamic subtree/paper treeへ伝播しなかったpathを修正し、static/dynamicの費用一致をsynthetic regressionで確認。holding costのdate alignmentをvalidateする変更もある。

**INTERPRETATION:** 「cost設定済み」でも全pathに適用されたことをtestする必要がある。入力costのfinite/nonnegative/time alignment、real/paper pathのidentityを検証する。

**LIMITATION:** 汎用portfolio frameworkでFX data/executionの保証ではない。US equities向けimpact defaultsやvolume assumptionsはFXへ流用しない。suiteは今回実行していない。

## freqtrade/freqtrade

Default **develop**: `f6a7b767a31720b2f34059dd7b166b28abef3f09`。既存repo reviewで固定された旧mainと区別。

現行 [lookahead docs](https://github.com/freqtrade/freqtrade/blob/f6a7b767a31720b2f34059dd7b166b28abef3f09/docs/lookahead-analysis.md) と [Issue12507](https://github.com/freqtrade/freqtrade/issues/12507) をfresh read。existing research/prior-art/freqtrade.mdのcomponent reproduction/commit reviewを既存証拠として再取得し、今回の新規replicationとは区別。

**FACT:** docsはtriggerされないsignalのfalse negatives、cross-sectional pairlist依存、market-order overrideによるcallback除外を明記。Issue12507はhigher-timeframeの未確定closeをmerge_asof backwardで早期に渡す問題を報告。closedはbias不存在の証明ではない。

**INTERPRETATION:** rankingをsingle pairに分割したdiagnosticは本来のcross-sectionと異なる。full/cut一致でも両方が同じ未公表情報を持つならavailabilityは検査できない。

**LIMITATION:** crypto-oriented engine。本testへimportしない。現行コードと全Issueのend-to-end再現はBに残す。既存reviewのreproductionは当時installed2026.8のcomponentのみであった。

## 共通原則と未解決点

1. prefix-invarianceとexplicit availability/date rulesを併用。diagnostic PASSを無漏洩証明にしない。
2. cost-free signal、actual execution、fundingのoutcomeを別entityにする。
3. synthetic polarity/inversion/missing/nonfinite/cost-path testsを実験前に通す。
4. negative、changed objective、removed code、uncommitted calculationを保持し、科学結論の保証範囲を示す。
5. code/data hashesは実際に読んだbytesへ結びつける。framework全体の採用は不要。

**Bに残るgap:** current FX backtest cost/lag/financing code、updated tests、commit chronology、live/backtest報告の一次証拠、他のFX-specific repoの独立例。今回3 repoを見たがFX replicationの比較を完了したとは主張しない。
