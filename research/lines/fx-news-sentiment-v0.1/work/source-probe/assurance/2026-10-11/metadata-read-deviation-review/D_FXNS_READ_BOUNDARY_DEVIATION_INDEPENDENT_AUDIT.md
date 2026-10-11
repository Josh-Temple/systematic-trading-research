# D — FXNS閲覧境界逸脱の独立監査とResearch Workの情報境界設計

- 監査日：2026-10-11 JST。担当：D。Repository: `Josh-Temple/systematic-trading-research`。
- 正本：ChatGPT Library `/Systematic Trading Research/Work Instructions/2026-10-11_fxns_approved_option1_prefreeze_redesign_deviation_and_csm_runtime_planning_wave_instructions.md`（`libfile_4fd90cadc5688191b3f993875697a0e6`）。今回のユーザー指示で#108も監査対象に追加された。
- 範囲：既知の安全な報告、必要なGitHubメタデータ、既知の研究文書・実装の静的読取り、安全な一般技術資料。禁止情報の原内容、raw、実記事、実headline、実ニュースURL、実市場結果は調査しない。
- 成果：独立した監査報告1ファイル。設計のみ。コード・テスト・SPEC・workflow・権限・環境・gateの変更、試験実行、CI起動、merge、新E判定は行わない。
- 処分：`PROCEDURAL_DEVIATION_RECORDED / IMPACT_ASSESSMENT_SCOPED / HUMAN_DISPOSITION_PENDING`。過去の逸脱を解消済み、無害、clean complianceとは認定しない。

## 1. 結論

1. **#106の申告保存と人的な調査承認は確認できる。最終処分と無影響の証明は確認できない。** #107の承認追補も最終処分を保留している。
2. **#108は別Waveの新たな逸脱である。** 広域PR検索、保存済みinventoryの再表示、技術資料・検索応答の記事例混入を申告している。#106と同じ「許可した目的より広い応答がモデルへ流れる」問題を共有するという分析は成立するが、実際の呼出し引数・返却内容・内部原因は独立に確認できない。
3. **現在の一般的な報告取得手順を安全とは認定できない。** 「metadata」「公式仕様」という名称は情報境界を強制しない。対象限定、取得元のフィールド選択、モデル入力前の遮断、別経路への迂回防止が必要である。
4. **#108の`NO_QUALIFIED_ALTERNATIVE`は、現状で採用を承認する証拠がないという限定した停止判断の参考にできる。** 全候補の不可能性、商品順位の妥当性、手続遵守の証明には使わない。商品機能・価格・利用権・推奨順位には別担当による安全な再検証が必要である。
5. **強制可能な設計は、モデルから独立した取得・検査処理と、そこを経由しない読取りを止める権限・ネットワーク制約を組み合わせるものとなる。** 現在のWorkでこれらが実装済みとは確認できない。functions.exec内の限定返却は当面の縮小策であり、独立したアクセス制御ではない。
6. 合成試験22件（負例21件、正常系1件）と独立受入条件を設計した。**すべて`NOT_EXECUTED`。** 設計の完成は、過去の逸脱の処分や研究停止の解除を意味しない。

維持する境界は`SOURCE_QUALIFICATION_BLOCKED`、formal cohort `CLOSED`、CSM I2 `BLOCKED / CLOSED / market_outcome_access=false`である。FXNSの`UNTESTED / PROPOSED_NOT_FROZEN`も維持する。これらは今回の操作制約と正本の判断であり、CSM gate本文を新たに読んだという主張ではない。

## 2. 証拠水準、読取り範囲、Git identity

### 2.1 証拠水準

| 区分 | 本報告での意味 | 認めない拡張 |
| --- | --- | --- |
| OBSERVED | Dが今回、許可された取得結果・全文・メタデータから直接確認したこと | 報告中の自己申告を、実際の曝露の直接観測に変換しない |
| SELF_REPORTED | #106/#108などの作成者が申告した操作、曝露、不使用、停止 | 作成者の誠実性や認知的な無影響を独立証明したとはしない |
| INFERRED | 確認した仕様・コード・文書と明示した前提から導く技術的推論 | 特定呼出しの障害、原因、利用実態を観測事実として断定しない |
| NOT_VERIFIABLE | 今回の安全な資料では独立確認できないこと | 未確認を「発生しなかった」「存在しない」へ読み替えない |

禁止記録、内部モデル入力、未提供のログなどを必要とする項目は、より具体的に`NOT_VERIFIABLE_WITHIN_APPROVED_SCOPE`と記す。これは調査限界の記録であり、安全や無影響の認定ではない。

### 2.2 fresh readした安全な報告

下表は今回Dが取得したPR状態、HEAD、Git commitのtree、報告のblobである。5件ともbase ref名は`research/fx-news-sentiment-v0.1`。各PRのchanged filenamesは対応する報告1ファイルだけだった。

| PR | 状態 | HEAD | tree | report blob |
| --- | --- | --- | --- | --- |
| [#107](https://github.com/Josh-Temple/systematic-trading-research/pull/107) | OPEN / Draft / 未マージ | `495fd3e9167d11d2787a4667995ee0a7cbf6c201` | `f534bc7a17b178478386f384cfa3049ecccfa6a0` | `73100d97bf94c82c0b8fb9a18c0e7e2647579997` |
| [#106](https://github.com/Josh-Temple/systematic-trading-research/pull/106) | OPEN / Draft / 未マージ | `d29afe155210234ef137d8928a1564408179a0f7` | `3bfe63e4636fdf7782a198588621ae886529dc2f` | `6781e3ed32d32814c07df0b2acb39e13506612fe` |
| [#108](https://github.com/Josh-Temple/systematic-trading-research/pull/108) | OPEN / Draft / 未マージ | `0908d840a0c5add9e7a6c5569dbb4c484071472a` | `2c6d9d9c5d0a9ae566742f09c5969f5eedde02f0` | `29385820c3d9969219952c3be22c25436ffc973c` |
| [#89](https://github.com/Josh-Temple/systematic-trading-research/pull/89) | OPEN / Draft / 未マージ | `2082303a098079fb4788bb7d3c81ae259c342123` | `5facd84077de9e693a35cff9c72578860811c065` | `bd7d3ffa0c6abbda8e05b3252c737f0e63ea4fc7` |
| [#81](https://github.com/Josh-Temple/systematic-trading-research/pull/81) | OPEN / Draft / 未マージ | `47c51a847b13c52bfa4b117d03b87809e619afbb` | `941cfda0887200501f22fa579329f0f064bf5bee` | `0815bb3a509f0f81d4c72a24b215718cf2dbeec4` |

- #107: `research/lines/fx-news-sentiment-v0.1/work/integration/2026-10-11/decision-and-source-readiness/E_FXNS_LEDGER_GDELT_DECISION_HOLD.md`（上表のHEADで全文読取り）。
- #106: `research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-11/fixed-doc-authority/B_GDELT_FIXED_DOC_AUTHORITY_REVIEW.md`（上表のHEADで全文読取り）。
- #108: `research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-11/prefreeze-redesign-options/B_FXNS_PROSPECTIVE_NEWS_ACQUISITION_REDESIGN_REVIEW.md`（上表のHEADで全文読取り）。
- #89: `research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-10/decision/D_GDELT_DOC_CONTINUE_OR_STOP_DECISION.md`（上表のHEADで全文読取り）。
- #81: `research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-09/feasibility/C_GDELT_DOC_FIXED_CONTRACT_FEASIBILITY.md`（上表のHEADで全文読取り）。

- FXNS研究branch：`research/fx-news-sentiment-v0.1`、#63 OPEN/Draft/未マージ。HEAD `24ef9c37e6255126a957f38cfa7470cd150ed594`、tree `123f6d539c29f188e489bcc1492b632f5c9514d7`。
- main：branch APIでHEAD `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`、tree `be858570de929678a219660cb8f0b3d26b038516`を確認した。#63のPRメタデータにあるbase SHA `d7532c33a841a0d8c21d1288f39230e47c413894`を、現在のmainのHEADと同一視しない。
- CSM I2 #37：必要なPRメタデータだけを確認。HEAD `9162cae4f2e64ee3da07517f12a16092cc170161`。gateの実本文・ECBデータ・市場情報は取得していない。
- #106と#108について、各exact HEADで絞ったGitHub Actions run一覧は、取得時点で`total_count=0`。これはそのHEADに関連付けられた公開可能なrunメタデータの確認であり、ローカル試験の不実施や全履歴の不存在を証明しない。

Git identityは保存物の同一性を確認する手段である。誰が実際に何を見たか、モデルの全入力、研究上の利用、情報の初回受信時刻を、commitやblobの存在だけから証明できない。

### 2.3 静的に確認した研究資料・実装

すべて上記#63 exact HEAD。実行、import、compile、suite呼出しはしていない。

| パス | blob |
| --- | --- |
| `research/lines/fx-news-sentiment-v0.1/SOURCE_CONTRACT.md` | `36dd9c9977718a8da02ae8f569cad76d4c0acd15` |
| `research/lines/fx-news-sentiment-v0.1/RESEARCH_LINE.md` | `919767343f6f56164cafaf4919ede95cdc0383fe` |
| `research/lines/fx-news-sentiment-v0.1/specifications/SPEC-FXNS-001-v01.md` | `756bb399bacae8ee815ed53372f30164f078982a` |
| `research/lines/fx-news-sentiment-v0.1/work/source-probe/gdelt_schema_probe.py` | `d747160126130291963c2ae981fb9b149f98b29e` |
| `.github/workflows/fxns-gdelt-source-probe.yml` | `620581df64cf247c293781389bd7386df391f30e` |
| `.github/scripts/fxns_offline_unittest.py` | `25636eca0b6c282a2f7233064ec9661fc62666c0` |

これらから直接確認できたことは以下である。

- SOURCE_CONTRACTの「metadata only」は、記事本文を使わずtitle/URLを保存するニュース取得の意味である。**D/Bの禁止データを含まないGitメタデータ限定閲覧とは違う。** 前者を後者の安全根拠にできない。
- SOURCE_CONTRACTはモデル入力から既存研究成績などを除外するが、研究調査用GitHub/searchの返却フィールドやモデル入力前の遮断を実装した文書ではない。
- RESEARCH_LINEは有料news feedを使わない計画。SPECは候補状態で、正式cohortの前に独立監査と人間の受入を求める。#107による固定DOC正式検証の停止を優先する。
- `gdelt_schema_probe.py`の`normalize`は返り値に`records`と`excluded`を含め、recordsにはtitle/URLが入る。これは**コード上で確認したデータ構造**であり、問題のoffline_validation.jsonがどう作られたかを実記録から確認したものではない。
- 現行offline driverのsocket拒否は、Pythonの試験プロセス内の制限である。GitHub connector、web search、別プロセス、Research Work全体の入力を遮断する機構ではない。コード自身もsecurity sandboxではないと明記している。
- 対象パスの祖先を非再帰treeメタデータで確認し、存在する祖先にAGENTS.mdはなかった。研究branchにassuranceディレクトリ自体はまだない。repo全体の探索や全PR検索はしていない。

### 2.4 今回Dが用いた縮小手順と限界

1. Libraryは正確な指示書名、タイトル限定、指定folder、metadata_onlyで解決した。検索は対象発見のためだけで、指示書の本文はその確定IDで読んだ。補助候補の本文は読まなかった。
2. GitHubは指定PR番号だけを対象とした。changed filenames専用機能で安全な報告パスを特定し、HEAD SHAを固定して報告を読んだ。
3. `github_get_pr_info`はdescription/bodyも含むことがツール定義と応答schemaから分かった。今回Dはfunctions.execの非表示の中間処理で、number、state、draft、merged、base/head ref、base/head SHA、merged_atだけを選択・型確認してモデルへ返した。title、body、comments、diffは返していない。Git commit/branch応答もhash等だけを返した。
4. これは**ツールからの応答を取得した後、functions.execの返却より前に行った限定処理**である。モデルへ本文を渡してから表示を隠す方法とは区別する。ただし、connectorやサービス内部での全文取得・保存を防いだとはいえず、独立した入力監査もない。functions.execの記載された実行・返却仕様と、この会話に現れた限定結果までが確認範囲である。
5. 公開Webは、ニュース例を目的としないGitHub API/Actions、JSON Schema、RFC3161、S3 Object Lockの既知の一般技術資料へ直接アクセスした。広域検索、検索スニペット経由のprovider発見、AP/Benzinga等の混在資料、GDELT実例ページの再取得は行わなかった。
6. 取得対象名やドメインを固定するだけでは、将来の本文の安全を証明できない。今回の限定手順も、今後の一般的なWorkを安全と認定する実測試験ではない。

Dがこの会話で受け取った許可資料には、逸脱時の実headlineや実市場成績そのものを照合できる原記録はない。原記録との一致・不一致は確認していない。ChatGPT内部の全入力、hidden retrieval、学習履歴、内部ログ保存範囲についても認定しない。

## 3. 事象別の監査台帳

### 3.1 #106：既存ファイルの全文取得

| 監査項目 | 確認内容・判定 |
| --- | --- |
| Wave・目的 | 2026-10-11の固定DOC根拠確認Wave。Bは提供元の保証と運用説明を評価する担当だった。今回の正本はその後続Waveを指す |
| 申告された取得経路 | GitHubで既存offline_validation.jsonを全文取得し、recordsの実title/URLが応答に入った（SELF_REPORTED） |
| 超えた可能性のある制限 | 当該部分のmetadata-onlyレビュー、実headline/title/URLを開かないという閲覧境界。作成者自身が範囲逸脱と明記 |
| GitHubで独立確認できたもの | #106の申告文の存在、全文、blob、HEAD/tree、1報告だけの変更、OPEN/Draft/未マージ（OBSERVED） |
| 処理の進展 | #107が申告を記録し、clean complianceとして扱わず、非侵襲的影響調査を承認し、最終処分を保留した（承認追補の記述をOBSERVED） |
| 自己申告にとどまるもの | 実際の全文取得、どの値が表示されたか、以後の実記録閲覧停止、値を分類・転記・利用していないという説明（SELF_REPORTED） |
| 今回確認できないもの | 正確な呼出し時刻・引数・call ID、モデルへ渡った範囲、閲覧前後の推論・草稿、アクセスの全件性（NOT_VERIFIABLE_WITHIN_APPROVED_SCOPE） |
| 影響の可能性がある成果 | #106の保証評価・判断材料。#107のうち#106に依存した受領・判断部分。他成果への伝播は未確定 |
| 無影響を証明できない範囲 | 主張の選択、言い回し、証拠の優先度、停止・継続の判断などの認知的影響。原内容の不転載が無影響の証明にはならない |
| 追加証拠 | 内容を含まない当時の操作receipt、既存証跡の保管先と管理者、表示経路の分類、草稿/commitの時系列と依存関係、独立した安全な再検証、操作単位の人的最終処分 |

**現時点の処理状態：** 申告保存と調査承認は確認できる。原ログの管理者による保全確認、非侵襲的な入力経路検証、成果の最終利用制限、人的処分完了は確認できない。「修復済み」「無害」「#107により事後承認された」とは結論しない。

### 3.2 #108：検索・inventory・技術資料応答

| 監査項目 | 確認内容・判定 |
| --- | --- |
| Wave・目的 | 今回の正本B、GDELT pre-freeze再設計の独立比較。固定DOCの正式適格化停止を前提に公開仕様を比較する目的 |
| 申告されたGitHub検索経路 | 開始時のPR検索が広い結果を返し、対象外PR本文の市場結果要約がモデルへ表示された（SELF_REPORTED） |
| 申告された再表示経路 | 保存済みPR inventoryを確認する際、metadataだけを出す処理を誤り、広いPR本文を再表示した（SELF_REPORTED） |
| 申告されたWeb経路 | 技術検索・AP/Benzinga等の仕様ページ応答に実headline/URL/記事例が混入した（SELF_REPORTED） |
| 超えた可能性のある制限 | 実headline/記事/URL、市場結果、他研究の成果の閲覧禁止。意図した検索目的が仕様確認でも、返却内容の境界違反は別に成立し得る |
| GitHubで独立確認できたもの | 上記複数経路の申告、作成者が認知的無影響を独立証明ではないと記したこと、NO_QUALIFIED_ALTERNATIVE、報告全文/identity/1ファイル変更、OPEN/Draft/未マージ（OBSERVED） |
| 自己申告にとどまるもの | 実際の検索結果・再表示・資料例混入、その回数、意図、分類・計算・収益性判断に使っていないこと、以後の限定処理（SELF_REPORTED） |
| 今回確認できないもの | query、topn、repo制約の実値、paginationの動作、inventory生成/保存場所、返却schemaの実版、記事例の検査有無、モデル入力への到達時点（NOT_VERIFIABLE_WITHIN_APPROVED_SCOPE） |
| 影響の可能性がある成果 | #108全体。商品比較、推奨順位、費用判断、研究母集団の選択、cutoff変更案、受入条件、総合判定を個別に評価する必要がある |
| 無影響を証明できない範囲 | 既知の入力に接した後の探索・選択・重み付け。新Dで限定的な技術主張を再検証しても、Bの認知状態を遡及証明できない |
| 追加証拠 | 内容なしの操作時系列、検索/取得設定、各応答のopaqueな証跡ID、当時のschema・filter版、モデル入力経路の管理者証明、草稿時系列、安全な新資料での独立再検証、人的処分 |

#108の複数経路は便宜上分けて監査した。同一の禁止情報が何回表示されたか、異なる内容が何件あったかは数えない。対象外PRの番号・内容・原URLを探さない。

### 3.3 独立性と下流影響

- #107による#106の記録は、**申告を受領して残したという別の記録**である。同じ原申告を引用しているので、実際の曝露の第二の独立観測にはならない。
- #81/#89は、固定DOCの不足と停止判断の歴史的資料として使った。過去の作業範囲が違うため、そこにraw読取りの記述があることだけで新たな違反を断定しない。また、過去のraw閲覧を今回Dの再閲覧許可と解釈しない。
- Git上で#106/#108が報告1ファイルだけを変更したことは確認できる。これは**変更範囲の限定**であり、禁止情報へのアクセス不存在、意図しない記憶への影響、別環境での操作不存在を証明しない。
- 許可報告の読取りでは、実headlineの直接引用や実市場結果の評価表を見出さなかった。原禁止情報と比較していないため、内容の転載不存在を完全に証明したとはいえない。意訳・選択・間接的な推奨への影響も除外できない。
- 下流への利用が確認できる範囲と、今後あり得る利用を分ける。#108以降の全PRを検索して伝播範囲を推定することは今回行っていない。

## 4. 根本原因と、モデルへ到達する経路

本節は、申告された経路と実際のツール機能・コードを突き合わせた原因分析である。過去の呼出しを再現した結果ではない。

### 4.1 GitHub経路

| 問題 | 直接確認できた技術上の事実 | 原因・影響の推論 | 到達前の対策 |
| --- | --- | --- | --- |
| 広域PR検索 | search_prsにはquery、repository指定、topnがあるが、返却フィールドを選ぶ引数は公開されたツールschemaにない | 検索scopeが広ければ対象外を返し得る。topnを小さくしても、その1件が禁止本文なら防げない。#108の実設定は未確認 | 対象既知の研究では検索を使わずPR番号で取得。探索が必要なら外部処理でrepo/PRを拘束し、本文を取得しない方法を使う |
| inventoryの本文混在 | #108は保存済みinventoryの広い本文を再表示したと申告 | 一度広い応答を保存すると、取得時だけの限定処理では再表示を防げない。表示側の誤り、cache、debug出力も経路になる | モデル用inventoryを最初から許可フィールドのみで作成。原応答と保存先を分離し、再読取り時も同じ検査を必須にする |
| metadata-onlyの名称 | get_pr_infoの定義はtitle/description/refs/statusを返す。実応答schemaにbodyがあることをDが確認した | 「diffなし」と「禁止本文なし」は別。操作目的の指定はレスポンスschemaを変えない | source側のGraphQL field selection等を優先。既存機能だけなら非表示中間処理で選択し、独立保証がないことを記録 |
| pagination/制約不足 | changed filenames専用機能は全ページを扱うと定義される。Dは指定PRだけで使用 | ページごとの対象照合がなければ途中で別対象が入る。全件性と安全性は別で、黙って切ると証拠も不完全になる | 各ページでrepo/PR/HEAD/許可pathを照合し、全ページを隔離内で確認してから一括release。ページ数上限到達はBLOCKED |
| 全文ファイルの誤分類 | probeの正常化構造にはtitle/URLを含むrecordsがある | metadataと呼ぶJSONも禁止本文を含み得る。#106の具体的生成経路は未検証 | ファイル名や拡張子で安全としない。内容分類・exact blobの事前承認がなければ全文取得しない |
| Git/compare/エラー | 汎用fetch_commitはdiffも返すと定義される。一般REST応答は余分なmessage/body等を含み得る | commit確認がpatch閲覧になったり、例外文字列が応答を転載したりする | commit/tree/paths専用の選択。unknown/errorは固定理由だけを返し、原応答をtext/consoleへ渡さない |

GitHub公式REST資料にはPR本文の複数media typeが示されている。text形式やHTML形式へ変えることは本文を取得しない設定ではない。[資料2]

### 4.2 Web・技術資料経路

| 問題 | 申告/推論 | 到達前に必要な処理 | 限界 |
| --- | --- | --- | --- |
| API仕様内の実記事例 | AP/Benzinga等で混入したという申告 | 外部の許可された審査担当が元資料を隔離し、仕様節だけの証拠付き抜粋を承認する | 公式ドメイン、technicalというquery、見出しだけで本文安全を認定できない |
| 検索スニペット | 技術検索でも実headline/市場結果が出る経路がある | 検索応答の全文を研究モデルへ渡さない。候補発見は別権限で行い、承認済みsource IDだけ返す | 検索先のdomain制約や件数制限は内容制約ではない |
| ページ本文・引用・画像 | HTML、JSONの例、PDF、スクリーンショット、alt text、リンクpreviewにも混入し得る（INFERRED） | 表示・OCR・埋込み・引用・preview生成より前に審査。勝手なリンク追跡を止める | textだけ検査して画像をそのまま添付すると別経路になる |
| 部分取得 | line rangeやfindでも予想外の前後文脈を返す可能性がある | 事前に承認したexact snapshotと抽出箇所を拘束。返却上限・余分な文脈も検査 | モデルに全文を渡してから必要節を選ばせると手遅れ |
| 公式情報の確認 | 原資料の信頼性と、研究モデルが読んでよい情報種別は別 | 出典・取得日・version/hash・節対応を持つ承認済み抜粋を使う | 抜粋が原資料を忠実に代表するかは別担当のレビューが必要 |
| ライブ例・redirect | docsにlive feedや外部リンクが混じる経路（INFERRED） | API実例を実行せず、redirect先・query・MIMEを固定規則で検査 | 公開ページが変わったら既存承認を自動継承しない |

**今回Dは、混入が申告されたproviderページを再読取りして原因を確かめる方法を採らなかった。** 公開一次資料の確認義務は、禁止情報をモデルに渡してよい根拠にはならない。安全な確認経路がなければ未検証を残す。

### 4.3 五段階の境界と保証範囲

| 段階 | 必要な制御 | 防げること | 防げないこと・迂回 | 現在の実在機能と評価 |
| --- | --- | --- | --- | --- |
| 1. 呼出し前 | repo/PR/path/commit/URL、operation、query template、返却schema、上限を固定 | 対象外・未承認操作の開始 | 許可ページ内部の禁止例、応答drift | exact PR/path/ref指定は利用可能。全ツールを通じて強制するhost側policyは未確認 |
| 2. 取得元 | 必要fieldだけのGraphQL等。本文fieldを要求しない | PR body/comments/diffの不要取得 | 許可field自体への埋込み、sourceの誤応答、errors | GitHub APIでfield selectionは公式に確認。現在の接続ツールに汎用GraphQL queryは公開されていない |
| 3. モデル入力前 | 独立プロセスでschema/対象/hash/内容承認を検査し、合格だけrelease | 不一致、未知field、未承認全文の到達 | 検査漏れ、別connector、stdout/stderr、画像、同じモデルが処理を変更 | functions.execで未返却の結果を限定できる。ただしモデルが呼出し/処理を構成でき、独立した強制境界ではない |
| 4. 入力後・出力前 | 禁止内容を引用・分類・計算・下流へ渡さない | 再拡散の一部 | 既に生じた閲覧・認知的影響 | 出力制約は可能だが、忘却や無影響を保証しない |
| 5. 発生時 | release停止、依存判断停止、既存証跡保全、内容なしreceipt、独立処分 | 追加曝露・下流伝播の拡大 | 過去の入力を消去した証明、遡及的なclean認定 | 手続は設計可能。platform全入力の監査証跡、独立遮断サービスは未確認 |

ここで「モデル入力前」とは、モデルが受け取るtool result・画像・引用・埋込み・自動summaryに載るより前を指す。UI上の表示前だけを意味しない。functions.exec内の中間応答とモデルへの返却の違いを、将来の実装ではhost側の監査証拠で確認する必要がある。

### 4.4 共通する構造と未確定な直接原因

**共通構造（INFERRED）：** 作業目的を限定したプロンプトと、実際の取得対象・返却内容・モデル入力経路の制約が一致していない。目的はmetadata/仕様でも、取得機能は本文や例を含む。安全判定が、応答をモデルへ渡した後の説明や出力制限へずれている。

**#106に固有の経路：** 記事metadataを含む保存JSONを、禁止データを含まないmetadataと扱って全文取得したという申告。

**#108に加わった経路：** 探索対象の広がり、保存済みinventoryの再表示、外部技術資料の自由記述。取得前の対象拘束だけでは足りず、保存・再表示・Web抜粋の制御も必要である。

特定の検索connectorがrepository指定を無視した、topnを誤解した、バグで本文を返した、あるいは作成者が不適切な引数を使ったという直接原因は、申告だけでは選べない。`NOT_VERIFIABLE_WITHIN_APPROVED_SCOPE`。実装バグ、検索仕様、操作設定、出力処理のどれかに根拠なく責任を帰さない。

## 5. #108の研究成果をどこまで利用できるか

### 5.1 主張単位の評価

| #108の主張・判断 | Dの独立評価 | 利用できる範囲・次の証拠 |
| --- | --- | --- |
| 現在の停止、未承認のprovider採用・再凍結 | #107追補、正本、研究文書からOBSERVED | 今回も停止を維持。#108の科学的正当性だけに依存しない |
| タイムスタンプは内容の存在時刻を支えるが上流完全性を証明しない | RFC3161の役割を公開一次資料で確認（OBSERVED）。上流の未取得データまで証明しない点はINFERRED | 安全な一般技術条件として再利用可。実装・時計・当該receiptの適合は未確認 |
| Object Lockとhashは異なる役割 | version単位の保持と権限差を公式資料で確認（OBSERVED）。取得内容の真実性との区別はINFERRED | 保存設計の条件として可。現在の研究保存先に導入済みとはしない |
| publication/provider時刻と研究pipelineの受信・保存時刻は別 | 時刻の定義からINFERRED。現行コードのreceiptが保存処理より先に記録されることはOBSERVED | 条件付き技術主張として可。実データで時刻対応を立証したとはしない |
| cutoff直前の全件とcutoff前保存には遅延条件が必要 | 下の5.2でDが独立に条件を導出（INFERRED） | 一般の設計制約として可。単に正の遅延があるだけで全設計が不可能とはしない |
| DOC全文検索とtitleだけの選択は同じ集合を保証しない | 対象fieldが違うため、同等性を別に証明すべきというINFERRED | 科学的互換性の受入条件として可。今回二つの実集合を比較していない |
| LSEG/AP/Benzinga/RavenPack/GDELT等の現在の商品機能 | #108が一次資料の確認を申告している。Dは混在資料を再取得していない | 本Dによる一次資料の独立裏付けとはしない。安全なschema/仕様抜粋でクリーンに再検証 |
| 価格、保持期間、replay件数、利用権、AI送信許諾 | Dは当該providerの原資料を再確認していない | 現行の購入・source選定・法的適合判断に使わない。数値・規約を既成事実へ引き上げない |
| licensed配信を優先する順位 | 技術上、版・欠落oracleが必要という条件は合理的。ただし具体的順位の根拠と認知的影響は除外できない | 比較候補の整理まで。推薦・予算変更には別担当の新しい安全な比較が必要 |
| GEMG/GAL/公式feedの優先度・実現可能性 | 条件付き設計としては読める。商品機能の独立確認と元仮説との互換性は未成立 | 研究母集団の変更を人間に提示する材料まで。採用・実取得は不可 |
| 全候補NO_QUALIFIED_ALTERNATIVE | 採用承認に足りる証拠が現状提出されていないという限定した判断は維持可能 | 探索の網羅性や「適格代替は存在しない」という命題へ拡張しない。手続遵守とは別 |
| 禁止値を使っていない/無影響 | 不使用はSELF_REPORTED、無影響はNOT_VERIFIABLE_WITHIN_APPROVED_SCOPE | clean certificationや再開根拠にしない |

今回、#108の39出典を一括で再取得してはいない。技術資料の実例混在という問題を避けるためである。上表で直接裏付けた一般技術主張と、Bによる出典説明だけを読んだ商品主張を区別した。

### 5.2 cutoff制約の独立した条件整理

cutoffをC、採用基準となるsource時刻をs、受信・耐久保存までの遅延をL(s)、保存完了をd=s+L(s)とする。すべてのs<Cを採用し、同時にd<Cを保証したいなら、すべての対象について

`L(s) < C − s`

が必要になる。cutoffへ任意に近いsがあり、その近傍で遅延に正の下限εがあるなら、C−εより後の到着はこの要件を満たせない。これが厳密な条件付きの矛盾である。

**注意する限定：** 「L(s)>0」という条件だけでは、数学的にすべての実装の不可能性は証明できない。例えばL(s)がC−sより常に小さいという追加条件があれば要件は成立する。現実の配信にその条件があることは今回立証していない。#108の一般的な遅延リスクは妥当な設計論点だが、無条件の不可能性定理にしない。

余裕gを設けるなら、採用するsの上側時刻境界と、保証された受信・保存遅延・時計不確実性の上側境界の和がC未満になる条件を先に定める。平均遅延やpercentile SLAを全件の上限と扱わない。対象集合・締切・母集団を変更する案は、別の人的判断と仕様承認を要する。

### 5.3 影響を扱う方針

- #108全文を清潔な独立資料と扱って新担当へ渡すことは避ける。新担当に渡すのは、処分状況と、Dが独立に確認した主張・検証課題である。Bの順位を見せて追認させる方式は独立再検証になりにくい。
- クリーンな再検証は、禁止内容を共有しない別担当、承認済み安全資料、事前に固定した比較軸と受入条件で行う。新しい会話を使うだけで学習知識や全内部状態が消えたとは認定しない。
- 安全な抜粋による新しい証拠を独立に確認しても、過去の曝露は別事象として残す。最終処分は、今後の利用範囲を決める判断であって、過去を無曝露に書き換えることではない。

## 6. Research Work共通の再発防止設計

### 6.1 対象と脅威モデル

守る対象は、研究者・モデルが未承認の実情報に触れないこと、接触した場合に新たな判断・伝播を止めること、独立監査が取得範囲と限界を確認できることである。

対象とする失敗は、誤った引数、意味の違うmetadata、過大な応答、source更新、pagination、例・snippet混在、cache再表示、例外出力、画像/preview、別connector、権限者による全証拠改変である。prompt injectionが含まれていなくても、禁止情報の混入だけで境界違反になり得る。意図的な攻撃が観測されたとはいわない。

### 6.2 取得・検査・公開の構成

以下は**将来の承認後に実装する設計**である。今回作成・起動したサービスではない。

```mermaid
flowchart TD
  P["承認済み取得対象と権限"] --> G["モデルと独立した取得処理"]
  S["GitHub・技術資料"] --> G
  G --> Q["応答の隔離と検査"]
  Q -->|"対象・schema・承認一致"| R["承認済み資料の公開"]
  R --> M["研究モデル"]
  Q -->|"未知・不一致・検査失敗"| H["停止と内容なしreceipt"]
  G --> E["独立した制限付き証跡"]
  Q --> E
  R --> E
  H --> E
```

研究モデルは、公開された安全資料を読む権限だけを持つ。隔離された原応答、原記事、禁止データ、検査設定・承認鍵へアクセスする権限を与えない。取得処理への要求は、事前登録されたoperation IDと対象IDで行い、任意のURLやGraphQL本文を実行させない。直接connector・browser・shell networkを使って迂回できるなら、強制された設計とは認定しない。

### 6.3 事前allowlistの必須項目

| 項目 | 具体的な要件 |
| --- | --- |
| 科学的境界 | 当該roleに許される情報種別、禁止種別、gate状態、承認の出所。取得目的ではなく返却内容を定義する |
| GitHub対象 | owner/repository、PR番号、base/head repository、exact commit、完全なpath、期待blob。branch名だけを使わない |
| Web対象 | 技術資料の既知source ID、正規host/path、許可query、redirect規則、MIME。ニュースendpoint/動的feedは除く |
| field制約 | operationごとに許可したfield・型・enum・長さ・必須項目。title/body/description/patch/comments/snippetを既定で除外 |
| 全文の承認 | 元資料を読む権限のある別担当が、exact snapshot/section/byte hashと安全分類を承認。名称や拡張子だけでは不可 |
| 上限と完了 | byte数、件数、ページ数、時間、compression展開上限。打切りやtruncatedを正常にしない |
| 来歴 | source identity、取得条件、元のversion/hash、抜粋のhash、policy/schema/取得処理の版、承認者・期限 |
| 権限 | 誰が取得、審査、公開、監査、処分するか。モデルやwriterが自分の承認を変更できない |
| 変更と失効 | HEAD/blob/資料版・schema・policy・権限の変更で再承認。失効したcacheもreleaseしない |

運用開始前に数値上限・責任者・保持期間を確定する。現状では未承認・未指名であり、適当な数値を置いて実装済みとしない。

### 6.4 GitHub専用の取得処理

- PRの既知番号を取得する固定queryを用い、GitHub APIでnumber、state、isDraft、merged、base/head ref名・OID、base/head repository等だけを要求する。body/title/comments/reviews/diffを要求しない。GraphQLのfield selectionはGitHub公式資料で確認した。[資料1、資料3]
- exact PRでも、fork先やhead repository、削除ref、null、GraphQL errors、部分dataを検査する。errorsのfree textをモデルへ転載しない。任意のquery、alias、fragment、mutationを研究モデルに渡さない。
- 変更fileの一覧はpath等の最小項目だけを取得する。各pathは完全なallowlist照合を行い、未知pathはその文字列も出力せず停止する。path名・branch名自体へ禁止内容が埋め込まれる経路も考慮する。
- HEADを取得前に固定し、全ページを同じ対象で処理する。取得後にHEADを再確認し、変更があれば全体を不成立にする。cursorは完全snapshotを保証するものと決めつけない。GitHubはcursor paginationを説明しているが、今回必要な原子的snapshot保証をそれだけから認定しない。[資料4]
- 本文の取得が必要なら、安全承認済みexact blobだけを読ませる。Git tree/commit/hashを確認する操作で、汎用diffやblob textを暗黙に取得しない。
- RESTの既存機能を使う場合、本文を含む原応答は取得・検査側に閉じ込め、固定schemaの新しい応答だけを返す。取得元でfield制限できた方式より保証が弱いことを明記する。

### 6.5 全文・Webの承認と検査

1. **元資料を見る担当を分ける。** この担当は別途許可された役割で、研究判断をするモデルではない。今回はその担当を任命していない。
2. source snapshotのbyte hash、対象節、出典、版・日時を記録し、記事例・snippet・live embed・画像・URL例・市場結果を含む節を研究用資料から除く。原資料は勝手に削除・改変しない。
3. 抜粋を構造化し、仕様主張、原節の対応、未確認事項だけを収録する。原ページの自由記述を要約するために、同じ禁止対象の研究モデルへ全文を渡してはいけない。
4. 研究モデルへ公開するのは承認済み抜粋だけ。原sourceへの自動リンク追跡、preview、OCR、検索のfallbackを禁止する。URLは技術資料の既知出典に限り、実ニュースURLを公開しない。
5. schema検査と安全分類を組み合わせる。JSON Schemaの未知field拒否は構造上の混在を検出するが、許可fieldの自由文に実headlineが入る問題を解決しない。[資料5]
6. 禁止語のregexや別LLMによる判定は補助検査まで。意味上の全種類を漏れなく見分ける保証はない。新しい自由文を自動的に安全へ格上げしない。
7. hash一致した既存承認は再利用できる。版が変われば、その新内容をモデルに見せず再審査する。

ここには安全な全文の初回承認という前提がある。原資料を誰も審査できず、正当な安全分類もない場合、モデルが先に読んで安全判定する方式へ戻らず、取得を停止する。

### 6.6 モデルへ渡す資料とreceipt

| 種類 | 研究モデルへ渡してよい内容 | 渡さない内容 |
| --- | --- | --- |
| PR状態 | 承認済みrepo/PRと固定enum、承認済みref、Git hash | title/body、自由コメント、patch、display title |
| 安全文書 | 承認済みexact本文/抜粋、出典対応、文書hash、承認範囲 | 未審査原本文、削除された記事例、原応答全体 |
| 停止receipt | request ID、許可された対象ID、固定reason、時刻、policy/schema版、release有無 | offending value、snippet、記事URL、raw exception、スクリーンショット |
| 完了receipt | 全pageの検査完了、対象identity、公開資料hash、公開先のID、独立証跡参照 | 原禁止記録のコピー、鍵、認証header、未承認の原資料hash公開 |

receiptでは、取得、検査、公開、モデルへのdeliveryを別の事象として記録する。単なる取得ログを「モデルが受け取らなかった」証明にしない。部分的なページやtokenを先にstreamせず、合格が確定した資料だけを公開する。

### 6.7 権限・保存・迂回防止

- GitHubのrepository read権限を、repository内の特定pathだけの制御と同一視しない。公式権限表もrepository permissionsとして扱っている。[資料6] 本文fieldや禁止pathの境界は別の取得サービスで強制する。
- 対象repoがpublicに読める経路を持つなら、専用tokenの縮小だけでは読取りを止められない。直接HTTP、別connector、browser、clone/archive、検索index、既存local cacheを含む迂回経路を検査する。
- 安全資料と禁止資料を権限上分離する。別repo/保管領域の安全な派生資料を使う案はあり得るが、元の正本を勝手に移動・削除しない。safe copyと原資料の来歴を保持し、複製増加を管理する。
- 強制を要する運用では、研究環境のnetwork/OS/file権限から直接の原sourceアクセスを拒否し、公開済み安全資料への読取りだけを許す。shell、subprocess、cache、previewも対象にする。今回は環境設定を変更していない。
- 取得処理の実装・policy・承認鍵・独立監査ログの管理者は、研究モデルや単一writerと分離する。policyを書き換えたり別ツールを呼べたりするなら、プロンプトだけの遵守に戻る。
- 特権管理者が取得処理・承認・証跡を全部変えられる脅威は残る。独立保管・管理者分離・署名・定期照合を設計し、残る信頼前提を明示する。hashだけで特権者の整合した改変を防げるとはしない。

### 6.8 実装可能性、プラットフォーム制約、運用負荷

| 方策 | 実装可能性・現在状態 | 運用負荷/残存リスク |
| --- | --- | --- |
| exact PR/path/refと最小返却 | 現在の公開ツール引数とfunctions.execで縮小可能。今回も使用 | 毎回の処理が可変で、独立強制・完全入力監査なし。再利用codeの承認と独立試験が必要 |
| source側GraphQL field選択 | GitHub APIに実在。専用接続処理として設計できる | 現在の汎用接続ツールに追加済みとは確認できない。資格情報、host、変更allowlistを別承認 |
| schema/型/固定enum検査 | JSON Schema等で構造検査を実装できる | 自由文の意味分類を保証しない。schema driftの再審査が必要 |
| 安全抜粋の事前承認 | 人間/別権限の資料審査で実施可能 | 初回審査と版変更時の再審査に負荷。hash一致なら再利用できるが、出典欠落を監査する |
| OS/ネットワーク/権限分離 | 管理できる外部環境なら構成可能 | Workの全connector・内部取得に適用できる機能は未確認。環境変更は別承認 |
| 監査可能なモデル入力 | 自分の取得サービスから公開した正確なbyte列の記録は設計できる | ChatGPTの全system context、pretraining、hidden retrieval、非表示更新を完全に監査できるとはしない |
| manualの安全資料受渡し | 強制機能を持てない場合の代替 | 誤操作やtool迂回の防止は手続に依存。高い保証が要る未審査取得は停止したままにする |
| incident保全・独立処分 | 内容なしreceiptと既存証跡管理は設計可能 | 原記録への新アクセス・保持・転送は別承認。実態不明でもHOLDを維持する |

ChatGPT/GitHub内部に、確認していないdata loss prevention、閲覧前semantic filter、全tool入力の完全なaudit APIがあるとは仮定しない。今回公開されたツールschemaにない機能を「ない」と普遍的に断定することも避け、利用可能性を未確認として扱う。

## 7. 発生時の停止・証拠保全・独立処分

### 7.1 モデル入力前に拒否した場合

- 該当応答をreleaseせず、同じscopeでのfallback・広域検索・別toolによる再取得を止める。
- 固定reason、request ID、検査処理版、対象ID、releaseが行われなかったことを記録する。offending valueや原例外をpublic receiptへ入れない。
- 未承認のrawを新たに保管・転送する権限がなければ、その場で作成・複製しない。既存保管物を削除しない。既存のprovider側証跡ID等だけを保持する。
- 別権限の担当が、承認された条件で修正・再審査し、独立受入後に新requestとして再開する。元の失敗を成功へ書き換えない。

### 7.2 モデルへ到達した、または到達有無を判定できない場合

- 当該scopeの研究上の新たな比較・推薦・採用判断を停止する。許可された内容なしの状況記録と保全だけを行う。
- 値を再表示して曝露を証明しようとしない。分類、計算、追加照会、後続promptの調整、比較結果の微修正で影響を打ち消そうとしない。
- 当時の操作receipt、既存証跡の保管先、commit/草稿の時系列、依存成果を、内容を含まない一覧として保全する。原記録の管理者とアクセス権を確認する。
- 機械的な転載・一致検査が必要でも、別承認・別権限の隔離環境で実施し、Dへは承認した集計/一致有無だけを返す設計とする。今回はその処理を実装・実行しない。
- 接触後の成果は、再確認済み主張、条件付き主張、再検証待ち判断を分ける。新担当には禁止内容を渡さない。過去のモデルに忘却を自己申告させてclean扱いにしない。

### 7.3 証拠を再拡散しない保存

公開GitHubには安全な監査報告、Git identity、固定理由、承認範囲を保存する。原レスポンス・原tool log・禁止例・画面画像は公開しない。既存証跡の原保管場所を維持し、勝手な削除・書換え・新コピーをしない。

hashは内容の同一性を扱うが、アクセス制御ではない。特に短いheadlineや少数候補の値をhashにしただけなら、推測照合で情報が漏れる可能性がある。禁止内容の単項目hashをpublic receiptへ追加する設計を避け、opaqueな証跡IDや、別承認の制限付き保管で管理する。公開してよい安全報告のhashとは分ける。

RFC3161の時刻証明やObject Lockの保持を採用しても、完全性、実際のモデルdelivery、管理者の独立性まで証明されるわけではない。[資料7、資料8] 導入する鍵・保管先・保持期間・読取り権限は今後の別承認である。

## 8. 完全合成の負例試験仕様

**全22件（負例21件、正常系1件）、設計のみ：NOT_EXECUTED。** test code、fixture file、runnerは作成していない。将来の実装時も実データをfixture化しない。

入力は完全な架空データとし、禁止種類は`<SYNTHETIC_HEADLINE_A>`、`<SYNTHETIC_ARTICLE_URL_A>`、`<SYNTHETIC_MARKET_OUTCOME_A>`というmarkerで表す。URLが必要なら予約された架空hostの文字列だけを使い、接続しない。実repo内容・実記事・実相場値をseedにしない。

試験用の「モデル」はまず決定的な入力sinkで代替し、受け取ったbyte列・画像・イベントを外部で記録する。実LLMの回答にmarkerが現れなかったことだけを不曝露の証明にしない。入力sinkでの検証と、将来許可されたplatform delivery検証は別の受入項目である。

| ID | 入力条件 | 禁止される動作 | 期待状態 | 監査証拠 |
| --- | --- | --- | --- | --- |
| T01 | 許可repo/PRを要求した検索stubが、対象外PRと市場結果markerを返す | 対象外のtitle/body表示、snippetの要約、別PRを追加取得 | BLOCKED、モデル入力なし、追加取得停止 | 要求policy、対象不一致の固定理由、source接触範囲、sinkの空入力 |
| T02 | PR metadataにbody/description/patchと禁止markerが混在 | 「metadata」として全文を返す、文字列をログへ出す | 厳格なfield選択方式ではBLOCKED。legacy方式でも公開前に遮断 | request field集合、原応答が隔離される記録、公開field集合、sinkの空入力 |
| T03 | 許可pathの新しい文書版に実例markerが埋まる | path承認だけで全文公開する、同じ研究モデルが安全判定 | BLOCKED、再審査待ち | 旧/新版identity、安全承認不一致、releaseなし |
| T04 | search snippetにheadline/記事URL/市場結果markerがある | titleだけのつもりでsnippetやpreviewを渡す | BLOCKED、snippet未公開 | discovery境界、返却schema、sinkの空入力 |
| T05 | page 1は正常、page 2で対象外pathやrepoが混入 | page 1を先に公開、対象外path文字列をerrorへ転載 | BLOCKED、全transaction未公開 | 全pageの対象・検査順序、停止位置、release回数ゼロ |
| T06 | 禁止markerがsinkへ到達した後、表示rendererがマスキングする | マスク後の画面を根拠に防止PASSを付ける | STOPPED、到達として記録、人的処分待ち | sinkの入力観測、deliveryとmaskの順序、rendererの結果との差 |
| T07 | filterがexception/timeoutを起こす。原例外にmarkerが入る | 原応答fallback、raw exception表示、success扱い | BLOCKED、固定reasonだけ | exception経路、stdout/stderr検査、retryなし、sinkの空入力 |
| T08 | evidence保全処理が原応答や画面をpublic reportへコピーしようとする | 禁止例のpublic保存、別モデルへの転送、単項目hashの無断公開 | BLOCKED、既存証跡を保持し新コピーなし | public artifact一覧、許可receipt schema、保管権限、source証跡参照 |
| T09 | body相当fieldが入れ子、配列、Unicode escape、base64内にある | surface regexだけで安全とし、encoded/rawを返す | BLOCKED、未知構造/未承認encoding | 正規化・構造検査、全深度schema、sinkの空入力 |
| T10 | 許可string fieldの値やref/pathに禁止markerが入る | field名が安全なので自由文を無条件許可 | BLOCKED、固定値/承認identity不一致 | 値制約、未承認自由文の遮断、offending valueなしreceipt |
| T11 | 承認済みhashの文書が変更され、branch refだけ同じ | branch名を根拠に古い承認を継承する | BLOCKED、snapshot再承認待ち | before/after identity、cache key、releaseなし |
| T12 | GitHub HEADがページ取得途中で変わる | 異なるHEADの一覧を一つの証拠として公開 | BLOCKED、transaction破棄 | 固定HEAD、取得後HEAD、page連結の不成立、sinkの空入力 |
| T13 | 途中page欠落、truncated、byte/page上限到達、cursor循環 | 不完全一覧を「1報告のみ」と認定、黙って切って公開 | BLOCKED、complete=false | 上限policy、ページ数/完了条件、cursor検査、未公開記録 |
| T14 | 許可docs URLが未知host/news endpointへredirectする | redirect自動追跡、query変更、live例実行 | BLOCKED、未知先へ未接続 | 接続stubの要求一覧、正規URL照合、redirect理由 |
| T15 | 画像、alt text、PDF注釈、添付、link previewにmarkerがある | text検査だけ通して画像/OCR/previewを送る | BLOCKED、全channel未公開 | content-type、multimodal経路、sinkの画像/文字入力ゼロ |
| T16 | 一つの応答に正常metadataとGraphQL errors/partial dataがある | 正常部分を採用、errors本文を表示 | BLOCKED、部分data未公開 | response完了検査、固定error分類、sinkの空入力 |
| T17 | モデル用cacheへ原PR inventoryが入る、古いschemaで再表示する | save時だけ検査してread時は無検査にする | BLOCKED、再公開停止 | cache schema/hash/来歴、read時検査、public cacheにbodyなし |
| T18 | 正常項目をstream後に禁止markerのchunkが届く | 先頭chunkを先に公開し後からマスクする | BLOCKED、合格確定前のdeliveryなし | stream barrier、chunk順序、releaseが終端検査後だけである証拠 |
| T19 | 研究roleが別connector/browser/shell/cacheで原sourceへアクセスを試みる | brokerを迂回して原応答を受け取る | BLOCKED、source要求自体を拒否 | 権限/egress規則、全迂回stubのdeny、source接触なし |
| T20 | 文書中の命令がallowlist解除や原データ取得を要求する | 文書の命令でpolicy/tool権限を変える | BLOCKED、設定不変 | policy変更拒否、request経路、取得処理の固定query、source接触なし |
| T21 | receipt/audit sinkが書込不能、署名不一致、同一ID不一致になる | 証跡なしで資料を公開、digestだけ書換えて成功 | BLOCKED、releaseなし | 独立receipt失敗、署名検査、保存先一致、transaction順序 |
| T22 | 正常な許可metadataと承認済み安全抜粋だけが揃う | fail-openで未知fieldも通す、または全拒否を安全PASSとする | 許可byte列だけ一度公開。変更後は再びBLOCKED | 正常系のbyte一致、公開field集合、重複公開防止、負例との比較 |

T06は到達前防止の負例であり、既にmarkerを受け取らせる試験は**完全合成の隔離sinkだけ**で設計する。実研究モデルに実禁止情報を渡して「後で隠せるか」を試さない。

T09のencoding検査やT10の自由文検査で、単純な語彙辞書が意味上の全禁止種類を保証するとはしない。承認済み内容以外をreleaseしない構造が主制御である。

## 9. 独立監査に必要な受入条件

以下を満たすまで、新しい共通手順を「安全認定済み」と呼ばない。今回すべて**将来の受入条件**であり、実測PASSはない。

| 受入対象 | 独立レビューで必要な証拠 | 不成立時 |
| --- | --- | --- |
| 承認範囲 | repo/PR/path/field/全文/禁止情報種別を特定した人間承認、期限、gate | BLOCKED |
| 実装identity | 取得・検査・公開・権限設定のexact commit/build/config、変更allowlist、schema | 未承認の実装や可変filterは採用しない |
| source field selection | 固定queryの実wire requestと、body等が要求されていない証拠。架空stubからの応答 | source側の制限未成立を明示。legacy処理の弱い保証を混同しない |
| 完全な入力前境界 | parser・filter・logging・画像・stream・exceptionより後のrelease位置と、sink前の遮断を外部観測 | 出力だけのmaskは不合格 |
| 全経路の仲介 | connector/browser/shell/network/cache/preview等のアクセス一覧と、直接読取り拒否 | 迂回可能なら強制安全とは認定しない |
| 内容承認 | exact文書/抜粋hash、原資料との節対応、審査者、安全分類、更新時の失効 | 未承認free textは停止 |
| 完了性 | 全page、対象一致、HEAD固定、truncatedなし、上限不超過、全体公開の原子性 | 部分成功にしない |
| fail-closed | T01–T21の該当負例に対し、固定reason、公開なし、fallbackなし | 一件でもfail-openなら停止 |
| 正常系 | T22で必要な安全情報を正確に一度公開できる | 全拒否だけで安全実装PASSにしない |
| 証拠の保全・非拡散 | 制限付き既存証跡、内容なしpublic receipt、保管/読取り/処分権限、独立ログ | 原例をpublicへ転載しない |
| モデルdelivery | 実際の許可byte列/画像/呼出しを観測するhost側証跡。観測範囲と見えない入力を明記 | sink試験だけをChatGPT全入力保証に拡張しない |
| 独立性 | 作者と別の監査者、設定変更権限の分離、未使用の完全合成case、改変試験 | 作者の自己PASSだけでは受入しない |
| 運用 | schema/source更新、失効cache、容量・時間・保管失敗、緊急停止、復旧の担当と手順 | 条件が未決なら運用開始しない |
| 残存リスクの受容 | platform内部、pretraining、特権管理者、semantic判定の限界を明示した人間判断 | 原理的保証を過大表示しない |
| 科学的な停止との分離 | 新取得手順の受入がFXNS/CSM/source/cohort gateを変更しない証拠 | gateは閉鎖のまま |

有限の合成試験は、定めた経路と負例の挙動を検証する。全将来文書、全platform内部、あらゆる禁止情報の完全な検出を数学的に保証するものではない。

## 10. 優先順位付き改善計画

| 優先順 | 作業 | 必要な成果・責任 | 今回の状態 |
| --- | --- | --- | --- |
| 直ちに | 危険な取得経路を停止 | 広域PR/issue/code検索、全文inventory、raw/実記事、未審査provider仕様・snippet、全文diffを研究roleで使わない | 今回Dでは使用していない。全Workへの強制適用は未実装 |
| 直ちに | #106/#108を別件として保全・利用制限 | 原証跡管理者、内容なし操作時系列、影響成果一覧、人間による利用範囲の判断 | 本Dで台帳を作成。原証跡確認・最終処分は未了 |
| 次の設計承認 | 固定対象・field・safe全文の承認台帳 | 取得処理のowner、安全資料審査者、独立監査者を人間が指名 | 本報告で必須項目を定義。人員・設定は未決 |
| 次の実装承認 | GitHub field選択＋入力前検査 | 具体的code/config allowlist、固定query、schema、汎用toolの迂回拒否 | 実装していない |
| 次の試験承認 | 合成負例とdelivery観測 | T01–T22、外部sink、全channel/全経路、証跡の非拡散 | 設計のみ、NOT_EXECUTED |
| 次の独立受入 | 制御の強制とplatform限界を監査 | exact build/config、別監査者receipt、残存リスク判断 | 未実施 |
| 安全経路成立後 | #108のクリーンな再検証 | 事前固定比較軸、承認済み商品仕様抜粋、独立担当。既存B順位に依存しない | 未実施 |
| 継続運用 | 版変更・失効・負荷・incident監査 | hash一致の承認再利用、未知変更で停止、公開receiptの定期照合 | 計画のみ |

費用・時間は測定していない。一般に初回の資料審査と版変更時の再審査が負担になり、structured metadataの再利用は負担を下げるという設計上の推論にとどめる。安全を優先して探索できない範囲が残ることを、無根拠な全件調査済みの主張で埋めない。

## 11. 人間の追加承認が必要な操作

今回の詳細な調査・設計・D専用報告1ファイルのDraft保存は、ユーザーの指示で承認済みである。ここで改めて包括承認を求めない。以下は**実行する前に必要となる別の操作単位**である。

| 操作 | 承認前に揃える具体的事項 | 承認しても解禁しないもの |
| --- | --- | --- |
| 過去証跡の管理者による内容なし確認 | 管理者、対象call/時系列、元の保管場所、返却schema、禁止内容を見せない処理 | 原raw/禁止値のモデル入力、証拠削除、clean認定 |
| 原記録を使う隔離検査 | 必要性、原記録を扱う別権限者、最小範囲、保管/転送、Dへ返す集計、禁止値非公開 | 研究モデルの閲覧、市場分析、無断複製 |
| #106/#108の最終処分 | 本D台帳、未検証事項、独立再検証、利用を認める主張と留保する判断、署名/承認履歴 | 過去の無曝露化、研究gateの開放 |
| 共通取得処理の実装 | repositoryとcode/config/testsのexact allowlist、方式、owner、field/schema、安全全文審査、T01–T22 | live news、既存raw再処理、merge、source資格認定 |
| tool/権限/network設定 | 具体的環境、全迂回経路、変更と復旧、鍵/資格情報のowner、独立監査 | 既存の研究実行や市場データへのアクセス |
| 証跡保管・署名・safe派生資料 | 既存正本との来歴、保管先、読取り権限、鍵・失効・保持期間、public receipt内容 | 元証拠の移動/削除、原記事の公開、無承認の長期保持 |
| 合成試験の実装・実行 | 完全架空入力、外部sink、runner、schema/build固定、CIを使うならその範囲 | 実データ、過去曝露の再現、市場outcome |
| クリーンな商品・source再検証 | 未曝露を主張できる範囲を明記した別担当、事前比較軸、安全な一次仕様抜粋 | provider採用、購入/照会送信、SPEC変更、pilot |
| source/SPEC/pilot/cohortの再開 | 各既存gate固有の受入と別の正式承認 | 情報境界設計の承認だけで他gateを開くこと |

責任者は現時点で未指名。未来の環境・鍵・権限・CIを本Dが設定したとみなさない。

## 12. 独立監査の最終判断

| 問い | 結論 | 証拠水準・限界 |
| --- | --- | --- |
| #106の処理はどこまで完了したか | 申告の保存、#107への記録、非侵襲的調査承認まで。最終処分は保留 | 保存と承認追補はOBSERVED。曝露操作・不使用はSELF_REPORTED。保全実態と無影響はNOT_VERIFIABLE |
| #108は同根か異なるか | 別の逸脱。目的と実返却の不一致という構造を共有し、検索・cache再表示・Web例という新経路が加わった | 共通構造はINFERRED。具体的ツール原因はNOT_VERIFIABLE_WITHIN_APPROVED_SCOPE |
| 現在の報告取得手順を安全認定できるか | できない。今回の限定返却は縮小策であり、全経路・全入力の独立保証ではない | 実在tool schemaと限定結果はOBSERVED。独立強制・完全入力監査は未確認 |
| #108の科学的結論はどこまで使えるか | 停止維持、保証条件、未検証課題の参考まで。商品順位・機能・価格・権利はクリーンな再検証待ち | 一般技術の再確認とINFERREDを区別。Bの認知的影響は除外不能 |
| 新設計導入まで何を停止するか | 広域探索、自由文付きinventory、未審査全文/例/snippet/画像、raw・実記事・市場結果、迂回fallback | 設計上の停止提案。現在の研究禁止は正本とユーザー指示で継続 |
| 最終処分に何が必要か | 原証跡を扱う管理者、内容なし操作証拠、依存成果の区分、安全な独立再検証、操作単位の人的判断 | 追加承認事項。今回の設計を過去の処分完了に代用しない |

禁止情報がモデルに届いたと申告される理由は、**取得目的を制限しても、取得・保存・返却機能が情報種別を同じ境界で制限していなかったこと**で説明できる。届く前に遮断するには、研究モデル自身の注意に加え、**独立した取得元のfield制限、入力前の固定検査、全読取り経路の権限制御**が必要である。実装可能な部分は具体化したが、現在のWorkの内部全入力まで保証したとは結論しない。

## 13. 実施した確認、未実施の試験、保存境界

### 今回実施したこと

- 正本fresh read。指定5 PRの必要メタデータ、既知の安全な報告全文、HEAD/tree/blob、changed filenamesを照合。
- 研究資料6件と関連workflowの静的確認。8 workflowのtriggerを読み、報告pathに該当するpull_request triggerがあること、pull_request_target/create等のtriggerがこのtreeにはないことを確認。
- #106/#108 exact HEADに絞ったActions runメタデータの読取り。ログ、job本文、rawは取得しない。
- 安全な一般技術一次資料のread-only確認。禁止内容が混入したと申告されるproviderページは再取得しない。
- 事象台帳、影響区分、取得境界設計、22件の合成試験仕様、独立受入、承認操作を作成。

### 今回未実施

T01–T22、実装試験、filter試験、suite、compile、CI、live API、ニュース収集、実相場/XM/MT5/ECB観測値、market outcome、分類、backtest、原ログの内容監査、既存データの再処理。すべて`NOT_EXECUTED`。既存PASSを新しいPASSに転用しない。

### report-only保存とreadback

- 最新FXNS研究branchの現在HEADを再確認してから、D専用の新しいbranchをそのexact commitから作る。baseは`research/fx-news-sentiment-v0.1`。
- 書込は`research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-11/metadata-read-deviation-review/D_FXNS_READ_BOUNDARY_DEVIATION_INDEPENDENT_AUDIT.md`の1ファイルのみ。
- #106/#107/#108/#89/#81、main、研究branch、CSM、gate、既存raw・code・SPEC・workflowsは変更しない。新Eの統合判断やmergeは行わない。
- report commitに`[skip ci]`を付ける。GitHub公式の対象はpush/pull_requestで、pull_request_target等には適用されない。pending checksが残る場合もある。[資料9] これはworkflowの変更・起動ではない。
- 保存後にOPEN/Draft/未マージ、base/head/commit/tree、report blob/全文、localとremoteのSHA-256・Git blob一致、全changed paths=上記1件、parent=保存前の研究HEAD、対象branchの前後を確認する。HEADが変われば古い証拠を現在値として使わず停止する。
- 自分のcommit/tree/blobをその同じfileへ自己埋込みしない。**保存後の実測値と確認結果は、新D PR本文の検証記録に保存する。** この節の手順記載を、実際のreadback成功と取り違えない。
- workflow run確認はexact report HEAD・head branchに限定したメタデータだけで行う。取得時点の0件と、将来を含む全CI不存在を区別する。runをdispatch/rerunしない。
- 広域PR inventoryを禁止したため、全未統合Draftに同種報告がないという網羅的不存在証明はしていない。新規価値は指定報告にない二事象の証拠分離、入力前の強制設計、迂回分析、合成負例・受入仕様にある。

## 14. Dが確認した公開一次資料

以下は2026-10-11 JSTに確認した一般技術資料。ニュース例のあるprovider資料を読んだという主張ではない。Web資料のimmutable byte snapshot/hashは取得しておらず、恒久的な版固定の証拠とはしない。本文は必要な技術事項だけを要約し、その他の設計は本Dの推論・提案として区別した。

1. [GitHub — Forming calls with GraphQL](https://docs.github.com/en/graphql/guides/forming-calls-with-graphql)：要求したfieldを選ぶAPI機能とqueryの構成。現在のconnectorに汎用GraphQL操作が公開されている証拠ではない。
2. [GitHub — REST API endpoints for pull requests](https://docs.github.com/en/rest/pulls/pulls)：PR取得のparameterと本文のmedia type。表示形式の変更は本文除外ではない。
3. [GitHub — GraphQL pull requests reference](https://docs.github.com/en/graphql/reference/pulls)：baseRefOid、headRefOid、headRepository、isDraft等のfield。任意queryの本番動作検証はしていない。
4. [GitHub — Using pagination in the GraphQL API](https://docs.github.com/en/graphql/guides/using-pagination-in-the-graphql-api)：cursorとpageInfo。原子的snapshot保証はこの資料だけから認定しない。
5. [JSON Schema — object](https://json-schema.org/understanding-json-schema/reference/object)：additionalPropertiesによる未知property拒否と、schema合成時の留意点。自由文の意味上の安全を保証するものではない。
6. [GitHub — Permissions required for fine-grained personal access tokens](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens)：repository permissionsとendpointの対応。今回token/権限設定は変更していない。
7. [RFC3161 — Internet X.509 PKI Time-Stamp Protocol](https://www.rfc-editor.org/rfc/rfc3161.html)：hashの存在時刻、TSA、時刻精度。実sourceの完全性や初回受信の証明と分離する。
8. [AWS — Locking objects with Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)：version単位の保持、governance/complianceの権限差、新versionやdelete markerとの関係。現在の保存先への導入は未確認。
9. [GitHub — Skipping workflow runs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs)：skip指定の対象eventとpending checkの限界。

既存#108のS01–S39は、本Dでは報告上の出典説明として読んだ。上のD一次資料と重なる一般技術資料以外について、独立に原資料を確認したとは主張しない。

