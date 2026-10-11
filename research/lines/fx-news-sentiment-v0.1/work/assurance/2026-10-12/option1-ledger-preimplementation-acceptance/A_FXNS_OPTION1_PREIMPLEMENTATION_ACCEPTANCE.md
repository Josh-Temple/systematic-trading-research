# A — FXNS台帳案①の実装前受入仕様・競合線形化点・移行と真正性（2026-10-12 JST）

**結論：`DESIGN_READY / IMPLEMENTATION_UNAPPROVED / MIGRATION_UNAPPROVED / NOT_EXECUTED / HOLD_NO_MERGE`。** 本書は承認済み案①（二形式 `<event_id>.json` と `<event_id>.blocked.json` を維持し、同一IDの競合・不明・検証不能時はfail-closed）の**実装前仕様**。実装・テスト・CI・移行・実データ参照・ゲート操作・mergeは行っていない。既存の二重記録の実在件数も調べていない。

## 1. 適用根拠、exact identity、旧資料との差分

- GitHub repository: `Josh-Temple/systematic-trading-research`。
- 研究branch `research/fx-news-sentiment-v0.1`、PR #63は作業開始時・保存直前ともOPEN/Draft/未merge、**head `24ef9c37e6255126a957f38cfa7470cd150ed594`**。当該コミットのtree `123f6d539c29f188e489bcc1492b632f5c9514d7`は既存#105/#107の証跡による値で、本Aは差分全文を避けるためcommit/tree APIで再独立照合していない。
- 同headから**指定パスで直接取得**：`research/lines/fx-news-sentiment-v0.1/work/implementation/event_ledger.py` blob `3faa396953c7cb951d32d1f3521ea303010e8598`、`test_event_ledger.py` blob `e4bf1a3c8ab6d47c86fb92483d71768e87ab3a05`。
- 参照した既存report：PR #94（head `f4b7614839de653cf3644d0c4f22bc694483afc4`、報告blob `af363897339433dbb0289e38f671cdc5c664b2c1`）、PR #105（head `cda9bcec3ddbd352845c77fa73bb60d28e6b1cab`、報告blob `b4e7d951778e1d9d8f4ba1648b205561a0fff7df`）、PR #107（head `495fd3e9167d11d2787a4667995ee0a7cbf6c201`、報告blob `73100d97bf94c82c0b8fb9a18c0e7e2647579997`）。
- **承認の正本**：PR #107「6. 承認追補」（2026-10-11 JST）。**案①の方針**と真正性対策の**設計・審査**のみ承認。writerの具体的拒否方法、同期基盤、reader API、監査鍵、旧記録移行・cutoverは未承認。
- **旧#105からの新規具体化**：①ファイル名と内部event IDの非結合というコード上の欠落、②全writer/reader/consumerで守る単一の整合性境界と線形化点、③状態別のAPI出力・例外の判定、④永続化と排他を分離したcrash/restart oracle、⑤全件inventoryの型・移行停止票・人間の責任分離、⑥実装許可申請を操作ごとに分割。#105のT01–T16は**設計だけ**であり、同番号を新しい実行結果と誤認させない。

## 2. 現行実装から確実に言えることと、新規の受入上の欠落

**直接静的確認**：
1. `write_synthetic_event` は検査後 `<event_id>.json` を `open("xb")`、file `flush/fsync`、同一bytesの即時readbackで書込。対して `write_blocked_receipt` は `<event_id>.blocked.json` への `xb` と `flush/fsync` で終了し、同等の即時readbackがない。双方とももう片方のパスを参照しない。ファイル単位の `O_EXCL` はevent ID単位の排他ではない。
2. `verify_synthetic_event(file)` は指定された**一つのファイル**の末尾改行、strict JSON member、outer `record_sha256`、nested synthetic recordを検証して返すが、**渡されたfileの basename が内部 `record.event_id` と対応するかを検証しない**。このAPI単独では相手形式の存在確認・readerの原子的snapshot・権限ある置換者の検出を保証できない。未知の呼出元で無条件に正常決定として採用されないことも未確認。
3. `test_same_event_id_normal_and_blocked_files_coexist_design_hold` は両形式が同一IDで共存し**個別verifyを通る**ことを意図的に示す。これは競合を拒否する受入テストではない。#99由来の重複JSON member拒否とも別の問題。
4. `write_* ` の `mkdir(parents=True, exist_ok=True)`、`Path(file).read_bytes()` には、管理者や他プロセスが変更するパス・ディレクトリ・symlink/hardlinkへの権限保証は実装されていない。後述のパス隔離とACLは**要求仕様**であり、現状にあるとはみなさない。
5. `issue_formal_event` / `associate_market_outcome` は現在 `EventBlocked` を出し、`COHORT_STATE="CLOSED"`。台帳の設計PASSはこの停止を解除しない。

**脅威と非保証**：同期に参加しない旧reader、別ホストの独立writer、再起動後の古いcache、privileged attackerによるrecord+digest整合置換、監査ログと正本の同時改変、ディレクトリ置換、書込後の障害、接続FSのlock/fsync意味論の不一致。通常の読取成功やSHA-256一致だけでは安全性を認定しない。

## 3. 案①の仕様上の状態・返値・停止条件

以下は**実装候補への受入要求**。API名・例外クラス名は具体実装の承認前に固定しない。「正常」と「blocked」を同じ肯定的なdecisionとして返すことを認めない。

| 安定したID単位の観測 | 受入期待値 | 記録／許可 |
| --- | --- | --- |
| 双方なし | `MISSING`。通常判断を生成しない | 新規createは別途writer資格・同期条件を満たす場合だけ |
| 通常のみ・内部recordとfilenameのID一致・検証完了 | `NORMAL_SYNTHETIC_ONLY`。合成の決定を返せる | formal発行はなおCLOSED |
| blockedのみ・ID一致・検証完了 | `BLOCKED`。理由を残す。 `NO_TRADE` へ変換しない | 正常決定を返さない |
| 両形式が存在（片方のhashが正しくても） | `CONFLICT`、理由と二つのパス識別子。**非決定** | 自動優先・削除・隔離解除なし |
| 破損・パスと内部ID不一致・不正UTF-8・重複member・未知形式・未完成・不明なtemp/txn残骸 | `UNRESOLVED` / `QUARANTINED`、原因コード | 他方が正しくても肯定的な返却を禁止 |
| lock失敗・アクセス権不足・古いsnapshot・同期に未参加のconsumer・不明な永続化状態 | `UNAVAILABLE` / `UNRESOLVED`。失敗理由を記録 | **ロックなしの片側readへのfallback禁止** |

既存の `verify_synthetic_event(file)` は**個別検査の低水準API**としてなら残せるが、ID単位の正常判断の唯一の入口としては不十分。全consumerに対し、どの公開APIが「decisionを返せるか」を一覧化し、単独verify成功を最終採用に変換する経路をゼロにする。path引数・recordの `event_id`・期待ID・レコード種別・拡張子を照合し、管理下ディレクトリ外・symlinkを許さない設計にする。これらは実装前レビュー対象であり、既存ファイルを検査・移動しない。

## 4. reader/writerの排他と線形化点：設計段階の選択肢

**不変条件**：同一IDについて二つの意味が衝突する状態、もしくはその可能性を排除できない状態から、どのconsumerも肯定的なdecisionを返さない。全writerと全readerが同じ同期領域／commit解釈を使い、旧readerがそれを迂回できないことを実装とテストで確認する。

- **候補A：同一ホストの協調的なID単位ロック**。IDから決定的に導出したlock対象を、write側は「両形式・temp/障害痕跡の確認→必要なら新規確定書込→dir fsync→ID単位readback」まで保持し、read側は「両形式の存在、全bytesとrecord IDの検証→状態確定→decision返却」まで保持。**readの線形化点**は同一ロック下で全候補の検証を終えて状態を確定した時点。**writerの成功点**は必要なdurable commitとID単位readback後に限定。ロック取得前のcheck、read後のロック取得、片方だけlockingでは不合格。再起動でlockが失われるため、durability/recoveryは別途必要。ファイルlockのOS・FS・NFS等の意味論が未確認の環境では採用不可。
- **候補B：プロセス／ホストを跨ぐtransactional storeまたは権威ある仲介者**。全reader/writerが一つの直列化可能なevent IDキーと世代を参照し、同じsnapshotとcommit点を観測する。ただし二つのファイル以外の権威ある状態・サービスを導入するなら、形式と整合性契約への影響を人間が別承認する。仲介者が止まればfail-closed、旧読取経路は遮断。候補A/Bの採用は未決。
- **新規対立書込の扱いは別承認**：他方が既にある場合、（a）2件目は**書込前に拒否し、独立監査へ拒否事実を保存**、または（b）双方を競合として残して全consumerを停止、のどちらにするかは案①の承認だけでは確定しない。どちらも「競合後に正常と主張しない」ことが必要。失敗したblocked事実を消す・通常を優先する規則を暗黙に導入しない。
- **TOCTOU**：ロック下で個々の `stat()/exists()` を二度呼ぶだけでは、非協調的書込／置換に対して原子的ではない。協調する全実行者の排他・ACL・同一FS確認、世代不一致の停止、試験で証明できる範囲を固定。書込後に他者がデータやパスを交換できる脅威では真正性／特権分離が必要。
- **timeoutと再試行**：lock失敗・timeout・予期せぬ例外は停止。再試行による二重作成や同一IDの反対形式の後勝ちを禁止。成功receiptとfailure/unknown receiptを区別し、障害中の「最後のreadが正常」cacheの再利用を禁ずる。

## 5. durable write、crash、再起動の受入点

1. **書込とreadbackを分離して記録**：通常・blocked双方で、事前validator → 隔離tmp作成（既存宛先の上書き禁止）→全bytes書込→file `fsync`→必要な原子的公開操作→parent directory `fsync`→同一ID両形式を改めてreadback、という**候補手順**を比較する。具体的なPOSIX/Windows/FS・atomic rename/rename-no-replaceのサポートが未証明なら成功扱いしない。 `xb` + file `fsync` だけでディレクトリエントリの耐障害性を証明しない。
2. **クラッシュ注入マトリクス**：tmp前、書込中、file fsync前／後、公開前／後、dir fsync前／後、readback前／後、成功receipt前／後の各点で外部停止を注入。再起動後、対象IDの二形式・孤立tmp・必要なjournal/lockの残骸を列挙し、`CLEAN`、`RECOVERABLE_BUT_HOLD`、`CONFLICT`、`UNKNOWN_HOLD` へ保守的に分類する。**完了点未到達の操作を「成功した」と捏造しない**。未確定でもファイルが見えた場合、再照合・監査完了までは正常決定禁止。
3. **2ファイルの原子性の限界**：別々の `rename` や `fsync` は2ファイル一括のatomic transactionではない。event IDごとに協調的に公開状態を固定する設計、障害後に再検証して停止する設計を区別する。存在している古い競合・壊れた記録を一方だけ修復して肯定しない。
4. **成功receipt**：commit済みと判定するために必要なログ・file bytes hash・ID・レコード種別・親ディレクトリ同期結果・双方のreadback hash・世代/同期保証・終了時刻を保存する**設計案**。監査ログのdurable化失敗時の成功返却は不合格。receipt自身が正本を置換できるわけではない。
5. **再起動とcache**：再起動したreaderはID単位の状態を取り直す。last-known-good snapshotを現在の正常判断として返さない。キャッシュと権威ある保存先の世代・hash不一致は停止。多ホスト／ネットワークFSでは協調ロックとflush/FS証明ができない限り`DESIGN_BLOCKED_FOR_ENVIRONMENT`。

## 6. #105 T01–T16を案①の実装受入oracleに固定

**下表はT01–T16の再実行ではない**。実装後、各ケースに「実行コマンド、exact commit/tree、OS/FS、exit、標準出力/エラー、failure/error/skip、関与した全reader、クラッシュ時点、readback/hash、監査receipt」を添付し、未観測をPASSにしない。

| #105 ID | 案①で最低限assertする観測結果 | 追加証拠・拒否すべき誤成功 |
| --- | --- | --- |
| T01 | 通常のみで完全検査・ファイル名↔内部ID一致・相手形式なしを**同一同期境界**で確認 | 片側verify成功だけでdecisionを返したら不合格 |
| T02 | blockedのみでNO_TRADEとの区別・blocked readback/hash・再起動後の理由維持 | blocked側readback省略と「通常に変換」を拒否 |
| T03 | 通常→blocked。既存正常を消さず、拒否か競合停止（選定済みwriter規則に従う） | 再検査なしの「先勝ち正常」を拒否 |
| T04 | blocked→通常。T03と対称。拒否事実を消さない | 後書き通常による昇格を拒否 |
| T05 | 2 process同ID同時writeで排他・linearizationと全receipt整合 | 単に二つの`xb`が成功しただけではPASSでない |
| T06 | writer交差中の2 readerと遅いconsumerが同じID状態を観測、矛盾時全停止 | 片側のみreadや古いcacheの肯定を拒否 |
| T07 | 途中切断・改変・不正encodingはID全体`UNRESOLVED` | 他方validを理由に通過させない |
| T08 | 全crash地点の前後で、成功宣言・永続化・再起動観測の整合を検査 | `rename`だけ、file fsyncだけで耐障害PASSにしない |
| T09 | 片側commit/孤立tmp/索引不一致で復旧後も停止し、履歴・hash残す | 自動で片側を正本化しない |
| T10 | 両形式validでも`CONFLICT`＋隔離、いずれも決定採用しない | 両方の単体verify PASSをIDのPASSにしない |
| T11 | 片側破損・filename/internal ID不一致・symlink等、全ケース拒否 | #99の重複JSON拒否をID単位検査の代用にしない |
| T12 | 承認済み**架空inventory**だけで中断・再開・件数/byte hash一致、対象IDだけHOLD | 実記録移行は別承認、削除なし |
| T13 | 再起動・全consumer・cache再利用への同一停止結果 | 一つでも旧単体verify経由で肯定ならFAIL |
| T14 | 特権者による整合record+digest置換は**hash-onlyでは検出不可**と実証 | 署名・独立保全なしにAUTHENTICITY PASSを出さない |
| T15 | 改変・削除・journal断絶・replayの検知は独立保護の採用後のみ検査 | 未実装の場合`AUTHENTICITY_NOT_ESTABLISHED` |
| T16 | 異ID正常系、LONG/SHORT/NO_TRADEとblockedを区別、formal/outcome APIは常時拒否 | synthetic PASSからSOURCE/COHORT開放不可 |

**本A追加の必須合成負例（#105表から独立の細分）**：①basename↔内部ID不一致、②raw verifierの直接利用をconsumerが許してしまう経路、③readerのlock取得前後で2 writerが交差、④別ホスト／異FS lockの非互換性、⑤権限不足/親directory fsync失敗、⑥symlink／directory交換、⑦成功receipt後に監査書込失敗、⑧復元した古いcacheで一度だけ正常が返る、⑨孤立tempと再起動同時起動、⑩誤った移行解除・rollbackで通常化。いずれも**設計**、実行件数ゼロ。

## 7. 既存競合の架空inventory、移行・隔離・rollbackの承認票

実際のledgerを走査しない。まず完全架空ディレクトリにID単位のinventory表を設計する。**必須列**：固定作業ID、対象event ID、想定rootと相対basename、normal有無/bytes/SHA-256/strict結果、blocked有無/bytes/SHA-256/strict結果、temp/journal有無、record ID↔filename一致、同一ID種別、conflict/unknown reason、発見日時とsnapshot/manifest digest、処理者/独立監査者、承認者、解除判断参照、前後件数と各bytes hash、処理操作・開始/終了時刻、復旧/rollback参照、未確認項目。**現時点の実ID一覧・件数・bytes・SHAは未取得／UNKNOWN**。

移行の手順案：
1. **事前承認**：目的、対象パス、対象期間/ID、アクセス権/保全責任者/監査者、read-only inventoryの安全な手段、閲覧してはいけない資料の入力前遮断、承認済み停止基準、隔離場所とアクセス権、復旧手順を人間が操作単位で承認。担当者・鍵・保管先は**OWNER_NOT_ASSIGNED**。
2. **read-only inventory→隔離**：未解決IDを列挙し、二重記録・異常/欠番・名前不一致を隔離状態として**論理的に停止**。実ファイルの移動・削除・変更はこの段階では行わない。snapshot digest、分類別before counts/hash、操作対象IDリストを独立照合。
3. **人間の個別裁定**：競合IDごとに維持・調査保留・追加証拠・明示的承認を記録。**現在承認された案①には「通常優先」「blocked優先」も自動重複解消も含まれない**。解除不可はHOLDを保持。
4. **実移行の別承認後に限る**：まず完全合成でdry-runし、入力ID/出力状態の写像、before/after counts（normal/blocked/both/corrupt/unknown/quarantined）、manifest digest、原bytes照合、操作ログ、部分失敗/再実行/rollbackを検査。ゼロ差分と監査者の署名または承認参照なくcutoverしない。異常時は書込とdecision発行を停止し、承認済み安全時点への復旧判断を人間へ差し戻す。
5. **cutover/rollback停止条件**：旧reader残存、欠落したIDやhash、同期機構不一致、検証不能bytes、隔離解除票なし、参照可能な監査履歴なし、rollback時に意味の異なる状態が既に公開済み、のいずれかでSTOP。**途中処理したIDの黙示的な正常化は禁止**。

## 8. 信頼性と真正性を別々に受け入れる

| 保証対象 | 最低要件・独立検査 | 現段階の判断 |
| --- | --- | --- |
| ファイル単位の整合性 | strict parser、record digest、file↔event ID、二形式・snapshot検査 | 既存は単体のみ、一部未実装 |
| ID単位の排他・可視性 | 全reader/writerの同一同期境界、linearization、非協調経路の排除 | **NOT_IMPLEMENTED** |
| 障害耐性 | FSごとのatomic/no-replace・fsync・dir fsync、crash recovery、receipt順序 | **NOT_VERIFIED** |
| 作成主体・発行権限 | record bytes・ID・type・version等に結び付けた署名、公開鍵配布・信頼anchor・失効・鍵rotations | **DESIGN_ONLY / KEY_OWNER_NOT_ASSIGNED** |
| 削除・置換・replay検出 | 改変権限が台帳writerと独立したappend-only監査、欠番検出、外部保全と回復 | **DESIGN_ONLY / AUDIT_CUSTODIAN_NOT_ASSIGNED** |
| OS/ファイルの権限 | writer/reader/監査者分離、ACL、信頼できるroot directoryとsymlink方針 | **DESIGN_ONLY / ACL_OWNER_NOT_ASSIGNED** |

**整合するrecord+digestを特権者が置換した例は、digest検証に通り得る。** 限定的な署名を設けても鍵管理者と台帳改変者が同一なら独立した保証は不十分。責任候補と必要な権限は「研究所有者：要指名」「writer実装者：要指名」「独立受入監査者：別人/別Chat」「監査保全責任者：要指名」「鍵/ACL管理者：要指名」「移行承認者：人間が別途指名」。暗号方式、鍵作成、外部保全先、実ACL設定は本Aでは決定・作成しない。

## 9. 次に必要な**個別**人的承認と独立再受入

| 操作 | 最小の承認内容 | まだ許可されていないもの |
| --- | --- | --- |
| ① 台帳API/二形式の同期実装 | 実装担当、exact base HEAD、変更対象は`work/implementation/event_ledger.py`・限定新規helper・reader/consumerの**確認済み個別パス**、方式A/B、writer既存競合時の拒否か保持か、成功receipt定義 | 本Waveでのコード改変、承認していない第三の正本形式 |
| ② 完全合成テストと障害注入 | `test_event_ledger.py`と限定fixture、T01–T16＋本書負例、実行環境OS/FS/Python/隔離権限、独立した失敗証拠 | 外部ニュース/実市場や本番runner |
| ③ 全consumerの到達経路調査・封鎖 | 個別に確認した安全コードパス、全read/signal/export経路と旧API迂回のテスト、事前入力境界 | 無制限repository検索・実ledger読取 |
| ④ 真正性実装 | 署名・trust store・鍵管理・ACL・監査保全・責任者と検査手順**を別々に**決定 | 本番鍵・実権限・ログ保管の無承認変更 |
| ⑤ 既存ID inventory／隔離／移行 | 取得可能なmetadata範囲を事前定義し人間の安全審査、具体的ID対象、before/after/rollback・第三者照合、必要なら別Wave | 実記録の取得・削除・自動裁定・本番cutover |
| ⑥ 独立受入・最終統合 | 実装候補のexact tree/blob、全パス、実test/CI log、独立反証、認証・復旧・consumer coverage、Eと別の人的merge承認 | 自己評価だけでPASS/merge、source再開 |

**判定ゲート**：案①の方針は `LEDGER_OPTION_1_DESIGN_APPROVED`。本書の仕様は実装・移行を許可するものではなく `IMPLEMENTATION_UNAPPROVED`。実装後、writerとすべてのconsumerのID単位検査、crash/restart、既存競合の隔離、真正性を**保証の種類別に**別々に受け入れる。単独合成テストPASSをもって本番安全性を推定しない。

**継続HOLD**：FXNS `SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED / HYP-FXNS UNTESTED / PROPOSED_NOT_FROZEN`。#106/#108の閲覧境界逸脱の最終人的処分はPENDING。GDELT DOC/他source追加取得・実headline/URL・実FX値・market outcome・signal/returns・XM/MT5・取引・鍵/permission変更は禁止。PR #110の局所合成プロトタイプの判定を**台帳安全性の根拠にはしない**。

**作業範囲と未実施**：既知の安全なreport 3本と、研究branch exact-refの安全な`event_ledger.py`/`test_event_ledger.py`の指定箇所だけをGitHub read。未知パス探索・全PR diff/広域コード検索なし。既存T01–T16および追加負例の**実行0件 / NOT_EXECUTED**。対象以外のconsumer一覧、実record inventory、FS特性、OS権限、署名・監査鍵・リモートruntimeは**NOT_VERIFIED**。report-only専用Draft 1ファイル以外には書き込まない。
