# Prior-art candidate scan

調査日: 2026-09-27 JST  
対象: `Josh-Temple/systematic-trading-research` main `3436655278052bcaf9b00203a2aa901b959cb297`  
作業: WORK-PA-001 / Prior-Art Scout

## 目的と読み方

次のdeep reviewが、現在の暫定原則を最も厳しく検証できる対象を選ぶための**候補調査**。設計採用や個別repoの完全な監査ではない。調査開始時に指定されたREADME、ROADMAP、RESEARCH_PRINCIPLES、prior-artのREADME・TEMPLATE・WORK_QUEUE、既存3レビューをmainから読み、`CANDIDATE_SCAN.md` が未作成であることを確認した。既存3件は重複して候補数に算入しない。

- **FACT**: GitHubのrepo、実装ファイル、docs、Issue、PR、commitのうち実際に確認したもの。Issueの主張は「報告された事実」であって、不具合の独立再現ではない。未統合PRの案は現行mainの機能とみなさない。
- **INTERPRETATION**: その証拠から、このプロジェクトの仮説をどう試せるかについての調査者の見立て。
- **LIMITATION**: 未確認事項、適用範囲、候補の弱点。運用期間は作成日が取れた場合を除き、**確認できた最古のIssue/PR等から最新commit・資料までの可視範囲**として記す。開始日や連続運用を推定しない。

評価軸は星数でなく、時間をまたぐ実装・Issue/PR・失敗・移行の証拠、科学的再現性、provenance、negative result、AIと計算の境界。全候補のcontributor数、全closed Issue、全commitを網羅していない。各リンクはdeep reviewの入口であり、リンク先の議論の結論やmerge状態は再確認が必要。

## 候補一覧（21件）

### 1. `microsoft/RD-Agent` — HIGH

- URL: https://github.com/microsoft/RD-Agent
- **FACT**: 少なくとも[2025年のrelease PR](https://github.com/microsoft/RD-Agent/pull/976)から2026-09の[commit](https://github.com/microsoft/RD-Agent/commit/484776c211e4fbbeef03e0ec00d6bbee7362a4f4)まで履歴が見える。量的金融の仮説・experiment・feedbackは[`core/proposal.py`](https://github.com/microsoft/RD-Agent/blob/main/rdagent/core/proposal.py)、[`core/experiment.py`](https://github.com/microsoft/RD-Agent/blob/main/rdagent/core/experiment.py)、[Qlib実験](https://github.com/microsoft/RD-Agent/blob/main/rdagent/scenarios/qlib/experiment/quant_experiment.py)に分かれる。[PR #1442](https://github.com/microsoft/RD-Agent/pull/1442)は、反復評価が設定上のtest/holdout結果をfeedbackへ戻す経路を指摘し、validationと最終holdoutを分離する**未統合draft**。[PR #1438](https://github.com/microsoft/RD-Agent/pull/1438)はLLMを含まない実行・決定ゲートの提案だが**closed / unmerged**。[PR #1482](https://github.com/microsoft/RD-Agent/pull/1482)は失敗ログ欠落への**open**な修正提案。
- **INTERPRETATION**: 最も直接的なdeep review理由は、AI研究ループで「結果が次の仮説に戻る」こととholdout隔離の衝突が、実際のコード経路として議論されている点。AI推論と決定論的計算の分離、探索と確認の境界、失敗の可視性を同時に試せる。
- **LIMITATION**: PRの指摘と修正は現行挙動の独立再現やmerge済み証拠ではない。外部Qlib、MLflow、Docker、データ配布に依存し、repo単体で再現可能か未確認。

### 2. `treeverse/dvc` — HIGH

- URL: https://github.com/treeverse/dvc （旧 `iterative/dvc` は現ownerへ転送）
- **FACT**: [2020～21年頃のIssue #5369](https://github.com/treeverse/dvc/issues/5369)から2026年の[Issue #11058](https://github.com/treeverse/dvc/issues/11058)・[PR #11098](https://github.com/treeverse/dvc/pull/11098)まで履歴が見える。パイプライン定義とlockfileで依存・出力hashを追う[公式ソース](https://github.com/treeverse/dvc.org/blob/main/content/docs/start/data-pipelines/data-pipelines.md)がある。Issue #11058は「実行中に依存コードを変更すると実行後のhashが記録され、コードと出力の誤った対応が残る」と再現手順を提示。Issue #11004も凍結stageの依存hash更新を問題化している。
- **INTERPRETATION**: immutable run plan / manifestという仮説に最も強い反例候補。lockfileとGitだけでinput-at-start、競合変更、外部データの固定を保証できるかを厳しく試せる。
- **LIMITATION**: #11058は報告であり今回独立再現していない。DVCは科学上の事前登録や解釈の履歴を直接管理する道具ではない。実データremoteの可用性は別条件。

### 3. `freqtrade/freqtrade` — HIGH

- URL: https://github.com/freqtrade/freqtrade
- **FACT**: 少なくとも[2021年のIssue #5682](https://github.com/freqtrade/freqtrade/issues/5682)から2026-09の[commit](https://github.com/freqtrade/freqtrade/commit/5284e4d2721f313488dddf8a1e8c2652314c5cc7)まで可視履歴。実装に結び付く[lookahead-analysisのdocs](https://github.com/freqtrade/freqtrade/blob/develop/docs/lookahead-analysis.md)は、全期間のdataframeを先に作ることが先読みを招くと説明し、追加backtestでindicatorとsignalの差を調べる。[Issue #12507](https://github.com/freqtrade/freqtrade/issues/12507)は上位時間軸の未確定足を使う例が検出されないという利用者報告。[Issue #12894](https://github.com/freqtrade/freqtrade/issues/12894)は検査通過後もdry-runとbacktestのsignalが異なるという報告。[backtesting docs](https://github.com/freqtrade/freqtrade/blob/develop/docs/backtesting.md)は一部の動的pairlistで再現性を保証しないと明記する。
- **INTERPRETATION**: 整理されたknowledge graphやappend-only記録より先に、測定器そのものの感度、データ時点、sim/live差を試す反例。検査のPASSを「先読み不存在の証明」にしない設計に使える。
- **LIMITATION**: trading bot/engineが主で、事前登録やnegative resultの正本とは異なる。Issueの具体例は未再現で、個々の修正済み状態も未判定。

### 4. `microsoft/qlib` — HIGH

- URL: https://github.com/microsoft/qlib
- **FACT**: GitHub repository metadataの作成日[2020-08-14](https://api.github.com/repos/microsoft/qlib)、2026-09の[commit](https://github.com/microsoft/qlib/commit/be725493eb1a6bbb42bf11b37aa7669f59610ff1)を確認。[`examples/workflow_by_code.py`](https://github.com/microsoft/qlib/blob/main/examples/workflow_by_code.py)はtask config、dataset/model、recorderへのparam・artifact記録、signal分析とbacktestを結ぶ。[`qlib/workflow/record_temp.py`](https://github.com/microsoft/qlib/blob/main/qlib/workflow/record_temp.py)は結果artifactの生成形式を持つ。[Issue #1930](https://github.com/microsoft/qlib/issues/1930)はモデルを替えても同じbacktest結果となる利用者報告。
- **INTERPRETATION**: typedな研究entityをMarkdownに一から作る必要があるか、実験recorderを中心に結果と履歴を保持できるかという対案。RD-Agentとの組合せで、AI feedbackがどのsegmentを読むかも確認できる。
- **LIMITATION**: MLflow recorderの記録がraw dataの同一性、未使用holdout、事前登録を自動保証するとは確認していない。Qlib単体のIssueをRD-Agentの不具合と混同しない。

### 5. `kedro-org/kedro` — HIGH

- URL: https://github.com/kedro-org/kedro
- **FACT**: 少なくとも[2020年頃のversioning Issue #577](https://github.com/kedro-org/kedro/issues/577)から2026-09の[commit](https://github.com/kedro-org/kedro/commit/8d9abdf02b1ce93fbe9079cff6f696fb230facc4)まで可視。[`DataCatalog`実装](https://github.com/kedro-org/kedro/blob/main/kedro/io/data_catalog.py)と、versioning再設計の[Issue #4129](https://github.com/kedro-org/kedro/issues/4129)がある。同Issueは既存platformとの重複・相性、上流データの状態を軽量にsnapshotできない問題を明示し、[DVCとの連携検討 #4239](https://github.com/kedro-org/kedro/issues/4239)へつながる。
- **INTERPRETATION**: 「provenanceを自前の各output sidecarで完結させる」方向に対し、パイプラインの責務とデータ版管理を分ける成熟した対案。外部の変化するデータについて、manifestの記述と実際の固定を区別できる。
- **LIMITATION**: 汎用data/ML pipelineでtrading研究のholdoutやnegative resultを直接扱わない。#4129は提案と調査のまとめであり、完成済みmigrationとは扱わない。

### 6. `nautechsystems/nautilus_trader` — HIGH

- URL: https://github.com/nautechsystems/nautilus_trader
- **FACT**: [2021年頃のIssue #450](https://github.com/nautechsystems/nautilus_trader/issues/450)から2026-09の[commit](https://github.com/nautechsystems/nautilus_trader/commit/cd417b801942c9753f70024be11f078d940ccf99)まで可視。[BacktestEngine / BacktestNodeのdocs](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/apis-and-runs.md)は直接制御とcatalog-backed runを区別。[data/venue docs](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/data-and-venues.md)はbarからL2/L3粒度を復元できないと明示。[Issue #4063](https://github.com/nautechsystems/nautilus_trader/issues/4063)と[bar execution docs](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/bar-execution.md)はnext-bar-open執行の欠落・時点問題を扱う。
- **INTERPRETATION**: Horizontal Reactionで必要なBID/ASK tick、fill、clockの条件を、knowledge schemaとは独立に検証する候補。「同じ研究仕様でも、data粒度とexecution semanticsが違えば再現しない」を試す。
- **LIMITATION**: 研究結果のcurrent/historicalの管理は主眼でない。異なる市場・発注方式のsimulation設定をGOLDへ直輸入できない。

### 7. `nkaz001/hftbacktest` — HIGH

- URL: https://github.com/nkaz001/hftbacktest
- **FACT**: [2023年のbacktest/live議論 #54](https://github.com/nkaz001/hftbacktest/discussions/54)から2025-12の[commit](https://github.com/nkaz001/hftbacktest/commit/5f3ec40b2afb764e0fea112f941ed85523ef4e88)、2026年の[PR #328](https://github.com/nkaz001/hftbacktest/pull/328)まで可視。[queueモデルの実装](https://github.com/nkaz001/hftbacktest/blob/master/hftbacktest/src/backtest/models/queue.rs)は、実際の取引所挙動と異なり得るclear時の注文扱いをコメントで明示。[Discussion #167](https://github.com/nkaz001/hftbacktest/discussions/167)はlocal receive時刻とexchange時刻の双方を持つlatency dataを論じる。Issues一覧にはpartial-fill accounting問題も現れる。
- **INTERPRETATION**: tickデータを保存しただけではexecution再現性が得られない反例。queue、partial fill、両timestampの仕様と限界をrun metadataにどこまで含めるべきか試せる。
- **LIMITATION**: HFT・板データが中心で、M1境界突破の研究へ必要な粒度は別途判断する。Issues一覧の見出しだけでは不具合の確定や修正を判定できない。

### 8. `QuantConnect/Lean` — MEDIUM

- URL: https://github.com/QuantConnect/Lean
- **FACT**: GitHub metadataの作成日[2014-11-28](https://api.github.com/repos/QuantConnect/Lean)から2026-09の[commit](https://github.com/QuantConnect/Lean/commit/b1337938bacbdcdf7327ba4c6a10ffa89ffac403)まで長い履歴。[C# regression algorithm](https://github.com/QuantConnect/Lean/blob/master/Algorithm.CSharp/RegressionAlgorithm.cs)など既知結果を照合する仕組みがある。[Issue #9587](https://github.com/QuantConnect/Lean/issues/9587)は特定版以降の多銘柄分足backtest性能回帰、[Issue #6810](https://github.com/QuantConnect/Lean/issues/6810)はreportのbeta不一致を報告。
- **INTERPRETATION**: 長期に保守された計算エンジンでは、研究の物語よりregression algorithm・data format・result parityが有効な検証面になり得る。小規模Knowledge Baseへの反例。
- **LIMITATION**: 巨大なplatformで、個人研究の最小schemaへ直接移植しにくい。公開engineとcloud data/serviceを混同しない。

### 9. `ceruleane/trade-terminal` — MEDIUM

- URL: https://github.com/ceruleane/trade-terminal
- **FACT**: 確認できたPR・commitは2026年の短い範囲。2026-06の[PR #13](https://github.com/ceruleane/trade-terminal/pull/13)はnext-bar-openを、[PR #14](https://github.com/ceruleane/trade-terminal/pull/14)はpoint-in-time signalを扱う。[MCP docs](https://github.com/ceruleane/trade-terminal/blob/main/docs/mcp-server.md)はCLI/MCPを同一coreの薄いinterfaceとし、`run_backtest`、batch `optimize`、run provenance、lookahead・walk-forward・cost・deflated Sharpeを説明する。AIがinline codeを渡せる。
- **INTERPRETATION**: AIへ自由な戦略code生成を許しつつ、deterministic coreと実験の統計的guardrailで何を抑えられるかを試す、近いが異なる設計。PR #13・#14の時点変更はレビュー価値がある。
- **LIMITATION**: 短期履歴。docsのguardrail主張を独立検証しておらず、inline codeの安全境界と試行回数・holdout消費の実効性は不明。

### 10. `cloudQuant/backtrader-mcp` — MEDIUM

- URL: https://github.com/cloudQuant/backtrader-mcp
- **FACT**: 確認できた履歴は2026-09の[PR #1](https://github.com/cloudQuant/backtrader-mcp/pull/1)と[commit](https://github.com/cloudQuant/backtrader-mcp/commit/ad6312a11c2fe7ff9a4c3fcfcfab5037a951b58c)までの短期。[READMEのdistribution contract](https://github.com/cloudQuant/backtrader-mcp/blob/main/README.md)はpinされたfork、content-addressed CSV、typed draft、bounded subprocess、SQLite/WALのrun state、offline/backtest-onlyを定める。toolの経路制限・doctor・source rootの規則も具体的。
- **INTERPRETATION**: immutable dataset、draft review、実行をMCP境界で分ける候補。仕様が本当に実装・testsで強制されるかを深掘りすれば、AIとengineの接続方式を評価できる。
- **LIMITATION**: 長期運用・複数人の失敗履歴が乏しい。READMEの大きなtest件数や不変性の主張は今回監査していない。特定forkへのpinは移植性を下げる。

### 11. `quantopian/zipline` — MEDIUM

- URL: https://github.com/quantopian/zipline
- **FACT**: [2012年のIssue #13](https://github.com/quantopian/zipline/issues/13)から2020-10の[最終期commit](https://github.com/quantopian/zipline/commit/014f1fc339dc8b7671d29be2d85ce57d3daec343)まで可視。歴史的なevent-driven backtest engine。[Issue #1878](https://github.com/quantopian/zipline/issues/1878)はcommunity data bundleの発見・保守責任、[Issue #2615](https://github.com/quantopian/zipline/issues/2615)はbundle登録・環境の問題を示す。
- **INTERPRETATION**: dataset bundleとengineを分けた長期事例。Gitの研究記録だけではデータ配布と利用可能性を保証しない点、後継forkへ何が残ったかを検証できる。
- **LIMITATION**: 元repoの実装更新は2020年で止まっている。現在の推奨engineと扱わず、後継との比較対象に限定。

### 12. `stefan-jansen/zipline-reloaded` — MEDIUM

- URL: https://github.com/stefan-jansen/zipline-reloaded
- **FACT**: [2021年頃のIssue #8](https://github.com/stefan-jansen/zipline-reloaded/issues/8)から2025-11の[commit](https://github.com/stefan-jansen/zipline-reloaded/commit/943010b9da848e317fc520de87edade2b884d329)まで可視。Zipline継続fork。[Issue #319](https://github.com/stefan-jansen/zipline-reloaded/issues/319)はpandas 2 / NumPy 2 compatibilityと移行負債を具体化する。
- **INTERPRETATION**: 古いengineの継承時に、データbundle、環境、依存更新のどれが再現性を壊すかを元repoと対比できる。
- **LIMITATION**: 研究履歴の保存方法より依存保守の調査となる。元repoとの差分・移行の全PRは未追跡。

### 13. `polakowo/vectorbt` — MEDIUM

- URL: https://github.com/polakowo/vectorbt
- **FACT**: [2020年のIssue #42](https://github.com/polakowo/vectorbt/issues/42)から2026-09の[commit](https://github.com/polakowo/vectorbt/commit/ceffc501f2d37033a79dd86a9f883e69ec6977bd)まで可視。[Issue #101](https://github.com/polakowo/vectorbt/issues/101)は多時間軸での先読み、[Issue #809](https://github.com/polakowo/vectorbt/issues/809)は他engineとのtrades差の報告。[PR #872](https://github.com/polakowo/vectorbt/pull/872)はdeflated Sharpe計算の扱いを修正する。
- **INTERPRETATION**: 高速な大量parameter explorationとtrial accounting・時点整合性の緊張を確認できる。研究用の計算器と科学的な証拠管理は別物という対照になる。
- **LIMITATION**: Issueの差がengine bugか使用法かは未判定。trial ledgerやnegative result保存をrepoが提供するとは確認していない。

### 14. `AI4Finance-Foundation/FinRL` — MEDIUM

- URL: https://github.com/AI4Finance-Foundation/FinRL
- **FACT**: [2021年頃のIssue #112](https://github.com/AI4Finance-Foundation/FinRL/issues/112)から2026-09の[commit](https://github.com/AI4Finance-Foundation/FinRL/commit/adde5daf937701ffb476f65735de8ece0e494517)まで可視。[Issue #1359](https://github.com/AI4Finance-Foundation/FinRL/issues/1359)は論文図表に対応する正確なtrain/validation/test splitと再現codeを求める未回答の利用者質問。[Issue #1264](https://github.com/AI4Finance-Foundation/FinRL/issues/1264)はkernel再起動後の結果再現不能を報告。
- **INTERPRETATION**: 多数のnotebook・モデル・教材があっても、特定claimの再現に必要なsplitやrun identityが欠け得るという反例。『公開済み』と『再構成可能』を分ける検査に向く。
- **LIMITATION**: Issueは質問・報告であり論文結果の誤りを証明しない。DRLの確率性は単純なdeterministic backtestと異なる。

### 15. `mlflow/mlflow` — MEDIUM

- URL: https://github.com/mlflow/mlflow
- **FACT**: [2018年頃のIssue #468](https://github.com/mlflow/mlflow/issues/468)から2026-09の[commit](https://github.com/mlflow/mlflow/commit/98041cdf2d873c8ca1b93cff7557f3ee7adb608a)まで可視。experiment/run、parameters、metrics、artifactsのtrackingを提供。[Issue #6444](https://github.com/mlflow/mlflow/issues/6444)はsoft-delete semanticsの文書化、[Issue #17407](https://github.com/mlflow/mlflow/issues/17407)はdeleted runのartifact残存を論じる。
- **INTERPRETATION**: run DB中心の長期事例は、Git Markdownだけでhistoryを持つ必要性への対案。runと現在の採用判断を分ける際に、delete/GCやartifact storeの実際の保証を検証できる。
- **LIMITATION**: run trackingは事前登録、holdout、negative resultの意味づけを自動では定めない。serverとartifact storeの権限・永続性が別条件。

### 16. `IDSIA/sacred` — MEDIUM

- URL: https://github.com/IDSIA/sacred
- **FACT**: [2017年頃のIssue #224](https://github.com/IDSIA/sacred/issues/224)から2025-10の[commit](https://github.com/IDSIA/sacred/commit/86865b03d05e83da35ca582392ca31777db88d11)まで可視。[experiment実装](https://github.com/IDSIA/sacred/blob/master/sacred/experiment.py)と[observer docs](https://github.com/IDSIA/sacred/blob/master/docs/observers.rst)はconfiguration、source、run記録を扱う。[Issue #844](https://github.com/IDSIA/sacred/issues/844)は例外処理中の失敗が実験記録・再始動を妨げるという報告。
- **INTERPRETATION**: 汎用のrun configuration + observer方式は、一件ごとの独自Markdown schemaをどこまで減らせるかを試す比較対象。失敗runも観測する要件に直結する。
- **LIMITATION**: observer先の保存・source captureが常に完了するとは未検証。tradingの科学判断やcurrent canonは別層が必要。

### 17. `datalad/datalad` — MEDIUM

- URL: https://github.com/datalad/datalad
- **FACT**: 少なくとも[2018年頃のIssue #2850](https://github.com/datalad/datalad/issues/2850)から2026-09の[commit](https://github.com/datalad/datalad/commit/8357e625743e460f3967295d5efd9c5f8263b872)まで可視。[release notes](https://github.com/datalad/datalad/releases)は`datalad run`のprovenance recordの保持方法変更や`rerun`の境界問題を記す。[Issue #3154](https://github.com/datalad/datalad/issues/3154)は外部データ取得に失敗する実例。
- **INTERPRETATION**: Git外の大きなtick archiveをGit側の研究記録と結ぶため、command/input/output provenanceとデータ取得可能性を分けて検討できる。
- **LIMITATION**: 複雑な依存と大容量データ運用が前提。現時点の小規模pilotに導入すべきという推奨ではない。

### 18. `mementum/backtrader` — MEDIUM

- URL: https://github.com/mementum/backtrader （旧 `backtrader/backtrader` から転送）
- **FACT**: 2015年以降の[サンプル](https://github.com/mementum/backtrader/blob/master/samples/data-multitimeframe/data-multitimeframe.py)と2023-04の[release commit](https://github.com/mementum/backtrader/commit/b853d7c90b6721476eb5a5ea3135224e33db1f14)が見える。[resample/replayの実装](https://github.com/mementum/backtrader/blob/master/backtrader/feed.py)、timezoneによるresample問題への[PR #467](https://github.com/mementum/backtrader/pull/467)がある。
- **INTERPRETATION**: MCP wrapperが固定するengine自体の時間・bar意味論を調べる基準。wrapperの安全性と計算結果の正しさを別に評価できる。
- **LIMITATION**: 元engineの最近の開発は限定的。research ledger、immutable run manifest、current knowledge分離は主眼ではない。

### 19. `AlgorithmTrading-Strategy-MCP/BacktestPlatform` — MEDIUM

- URL: https://github.com/AlgorithmTrading-Strategy-MCP/BacktestPlatform
- **FACT**: 確認できた2026-01の[commit](https://github.com/AlgorithmTrading-Strategy-MCP/BacktestPlatform/commit/f3a69dcf9cb4436d70af26c8101c31559f2a7ca3)と[PR #104](https://github.com/AlgorithmTrading-Strategy-MCP/BacktestPlatform/pull/104)がある。[MCP tool設計報告](https://github.com/AlgorithmTrading-Strategy-MCP/BacktestPlatform/blob/main/docs/MCP_Tools_Token_Optimization_Report.md)は26個の個別toolからcategory別get/callへの変更とtoken測定を記す。PR #104はさらに14から8 toolへの統合案。
- **INTERPRETATION**: AI interfaceのtool数を減らすほど発見性・権限境界・観測性はどう変わるかという設計変更を追える。MCPは正本でないという暫定原則を、複雑な実装に照らせる。
- **LIMITATION**: 報告のtoken削減率と実運用効果は独立検証していない。製品全体の科学的妥当性をtool数から推定しない。

### 20. `locupleto/mcp-strategy-research-db` — LOW

- URL: https://github.com/locupleto/mcp-strategy-research-db
- **FACT**: 2026-08の[SDK移行commit](https://github.com/locupleto/mcp-strategy-research-db/commit/3e7e0ff804a34c8c3fd91eb77e88c7faa93ee779)を確認。[READMEとserver導線](https://github.com/locupleto/mcp-strategy-research-db)は外部trading-labが作るSQLite結果をread-only SQL・strategy比較等のMCP toolで検索する構成。今回のPR検索では有意な議論が得られなかった。
- **INTERPRETATION**: AI向け検索を後付けのread-only interfaceにする小さい対案として有用。生成・評価系と検索系を分離する境界が主な比較点。
- **LIMITATION**: DB producerは別repoで、run provenanceやnegative resultが本当にDBに入るか不明。短期・少数の可視履歴のためdeep review優先度は低い。

### 21. `scrtlabs/catalyst` — LOW

- URL: https://github.com/scrtlabs/catalyst （旧 `enigmampc/catalyst` から転送）
- **FACT**: [2017年頃の導入Issue #39](https://github.com/scrtlabs/catalyst/issues/39)から2021-09の[deprecation PR #585](https://github.com/scrtlabs/catalyst/pull/585)・[commit](https://github.com/scrtlabs/catalyst/commit/2e8029780f2381da7a0729f7b52505e5db5f535b)が見える。ownerは2022-11にarchive。[Issue #529](https://github.com/scrtlabs/catalyst/issues/529)はCLIが実行できない環境問題、[Issue #560](https://github.com/scrtlabs/catalyst/issues/560)はdata ingest問題を記す。
- **INTERPRETATION**: 「完成したtrading engineを正本の研究基盤に据える」ことの保守・依存終了リスクを、成功事例だけでなく廃止事例から検討できる。
- **LIMITATION**: 現行技術の採用候補ではない。deprecationの全因果関係はPR・Issueだけで確定しない。

## 次にdeep reviewすべき3件

1. **`microsoft/RD-Agent`** — [PR #1442](https://github.com/microsoft/RD-Agent/pull/1442)の指摘をmainのコードで再構成し、評価結果が次の提案へ入る正確な経路、holdoutが何回参照されるか、failed runの保存を確認する。未統合案と現行実装を混ぜない。Qlibは依存先として必要部分のみ併読。
2. **`treeverse/dvc`** — [Issue #11058](https://github.com/treeverse/dvc/issues/11058)を最小再現し、run開始時input identity、実行中変更、lockfile生成時点、remote dataを調べる。Gitにmanifestがあることと入力集合の凍結を同一視できるかを検証する。
3. **`freqtrade/freqtrade`** — [docs](https://github.com/freqtrade/freqtrade/blob/develop/docs/lookahead-analysis.md)の検出方式と[Issue #12507](https://github.com/freqtrade/freqtrade/issues/12507)などの見逃し報告を、修正履歴・tests・最小例で確認する。研究記録を整える前に測定器の感度とsimulation/live parityを独立監査すべきかを検証する。

この3件は、現在の暫定原則のうち **AIの探索とholdoutの境界**、**manifestによる再現性の保証範囲**、**決定論的engineの検査能力** を異なる方向から試す。HIGHはそのほかQlib、Kedro、NautilusTrader、hftbacktest。優先順位は設計採用の承認ではない。

## 未解決の横断質問

- frozen specification・run manifest・input-at-start snapshot・結果後の人間判断は、それぞれどの仕組みが担保するか。manifestが存在しても実行中変更と外部data driftを防げない場合は何を足すか。
- negative / failed resultは、engineのエラー、統計上の不採用、後から無効化された証拠として区別され、AIの検索で再発防止に使えるか。
- current valid knowledgeを一つの文書へ投影する方式以外に、run DB + explicit decision、pipeline graph、versioned artifactによる運用が成立しているか。その場合の人間・AIのread pathはどうなるか。
- backtestの再実行一致と、時点整合性・注文fill・cost・データ品質・holdout独立性という科学上の妥当性を、どのtestが別々に検証するか。

## 調査限界

これは**breadth scan**。各repoの全commit、contributor数、closed Issue総数、PR review comments、Discussions全件、全test実行、データ取得・run再現は未実施。長い履歴があるrepoでも、特定の研究設計がその期間すべて運用されたとは言えない。短命なMCP repoの契約・指標はdocsや一部PRまでの確認であり、宣伝上の件数・安全性・実性能を確証していない。GitHub検索結果のIssue見出しだけで不具合の確定・解消を判断しない。deep reviewでは対象commitを固定し、contributors、closed Issue、PR会話、削除された方式、実装・test、可能なら最小再現を追加する。
