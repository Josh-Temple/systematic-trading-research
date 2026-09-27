# Repository review follow-up — 2026-09-27

記録日: 2026-09-27 JST
状態: 完了（H3実装同一性、正本/Web整合性CI、Web根拠導線、公開状態更新を完了）
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
状態: 完了 — `DEC-HR-004` で実装参照をoutcome-blindに固定。H3自体は引き続き `WAITING_FOR_MATURITY`

監査記録: [H3_IMPLEMENTATION_IDENTITY_AUDIT_2026-09-28.md](../research/lines/horizontal-reaction-v0.1/H3_IMPLEMENTATION_IDENTITY_AUDIT_2026-09-28.md)

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

### 完了条件

- 別の実装者が、参照資料・コードの識別情報から同じ規則を確認できる。
- 確定条件と未解決条件が分離されている。
- H3実行に必要な未解決条件が残る場合、実行準備完了とはしない。
- H3の60 eligible sessionsのfreezeとsource gate PASS前に、touch outcome、群間比較、primary contrast、bootstrapを計算・閲覧していない。

この作業一覧はH3の実行許可を与えない。実行可否は着手時の正本と既存gateで確認する。

### 2026-09-28 fresh audit update

- Drive上の exact `run_v01.py` を回収し、SHA-256 `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd` を確認した。
- 2026-09-23 SHA manifest の `H2_frozen_touch_generator_run_v01.py` と同一hashで、H2 frozen replayがこのgeneratorを読み込んでいたことを確認した。
- touch / reset / confirmation / D4-H2 quote-side conventionはコードから再構成できた。
- 一方、legacy Gamma実装はcandidate barのClose変化を含む累積値を使い、H2では同じminute内のtouch tickを後から探索している。凍結文言「candidate minuteより前の観測だけ」とのtemporal-information mismatchがある。
- Gammaは全履歴prefixに依存するため、現行source-preparation handoffの「60-bar warm-up」だけではlegacy generatorを再現できない。
- legacy codeのsame-confirmation-bar ambiguityを、H3の二値 CONFIRMED / UNCONFIRMED のどちらへ写像するかも既存H3文書では未確定。
- 以上を結果前に解消するまで、H3 outcome実行準備完了とはしない。
- この監査ではDATA-HR-003 outcome、群間比較、primary contrast、bootstrapを閲覧・計算していない。

### 2026-09-28 implementation-resolution update

- 新規Decision `DEC-HR-004` で、H3が参照する実装を exact legacy H2 generator に固定した。対象は `run_v01.py` SHA-256 `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`。
- Gammaのstrict-before proseとlegacy codeの不一致は訂正して消していない。H3 v0.1では「exact H2 generatorを無変更で使用する」という凍結済み参照を優先し、candidate-bar Close変化を含むlegacy Gammaをそのまま使う。将来結果の解釈ではtemporal-information limitationを明示する。
- generator historyは、2025-12-31から2026-07-09までのexact H2 135-file inputを固定prefixとし、その後のfirst-party BID M1 sourceをcandidate scan順にselected-session filtering前で時系列追加する。2026-07-10でGamma履歴をresetしない。
- same-confirmation-barでは、元コードがconfirmation成立後にclean execution-event listから除外していることと、H3がexecution statusに依存せずconfirmation ruleで二値分類することを分離した。機械的confirmation条件を満たしたtouchは、同一barで別touchもconfirmしていてもH3では `CONFIRMED` とする。
- 上記はDATA-HR-003 outcomeを見ずに固定した。H3 outcome、CONFIRMED/UNCONFIRMED比較、primary contrast、bootstrapは未閲覧・未計算。
- したがって「実装条件の未解決」は解消したが、60 structurally eligible sessionsの成熟とsource gate PASSは別の既存gateとして残る。これらを満たすまでH3 runは作成しない。


## 2. 正本とWeb表示の整合性を最小限のCIで確認する

優先度: 中
状態: 完了 — PR #16でfail-closed consistency CIを実装し、Actions run `36334117643` がSUCCESS

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

### 2026-09-28 implementation update

- `.github/scripts/validate-research-consistency.mjs` と `.github/workflows/research-consistency.yml` を追加した。
- Horizontal Reactionの構造化recordをYAML/frontmatterとして解析し、stable ID重複、structured ID参照切れ、Resultの `execution_status` / `evidence_validity` / `scientific_status` の独立性を検査する。
- H1/H2/H3の主要状態・headline metrics、DATA-HR-001〜003の利用境界、H1 `SOURCE CONFLICT`、blocked Resultの `BLOCKED + NOT_APPLICABLE` をWeb projectionと照合する。
- Web内のrepository-local canonical linkとtimeline ID→record path対応を検査する。
- Web projectionへ `meta.canonicalSourceCommit` を追加し、公開画面のauthority sectionにも表示する。現在のprojection sourceは `78a3f335a6c66bcfda605f53435d3ec72cde0743`。
- `canonicalSourceCommit` より後に `research/lines/horizontal-reaction-v0.1/` が変更されている場合、Webを更新するまでCIはfailする。正本変更とderived Web同期は二段階で行う手順を `docs/WEB_UI_V0.1.md` に明記した。
- deliberate H1 trade-count mismatchと存在しないcanonical linkをメモリ上で注入するnegative self-testを組み込み、検出できなければCI自体を失敗させる。
- PR #16の初回Actions run `36334117643` はSUCCESS。したがって、正しい現在状態がPASSすることと、上記2種類の意図的な不一致が検出されることを同一runで確認した。
- このCIは科学計算を再実行しない。CI PASSをscientific validity、result recomputation、H3実行許可とは扱わない。

## 3. Webの根拠への導線を完成させる

優先度: 中
状態: 完了 — PR #13で根拠導線を実装し、public mobile validationで操作確認済み

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

### 2026-09-28 implementation update

- PR #13 で上部リンクの表記を `Canonical` から `Current summary` に変更し、CURRENTがderived projectionである境界と整合させた。
- H1 diagnosticsから `INT-HR-002` と `RES-HR-005` へ直接移動できるリンクを追加した。
- timelineのrecord IDを各Specification / Result / Decisionへの直接リンクへ変更し、複数recordの行も個別リンクにした。
- `DEC-HR-004` をWeb projectionへ同期した。
- Actions run `36333283755` で360 / 390 / 412px幅のpublic mobile Chromium validationを実行し、current-summaryのtap、diagnostic links、timeline links、状態区別、overflowを確認した。
- 物理Android端末では未確認である。この限界は `web/VALIDATION.md` とPhase 4 exit reviewへ明記した。

## 4. READMEと公開・検証状態を更新する

優先度: 低（短時間で対応可能）
状態: 完了 — README / ROADMAP / VALIDATIONを現在の公開・mobile validation・Phase 4 exit状態へ更新

### 確認した事実

- [README](../README.md)のCurrent stageはPhase 0のまま。
- [ROADMAP](ROADMAP.md)と[web/VALIDATION.md](../web/VALIDATION.md)には初回公開待ちの記録が残る。
- レビュー時点では[Actions run 36316165611](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36316165611)の成功と、公開ファイルの取得・リポジトリとの一致を確認した。

### 作業と完了条件

- 着手時のActions・公開状態を再確認する。
- READMEから現在の段階、公開URL、現在の研究要約、この作業一覧へ辿れるようにする。
- 過去の公開失敗は履歴として保持し、その後の成功を追記する。
- 公開成功と、Android視覚確認・Phase 4 exit review完了を区別する。未実施の確認を完了扱いにしない。

### 2026-09-28 update

- Actions run 36316165611 をfresh readし、deploy jobと Checkout / Configure Pages / Upload static site / Deploy がすべて success であることを再確認した。
- READMEのCurrent stageをPhase 0表記から現在のPhase 0–3 COMPLETE / Phase 4 IN PROGRESSへ更新した。
- ROADMAPとweb/VALIDATIONへ初回公開成功とpublic URLを反映した。
- 過去のPages作成失敗は履歴として残した。
- 公開成功とAndroid/mobile視覚確認を分離し、Phase 4は閉じていない。
- このセッションの直接Web取得機能ではpublic URLを開けなかったため、この時点では新しい視覚確認を実施済みとは記録していない。

### 2026-09-28 later update

- PR #13 のWeb同期後、Pages run `36333169298` が成功した。
- PR #14 でpublic mobile validationを追加し、run `36333283755` が成功した。
- 360 / 390 / 412pxのChromium mobile renderingについて、overflow、状態区別、リンク操作を機械確認し、生成スクリーンショットも目視確認した。
- `web/PHASE4_EXIT_REVIEW.md` でPhase 4 v0.1をPASSとして閉じる。物理Android端末を別途実行していない点は限界として保持する。

## 保持すべき良い点・既知の限界

- 仮説・仕様・実験・実行・結果・解釈・判断が分離されている。
- blocked executionとnegative scientific result、exploratoryとconfirmatory、consumedとunusedが区別されている。
- H1 D1-D5の資料間不一致は[RES-HR-005](../research/lines/horizontal-reaction-v0.1/results/RES-HR-005.md)に保存され、CURRENTとWebでも明示されている。今回その不一致を解決したとはしていない。
- Phase 3の「GitHubから再構成できる」は研究状態・経緯についての評価であり、同じ計算を再実行できることの証明ではない。
- MCP、研究ライン拡大、自動研究の拡大より前に、上記の実行仕様・整合性維持を補強することを推奨する。これはレビュー上の提案であり、既存roadmapや研究権限を上書きしない。

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
