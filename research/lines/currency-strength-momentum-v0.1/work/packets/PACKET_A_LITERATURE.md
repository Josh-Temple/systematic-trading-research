---
id: PKT-CSM-A
type: WorkInstruction
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PRE_OUTCOME_PACKET
relations: []
---

# Luna Max A — Literature / Scientific Prior Art

## Role / branch / allowed GitHub paths
Role: Luna Max A — Literature / Scientific Prior Art。Research Architectからのbounded work。専用branch: `work/csm-literature-20261001`。
書込allowlist: `work/literature/**`。共有CURRENT、spec、referencesの初回結果はread-only。

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
references/SCIENTIFIC_PRIOR_ART_2026-10-01.md、references/GITHUB_PRIOR_ART_2026-10-01.md、research/prior-art/README.md。

## Outcome-access permission
第三者の公刊論文・過去結果は閲覧可。本line actual FX data、holdout、market outcomeはアクセス不可。author factor dataの値downloadも今回は不要。

## Objective / scope
月次major8単一pairに先行証拠がどれだけ移転できるか評価する。最適horizonやstrategyを探索しない。

全項目:
1. Menkhoff/Sarno/Schmeling/Schrimpfの原文§data、return sorting、spot/excess、formation/holding、developed subset、cost、limits-to-arbitrageをpage/section付きで抽出。
2. Moskowitz/Ooi/PedersenのTSMOM signal/payoff、vol scaling、spot/roll contribution、CSとの相違。
3. Zhang Dissecting currency momentumのfull textを著者/機関/原出版から取得。static factor regressionとfactor momentum、残差、estimationの時点、sample・G10を確認。取得不能ならabstract-levelの結論に留める。
4. Iwanaga/Sakemoto 2025 Conditional currency momentum portfoliosのfull text、post-GFC split、currency coverage、cost、conditioning training/evaluationを確認。
5. Hutchinson, Kyziropoulos, O'Brien, O'Reilly and Sharma (2022), “Are carry, momentum and value still there in currencies?” のfull textを読む。G11 universe、sample split、cross-sectional momentumのexcess-return definition、core 3-month/1-month and parameter variations、post-2010 results/costs、past/future return regressionsをpage付きで抽出。2010–2020結果が本lineの1-month raw spot single-extreme ECB-reference testへどこまで移転するか、直接比較できない点とともに記録する。
6. 2020–2026のcurrency momentum replication/reassessmentを一次資料で検索し、major/G10、post-2010、post-GFC、ZIRP、政策正常化後の区別を調査。2025 basis-momentum/IR volatility、2026 FX momentumの候補を適用範囲でscreen。full textが無い候補も取得状態を残す。
7. winner/loser basketとsingle extreme、spot rankingとexcess ranking、USDをuniverseに含むこととUSD benchmark、carry/dollar/factor momentumをmatrixで対照。
8. 支持・反証・不確実を列挙し、monthly 1/1、8通貨、post-2010の推奨への影響を結果前のreasonで示す。変更はrecommendationのみ、仕様は変更しない。
9. model pretraining/既知historyを含むhistorical確認の限界、publication/search bias、独立unused/prospectiveの必要性を記録。

## Allowed sources / exact deliverables
原論文、著者website、大学repository、central bank paper、journal、著者replication code。secondary pageはdiscovery用で、fact根拠は一次へ。
- work/literature/RESULT.md: 全task matrix、FACT/INTERPRETATION/LIMITATION、contradictions、scientific recommendations。
- work/literature/EVIDENCE_TABLE.csv: author/year/version/URL/access_date/full_text_status/page/sample/universe/signal/payoff/cost/G10/recent-period/result_scope/limitation。
- work/literature/SEARCH_LOG.md: queries/date/routes、negative/nullの探索、unretrieved candidates、gap。
全文論文の無断再配布や大量引用は不要。最小paraphraseとpage locatorにする。完了は全8項目を処理し、根拠の無いcurrent-major net edge claimが無いこと。
