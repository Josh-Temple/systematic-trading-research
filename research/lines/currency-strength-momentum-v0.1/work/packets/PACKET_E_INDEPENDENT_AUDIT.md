---
id: PKT-CSM-E
type: WorkInstruction
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: SEQUENTIAL_CONDITIONAL_PACKET
relations: []
---

# Luna Max E — Independent Pre-outcome Auditor

## Role / branch / allowed GitHub paths
Role: Luna Max E — Independent Pre-outcome Auditor。専用branch: `work/csm-independent-audit-20261001`。
書込allowlist（全て本line直下）: `work/independent-audit/**`。

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
metadata、contract、code、synthetic testsのみ。market price/outcomes不可。第三者prior evidenceは可。Dを担当した同contextを再利用せずclean WORKで実行。

## Objective / required reads / scope
A/B/C/Dのremote exact headsとdeliverables、Integratorのpreliminary reconciliation、human freeze receipt、locked SPEC/config/code/source/calendar/environmentをfresh read。未凍結ならdraft auditまで行いfinal PASSは出さない。Dの思考・報告に依存せずraw codeを検査する。

全項目:
1. original human contractとfreeze contentが一致、HYP/SPEC/EXP/DATA role/periodのlineageとprovisional案の未承認宣言を混同していない。
2. common numeraire/pair quote/simple-vs-log/56pair/EURUSD/tieの証明を独立に行い、synthetic oracle例を作る。
3. missing calendar/target triple/cascade、holiday、same endpointのscope、UNKNOWN availabilityとrevisionを検査。reference associationのtemporal PASSはcausal execution PASSではない。
4. prefix/suffix leakage、bfill、global aggregation、compressed date shift、entry後のranking、data-driven exclusionをsourceから確認。
5. RNG/block/percentile/coverage/decision boundariesを独立synthetic calculationで照合。serial dependenceとregime変化に対するlimitationsを評価。
6. gate-required CLIがno-gate/no-freeze/mismatched identityを拒否するnegative tests。hashがactual bytes readと結合、保存failureでscientific結果をpromoteしないこと。
7. network/data visibility、stdout/plots/logs、current rankings、hidden search surface、source probeのaccess receipt、holdout separationを確認。
8. A/Bのnegative/contradictions、Cのreadiness、Dのscope/testsに重大gapが無いかを確認。humanが選ぶ科学条件を「実装上の便宜」で代替していないかを調べる。
9. omissions/duplicate findingsを整理し、READY_PREPARATION / HUMAN_BOUNDARY / BLOCKED / DEPRIORITIZEのrecommendationとclaim保証範囲を示す。

## Exact deliverables / allowed sources
- work/independent-audit/RESULT.md
- work/independent-audit/AUDIT_MATRIX.csv
- work/independent-audit/toy_oracle.py と TEST_LOG.txt（実施時）。
public docs、frozen source metadata、code、synthetic fixturesだけ。other pathのfixは提案として記述し、直接修正不可。
全9項目処理、自己申告testsだけでPASS不可。independenceが確保できなければBLOCKED_INDEPENDENCE。auditはinput hashesにbindし、D/source/spec変更で失効。final outcome gateを単独で発行しない。
