# Trading — 5役割による実証完走 Wave（2026-10-08）

## 0. 今回の目的と権限

対象リポジトリ: `Josh-Temple/systematic-trading-research`。

**目的**: 5つのChatGPTセッションを使って、既存の期待値プラス候補を「大量のアイデア」ではなく「将来の取引コスト控除後の期待値を検証できる状態」へ進める。今回の主軸は FX News Sentiment v0.1 / PR #63。二次候補の Currency Strength Momentum（CSM）はゲート未解決のまま保存し、別研究として継続する。

**このWaveの実行権限**: pre-outcome source qualification、必要最小限のコード修正、synthetic-only実装・テスト、独立監査、研究状態の統合記録。実データによる市場outcomeの閲覧・分類・計算・使用、実売買、ペーパー注文、ブローカー認証情報の持ち出しは許可しない。人間承認済みの科学条件、freeze、holdout、execution permissionを変更しない。

この文書は**作業指示と優先順位の提案**であり、研究 line の Specification、Human Decision、Packet D独立監査、source gateを代替・上書きしない。全担当者は現在のGitHub正本を fresh read し、矛盾した場合はそちらを優先して本指示との差を記録する。

## 1. 2026-10-08に確認した起点（以後は要 fresh read）

- main: `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`。
- FX News Sentiment: [PR #63](https://github.com/Josh-Temple/systematic-trading-research/pull/63)、branch `research/fx-news-sentiment-v0.1`、確認時 head `8d3771921fbab88ea56b913f9d6fe8d62236961c`。入口: `research/lines/fx-news-sentiment-v0.1/CURRENT.md`。
- 同研究の現在状態: `UNTESTED`、`PROPOSED_NOT_FROZEN`、正式prospective cohort `CLOSED`。source qualificationはGDELT `PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED`、XM `LOCAL_XM_EXECUTION_REQUIRED`。正式な人間freeze、独立Packet D、実際のEURJPY outcome、live/paper order authorityは**なし**。合成テストは現行CURRENTで53/53 PASSと記録されているが、次回実行の成功を保証しない。
- GDELTで既に確認したもの: DOC artlistのHTTP 200、raw byte/hash保存、12 raw / 10 deterministic retained。同じ条件での cap=10 比較はHTTP 429。これだけではDOC seendateの厳密な初回観測時刻・完全性・発行時点取得可能性の保証にならない。
- XM: EURJPY Friday exit対応のcollector v0.2は `FRIDAY_EXIT_PROBE_READY_NOT_RUN`。ユーザー本人のWindows MT5でのsource-only取得が必要。XMの実取引履歴やパスワードをChatGPTへ転送しない。
- CSM: [PR #37](https://github.com/Josh-Temple/systematic-trading-research/pull/37)の統合ゲートは `I2=BLOCKED`、`market_outcome_access=false`。別の[PR #53](https://github.com/Josh-Temple/systematic-trading-research/pull/53)でECB full-historyの**metadata-only** source-readinessがある。これはFXNSのsourceや市場結果と混ぜない。
- Horizontal Reaction: mainの `CURRENT.md` を正本としてH1/H2を消費済みと扱い、H3の成熟・source gateを守る。消費済みH1/H2から新しいrule/thresholdを探さない。
- JP225 EMA: mainの `CURRENT.md` における `WAITING_FOR_XM_STAGE1_DATA` と2026 holdout LOCKを守る。異なるproxyや有料データを自動採用しない。

確認対象: `docs/RESEARCH_PRINCIPLES.md`、`research/lines/INDEX.md`、PR #63の `CURRENT.md`、`RESEARCH_LINE.md`、凍結前SPEC、`SOURCE_CONTRACT`、`work/SOURCE_QUALIFICATION_RESULT.md`、`work/PRE_FREEZE_HARDENING_RESULT.md`、`work/packets`、`work/source-probe`、`work/xm-source`、`work/implementation`。

## 2. 並行実行と統合方法

1. **A・B・Cは独立したChatで並行実行**。各自、開始時にPR #63と必要な正本を再取得する。基本はその時点のPR #63 headから固有のwork branchを切り、PR #63の `research/fx-news-sentiment-v0.1` branch宛に個別のdraft PRを作る（GitHubが受け付けない場合はcommitせず差分とblockerを報告）。**PR #63やmainへ無条件に直接pushしない**。
2. 各担当は下記のpath allowlistだけ変更する。同じfileを二つの担当が変更しない。既存の共通 `CURRENT.md`、SPEC、SOURCE_CONTRACT、PROMPT/SCHEMA、`research/lines/INDEX.md`はA〜Dで変更しない。科学仕様の変更が必要なら `HUMAN_BOUNDARY` としてEへ送る。
3. **DはA・B・Cの各成果物のcommit SHAが確定してから**実施する。Dは作成者と異なるChatセッションで、過去の作業説明だけを根拠にせず、GitHubのbyte・diff・test・source identityを再確認する。Dの独立監査と統合後の総合検証は別の保証。
4. **EはDの後**に実施する。A〜Cの変更を監査結果ごとに統合候補として扱い、競合・科学条件・source gateを確認して採否を決める。変更を統合した場合、統合後の正確なheadでテストを再実行する。独立監査の対象commitが変化したら対象差分に対する再監査なしで `PASS` を付けない。
5. 統合対象にならなかったnegative/null/blocked成果も、理由をEの統合記録に残す。**準備ファイルやPRの件数を成果指標にしない**。
6. 既存の予定済タスク5件を停止・改変・再登録しない。このWaveの「5役割」は5つのChat実行指示であり、常時自動監視や5つの自動実行が設定されたことを意味しない。

新規Trading Discoveryは既存運用どおり1 run原則最大1件。今回の主作業は既存候補の**直接実証への解禁**であり、A〜Eから新戦略を量産しない。

## 3. A — GDELT source qualification（並行開始可）

**役割**: FXNS用のGDELT DOC article-list取得が事前情報として利用できるか、source-onlyで最小確認する。

**起点**: PR #63の `CURRENT.md`、`work/SOURCE_QUALIFICATION_RESULT.md`、`work/PRE_FREEZE_HARDENING_RESULT.md`、`work/source-probe/**`、現行SPECとSOURCE_CONTRACT。先行の429、seendate意味、時刻境界、MAXRECORDS=250、厳密な取得時刻をそのまま残す。

**作業**:
- 公式GDELT DOC documentationと現在のsource-probe実装を照合。既存のraw response/header/hashを読み直し、前回のAPI応答を新たなprospective観測として扱わない。
- 実アクセスするなら**結果に依存しない既存の固定query・固定window**を保持し、source-onlyで必要最小限の1回のbounded probeにする。HTTP 429/その他rate-limitを受けたら停止。ページ・query・windowの変更やリトライ反復で見かけの完全性を補わない。取得時刻を正確に保存し、後からcutoff前取得とみなさない。
- DOC `seendate` と publisher time の差、timestamp timezone / equality、実際の情報利用可能時刻、raw count>=MAXRECORDS時のfail-closed、source completenessを独立に分類する。証明できない項目は `UNVERIFIED` とする。
- source-validating codeの実バグが見つかった場合に限り合成回帰テスト付きで修正。論拠なくSOURCE PASSを宣言しない。

**書込可能範囲**: PR #63派生branchの `research/lines/fx-news-sentiment-v0.1/work/source-probe/**` のみ。既存raw成果物の上書き禁止。新規probeの保存は取得条件・取得時刻・hash・HTTP statusを含む新規ディレクトリ。

**成果条件**: SOURCE PASSまたは`PARTIAL_WITH_GAPS / BLOCKED`の根拠付き判定、再現可能なraw/metadata/hash（実リクエスト実施時）、修正した場合のテスト記録、次の**一つの**必要条件。Source-onlyの確認では市場outcome/ChatGPT実分類を扱わない。

**停止**: 適法なデータ使用・時刻・網羅性を確立できなければ無理に埋めず、HOLD原因を固定して終了。新しいproviderへの自動切替をしない。

## 4. B — XM Friday exit source readiness（並行開始可）

**役割**: ユーザー本人のXM Windows MT5から、EURJPYのFriday 08:15 JST exitをsource-onlyで資格確認できる最小手順を確定する。

**起点**: PR #63の `work/xm-source/**`、collector v0.2 / `RESULT.md` / `WINDOWS_RUNBOOK.md`、SOURCE_CONTRACT、GDELTとは独立したXM source gate。

**作業**:
- collectorの最新版と固定6 probe windows（Friday 3件を含む）をremoteから確認。コードに必要なtimestamp/time_msc、Bid/Ask、UTC↔JST、08:15から60秒以内、Friday・休場・no-quote、symbol/server identity、raw保存/hashがあるかを確認。
- **実際に再現可能な欠陥がある場合だけ**最小修正とsynthetic testを行う。テストに正しいBID/ASK、duplicate/ordering、欠損、JST日付変換、close例外を含める。既に十分なら「コード変更なし」を正式な成果としてよい。
- 意図するWindows/MT5環境にアクセスできなければ、collectorを実行したと偽らず `LOCAL_XM_EXECUTION_REQUIRED` で停止。追加の汎用runbookを作り直さない。
- 人間の1回のローカル実行後に必要な**機密でない**出力ファイル名・SHA/hash・coverageの検証項目を明示。ログイン情報、口座番号、注文履歴は収集しない。
- raw tickを取得できても今回のAI担当は価格方向、return、P/L、勝率を見ない。現行のsource-only境界を守る。

**書込可能範囲**: PR #63派生branchの `research/lines/fx-news-sentiment-v0.1/work/xm-source/**` のみ。既存証拠はappend-only。

**成果条件**: 実行したsynthetic testsの事実、collector修正の有無、正確なローカル操作とreview対象、`PASS/PARTIAL_WITH_GAPS/BLOCKED`の範囲付き判定。no-PCならファイル量産なしで停止理由を1つに絞る。

## 5. C — prospective event ledger / fail-closed synthetic implementation（並行開始可）

**役割**: PR #63で欠けているformal event ledger / issuance runnerの**安全な骨格のみ**を実装する。実市場データを使わない。

**起点**: PR #63のSPEC、SOURCE_CONTRACT、`work/implementation/**`、既存53 synthetic tests、PROMPT/SCHEMA exact-byte identity、FRIDAY exit改定。

**作業**:
- 既存の決定論的helperを再利用し、**input・time cutoff・source PASS・model identity・output parseの各条件が満たされるまで発行もscoreも不能**なevent recorderを実装する。source gatesは外部の独立検証済みevidenceから明示入力し、synthetic sample countからPASSを推定しない。
- prospective event ID、JST/UTC aware time、source raw/metadata/hash reference、prompt/schema file hash、可視のmodel/config identity、分類raw/parsed、decision、NO_TRADE、UNAVAILABLE・blocked、version、発行時点の凍結記録を分離する。
- formal cohort CLOSEDの時、real market response、real LLM classification、actual XM quotesが到着しても、形式上の正式eventへの昇格やoutcome joinを禁止。将来の人間freezeと独立監査まで開けない。
- synthetic fixturesで、木曜発行→金曜exit、金曜発行不許可、カットオフ後ニュース、raw count 250、時刻不明、価格未観測、duplicate、source未承認、version相違、あとからNO_TRADEへ変換、空のmodel identity等の拒否をテストする。
- 新しい売買ルール、パラメータ、pair選択、performance計算、データの取得経路は実装しない。実LLM分類・金融ニュース・EURJPY market outcomeは使用しない。

**書込可能範囲**: PR #63派生branchの `research/lines/fx-news-sentiment-v0.1/work/implementation/**` のみ。共有SPEC、SOURCE_CONTRACT、PROMPT、Schemaのbyte変更は禁止。

**成果条件**: 最小の新規コードとfixture、全synthetic testのコマンド/件数/結果、formal source CLOSED時に絶対進まない失敗例、将来データで未確認の保証範囲。新規汎用agent/MCP/databaseは作らない。

## 6. D — independent pre-outcome audit（A〜C終了後）

**役割**: A/B/Cの作者の説明や成功報告を信用せず、対象commit単位で独立評価する。元のPR #63 Packet Dの正式承認を自動で付与しない。

**起点**: A/B/Cで確定した3 commit SHA、各diff、PR #63の最新HEAD、現行SPEC/SOURCE_CONTRACT、凍結前後のsource roleとholdout。

**作業**:
- commit・変更ファイル・allowlistを照合し、各成果物を直接readbackする。SOURCE PASS・科学的Supported・live許可が証拠なしに昇格していないか検査。
- Cのsyntheticテストを独立実行し、可能なら意図的なbad fixtureでfail-closed確認。GDELT cap/first-seen/revision/HTTP 429とXM quote/time/Friday/holiday/no-quoteの境界を区別する。
- 不正な時点のニュース混入、future knowledge、source replayとprospective issuanceの混同、見送りの事後変更、負結果の消去、候補選択に使ったholdout再利用、model identityや価格providerの暗黙代替を監査する。
- A/B/Cの判定を `PASS_SCOPED`、`PARTIAL_WITH_GAPS`、`BLOCKED`、`FAIL` に分け、**何を検査していないか**を明示する。全システムPASSに一般化しない。

**書込可能範囲**: 固有の監査branchの `research/lines/fx-news-sentiment-v0.1/work/independent-audit/2026-10-08/**` のみ。対象worker成果物への変更は禁止（修正依頼として報告）。

**成果条件**: 対象headごとの観測、再実行testとログ、source/content/version一致、具体的な修正要否、残存blocker、E向け「採用可能・要修正・除外」の判断材料。

## 7. E — integration / next direct test（Dの後）

**役割**: FXNSの科学的状態を変えず、A〜Dの成果を現行PR #63へ安全に統合する。次に何をすれば将来outcomeを初めて正しく評価できるかを一意に示す。

**起点**: PR #63のfresh HEAD、A/B/Cの確定head、D独立監査、`CURRENT.md`、SPEC、source contracts、既存packets。必要ならPR #37/#53の状態もfresh read。

**作業**:
- 未承認/未検証の差分は統合しない。worker branchから取り込む場合は非forceで統合し、path衝突・固定仕様byte・raw evidenceの改変・tests・commit identityを確認する。合成テストの合格のみで source/formal gateを開けない。
- 統合後headで独立した全synthetic testsを再実行。取得済みrawのhashは再照合し、未取得rawは未取得と明示。Dの監査対象から変わった差分を監査済みとして扱わない。
- 真の状態が変わったときのみ `CURRENT.md` を改訂。改善成果が readinessだけなら、`UNTESTED / COHORT CLOSED` を維持して統合記録へ理由を残す。
- **次の直接の一手は最大2つ**: GDELT prospective acquisition qualificationまたはユーザー本人のWindows XM source-only collection等、すでに固定された具体的blockerを優先。どちらも実行不能なら無理な準備workを増やさず止め、独立CSM workへの移行を提案する。
- CSMへ移る場合、PR #37の I2 `BLOCKED`、PR #53のmetadata-only、trusted-key/isolated runner/human disposition の既存条件を再読し、metadata receiptを市場outcome PASSに混同しない。新規の手法を追加しない。

**書込可能範囲**: 統合対象のPR #63 branch上の、監査済みA/B/Cの変更ファイル、`research/lines/fx-news-sentiment-v0.1/work/integration/2026-10-08/**`、必要な場合の `CURRENT.md` のみ。既存仕様・prompts・source artifactsの無断変更禁止。mainへのmergeは別のCI/人間レビュー後に判断する。

**成果条件**: 統合commit、採用/不採用diffと理由、CI/合成テスト実行事実、current gates、次のdirect testと明確なhuman boundaryを1件のintegrator reportに記録する。正本のreadbackまで確認する。

## 8. 観測する成果と失敗条件

- **主要な運用成果**: (a) 客観的source gateが一つでも閉から前進したか、(b) 実施可能な直接のsource取得または正式観測を妨げる具体的blockerが減ったか、(c) synthetic/independent verificationを伴って正式評価への準備が完了したか。実際のmarket outcomeを開かなければ、期待値プラスとは認定しない。
- 新規Research discoveryの件数、書類数、PR数、LLMによるポジティブな評価数を成功指標にしない。
- コスト控除後の期待値は、独立したunused / prospective観測でのみ判定する。複数候補の探索履歴、試行回数、根拠となる効果量、期間/レジーム依存、信頼区間/不確実性、執行費用、欠測、NO_TRADEを保存する。
- 既存評価指標の閾値は結果前のSpecificationに従う。新しい数値閾値、売買停止規則、サンプル選択ルールを本Waveから作らない。
- GDELT側がデータ取得時刻とcomplete corpusを確認できない、XMがローカルWindows端末でしか実行できないなど、AI側で直接解消できない場合は**正確なBLOCKEDで終了**する。それを埋めるだけの新しい準備Waveを再帰的に作らない。

## 9. 共通のChat指示（全担当で先頭に付ける）

> Repository: Josh-Temple/systematic-trading-research。まずGitHubの現在のmainとPR #63のheadをfresh readする。このWave文書だけを現在状態の正本と扱わない。指定されたA/B/C/D/Eの節を実行する。変更可能パスはその役割のallowlistのみ。spec/holdout/closed outcome gateを変更せず、実データの市場outcome、return、P/L、win rate、方向別performance、実ChatGPT分類結果を参照しない。既存プロセスにない新しい科学的判断や代替sourceを勝手に採用しない。必要なことは最小限の変更・テスト・raw/hash provenanceとともに実行し、GitHubへ安全なbranch/PRとして保存してreadbackする。実行できなければ推測せず、ひとつの特定blockerで止める。最終回答では対象ref/head、実施事項、テスト、科学status、今も閉じているgate、次の一手を明示する。

**実行順序**: A/B/C 同時 → D 監査 → E 統合。5役割をすべて同時に走らせると、Dの監査対象が確定せず独立監査として不成立になり得る。

## 10. 根拠

- [Research Principles](RESEARCH_PRINCIPLES.md) — hypothesis/spec/result/decision、holdout once、negative result、source/provenance、live trading boundary。
- [既存先行例の比較](../research/prior-art/SYNTHESIS_V0.2.md) — adaptive loopのfinal holdout汚染リスク、診断PASSの保証範囲、live executionとの区別。
- [FXNS current](https://github.com/Josh-Temple/systematic-trading-research/blob/research/fx-news-sentiment-v0.1/research/lines/fx-news-sentiment-v0.1/CURRENT.md)、[PR #63](https://github.com/Josh-Temple/systematic-trading-research/pull/63)。
- [CSM integration PR #37](https://github.com/Josh-Temple/systematic-trading-research/pull/37)、[CSM source-readiness PR #53](https://github.com/Josh-Temple/systematic-trading-research/pull/53)。

**注**: 本書のSHA・判定は2026-10-08観測時のsnapshotであり、将来の有効性は保証しない。実行Chatは毎回現在のcanonical branchを読み直す。
