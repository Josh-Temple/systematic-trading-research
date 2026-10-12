# B限定差分 — D04/D05 silent-success故障のhost配送・監査受入条件（2026-10-12）

**判定:** `SPEC_DELTA_ONLY / PLATFORM_NOT_ENFORCED / BOUNDARY_NOT_ENFORCEABLE_FOR_UNRESTRICTED_WORK_TOOLS / NO_FETCH / HOLD_NO_MERGE`

**対象:** `Josh-Temple/systematic-trading-research`。研究branch固定起点 `24ef9c37e6255126a957f38cfa7470cd150ed594`。本報告はB専用の**1ファイルの設計差分**であり、合成コード、host、CI、権限、source、gateの変更ではない。

## 1. 安全な限定照合と出所の区別

- Library正本：`2026-10-12_fxns_pr117_eight_findings_remediation_independent_reacceptance_and_gate_handoff_wave_instructions.md`。D04（publishが正常終了しても配送事実・明示ACKなし）、D05（appendが正常終了してもreceipt保存なし）は、先行会話内の完全架空追加反証21件中の**期待不達8件のうち2件**。ローカルD testソースはGitHub未保存であり、Bは再実行・byte一致を主張しない。
- 前回B #116の**既知安全な報告blob** `adb6727985e1aa3e7c1025e20ab1921871ddd731` をexact SHAで読取。§2.4、§4、H14/H15/H18には「正常戻りはhost ACKではない」「永続append」「UNKNOWN/no retry」「独立model ingress観測」という原則が**既に存在**する。
- PR #117の既知完全合成 `safe_boundary.py` blob `25877308362fea8cefb8539f41b242c651606911`、`test_remediation.py` blob `c38987c8dae2acf0764ae0c00387df40633ffef8`、`README.md` blob `e0d76535354b450ba6d44948c899cafc62e3bf08` を限定読取した。研究branchのref `24ef9c37e6255126a957f38cfa7470cd150ed594`、#117 branchのref `8f69bded3be746f9f6b6fd1011ea8676f5d32877` を固定ref metadataから確認。
- **静的に検証できた機構:** `Boundary.run` は `DeliverySink.publish(content)` から例外がなければ `_audit("RELEASED")` に進む。`Boundary._audit` は `ReceiptSink.append(...)` が例外なく戻れば `True` を返す。どちらも他の主体が確認した明示ACK、耐久化済みreceiptのindependent readbackを型付き検証していない。これらは合成実装の限界であり、実Workの弱点を直接測定した事実ではない。
- PR body/自由文/広域検索/未知diff、実GitHub wire、実headline/article/URL、GDELT/ECB/FX/market/source raw、#106/#108禁止内容、credential、host hidden log、実probeは**取得・実行しない**。

## 2. #116に対する狭い差分

**新しい設計原則ではなく、H14/H15/H18の受入ケースに対する具体的な欠落補完。** 旧H14は監査保管先の障害を、H15はACK不明と配送後監査失敗を、H18はhost ACK・監査記録の照合を指定する。一方、APIが**エラーを返さず何もしない**場合の反証fixture、検査位置、観測主体、合否の型付き条件を独立ケースとして要求していなかった。既存H01–H18の番号・未実行状態を改変しない。

### H19 — synthetic silent-success publish（D04からの明示追加）

- **入力:** 完全架空の1 requestと承認済みdigest。合成delivery adapterが `publish(bytes)` を正常returnするが、受信側の配送記録・明示ACK・モデルingress観測はいずれも作成しない。別条件として、古いACK、異なるrequest/content hash、偽造または未署名ACK、ACK喪失を注入する。
- **期待:** `RELEASED`または成功bytesを返してはならない。配送試行後、観測可能なACKがない場合は公開有無を断定せず `UNKNOWN / NO_RETRY`。配送前の拒否が客観的に証明できる場合のみ `BLOCKED`。ACKが形式的に存在するだけでも署名者/権限/対象/対象bytesの証明がない場合はFAIL。
- **将来必要な実host側証拠:** 下流の**受信主体**（送信側publishとは別の信頼境界）から、`request_id`、document/operation、delivery identity、受信対象content digest、受信先principal/session、受信判定、時刻またはnonce、ACK schema version、署名/検証主体の識別を含む**認証済み構造化ACK**。配送元の自己申告だけでは不可。モデルingressに何が届いたかの独立観測も別証拠として必要。
- **安全な正常系:** 正しい1件だけが届き、独立観測済みACKとcontent hashが一致する場合のみ、その宣言した障害範囲内で成功とする。複数回・再起動後のexactly-onceは非保証。

### H20 — synthetic silent-success append（D05からの明示追加）

- **入力:** 完全架空の `RESERVED` appendが正常returnするが、耐久監査保管先に該当receiptが存在しない。別条件として、誤ったreceipt ID/状態/policy/対象hash、署名失効、読戻し失敗、`RELEASED`追記のみno-opを注入する。
- **期待（配送前）:** appendの呼出し成功では通過しない。監査保管主体からの**一意なdurable receipt identityおよび独立readback/検証**ができない場合、`publish` 呼出しゼロ・配送ゼロ。`RELEASED`作成禁止。
- **期待（配送後）:** 受信可能性が残る状況で `RELEASED` receiptの追記/確認が失敗した場合、配送済みを遡及的に取り消したと扱わない。`UNKNOWN / NO_RETRY`を保持し、後追い監査と人間の処分へ。追加publishによる修復は禁止。
- **将来必要な保全証拠:** 監査保管者を配信者と分離。append requestに対して、receipt ID・状態・request/policy/operation/content hash・保存先・durability確約の範囲・署名/鍵有効性・独立取得/復旧可否を確認。単一Python listの再読込では外部耐久性を証明できない。append-only権限、保管期限、復旧時の整合性、失効の責任主体は別途設計・人的承認が必要。

## 3. 独立受入で区別すべき観測

| 対象 | 当Bで確認可能 | 本番独立受入に未取得の証拠 |
| --- | --- | --- |
| #117 synthetic実装 | 既知blobの**静的な無例外return依存** | 新A修正の新固定SHA・新テスト・別Chat Dの独立実測 |
| H19 delivery | no-op fault injectionの入力/期待/結果判定を仕様化 | 独立した実受信側のACK、model ingress bytes、実host permission/egressの拒否receipt |
| H20 audit | no-op appendの入力/期待/結果判定を仕様化 | 別主体のdurable append/readback、鍵・失効・障害時処分のhost実証 |
| #116 H01–H18 | 原設計と既知報告を比較 | **H01–H18: 0実行、0実host PASS**。H19/H20も本Bで実行0 |

各将来caseは `fixture_id`、架空input hash、ACK/receipt failure injection、expected/observed state、delivered count、remote readback identity、独立観測者、tool/host build/configと权限、exit/skip/error、ログの安全なdigestを残す。モデルへの禁止rawの混入有無は、**モデル投入前の別権限で**観測する。禁止原文をモデルに投入して再検査してはならない。合成runner PASSをhost ACK/監査/権限強制のPASSへ転用しない。

## 4. 残るゲートと人的承認

`PLATFORM_NOT_ENFORCED / BOUNDARY_NOT_ENFORCEABLE_FOR_UNRESTRICTED_WORK_TOOLS / NO_FETCH / HOLD_NO_MERGE`維持。実Workが全tool・connector・browser・shell・file・network・cache・OCR/previewをhost側で拒否できるかは`NOT_VERIFIED`。専用GraphQL broker、principal、独立safe-excerpt審査者、ACK発行主体、永続audit owner、鍵管理、署名/失効設計、実delivery、独立D、実GitHub wireは**NOT_IMPLEMENTED / NOT_EXECUTED / NOT_VERIFIED**（該当範囲）。実装・設定変更には別個の具体的人間承認と、禁止rawに触れない独立host反証が必要。

FXNS `SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED / HYP-FXNS UNTESTED / NO_QUALIFIED_ALTERNATIVE`、CSM I2 `BLOCKED / CLOSED / market_outcome_access=false`、#106/#108の最終人的処分 `PENDING`。本Bはコード修正・新host probe・GraphQL/GDELT呼出し・CI/Actions・source/market取得・gate変更・mergeを**一切実施しない**。

## 5. 実行receipt・限定性

本Bの新事実は **#117の静的なno-op成功経路** と **既存H14/H15/H18に対応する明示的な二つの反証条件不足** のみ。#116の全体アーキテクチャ、既存H01–H18、以前の実測の独立性は変更しない。過去の同一Chat追加D21件を独立合格とは数えない。作成物はこの報告1件だけ、独立したB branchからFXNS研究branch向けの**Draft PR**に限定し、`[skip ci]`はCI成功ではない。GitHub保存の最終receipt（新head、blob、差分path、readback）は保存後に照合する。
