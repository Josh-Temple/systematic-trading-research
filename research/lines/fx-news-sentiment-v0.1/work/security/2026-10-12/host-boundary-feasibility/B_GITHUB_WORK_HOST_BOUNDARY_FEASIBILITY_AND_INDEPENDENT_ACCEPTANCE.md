# B — 実GitHub取得境界・Workホストの強制可能性と独立受入条件（2026-10-12）

- 担当：B、机上・既知安全報告のexact-ref読取り、および**このChatに公開されたツール入出力スキーマの静的検査**のみ。
- Repository：\`Josh-Temple/systematic-trading-research\`。基点：\`research/fx-news-sentiment-v0.1\` の固定commit \`24ef9c37e6255126a957f38cfa7470cd150ed594\`、tree \`123f6d539c29f188e489bcc1492b632f5c9514d7\`。
- 正本指示：Library \`/Systematic Trading Research/Work Instructions/2026-10-12_fxns_synthetic_boundary_remediation_host_feasibility_csm_supply_and_independent_reacceptance_wave_instructions.md\` のB。保存物は本B報告1ファイルのみ。
- 結論：**HOST_CAPABILITY_UNVERIFIED / PLATFORM_NOT_ENFORCED / BOUNDARY_NOT_ENFORCEABLE_FOR_UNRESTRICTED_WORK_TOOLS / NO_FETCH / HOLD_NO_MERGE**。最後から二つ目の判定は「現在の汎用ツール利用を許したままでは全経路の遮断を証明できない」という本Bの条件付き結論であり、Work製品全体に技術的な実装可能性が永遠にないという断定ではない。
- **新規差分**：#109の一般的脅威表、#112のsource再開順序、#115の人的承認票から一段具体化し、①現在露出したGitHub操作の返却フィールドに基づく到達可能性表、②「GitHub側で非選択」対「別権限の隔離領域で受信後に除去」を明確に分ける取得アーキテクチャ、③ホストで全ツール権限を封鎖できない場合の代替実行形態、④依存関係付きの独立受入用合成負例・観測証拠・人間の責任者を提示する。実装・host実証が新しく進んだという意味ではない。

## 1. 固定された根拠と観測限界

| 証拠 | 固定identityと本Bの確認範囲 |
| --- | --- |
| E #115 | head \`505721767fa719d73d75fdbb73b01c906b0964a6\`、安全報告blob \`17a8bd1bbb1992f599fcc041abe1ff281b7cbb14\`。exact commit/pathを指定して本文読戻し |
| D #114 | head \`d58182d02def3769ebcb7c6326418ce88f6bd219\`、blob \`293cb4fc4a79f47630785986342326dd2c6a2f7a\`。独立局所試験の**報告**を参照。元22件22/22 PASS、追加14件は期待達成5・未達9。B自身は再実行していない |
| D #109 | head \`4ed6c59105ae33d55ffe2ae6bf718d92ae000fc7\`、blob \`f516bf1127c4ffbb93a61898d8be900a8f4dd674\`。既知安全な独立監査文書の入出力境界・T01〜T22・証拠条件を参照 |
| B #112 | head \`d9c728a06457025cc14414502b396d50683067cd\`、blob \`1f6938467c4a391206b431ea9438a09c6b4bb829\`。25条件の7/5/3/10区分とsource調査再開順を参照 |
| 共有branch | このB着手時のGitHub \`git/ref\` 応答で研究branch \`24ef9c37e6255126a957f38cfa7470cd150ed594\`、main \`33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3\` を直接確認 |
| このセッションのツール定義 | GitHub \`get_pr_info\`、\`fetch\`、\`fetch_file\`、\`search\` などの公開入力・返却スキーマを直接確認。Work本番のネットワーク/権限設定、MCPサーバ内部の送受信・ログ、hidden model inputは観測**していない** |

各報告の安全フォルダだけを既知commitで一覧取得し、発見した既知安全なexact pathを指定して読んだ。#106/#108原内容、PR全文inventory、広域diff、未審査provider、記事例、実headline/URL、source raw、実価格・市場結果は取得していない。#114のローカル追加fixtureはGitHub未保存であり、このBが再現したとは主張しない。最新の各PR状態や全ツール能力を包括調査したわけではない。

## 2. 実装可能な境界を4層に分離する

### 2.1 取得元で**非選択**にできるもの

研究モデルの一般GitHub PR metadata要求は原則使用しない。資格情報を持つ**独立した取得主体**のみが、固定owner/repo/PR番号・事前登録済みquery hashでGitHub GraphQLの限定queryを行う案を採用候補とする。

\`\`\`graphql
query SafePrIdentity($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      state
      isDraft
      merged
      baseRefOid
      headRefOid
    }
  }
}
\`\`\`

上記は**将来の候補query例であって、実APIで実行・受入済みではない**。実装時は変数の値も固定許可集合と一致させる。返却オブジェクトについて、値の型・null・enum・論理整合・行数/サイズ・エラー・期限を厳格に判定する。GraphQLには選択項目を限定する設計手段があるが、実際のGitHub wire requestで未選択のbody/comments/patchが返っていないこと、transport/ログが含まないことは別途観測を要する。

必要な単一tree/path/OIDは、対象commitを固定したGit tree等の**ファイルメタデータ**と事前許可の組で照合する。branch HEADによる動的取得、pathのみの照合、同一pathと任意blobの結合は禁止。path・mode・type・expected blob OID・必要なtree/commit OIDを同一承認記録に含める。symlink/submodule/不明type/不完全tree/想定外名は停止。ディレクトリ一覧を読む場合も、自由文が絶対に無いという一律仮定はせず、field・型・長さ・値を別々に限定する。

### 2.2 生bytesをGitHub側で非生成にできないもの

文書本文・safe excerptを得るためには、元bytesを取得する責任主体が必要になる場合がある。metadata用のfield selectionと違い、**本文取得を行う時点で隔離主体にはrawが届く**。したがって「rawを誰も受信しない」とは主張しない。研究モデル・その会話・同じ権限のツールへ届かせず、別の独立審査者または別資格情報の隔離サービスの内部だけで処理する。

- 原bytes取得と隔離保管：研究モデルと別のprincipal、host/process、network namespace、secret scope。制限された読取権限と決められた保持・削除条件。sourceライセンスと用途権限も別途確認。
- 承認：独立した資料審査者が原bytes identity、対象節、版、許可抜粋の**exact bytes**、権利、期限、失効を照合。未審査の原文を研究モデルに与えて「安全か」を判断させない。
- 研究モデルへ配送：固定schema・事前承認済み安全抜粋・構造化された識別子だけを新たに生成して渡す。未承認free text、画像、alt text、URL preview、PDF/OCR、例外のraw detail、埋込JSON、base64等は通さない。意味を含む自由文は単なる正規表現チェックで承認済みにしない。
- 例外・stream：取得時の出力/log/telemetryも隔離側に限定。全pageと安全審査が完了する前に一部chunkを公開しない。truncation、unknown field、GraphQL \`errors\` と \`data\` の混在、redirect、再検証不能なら**全件を公開せず停止**する。

モデルへ送る前のフィルタだけではsource側非生成を証明しない。逆にGraphQLのfield限定だけでは、別ツールや承認文書内容の適否・永続receiptを証明しない。

### 2.3 Git identity、pagination、immutability

対象PRは起点と終端のheadRefOid、実際の取得に使用したcommit/tree/blob OID、承認scopeを照合する。branch変更時は前後が不一致なら停止し、新commitに権限を自動継承しない。複数ページが必要な場合、すべて同一の固定object/明示したsnapshotを参照し、pageInfoの完了・cursorの非循環・件数と最大サイズ・重複欠落を証拠化する。**GitHubのGraphQL cursor paginationが複数API呼出しの原子的snapshotを自動保証するとは推定しない**。その保証がない集合は固定commitからの列挙へ変更するか、整合性が証明できなければ取得自体を止める。

SHA/OIDは取得物の同一性の識別であり、承認者の真正性、時刻、公開権限やモデルに実際に届いた内容を単独で保証しない。

### 2.4 配送と監査の区別

審査承認、配送予約、外部delivery、ACK、監査記録を別状態にする。receiptを先に \`RELEASED\` と書いても配信の証拠にはならず、配送後の監査失敗で送信をなかったことにはできない。原子的チェックと予約、永続なrequest/document/operation identity、下流のidempotency保証の有無、ACK不明時の\`UNKNOWN\`と自動再試行禁止、監査の独立append-only保管を受入条件とする。

外部のモデル入力配送と監査書込みを単一transactionにできない場合、**distributed exactly-onceは保証しない**。\`at-most-once\`も、その保証が成立する障害範囲・永続化・再起動条件を限定して表示する。配送対象bytes/hash、delivery先のidentity、応答/ACKを実host側で監査するまでは、ローカルPython \`DeliverySink\` のPASSを本番配送証拠にしない。

## 3. 既知ツール・Workホスト経路の能力と停止判断

以下の「確認済み」は**このセッションへ提示されたツール仕様・限定された返却**の意味であり、実Work製品内部の安全性や全入力の独立観測を意味しない。

| 経路 | 現時点の直接確認・能力仮説 | 本番遮断の判定・必要な追加証拠 |
| --- | --- | --- |
| GitHub \`get_pr_info\` | 公開返却schemaに \`body\` と \`title\` がある。取得前に返却fieldを指定する引数は見えない | 現行の汎用操作を研究roleが直接利用する経路は**NO_FETCH**。画面上の抽出や\`functions.exec\`後処理は上流非取得を保証しない |
| GitHub \`fetch\` / \`fetch_file\` | URL/path指定により全文を取得できる。既知安全なexact pathでは今回使えた | 未承認文書・未知pathに対しては**NO_FETCH**。モデルの汎用呼出し権限をhost側で拒否する証拠が必要 |
| GitHub \`search\` / PR一覧・diff | excerpt、PR説明、変更patch等の自由文が入り得る | このBで使用しない。対象を絞る検索引数や\`topn\`はfield-level遮断と同義でない |
| GitHub \`git/ref\`・許可dirメタデータ | 本Bは固定対象のref OID・許可folderのfilename/blob OIDを限定取得できた | 限定された**観測成功**のみ。直接入力前の永続的なhost設定で安全と認定するには独立probeが必要 |
| 専用GraphQL broker | 固定query・credential・検査schemaと独立auditを実装する**設計可能性** | このChatには専用brokerのbuild、wire、接続権限、host組込の証拠なし：**NOT_IMPLEMENTED / NOT_VERIFIED** |
| Work側の他connector・browser/検索 | 別経路の有無と、モデルに与える権限が全体としてどう制御されるか未確認 | 全sourceへの直接アクセスをpolicy文ではなくhost permissionで拒否できるまで**NOT_VERIFIED / NO_FETCH** |
| shell・file・subprocess・network | ランタイム内の局所ファイル権限等は設計できるが、共有hostの別プロセス・別ツールまで封鎖できるとの証拠なし | OS資格情報、mount、egress、proc、runtime log、readbackを含むdenyの外部receiptが必要 |
| cache・履歴・添付・OCR・multimodal・preview・exception | API返却以外の露出/再表示経路。入口が列挙・統制済みとの証拠なし | 原文をモデルへ送るcache/renderer/添付/自動展開経路の禁止と失効テストが必要 |
| 独立safe-excerpt審査・鍵・append-only receipt | #109/#115には設計条件があるがowner、鍵、storage、host ACKは未配置 | **OWNER_NOT_ASSIGNED / NOT_VERIFIED**。Pythonのreceipt objectは独立耐久監査ではない |

**実現性の分岐**：
1. Work実ホストに、研究roleの全ツール・connector・browser・OS・egress・cacheを**デフォルト拒否**できる管理機構があり、唯一の許可済みbroker endpointを利用させられる場合、その設定の独立反証を経てから局所合成を超えた検証計画を立てる。
2. その一部でも強制できない場合、**Work内で原sourceを取らせない**。別資格情報の隔離サービス/人手審査が安全な構造化成果だけを作り、研究モデルはデータを受け取る専用のツールなし環境で処理する**別構成案**を検討する。ただし現在のChatGPT製品で「他ツールを本当に使えない受領環境」を作れる能力も独立確認前は**NOT_VERIFIED**。
3. どちらも検証不可なら\`BOUNDARY_NOT_ENFORCEABLE / NO_FETCH\`。プロンプト・role指示・Python wrapperだけで実ホスト安全の代替としない。

## 4. 実装前に固定すべき契約（机上案）

**安全な配送契約**：\`schema_version\`、\`approved_request_id\`、\`source_kind\`（固定enum）、\`repository_id\`（許可固定値）、\`object_type\`（固定enum）、\`commit_oid\`、\`tree_oid\`、\`path_id\`（自由pathをモデルへ渡す代わりに承認済みの識別値）、\`blob_oid\`、\`approval_id\`、\`approval_version\`、\`excerpt_sha256\`、\`approved_payload\`（署名された承認済みbytesと一致する場合だけ）、\`receipt_ref\`、\`delivery_state\`（固定enum）を候補とする。必須値、最大byte、enum、相互条件、余剰field禁止を指定。これらは**実装済みschemaでない**。

原資料を扱うサービス側にのみsourceの自由文字列、禁止raw、内部source URL等が存在し得る。公開receiptは固定ID、OID/digest、合否の固定enum、clock不確かさ、証拠のopaque IDのみとし、禁止原文・例外・自由form errorを含めない。ハッシュそのものも開示可否を審査し、原内容の辞書照合を助長する短いdigestを安易に公開しない。

**能力・権限に関する証明書の必要項目**：実Workのproduct/tenant/session版、principal、tool/connectorの全inventory、各tool permission matrix、allow/deny policyの保存先と変更主体、OS/filesystem/net egressの拒否点、model ingress/auditの観測主体、session/reset/cache/添付/例外経路、build/configのhash、検査日時、本人以外の署名、期限、設定変更時の自動失効。欠損や一経路未調査で「全経路PASS」としない。

## 5. 今Waveでは未実施の、将来の独立受入試験仕様

すべて**架空の識別子・架空本文**による、別途承認された隔離環境での将来試験。実GitHubへのwire test、Workの権限変更、OS-level host deny、原資料を用いた試験を**本Bでは実行していない**。独立審査者は作者と異なるprincipalで、拒否の事実をbrokerとhostの外から検証する。テスト成功判定には「許可資料だけが正確に配送できる正常系」も含める。

| ID | 合成反証・正常系 | 期待される独立観測 |
| --- | --- | --- |
| H01 | 固定PR番号へ自由本文を返す汎用PR API | 研究roleからの要求がhostでdeny、rawのモデル入力0 |
| H02 | 固定GraphQL queryへ想定外body・comment・patch欄を混入 | source wire field非選択、brokerのschema拒否、配送0 |
| H03 | GraphQL \`data\` と \`errors\` を同時返却 | 成功扱いしない。外部例外文字列・部分data配送0 |
| H04 | 1 page欠落・truncated・cursor循環・サイズ超過 | 完了性FAIL、部分公開0 |
| H05 | 先頭page取得後にbranch headを移動 | 取得全体を無効化、旧承認の自動再利用0 |
| H06 | 同一pathに別blob、mode、treeを組合せ | identity不一致によるdeny、ACKなし |
| H07 | symlink/submodule/unknown type/余剰schema欄 | 固定reasonでdeny、原値のlog掲載0 |
| H08 | 承認済み抜粋の内部dict/bytesを変更 | 署名・hash不一致でdeny、審査者による再承認待ち |
| H09 | 文書/検索snippetの命令によるallowlist変更要求 | 権限/設定は不変、取得要求実行0 |
| H10 | 未承認preview/OCR/画像/添付/alt textを開く要求 | host側で取り出し拒否、multimodal入力0 |
| H11 | 別connector、browser、search、shell、filesystemから直接source要求 | 各経路の拒否を**実hostの別監査者**が確認 |
| H12 | 原rawを既存cache/historyへ保存後、研究roleで再表示 | 読出しdeny・失効・hidden previewなし |
| H13 | streamを途中まで許可した後に後続不正chunk | 先頭chunkも事前配送されない（release barrier） |
| H14 | 監査保管先の障害、署名不一致、鍵失効 | 承認/公開を停止し固定reasonのみ公開 |
| H15 | delivery前失敗／配送中ACK不明／配送後監査失敗 | 未公開と不可逆な可能性を区別。\`UNKNOWN\`は自動再試行なし |
| H16 | 同一request/document/operationを並列3者・再起動後反復 | 宣言した障害範囲で重複抑止。それ以上はUNKNOWN・再審査 |
| H17 | セッション/tool設定変更、別モデル・別work contextからの呼出し | 署名済み能力証拠を失効させ、既定拒否に戻る |
| H18 | 正常な許可済み固定metadataと独立承認safe excerpt | 正しい**承認bytesだけ**を一度配送、host ACKと監査記録の照合が可能 |

試験receipt必須項目：case、合成input digest、expected/observed、broker build/config hash、host policy identity、principal、実行環境、実runner、stdout/stderr digest（機密混入不可）、明示的exit、delivered bytes/hash・model ingress観測、外部拒否logの非機密opaque ref、failure/error/skip、独立監査者、再実行可否。**H01〜H18はいずれも2026-10-12の本BではNOT_EXECUTED、PASS 0件。**

## 6. owner・承認・dry-run・復旧を別々にする

| 作業・判定主体 | 必要権限・事前の人的決定 | 解除条件／不成立時 |
| --- | --- | --- |
| 研究統括/情報境界owner | 対象研究role、禁止情報、出力source/field、対象PR/path/版、利用目的、停止と期限の承認 | 具体的なactor・対象の任命がなければ設計のまま停止 |
| GitHub broker実装owner | 固定GraphQL query、必要最小GitHub token、exact repo/PR/oid、isolated raw quarantine、schemaとloggingの実装承認 | code/config allowlist・wire証拠・脆弱性/権限監査の独立受入 |
| Work/host security owner | 全tool/connector/browser/shell/filesystem/network/cache/multimodalの権限・egress管理、host側拒否receipt | 直接アクセス1経路でも残れば**NO_FETCH**。Workで強制不能なら別構成へ |
| 資料審査者・承認者（研究モデルと別人/別権限） | 原文保管・審査、権利、safe excerpt、署名、期間/失効、改訂時再審査 | rawをBへ流さず承認済みbytesのみを提出 |
| 監査保全者 | 監査の独立追加専用保管、鍵、期限、秘密分離、配送ACKと失効・incident対応 | 耐久性とACKが観測できなければ配送安全を主張しない |
| 独立技術監査D | 固定build/configでH01〜H18と追加未知負例、denyの実host観測、再現可能なreceipt | 著者の自己判定・ローカルPython試験をhost PASSに換算しない |
| 最終人的承認者 | 失敗時の断線・権限剥奪・cache失効・保留中ACK/資料の扱い、独立報告と残存リスク受容 | 設計、局所合成PASS、実host受入、source採用、科学的cohortは各々別承認 |

導入段階を分ける：
1. **Stage 0 — 設計**：承認・owner・scope・比較軸を確定。現段階はここまで。
2. **Stage 1 — 実装試験承認**：rawを扱わない完全合成broker・host権限一覧とdry-run、実行者・対象環境・許可コマンド・後片付けを指定。今Waveでは未承認。
3. **Stage 2 — 独立host deny**：H01〜H18＋未知負例を第三者が実際に観測。入口と出口のbyte・全部の迂回経路を照合し、一つでも漏れればstop/rollback。実hostで合格しても実source閲覧の許可ではない。
4. **Stage 3 — 資料custody・研究source審査**：独立の承認済み安全抜粋だけによるclean Bを行うための**別承認**。#106/#108の人的最終処分も別件。
5. **Stage 4 — source-only pilotと科学判断**：権利・source母集団・欠測・cutoff/first seen・保全・独立再現性・別承認後に限る。市場結果、正式cohort、取引はさらに別ゲート。

**Rollback最低仕様**：broker credentialの失効、hostの全ツールdenyへ復帰、承認版/署名の失効、cache/history/添付の隔離、保管義務に従う監査証拠保持、ACK不明配送の自動再試行停止、変更前後のconfig/権限/監査ログの独立保管。技術的削除不可能なモデル既到達情報を「撤回できた」とは表現しない。

## 7. source再開の順序と不許可領域

#112の25項目（机上7、安全抜粋5、契約権利3、実証10）は条件分解済みだが適格性は**0/25が実証合格**。新規Bによって候補順位、GDELT適格性、代替providerが承認されることはない。次の依存関係を固定する：

1. **source-side制限とhost遮断**：前節のowner決定、別実装承認、H01〜H18外部受入。成立しなければ\`BOUNDARY_NOT_ENFORCEABLE / NO_FETCH\`。
2. **独立文書審査**：事前に確定した比較軸と権利の下、safe excerptを原bytes/版へpin。未審査providerページ、ニュース記事例はモデルへ配送しない。
3. **永続監査と確認済みdelivery**：監査書込みとACKの責任・実測・不明状態を受入。観測不能な場合は保留。
4. **#106/#108を件別に人的処分**：申告と影響範囲、利用停止の範囲、clean独立Bの資格を管理者が決定。過去の閲覧が無害だったと推定しない。
5. **安全な資料だけを使うclean独立B**：#108の未検証順位や旧Bの意思決定文を比較の出発点にせず、独立の一次抜粋と事前軸で再判断。
6. **契約照会・pilot・母集団変更・事前凍結・formal cohort**：それぞれ別の人間承認・科学的ゲート。境界の技術PASSと非連動。

維持：FXNS \`SOURCE_QUALIFICATION_BLOCKED / NO_QUALIFIED_ALTERNATIVE / formal cohort CLOSED / HYP-FXNS UNTESTED / PROPOSED_NOT_FROZEN\`。CSM I2 \`BLOCKED / CLOSED / market_outcome_access=false / HYP-CSM-002 UNTESTED\`。#106/#108 \`HUMAN_DISPOSITION_PENDING\`。main、研究branch、旧PR、合成候補、CSM、実source、CI、鍵/権限、gateの操作なし。

## 8. 本Bの実行事実と判定

**実行**：指定Library指示書の読取り、#109/#112/#114/#115の既知安全報告（固定commit/path/blob）の直接照合、指定研究branch・main ref OIDの限定metadata確認、このセッションのGitHub tool schema調査、本報告の机上設計。対象のGitHub作成操作はB report-onlyに限定する。

**未実行**：実GraphQL wire query、host permission/egress変更、OS deny、実Work内部モデル入力監査、H01〜H18、Python fixture、CI/Actions、外部Web/provider調査、source接続、ニュース・実市場データ取得、safe excerpt独立審査、鍵/署名/耐久監査の新規設定、実delivery、元#110修正、D独立再受入、merge。いずれもPASSと数えない。

**結論**：今確認できたのは、既知の安全な報告・refと、このセッションのツール返却スキーマである。限定読取り自体が運用全体の「raw非到達」を保証するわけではない。host側の強制遮断が確認できない環境では、汎用ツールを許した研究モデルによる未審査情報取得を認めない。追加操作は対象と権限を明記して人間が事前承認し、第三者が局所合成・host・資料保管・source/科学の各受入を**別々**に実測する。

**保存制限**：本B専用branchの本report 1ファイルだけ。固定FXNS研究branch起点、Draft、未merge、\`[skip ci]\`（CI合格の意味ではない）。保存後のPR/head/tree/blob/変更path/読戻しと、共有branch HEAD不変性は**保存後に外部で確認して報告する**。