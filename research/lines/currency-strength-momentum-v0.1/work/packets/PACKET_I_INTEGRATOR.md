---
id: PKT-CSM-I
type: WorkInstruction
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: SEQUENTIAL_CONDITIONAL_PACKET
relations: []
---

# Integrator — pre-outcome freeze, gate, later closure

## Role / branch / allowed GitHub paths
Role: Integrator — pre-outcome freeze, gate, later closure。専用branch: `work/csm-integration-20261001`。
書込allowlist（全て本line直下）: `work/integration/**; specifications/SPEC-CSM-002-v01.md（承認どおりのfreezeのみ）; experiments/EXP-CSM-002.md; datasets/DATA-CSM-002.md; decisions/DEC-CSM-003*.md; CURRENT.md`。

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
A–E metadata/report/code/testsのみ。市場price/outcomeはfreeze/gate stageでは不可。X/Rがdurably終了した後のclosure stageだけ記録済みResult/Interpretation閲覧可、独自market計算不可。

## Objective / stages / required fresh reads
Worker成果をfull fresh readしてcontradictionとreadinessを判定。初回実行権限はIntegratorが勝手に作れない。work/README、A–E packet/results、main最新schema、original human instruction、specific human freeze acceptance receiptを読む。前回CURRENTやchat要約をstateの根拠にしない。

### Stage I1 — A–D統合（outcome blind）
1. exact worker branch/head、input refs、remote全文readback、allowlist、全task matrixを確認。duplicateを一つのclaimに統合しsource linksは保持。
2. literatureのtransferability/G10/post2010、GitHub failureのreproduction scope、source/calendar/status/APIのreadiness、D code/testsを対照。
3. contradictionsをFACT/source/versionの違いか、科学条件の差かに分ける。未解決sourceを推測で埋めない。
4. SPEC案をhumanに提示する具体契約として固定。changeが必要なら理由をprior evidence/mathematical/source semantics/research efficiencyで記録し**新version**を作る別human instructionを待つ。既存案を黙って修正不可。
5. human receiptに質問/universe/horizons/target-period/reference-boundary/inference/progress ruleの明示確定がなければHUMAN_BOUNDARY。承認要求は完成したcontractへの最終判断に限定し、準備作業は継続。
6. humanが現SPECを確定したらfreeze_status、frozen_at、human decision referenceを記録。approval前後のbyte differencesを明示。code configがscience内容一致かDへ確認。D/Eに独立final auditを依頼するだけで市場実行しない。

### Stage I2 — E後のoutcome-access gate
A–E全成果をremoteから再取得し、code/source/spec変化があればauditを失効させる。readiness labelはpre-outcome運用labelで、Resultの3status dimensionsとは別。

**全項目PASS必要:**
- hypothesis/spatial universe/horizon/target/ranking/quote/metric/comparator/decision/stop ruleがhuman契約でfreeze。
- spec bytes SHA256、human acceptance、code commit/file hashes、locked configが一致。
- source route/series/unit/status/time range/latest-vintage/transport qualified、expected calendar hash fixed。
- data role=EXPLORATORY_DISCOVERY、access owner X、future confirmation sample未指定/未アクセス。no-HR/no-Pilot boundary preserved。
- no hidden horizon/era/universe/filter/source-performance/seed/block search。trial family1 empirical candidate。
- synthetic test matrix全PASS、negative gate tests PASS、environment lock。
- independent E audit PASS、identity/temporal tests/actual-byte receipt保証のscope明示。
- temporal scope=REFERENCE_ASSOCIATION_ONLY。historical publication timestamp/original-vintage UNKNOWNはcausal claimにはblocker。本reference questionには明示human受諾で限定可能。
- no data-derived outcome exposure。source metadata probeのaccess receipt、schema/coverage preflight plan、no stdout value/plot。
- baseline解析的0、pair identity、fixed inference/coverage/decision rule。
- raw-capture後のmachine preflightと二段階gate仕様が固定。
- durable artifact destination、attempt/access ledger、technical retry/correction semantics、結果後R担当が指定済み。

結果:
READY = 全項目PASS、run instructionを一回だけXへ渡せる。HUMAN_BOUNDARY = 科学選択/approval未確定。BLOCKED = source/code/audit/temporalの必須要件不足。DEPRIORITIZE = 追加研究の費用/証拠priorからlineを進めないdecision（未実行をnegativeにしない）。

### Stage I3 — execution後closure（X/R完了後だけ）
Result、Run、RのInterpretationをfresh readし、execution/evidence/scientificの独立dimensionsでDecisionとCURRENTを更新。X partial runや保存失敗はNOT_APPLICABLE/invalidとして扱う。
negative/weak/positiveの次行動はSPECとPACKET_Rに従う。same sample selectionへ戻さない。人間確定していないfutureholdout/経済条件をここで勝手に選ばない。

## Exact deliverables
- work/integration/RECONCILIATION.md: 全worker matrix/contradictions/gaps/ref。
- work/integration/HUMAN_CONTRACT.md: exact acceptance receipt/approved spec hash、未承認ならNOT_APPROVED。
- work/integration/GATE.md と gate.json: 各条件PASS/BLOCKED/UNKNOWN、input hashes、scope、X owner、stage。
- experiments/EXP-CSM-002.md、datasets/DATA-CSM-002.md: frozen IDs/role/boundaries/source/hypothesis/spec relations。未freezeならPLANNED、結果を作らない。
- decisions/DEC-CSM-003*.md: preparation/freeze/readiness/closureを別dated記録。CURRENTはderives IDsを列挙。
SOURCE/TESTのraw outcomes、A–E成果、historical documentsを書換えない。全stagesを今すぐ実行しようとせずI1/I2/I3依存状態を明記。準備一項目で終わらず全readinessを検査する。
