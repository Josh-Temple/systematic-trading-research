# Repository review follow-up — 2026-09-27

記録日: 2026-09-27 JST
状態: 対応中（2026-09-27 outcome-blind follow-up実施）
対象: Josh-Temple/systematic-trading-research
レビュー対象main: `997c08a393d06b293c0f908870367f3f36344046`
記録前のfresh readでも同じmainを確認。

## 目的と評価範囲

研究経緯を追跡する知識基盤としての構造は整っている。一方、再実行に必要な仕様・コードの確定と、研究正本とWeb表示の整合性維持を補強する余地がある。以下は後日着手するための作業一覧であり、科学的判断、凍結仕様、研究データの利用権限を変更しない。

今回のレビューはGitHub内の記録・コードと公開ファイルの確認に限る。Drive原資料との再照合、研究計算の再実行、Android実機の視覚確認は実施していない。以下の未解決事項は、原資料自体の欠陥が確定したという意味ではない。

## 着手時の共通手順

1. 現在のmainと関連文書をfresh readし、この記録以後の変更・既存対応を確認する。
2. [研究原則](RESEARCH_PRINCIPLES.md)、[Knowledge Base仕様](KNOWLEDGE_BASE_V0.1.md)、[現在の研究要約](../research/lines/horizontal-reaction-v0.1/CURRENT.md)、関連するDecisionを読む。
3. 過去のチャットやこのレビューの状態を、着手時点の現在状態の根拠にしない。
4. 研究条件やschemaを独自に変更せず、UNKNOWN / UNVERIFIEDを推測で埋めない。使用済みsampleを未使用へ戻さない。
5. 対応完了時は、この一覧に実装・検証のcommitまたはPRを追記する。未検証の部分は明示する。

## 1. 次の実験前に、H3が参照する実行仕様・コードを確定する

優先度: 高（次の実験の実行前）
状態: **HOLD — 仕様／保存コードの不一致を記録済み。H3実行前にversioned decisionが必要**

### 確認した事実

- [SPEC-HR-001-v01](../research/lines/horizontal-reaction-v0.1/specifications/SPEC-HR-001-v01.md)のGamma定義は、候補時点より前の終値変化を使うと記述しているが、平均の対象窓・観測数は本文だけでは一意にならない。
- 接近、再接近、interaction resetにも自然言語の記述が残る。
- [SPEC-HR-003-v01](../research/lines/horizontal-reaction-v0.1/specifications/SPEC-HR-003-v01.md)は「既存のfirst-touch generator」「既存D4のquote-side convention」を参照するが、GitHub内の仕様だけで実装を一意に再構成するには不足がある。
- H1の計算コード・実行環境には未取得のものがある。H2は[RUN-HR-006](../research/lines/horizontal-reaction-v0.1/runs/RUN-HR-006.yaml)にscript名とhashがあるが、コード本体の参照先は外部資料である。

### 作業

- 元の凍結資料・既存コードをfresh readし、計算窓、touch判定、reset、confirmation、時刻境界、価格側を照合する。
- 既存コードを取得できた場合は、既存hashとの一致、取得元・版・適用範囲を記録する。
- 凍結済みSpecificationを黙って書き換えず、必要なら既存の訂正・版管理方針に従い、原資料との対応を示す補足記録を作る。
- 原資料でも確定できない条件は未解決として残す。新しい仕様を作って旧仕様の再現と扱わない。
- H3の結果を見ずに、合成データ等による境界条件の確認が可能な範囲を整理する。

### 2026-09-27 follow-up result

Outcome-blindなfresh readで、Source Pack内の `run_v01.py` を回収し、stored manifestとSHA-256が完全一致することを確認した。

- Drive file ID: `1nWSPnCI-cVn0miZuQZrgm9ihWc6ap3NO`
- bytes: `24350`
- SHA-256: `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`
- H2 reproducibility codeはこの `run_v01.py` の `build_session_events(...)["touches"]` を再利用している。

exact codeから、60-bar S/R、approach/touch、pending confirmation、interaction lock/reset、D4 quote-side conventionは復元できた。

一方、重要な不一致を確認した。凍結仕様とH1 Execution ResultはGammaをcandidate minuteより前のClose変化だけから計算すると記述するが、保存コードの実行pathは `abs_change_prefix[global_i]` を使用し、candidate bar CloseをGammaへ含める。さらにGammaは60-bar windowではなくexpanding prefix calculationである。outcome-free synthetic checkでもcandidate bar Closeだけを変えると実行Gammaが変化した。

また、historical generatorが同一confirmation bar上の複数confirmationをambiguousとしてclean eventから除外する一方、H3は全eligible touchを `CONFIRMED` / `UNCONFIRMED` の二群へ分類するため、そのmappingも資料だけでは未確定。

詳細:
[H3 execution identity precheck](../research/lines/horizontal-reaction-v0.1/H3_EXECUTION_IDENTITY_PRECHECK_2026-09-27.md)

結論: H3はmaturityだけでは実行準備完了にならない。Gamma authorityとambiguous confirmation mappingをversioned decisionで解消するまで、outcome計算はHOLD。H3 outcomeは閲覧・計算していない。

### 完了条件

- 別の実装者が、参照資料・コードの識別情報から同じ規則を確認できる。
- 確定条件と未解決条件が分離されている。
- H3実行に必要な未解決条件が残る場合、実行準備完了とはしない。
- H3の60 eligible sessionsのfreezeとsource gate PASS前に、touch outcome、群間比較、primary contrast、bootstrapを計算・閲覧していない。

この作業一覧はH3の実行許可を与えない。実行可否は着手時の正本と既存gateで確認する。

## 2. 正本とWeb表示の整合性を最小限のCIで確認する

優先度: 中
状態: 未着手

### 確認した事実

- [Web表示データ](../web/data/horizontal-reaction-v0.1.js)は、研究正本とは別の静的JSファイルに数値・状態を保持する。
- [Pages workflow](../.github/workflows/pages.yml)のpush対象は `web/**` とworkflow自身であり、研究記録だけの変更では動かない。
- 表示データには生成日があるが、参照元commitの識別情報はない。
- レビュー対象のtreeには、研究エンティティと表示の整合性を検証するCIはない。

### 作業

- 既存schemaを変更せず、ID重複、参照先欠落、YAML解析、Resultの独立した状態項目を検証する。
- H1/H2/H3の状態、主要数値、データ利用状態、未解決conflictを正本と照合する。
- 正本変更時に、古い表示のまま検証を通過しない仕組みを作る。小さな生成処理か同期確認のどちらが適切か、既存Phase 5計画と整合させる。
- 表示がどの正本commitを参照するか確認できるようにする。
- 新しい大規模frameworkの導入を前提としない。

### 完了条件

- 参照切れや主要状態・数値の不一致を意図的に入れると検証が失敗する。
- 正本と表示が一致する状態では検証が成功する。
- 正本更新から公開表示までの更新手順・失敗時の扱いが明文化される。
- CI成功を科学的妥当性や再現計算の成功と同一視しない。

## 3. Webの根拠への導線を完成させる

優先度: 中
状態: 実装・静的検証済み（review branch）

### 確認した事実

- [app.js](../web/app.js)は `diagnostics.canonical` を画面に描画していない。
- 研究履歴はResult等のIDを文字列で表示し、各記録へのリンクにはしていない。
- 上部の「Canonical」は派生要約の `CURRENT.md` に遷移する。一方、Knowledge Base仕様はCURRENTを非正本のprojectionと定義する。

### 作業と完了条件

- 診断欄から関連Interpretation / Resultへ直接移動できるようにする。
- 履歴の各IDから対応記録へ移動できるようにする。複数IDの行は各記録を明示する。
- CURRENTへのリンク名を「現在の要約」等にし、Result・Decision等の正本との区別を明確にする。
- スマートフォン幅でリンクの操作・折返しを確認する。Android実機での確認ができない場合は、その限界を記録する。
- SOURCE CONFLICT、BLOCKED、NOT SUPPORTED、CONSUMED、UNUSEDの区別を維持する。

## 4. READMEと公開・検証状態を更新する

優先度: 低（短時間で対応可能）
状態: 実装・Actions再確認済み（Android実機確認は未完了）

### 確認した事実

- [README](../README.md)のCurrent stageはPhase 0のまま。
- [ROADMAP](ROADMAP.md)と[web/VALIDATION.md](../web/VALIDATION.md)には初回公開待ちの記録が残る。
- レビュー時点では[Actions run 36316165611](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36316165611)の成功と、公開ファイルの取得・リポジトリとの一致を確認した。

### 作業と完了条件

- 着手時のActions・公開状態を再確認する。
- READMEから現在の段階、公開URL、現在の研究要約、この作業一覧へ辿れるようにする。
- 過去の公開失敗は履歴として保持し、その後の成功を追記する。
- 公開成功と、Android視覚確認・Phase 4 exit review完了を区別する。未実施の確認を完了扱いにしない。

## 保持すべき良い点・既知の限界

- 仮説・仕様・実験・実行・結果・解釈・判断が分離されている。
- blocked executionとnegative scientific result、exploratoryとconfirmatory、consumedとunusedが区別されている。
- H1 D1-D5の資料間不一致は[RES-HR-005](../research/lines/horizontal-reaction-v0.1/results/RES-HR-005.md)に保存され、CURRENTとWebでも明示されている。今回その不一致を解決したとはしていない。
- Phase 3の「GitHubから再構成できる」は研究状態・経緯についての評価であり、同じ計算を再実行できることの証明ではない。
- MCP、研究ライン拡大、自動研究の拡大より前に、上記の実行仕様・整合性維持を補強することを推奨する。これはレビュー上の提案であり、既存roadmapや研究権限を上書きしない。

## 2026-09-27 follow-up implementation progress

Review branch: `review-followup/h3-integrity-and-phase4-state`

- H3 exact code identity / hash確認: 完了
- H3 Gamma spec/code conflictの記録: 完了
- CURRENTへのexecution boundary反映: 完了
- Web diagnostics canonical link: 実装済み
- Timeline artifact links: 実装済み
- CURRENTリンク名を「現在の要約」へ変更: 実装済み
- WebへH3 execution HOLD表示を追加: 実装済み
- README / ROADMAP / web/VALIDATIONのPages公開状態更新: 実装済み
- Actions run `36316165611`: fresh readで `SUCCESS`、deployment source `997c08a393d06b293c0f908870367f3f36344046` を再確認
- JavaScript syntax: PASS
- app.js参照DOM ID: 20、欠落0、重複0
- Web projection内GitHub research path: 17/17をreview branchで解決確認
- Android実機visual review: 未実施
- Phase 4 exit review: 未作成
- Follow-up 2（canonical/Web同期CI）: 未着手

## 今回実施した確認

レビュー対象commitに対して実施:

- 40件の研究エンティティのYAML解析: 成功。
- `relations` に明示された参照先: 欠落なし。
- 調べたローカルMarkdownリンク15件: 参照先欠落なし。
- WebのJavaScript構文確認: 成功。
- DOMスタブによる描画実行: 成功、重複DOM IDなし。実ブラウザの視覚検証ではない。
- 公開HTML・JS・CSS: レビュー対象リポジトリの内容と一致。
- H3 outcomeの閲覧・計算、研究結果の変更、実装修正: 実施していない。

この確認結果は上記commitとレビュー時点に限定される。着手時の再検証を省略する根拠にはしない。
