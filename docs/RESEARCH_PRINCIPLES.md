# Research Principles

Updated: 2026-09-27

## 1. Separate research states

以下を混同しない。

- observation / fact
- hypothesis
- specification
- data
- experiment
- result
- interpretation
- decision

結果を見た後の解釈を、事前仮説や仕様へ遡及的に混ぜない。

## 2. Preserve negative and null results

negative / null / rejected / hold は削除対象ではない。

「何が効かなかったか」「どの仮説が支持されなかったか」「どの経路が実行不能だったか」は、将来の重複研究や後知恵を防ぐ重要な研究成果として保存する。

## 3. Preserve provenance

重要な結果は、可能な範囲で次を追跡可能にする。

- source identity
- dataset / artifact identity
- time range
- instrument definition
- code / commit
- parameter / configuration
- protocol version
- output artifacts
- relevant hashes
- research status

## 4. Holdout is consumed once

holdout / unused sampleの結果を確認した後、その結果に合わせて変更したruleやparameterを同じsampleで再検証済みとは扱わない。

使用済みsampleは、新しいsubset、threshold、parameter、window、ruleの選択には再利用しない。

## 5. Prefer preregistration for confirmatory tests

確認的検証では、可能な範囲で結果を見る前に次を固定する。

- research question
- predictor / signal
- target / outcome
- horizon
- population / sample
- baseline / comparator
- metric
- stopping / kill condition
- interpretation boundary

結果後に条件を救済しない。

## 6. Keep append-only research history

過去の研究記録を書き換えて現在の説明へ合わせない。

誤りの訂正が必要な場合は、訂正内容、理由、影響範囲を新しいversionまたは明示的なcorrectionとして残す。

現在有効な知識とhistorical recordは分ける。

## 7. Distinguish exploratory from confirmatory evidence

探索的な診断、post-hoc observation、feature selection、parameter searchは、独立したunused / prospective testなしにconfirmatory evidenceへ昇格させない。

「興味深い」は「検証済み」と同義ではない。

## 8. Do not optimize infrastructure before evidence

データ取得、MCP、dashboard、agent、execution infrastructureは研究を支える手段である。

研究価値が未確認の候補のために、大規模な固有インフラを先行して構築しない。複数研究で再利用できるsource packや取得経路は例外になり得る。

## 9. Separate AI reasoning from deterministic computation

AIは主に以下を担当できる。

- literature / repository research
- hypothesis organization
- source evaluation
- structured extraction
- experiment design support
- code generation
- result interpretation
- contradiction / duplication checks

一方、計算可能な部分は可能な限り決定論的なコードで実行し、入力・設定・出力を保存する。

AIの自由回答そのものを市場edgeの証拠にはしない。

## 10. Human boundary

未固定の科学条件をAIが結果を見ながら代わりに選ばない。

研究上重要な選択肢に安全な一意解がない場合は、人間判断待ちとして明示する。

## 11. Study prior art before designing new infrastructure

新しいKnowledge Base、research workflow、MCP、experiment system等を設計する前に、先行するGitHub repositoryや研究事例を調べる。

READMEだけでなく、可能な範囲で以下を見る。

- issues
- commit history
- redesigns
- removed approaches
- failures
- long-lived design choices

1つのrepositoryをそのまま模倣せず、複数例で共通して残った原則と、project固有の事情を区別する。

## 12. Start small and validate usability

最初から百科事典を作らない。

最小schemaを作り、1本のresearch lineageを完全に表現する。人間が理解しやすく、AIが誤読しにくく、provenanceを追えることを確認してから拡張する。

## 13. Current pilot boundary

Knowledge Base v0.1の最初の移植対象は Horizontal Reaction Strategy v0.1 とする。

ただし、この指定はHorizontal Reactionの結果を優先・支持することを意味しない。複雑な研究履歴、negative result、data provenance、diagnostic / confirmatory boundaryを持つため、schemaの試験材料として適しているという位置づけである。

## 14. Live trading boundary

初期のknowledge/research基盤では、ブローカーへの注文送信、自動売買、ライブ資金の自動ポジションサイズ決定を行わない。

実証研究とexecution infrastructureの境界を維持する。


## 15. Separate state reconstruction from computational reproducibility

「研究状態を後から再構成できる」と「同じ計算を同じ条件で再実行できる」は別の保証である。

GitHub上でHypothesis、Specification、Dataset、Run、Result、Interpretation、Decisionを追跡できても、次が欠ければ計算再現性は成立しないことがある。

- executable code identity
- exact calculation semantics
- environment identity
- source/input identity
- runtime boundary conditions

Phase exitやレビューでは、どちらの保証を確認したのかを明示する。

## 16. Preserve unresolved source conflicts as first-class evidence

複数の一次資料が同じ実験について異なる数値、sample count、classification、解釈を示し、どちらが後者を無効化したか確認できない場合、無理に統合しない。

- 両方をhistorical evidenceとして残す
- current projectionではconflictの存在を明示する
- どの資料をcurrent interpretationの根拠に使っているかを示す
- 明示的なcorrection / invalidation evidenceなしに古い記録を削除しない

「矛盾が残っていること」自体が研究状態の一部である。

## 17. Distinguish UNKNOWN from NOT_APPLICABLE

欠測と非適用を同じ値で表さない。

- `UNKNOWN` / `UNVERIFIED`: 本来必要な情報だが、現在の証拠では確定できない
- `NOT_APPLICABLE`: そのdimension自体がそのartifactには適用されない

例:

- source qualificationが科学的仮説を検定しない場合の `tests_hypothesis`
- blocked runが科学的outcomeを生成していない場合の `scientific_status`

この区別により、後から「調べれば埋められる未確定情報」と「埋める必要がない項目」を混同しない。

## 18. Derived interfaces must expose authority and freshness

Web UI、CURRENT projection、index、search、MCP responseは、canonical evidenceそのものではなくderived interfaceとして扱う。

derived interfaceは少なくとも次を確認可能にする。

- canonical sourceへの導線
- どのresearch stateを要約しているか
- source commit / generation pointなどのfreshness情報
- unresolved conflict
- historical / blocked / exploratory / consumed / unused の区別

derived viewが古いままでも正常表示できる状態は、科学的には危険である。可能な範囲でcanonical updateとderived projectionの不一致をCIや生成処理で検出する。

UIの表示成功、workflow成功、deployment成功は、研究結果の科学的妥当性を意味しない。
