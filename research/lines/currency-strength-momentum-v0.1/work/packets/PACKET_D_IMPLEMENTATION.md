---
id: PKT-CSM-D
type: WorkInstruction
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PRE_OUTCOME_PACKET
relations: []
---

# Luna Max D — Outcome-blind Deterministic Implementation

## Role / branch / allowed GitHub paths
Role: Luna Max D — Outcome-blind Deterministic Implementation。Research Architectからのbounded work。専用branch: `work/csm-implementation-20261001`。
書込allowlist: `work/implementation/**`。共有CURRENT、spec、referencesの初回結果はread-only。

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

## Additional required fresh reads
references/GITHUB_PRIOR_ART_2026-10-01.md、references/SOURCE_REVIEW_2026-10-01.md。Cのsource-lockが完成後にfresh readしてintegration testsを追加（初期synthetic作業は待たない）。

## Outcome-access permission
完全にsynthetic/toy pricesだけ。actual market q、historical rankings、outcomes、strategy performance不可。forward-return/metric codeをsyntheticで検証することは可。

## Objective / scope
SPECを実装する小さなdeterministic moduleとtest harness。巨大framework・horizon search・optimizationは不要。未凍結specに対して実装し、後のfreezeで同一bytes確認が必要。

全項目:
1. pure parse/validate（decimal input、quotes、units/status、finite/positive、duplicate、ordered dates）とsignal/target/metrics/receiptを分離。
2. EUR constant、USD inclusion、inversion、q_b/q_a、raw max/minと56ordered max、numeraire invarianceをsyntheticで証明。simple return差の誤実装を捕捉。
3. exact decimal ratio tie、unique extrema、EURがwinner/loser、USDがwinner/loser、28-long-onlyの非同値、equal pair-average同順位をtest。
4. full calendar gridを維持。weekend/holiday、month-year boundary、whole missing month、one currency missing end、missing target、nonfinite/duplicate/status mismatchをtest。currency別rollbackやcompressed-shiftをreject。
5. prefix truncationとfuture-suffix perturbationで過去signalが変化しないこと。formation endとtarget startの共有referenceは統計用途のみ。偽AVAILABLE_AT、same timestamp executable claimをrejectするreceipt validator。
6. metricsと12slot circular bootstrapのfixed RNG、percentile type7、missing-grid preservation、partial-year、valid0replicate failure、120/.80 sufficiency・decision boundariesをsynthetic hand-calculated casesで確認。iidやyear-clusterへ勝手に変えない。
7. loaderはreal dataを直接読むがstdoutにはprice/head/tail/rank/metricをgate前に出さない。gate-required CLI、raw-capture preflight、event-ledger先行hash、identity mismatch fail、no network during calculate、runtime/file snapshotとoutput hashesを実装。
8. stable code/environment identity、frozen config（SPEC1個、no parameter CLI/sweep）、test log、guarantee boundaries、unused features無しを確認。C metadata adapter integrationは必要だがactual full-history runは不可。
9. no-access receiptとsource/spec discrepanciesを残し、結果前の修正案はIntegratorへ報告。blockerを独自に解決するscience changesは禁止。

## Allowed sources / exact deliverables
本repo仕様、standard-library docs、external公開source snippets（license尊重）、synthetic fixtures。API credential不要。
- work/implementation/RESULT.md
- work/implementation/csm.py（または最小module群、同pathのみ）
- work/implementation/test_csm.py、fixtures/**（全てSYNTHETICと明記）
- work/implementation/config.json、RUNBOOK.md、ENVIRONMENT.md、TEST_LOG.txt。
- work/implementation/TEST_MATRIX.md: 上記全taskとtestsの対応。
全9項目を最後まで処理。tests passだけでscientific条件を確定しない。DはGate PASS発行・市場実行・merge不可。C未完でもpure testsを完了しintegrationだけBLOCKED。
