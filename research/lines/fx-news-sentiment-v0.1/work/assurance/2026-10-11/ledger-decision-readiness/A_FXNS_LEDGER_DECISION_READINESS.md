# A — FXNS台帳の同一ID競合・真正性：選択後の実装に必要な受入設計（2026-10-11 JST）

**判定：DECISION_READY_FOR_HUMAN_REVIEW / LEDGER_CONTRACT_HUMAN_DECISION_REQUIRED。仕様未承認、実装未着手、テストNOT_EXECUTED。** 本報告は既存[PR #94](https://github.com/Josh-Temple/systematic-trading-research/pull/94)を置換せず、同報告に不足する具体的な失敗時の期待結果・移行停止条件・検証証拠を追加する。①〜③のどれも選択していない。実相場・GDELT live DOC・XM・市場outcome・本番鍵にはアクセスしていない。

## 1. 対象・再取得した証拠と修正済み／未修正の区別

- Repository: `Josh-Temple/systematic-trading-research`。対象研究branch `research/fx-news-sentiment-v0.1`、[PR #63](https://github.com/Josh-Temple/systematic-trading-research/pull/63) OPEN/Draft。A開始時のbranch HEAD `24ef9c37e6255126a957f38cfa7470cd150ed594`、直接取得したGit tree `123f6d539c29f188e489bcc1492b632f5c9514d7`（[merge commit](https://github.com/Josh-Temple/systematic-trading-research/commit/24ef9c37e6255126a957f38cfa7470cd150ed594)）。このheadより前の#94 base `b1b31e5...`を現行と取り違えない。
- 現行 `work/implementation/event_ledger.py` blob `3faa396953c7cb951d32d1f3521ea303010e8598`、`test_event_ledger.py` blob `e4bf1a3c8ab6d47c86fb92483d71768e87ab3a05`。両ファイルを対象exact refで読み、書込・readback・検証の実装を確認。パスの共通prefixは `research/lines/fx-news-sentiment-v0.1/`。
- 統合済み[PR #99](https://github.com/Josh-Temple/systematic-trading-research/pull/99)の変更：`verify_synthetic_event`は、永続化されたJSONの**同一object内の重複member**を `json.loads(..., object_pairs_hook=_unique_ledger_json_members)`で拒否する。独立B [#101](https://github.com/Josh-Temple/systematic-trading-research/pull/101)はそのexact treeをsynthetic-only `PASS_SCOPED`、Actions run `38006886615`/job `114077610920`で96件成功を確認したと記録する。**本Aによる新実行や新CIではない**。E [#103](https://github.com/Josh-Temple/systematic-trading-research/pull/103)は#99だけを研究branchへ統合した。
- **未修正の別現象（競合）**：`write_synthetic_event`は `<event_id>.json`、`write_blocked_receipt`は `<event_id>.blocked.json`へ別々に `open("xb")`。各ファイル単位の既存保護はあるが、異なる2パスのイベントID単位排他・確定状態の同期はない。`verify_synthetic_event(file)`は渡された**一つのファイル**のみを検査し、対応するもう一つを探索しない。`test_same_event_id_normal_and_blocked_files_coexist_design_hold`は両ファイルが個別検証できる状態を既知ギャップとして示す。これは#99の修正対象外。
- **未修正の別現象（真正性）**：`record_sha256`はレコードとダイジェストの不整合を検出するが、権限ある主体が妥当なrecordとdigestを一緒に置換した場合、作成主体・発行権限・履歴は立証しない。既存の静的テストはその限界を示す。署名・独立保全・ACLを導入済みとは扱わない。
- [#94](https://github.com/Josh-Temple/systematic-trading-research/pull/94)は①曖昧ID停止、②単一正本、③明示的優先／競合管理の三案と概略の費用・安全境界を整理済み。本報告の**追加分**は、下記の操作単位の受入oracle、移行時の拒否・回復条件、各構成の非保証、B/CIへ引渡す証拠要件である。

## 2. 未承認の選択肢と検証可能な契約（提案、現行実装ではない）

| 案 | 将来決定すべき観測上の契約 | 同時実行・障害の要件 | 既存二重記録の扱い | 未保証・追加コスト |
| --- | --- | --- | --- | --- |
| ① 二つのパスを残し、曖昧IDをfail-closed | 読取APIがID単位で両方と異常ファイルを調べ、両方存在・検査不能・矛盾なら**決定を返さず競合／停止**。単一ファイルの検証成功をID全体の承認と取り違えない | 他方の有無の事前checkだけではTOCTOU競合を防げない。書込・確定read・consumer間でロックまたは同等の整合した可視化境界を定義。race中に正常決定を返さない | 競合履歴を隔離し、手動判定まで保持。暗黙の消去・自動優先は禁止 | 履歴互換性は比較的高いが、読取側も全件列挙・停止・再試行が必要。安全なIDごとの直列化を証明できなければfail-closedのみでも不足 |
| ② ID単位の一つの正本 | ID→一つの権威ある状態／レコードの表現と、正常↔blockedの許可／禁止遷移を**人間が明示**。一つのIDに相反する確定決定を認めない | ID単位の原子的作成／更新、競合時のcompare-and-swap相当、確定前のtemp/commit/dir fsync、再起動後の確定記録照合の設計が必要 | 現行二形式のマッピング、差分保存、照合不能IDの隔離。成功確認まで旧ファイルを破棄しない | データ形式とwriter/readerの広い改修。単一ファイルにしただけでは状態遷移・真正性を保証しない |
| ③ 二形式と明示的な優先／競合状態 | **優先規則または第三のCONFLICT状態そのものが未承認**。既存2ファイルのどちらを採るか、選択根拠の記録と全consumer一致を契約化する必要 | 2ファイルと索引／裁定記録の原子的整合性。索引書込前クラッシュ・古いcache・複数consumerの解釈差を拒否または検知 | 競合ごとに裁定履歴を保全し、未決ならfail-closed。移行が一部だけ済んだ場合は対象IDを止める | 優先の正当性、索引再構築、監査追跡の複雑性。無根拠な「blocked優先」等は設定しない |

**3案共通の安全制約案**：未承認時は現行合成プロトタイプのまま正式発行を閉じる。実装後も、保存・ロード・外部consumerのうち一つでもID単位の整合性を実証できない場合、正式発行を開かない。

## 3. 承認後のsynthetic-only受入試験：操作・期待結果を分ける

以下は**試験仕様案**であり実行結果ではない。全ケースで同じ `SYNTHETIC-FXNS-20261008` 等の架空ID、架空レコード、隔離tmp directoryを使用。全案の「正常→blocked」「blocked→正常」に対する最終状態は**人間が定める遷移規則に依存**し、現時点でどちらかを採用したと断定しない。

| ID | 操作／故障注入 | 必須の検証結果（案固有の可否は承認後に固定） |
| --- | --- | --- |
| T01 | 通常だけ新規作成→bytes/fsync→readback→再読込 | 記録の厳密検証、ID一致、別パス不存在／権威状態一致、結果の決定性 |
| T02 | blockedだけ新規作成→readback→再起動 | blockedをNO_TRADEや通常決定へ変換せず、停止理由が残る。blocked側の書込後readback不足を補う |
| T03 | 通常→blockedを同一IDに逐次要求 | ①競合なら停止、②承認済遷移以外は拒否、③裁定規則未確定なら停止。どの場合も黙った上書きなし |
| T04 | blocked→通常を同一IDに逐次要求 | T03と対称。後からの通常レコードで拒否事実を消さない／明示的に許すなら監査痕跡を要求 |
| T05 | 別プロセス2つが同一IDを同時create、順序入替・繰返し | 有効な確定レコード／権威状態が矛盾して公開されない。排他・線形化点、負けた書込の例外／再試行結果を採取 |
| T06 | readerが一方を読んだ直後に他方がcommit、consumer複数 | race後のID状態を取り違えて決定を返さない。ロックなしの二回存在checkのみを成功としない |
| T07 | open後一部bytesだけ書込、末尾改行なし／digest不一致 | 未完成を正常扱いせずBLOCK/隔離。障害回復後にも不完全を受入れない |
| T08 | ファイルflush前・fsync前・後、rename前・後、directory fsync前・後に電源断相当の停止を模擬 | 各commit点の永続性・可視性の設計上の期待を明示。欠損・孤立temp・誤った「成功」receiptを拒否 |
| T09 | 二つ目のファイル／索引のみcommit後にクラッシュ→再起動 | 全ファイルと索引を再照合し、片側のみを正当化しない。復旧可能状態・隔離状態の判定が決定的 |
| T10 | 既存同一IDに通常・blocked双方（どちらも個別hash妥当） | 移行が承認されるまでIDを隔離。サイレント選択・削除・優先なし |
| T11 | 既存二重記録の片方が破損／未知フィールド／不正UTF-8／重複JSON member | 他方が正常でも全体を未解決として扱う。#99のobject-level拒否とID-level矛盾検出を別assertionにする |
| T12 | 移行途中で失敗／権限不足／容量不足→再実行 | 途中の成功記録を捏造せず、冪等な再実行または隔離。before/after inventory、件数・内容hashと未処理IDを照合 |
| T13 | 競合を認識した後、再起動・cache復元・複数consumerからアクセス | 各consumerが同一の停止／承認済状態を返す。古いcacheやevent単体検証によるすり抜け禁止 |
| T14 | privileged actorが妥当な全record+SHAを置換 | 現行hash-onlyでは**検出できない想定の陰性**を明示。署名／独立保管が別にあれば検出・報告の試験を独立定義 |
| T15 | 保護されたjournalなしの記録削除、または正規journalの欠落／連番断絶／再生 | 単なる存在・整合hashでは削除証拠にならない。採用する保護機構がなければAUTHENTICITY_NOT_ESTABLISHED |
| T16 | 異なるイベントID、合成LONG・NO_TRADE・blockedの正常系 | 既存の合成正常系を維持し、NO_TRADEとblockedを混同しない。正式発行／outcome joinは常にCLOSED |

**合格の単位**：テスト名と個別subcaseの対応、対象コミット/tree/blobs、期待値（承認済み版）、実施時刻・Python/OS、実行コマンド、exit code、failure/error/skip、ログ、クラッシュ注入位置、再起動readbackのbytes/hashを保存。方法定義だけを「実行PASS」としない。

## 4. 移行前提・停止基準・最小改修領域（すべて未実装の設計）

1. **移行前inventory**：IDごとに通常／blocked／双方／どちらもなし／破損／未知形式／未完成／既存tempを分類し、ファイル名・byte hash・検証結果・重複の件数を記録。二重記録の優先を自動判断しない。
2. **承認した対応表**：各分類を新状態、隔離、保留にどう写すか、どの状態遷移を許すかを正式な決定記録へ固定。対応不能は保留。旧bytesを消さずに照合可能にする。
3. **変更の最小候補**：`event_ledger.py`の二つのwriterとID単位の読取／検証入口、必要なら新しい合成専用のID索引・状態遷移・排他／atomic commit補助、`test_event_ledger.py`のT01–T16、新形式を採る場合の限定された移行ユーティリティ。既存`fxns.py`、source probe、固定PROMPT/SCHEMA、SPEC、workflow、gate、`main`は**このAでは変更しない**。どの補助を採るかは承認された案に依存。
4. **cutoverの判定**：対象IDのinventory差分ゼロ（承認済み隔離対象を明示）、原記録との照合・数・hash追跡、読み戻しと再起動試験、異常時に読取・発行が停止する証拠、復旧手順の独立レビューが必要。部分的に移行した時点で旧readerを黙って生かさない。
5. **障害復旧**：障害直後は入力を追加せず、原記録を保全し、隔離されたIDを列挙して修復理由・操作者・before/after証跡を残す。代替ファイルを差し替える手続は署名・承認や保管管理が確立されるまで仮設計に留める。
6. **rollback**：新旧混在したまま両writerを同時稼働させない。戻す場合も監査履歴、未移行ID、状態遷移の非可逆性を考慮して承認を取り、失敗時は停止を優先する。

## 5. ハッシュ、本人性、改変履歴は別の保証

| 構成候補 | できること | 単独では証明しないこと／必要な独立証拠 |
| --- | --- | --- |
| 現行canonical JSON＋SHA-256、strict parser | 期待する構造と内容に一致するか、不整合や重複keyの検出 | 作成主体・承認権限・原文からの非改変・削除・完全な履歴。全record+digestの整合置換は通りうる |
| ID単位の排他とtemp→atomic rename、file/dir fsync | 適合するFSと手順で並行書込、部分可視化、クラッシュ耐性を改善しうる | 権限ある改変者の排除、外部監査、マシン・FSを超えた絶対的永続性。renameだけ／file fsyncだけで十分と主張しない |
| 記録と文脈（ID・type・version・prev hash等）を結び付けた電子署名 | 対応する信頼済み公開鍵への検証と対象bytesの改変検知 | 鍵所有者の実身份・適法な権限・鍵流出なし・署名時刻・取消状態。別途鍵配布／権限・失効・検証境界が要る |
| 独立保護されたappend-only監査記録と外部保全 | 保全された別主体の証跡と照合できれば置換・削除・順序異常を検出しやすくする | 同じ特権主体が両方書換可能なら独立証拠にならない。保持期間・ACL・外部読戻し・欠番検出が必要 |
| 保管ACL・最小権限・監査権限分離 | 誰が書けるかの制限と事故範囲縮小 | 記録の作成主体自体の暗号学的証明、OS管理者侵害耐性、災害からの復旧。root-owned trust store/本番鍵の作成・操作は別承認事項 |

**方式との関係**：①はread/writeのID全体の整合と別保護された監査、②は単一正本の版・遷移の署名／履歴、③は裁定の根拠とその署名・索引変更履歴の保全がそれぞれ必要になり得る。ただしどの案もSHA-256だけで真正性は達成できない。署名の秘密鍵、trust store、OS ACL、本番保管領域は本Aで新設・変更していない。

## 6. 人間への一問と次の独立受入

**人間への一問：** 同一event IDの将来の権威ある扱いとして、①「二形式を残し曖昧IDは停止」、②「IDにつき単一正本（遷移は別途承認）」、③「二形式と明示的裁定・競合状態」のどれを選びますか。また**既存の二重記録は、選択した方式への照合・移行が個別承認されるまで隔離し、暗黙に優先・削除しない**という条件を承認しますか（未承認なら設計・移行・formal gateはHOLD）。

承認が得られた**後にのみ**実装担当がT01–T16の期待値を選択案と移行規則に固定し、新規の限定コードPRを別Waveで作成する。独立Bはその**新しいexact HEAD/tree**を取得してwriter/reader/consumer/移行fixture・negative matrix・ローカル再実行の有無・同一tree offline CIの実ログを検査する。Eは明示的な承認と全証拠なしにmergeしない。

**本Aの実施／非実施**：GitHubコード・test・#94・#99・#101・#103のread-only確認とreport作成。T01–T16は設計のみで**NOT_EXECUTED**、A独立run **NOT_RERUN**。候補の比較・クラッシュ時期待動作は設計上の提案であり試験観測値ではない。既存の研究状態 `UNTESTED / PROPOSED_NOT_FROZEN`、GDELT `SOURCE_QUALIFICATION_BLOCKED`、formal cohort `CLOSED`を保持。source取得・本番運用・XM/MT5・実相場・outcome・注文・取引、code/SPEC/workflow/gate変更なし。report-only Draft PRはmerge禁止。
