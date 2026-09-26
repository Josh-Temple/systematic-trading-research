# Prior Repository Review — zestoles/quant

## Metadata

- Repository: `zestoles/quant`
- URL: https://github.com/zestoles/quant
- Review date: 2026-09-26
- Reviewed default branch: `main`
- Reviewed head observed: `192f4bab8fb622dc65b7d245d2a58e9a20de5430`
- Visible commit history reviewed: 61 commits, 2026-08-17 through 2026-08-26
- Repository purpose: systematic trading researchの成功例だけでなく、失敗したstrategy family、backtest bug、preregistration、trial accounting、provenance、forward evidence、gate failureを監査可能な形で保存する研究記録
- Maturity / activity notes: GitHub上のrepository自体は2026-08-26作成で、visible development historyも約9日間に集中している。実装・事故記録は非常に密だが、長期運用・複数人運用・長期schema evolutionの証拠は弱い。
- Review status: **PARTIAL**

## 1. What problem is this repository solving?

### Fact

READMEは、このrepositoryを「利益が出るbot」ではなく、約1,200件のsystematic trading experimentの研究記録として位置づけている。中心的な価値として、negative resultと、損失strategyを利益strategyに見せた2件のbacktest bugを明示している。

実際に、Phase 2–3とV2 campaignでは複数のstrategy familyを評価し、`REJECTED`、`NEEDS_MORE_EVIDENCE`、`VALIDATED_FOR_SHADOW`などを記録している。最終公開時点では、plain momentumはcost bug訂正後に自身の事前固定基準でrejectされ、cash-and-carryのみが「alphaではなくyield」と限定して残されている。

### Interpretation

このrepositoryが解こうとしている主要問題は、「良いstrategyを見つけること」だけではない。

より本質的には、

- 結果を見た後の基準変更
- parameter / trialの見えない増加
- backtest implementation bug
- data format drift
- forward collectorとfrozen specificationの乖離
- 測定不能な条件をPASS扱いするfail-open
- historical resultとcurrent valid stateの混同

によって研究者自身が誤った結論を採用することを防ぐことに重点がある。

### Limitation

公開履歴は短く、設計が数年単位で維持された証拠はない。「約1,200 experiments」はrepository内の研究記録としては確認できるが、この設計が長期間・複数researcherで安定運用されたとは評価できない。

## 2. Canonical source of truth

### Fact

current stateについては、`docs/GECERLI_DURUM.md` が「現在の唯一のbinding page」と明示されている。

同文書は、

- current valid stateは `GECERLI_DURUM.md`
- `README.md` や `docs/DURUM.md` など古い層はhistorical record
- conflict時はcurrent status pageを優先
- historical documentsは削除しない

という優先関係を明示している。

科学条件については、`config/*CONTRACT*.yaml` と `config/*GATE*.yaml` がfrozen specificationとして扱われる。experiment preregistrationはmachine-readable objectからSHA-256 fingerprintを作る。

生成物はcanonical sourceと混同されていない。

- machine-readable measurement: `measurements/`
- human-readable report: `reports/`, `docs/`
- frozen scientific condition: `config/*CONTRACT*.yaml`, `*GATE*.yaml`
- current valid interpretation / operating state: `docs/GECERLI_DURUM.md`
- invalidated historical evidence: `measurements/archive/`

### Interpretation

「current state」と「historical evidence」を同じ文書に押し込まず、current pointer相当のstatus documentを置き、古いresultを削除しない構造は、systematic-trading-researchのKnowledge Base設計に直接関係する。

特に、過去に `VALIDATED_FOR_SHADOW` だったmomentumがcost bug発見後にcurrent stateではrejectedになっても、historical campaign report自体は保存される点が重要である。

### Limitation

current stateはMarkdown文書へかなり集約されており、全てのsupersedes / invalidates関係がmachine-readable relationとして正規化されているわけではない。

## 3. Current repository structure

研究・knowledge・experimentに関係する主要構造は以下。

```text
README.md
config/
  *_CONTRACT_*.yaml
  *_GATE_*.yaml
  config.yaml

src/quant/
  provenance.py
  ...
  v2/
    prereg.py
    ledger.py
    evidence.py
    arkatest.py
    motor_spec.py
    risk.py
    maliyet.py
    yurutme.py
    ...

scripts/
  00_... -> 115_...
  58_v2_kampanya.py
  87_gate_controller.py
  106_evidence_auditor.py
  108_momentum_forward_kolektor.py
  112_gate_fizibilite.py
  114_maliyet_hatasi_denetimi.py
  115_carry_getiri_izleyici.py

measurements/
  *.json
  *.json.meta.json
  research_ledger*.jsonl
  research_shadow/
  shadow/
  engine_fingerprints.json
  evidence_integrity.json
  archive/

reports/
  strategy / phase / validation / failure reports
  many *.meta.json sidecars

docs/
  GECERLI_DURUM.md
  PROJE_KURALLARI.md
  sessiz_hata_kurallari.md
  tasarim_kisitlari.md
  campaign reports
  en/
    STATUS.md
    COST_BUG.md
    GATE_FEASIBILITY.md
```

### Interpretation

単一のKnowledge Baseというより、

1. frozen specification
2. executable code
3. raw/measured machine-readable evidence
4. human-readable interpretation
5. current-state document
6. archived invalid evidence

を分離したresearch systemである。

### Limitation

番号付きscriptが100本以上あり、research lineageをdirectory treeだけから理解するのは容易ではない。後半では重複collectorが実際にspec driftの原因になっており、file countの増加自体が運用リスクになっている。

## 4. Knowledge / data model

### Fact

主要entityは少なくとも以下。

**Preregistration**

`src/quant/v2/prereg.py` の `Preregistration` は次を必須にする。

- experiment ID
- research family
- economic rationale
- symbol universe
- timeframe
- signal logic
- parameter range
- maximum trial count
- training period
- OOS period
- walk-forward plan
- cost model
- benchmark
- primary metrics
- rejection criteria
- promotion criteria
- extra fields

stable JSONからSHA-256 fingerprintを作り、変更時は同じexperiment IDを上書きせず、新しいIDを要求する。

**Research ledger**

`src/quant/v2/ledger.py` は、

- experiment ID
- family
- prereg fingerprint
- prereg body
- actual trial count
- maximum trial count
- candidate ID
- classification
- result summary
- note

をJSONLへ保存する。actual trialがpre-registered budgetを超えると例外になる。同じexperiment IDの再追加も拒否する。

**Contract / Gate**

後期campaignでは `config/C*_CONTRACT_*.yaml` と `C*_GATE_*.yaml` がfrozen scientific / acceptance conditionを持つ。

**Forward evidence**

`src/quant/v2/evidence.py` は各JSONL lineに直前line本文のSHA-256を `prev_sha` として持たせ、append後にflush + `os.fsync` を実行する。auditでchain breakを検出し、silent repairしない。

**Provenance sidecar**

`src/quant/provenance.py` はoutputごとに `.meta.json` を作り、

- producing script / command
- git commit / branch / dirty working tree
- full effective config / parameters
- Python / platform / package versions
- input SHA-256
- output SHA-256 / byte size

を保存する。Parquetではprovenanceをschema metadataにも埋め込む。

### Status model

確認したstatusには、

- `REJECTED`
- `NEEDS_MORE_EVIDENCE`
- `VALIDATED_FOR_SHADOW`
- `PASS`
- `FAIL`
- `INSUFFICIENT_EVIDENCE`
- `COLLECTING`
- `SKIPPED_CONDITION_NOT_MET`

などがある。

### Interpretation

研究の最小単位を単なるreport fileではなく、

```text
Preregistration
→ fingerprint
→ bounded trials
→ deterministic result
→ classification
→ forward evidence
→ gate
→ current decision/status
```

として結ぶ方向が明確である。

### Limitation

entity relation全体を一つのschema / graphとして管理しているわけではない。relationの一部はfilename、experiment ID、campaign convention、文書記述に依存する。

また、`research ledger` と `forward evidence ledger` のimmutability保証は同一ではない。後者はhash-chain + fsyncを持つが、前者は同じ保証を持たない。

## 5. Research lifecycle

### Fact

V2 campaignから確認できる典型的なlifecycleは以下。

```text
economic hypothesis
→ machine-readable preregistration
→ fingerprint / max trial budget
→ deterministic backtest / walk-forward / cost evaluation
→ benchmark comparison
→ classification
   REJECTED
   NEEDS_MORE_EVIDENCE
   VALIDATED_FOR_SHADOW
→ if promoted: frozen contract / forward evidence
→ fail-closed gate
→ current status
```

first edge campaignでは6件のpre-registered program、14 trialを実行し、全6件をREJECTEDとして `NO ROBUST EDGE FOUND` で終了している。

second edge campaignでは、carry、basis、cross-exchange、vol-target等をpre-registerし、carryのみshadow候補へ進め、日次barではexecution/latencyを正直にmodelできないcross-exchangeは `NEEDS_MORE_EVIDENCE` に止めている。

post-hoc observationについては、rejected candidateを「復活」させず `EXPLORATORY — NOT VALIDATION` と明示し、新しいhypothesisの理由にしか使わない例がある。

### Interpretation

研究lineageをpositive resultだけで管理せず、rejection / unresolved / exploratoryをterminalまたはintermediate stateとして保持する点は強い。

### Limitation

初期Phase 1–3と後期V2ではresearch machineryが変化しているため、repository全期間に一つの統一lifecycleが最初から存在したわけではない。

## 6. Experiment reproducibility

### Fact

確認できた再現性要素:

- dataset / source fingerprints
- prereg SHA-256 fingerprint
- code Git commit
- dirty working-tree state
- command / producing script
- full configuration / effective parameters
- Python / platform / package versions
- input SHA-256
- output SHA-256
- output size
- human-readable report
- machine-readable measurement
- contract / gate fingerprints
- deterministic rerun checks
- known-answer tests
- evidence-chain audit

cost bug auditでは、修正値を報告する前にoriginal engineをre-implementし、original outputとの差を `0.000000` まで一致させてからturnover formulaだけを変更している。最初の再実装は0.90 percentage pointずれ、candidate filter漏れを修正してから結論を出している。

### Environment

初期commitはpinned dependenciesとcentral configを導入している。provenance sidecarの実例にはPython、OS、package versions、git commit、dirty filesが保存されている。

### Randomness

今回確認した範囲では、repository全体に共通するrandom seed policyをcanonical ruleとして確認できなかった。

### Rerun procedure

numbered scriptsとreportsが強く対応しており、特定resultの再実行経路は比較的追いやすい。一方、Windows固定pathなどportableでない点はREADME自身も認める。

### Interpretation

「resultを再計算できる」だけでなく、「そのresultを生んだmeasurement implementationが正しいかをknown-answer / sensitivity / fidelity testで検証する」という二段階のreproducibilityが特徴的である。

### Limitation

market data本体はlicense不確実性のためrepositoryに含まれない。したがって第三者がcloneだけで完全再現することはできない。

また、約50ファイルで `C:\quant` hardcodingがあり、environment portabilityは弱い。

## 7. Negative / failed research

### Fact

negative / failed resultはfirst-classに近い扱いを受けている。

例:

- first campaign: 6/6 experiments REJECTED
- basis: REJECTED
- vol-target: REJECTED
- cross-exchange: NEEDS_MORE_EVIDENCE
- Phase 3の誤ったfamily rejection: bug発見後に「以前の結論がinvalid」と記録
- C8: `C8-MALIYET-HATASI` をresearch ledgerへFAILとして記録
- invalid forward evidence chainは削除せず `measurements/archive/` へ保存
- abandoned / eliminated source candidatesは理由付きでconfig / incident docsへ残す
- silent failure catalogue `K1–K9`, `S1–S21` を保持

`docs/PROJE_KURALLARI.md` は、「economicにinvalidだったparameter pointでも実際に探索したならtrial countから消さない」という方針も記録している。

### Interpretation

negative resultだけでなく、

- scientific rejection
- insufficient evidence
- measurement invalidation
- implementation failure
- data-source failure
- operational failure

をある程度分離している。

これは「失敗研究を消さない」というsystematic-trading-researchの原則と非常に近い。

### Limitation

failure taxonomyは複数のdocs / status string / incident codeへ分散している。完全に正規化されたmachine-readable failure ontologyではない。

## 8. Current knowledge vs history

### Fact

このrepositoryで最も明確な設計変更の一つ。

初期・中期にはREADME、`DURUM.md`、campaign reports等が異なる時点の状態を保持し、後に相互矛盾が生じた。

2026-08-25のhandover audit commit `77df91686430...` で、

- README / DURUMをhistorical record扱い
- `docs/GECERLI_DURUM.md` をcurrent binding statusに固定
- invalid forward evidenceをarchiveし、削除しない
- evidence counterをGENESISから再開

する方式へ整理された。

その後、2026-08-26にmomentum cost bugが発見され、historical `VALIDATED_FOR_SHADOW` resultを削除せず、current statusだけをrejected / suspendedへ変更している。

### Interpretation

「過去に何を信じていたか」と「現在何を有効とみなすか」を分けることの必要性を、実際の事故から学んだ事例になっている。

systematic-trading-researchのKnowledge Baseでは、current viewをhistoryから生成するのか、明示的current documentを置くのかを比較する材料として特に価値が高い。

### Limitation

current documentは手動で維持されるMarkdownであり、ledgerから決定論的に再構成できることまでは示されていない。

## 9. AI / agent role

### Fact

`docs/QUANT_V2_SYSTEM_REPORT.md` には、

- agents cannot send orders
- `RiskCore` is the sole deterministic gate
- agent cannot bypass it

という `LIVE AI BOUNDARY` が明示されている。

一方、current repositoryで `AI`, `LLM`, `Claude`, `OpenAI`, `MCP` 等をcode searchした範囲では、具体的なLLM / agent integrationは確認できなかった。

### Interpretation

AI-assisted research architectureの実装例としては弱い。

参考になるのは「AIが存在する場合もexecution authorityはdeterministic gateの外へ出さない」というboundaryであり、AI retrieval / reasoning / write workflowそのものではない。

### Human review

mainnet移行はgate PASSだけで自動許可されず、manual human lockとrunbookが必要とされる。

### Limitation

agentが何をread/writeできるか、AI-generated interpretationをどうreviewするか、AI retrievalをどう制限するかは実装証拠がない。AI部分は他repositoryで補う必要がある。

## 10. Deterministic execution boundary

### Fact

deterministic codeへ置かれている主要部分:

- data loading / normalization
- cost / fill model
- backtest
- walk-forward evaluation
- metrics
- trial counting
- prereg fingerprint
- evidence hashing / chain audit
- gate evaluation
- engine fingerprint checks
- RiskCore
- execution reconciliation
- stale-data fail-closed checks
- evidence integrity audit

`scripts/87_gate_controller.py` はfrozen gate fileからthresholdを読み、unmeasurable thresholdが残る場合にPASSへ進ませず `INSUFFICIENT_EVIDENCE` とする。

### Major lesson from failure

2026-08-25 auditでは、deterministicであってもimplementationがfrozen specからdriftしていた。

原因として、

- duplicated spec source lists
- duplicated forward collectors
- incomplete fingerprint coverage
- silently swallowed fetch failures

が特定され、shared `motor_spec.py` とsingle collector pathへ統合された。

### Interpretation

「AIをdeterministic codeから分離する」だけでは不十分であり、deterministic code自身もspec fidelityとmeasurement validityをauditする必要があることを示す。

## 11. Human-facing interface

### Fact

human interfaceは複数ある。

- README
- current status document
- campaign reports
- incident catalogue
- final handoff reports
- HTML dashboard / command center
- raw JSON / JSONL
- numbered scripts

dashboardも存在するが、公開repositoryの主なknowledge navigationはMarkdownとdirectory structureである。

### Strength

headline performanceだけではなく、failure reason、measurement limitation、current vs historical statusへ辿れる。

### Limitation

research lineageが大きくなると、100本以上のnumbered scriptsと多数のreportsから必要なentityを探す負担が大きい。専用graph / search UIはない。

## 12. AI-facing retrieval

### Fact

MCP、embeddings、RAG、structured retrieval APIは確認できなかった。

machine-readable assetsとしては、

- JSON / JSONL ledgers
- YAML contracts / gates
- provenance sidecars
- `docs/research.json`
- fingerprint files

がある。

### Interpretation

AI retrieval interfaceは未実装だが、将来targeted retrievalへ利用できるmachine-readable substrateは比較的豊富。

### Limitation

AIが「current valid status」だけを安全に取得するindexはない。historical `VALIDATED_FOR_SHADOW` とcurrent `REJECTED` が同時に存在するため、naive file searchでは誤読リスクがある。

## 13. Issues / discussions findings

### Fact

fresh API readで、

- all-state GitHub Issues: 0
- Pull Requests: 0
- Discussions: repository settingでdisabled

だった。

### Interpretation

設計判断・事故・修正理由はIssue / PR discussionではなく、commit messageとrepository内docsに非常に多く保存されている。

### Limitation

reviewer discussion、複数人の異論、長期issue lifecycleから得られる証拠はない。

## 14. Commit-history findings

61 commitsを確認した。重要な流れは以下。

### 2026-08-17 — infrastructure before trading logic

`5179a86b02...`:

- pinned dependencies
- central config
- logging
- output provenance sidecars
- crash-resistant JSONL measurement
- infrastructure self-test

を導入。commit messageはtrading logicを含まないと明示する。

この初期設計からprovenanceとknown-answer verificationは最後まで残っている。

### 2026-08-17〜19 — data-source failures create rules

data archive probingで、

- column order traps
- reverse chronological data
- volume-unit mismatch
- S3 pagination truncation
- timestamp-unit changes
- inconsistent headers
- broken daily data

などを実測し、後に `K1–K9`, `S1–S21` のsilent-failure rulesへ蓄積した。

### 2026-08-20〜22 — strategy research and first major invalidation

Phase 2–3で複数strategy familyを大量評価した後、`S19` bugにより過去のtrend-following eliminationの一部がinvalidと判明。

`maliyet_uygula()` がpositionをreturnへ掛けておらず、「buy-and-holdを超えない」という結論が測定ではなく構造的tautologyだった。

旧判断を削除せずinvalidとして記録し、232 trialsをrerunした。

### 2026-08-24 — V2 introduces preregistration / ledger / bounded campaigns

V2 first edge campaignはpreregistration、fingerprint、trial budget、OOS / benchmark / cost evaluationを統合。全6件REJECTED。

続くcampaignでcarry等を評価し、positive / negative / unresolvedを分離した。

### 2026-08-25 — forward-evidence architecture redesign after audit

commit `77df91686430...` は大規模なhandover audit。

確認された問題:

- gate decision pathが30日目にKeyErrorになる
- collector universeが45-symbol PIT specではなくhardcoded 12 symbols
- rebalance event countingがhourly observationsを誤カウント
- concentration metricの意味を取り違える
- incomplete daily candleを使用
- fetch failureをsilent swallow
- gateが8 threshold中5つを実質skipしてもPASS可能
- forward evidenceにfsync不足
- engine specification sourceが複数箇所にduplicate
- fingerprintがactual collector / engineの一部を覆っていない

変更:

- `motor_spec.py` へsource definitionをcentralize
- duplicated C6/C7 collectorsを `108_momentum_forward_kolektor.py` へ統合
- old collectors `80` / `85` は削除せずintentional fail stubへ変更
- old invalid evidenceをarchive
- current binding statusを `GECERLI_DURUM.md` に一本化
- fail-closed gateへ修正

### 2026-08-26 — credential-path / execution-path bugs

testnetを実際に開いた時点で、

- append-only ledgerをin-place rewriteし得るreconciliation bug
- fixed quantity / fake intended price
- unstable intent IDによるduplicate-order risk
- testnet commissionが0でcost calibrationを代表できない

など、初めてそのpathが実行された時にのみ現れるbugが見つかった。

### 2026-08-26 — second major cost bug overturns momentum result

commit `db2041ead8...`:

momentum turnoverを

```python
abs(sum(delta_weight))
```

としていたため、full rebalanceでcostがほぼ0になるbugを発見。

auditはoriginal engineをbit-exactに再現してからformulaだけを変更。corrected breakevenは約1.69xとなり、frozen C7 contractの `breakeven < 2x` rejection criterionを満たした。

commit `810e76ad81...` でformulaを修正し、さらにactual engine fileがfingerprint対象に含まれていなかったgapを修正した。

結果を見てlow-turnover variantを探すことは行わず、同じparameterで再評価した。

### 2026-08-26 — publication / shutdown

`e94b7d9202...`:

- scheduled tasksを全停止
- running processを停止
- English entry docsを追加
- cloneしても何も自動起動しない状態にした

### Interpretation

このcommit historyの価値は「成熟した最終architecture」そのものより、短期間に複数回、研究結論やevidence pipelineがimplementation bugで覆り、そのたびに

- invalid evidenceを保存
- current stateを更新
- source duplicationを減らす
- measurement itselfをtestする

方向へ設計が変化した点にある。

### Limitation

全履歴が約9日間に集中しており、「長く残った設計」を長期耐久性の証拠として扱えない。

## 15. Failure cases / abandoned approaches

### Confirmed abandoned / invalidated approaches

1. **Phase 3 original trend-following conclusion**
   - position application bugでinvalid
   - rerun
   - old conclusionをhistorical failureとして保持

2. **Duplicated C6/C7 forward collectors**
   - frozen spec drift
   - old scriptsはintentional fail stub
   - original code/evidenceをarchive
   - replacementはsingle shared collector

3. **Forward evidence before universe/spec correction**
   - chainをarchive
   - evidence windowをGENESISからreset

4. **Gate that could silently PASS unmeasured thresholds**
   - fail-closedへ変更

5. **Frozen gate interpretation that was statistically ill-posed**
   - `GATE_FEASIBILITY.md` でpassability自体を測定
   - outcome蓄積前だったためreinterpretationではなくredesign対象にした

6. **Momentum VALIDATED_FOR_SHADOW status**
   - cost bug発見後にcurrent stateでrejected / suspended
   - historical reportは保持

7. **Live/scheduled operation**
   - publication前に全scheduled task停止

### Interpretation

「abandoned codeを完全削除する」のではなく、dangerous predecessorをdisabled stubまたはarchiveとして残し、後から「なぜ使ってはいけないか」を追えるようにする設計は有力。

## 16. Strengths

### A. Negative results are discoverable

成功strategyだけでなく、REJECTED / NEEDS_MORE / FAILをmachine-readable ledgerとreportへ残す。

### B. Preregistration is executable metadata

preregistrationがproseだけでなくfingerprint可能なstructured objectになっている。

### C. Trial budget is enforced

actual trialsがpre-registered maxを超えるとcodeが拒否する。related momentum lineageではtrial accountingをresetしないこともcontractに明示する。

### D. Provenance is unusually concrete

command、git state、config、environment、input/output hashまでoutput sidecarへ残す。

### E. Measurement machinery itself is audited

known-answer tests、cost-rate sensitivity、bit-exact fidelity、gate feasibility等で「測定器が測れているか」を確認する。

### F. Current state and historical record are explicitly separated

過去のheadline resultを消さず、current statusだけを訂正する。

### G. Fail-closed behavior

unmeasurable threshold、missing data、integrity failureをautomatic PASSへ変換しない。

### H. Invalid evidence is preserved

wrong collectorのevidenceを削除せずarchiveし、why-invalidを残す。

### I. Deterministic execution authority is narrow

RiskCore / gate / backtest等をfixed codeへ置き、mainnetはhuman approvalを残す。

## 17. Limitations

### A. Long-term evidence is weak

visible historyは約9日間。長期operation、schema migration、多人数collaborationは未検証。

### B. Research ledger is not uniformly append-only

READMEはappend-only ledgerを強く打ち出すが、実装上は区別が必要。

`src/quant/v2/evidence.py` のforward evidenceはhash-chain + fsyncで強いappend-only性を持つ。

一方、`src/quant/v2/ledger.py` 自体はappendするもののhash-chain / fsyncを持たず、さらに `scripts/58_v2_kampanya.py` はcampaign開始時に既存 `measurements/research_ledger.jsonl` を削除して再生成する経路を持つ。

したがって「全research historyがimmutably append-only」とは評価できない。

### C. Current state is partly manually curated

`GECERLI_DURUM.md` は有用だが、ledgerからdeterministically generatedされたprojectionではない。

### D. Portability is weak

Windows / `C:\quant` hardcodingが広範囲にある。

### E. Raw market data is absent

licence uncertaintyによりdataを再配布しないため、third-party full reproductionはcloneだけでは不可能。

### F. AI-assisted research is not implemented

AI boundaryの文書はあるが、LLM / agent / MCP / retrieval architectureの実装は確認できない。

### G. Repository complexity became a failure source

duplicated collector / spec listがactual driftを生んだ。100本超のnumbered scriptsはaudit trailには役立つ一方、maintenance riskを増やす。

### H. Issues / PR review evidence is absent

single-author commit historyが主なdecision logであり、external review / adversarial collaborationは確認できない。

## 18. Transferable lessons

### PLAUSIBLE_PATTERN — current valid knowledgeとhistorical recordを分離する

**Evidence:** historical campaign resultを保存したまま、`GECERLI_DURUM.md` をcurrent binding stateにした。

**Why transferable:** Trading Second Brainでもdurable current knowledgeとdecision historyの分離が見られた。2 repositoryで方向性が一致しているため有力だが、まだstrong common principle確定には早い。

**Implication for synthesis:** Knowledge Baseでは「最新文書へ過去を上書き」するより、historyを残しcurrent viewを別に持つ設計を優先比較する。

### PLAUSIBLE_PATTERN — preregistrationをmachine-readable fingerprintへする

**Evidence:** hypothesis、sample、cost、metric、rejection / promotion criterion、trial budgetをstable JSONとしてfingerprintする。

**Why transferable:** confirmatory boundaryとresult-after-the-fact rescueを機械的に区別しやすい。

### PLAUSIBLE_PATTERN — failed / rejected / unresolvedをfirst-class searchable stateにする

**Evidence:** `REJECTED`, `NEEDS_MORE_EVIDENCE`, `FAIL` がledger / summaryへ残る。rejected candidateのpost-hoc observationもvalidationへ昇格しない。

**Why transferable:** positive-result-only archiveよりduplicate researchとsurvivorship biasを抑えやすい。

### PLAUSIBLE_PATTERN — trial accountingをlineageと一緒に保持する

**Evidence:** C7 contractは同じmomentum familyのimplementation変更でtrial countをresetしない。

**Why transferable:** strategy nameやimplementationを変えてmultiple-testing burdenを隠すことを防げる。

### PLAUSIBLE_PATTERN — measurement implementationにknown-answer testを要求する

**Evidence:** K6、cost 10x sensitivity、bit-exact reimplementation、gate feasibility。

**Why transferable:** backtest resultの再現だけでは、同じbugを再現している可能性を排除できない。

### PLAUSIBLE_PATTERN — fail-closed gate

**Evidence:** unmeasurable thresholdがある場合は `INSUFFICIENT_EVIDENCE` で止める。

**Why transferable:** missing evidenceをneutral / PASSへ変換しない原則として、data quality、AI retrieval、research promotionにも使える。

### PLAUSIBLE_PATTERN — invalid artifactをarchiveし、successor relationを残す

**Evidence:** invalid forward evidence chainとold collector sourceをarchiveし、old executable entrypointは明示的fail stubへ変更。

**Why transferable:** deletionよりも再発防止とauditabilityが高い。

### PLAUSIBLE_PATTERN — provenanceをresultの隣へ置く

**Evidence:** per-output `.meta.json` にcode/config/environment/input/output identityを保存。

**Why transferable:** central provenance databaseだけに依存せず、artifact単体でもoriginを追いやすい。

### PROJECT_SPECIFIC — Windows crash-resilience / Memurai / Task Scheduler design

single-machine operational constraintから生まれた設計。一般化せず、必要なprincipleだけ抽出する。

### PROJECT_SPECIFIC — Binance testnet / carry / momentum-specific gates

domain-specific thresholdやexecution detailはそのまま移植しない。

### DO_NOT_COPY — numbered script sequenceをKnowledge Base taxonomyとして使う

00→115のsequenceはhistoryを追いやすいが、scaleするとmeaningがfilename orderへ埋まり、duplicate implementationも生んだ。

### DO_NOT_COPY — prose current-status pageだけを唯一の整合性機構にする

current pointer自体は有用だが、可能ならcanonical entitiesからcurrent projectionを再構成できる設計と比較すべき。

### DO_NOT_COPY — “append-only”をstorage layer全体の性質だと仮定する

forward evidenceとresearch ledgerで保証強度が異なる。immutability requirementはartifact typeごとに明示し、実装で検証する必要がある。

## 19. Questions for cross-repository synthesis

1. current valid knowledgeは手動status documentに置くべきか、immutable research entitiesから生成するprojectionにすべきか。
2. `supersedes`, `invalidates`, `corrects`, `derived_from` をmachine-readable relationとして持つrepositoryはあるか。
3. immutableにすべき最小単位はexperiment result、research ledger、forward evidence、decisionのどこまでか。
4. preregistration fingerprintとGit commitだけで十分か。dataset / source manifestを独立entityにすべきか。
5. historical `VALIDATED` とcurrent `REJECTED` をAI retrievalで誤読させないindex設計は何か。
6. invalid evidence chainをarchiveする場合、archive metadataをどこまでstructuredにするべきか。
7. related strategy lineageのtrial countをどの単位でcarry forwardするのが妥当か。
8. failure taxonomyはprose incident catalogueとmachine-readable statusのどちらを中心にすべきか。
9. measurement implementationのknown-answer / sensitivity testをexperiment contractへ組み込んでいる他repoはあるか。
10. provenance sidecar方式は長期的に維持しやすいか。それともcentral manifest / content-addressed storeの方が良いか。
11. duplicated execution pathを減らすため、strategy specificationとdeterministic engineをどの粒度でsingle-source化すべきか。
12. AI agentへcanonical stateのwrite権限を与える場合、zestoles/quantのfail-closed gateに相当するguardrailをどう設計するか。
13. human-readable Markdownとmachine-readable experiment entitiesの二重管理を、長期にdriftさせず運用した事例はあるか。
14. current knowledgeをWeb / MCPへ公開する前に、historical contradictionsをどのindexで遮断すべきか。

## 20. Sources reviewed

### Repository / current structure

- Repository metadata: https://github.com/zestoles/quant
- default branch head `192f4bab8fb622dc65b7d245d2a58e9a20de5430`
- recursive repository tree
- root README
- all-state Issues API
- all-state Pull Requests API
- commit history, 61 visible commits

### Core docs

- `README.md`
- `docs/GECERLI_DURUM.md`
- `docs/PROJE_KURALLARI.md`
- `docs/sessiz_hata_kurallari.md`
- `docs/tasarim_kisitlari.md`
- `docs/en/STATUS.md`
- `docs/en/COST_BUG.md`
- `docs/en/GATE_FEASIBILITY.md`
- `docs/FIRST_EDGE_CAMPAIGN_REPORT.md`
- `docs/SECOND_EDGE_CAMPAIGN_REPORT.md`
- `docs/QUANT_V2_SYSTEM_REPORT.md`
- `docs/QUANT_V2_FINAL_HANDOFF_REPORT.md`
- `docs/research.json`

### Core implementation / data model

- `src/quant/provenance.py`
- `src/quant/v2/prereg.py`
- `src/quant/v2/ledger.py`
- `src/quant/v2/evidence.py`
- `scripts/58_v2_kampanya.py`
- `scripts/87_gate_controller.py`
- `scripts/106_evidence_auditor.py`
- `scripts/108_momentum_forward_kolektor.py`
- `scripts/114_maliyet_hatasi_denetimi.py`
- `config/C7_CONTRACT_PLAIN.yaml`
- `measurements/research_ledger.jsonl`
- `measurements/research_ledger_c8.jsonl`
- `measurements/00_temel_dogrula_sonuc.json.meta.json`
- `measurements/archive/`
- disabled predecessor collectors `scripts/80_c6_shadow.py`, `scripts/85_c7_shadow.py`

### Material commits

- `5179a86b02...` — project foundation / provenance / crash-resistant records
- `178ceadcce...` — provenance Git-status parsing fix
- `7fab25405f...` — parquet compatibility gate / timestamp-unit assumption failure
- `9e29977c52...` — source probing / pagination failure / format traps
- `e746a59dcc...` — Phase 1–3 archive / strategy ledgers / S19 correction
- `ba6026d604...` — V2 first edge campaign, no robust edge
- `25efcba35c...` — second edge campaign
- `77df91686430...` — handover audit / forward-evidence redesign / current-state separation
- `ed6b3a7f39f1...` — testnet-path failures / append-only reconciliation correction
- `db2041ead8...` — momentum transaction-cost bug discovery
- `810e76ad81...` — turnover correction / engine fingerprint coverage
- `751955fc94...` — carry validation / return monitor
- `e94b7d9202...` — shutdown / publication preparation
- `192f4bab8f...` — reviewed head

## Review status

**PARTIAL**

### Reason

repository内部には、失敗研究、preregistration、provenance、trial accounting、current-vs-history separation、silent-failure incident、major redesignの具体的証拠が多く、Phase 1 prior-artとして非常に有用である。

ただし、visible development historyは2026-08-17〜2026-08-26の約9日間に集中し、GitHub Issues / PR / Discussionsも存在しない。したがって、長期運用で残った設計、複数人運用での耐久性、長期schema evolutionについての証拠は不足している。

このため **COMPLETEとはせずPARTIAL** とする。
