# FX News Sentiment — 5役割Wave E統合判断（2026-10-08）

## 判定

**PARTIAL_WITH_GAPS / INTEGRATION_DEFERRED**。A〜Dの成果、Cの修正版をGitHubで確認した。A/B/C/Dの変更を科学的妥当性の根拠として扱わず、現時点では研究PR #63へいずれもマージしない。修正はPRとして保存し、未解決条件を明示する。

このE記録は *統合判断の成果物* であり、形式的なPacket D独立監査のPASS、SOURCE PASS、正式イベント発行、モデルfreeze、期待値プラスの確認、実売買の承認を意味しない。

### Fresh-read identities

| 対象 | 観測時HEAD | 統合判断 |
| --- | --- | --- |
| main | `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3` | 変更なし |
| FXNS [PR #63](https://github.com/Josh-Temple/systematic-trading-research/pull/63) | `8d3771921fbab88ea56b913f9d6fe8d62236961c` | OPEN/DRAFT、source/freeze/cohort gates CLOSED |
| A [PR #68](https://github.com/Josh-Temple/systematic-trading-research/pull/68) | `8e55f817795a68b167f5785f6ac814c898cda11d` | 条件付き採用候補（まだ未マージ） |
| B [PR #66](https://github.com/Josh-Temple/systematic-trading-research/pull/66) | `769b94228307474fdaa91e84457c8f66390d69c5` | blocked readiness receiptとして採用可能候補（まだ未マージ） |
| C [PR #67](https://github.com/Josh-Temple/systematic-trading-research/pull/67) | `166a8222e09dde4413b799acd92d74c4a2586c04` | D-C-01により元実装の無条件採用禁止 |
| D [PR #69](https://github.com/Josh-Temple/systematic-trading-research/pull/69) | `da35d13179532ea1988bb476bf219662d1824e40` | 部分監査、正式Packet Dの代わりにはならない |
| C修正 [PR #70](https://github.com/Josh-Temple/systematic-trading-research/pull/70) | `9c5422e6bb92ef34db2303346aa513acf8bf8bab` | コード+回帰テスト定義は保存・readback済み。実行テスト・独立再監査待ち |

上記すべてPR #63またはそのC派生branchであり、mainへの直接変更はない。作業の時点を将来に拡張しないこと。後続作業は毎回HEADをfresh readする。

## A/B/C/Dの採否

### A — GDELT

3ファイルがsource-probe配下のallowlistに収まる。既存429の応答受信完了時刻を、後段の例外処理で上書きしない修正は妥当な限定的候補。11個の合成テスト定義（元9件+追加2件）と報告を確認したが、E自身はこの修正済みcommitでPythonテストを実行していない。GDELTは `PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED` のまま。

**重要なCIの問題**: PR #63の現在の `.github/workflows/fxns-gdelt-source-probe.yml` は `pull_request` と `work/source-probe/**` に反応し、合成テストの次のstepでネットワーク経由の `gdelt_schema_probe.py` を呼び出す。PR同期時に対象PRのchanged pathsが含まれる場合、後続の統合で意図しないlive source取得を起こす可能性を排除できない。PR #68の `[skip ci]` 記録のみでは将来の別commitによる無条件安全性を保証しない。**ネットワーク遮断か固定された明示的実行条件でsource-only probeを制御し、offline synthetic CIと分離してから**正式な統合を検討する。現WaveのA/B/C/D/E変更allowlistはworkflow改変を含まないため、ここで無断修正しない。

### B — XM

変更は `work/xm-source/**` にあるreadiness文書1件のみ。既存collector v0.2、指定日付、sourceやテストコードを変更していない。独立Dの結論どおり**append-onlyのBLOCKED記録として採用候補**だが、XMデータを取得したことやFridayの実約定可能性を証明するものではない。`LOCAL_XM_EXECUTION_REQUIRED` を維持。

### C — synthetic event ledger

元のC code / PR #67はイベントのbuild pathとは別に、任意の辞書をwriterに直接渡しても `record_type`、`formal_cohort_status`、`event_id` しか検証しないため、実際には非合成のsource/outcomeフィールドが混入できるというD-C-01がある。正式発行や結果結合を閉じていることは維持されていた。

**Cの修正PR #70**は、writer・verifier・blocked receiptの共通合成専用guardを追加。イベントのsource参照、unknown fields、market_outcome sentinel、version、凍結済みtimeline、model/config、NO_TRADE・BLOCKED区別を検査する。改変後にhashを計算し直す試験を含む新規回帰テスト**2件**を追加し、全体のテスト定義が26→28件であることをGitHubでreadbackした。修正はC allowlist配下のみ。

**テスト境界**: GitHub本体の完全なPython checkoutと実行はこのE実行環境で成立していない。28/28 PASS、既存53/53 + A 11/11 + C 28/28の合算PASS、実行環境での悪意あるdirect-writer test PASSは**未確認**。A/B/Cの報告に記載された過去のPASS数をEの再実行結果として転記しない。新guardは内容の一部を検査するだけで、モデル出力の生成経路やソース真正性、特権ユーザーによるファイル+hashの同時改ざん防止を保証しない。

**決定**: PR #70の追加回帰テスト、元Cの合成suite、Aのsource-only suite、既存FXNS suiteを、最新commitの全ファイルを持つ隔離環境でネットワーク要求なしに実行し、そのexact headに対する**別の独立Dレビュー**を取る。結果がPASSかつ修正SHAが固定されるまでCをPR #63へ統合しない。

### D — independent audit

PR #69の監査記録を参照したが、これは元A/B/Cのcommitを対象にした部分監査であり、C修正版の独立レビューではない。過去の正しい監査対象commitは保持し、修正版で上書きしたことにしない。Dの部分評価 `PARTIAL_WITH_GAPS` を保存し、無根拠の全体PASSは付けない。

## 変更範囲・安全確認

GitHubでPR #66/#67/#68/#69/#70それぞれのchanged-file listを再取得し、以下を確認した。

- A: `work/source-probe/**` に3ファイル。
- B: `work/xm-source/**` に1ファイル。
- C: `work/implementation/**` に3ファイル。C修正:同ディレクトリ内2ファイル。
- D: `work/independent-audit/2026-10-08/**` に1ファイル。
- E: この統合判断文書 `work/integration/2026-10-08/**` のみ。PR #63本体および他worker branchへの書込はしない。

Specification、CURRENT、SOURCE_CONTRACT、prompt/schema、既存生ニュースデータ、XM tick、CSM/HR/JP225の仕様・holdout・研究判定は変更していない。ユーザーの予定済タスク5件も変更していない。実相場データの方向・return/P&L・勝率、リアルLLM分類、注文は未実行。

## 今後の受け入れ条件

### 統合条件（実装・監査側）

1. GDELTのネットワークlive probeを自動起動するworkflowについて、source-onlyの実行を明示的・適法・固定条件でしか行えないようにし、**offline synthetic checks** を別途実行できることを確認する。Eのallowlistではこのworkflowを編集しない。
2. C修正 `9c5422e6bb92ef34db2303346aa513acf8bf8bab` とA修正 `8e55f817795a68b167f5785f6ac814c898cda11d` を組み合わせたピン留めチェックアウトでnetwork-disabledのsynthetic suitesを実行し、実行ログ・Python環境・コードsource identitiesを保存。Cについて新しい独立レビューを実施。
3. CIと科学的境界を確認した後だけ、承認した変更をPR #63へ非forceで統合し、**統合後のHEADで再テスト・readback**。統合しない差分も記録し、実データでの結果を推測しない。

### 実データへの直接の次の一手（2件以内）

- **XM**: 利用者の意図したローカルWindows XM MT5で、既存collector v0.2を一度だけsource-only実行。固定6窓のtick raw / metadata / SHA manifestと失敗・欠測も保存。時刻・Friday 08:15境界・重複順序・symbol/server・必要コストは独立レビュー。注文情報・口座番号は取得/公開しない。別providerで補完しない。
- **GDELT**: 現行固定DOC query/24h windowのまま、8:00 JST cutoff以前の実際のretrieval receiptの証明とDOC time/網羅性の権威ある評価を得る。過去に12:20 JSTに取得したrawを「8:00に利用可能」と読み替えない。429時の再試行やprovider変更で穴埋めしない。

両source gateを独立にPASSし、モデル条件とpromptをfreezeし、正式Packet DがPASSし、人間の最終承認が記録されるまでは、科学的状態 **UNTESTED / PROPOSED_NOT_FROZEN / COHORT CLOSED** を維持する。

## 最終的な判断と成果指標

今回の成果は、A/Bのsource現況確認・Aのtimestamp error-path修正、Cの合成イベント骨格・D-C-01検出と修正候補、D/Eの責任境界を固定したことである。**GDELTまたはXM source gateを解放した事実、収益性を認定した事実はない。**

新規ファイル・PR・試行件数ではなく、source gateが検証により実際に進んだか、独立性が保たれたか、正式prospective cohortに適法・再現可能に進めるかを次回も測定する。

この文書の判断は上記参照SHA時点に限定。後続担当はgit HEAD/PR/コードとCI状態をfresh readし直すこと。
