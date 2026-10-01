---
id: PKT-CSM-C
type: WorkInstruction
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PRE_OUTCOME_PACKET
relations: []
---

# Luna Max C — Data Source Qualification

## Role / branch / allowed GitHub paths
Role: Luna Max C — Data Source Qualification。Research Architectからのbounded work。専用branch: `work/csm-source-qualification-20261001`。
書込allowlist: `work/source-qualification/**`。共有CURRENT、spec、referencesの初回結果はread-only。

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
references/SOURCE_REVIEW_2026-10-01.md。provisional DATA-CSM-001はreview対象のみ。

## Outcome-access permission
公式metadata/docsと値を遮断した固定bounded probeのみ。actual OBS_VALUEをtool/model出力へ展開不可。full-history price retrieval、ranking、forward return、broker接続は禁止。

## Objective / scope
最小ECB routeをqualifyし、dates/status/calendar/unitsを独立に確認。data acquisition readinessと市場outcome readinessを分ける。

全項目:
1. ECB7 exact series keys、quote/currency/base/unit/frequency/status codes、API endpoint/format/query、official fallback transportをdocs/metadataで確定。
2. 2009-11〜2026-09のreference publication/setting、methodology変更、republication/vintage、CET/DST表記の保証を確認。歴史的exact availabilityが無いならUNKNOWN。
3. expected TARGET operating-day calendarをofficial rules/historyから作りhash。末日の予定日はpricesの存在で選ばない。holiday欠行とunexpected gapを分ける。
4. bounded probeは2009-11の固定期間のみ。scratch deterministic scriptでprice bytesをoutputしない。series/date/status/unit/schemaのみreportし、raw probeのhash/access receiptを保存。full history coverageはXで確認予定と明記。
5. source-lockにallowed status、identity、parse rules、schema validation、duplicate/nonfinite handling、missing semantics、publication/availability scope、retrieval failureとscientific gapの扱いを固定。科学条件はSPECを変更しない。
6. ECB/BIS bilateral/EER/Fed/FRED/Dukascopy/OANDAを全field（officiality/currency/frequency/history/timestamp/timezone/fixing-vs-executable/BIDASK/spread/carry/financing/missing/revision/license/API/automation）で評価。未取得fieldはUNKNOWN。FRED daily dateをsame-day availabilityにしない。
7. ECB copyrightとESCB statistics reuse policyを各7 seriesのprovenanceへ適用する。source citation、raw bytesを正確に保つこと、変換の明示、revision可能性を記録し、公開GitHubでのraw snapshotとderived artifactsの再利用条件を確認する。権利やsource-originが不明なら公開captureをBLOCKし、非公開のdurable storage等の許容経路を提案する。rate dataと論文再配布を区別。
8. no-tick最小route、後続economic/factor source候補、blocking gaps、human choicesを整理。代替providerへ切替えない。

## Allowed sources / exact deliverables
公式central bank metadata/legal/API、broker public data docs、author factor docs。第三者wrapperは候補確認に限りsource identityへ昇格しない。account authは不可。
- work/source-qualification/RESULT.md
- work/source-qualification/SOURCE_MATRIX.csv
- work/source-qualification/source-lock.json: qualified route、7 series、unit/status/format、expected dates identity、unknown availability、hash workflow。
- work/source-qualification/expected-calendar.json: fixed rangeのexpected operating days/month-ends。未確認なら作り話のcalendarを出さずBLOCKED receipt。
- work/source-qualification/PROBE_RECEIPT.md と metadata-only probe artifacts/script（実施時）。
full-history coverage/raw hashはこのstageで必要ではない。source route/schema/calendarがqualifiedか、execution前に何を確認するかを明確にすることが完了条件。qualifyできないsourceは未完として保存し他source比較を最後まで処理。
