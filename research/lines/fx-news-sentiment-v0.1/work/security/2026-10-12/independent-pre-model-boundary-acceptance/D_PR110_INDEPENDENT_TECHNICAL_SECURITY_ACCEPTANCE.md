# D — PR #110 独立技術・安全性受入監査（2026-10-12 JST）

**結論：NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE。SECURITY_ACCEPTEDではない。**
被監査者の22/22の自己申告を追認せず、既存22試験を独立再実行し、別の完全合成反証14件を実行した。既存は22/22 PASS、独立反証は**5件が期待条件を満たし、9件が期待条件を満たさなかった**。後者には、実装自身の局所的欠陥（並列二重公開、部分delivery後の再公開、誤ったRELEASED監査、mutable approval）と、元から未実装と開示済みのtrust precondition/照合要件を分けて含む。実市場・ニュース・禁止ログ・実モデルを用いた試験ではない。

## 1. 根拠・identity・非干渉

- 研究repo：`Josh-Temple/systematic-trading-research`
- 被監査 [PR #110](https://github.com/Josh-Temple/systematic-trading-research/pull/110)：OPEN / Draft / unmerged。base `research/fx-news-sentiment-v0.1`, base SHA `24ef9c37e6255126a957f38cfa7470cd150ed594`; head `0faf05b453c5d7897c3566d871591b2926ba928e`; tree `380d646e017be68ef45f57c5889c78b52fe41605`。
- #110の変更は次の4新規ファイルのみ（いずれも `research/lines/fx-news-sentiment-v0.1/work/security/2026-10-11/synthetic-pre-model-gate/` 以下）：
  - `safe_boundary.py`: Git blob `cfa10e14af6780659f79cf25fc9cf743844ea4d1`、SHA-256 `657619311e8f4045b8e60a8a71085e52782649a0dbe2dda3b52a96d267857678`、12,673 bytes。
  - `test_safe_boundary.py`: Git blob `97fdb367d198426c1b5da4600ec1ea3f771e9ac2`、SHA-256 `e1bc61dcd6d1b79adc086fc80d819d8186bd2afc0a2e2092f3c81ed3572ce515`、8,596 bytes。
  - `README.md`: Git blob `d9261c5716aae0e85fcdaced85d2d050e516d406`。
  - `TEST_RECEIPT.md`: Git blob `1ccfbaa8d71a7a090014f041008580f16894d52a`。
- 仕様 [#109](https://github.com/Josh-Temple/systematic-trading-research/pull/109) exact head `4ed6c59105ae33d55ffe2ae6bf718d92ae000fc7`、安全な監査文書内の§6・§8・§9の必要部分（T01–T22）を対象とした。#106/#108の禁止された原記録・raw・実headline/値・商品順位は取得していない。
- 着手時 `main` HEAD `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`、FXNS研究branch HEAD `24ef9c37e6255126a957f38cfa7470cd150ed594`。GitHub RESTの既知ref metadataで取得。#110を直接変更していない。
- 報告者が実装したのは**GitHub候補の変更ではなく隔離領域の追加反証14件**のみ。元候補2 PythonファイルはGitHub exact HEADから取得した内容をローカルに配置し、双方のSHA-256とGit blobが上記と一致した後だけ実行した。ネットワーク到達性なし。実repo clone、pip、CI、Actions dispatch、実connector呼出しなし。

## 2. 独立した実行証拠（完全架空・ローカルのみ）

- 実行系：Python `3.13.5`、標準ライブラリ `unittest`・`py_compile`、隔離一時パス `/mnt/data/fxns_d_audit_20261012/`。対象候補本体は改変していない。
- 元22件：`PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_safe_boundary`、exit **0**、`Ran 22 tests`、`OK`、failures=0 / errors=0 / skips=0。stdoutは空、testごとの結果とsummaryはstderr。stderr SHA-256 `13cd904eea72a0fcbabc2f05e57c7fc8e6d4182ebf1b9fd16bd7ed07a48298fd`。T01–T22全件 `ok`。
- compile：`PYTHONDONTWRITEBYTECODE=1 python -m py_compile safe_boundary.py test_safe_boundary.py`、exit **0**、stdout/stderrとも空。
- 独立追加14件：`PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_independent_adversarial`、exit **1**、`Ran 14 tests` / `FAILED (failures=9)`、errors=0、skips=0。stdoutは空、各ケース・traceback・summaryはstderr。stderr SHA-256 `f160d83d72d68199dd4ac10f83356a9e71a890753d01b93fefa8febe2630e8cb`。
- 独立追加テストコードのローカルSHA-256：`5e182f8898b9115188bdf481146d1a4943cfba67fd5158998e5c8c034620c9bd`。**追加test codeはGitHubへpushしていない**。追加試験は元の22件とは別に起動。元の成功と独立反証の失敗を混合した「36/36 PASS」とは主張しない。
- 試験がモデル入力の漏洩不存在を示す範囲はPythonの`DeliverySink`のみ。host、wire、browser、shell、network、実model input、durable logのテスト数は0。

## 3. 独立追加14ケースの個別実測

**FAIL**は「試験で設定した安全性の期待条件に反した」という意味。既存実装の文書で明示される非目標と、新たに発見した局所欠陥は区別する。

| ID | 架空入力・操作／期待条件 | 実測 | 判断 |
| --- | --- | --- | --- |
| R01 | 同一`Boundary`への同一operationを2スレッドで同時実行。合成audit appendのbarrierで両者を同期。配送は最大1回 | 配送 **2回** | **FAIL**：checkとsetが原子的でなくrace |
| R02 | `DeliverySink.publish`が最初にbytesを追加した直後に例外を投げる。再試行でも最大1回 | 配送 **2回** | **FAIL**：不明な部分delivery後に再配送 |
| R03 | `publish`が配送前に例外。監査に`RELEASED`を残さないこと | 未配送なのに`RELEASED`記録あり | **FAIL**：監査のstateが実配送を誤表現 |
| R04 | `Policy(frozen=True)`の内部`approved_documents` dictを生成後に更新。既存の安全承認が勝手に変わらないこと | 未承認の完全架空markerが出力 | **FAIL**：承認設定の可変参照 |
| R05 | 同一policy/sinksで新`Boundary`を作成し同一operationを再実行。重複禁止を維持 | 配送 **2回** | **FAIL**：インスタンス内setしかない（分散/再起動の非目標として既知でも運用受入不可） |
| R06 | requestに未承認`request_id` fieldを追加して遮断確認 | 遮断、配送0 | **PASS_SCOPED**（ただし認証済みrequest ID機構は未実装） |
| R07 | metadataの`draft`にnested dict/markerを混入 | 遮断、配送0 | **PASS_SCOPED** |
| R08 | page1は許可、page2に非許可path | 全体遮断、配送0 | **PASS_SCOPED** |
| R09 | 3ページ中cursorを循環させる | 全体遮断、配送0 | **PASS_SCOPED** |
| R10 | 巨大な架空文書body | 遮断、配送0 | **PASS_SCOPED** |
| R11 | 最初から`ApprovedDocument.safe_excerpt`を架空禁止markerに設定。事前承認の不備を自力で検知すること | そのmarkerを出力 | **FAIL**（コンテンツ審査はコード外の信頼前提。未実装を新たな実安全保証として扱えない） |
| R12 | `Policy.policy_id`に架空自由文marker。内容なしreceiptが固定schemaに収まること | receiptの`policy_id`にmarker | **FAIL**：policy由来の未検証自由文がauditへ伝播（source response漏れとは異なる） |
| R13 | `PR_METADATA`に`state=OPEN, merged=true, draft=true`。論理矛盾を拒否すること | そのまま公開 | **FAIL**：field個別型検査は行うがstate整合制約がない |
| R14 | 許可pathと任意の40桁hex blob OIDを組にする。事前に承認したexact blob以外を拒否すること | 任意blob OIDを公開 | **FAIL**：path allowlistのみ。#109が求めるexpected blob identityとの照合なし |

R01–R05の最小再現は次のとおり。いずれも架空の `fixture()` / `request()` / `metadata()` のみ：
- **R01**：二つのスレッドで `b.run(request(), metadata())` を呼び、`ReceiptSink.append(state="RELEASED")`に2者同期barrierを置くと`len(delivery.delivered)==2`。
- **R02**：`publish`が`delivered.append(content)`後、一度だけ`RuntimeError`を投げる。最初の`run`が`None`、再`run`で公開が再び行われる。
- **R03**：`publish`を即例外にした場合、受信数0でも`receipts`に`RELEASED`と`BLOCKED`が残る。
- **R04**：最初に正しいhashを持つ`ApprovedDocument`を生成後、元dictの`PATH`値を同hash・marker入り抜粋に置き換える。承認監査を経ずに配送内容が変化する。
- **R05**：`b.run(...)`後、`Boundary(b.policy, sink, receipts).run(...)`を呼ぶと再配送される。

R11/R12/R13/R14は完全合成のtrust-precondition/型・identity検査を厳しくした追加期待条件。実hostでの攻撃成立を検証したものではない。R11はREADMEが明示する**外部審査への依存**であり、コードだけの機能追加を唯一の修正解と決めつけない。

## 4. 静的監査：API、順序、可変状態、真正性

1. **入力開始**：`_start`は3 literal operation・4 field request・repo/PR/headの一致を要求。ただし署名済request identity、期限、principal/権限はなく、request IDの概念もない。`run`が`request.get`をtryの外で実行するため、通常dictの有効な形では問題を観測しなかったが、host例外隔離の実証ではない。
2. **応答検査**：`_shared`は完全一致キー、`pr_number`のint、`complete`のbool、空`errors`、固定MIME、前後headを確認。外部providerからの原応答がモデル・上流ログへ入らないことはこの関数で証明されない。`post_head_oid`は渡された値を信頼し、GitHubに再照会していない。
3. **metadata**：固定8 field、既知state値、exact repository/head/baseに一致し、本文fieldを拒否。R13の状態整合関係は未検証。`requested_fields`もローカルresponse自己申告であり、実GitHub GraphQL wire requestではない。
4. **paths**：全page検査後に一括JSON構築、cursor・item・page件数に上限あり、未知pathを遮断。R14のとおりexpected path→blob OIDのbindingがなく、許可pathに別内容のblobを紐付けても通る。Unicode/パス正規化は検証より前のtrusted exact canonical pathが前提。実Gitのsymlink、file mode、tree provenanceは未照合。
5. **document**：受信`body`はbytesのみ、サイズとsha256を確認し、raw bytesでなく固定`approved.safe_excerpt`を出す。照合するhashと抜粋が**同一承認審査から不可分に固定されたこと**は証明しない。R04/11で欠落が再現。抜粋のschema・長さも最後のJSON全体byte上限以外は限定しない。
6. **receipt/delivery**：`RELEASED` receiptを先に書き、`publish`後に内部setへ登録する。R01/R02/R03のとおり、排他・idempotent ACK・不明状態・durable 2相でない。`ReceiptSink`は自由に書換えられるmemory list。append失敗時のfail-closedは局所的には成立するが、独立auditの耐久性・書込み結果・実モデル到達を証明しない。R12の`policy_id`自由文も問題。
7. **error**：例外メッセージは`run`の返却に出ない（元22件内で確認）。ただし配送後の例外では既にsinkが受信している可能性があり、後から`BLOCKED`を記録しても取り消せない。実OS stderr、instrumentation、provider logの漏出をこのテストで証明できない。
8. **policy**：`Policy`はfrozen dataclassだが、内部mappingとsinksは可変。`policy_id`・`approved_excerpt`には独立承認者/秘密鍵/権限によるimmutable custodyがない。T20の「不審文書bodyから直接policyを変えられない」合成PASSとは別物。
9. **可用性/同一性**：`_released_operations`のキーはoperationのみのため、一回公開後に別の許可文書を`SAFE_DOCUMENT`で読む場合も一括拒否する。複数request/doc/operationを正確に識別したdelivery semanticsを設計する必要がある。再初期化のduplicateはR05で実測。
10. **host情報境界**：broker、model-input sink、auditは単一プロセス内。GitHub field selection、browser/alternate connector/shell/network/cache/preview/OCR/添付のhost deny、元raw隔離を実装しない。この候補に本番不曝露の実証を求めることはできない。

## 5. 段階別受入判定

| 判定対象 | 判定 | 根拠・残課題 |
| --- | --- | --- |
| Local deterministic T01–T22（元22個の固定caseに限る） | **PASS_SCOPED** | 独立で22/22を実行、exact bytes照合、compile成功 |
| Local adversarial safety conditions | **FAIL / NEEDS_REVISION** | 未使用14件で9件期待条件不成立。特にR01–R05が局所一貫性を破る |
| 実GitHub source-side field restriction | **NOT_VERIFIED** | wire query/固定schema/最小レスポンスの独立観測がない |
| Work host-level bypass prevention | **NOT_VERIFIED** | 全connector/browser/shell/cache/OS/network/multimodalへの強制なし |
| Approved excerpt independent review and custody | **NOT_VERIFIED** | 審査者・署名・権限・不可変承認/失効機構がない（R04/R11） |
| Durable independent audit and true model delivery | **NOT_VERIFIED** | in-memory list/sinkのみ。delivery ACK/外部証跡がない（R02/R03） |
| #106/#108 過去閲覧逸脱の最終処分 | **HUMAN_DISPOSITION_PENDING** | 原資料は再取得していない。合成試験から過去の影響を判断できない |
| Source qualification、正式cohort、CSM outcome gate | **NOT_APPLICABLE**（今回変更なし） | FXNS/CSM研究・市場結果の合否をこの試験で判定しない |

**総合**：`NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE`。仮にR01–R14を全部局所PASSにしても、実ホストの強制/保管/独立審査の証拠がなければ`SECURITY_ACCEPTED`にはならない。

## 6. 次Waveの操作単位の承認が必要な事項（本Dでは実行禁止）

1. **局所合成候補の修正**：#110から派生した**別の候補branch**で`safe_boundary.py`・`test_safe_boundary.py`と独立追加の合成testsを対象に、単一インスタンス排他だけでなく、リクエスト/文書/操作の識別子、曖昧な部分配送の停止・再試行禁止または下流idempotency、receiptの状態遷移、immutable policy、approved path＋blob pin、metadata整合、policy_id schemaを実装。合成負例R01–R14と元T01–T22を固定再現し、独立再監査。元PR #110への直接追記・mergeは本Dの許可外。
2. **実GitHub broker/field制限**：事前にprincipal、exact repo/PR/path/blob、GraphQL固定field、上流raw隔離、取得前後OID、ページ完了/取得制限、ネットワーク資格情報、監査者を指名して別承認。現在のWork connectorが同じ保証を提供するとは認定しない。
3. **実host権限/迂回遮断**：connector、browser、shell、OS/file/network/cache、preview/multimodal等の全経路を列挙し、実験用の専用隔離環境に対する拒否権限を事前に承認。hostが保証できない場合は`BOUNDARY_NOT_ENFORCEABLE / NO_FETCH`。
4. **文書承認・custody・durable receipt**：原資料を扱う別権限の審査者、safe excerptのexact hash/signature、期限/失効/権限、独立append-only監査とdelivered-ACK/unknown状態の扱い、監査責任者・秘密管理の別承認。モデルに同じ文書を先に読ませて安全判定をさせない。
5. **閲覧逸脱の最終人的処分**：#106と#108を別件として扱い、禁止資料を再表示せず利用影響と独立clean検証の要否を決定。#108の旧source順位は独立にclean認定していない。
6. **研究ゲートの別承認**：台帳実装、source再選定、CSM runner、本番/実データ取得、各研究gateは独立の承認事項。D合成監査に便乗して開放しない。

## 7. 維持するHOLDと保存境界

- FXNS：`SOURCE_QUALIFICATION_BLOCKED`、formal cohort `CLOSED`、`UNTESTED / PROPOSED_NOT_FROZEN`。
- CSM I2：`BLOCKED / CLOSED / market_outcome_access=false`、`HYP-CSM-002 UNTESTED`。
- #106/#108最終処分は`PENDING`。実見出し、GDELT live DOC、その他feed、実FX値、ECB OBS_VALUE、XM/MT5、market outcome、real snippet、raw logを取得しない。
- 本報告は指定D allowlist以下の**新規1ファイルだけ**。候補コード、元PR、研究branch、main、他PR、SOURCE_CONTRACT、SPEC、workflow、CI、gateは編集しない。[skip ci]はCI成功の証明ではない。
- 作業後のGitHub PR/branchのcommit、tree、Git blob、全文remote readback、変更path、共有HEAD非干渉は**作成後に別途確認**する。報告本文に未来のcommit hashを予め記入しない。
