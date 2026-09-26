# Research Principles

Updated: 2026-09-26

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
