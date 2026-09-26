# Prior Repository Review — Epsilon Quant Research

## Metadata

- Repository: `Epsilon-Fund/Epsilon-Quant-Research`
- URL: https://github.com/Epsilon-Fund/Epsilon-Quant-Research
- Review date: 2026-09-27
- Reviewed default branch: `main`
- Reviewed head observed: `e40d6b64b92c31c18c1b4a4903b872d913adfefb`
- Repository created: 2026-02-18
- Visible commit history: 251 commits returned by the GitHub commits API, from 2026-02-19 through 2026-09-09
- Repository purpose: systematic crypto trading researchとPolymarket research / executionを同一repositoryで運用し、Git-tracked Markdown knowledge brain、strategy hubs、data manifests、research findings、deterministic research code、handoff filesを組み合わせて研究を継続する
- Maturity / activity notes: repository全体は約7か月の履歴があり、knowledge-brain architectureは2026-06-05以降約3か月の運用・再設計履歴を確認できる。複数collaborator、Mac/Windows、複数agent role、large data layerを実際に扱った痕跡がある。
- Review status: **PARTIAL**

### Repository identification

#### Fact

GitHubで `Epsilon Quant Research` をfresh searchしたところ、主要候補は2件だった。

1. `Epsilon-Fund/Epsilon-Quant-Research` — `fork: false`
2. `Gonzalo-GallegoToscano/Epsilon-Quant-Research` — `fork: true`

後者のGitHub metadataはparent/sourceを `Epsilon-Fund/Epsilon-Quant-Research` と明示する。

#### Interpretation

今回の対象は推測ではなく、source repositoryである `Epsilon-Fund/Epsilon-Quant-Research` と特定できる。

#### Limitation

public repositoryだけを対象としており、READMEが明示するprivate deployment parameter / proprietary edge materialは確認対象外。

## 1. What problem is this repository solving?

### Fact

初期commit `3ed0f1459b020afadebb4b604dc335bf55f7728b`（2026-02-19）は、

- `infrastructure/data`
- `infrastructure/backtester`
- `topics/`
- newsletters
- meetings
- templates

という比較的通常のresearch-folder + backtesting infrastructureから始まっている。

その後、研究テーマとagent workが増え、2026-06-05以降に `brain/` というGit-tracked Obsidian knowledge layerが追加された。現在の `brain/VAULT_MAP.md` は自らを “the single start-here surface for humans and agents” と定義し、repository全体を直接scanする代わりに、hub、current task list、strategy map、data manifestへ段階的にnavigateする方式を採る。

現在のrepositoryは大きく、

- Polymarket research / execution
- crypto systematic research / live trading
- shared knowledge / agent control plane

を同じrepositoryに持つが、Polymarketとcryptoはruntime / dependency / code importを分離する。

### Interpretation

このrepositoryの後期設計が解こうとしている問題は、単なる「quant code整理」ではない。

研究量が増えると発生する、

- どのresearch branchが現在activeなのか分からない
- old findingとcurrent conclusionが混ざる
- dataset / outputが増えすぎてraw folderから探せない
- agentが過去研究を再発見できない
- note名重複、orphan、broken link、stale TODOが増える
- 複数collaborator / agentの同期方式自体が壊れる
- handoffでcurrent stateとhistoryが混ざる

というknowledge-maintenance問題を、Git、Markdown hubs、wikilink graph、generated hygiene reports、local retrieval layerで解こうとしている。

### Limitation

repositoryは研究管理専用systemではなく、research code、execution code、live trading、knowledge docs、data toolingを含むmonorepoである。そのため「研究知識schema」だけを独立製品として評価することはできない。

## 2. Canonical source of truth

### Fact

単一の万能source-of-truth fileではなく、役割別のcanonical surfaceが明示されている。

現在の主なprecedenceは以下。

- `brain/VAULT_MAP.md`
  - human / agentのsingle start-here surface
  - Agent Bootstrapのcanonical copy
  - where-to-write tableのcanonical copy
  - active research branchへのrouting
- `brain/TODO.md`
  - “AUTHORITATIVE live task list”
  - 2026-08-25にone active threadへrewrite
  - old task historyは `TODO_ARCHIVE.md` へ分離
- `brain/POLYMARKET_BRAIN.md`
  - Polymarketのcurrent active / deprioritised / parked map
- `polymarket/research/notes/market_making/strat_market_making.md` → `mm_model.md`
  - current active Polymarket strategyのcanon surface
- `brain/handoff/STATUS.md`
  - data-layer handoff loopのcurrent one-screen status
- data manifests
  - `polymarket_data_manifest.md`
  - `docs/CRYPTO_DATA_MANIFEST.md`
- `polymarket/research/epsilon_data/`
  - `research_v1` dataへのcanonical programmatic access layer。READMEはdashboard / notebook / analysisがraw Parquet pathを直接読まず、このloaderを通ることを要求する。

historical recordは削除せず別層に置く。

- findings notes
- `TODO_ARCHIVE.md`
- dated `brain/handoffs/*.md`
- `brain/handoff/LOG.md` / reports
- `polymarket/archive/`
- Git history

generated navigationは `brain/generated/` に置かれるがgit-ignoredで、`tools/brain_hygiene.py` / `brain_graph_audit.py` から再生成される。`VAULT_MAP.md` はこれをnon-durable generated layerとし、自身をdurable mapと位置づける。

gbrainもsource of recordではない。`docs/tooling/gbrain_retrieval_layer.md` はMarkdown + hubs + wikilinksをsole source of recordとし、gbrain indexをdisposable local read-only layerと明示する。

### Interpretation

Epsilonの設計は「canonical databaseを一つ持つ」方式ではなく、**canonical routing surfacesを少数に絞り、詳細history / evidenceを下位layerに残す**方式である。

研究数が増えたときの答えは、

`current orientation → current tasks → strategy canon → findings/history → raw evidence`

というread pathに近い。

これはfolder treeそのものを正本にする設計ではない。

### Limitation

canonicalityはprotocol / documentationで強制されており、全surfaceが一つのmachine-readable stateから自動生成されるわけではない。

実際、2026-06-10 auditでは、

- `TODO.md` frontmatterが `status: closed` のまま
- stale path
- COWORK / TODOに古いstrategy primacyの説明
- completed capture taskがuncheckedのまま

というdriftが確認されている。

したがって「canonical surfaceを置く」だけではdriftを消せず、定期auditを必要としている。

## 3. Current repository structure

### Fact

reviewed headのrecursive treeは1,820 entriesで、主要構造は以下。

```text
brain/
  VAULT_MAP.md
  TODO.md
  TODO_ARCHIVE.md
  POLYMARKET_BRAIN.md
  CODEX.md
  COWORK.md
  ONBOARDING.md
  MERGE_PROTOCOL.md
  START_RESEARCH_IDEA.md
  OPERATING_RHYTHMS.md
  OBSIDIAN_INFRA_ROADMAP.md
  SKILL_MAP.md
  handoff/
    PROTOCOL.md
    NEXT.md
    STATUS.md
    LOG.md
    reports/
  handoffs/
    YYYY-MM-DD_*.md
  agents/

polymarket/
  research/
    notes/
      overview/
        synthesis/
        foundations/
        data_quality/
        market_maps/
      market_making/
      options_delta/
      copytrade/
      dali/
      news_agent/
    epsilon_data/
    dashboard/
    notebooks/
    mm_engine/
    mm_eval/
    scripts/
    tests/
    data/
    data_layer/
  execution/
  midas/
  archive/

topics/
  momentum/
  statistical-arbitrage/
  long-short/
  memecoin-defi/
  ml-prediction/
  regime/

infrastructure/
  backtester/
  walkforward/
  validation/
  data/
  data/l2_ingestion/
  ...

docs/
  STRATEGY_REFERENCE.md
  CRYPTO_DATA_MANIFEST.md
  tooling/

tools/
  brain_hygiene.py
  brain_graph_audit.py
  brain_commit_push.sh
  sherpa.py
  wip_audit.py
```

### Fact — navigation structure

Polymarket notesは単純なflat folderではない。

- strategy branch別folder
- cross-branch synthesis
- foundations
- data quality
- market maps
- strategy hub
- global Polymarket map
- global Vault Map

という複数levelのnavigationを持つ。

### Interpretation

研究量が増えた後、folder hierarchyだけでは不十分と判断し、

- domain folder
- hub graph
- status metadata
- generated structural audit
- semantic retrieval

を重ねる構造へ発展したと読める。

### Limitation

hierarchyとgraphの両方を持つため、理解すべきnavigation concept自体は増えている。VAULT_MAPが無ければstructureはかなり複雑であり、bootstrapへの依存が高い。

## 4. Knowledge / data model

### Fact — Markdown knowledge model

durable notesはYAML frontmatterとwikilinkを使う。

確認できた典型field:

- `title`
- `created`
- `updated`
- `status`
- `owner`
- `project`
- `para`
- `hubs`
- `tags`

relationは主として `[[wikilink]]` で表現される。

strategy hubはcurrent interpretationをまとめ、detail findings notesをevidenceとしてlinkする。

2026-07-19 canon auditでは62件のpre-Alvaro Polymarket notesを、

- 16 CANON
- 17 CLOSED-ROBUST
- 29 HISTORICAL
- 0 DEMOTED

へ分類し、各noteにstatus bannerとfrontmatterを追加した。

2026-07-21 adversarial audit後、このledger自身にも “SUPERSEDED IN PART” bannerを追加し、後続auditへのlinkを置いた。

### Fact — research lifecycle metadata

`START_RESEARCH_IDEA.md` はnew ideaに対して、

- plain-English thesis
- why now
- target data
- expected mechanism
- cheapest falsifier
- success / failure gate
- durable output location

を含むidea cardを要求する。

test前には、

- primary metric
- sample
- leakage guard
- CI / uncertainty
- cost assumptions
- close criterion

をpre-registerする。

hyperparameter searchを使うstrategyはlive前にtrial-level dataを保持し、Deflated Sharpe Ratio、PBO / CSCV、White’s Reality Checkを通すことを要求する。

### Fact — dataset model

Polymarket dataはfamily-level manifestで管理される。

`polymarket_data_manifest.md` はraw seed、append-only delta shards、market snapshots、closed positions、cohorts、directionality、analysis feature panels、backtest outputs等を「dataset family」として記録し、main readersとknown trust stateを示す。

2026-07-21 auditで不正確と判定された `closed_positions.parquet` やdirectionality datasetは、削除せずmanifest上に `CONDEMNED` statusとreason linkを持つ。

`research_v1` は別のdata productとして、

`universe → event → market → token`

のidentity tree、L1 tape、trades、coverage等を持つ。human / analysis accessは `epsilon_data` loader経由に固定する。

### Fact — experiment / result model

experiment resultは統一database entityではなく、主として、

- scripts / notebooks
- CSV / Parquet / pickle
- `*_findings.md`
- strategy hub
- handoff / decision note

で結ばれる。

crypto walk-forward engineはfold records、best parameters、consensus parameters、stability dataframe、stitched OOS dataframe、OOS metrics等をstructured returnとして持ち、一部をCSV / pickleにpersistする。

### Interpretation

Epsilonはformalな

`Hypothesis → Experiment → Result → Interpretation → Decision`

database schemaを持たない。

代わりに、

- structured Markdown metadata
- wikilink relation
- naming convention
- filesystem placement
- data manifests
- deterministic artifacts

を組み合わせたlightweight knowledge graphとして機能している。

### Limitation

「あるhypothesisに紐づく全experiment」「あるdatasetを使った全result」「あるdecisionを無効化したresult」をmachine queryだけで完全に復元するforeign-key schemaは確認できない。

relationの一部はproseとlink disciplineに依存する。

## 5. Research lifecycle

### Fact

`START_RESEARCH_IDEA.md` から確認できるcurrent intended lifecycle:

1. ideaをPolymarket / crypto / cross-project / infraへclassify
2. existing hubs / findings / gbrainでprior workを検索
3. local scratch / chatでdraft
4. idea card作成
5. metric / sample / leakage / cost / close criterionをpre-register
6. parameter searchならoverfitting audit planを固定
7. implementation agentがcode / notebook / data query / chart / findingsを実行
8. durable editはpersonal Git branchへ
9. final resultをproper findings folderへpromote
10. active branchならTODO / hubを更新、cross-thread decisionならdated handoffを作る

### Fact — role boundary

- Cowork: strategic framing、prompt drafting、interpretation、brain maintenance
- Codex / Claude Code implementation role: code、analysis、data query、test、findings output

current lawは、code-like researchをorchestration agentが代替しないよう分離する。

### Fact — continuation

data-layerではさらに明示的なfile-based continuation protocolがある。

- `NEXT.md` — current instruction
- `STATUS.md` — current state、毎step overwrite
- `LOG.md` — append-only chronological record
- `reports/<step>.md` — full result
- Cowork reads result and writes next instruction

verification failure、unexpected result、scope外action等はstop conditionであり、surpriseもresultとしてLOG / STATUSへ残す。

### Interpretation

研究continuationはchat memoryよりrepository fileを優先する方向へ進んでいる。

特にcurrent stateとhistoryを別file behaviorで表している点は明確。

### Limitation

全research branchが同じstrict handoff protocolを使うわけではない。`brain/handoff/` protocolはdata-layer projectで明示的だが、他branchはdated handoffs + hubs + TODOに依存する。

## 6. Experiment reproducibility

### Fact

再現性に寄与する仕組みとして以下を確認した。

- Git commit history
- deterministic Python research code
- tests
- explicit random seeds in walk-forward / Optuna flow
- CPCV / walk-forward infrastructure
- pre-registered metrics / close criteria
- overfitting audit requiring trial accounting
- append-only Parquet rule for Polymarket delta data
- data manifests
- `research/v1` versioned dataset concept
- loader anti-drift tests
- `_manifest.json` accompanying published data product
- `_fetch_receipt.json` after download verification
- handoff reports that identify steps and outputs
- replay engine determinism as a stated and tested current market-making invariant

`research_v1` onboarding also distinguishes raw archive from human-facing derived library, and explicitly states that the L1 library cannot substitute for full depth required by the queue-position backtester.

### Fact — failures in reproducibility

PR #4 identified that a generic `.gitignore` rule `lib/` silently excluded the real `polymarket/research/lib/` source package. It existed locally but not in clones, causing `ModuleNotFoundError` and breaking research/backtest components. The current reviewed tree does contain the package, but the PR documents the failure mode.

Open PR #5 is an independent audit of `research_v1` against `alvaro @ 9810c2b`. It reports:

- fresh oracle checks supported the token mapping on sampled cases
- however, code that generated the five verification columns was not committed in the audited state
- one check definition was undocumented / unclear
- one verification column covered only a small subset
- a “pair sums to 1” check was algebraically guaranteed rather than independent evidence
- L1 dedup reset at part boundaries introduced 195,984 rows, about 0.19% of L1, that were not actual touch moves
- some documentation evidence overstated what shipped tests proved

PR #5 remains open and is not part of reviewed main; these findings are evidence about the audited branch/state, not automatically a statement that every defect remains in current main.

### Interpretation

Epsilon has substantial reproducibility infrastructure, but it also shows a useful distinction:

**reproducible analysis code is not sufficient if the build code or provenance chain for a derived dataset is missing.**

The later design increasingly treats dataset construction and auditability as first-class.

### Limitation

repository-wide、uniformなper-experiment manifest combining

- dataset hash
- code commit
- exact config
- package environment
- output hashes
- result status

を必須化する仕組みは確認できない。

zestoles/quantのようなevery-output provenance sidecar型ではなく、Epsilonはsubprojectごとに再現性mechanismが異なる。

## 7. Negative / failed research

### Fact

negative researchは大量に残されている。

current `POLYMARKET_BRAIN.md` は、

- earlier market-making eras
- valuation / fair-value overlay
- microstructure signal lineage

をPARKED historical recordとして明示し、active workでbuild onしないよう要求する。

`mm_model.md` もtested-and-rejected additionsを残し、「誰かが後で再導入しない」ことを理由として記録する。

2026-07-19 canon auditは古いnotesをCANON / CLOSED-ROBUST / HISTORICALへ分類した。

2026-07-21 pipeline trust auditでは、

- earlier OOS-collapse claimの一部がmetric mismatchだったことを訂正
- derived position / trader / directionality artifactsをcondemn
- A17 calibration evidenceをcondemn
- それでもstrategy closure自体は別根拠で維持

した。

つまり「過去のnegative conclusionを守るために誤った根拠を温存する」のではなく、supporting evidenceが誤りなら訂正し、decisionが別根拠で残るかを再評価している。

### Interpretation

negative resultは単なるarchiveではなく、

- CLOSED-ROBUST
- HISTORICAL
- PARKED
- CONDEMNED dataset/evidence

のように「なぜ現在使わないか」を可視化する方向へ進んでいる。

### Limitation

これらstatusは統一enum schemaではない。note banner、frontmatter、manifest prose、hub proseに分散するため、全failure stateを機械的にenumerateするには追加normalizationが必要。

## 8. Current knowledge vs history

### Fact

Epsilonでもcurrent stateとhistoryの分離は独立に、かつ明示的に存在する。

現在の構造:

- current active map: `VAULT_MAP` / `POLYMARKET_BRAIN`
- current live tasks: `TODO`
- current strategy canon: `strat_market_making` → `mm_model`
- historical tasks: `TODO_ARCHIVE`
- historical evidence: detailed findings notes with status banners
- cross-thread snapshots: dated handoffs
- archived implementation / strays: `archive/` / `polymarket/archive/`
- data-layer current status: overwritten `STATUS.md`
- data-layer history: append-style `LOG.md` + step reports

### Fact — this separation was introduced after drift

2026-06-10 commit `e788e34b444ae076797aea4e37c17ae5323fceb0` explicitly removed dated status prose from `CODEX.md` / `COWORK.md` and replaced it with pointers to `TODO` and `VAULT_MAP`. The stated reason was to keep law files timeless.

2026-08-25 rewrite reduced active research to one thread and moved pre-handoff tasks into `TODO_ARCHIVE`.

### Interpretation

これは最初からのarchitectureではなく、**status driftを経験した後のdesign response** である。

既存2 reviewと同じ方向性は確認できるが、Epsilon固有の特徴は「current vs history」を単一current fileではなく、routing map + task list + strategy canon + status bannersの多層構造で実現している点。

### Limitation

current stateのsourceはdomainごとに複数あるため、precedenceを読まないagentは誤る可能性がある。

実際 `TODO.md` のdata-layer section自身が「checkbox stateは古い。`STATUS.md` をtrust」と注意している。

current-state projectionは完全自動生成ではない。

## 9. AI / agent role

### Fact

AI / agent integrationはknowledge systemの中心にある。

roles:

- implementation agent: Codex / Claude Code
- orchestration agent: Cowork

shared role lawとlocal personal overlayを分離する。

- shared: `brain/CODEX.md` / `brain/COWORK.md`
- local private: `local_agents/<role>.md`
- scratch: `scratch/<agent>/YYYY-MM-DD.md`

local overlayとscratchはgit-ignored。

agentはcanonical hubをscratchpadとして使わず、working materialからdurable findingsだけをpromoteする。

durable editsはpersonal Git branchで行い、mainへのintegrationは `MERGE_PROTOCOL.md` に従う。

semantic conflictではagentが勝手に平均・選択せず、両versionを残してhuman decision flagを出す。

### Fact — retrieval

gbrainはlocal read-only semantic / graph indexとしてMCP接続される。

提供機能:

- semantic search
- graph traversal
- backlinks

Markdown / wikilink sourceはcanonicalのままで、gbrain databaseはdisposable。

cloud synthesisは意図的に無効化され、local embeddingだけを使う。retrieved evidenceのsynthesisはagent側。

### Interpretation

AI integrationは「AIがknowledge databaseそのもの」ではない。

AIは、

- mapからcontextを取得
- local retrievalでprior workを探す
- research questionをframe
- deterministic codeを実行 / 依頼
- findingsをhuman-readable noteへpromote

する。

canonical stateはGit-tracked source側に残す。

### Limitation

AI read/write permissionをentity単位でenforceするdatabase ACLや、research-status transitionをAPIで制約するworkflow engineは確認できない。guardrailはGit branch / merge protocol / conventions中心。

## 10. Deterministic execution boundary

### Fact

deterministic codeへ委ねられているもの:

- backtesting
- walk-forward
- CPCV
- performance metrics
- overfitting audit
- data loading / transformation
- replay
- capture-quality gate
- dashboard computations
- graph / hygiene scan
- data fetch verification

research idea framing、interpretation、priority、semantic merge judgmentはhuman / orchestration側。

Polymarket current market-making hubはreplay determinismをtrustworthy layerとする一方、unmeasured fill / queue modelやinstant-latency assumptionはpreliminaryと明示する。

`audit_market()` はread-onlyで、exclusion writeは別のexplicit `write_exclusion()` に分離される。

brain hygiene toolsも “finds issues; does not fix them” を原則とする。

### Interpretation

Epsilonでは、

**retrieval / reasoning / orchestration**
と
**measurement / computation / data transformation**

の境界をかなり明示している。

さらに「deterministicだから正しい」とは扱わず、2026-07-21 trust auditやPR #5のようにmeasurement pipeline自体を再監査している。

### Limitation

repository全体で一つのexecution protocolがあるわけではない。subprojectごとのdeterministic boundaryを共有brainがnavigationしている構造。

## 11. Human-facing interface

### Fact

human-facing interfaceは複数層。

1. **GitHub Markdown**
   - README
   - VAULT_MAP
   - TODO
   - strategy hubs
   - findings
   - handoffs

2. **Obsidian**
   - wikilink graph
   - backlinks
   - graph presets
   - hub navigation

3. **Generated Markdown reports**
   - GENERATED_INDEX
   - hygiene report
   - stale notes
   - graph audit

4. **Polymarket Streamlit research terminal**
   - search
   - Explore / Audit panels
   - research_v1 browsing

5. **notebooks**
   - worked analysis / cookbook

6. **CLI / scripts**
   - check setup
   - fetch data
   - audits
   - deterministic analyses

### Research navigation assessment

「この仮説について過去に何を試したか」

- gbrain semantic search / backlinks
- strategy hub → historical findings
- canon audit ledger
- Git history

「現在どの研究がactiveか」

- VAULT_MAP
- TODO
- POLYMARKET_BRAIN
- current strategy hub

「どのdatasetを使ったか」

- data manifest
- findings note
- dataset-specific README / loader

「何が失敗済みか」

- PARKED / HISTORICAL / CLOSED banners
- canon audit ledger
- strategy hub rejected-addition section
- archived notes

で比較的短いread pathが存在する。

### Interpretation

現在状態では、単なるfolder整理より明確に上のnavigation systemが存在する。

特に、「rootから全部読む」のではなく「start surface → project hub → strategy hub → evidence」に絞ることが設計目的。

### Limitation

human navigation品質はlink disciplineに依存する。

2026-06-07 scannerのinitial stateでは、

- 216 files
- 3 duplicate basenames
- 1 broken link
- 1 orphan
- 27 findings missing hub backlink
- 146 missing frontmatter
- 114 findings without Summary

が検出された。

自動scannerとJanitor passで修復されたため、現在のnavigationは「自然に保たれた」のではなく継続maintenanceの成果。

## 12. AI-facing retrieval

### Fact

AI-facing retrievalとして最も明確なのはgbrain MCP。

- local semantic index
- wikilink graph
- search / traverse_graph / get_backlinks
- read-only against canonical Markdown
- index stored outside repo
- re-import required after large vault changes

agent instructionsは “find prior work on X” の場合、全hubを読むよりgbrainを優先する。

`tools/sherpa.py` はtask contextからrelevant skillをsurfaceする別のlocal routing tool。

### Generated index

`tools/brain_hygiene.py` は、

- duplicate basename
- broken link
- orphan
- missing hub backlink
- missing frontmatter
- missing Summary
- stale TODO
- recently changed files

をscanし、`brain/generated/GENERATED_INDEX.md` 等を生成する。

`brain_graph_audit.py` は、

- authorities
- index hubs
- over-connected notes
- orphans
- dead ends
- topic islands
- components

を検出する。

generated outputsはgit-ignoredで、canonical contentを自動書換えしない。

### Interpretation

AI retrievalは「大量contextを毎回読む」方式から、

- durable compact maps
- local generated index
- semantic search
- graph traversal

へ進んでいる。

### Limitation

gbrain indexは自動continuous syncではなく、vault変更後にre-importが必要。

したがってindex freshnessはoperationに依存する。

また、formal `search_experiments(status=REJECTED, dataset=X)` のようなtyped research APIはない。

## 13. Issues / discussions findings

### Fact

fresh API readでは、standalone GitHub Issuesは確認できなかった。`/issues` に返った5件はすべてPull Requestだった。

GitHub Discussionsはrepository settingでdisabled。

Pull Requests:

- #1 / #2 / #3 — generic collaborator merges、merged
- #4 — `fix(gitignore): track the research lib/ package (anchor /lib/)`、open
- #5 — `research_v1 audit: findings + mechanical fixes`、open

### PR #4 — source package silently absent from Git

#### Fact

generic Python `.gitignore` のunanchored `lib/` がnested source package `polymarket/research/lib/` までmatchし、local machineには存在するのにGit cloneには存在しない状態を作った。

cloneした利用者はbacktest / MM codeのimport failureを起こす。

reviewed current treeには `polymarket/research/lib/` が存在するが、PR #4自体はopenのまま。

#### Interpretation

「working local machine = reproducible repository」ではないことを示す具体例。

### PR #5 — research_v1 independent audit

#### Fact

audited branch/stateに対して、data mapping自体はfresh sampleで良好だった一方、

- verification build codeの欠落
- verification columnの意味 / coverage不足
- circular / weak verification
- part-boundary L1 dedup defect
- doc / code contradiction

が指摘された。

#### Interpretation

human-facing “verified dataset” storyと、machine-reproducible evidenceがdriftし得ることを示す。

### Limitation

Issue discussionを通じた長期design debateはない。design rationaleの多くはcommit message、handoff、findings noteに記録されている。

## 14. Commit-history findings

以下は完成形ではなく、設計が変わった理由を追える主要commit。

### 1. `3ed0f1459b020afadebb4b604dc335bf55f7728b` — 2026-02-19
**Add complete repository structure and backtesting infrastructure**

#### Before / problem

initial repository foundation。

#### After / design

- topic-based research folders
- shared backtester
- data infrastructure
- newsletters / meetings

を作成。

#### Significance

現在も `topics/` / `infrastructure/` は残っており、domain folder + shared deterministic toolingは初期から残った長寿命の設計。

---

### 2. `ef24478e3019626bbd9a7f3c77139e5c4827463a` — 2026-06-05
**Add shared Obsidian brain onboarding**

#### Before / problem

research notes / handoffsは存在したが、shared orientation layerが弱い。

#### After / design

- CODEX
- COWORK
- POLYMARKET_BRAIN
- TODO
- glossary
- dated handoffs

を `brain/` へ導入。

---

### 3. `151ee04133c81025ba9217a596277680032a5d07` / `9031a2e5610b7db9dc20fe22e2e2eb540018632c` — 2026-06-07
**brain hygiene cleanup / Obsidian infrastructure**

#### Before / problem

scannerのinitial state:

- 216 files
- duplicate basenames 3
- broken link 1
- orphan 1
- missing hub 27
- missing frontmatter 146
- missing summary 114

flat notes / generated artifacts / duplicate filenamesも存在。

#### After / design

- strategy-folder split
- overview subfolders
- hub backlinks
- unique basenames
- YAML metadata
- Summary requirement
- hygiene scanner
- graph audit
- generated index
- VAULT_MAP

を導入 / 強化。

---

### 4. `e788e34b444ae076797aea4e37c17ae5323fceb0` — 2026-06-10
**Retire Obsidian Relay; install git branch-per-person collaboration model**

#### Before / problem

Obsidian Relay live syncがcollaborator側で壊れ、CRDT syncにedit locksとper-machine configurationが必要だった。

またAgent Bootstrap / where-to-write / dated statusが複数fileに重複していた。

#### After / design

- Relayを廃止
- personal Git branch per collaborator
- mainはdeliberate integration branch
- edit-lock mechanism retirement
- Agent BootstrapをVAULT_MAPへ一本化
- where-to-write tableをVAULT_MAPへ一本化
- law filesからdated statusを除去
- local scratch / overlayをgitignore

#### Significance

large-scale collaboration designを「more coordination machinery」ではなくGitへ簡素化した明確なrollback / simplification。

---

### 5. `4f41307e14265228eccf6e60bfe6b10a4740680b` — 2026-06-18
**cross-platform CRLF safeguards + daily canon check**

#### Before / problem

Mac / Windows間でline endingだけが異なる約178 filesがphantom mega-mergeを作る状態が発生。

#### After / design

- `.gitattributes` LF canonicalization
- daily canon check
- merge.renormalize guidance
- staged CRLF guard
- bootstrapへcanon syncを追加

#### Significance

knowledge repoではtext storage format自体もcollaboration scalability問題になる実例。

---

### 6. `f4c6b6893415d2def4612105c71c9dd1a027d375` — 2026-07-19
**pre-Alvaro canon audit**

#### Before / problem

62件のold Polymarket notesが同じvisibilityで存在し、current / closed / historicalの区別が弱い。

#### After / design

全62 noteを、

- CANON
- CLOSED-ROBUST
- HISTORICAL
- DEMOTED

でauditし、status bannerとnormalized frontmatterを追加。ledgerをhubからlink。

---

### 7. `0c71650630b0e02c92e4478d0c1f33cc89e64b3e` — 2026-07-21
**pipeline trust audit — corrected results, condemned artifacts**

#### Before / problem

canon classificationだけではunderlying evidence validityを保証できなかった。

具体的に、

- OOS collapse claimのmetric mismatch
- sign fixがderived dataへ未反映
- aggressor double count
- phantom complementary-token positions
- regime confound

が見つかった。

#### After / design

- wrong numerical storyを訂正
- suspect derived tablesをCONDEMNED
- dependent notesにbanner
- closureを別のrobust evidenceで再評価
- “correct or condemn” をaudit standardへ

#### Significance

navigation / status整理とscientific validity auditは別問題であることを示す。

---

### 8. `ef16fabc5d0728ee83105441fdda13dad5923f75` — 2026-07-21
**reorg(polymarket): one PM root**

#### Before / problem

Polymarket related workが、

- root `midas/`
- `topics/prediction-markets/`
- `polymarket/sports-arb/`
- root/archive material
- duplicated notebook/data working trees

へ散在。

#### After / design

- Polymarket workを `polymarket/` 下へ集約
- retired Falcon pipeline / sports-arbを `polymarket/archive/`
- Midasを `polymarket/midas/`
- empty canvases削除
- accidental duplicate data tree除去
- data manifest pointer追加

#### Significance

folder designも固定ではなく、研究量増大後にdomain root単位へ再編された。

---

### 9. `bd752c1654847fa754b00d6e3616c4d11684f108` + `29afd29895e5bafa1bcc8b8a6050b07290c4d24b` — 2026-07-21
**workflow revision + required capture-quality gate**

#### Before / problem

historical workflowに、

- wrong metric definition
- capture quality gate不足
- real bookがあるのにspreadを推定
- fix後にderived dataをregenerateしない
- findingsとrepro scriptsの分離

というrecurring defectがあった。

#### After / design

- close / fix / re-measure tier
- real L2がある場合はbookを直接読む
- capture-quality fail-closed gate
- findings + reproduction script discipline

を追加。

---

### 10. `3b862b3735b2cd7f20a66a20c0c2efe9b79fe93b` — 2026-08-26
**L2 pipeline quarantine-and-continue**

#### Before / problem

hard rebootで3 capture shardsがtruncateし、compression processが最初のbad shardで毎回crash。3日間Parquet / sync / pruneが停止しdisk 93%まで上昇。

#### After / design

- unreadable shardをquarantine
- other shardsはprocessing継続
- degraded non-zero exit
- salvage tool
- quarantine dedup / retry
- tests
- R2 rawからrecovery

#### Significance

large-scale data pipelineではfail-stop一辺倒も危険であり、corrupt unitを隔離しつつ全体progressを維持する設計へ変更。

---

### 11. `0a74c10df8f00c6c333693850adf9823fe93d95f` — 2026-08-30
**research_v1 panel registry / loader / handover**

#### Before / problem

71 GB raw captureはmachine向きだがhuman exploration / onboardingには重い。

#### After / design

- versioned research library
- one loader API
- Streamlit terminal
- plugin-like panel registry
- audit function
- read-only data fetch
- onboarding / handover
- data-root abstraction

を追加。

---

### 12. `a4ad608aacbb06b2c61ea52be0053f7dd3342bb9` — 2026-09-09
**data-layer handoff assets committed**

#### Before / problem

open PR #5がauditした2026-09-01 stateでは、HANDOVERが指すstep reports / LOGがrepositoryに存在しないという指摘があった。

#### After / design

- `brain/handoff/LOG.md`
- `NEXT.md`
- `PROTOCOL.md`
- `STATUS.md`
- step reports
- data-layer build scripts

をGitへ追加。

#### Interpretation

handoff historyがlocal / uncommittedである状態から、repository内durable continuation interfaceへ移った。

---

### 13. `e40d6b64b92c31c18c1b4a4903b872d913adfefb` — 2026-09-09
**reviewed head merge**

current market-making brain rewriteとdata-layer artifactsをintegration。

### Overall interpretation of history

最も重要なのは、現在のhub / graph / handoff systemが最初から存在したわけではないこと。

実際の順序は概ね、

`topic folders → shared brain → hygiene tooling → sync failure → Git branch model → canon/status audit → domain reorg → evidence trust audit → current/historical banners → data-layer handoff protocol`

である。

## 15. Failure cases / abandoned approaches

### 1. Obsidian Relay live synchronization

**Fact:** collaborator sync failureとcoordination overheadを理由に廃止。

**Replacement:** Git branch-per-person + deliberate merge。

### 2. Per-file edit locks

**Fact:** Relay eraのcoordination mechanismとして存在したが、branch isolation導入後に不要としてarchive。

### 3. Dated status in law / orientation files

**Fact:** CODEX / COWORKから除去し、TODO / VAULT_MAP / dated handoffへ移動。

**Reason:** timeless rulesとcurrent changing stateを混ぜるとstaleになる。

### 4. Flat / duplicate note layout

**Fact:** duplicate basenames、flat notes、orphan、missing hub linksがscannerで検出され、strategy folder / overview / hub schemeへ整理。

### 5. Overgrown live TODO

**Fact:** 2026-06 auditで433 lines / 約72.6 KBから367 lines / 約61 KBへpruneし、old done / falsification historyをarchive。2026-08にはone active threadへさらにrewrite。

### 6. Scattered Polymarket roots

**Fact:** Midas、prediction-market topic、sports-arb等をone `polymarket/` root + archiveへ再編。

### 7. “classified = trustworthy” assumption

**Fact:** July canon classification後のadversarial auditでunderlying metrics / derived datasetsに問題が見つかった。

**Replacement:** correct-or-condemn、capture-quality gate、re-measure rules。

### 8. Pipeline abort on first corrupted shard

**Fact:** reboot corruptionで3-day downstream stall。

**Replacement:** quarantine-and-continue + explicit degraded failure + salvage。

### 9. Local-only source package

**Fact:** `.gitignore` ruleによりcloneにsource packageが欠落。

**Lesson:** reproducibilityにはworking treeだけでなくGit inclusion verificationが必要。

### 10. “verified dataset” documentation stronger than reproducible evidence

**Fact:** PR #5のindependent auditはaudited branchでverification build provenance不足を指摘。

**Lesson:** human-readable verification claimとmachine-reproducible construction chainを別々に監査する必要がある。

## 16. Strengths

### A. Explicit start-here hierarchy

VAULT_MAPから必要なhubだけを読むため、大規模repositoryを毎回full scanしない。

### B. Current state and history are separated operationally

TODO / strategy canon / STATUSと、TODO_ARCHIVE / findings / LOG / handoffsが別surface。

### C. Navigation is tested, not assumed

duplicate、orphan、broken link、stale note、over-connected nodeをscannerで検出する。

### D. Negative research remains discoverable

PARKED / CLOSED / HISTORICAL / CONDEMNEDとして保存し、current builderから外す。

### E. Canon status itself can be superseded

canon audit ledgerに後続auditのsupersession bannerを付け、過去評価を不変真理として扱わない。

### F. AI retrieval is explicitly noncanonical

gbrainをread-only disposable indexとし、source Markdownを書換えない。

### G. Scratch and durable knowledge are separated

local scratchからdurable findingへ意図的にpromoteする。

### H. Human handoff is designed as state + history

STATUS overwrite / LOG append / report immutable-ish accumulationという役割分離。

### I. Data navigation scales by family manifest

raw shardをknowledge graphへ全部linkせず、dataset family単位でmapする。

### J. Large-data human interface exists

research_v1ではloader + dashboard + searchでraw 71 GBを直接扱わず探索できる。

## 17. Limitations

### A. Knowledge graph relation is convention-based

wikilinkとfrontmatterは有用だが、Hypothesis / Experiment / Dataset / Result / Decision間のtyped foreign-key modelではない。

### B. Multiple current-state surfaces remain

TODO、POLYMARKET_BRAIN、strategy hub、STATUS、manifestがdomain別にcanonicalで、single deterministic projectionではない。

### C. Manual canon can drift

実際にstale TODO、wrong status、contradictory strategy framing、stale pathが発生している。

### D. Generated navigation is local and ignored

generated index / hygiene reportsはcommitしないため、fresh cloneはregenが必要。

これはderived-state driftをGitへ固定しない利点がある一方、shared current scan resultはrepositoryだけでは見えない。

### E. gbrain freshness is operational

vault変更後のre-importが必要で、index stale防止は完全自動ではない。

### F. Data provenance is not uniform

research_v1のauditではderived verification build codeの欠落が指摘された。repository全体のevery-output provenance contractはない。

### G. Public repo has no substantive Issues history

design debateはcommit / docs / PR中心で、Issue lifecycleからpain pointを追うことはできない。

### H. Brain architectureの長期証拠は約3か月

repository自体は約7か月だが、VAULT_MAP / Obsidian brain / gbrain / branch collaborationという今回最重要のknowledge-base architectureは2026-06以降。

年単位のdurabilityはまだ確認できない。

### I. Shared brain and project-specific handoff mechanisms are not fully uniform

data-layerは非常にstructuredなNEXT / STATUS / LOG protocolを持つが、全研究branchが同じstate machineを使うわけではない。

### J. Some source-of-truth claims rely on external data

R2 raw archiveはGit外で、docs自身が「71 GB raw archiveには別backupがない」と警告する。knowledge provenanceとdata durabilityは別問題として残る。

## 18. Transferable lessons

### PLAUSIBLE_PATTERN — compact start-here map + domain hubs

**Evidence:** VAULT_MAP → project map → strategy hub → findingsのrouting。

**Why:** research数が増えてもhuman / agentが全folderをscanせずに済む。

**Caution:** map自体のstaleness監査が必要。

---

### PLAUSIBLE_PATTERN — current stateをhistoryから物理的 / semanticに分離する

**Evidence:** TODO vs TODO_ARCHIVE、active canon vs HISTORICAL/PARKED notes、STATUS vs LOG/reports。

**Why:** current decisionを探す速度を上げつつ、falsified / superseded researchを消さない。

**Caution:** current projectionがmanualならdrift detectionが必要。

---

### PLAUSIBLE_PATTERN — generated indexesはcanonicalにしない

**Evidence:** `brain/generated/` はgit-ignored、再生成可能。durable canonical mapはVAULT_MAP。

**Why:** derived indexを手編集して二重source of truthにしない。

**Caution:** regeneration cadence / freshness visibilityが必要。

---

### PLAUSIBLE_PATTERN — knowledge graph healthをtestable maintenance targetにする

**Evidence:** duplicate basenames、orphans、broken links、missing hubs、topic islandsをscriptで検出。

**Why:** note数増大時に「存在するが見つからない知識」を検出できる。

---

### PLAUSIBLE_PATTERN — datasetはshard単位ではなくfamily manifestでmapする

**Evidence:** Polymarket data manifestはraw / derived familyとreaderを記録し、個別Parquet shardをgraph node化しない。

**Why:** large dataでknowledge graphをartifact explosionから守る。

---

### PLAUSIBLE_PATTERN — scratch → durable finding promotion

**Evidence:** local gitignored scratchをcanonical hubと分離。

**Why:** unfinished reasoningとcurrent knowledgeを混ぜにくい。

---

### PLAUSIBLE_PATTERN — status classificationだけでなくevidence trust auditを別工程にする

**Evidence:** July canon auditの2日後にpipeline trust auditが数値claimとderived data defectを発見。

**Why:** well-organized incorrect researchを防ぐ。

---

### PLAUSIBLE_PATTERN — AI retrieval indexはread-only / disposableにする

**Evidence:** gbrainはlocal semantic / graph retrieval専用でsource Markdownを書かない。

**Why:** retrieval optimizationがcanonical knowledgeを変形しない。

---

### PLAUSIBLE_PATTERN — structured handoff separates “now” from “record”

**Evidence:** NEXT / STATUS / LOG / reports。

**Why:** long-running agent workflowでcurrent contextを短く保ち、historyも追える。

---

### PROJECT_SPECIFIC — Obsidian basename wikilinks

Obsidian中心のtool choice。unique basename requirementはこのchoiceから生じる。systematic-trading-researchが同じeditorを使わないならそのまま移植する必要はない。

### PROJECT_SPECIFIC — Cowork / Codex role names and local gbrain setup

agent product / local environmentに依存する。抽出すべきはrole separationとread-only retrieval boundary。

### PROJECT_SPECIFIC — R2 + DuckDB + Streamlit research_v1

large Polymarket dataに合わせたimplementation choice。Knowledge Base全体の必須構成ではない。

### DO_NOT_COPY — canonical stateを多数のmanual Markdownへ無制限に増やす

Epsilon自身がstatus contradictionを経験している。canonical surface数は小さく保つべき。

### DO_NOT_COPY — folder / wikilinkだけでexperiment lineageが完全に表現できると仮定する

現在のsystemはhuman navigationには強いが、typed experiment relationshipは弱い。

### DO_NOT_COPY — “documentation says verified” をprovenanceの代用にする

PR #5が示す通り、verification claimを生成したcode / input / construction pathが再現できるか別に確認する必要がある。

### DO_NOT_COPY — generated indexをshared truthとしてcommitし続ける

Epsilonがgenerated stateをgitignoreした理由と整合する。canonical sourceから再生成できるものはderived layerとして扱う方が二重管理を避けやすい。

## 19. Questions for cross-repository synthesis

1. current stateはEpsilonのような複数canonical routing surfaceがよいか、より小さなsingle current-state projectionがよいか。
2. strategy hub / findings graphに、`hypothesis_id`、`experiment_id`、`dataset_id`、`decision_id` のtyped relationを追加するとnavigationとmachine retrievalは改善するか。
3. manual hubとgenerated indexの境界はどこが適切か。
4. current stateをimmutable historyから自動生成できる部分はどこまでか。
5. historical noteのstatus enumを `CANON / ACTIVE / CLOSED / HISTORICAL / PARKED / CONDEMNED / SUPERSEDED` のように正規化すべきか、それともmeaningの違いを保持すべきか。
6. experiment-level provenanceはEpsilon型のmanifests + docsで十分か、zestoles型のper-output sidecarが必要か。
7. gbrainのようなlocal semantic indexを導入する前に、wikilink / metadataだけでどの規模まで耐えられるか。
8. semantic index freshnessを自動checkする最小mechanismは何か。
9. strategy researchとdata-product constructionを別lineageとして管理すべきか。
10. “canon audit” と “evidence trust audit” を別工程にするのは一般化できるか。
11. long-running AI handoffの最小構造はNEXT / STATUS / LOG / reportの4層か。
12. handoff STATUSをbranch merge後にstale化させない方法は何か。
13. failed / parked researchをAI retrievalでdefault除外しつつ、duplicate hypothesisを防ぐためには検索可能に保つ方法は何か。
14. datasetがCONDEMNEDになったとき、それを使ったdownstream experimentをmachine-readableにinvalidateするrelationが必要か。
15. graph hygiene scannerはKnowledge Base v0.1から必要か、それともnote数増大後でよいか。
16. current task listをarchiveへpruneする閾値は何か。
17. large research repoでdomain foldersを統合する判断基準は何か。
18. generated dashboard / web UIをcanonical research stateから自動deriveできる範囲はどこまでか。
19. AI agentがsemantic merge conflictを解決せずhuman decisionへ上げるruleをsystematic-trading-researchでも採るべきか。
20. raw dataがGit外にある場合、dataset identityとdurabilityをどのmanifest / hashでGit側へ固定すべきか。

## 20. Sources reviewed

### systematic-trading-research — fresh read before review

- `Josh-Temple/systematic-trading-research` main @ `f116c581b5fb1ff6ea4444d2e9e976cf5f2778c9`
- `README.md`
- `docs/ROADMAP.md`
- `docs/RESEARCH_PRINCIPLES.md`
- `research/prior-art/README.md`
- `research/prior-art/TEMPLATE.md`
- `research/prior-art/trading-second-brain.md`
- `research/prior-art/zestoles-quant.md`

### Epsilon repository identity / metadata

- `Epsilon-Fund/Epsilon-Quant-Research` repository metadata
- `Gonzalo-GallegoToscano/Epsilon-Quant-Research` metadata and parent/source relation
- default branch metadata
- current recursive tree
- commits API pagination
- all-state Issues API
- all-state Pull Requests API
- Discussions repository setting

### Core Epsilon orientation / knowledge files

- `README.md`
- `CLAUDE.md`
- `brain/VAULT_MAP.md`
- `brain/ONBOARDING.md`
- `brain/CODEX.md`
- `brain/COWORK.md`
- `brain/TODO.md`
- `brain/TODO_ARCHIVE.md`
- `brain/POLYMARKET_BRAIN.md`
- `brain/START_RESEARCH_IDEA.md`
- `brain/MERGE_PROTOCOL.md`
- `brain/OPERATING_RHYTHMS.md`
- `brain/OBSIDIAN_INFRA_ROADMAP.md`
- `brain/COWORK_MIGRATION.md`

### Handoff / continuation

- `brain/handoff/PROTOCOL.md`
- `brain/handoff/STATUS.md`
- `brain/handoff/NEXT.md`
- `brain/handoff/LOG.md`
- `brain/handoff/reports/*`
- `brain/handoffs/2026-06-01_brain_audit.md`
- `brain/handoffs/2026-06-07_brain_hygiene_cleanup.md`
- `brain/handoffs/2026-06-10_brain_audit.md`
- `brain/handoffs/2026-06-10_relay_retirement_branch_model.md`
- `brain/handoffs/2026-07-21_prealvaro_canon_audit_reorg_trust_pass.md`
- `brain/handoffs/2026-08-25_cowork_data_layer_session.md`
- `brain/handoffs/2026-08-25_l2_pipeline_recovery.md`
- `polymarket/research/HANDOVER.md`

### Research navigation / current canon

- `polymarket/research/notes/INDEX.md`
- `polymarket/research/notes/market_making/strat_market_making.md`
- `polymarket/research/notes/market_making/mm_model.md`
- `polymarket/research/notes/overview/pm_prealvaro_canon_audit_findings.md`
- `polymarket/research/notes/overview/pm_prealvaro_pipeline_trust_audit_findings.md`

### Data / machine-readable layers

- `polymarket/research/notes/overview/data_quality/polymarket_data_manifest.md`
- `docs/CRYPTO_DATA_MANIFEST.md`
- `docs/STRATEGY_REFERENCE.md`
- `polymarket/research/epsilon_data/README.md`
- `polymarket/research/CONTRIBUTING.md`
- `docs/tooling/gbrain_retrieval_layer.md`

### Navigation tooling

- `tools/brain_hygiene.py`
- `tools/brain_graph_audit.py`
- `tools/brain_commit_push.sh`
- `tools/sherpa.py`

### Pull Requests

- PR #4 `fix(gitignore): track the research lib/ package (anchor /lib/)`
- PR #5 `research_v1 audit: findings + mechanical fixes`

### Material commits

- `3ed0f1459b020afadebb4b604dc335bf55f7728b` — 2026-02-19 — initial repository / backtesting structure
- `ef24478e3019626bbd9a7f3c77139e5c4827463a` — 2026-06-05 — shared Obsidian brain onboarding
- `151ee04133c81025ba9217a596277680032a5d07` — 2026-06-07 — brain hygiene cleanup record
- `9031a2e5610b7db9dc20fe22e2e2eb540018632c` — 2026-06-07 — Obsidian brain infrastructure
- `e788e34b444ae076797aea4e37c17ae5323fceb0` — 2026-06-10 — Relay retirement / branch-per-person
- `4f41307e14265228eccf6e60bfe6b10a4740680b` — 2026-06-18 — LF safeguards / daily canon check
- `f4c6b6893415d2def4612105c71c9dd1a027d375` — 2026-07-19 — canon audit
- `ef16fabc5d0728ee83105441fdda13dad5923f75` — 2026-07-21 — one Polymarket root reorg
- `0c71650630b0e02c92e4478d0c1f33cc89e64b3e` — 2026-07-21 — pipeline trust audit
- `bd752c1654847fa754b00d6e3616c4d11684f108` — 2026-07-21 — Dali workflow revision
- `29afd29895e5bafa1bcc8b8a6050b07290c4d24b` — 2026-07-21 — capture-quality gate
- `3b862b3735b2cd7f20a66a20c0c2efe9b79fe93b` — 2026-08-26 — L2 quarantine / recovery redesign
- `0a74c10df8f00c6c333693850adf9823fe93d95f` — 2026-08-30 — research_v1 human interface / loader / handover
- `a4ad608aacbb06b2c61ea52be0053f7dd3342bb9` — 2026-09-09 — handoff reports / build scripts committed
- `e40d6b64b92c31c18c1b4a4903b872d913adfefb` — 2026-09-09 — reviewed head

## Review status

**PARTIAL**

### Reason

今回の重点である、

- large-scale research organization
- research navigation
- current vs historical separation
- handoff
- AI retrieval
- data manifest
- scaling failures
- major redesigns
- negative / superseded research handling

については、READMEだけでなくimplementation、handoff、PR、251-commit historyから具体的な証拠を確認できた。

特にknowledge brainは実際のduplicate / orphan / stale status / sync failure / directory sprawl / data-trust failureを受けて複数回再設計されており、prior-artとして高い価値がある。

一方で、今回最重要のknowledge-base architecture自体は2026-06以降約3か月の履歴しかなく、GitHub Discussionsはなく、standalone Issuesもない。またopen PR #5がdata productのprovenance / documentation gapを現在も検討中で、長期・安定運用済みarchitectureとまでは評価できない。

したがって **COMPLETEではなくPARTIAL** とする。
