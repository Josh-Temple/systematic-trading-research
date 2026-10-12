# E — 2026-10-12 FXNS/CSM Wave統合判定と個別人的承認票

- 統合対象：A #111、B #112、C #113、D #114。監査対象 #110。既存人的承認 #107、旧CSM E #104。
- Repository：Josh-Temple/systematic-trading-research。
- 判定：**E_INTEGRATION_COMPLETE / PR110_NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE**。
- 重要：本EはA〜Dの保存済み安全報告、既知のPR/commit metadata、変更ファイル一覧、既知のCSM gateだけを検証する**文書統合**。Dのローカル試験をEが再実行したわけではない。実News/FX/市場値/ECB観測値/元raw/禁止ログを取得・分析していない。新規コード、CI、workflow、契約、source、権限、gate、mergeは変更していない。

## 1. 最優先結論と証拠区分

**PR #110 は独立受入不合格。** D #114（head d58182d02def3769ebcb7c6326418ce88f6bd219）が、被監査 #110 の固定head 0faf05b453c5d7897c3566d871591b2926ba928e の安全な4ファイルをpinして行った独立試験の記録を、Eは文書とGit object identityで照合した。

- Dの**記録上の実測**：Python 3.13.5、ローカルoffline、既存T01〜T22は22/22 PASS、py_compile exit 0。独立追加14例は5期待条件達成、9期待条件不達（unittest exit 1、failures 9、errors/skips 0）。D report内にcommands、exit、stderr SHA-256、各R01〜R14の観測がある。**この36件を36/36 PASSと解釈しない**。Dの保存済みtest code自体はGitHubにはないため、本Eは実行receiptと報告の整合確認であり独立実行の再現ではない。
- **局所実装の重大な問題**：R01 同時呼出しで二重公開、R02 部分delivery後の再試行で二重公開、R03 未配送なのにRELEASED監査、R04 frozen policy内部dictの変更で未承認抜粋を公開、R05 Boundary再初期化で重複公開。request identity、atomicity、配信ACK/UNKNOWN、承認固定性の具体的な修正・負例受入が必要。
- **追加の期待条件が不成立**：R11 外部safe excerpt事前審査なし、R12 policy_id未検証自由文のreceipt混入、R13 metadata stateの意味的矛盾を許可、R14 allowlisted pathに任意blob OIDを組合せ可能。R11は候補READMEが明示した「外部承認前提」の欠如でもあり、9件すべてを同種類の新規コード欠陥と数えない。
- **限定的に成功**：R06〜R10は完全架空入力に対する局所遮断を確認。元22試験の合格もin-process Python surrogateに限定する。
- **独立受入判定**：LOCAL_ORIGINAL_TESTS=PASS_SCOPED、LOCAL_ADVERSARIAL=FAIL、SOURCE_SIDE_FIELD_RESTRICTION=NOT_VERIFIED、HOST_BYPASS_PREVENTION=NOT_VERIFIED、APPROVED_EXCERPT_CUSTODY=NOT_VERIFIED、DURABLE_AUDIT_AND_MODEL_DELIVERY=NOT_VERIFIED。したがって **NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE**。候補を実Workモデル入力前安全境界と認証してはならない。

## 2. A〜Dの終端報告の同一性と変更境界

開始時・統合時のFXNS研究branch / #63 headは 24ef9c37e6255126a957f38cfa7470cd150ed594（tree 123f6d539c29f188e489bcc1492b632f5c9514d7）。mainは 33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3（tree be858570de929678a219660cb8f0b3d26b038516）。CSM #90 headは 94e7719839dcacf281d7d479c597222582f0d920。A/B/C/Dの報告は各1ファイル追加、既存共有branchと既存候補ファイルの変更なし。各PRは OPEN/Draft/未merge。各報告ファイルをhead指定で直接取得し、Git blobと変更一覧を確認した。compareは全て当該baseに対してahead=1 / behind=0 / 追加1ファイル、削除0。

| 担当・PR | exact head / Git tree | report Git blob / 対象概要 | 実行・最終判定 |
| --- | --- | --- | --- |
| A #111 | eb7cb765665e9acfbf7591e6374fbc156fafbd18 / 4d021afe7328877443c176e3de01a02b365bde64 | 83653c7e276db7858f69a4f47a9d54184b7256f5 / FXNS案①受入設計 | T01–T16は設計のみ、tests 0、CI未実行。DESIGN_READY / IMPLEMENTATION_UNAPPROVED / MIGRATION_UNAPPROVED |
| B #112 | d9c728a06457025cc14414502b396d50683067cd / d3a2da31feb8f3209ca6928087870f6a599026e1 | 1f6938467c4a391206b431ea9438a09c6b4bb829 / source再開判断条件 | 25条件を机上7、安全抜粋5、契約権利3、別承認を要する実証10に分類。実source検査0。NO_QUALIFIED_ALTERNATIVE / SOURCE_QUALIFICATION_BLOCKED |
| C #113 | bf798a77c5b9bf937bf118d29d792632fb8f7c4e / 55f9056c103c2d5f13bc970b6c916a75046f6233 | 13ccd2ee510f6fc6f5ec35f71417cb9b072d1427 / CSM環境供給設計 | baseは#90 head。完全checkoutなし、runnerなし、metadata実runtime hashなし、suite実行0。OWNER_NOT_ASSIGNED / BLOCKED_ENVIRONMENT / NOT_EXECUTED |
| D #114 | d58182d02def3769ebcb7c6326418ce88f6bd219 / 3d28845d5e32cee733d7ca4fccc5000d91eab11b | 293cb4fc4a79f47630785986342326dd2c6a2f7a / #110独立監査 | 元22件PASS、追加14件中9件期待不達。NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE |

報告変更対象の許可パス：
- A: research/lines/fx-news-sentiment-v0.1/work/assurance/2026-10-12/option1-ledger-preimplementation-acceptance/A_FXNS_OPTION1_PREIMPLEMENTATION_ACCEPTANCE.md
- B: research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-12/safe-source-decision-gates/B_FXNS_SAFE_SOURCE_DECISION_AND_RESTART_GATES.md
- C: research/lines/currency-strength-momentum-v0.1/work/implementation/2026-10-12/exact-checkout-isolated-runtime-supply/C_CSM_ISOLATED_RUNTIME_SUPPLY_PLAN.md
- D: research/lines/fx-news-sentiment-v0.1/work/security/2026-10-12/independent-pre-model-boundary-acceptance/D_PR110_INDEPENDENT_TECHNICAL_SECURITY_ACCEPTANCE.md

これらのcommitは各々固定baseの単一parentを持つことをGit metadataで照合した。ただしA〜Dの過去の試験環境そのものをEが再構築したものではない。[skip ci]はCI PASSの証拠ではない。

## 3. 前回の承認と停止条件

- 人的承認の記録 #107 head 495fd3e9167d11d2787a4667995ee0a7cbf6c201、報告blob 73100d97bf94c82c0b8fb9a18c0e7e2647579997 の「6. 承認追補」を直接確認。承認済みは二形式のFXNS台帳**案①**（同一ID競合・不明時fail-closed）、真正性対策の設計、固定DOC正式適格化停止とpre-freeze再設計、閲覧逸脱の非侵襲調査、CSM供給経路**設計**であり、実装・移行・実データ閲覧・権限・実環境・merge・cohort開放ではない。
- #110 は別途承認された独立の完全合成プロトタイプ。D #114の反証により受入待機状態から**NEEDS_REVISION**に更新する。既存 #110 コード/branch はこのEで変更しない。
- B #112は研究母集団を「広いworld FX news」「licensed providerの配信集合」「受信保全集合」「中央銀行発表」に区別。異なる母集団への変更を単なるデータ入手先の差替えと扱わない。#108の候補順位や科学的な推奨は独立clean検証済みではない。
- A #111のevent ledger正常/blocked形式、競合停止、reader/writer線形化、crash、真正性/鍵、仮想inventory・移行は**設計受入仕様まで**。現在のコードで全consumerがatomic ID単位判定できるとの実証ではない。
- C #113は #90 exact checkout / Python >=3.12 offline隔離 / #35 metadata 3ファイルの**実runtimeでの** SHA-256照合 / 責任分離 / durable receipt / 新Cの後の独立Dまでを供給計画として明確化したが、担当者も環境も供給されていない。旧E #104はHOLDのまま。
- CSM I2 の既知正本 research/lines/currency-strength-momentum-v0.1/work/integration/gate.json を integration branch work/csm-integration-20261001 から**このEで直接read**。branch head 9162cae4f2e64ee3da07517f12a16092cc170161、tree 1bd6b67af2c5b59ae5e0c8f8c1f7b712dd72b585、gate blob 19442215345b35b0db3910c01acd910a5d57889b、state=BLOCKED / gate_status=CLOSED / market_outcome_access=false を確認。変更禁止。
- #106/#108の逸脱最終処分は件別に HUMAN_DISPOSITION_PENDING。禁止資料を再取得せず認知的無影響を証明したと扱わない。

**維持する正式状態**：FXNS SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED / HYP-FXNS UNTESTED / PROPOSED_NOT_FROZEN / NO_QUALIFIED_ALTERNATIVE。CSM I2 BLOCKED / CLOSED / market_outcome_access=false / HYP-CSM-002 UNTESTED。全候補 HOLD_NO_MERGE。市場・outcome・取引システムの許可は一切生じない。

## 4. 人間に求める承認票（操作ごとに別申請、今回承認は行われていない）

### 優先1 — #110の局所合成不合格の修正と再受入
- **申請対象**：固定 #110 0faf05b453c5d7897c3566d871591b2926ba928e から別の隔離candidate branchを起こし、当該 synthetic-pre-model-gate の safe_boundary.py / test_safe_boundary.py と、新規の完全架空の adversarial test/receipt に限定して改修する。
- **必須不変条件**：R01–R05の重複・部分配送・ACK不明・RELEASED誤監査・mutable approvalをfail-closed化。R11の外部審査前提は実コードの仮想approval interfaceと現実の人的審査を分ける。R12–R14のschema/状態整合/path＋OIDをpin。request/doc/operation id、reset/retry/concurrent処理、受信確認と監査永続性が局所版に実装済みなのか明示する。
- **受入**：旧T01–T22、D新R01–R14、独立の追加未使用負例、固定Git SHA・bytehash、実行exit/stderrと故障注入receipt、作者と別の新D。欠落、再現不一致、モデル/実sourceへ接続を始めた場合は停止。**PR #110への直接上書き・merge・実Work配備はこの承認に含めない**。
- **現状態**：具体的な人間の新承認・実装者指名待ち（UNAPPROVED）。

### 優先2 — 実GitHub取得brokerとWork host強制（局所合成とは別）
- **申請対象**：実現可能性評価から分け、実装する場合はexact principal/repo/PR/path/blob、固定GraphQL response field selection、上流raw非到達、permitted metadata、cursor/HEAD、全connector/browser/shell/cache/preview/file/OS/network/multimodal迂回のホスト拒否を設計・許可。候補コードと環境権限を限定。
- **受入**：研究モデルへの入力**前**に拒否した外部観測証拠、negative bypass probes、権限/credential分離、fail-closedの停止と復旧。一般的なGitHub read権限やin-process Python遮断は代用不可。host側で強制不可能なら **BOUNDARY_NOT_ENFORCEABLE / NO_FETCH**。
- **現状態**：実host保証の責任者・能力・権限未確認。**実資料取得の承認を含まない**。

### 優先3 — safe excerpt独立審査、鍵・保全、監査receipt
- **申請対象**：原資料を研究モデルとは異なる権限で扱う文書審査者と承認者を指名。許可文書の版・excerpt・digest・署名・期限/失効を不可分にpinし、独立の改変耐性監査、delivered/unknown ACK、保管先、鍵とACL、証拠の破棄/保存規則を設計・受入。
- **受入**：原資料と承認safe excerptを混同しない独立レビュー、変更時の再承認、監査障害時の公開禁止・再試行時の不明状態。暗号鍵やログ保管先を無断作成しない。
- **現状態**：OWNER_NOT_ASSIGNED / NOT_VERIFIED。

### 優先4 — #106と#108の逸脱を各々処分し、clean B再検証の独立性を定義
- **申請対象**：管理者が実禁止内容をモデルへ再提示せずに、閲覧事象・影響した下流成果・利用停止範囲・記録保全・最終処分をそれぞれ個別裁定。#108のprovider順位はclean独立Bの事前比較軸へ入力しない。
- **受入**：別件ごとの処分票、証拠参照と残る不可知、独立担当指名、将来の安全抜粋を使った比較条件。
- **現状態**：HUMAN_DISPOSITION_PENDING / NO_FETCH。

### 優先5 — FXNS案①の実装と旧競合の移行は分ける
- **申請5a（新規コード）**：#111受入仕様T01–T16に従うevent_ledger.pyと全reader/consumer、決定済み許可helperと完全合成testsを対象に、二形式のID単位検証、排他/linearization、crash/restart/dir-fsync、event ID↔basename、監査失敗、署名/custody責任を別々に実装提案・独立受入。
- **申請5b（旧記録）**：5a成功後に限り、内容遮断されたread-only inventoryと隔離裁定、対象ID/paths、before/after hash/count、rollback、cutoverを**別承認**。既存競合を勝手に選択・削除・移行しない。
- **現状態**：OPTION_1_DESIGN_APPROVED / IMPLEMENTATION_UNAPPROVED / MIGRATION_UNAPPROVED。

### 優先6 — source調査・契約・実証・科学変更を各々別申請
- **申請6a**：情報境界の独立受入後、独立のsafe excerpt作成と#108を参照しないclean source仕様比較を許可するか判断。
- **申請6b**：有料provider等への権利/契約/価格の**照会のみ**について送信者・宛先・質問・返答審査経路を特定する。照会の承認は購入・API使用の承認ではない。
- **申請6c**：情報境界・権利・母集団が確認できた後、固定条件のsource-only pilotを別申請。欠番oracle、時点、coverage、revision、cutoff、保全、障害停止、実取得を対象単位で承認。
- **申請6d**：母集団変更による仮説/SPEC/source契約/再freeze、formal cohortの開始判断は各々別の独立科学的承認。
- **現状態**：NO_QUALIFIED_ALTERNATIVE / SOURCE_QUALIFICATION_BLOCKED / pilot未実施。

### 優先7 — CSMの実checkout、隔離runner、元suite実行を分ける
- **申請7a**：#90 exact commit/treeの完全authentic checkout（または真正な完全Git bundle）を管理者がstagingで供給し、実run identityから不要な.git/history/raw/credentialをOS権限で遮断。#35の3 metadataを別custodianから渡す。各担当者/アクセス権/期限を実名または認証済service accountで指名。
- **申請7b**：オフラインPython >=3.12のread-only runnerとnetwork/file/process拒否負例、protected append-only receipt、runtime-local 3 SHA-256を**実物byte**から証明する。正当な完全checkoutと禁止ファイル非露出が両立しない場合はSTOP。
- **申請7c**：7a/7bの独立受入後に限り、変更していない#90のpy_compile/unittestを指定環境で一回実行し、実件数/exit/logを保存し**実行者と異なるD**が独立後監査。#102/#104や今回#113を未来の実行証拠に読み替えない。
- **現状態**：OWNER_NOT_ASSIGNED / BLOCKED_ENVIRONMENT / NOT_EXECUTED。CSM gate開放・market outcome・broker・取引は承認範囲外。

## 5. 優先順、停止、次のWaveへの条件

1. **最優先は#110局所不合格の修正と独立再監査**。同時に、実host broker/権限制御の実現可能性を別責任者で調べる。局所修正が完成してもhost保証がなければ実資料はNO_FETCH。
2. A（台帳）とC（CSM）は研究・市場・実runtime実行を伴わない限り独立の準備を進められるが、既存承認は**設計まで**。コード化や環境供給は上記5a/7a/7b/7cの個別承認が前提。
3. B（source）の実問い合わせ・safe excerpt・pilotは現時点では止める。#106/#108の扱いと上流での実安全境界を先に決め、仮説の母集団変更を独立判断に上げる。
4. 人間が明示した**操作単位の承認がない限り**新しい実装Waveを実行しない。承認は別研究line・既存PR・権限・CI・source・gate・取引に伝播しない。異常時はHOLDし既存branch/receiptsを保持する。

## 6. このEの実行・保存限界

- **Eで再実行していない**：Dの22+14試験、Aの設計上のT01〜T16、Cの62定義済みtest suite、Bの25適格条件の外部検証、GitHub Actions、actual broker/host安全検査、実市場データ。
- **Eで実際に照合した**：#111〜#114のPR状態・exact head、報告ファイルの直接Git blob、変更パスとbase比較、commit/tree/parent metadata、#110の固定head、#107承認追補、#104旧E、現行 main/研究/CSM integration branch refs、CSM gate.json bytes。
- 保存するのは本 E report-only ファイル一つに限る。報告作成後にGitHub readbackでHEAD/tree/blob/変更一覧/共有base非干渉を追検証する。保存後SHAは本ファイル内に自己記載せず、Draft PR本文または最終会話に記録する。新Eの存在は **実装・安全性・研究の承認を意味しない**。
