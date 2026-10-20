---
id: PKT-CSM-R
type: WorkInstruction
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: SEQUENTIAL_CONDITIONAL_PACKET
relations: []
---

# Independent reviewer / Sol — post-result interpretation

## Role / branch / allowed GitHub paths
Role: Independent reviewer / Sol — post-result interpretation。専用branch: `review/csm-result-002`。
書込allowlist（全て本line直下）: `interpretations/INT-CSM-002-*.md; work/post-result-review/**`。

## Required fresh reads / authority
開始時に `Josh-Temple/systematic-trading-research` のmain SHAをfresh readし、README、docs/RESEARCH_PRINCIPLES.md、schema/v0.1/README.mdを読む。さらに本lineのREADME、ARCHITECTURE_REVIEW_2026-10-01.md、specifications/SPEC-CSM-002-v01.md、decisions/DEC-CSM-002.md、本Packetを読む。関連sourceだけを追加取得し、Memoryを現在状態の根拠にしない。
本計画がmain未統合なら、人間が指定したarchitecture PRのexact head SHAからPacketと仕様を取得し、`proposal_ref` と `main_sha` を別々に記録する。mainの正本と同一扱いしない。既存 `research/currency-strength-momentum-v0.1` branchのSPEC-CSM-001を実行契約に使わない。required file欠落、重要なmain変更、ref不一致ならその依存部分をBLOCKEDとし他の独立項目は継続。
成果には閲覧したref/URL/日付、コードの実行有無、access receiptを残す。現時点のhuman承認やgateが存在しないことを、仮定で補わない。

## Common forbidden actions
canonical scientific specification、hypothesis、data role、universe、horizon、period、decision ruleを独自に変更しない。他worker path、Horizontal Reaction/H3/DATA-HR-003、Autonomous Pilotのmarket/hidden inputs、既存Web、MCP、live/paper orders、broker connection、position sizingを触らない。
forward return、strategy P/L、Sharpe、best parameter/period/subgroup、current currency-strength rankingを計算しない（X/Rの明示的例外だけ後述）。価格plot、performanceによるsource比較、同sample救済は禁止。
tokens/timeの都合で一項目だけ処理して完了扱いにしない。Packet全scopeを最後まで処理する。個別gapはsource/理由/次の検証方法を記録し、独立項目を継続。必須条件のgapをPASSへ書き換えない。

## Failure semantics / completion / verification
成果のstatusはCOMPLETE、PARTIAL_WITH_GAPS、BLOCKEDを区別。scientific outcomeを生成しない準備成果は `scientific_status: NOT_APPLICABLE`。access失敗やtests失敗をnegative strategy resultにしない。FACT、INTERPRETATION、LIMITATIONを分け、reporter claimとindependent reproductionを明示。
全taskをPASS / GAP / NOT_APPLICABLE / BLOCKEDのmatrixにし、未完を隠さない。resultにはinput refs、source evidence、deliverable paths/hash、changed files、許可された読取範囲、禁止outcomeを見なかった確認を含める。
専用branchを指定base SHAから作り、自分のallowed pathsだけcommit。force push/main直接write/mergeは不可。PRを作成してよいが、他workerの科学的承認を代行しない。main未統合なら同じarchitecture branchをbaseとするstacked PR、統合後ならfresh mainをbaseとする。architecture baseを変更する場合はexplicit receipt。
push後にremote exact headから全deliverableを全文readback、local bytes/hashと照合し、差分がallowlist内か確認。成功したpush、PR URL、head SHA、readback結果を報告する。保存できなければ未保存と明記し、COMPLETEとしない。

## Outcome-access permission
X終了後にfrozen Result/Run/metric/outcome/event ledger閲覧可。new market price retrieval、別outcome/variant計算、再最適化不可。既存ledgerの算術・rule照合はverificationとして可、探索や第二empirical runとして扱わない。

## Objective / required reads
実験担当Xと異なるsessionで、結果の有効性、限定解釈、次の許容行動を評価。可能ならSolが担当。fresh main、frozen HYP/SPEC/EXP/DATA、human/gate/E audit、X actual-code/data/output hashes、attempt/access ledger、Result全文を読む。summaryや良いmetricだけで判断しない。

全項目:
1. run一回、試行漏れ、source/code actual-use identities、partial results/retries、snapshot保存、data-role/accessを確認。
2. count/skip/calendar/direction/logbps、selection ledger-before-outcome、bootstrap settings、sufficiency、predefined ruleを照合。異常の任意除去やhorizon変更不可。
3. execution_status/evidence_validity/scientific_statusを独立評価。BLOCKED/invalid/provenance不足なら科学結論を出さずcorrection提案。
4. FACT: predefined mean/CI/count/median/positive-rateとexact decision threshold。INTERPRETATION: priorとの一致/不一致、共通因子、risk premium、concentration、era/regime、reference timing/revision。LIMITATION: causality、execution、funding、G10一般化、intraday、sample/power、bootstrap stationarity。
5. uniform random expected0はrisk-matched alpha benchmarkでない、max pair同値は別mechanism証拠でない、spot positiveはnet total-return証拠でないことを確認。
6. 次の許容行動を下記branch rulesへmappingし、同sample posthoc conditionを「検証済み」にしない。
7. prior文献のgapが残る場合も結果後の解釈をhindsightでspecに書き戻さない。scientific contradictionを明示してclaimのscopeを制限する。

## Precommitted post-result branches
**Valid negative:** exact SPECをNOT_SUPPORTED/DEPRIORITIZE、terminal recordに保存。same sampleのhorizon/universe/vol/regime/source rescue禁止。新しい独立仮説へ移るなら別事前契約とunused証拠、またはline終了。negative平均は普遍的momentum不存在ではない。
**Weak/inconclusive:** meanpositive/CI含0と、n/coverage不足を区別。HOLD、arbitrary horizon検索/sample延長禁止。外部情報で別研究を提案できるが同sampleでconfirmedにしない。
**Invalid/operational:** source/code/provenance repairを別correction/run identityで提案。既知outcome exposureを残し、「最初のclean test」をやり直したと称さない。
**Positive:** PROMISING_EXPLORATORYだけ。順序は(1) public-information timingとBIDASK/commission/slippage/financing/carryの経済screen設計、(2) factor momentum/dollar/carry/残差のdecomposition設計、(3) 必要なら事前固定top-k basket、(4) independent unused confirmation、(5)別許可によるprospective shadow。1/2の仕様準備は並列可、outcome・判断はserial。observed discoveryを追加filter選択に使わない。
net unsupportedならexecution specificationを終結、残差なしなら独自currency mechanism claimを却下。confirmationのsample/power/効果thresholdは今のResultから都合よく決めずhuman契約にする。

## Exact deliverables / completion
- interpretations/INT-CSM-002-<review-id>.md: interprets_result relation、facts/interpretation/limits、validity、bounded claim。
- work/post-result-review/RESULT.md と REVIEW_MATRIX.md: 全7項目、errors/correction recommendations、post-result branch mapping。
Current/DecisionはIntegratorが更新。ここではscience条件/decision ruleを書換えずrecommendationのみ。full-scope/remote readbackとResultのscopeを保った解釈まででCOMPLETE。
