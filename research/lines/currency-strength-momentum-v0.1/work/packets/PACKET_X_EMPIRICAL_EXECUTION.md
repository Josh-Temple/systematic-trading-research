---
id: PKT-CSM-X
type: WorkInstruction
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: SEQUENTIAL_CONDITIONAL_PACKET
relations: []
---

# Luna Max X — One fixed empirical execution

## Role / branch / allowed GitHub paths
Role: Luna Max X — One fixed empirical execution。専用branch: `work/csm-empirical-002`。
書込allowlist（全て本line直下）: `runs/RUN-CSM-002-ATTEMPT-*.yaml; results/RES-CSM-002-ATTEMPT-*.md; artifacts/EXP-CSM-002/**; datasets/DATA-CSM-002/snapshots/**`。

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
Iのfrozen gate PASSとhuman確定がある場合だけ、frozen範囲のECB snapshotをdeterministic codeへ渡しpredeclared y/metricsを一回計算可。human/modelがraw values/current ranking/plotsを見ることは不要で禁止。別期間・別source・parameter・subgroup・holdoutは不可。

## Objective / required reads
科学条件を変更せず、frozen code/inputsを実行して完全artifactを保存する。SPEC案状態のままなら実行不可。
A–E全reportを再reviewする役ではない。fresh mainとschema、I GATE.md/gate.json、human receipt、frozen SPEC/HYP/EXP/DATA、source-lock/calendar/code/config/environment、D RUNBOOKをexact refsから読む。code変更権限なし。

## Exact serial procedure
1. claim sole execution ownership in attempt receipt、RUN-CSM-002-ATTEMPT-1（既存attemptがあればfresh一覧で衝突確認）。run/access ledgerを**outcome前**にdurably保存しreadback。複数worker/同run並列は禁止。
2. verify gate all PASS、human accepted frozen spec、exact code/config/source/calendar/environment hashes。readinessだけでactual raw data hashが既にあるとは仮定しない。
3. frozen official routeから7 seriesを2009-11-01〜2026-09-30で一回capture。headers/URLs/request/retrieval time/exact bytes/SHA256を保存、license/source attribution/変換明示。raw price/head/tailをtool outputへ出さない。
4. **capture gate:** snapshot path/bytes/hash、returned series/currency/unit/status、range、duplicates、expected calendar、nonfinite/invalid values、date-only coverageをmachine検査。source変更/unknown schema/material errorならSTOP、outcome不可。unexpected missingはSPEC skip規則を適用し、期間を変更しない。metadata validation結果とdataset identityをdurably保存/readback。
5. offline/read-only snapshotでsignal/event ledgerを作りpersist/hash。future qをsignal functionから遮断。identity assertions/temporal-scope check PASSをrecord。gate receiptをactual bytesとcode-at-useへbind。actual dataset roleはEXPLORATORY_DISCOVERY、以後アクセス/消費状態をledgerに残す。
6. frozen codeでyとpredeclared metricsを**一回**実行。bootstrap/missing/countも指定どおり。Shard/worker別の結果閲覧、parallel horizon、metric-driven retryをしない。
7. raw input identity、event ledger、monthly outcome ledger、metric JSON、status、stdout/environment/code/config snapshots、output SHA256、start/end/access receiptを保存。
8. Resultは観測・predefined mechanical classificationだけ記録し、mechanismやstrategy採用の新解釈をしない。scientific_statusはSPEC ruleに従う。Result/Run/Git remote artifactsを全文/bytes readbackして一致確認。
9. code/market outcome/errorに重要な不整合があるならclaimしない。Rへremote refs/receiptsを渡して終了。

## Failure / retry / cost / forbidden actions
science changes、code edits、source substitutions、calendar tightening、outlier除去、sample extension不可。pre-price metadata-only技術retryは同条件でattempt receipt。valid outcomeが一部でも生成されたらpartial accessを記録しsampleをunusedと主張しない。
outcome0のtechnical failureだけfrozen inputs不変で別attempt可。partial outcome後のcorrected rerunは別承認・correctionとして扱い、one-shot independent evidenceに数えない。保存失敗時はscratch checkpointを保持してresaveし、計算を再開して二度スコアしない。
コストはUNOBSERVED。net、Sharpe、best pair/month/subgroup、current prediction、broker ordersを出さない。

## Exact deliverables / completion
- runs/RUN-CSM-002-ATTEMPT-N.yaml: protocol/code/config/data/environment identities、dataset_uses、access/timestamps/artifacts/hash/provenance guarantee（actual-read snapshotまで、hardware attestationなし）。
- results/RES-CSM-002-ATTEMPT-N.md: execution_status/evidence_validity/scientific_status独立、primary/secondary metrics、skip/sufficiency/CI、limitations、run relations。
- datasets/DATA-CSM-002/snapshots/<snapshot_id>/**: official raw bytes、retrieval metadata、hash manifest。
- artifacts/EXP-CSM-002/<attempt_id>/**: capture gate、event/outcome ledger、metrics.json、logs、access ledger、code/config/environment snapshots。
全9stepにreceipt。remote bytes/hash照合済みまでCOMPLETEとしない。returnが悪いことをfailed executionにせず、実行failureをnegative strategyにしない。
