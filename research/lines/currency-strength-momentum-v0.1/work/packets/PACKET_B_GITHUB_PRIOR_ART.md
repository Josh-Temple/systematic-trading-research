---
id: PKT-CSM-B
type: WorkInstruction
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PRE_OUTCOME_PACKET
relations: []
---

# Luna Max B — GitHub Prior Art / Failure Review

## Role / branch / allowed GitHub paths
Role: Luna Max B — GitHub Prior Art / Failure Review。Research Architectからのbounded work。専用branch: `work/csm-github-prior-art-20261001`。
書込allowlist: `work/github-prior-art/**`。共有CURRENT、spec、referencesの初回結果はread-only。

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
references/GITHUB_PRIOR_ART_2026-10-01.md、research/prior-art/freqtrade.md、SYNTHESIS_V0.2.md。

## Outcome-access permission
第三者repositoryの記録済みperformance/Issuesは閲覧可。external market backtestやlive/paperは実行不可。toy/component testだけ実行可。本line market outcome不可。

## Objective / scope
README以上の証拠を複数repoから確認し、失敗を防ぐ最小testsへ変換する。

全項目:
1. nateemma/fx-strategy-frameworkのfresh default SHA、README、momentum/features/basket、simulatorのlag、data quote、cost、financing code、testsを取得。
2. b723aa48…のintraday rejection、74d3c0f…のremoved bfillとcurrent regression、monthly verdictと未commit scriptを追跡。時系列・basket・carry-change momentumを混同しない。
3. live/backtest・FX-only/account・financing/interest postingの履歴をsource code/commit/公開evidenceで照合。paper observations、published schedule、実資金結果を別扱い。
4. pmorissette/btのfresh SHA、SelectMomentum/date/lag、cost path/tests、PR572、holding cost alignment/nonfinite修正を確認。FXへコピーできないequity cost assumptionsも記録。
5. freqtradeのfresh default（develop/mainを区別）、lookahead code/tests、HTF merge、Issues12507/12894、full-row/market-order変更履歴を確認。existing reviewのcomponent reproductionと今回の再現を区別。
6. 追加のFX/cross-sectional/momentum/systematic-research repoを最低1個screenし、3本以上の実装・履歴比較を完成。選定reasonを記録し、data/performanceを独立replicationせずcopyしない。
7. 可能なら合成入力でprefix-invariance、cost-applied-path、date alignmentの一部を独立確認。実行環境がない項目はNOT_REPRODUCED。
8. 共通原則、repo固有、模倣しない選択、未確認negative claimを分けてD/Eに必要なtest checklistを作る。

## Allowed sources / exact deliverables
GitHub code/tests/issues/PR/commits/releases、maintainer docs。private account/取引記録やcredentialsを求めない。market datasetはdownloadしない。
- work/github-prior-art/RESULT.md
- work/github-prior-art/REPOSITORY_MATRIX.csv: repo/default/ref/path/claim/source_type/reproduced/failure/transferability。
- work/github-prior-art/FAILURE_TEST_CHECKLIST.md
- work/github-prior-art/toy_checks/** と environment/test output（実施時だけ）。
全8項目にstatusを付け、少なくとも3repoでREADME以外の証拠を得る。取得不能なら全独立項目を続けPARTIAL。snapshot pin、reporterと再現の区別が完了条件。
