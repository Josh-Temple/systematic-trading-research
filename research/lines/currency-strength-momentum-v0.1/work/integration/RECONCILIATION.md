---
id: INT-CSM-I1-20261001
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PARTIAL_WITH_GAPS
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: NOT_APPLICABLE
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
  - type: derived_from
    target: DEC-CSM-002
updated_at: 2026-10-02
---

# Packet I — Stage I1 reconciliation

## Current amendment after Packet E re-audit — 2026-10-02

This amendment supersedes prior current-state passages that describe E as pending or the E audit at `d1335b29eeb01cdd4b71cd5ded62033b8468e539` as the current audit. Current E is `4f683901d01fd6b5ce161c874118a34d40bcac82`; it audited current D head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`. The earlier E report remains an unchanged historical record for old D head `4f739d9cc2b21c138771afec4a728bf2b57060ba`.

### Current decision

Packet I I1 remains **PARTIAL_WITH_GAPS**. Current independent E audit `AUDIT-CSM-E-20261001-REAUDIT-01` is **PARTIAL_WITH_GAPS / BLOCKED**. I2 remains **BLOCKED / CLOSED** and `market_outcome_access=false`. HYP-CSM-002 remains UNTESTED. E independently reran D's 53 tests and synthetic oracle, but did not access market outcomes. No full-history capture, ranking, forward return, strategy P/L, Sharpe, or performance plot was accessed or calculated in this I refresh. No instruction was issued to X.

The exact human acceptance and frozen SPEC remain unchanged: accepted pre-freeze SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`; frozen blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`.

### Current refs and E identity

| Input | Current exact ref |
|---|---|
| main | `a765b33fc0915fdfdcf21287a4418aca4f5b8b7c` |
| Architecture PR #31 | `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`, open/unmerged |
| C / PR #35 | `9870c710c3cba7bb9226c9eee8ec36687b96fd9d` |
| D / PR #34 | `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`, open/draft/unmerged |
| E / PR #38 | `4f683901d01fd6b5ce161c874118a34d40bcac82`, open/draft/unmerged; audit `AUDIT-CSM-E-20261001-REAUDIT-01` |
| I / PR #37 before this refresh | `c2fdbc1f2a9fcccc32717b130a36433819aaa2fa` |

E read all nine D files at `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`, verified the supplied Git blob/SHA-256 identities, independently reran the 53-test suite, and ran an E-authored synthetic oracle. Item statuses are 1 GAP, 2 PASS, 3 GAP, 4 PASS, 5 PASS, 6 GAP, 7 GAP, 8 GAP, 9 PASS. Full finding details and hashes are in the current E RESULT and AUDIT_MATRIX.

### Independently resolved and still-open D findings

- E reproduced that formation score identities are recorded before target outcomes and remain byte-identical when synthetic target values or availability change. This resolves the old score-identity finding at the code/synthetic-test level.
- E reproduced configured synthetic signature/role/principal/expiry/revocation checks and raw source-lock-byte binding. However, D's expected current-I and current-E audit identities still pin old refs. E confirmed that D rejects the exact current I gate and this re-audit identity. Production keys are not provisioned.
- E passed the isolated write/flush/fsync/rename/promotion failure tests, then reproduced a compound failure: parent-directory fsync fails after promotion and rollback deletion also fails; the final directory still contains `run-receipt.json` even though promotion reports failure. D must fix this and add the compound case as a regression test.
- D's RUNBOOK and TEST_LOG still cite the old I gate and old E audit. D needs a non-circular identity-refresh design, accurate current refs, new D hashes and a further E audit after changes.

### Current E audit identity

PR #38 head `4f683901d01fd6b5ce161c874118a34d40bcac82` records `AUDIT-CSM-E-20261001-REAUDIT-01`, PARTIAL_WITH_GAPS / BLOCKED, bound to D `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779` and I `c2fdbc1f2a9fcccc32717b130a36433819aaa2fa`. Exact readback artifact identities:

| E artifact | Git blob SHA-1 | SHA-256 |
|---|---|---|
| `RESULT.md` | `e94a0c7ece92046d9abe5dd77d056a0291b9b461` | `69114a4c56164e36e508b46c3565f9ddc4d7ef3b5b78315cfbe8384a6228c372` |
| `AUDIT_MATRIX.csv` | `cd9625bef4f462e441d9cd581c9207d3d89331fb` | `5201506d5be8db71e281e8a59b2264cf33f9e3493621fdfc227f0d633b903062` |
| `toy_oracle.py` | `940c46da336a887b3ff7231b5f8aef747a289f30` | `1c2e7963d2891a0c5e62479c5ca51df65a71b2a89aa8566cbeec1f3ca42eb6c3` |
| `TEST_LOG.txt` | `54716715f0ea42a56b06e34924026402bf96c0e6` | `f3397bb632bbba146413e79e4adcf8b7ccf0d2a190ac3d1d3cdbe22eb64a2342` |

The previous E audit `AUDIT-CSM-E-20261002`, head `d1335b29eeb01cdd4b71cd5ded62033b8468e539`, remains historical and was not reused as current evidence. PR #38's description still shows its earlier 42/42 and 5/5 summary; the current RESULT.md and AUDIT_MATRIX.csv at the head above contain the re-audit. The I record follows the exact artifact files and fresh PR head, not the stale PR description.

### Conditions still blocking I2

1. D must resolve stale current gate/audit identity pins without a circular hash dependency, fix the compound receipt-promotion failure, add regression coverage, and publish fresh D identities. E must then audit the new D head.
2. Source readiness remains limited: external calendar authority, full-history coverage, missing/status distribution, historical publication timing, and revision/vintage are unresolved.
3. Production trust-key distribution, OS-level isolation, filesystem allowlist, durable destination, persistent append-only access/attempt ledger, and named outcome-access operator remain unestablished.
4. Human disposition is pending for both exposure disclosures; no observation values are reproduced.
5. B path/base conformance and original brief traceability remain separate lineage gaps.

DATA-CSM-002 remains PLANNED / NOT_CAPTURED_FOR_EXPERIMENT; EXP-CSM-002 remains PLANNED / NOT_RUN. The human freeze does not authorize capture or analysis.

No C raw probe CSV, OBS_VALUE, market history, price, ranking, return, P/L, Sharpe or performance plot was read or calculated for this amendment. No H3, DATA-HR-003, Autonomous Pilot, broker, live or paper-trading input was accessed.

---

## Prior D-stage snapshot — historical; reviewed old D head `4f739d9cc2b21c138771afec4a728bf2b57060ba`

## Initial I1 reconciliation snapshot — 2026-10-01


## 結論と範囲

I1の統合準備を実施し、A–Dの正確なremote headから報告・表・コード・testsを読み直した。Worker結果は研究条件の異なる文献・実装・source qualification・合成実装であり、今回の仮説に対する市場結果ではない。I1の統合記録は **PARTIAL_WITH_GAPS**。I2のoutcome-access gateは閉じたままで、I3は未実施である。

Human acceptance receipt is now recorded, but independent E audit still does not exist. C's disclosed search-result observation exposure, B's artifact path/base mismatch, unknown full-period coverage and historical vintage, and unresolved trusted authorization and file/process isolation remain. These have not been changed to PASS.

この記録は、承認されたSPECのexact pre-freeze bytes、その後のfreeze metadata差分、現在確認できる証拠と限界を固定する。承認後のSPEC本文・仮説・期間・universe・dataset role・decision ruleは変更していない。実データのranking、forward return、P/L、Sharpe、性能plotは計算していない。

## Human acceptance and freeze follow-up

Human decision HDEC-CSM-002-20261001 records the user's exact response 「承認します 進めて下さい」 at 2026-10-01T21:35:55+09:00 to the request naming pre-freeze SPEC SHA-256 e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90. The accepted proposal bytes had blob SHA-1 a073e77dec14337ee20609ed6136e50a8c1e76e2. Freeze commit 4ac1e797c777f33a467ec73b250401886d160e80 changed only SPEC frontmatter lifecycle fields; frozen blob SHA-1 is 7fe114e2fcfa33b0565b51c717455abd8837d5d9 and SHA-256 is a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2. The post-freeze body is byte-for-byte identical to the accepted body.

The human decision resolves exact-spec acceptance and the reference-association-only temporal boundary. D's config remains pinned to the accepted pre-freeze SHA and `PROPOSED_NOT_FROZEN`; implementation/spec identity is therefore BLOCKED pending D refresh and independent audit. This freeze does not authorize capture or execution. The I2 gate remains BLOCKED / CLOSED.

## Authorityとfresh-read receipt

| 項目 | fresh-read ref / 内容 |
|---|---|
| main | 2026-10-01にdefault branch mainを取得。headは a765b33fc0915fdfdcf21287a4418aca4f5b8b7c。README、docs/RESEARCH_PRINCIPLES.md、schema/v0.1/README.mdをreadbackした。 |
| mainの後続変更 | main headはworker報告の1bba695ea252863c3b7366b8b910aa36e211c325から進み、a765b33fc0915fdfdcf21287a4418aca4f5b8b7cでresearch/lines/INDEX.mdだけを追加していた。 |
| current main index | INDEXはcurrency-strength lineをbranch research/currency-strength-momentum-v0.1へrouteしている。ユーザー指定proposalはresearch/csm-architecture-review-20261001のe0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ffで、同じscience documentがmainにあるとは扱わない。古いprovisional branchやそのSPEC-CSM-001は今回読まず、契約に使っていない。Indexのroute差はこのPacketのwrite allowlist外なので変更していない。 |
| proposal | ユーザーのURLで指定されたArchitecture PR #31のexact head e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff。PR #31はmain未統合。README、ARCHITECTURE_REVIEW_2026-10-01.md、SPEC-CSM-002-v01.md、HYP-CSM-002.md、DEC-CSM-002.md、work/README.md、Packets A–EとIを取得した。 |
| SPEC-CSM-002-v01 | Accepted pre-freeze blob SHA-1 a073e77dec14337ee20609ed6136e50a8c1e76e2 / SHA-256 e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90. Frozen post-metadata blob SHA-1 7fe114e2fcfa33b0565b51c717455abd8837d5d9 / SHA-256 a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2; status ACTIVE / FROZEN. |
| original human instruction / freeze receipt | Packet Iの実行依頼後、exact pre-freeze SHA-256を示した受諾依頼へのuser返信「承認します 進めて下さい」を2026-10-01T21:35:55+09:00に記録した。元のuser brief全文はreviewed repository artifactsに見当たらない。人間承認は推定ではなく、HDEC-CSM-002-20261001のreceiptに基づく。 |

現在mainのINDEXが案内するbranchとユーザー指定proposal branchは異なる。proposal branchの内容を、current mainの正本や承認済み科学条件として扱っていない。

## Worker branch/headとbaseの照合

| Worker | PR / branch | exact head | e0fとの比較 | 判定 |
|---|---|---|---|---|
| A Literature | [PR #33](https://github.com/Josh-Temple/systematic-trading-research/pull/33) / work/csm-literature-20261001 | 5e45377b890877ff18275a7fbd4371ffe80c92ba | e0fからahead 3、behind 0 | line内allowlist。結果にはproposal head e0fを反映。main refは作業開始時の1bba。 |
| B GitHub prior art | [PR #32](https://github.com/Josh-Temple/systematic-trading-research/pull/32) / work/csm-github-prior-art-20261001 | c756805692658c99394ca71f88203ba224e78c3c | diverged。ahead 5、behind 6、merge base 36240da15fc83120d12d081c227f3e0dd8badaaa | 結果は利用可能な第三者調査だが、成果物5件はrepository rootのwork/github-prior-art/**にある。work/README.mdの「全pathはline相対」に対し、line内のallowlist pathではない。e0fへの更新もない。自動移動・修正はしていない。 |
| C Source qualification | [PR #35](https://github.com/Josh-Temple/systematic-trading-research/pull/35) / work/csm-source-qualification-20261001 | 9870c710c3cba7bb9226c9eee8ec36687b96fd9d | diverged。ahead 2、behind 6、merge base 36240da15fc83120d12d081c227f3e0dd8badaaa | line内allowlist。報告・source lockは指定proposal_ref 36240とmain 1bbaを記録し、最新mainとの差はroute index。PRはe0fをbaseにする。内容はbounded qualificationとして扱う。 |
| D Implementation | [PR #34](https://github.com/Josh-Temple/systematic-trading-research/pull/34) / work/csm-implementation-20261001 | 2271ce68039e295aa3cd50b5b2431e1a03d5dfdc | e0fからahead 13、behind 0 | line内allowlist。configは提案SPECのexact bytesと一致し、C head 9870をpin。main refは作業開始時の1bba。 |
| E Independent audit | work/csm-independent-audit-20261001 | branch/head/resultなし | — | final auditは未実施。人間freezeとfinal code/source identityに依存する。 |

B/Cのbranchがe0fより遅れていること自体を科学的否定証拠とはしない。ただしinput refとline内成果物の要件を満たしたことにもしない。Bの調査内容はsource-reported evidenceとして読むが、integrated canonical artifactとは扱わない。

## A–E task matrix

下表は各WorkerのResultにあるtask単位statusを転記した。PASSはそのWorkerが定義した範囲の完了であり、独立したE監査や仮説検証を意味しない。

### A — Literature / Scientific Prior Art

| # | Task | Worker status | 統合上の範囲 |
|---|---|---|---|
| 1 | Menkhoff et al.原文・portfolio・developed subset・cost | COMPLETE | 広いcurrency universeのCS basket。15-developed-country 1/1 net resultは0.79%年率、t=0.44。提案pairとは異なる。 |
| 2 | Moskowitz et al. TSMOM | COMPLETE | own-series excess-return sign、volatility scaling、spot/rollをCS rankと分離。 |
| 3 | Zhang, Dissecting Currency Momentum | PARTIAL_WITH_GAPS | publisher abstract等のみ。full text、G10/sample、regression timing、residual詳細は未確認。 |
| 4 | Iwanaga & Sakemoto 2025 | PARTIAL_WITH_GAPS | abstract/indexed preview。post-GFC cut、member currencies、cost、training/evaluationは未確認。 |
| 5 | Hutchinson et al. 2022 full text | COMPLETE | G11、3-month formation/1-month holdingのexcess-return basket。Jan 2010–Apr 2020 OOS net mean −3.95%年率、Sharpe −0.77。single-extreme spot testではない。 |
| 6 | 2020–2026 reassessment | PARTIAL_WITH_GAPS | Fan等を含むprimary-source screen。全候補full text、2021年以降の対象統計は未確定。 |
| 7 | construct comparison matrix | COMPLETE | basket/pair、spot/excess、USD、carry/factor等を区別。 |
| 8 | support/adverse evidenceと仕様への含意 | COMPLETE | proposed specificationを変えず、gate closedを推奨。 |
| 9 | pretraining/history、bias、independent confirmation | COMPLETE | 限界を記録。独立replicationではない。 |
|  | **総合** | **PARTIAL_WITH_GAPS** | exact 8-currency monthly ECB single-pair questionを直接推定する文献結果はない。 |

**解釈:** 2012年のbroad sample、Hutchinson 2022のpost-2010 negative、Iwanaga & Sakemotoのconditional result、Fan 2025のbasis momentumは、signal・payoff・universe・portfolio・期間が異なる。Fanの2011–2020普通の1M momentum benchmarkは0.27%/month、t=1.42との報告だが、basis strategyとは別であり、本案への反証・支持として直接移転しない。これらは仕様確定後の結果ではなく、事前priorである。

### B — GitHub Prior Art / Failure Review

| # | Task | Worker status | 統合上の範囲 |
|---|---|---|---|
| 1 | Nate Emma frameworkのcode/tests | PASS | lag、quote inversion、cost/financing経路等。repository suiteは未実行。 |
| 2 | intraday negative、bfill修正、monthly verdict | PASS | author-reported結果とcommit/codeを照合。throwaway raw runは独立再現なし。 |
| 3 | backtest/live/paper、FX-only/account、financing history | PASS | public GitHub recordのみ。private statements等は未確認。 |
| 4 | bt momentum、lag、cost path、PR #572 | PASS | source/history/testsを確認。suite未実行、equity assumptionsは移転しない。 |
| 5 | Freqtrade lookahead / HTF / Issues #12507/#12894 | GAP | source/docs/testsを確認。CLI・Issue #12894の挙動は未再現。 |
| 6 | 追加repoと3実装以上の比較 | PASS | Leanを追加screen。momentum outcomeの根拠ではない。 |
| 7 | synthetic independent checks | GAP | toy checks 4/4。external source-level reproductionは未実施。 |
| 8 | 共通原則・failure checklist | PASS | 後続D/E向けtest checklistを用意。 |
|  | **総合** | **PARTIAL_WITH_GAPS** | さらに、branchは旧base、5成果物はline-relative path外。 |

**path所見:** BのPR差分とheadで5ファイルをreadbackしたが、所在はrepository rootのwork/github-prior-art/**である。作業計画は全pathをline相対と定義し、期待pathはresearch/lines/currency-strength-momentum-v0.1/work/github-prior-art/**。この統合では内容を読むだけに留め、権限外の移動・改変をしていない。B workerによる正規pathでの保存とbase更新を要する。

### C — Data Source Qualification

| # | Task | Worker status | 統合上の範囲 |
|---|---|---|---|
| 1 | ECB exact keys、dimensions、unit、status、API/fallback | PASS | 7 seriesのbounded route/schema identity。 |
| 2 | historical setting/publication、revision/vintage、timezone | GAP | historical exact availability、method continuity、vintage/republicationはUNKNOWN。 |
| 3 | TARGET expected calendarとhash | PASS | 2009-11〜2026-09の4,331 expected open dates、203 month ends。 |
| 4 | fixed 2009-11 bounded probe | PASS | 各series 21 expected dates/status A。ただしfull-history coverageではない。 |
| 5 | source-lock、parser/missing/revision semantics | PASS | source-lockはQUALIFIED_BOUNDED_ROUTE_ONLY。 |
| 6 | provider alternatives matrix | PASS | 未取得fieldはUNKNOWN、ECBから切替なし。 |
| 7 | per-series provenance / reuse | PASS | ECB agency 4F0、attributionとraw byte保持条件を記録。 |
| 8 | minimal route / blockers / human choices | PASS | reference-only route、full-history gate closed。 |
|  | **総合** | **PARTIAL_WITH_GAPS** | evidence_validityもPARTIAL。 |

**source identity:** source-lock CSM-SOURCE-LOCK-ECB-001はD.AUD/CAD/CHF/GBP/JPY/NZD/USD.EUR.SP00.A、currency-per-EUR、daily、status Aを固定する。codelist suffix Aの表示「Average」はlabelであり、bid/ask平均やintraday平均の証拠ではない。source-lock Git blob SHA-1は81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf、SHA-256はebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71。calendar Git blob SHA-1は6ed720353472ba6f35391936c536d46fb6ae8c66、SHA-256は6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4。

**露出インシデント:** C Resultによると、source discovery中にECB currency converterとFRED seriesの検索結果が個別のcurrent observationsを表示した。値は報告・比較・計算に使わず、Resultにも再掲していないとのworker申告を確認した。Integratorとして値やraw CSVを取り直していない。この申告はEと人間によるreviewを要するため、gate conditionはBLOCKEDのままにした。2009-11 bounded probeはCの許可範囲内で、responseにOBS_VALUE列を含むraw CSVをbyte-exactで保存したが、probeはvaluesを抽出・出力・分析していないと報告されている。

**公式資料によるIntegrator追確認 (2026-10-01):** 上記C作業とは別に、値系列へのAPI requestをせず、ECB frameworkとAPI helpを確認した。現行の2026-06-23 frameworkは、reference rateが情報提供目的であること、設定・公表の現在の時刻帯、一定の条件で翌TARGET営業日の同一通貨レート公表まで訂正・再公表し得ること、関連記録を最低5年保持することを示す。API helpはstartPeriod/endPeriodとupdatedAfterによる絞込を記載する。これらは現行方針と更新検出の理解を補うが、2010–2026全期間への方針適用、原初vintageの復元、全期間のcoverageを証明しないため、historical availability/vintageはUNKNOWNのままにする。

**Integratorの追加露出:** 公式資料の確認中、ECBの一般公開current reference-rates pageを開いたところ、tool outputに個別のcurrent observationsを含む日次表が返った。これはmetadata-only範囲を超えた。値を統合artifactへ転記・引用せず、比較・計算・分析に使っていない。strategy statisticも計算していない。Cのincidentとは別にhuman/E reviewと処置を要するため、data-exposure conditionはBLOCKEDのままとする。監査対象ページ: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.eu.html。

### D — Deterministic Implementation

| # | Task | Worker status | 統合上の範囲 |
|---|---|---|---|
| 1 | parse/validateとsignal/target/metrics/receipt分離 | PASS | synthetic coreとC artifact adapter。 |
| 2 | EUR/USD、inversion、quote direction、56 pairs、numeraire | PASS | synthetic algebraのみ。 |
| 3 | exact ties、extrema、28 vs 56、pair-average rank | PASS | synthetic cases。 |
| 4 | calendar grid、missing、no rollback/compression | PASS | C calendar identityとsynthetic grid logic。 |
| 5 | prefix/future-suffix invariance、temporal claim | PASS | synthetic logic。 |
| 6 | circular bootstrap、seed/type 7、coverage/decision boundaries | PASS | fixed synthetic tests。 |
| 7 | gate/capture/ledger/hash/network boundary | PARTIAL | no full-history capture。trusted receipt、OS/file/process isolation unresolved。 |
| 8 | config/code/environment identity、no search features | PASS | preparation artifact identityのみ。 |
| 9 | no-access receiptとdiscrepancies | PASS | C disclosureを再掲せずレビュー課題として保持。 |
|  | **総合** | **PARTIAL_WITH_GAPS** | 42 testsはDの報告・TEST_LOGによる。Iは再実行せず、E独立監査も未実施。 |

Dのconfigはaccepted pre-freeze SPECのGit blob SHA-1 a073e77dec14337ee20609ed6136e50a8c1e76e2 / SHA-256 e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90を記録し、freeze_status PROPOSED_NOT_FROZENとしている。SPEC凍結後のGit blob SHA-1は7fe114e2fcfa33b0565b51c717455abd8837d5d9 / SHA-256 a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2である。したがってD configは現在のfrozen file identityと一致せず、I2条件はBLOCKED。D code/test Git blob SHA-1は11e4fa7729e5ec1c271a9b4b54c76de4cf049466 / 965e8f49ee9d5678d1022dfb45a313d79b4655b8。D Resultが報告するSHA-256は、それぞれdfd42a29e4cd042ad44ce9461d29246c0609bee401463cd21b82e0f0d6a37267 / 69693bba8efbfa37e64c0fe08be332d583a15b9f8f4d3c99652e70acba634171。D TEST_LOGは42件成功と記録するが、実験用市場データやoutcomeは含まないとされる。

Dはsynthetic CSVでC source lockとcalendarを統合テストした。Cのprobe response CSVは読んでいない。code上はclosed gate時のno-read test、event-ledger先行保存、source identity checksがある。一方、human/auditor/Integrator identityを暗号学的に認証せず、OSレベルの権限制御も実装されていない。この限界はコードテスト合格で解消されない。

### E — Independent Pre-outcome Audit

Packet Eでは、SPEC freezeがない場合はdraft auditまで行いfinal PASSを出さないと定義する。2026-10-01 fresh read時点で、指定branch、PR、RESULT、AUDIT_MATRIX、toy oracleは見つからない。したがってEのtask 1–9は **NOT_RUN**。IはEを代行していない。最終コード/source/spec identityに対する独立監査はgate blockerである。

## Claimの統合と不一致の分類

| Claim / mismatch | 分類 | 統合判断 |
|---|---|---|
| Broad currency momentumの過去結果とmajor-only後年結果 | population、payoff、portfolio、期間の違い | adverse priorとして保持。今回のsingle-pair spot questionの推定値として使わない。 |
| Hutchinson 2022 negativeとFan 2025 positive basis result | spot/excess basketとforward-curve basis strategyの違い | direct contradictionではない。普通の1M momentum benchmarkもFanの該当subperiodではt=1.42の報告。 |
| Bのintraday rejectionと月次proposal | horizon/universe/data/constructionの違い | 月次仕様のnegative resultとは分類しない。Bの報告はsource-reported。 |
| 「通貨強弱meter」と全56 directed pairの最大形成return | 同じraw common-numeraire scoresによる数学的同値 | 独立機構として重複主張しない。HYP-CSM-002もこれを記載する。 |
| ECB suffix Aの「Average」と平均bid/ask解釈 | labelとmarket conventionの混同 | C source lockはlabelだけを採用。bid/ask平均・取引値を推定しない。 |
| Cのhistorical timestamp / revision / latest vintage | source qualification gap plus accepted claim boundary | Historical availability/original vintage remains UNKNOWN and cannot support causal/executable claims. The human accepted retrospective latest-vintage reference association only; this does not qualify full-history coverage or vintage retrieval. |
| main INDEXとuser-pinned proposal branchのrouting | repository state/refの差 | science evidenceの矛盾ではないが、将来のcanonical routingに要修正。現Packetのallowlist外。 |
| Bのroot-level deliverablesとline-relative rule | path/baseの非適合 | Worker成果の配置・refを修正するまでcanonical line artifactとして扱わない。 |

文献やGitHubのnegative/positive数値は、各Workerが確認した第三者sourceの報告である。いずれも今回の提案に対するindependent reproductionではない。最初のscreenは過去文献が実際のペア収益・費用を示すかを決めず、screenの実行は別の承認とgateが必要である。

## 現在の境界と次の必須条件

- SPEC-CSM-002-v01はFROZEN。human decision HDEC-CSM-002-20261001 accepted the pre-freeze SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`; the metadata-frozen file SHA-256 is `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`. The scientific body is unchanged.
- HYP-CSM-002はUNTESTED。EXP-CSM-002とDATA-CSM-002はPLANNED、実験はNOT_RUN、Dataset captureはNOT_CAPTURED_FOR_EXPERIMENT。
- 2009-11 bounded source probeはsource qualificationのみ。2010-01〜2026-09のfixed discovery historyはcaptureされていない。future confirmation sampleは指定・アクセスされていない。
- 記載されたXは実行roleであり、named operatorは未指定。別の明示的execution instruction、独立E audit、I gate全項目PASSが要る。
- D configはpre-freeze SPEC identityのままで、frozen file identityと一致しない。Dによるconfig refresh/revalidationと、その後の独立E auditまではGate I2はBLOCKED。
- B workerは成果物のline-relative path/base mismatchを解消する必要がある。C source lock、D code/config、calendar、environmentのbyte identitiesが後続変更で変われば、既存D結果・E auditをそのまま引き継がない。
- Full-history coverage、実際のmissing/status分布、revision/vintage取得、CとIntegratorのdata-exposure disposition、trusted receipt channel、file/process isolation、durable raw snapshot/attempt ledger destinationは未解決。Historical availability/original vintageはUNKNOWNだが、受諾されたreference-association-only claimではcausal claimに使わない。
- Current main research indexのrouting差は別の変更管理で直す。今回のIntegration PRでは触らない。
- 全条件pass後にのみGate I2を再fresh-readし、Xへの一回実行指示を検討する。X/R完了後に限りI3 closureを実施する。

## Integrator access receipt

2026-10-01に、GitHubからmain a765b33fc0915fdfdcf21287a4418aca4f5b8b7cとproposal e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff、A/B/C/Dのexact headsを読み取った。上記すべてのworker deliverableを各exact headから取得し、各Git blob SHA-1を下表へ記録した。Cのraw probe CSVは取得していない。D code/testsは読み、D報告の42件test logもreadbackしたが、このI sessionで再実行していない。E auditは実行していない。

I sessionでranking、forward returns、strategy P/L、Sharpe、best parameter/period/subgroupは計算していない。追加確認中に公式ECBのcurrent reference-rates pageを開き、tool outputに個別のcurrent observationsを含む日次表が返った。許可範囲を超えた露出として記録し、個別値は成果物へ転記・引用せず、比較・計算・分析に使っていない。Cの検索結果上の露出もworker Resultからのdisclosureとして扱い、観測値は再掲しない。H3、DATA-HR-003、Autonomous Pilot inputs、broker、live/paper ordersは触れていない。

## Remote deliverable identities

以下の値は各fileのGit blob SHA-1であり、SHA-256とは表記していない。全ファイルを示されたexact refからfetchした。

### A — head 5e45377b890877ff18275a7fbd4371ffe80c92ba

| Remote path | Blob SHA-1 |
|---|---|
| [RESULT.md](https://github.com/Josh-Temple/systematic-trading-research/blob/5e45377b890877ff18275a7fbd4371ffe80c92ba/research/lines/currency-strength-momentum-v0.1/work/literature/RESULT.md) | 51bb89bc83dab3db6aad7b3df773b7ca586e9b63 |
| [EVIDENCE_TABLE.csv](https://github.com/Josh-Temple/systematic-trading-research/blob/5e45377b890877ff18275a7fbd4371ffe80c92ba/research/lines/currency-strength-momentum-v0.1/work/literature/EVIDENCE_TABLE.csv) | d52d1659c87fdab23f8ee58014b277c1343ae92a |
| [SEARCH_LOG.md](https://github.com/Josh-Temple/systematic-trading-research/blob/5e45377b890877ff18275a7fbd4371ffe80c92ba/research/lines/currency-strength-momentum-v0.1/work/literature/SEARCH_LOG.md) | 0e36124fd5f395a3434b38a62033c6a264c834f4 |

### B — head c756805692658c99394ca71f88203ba224e78c3c; remote root paths

| Remote path | Blob SHA-1 |
|---|---|
| [work/github-prior-art/RESULT.md](https://github.com/Josh-Temple/systematic-trading-research/blob/c756805692658c99394ca71f88203ba224e78c3c/work/github-prior-art/RESULT.md) | b835541c78f826237ee30d7e87aff42636ccb5d1 |
| [work/github-prior-art/REPOSITORY_MATRIX.csv](https://github.com/Josh-Temple/systematic-trading-research/blob/c756805692658c99394ca71f88203ba224e78c3c/work/github-prior-art/REPOSITORY_MATRIX.csv) | f66cbcc0dc816a51b6a019e6ca7914818723951a |
| [work/github-prior-art/FAILURE_TEST_CHECKLIST.md](https://github.com/Josh-Temple/systematic-trading-research/blob/c756805692658c99394ca71f88203ba224e78c3c/work/github-prior-art/FAILURE_TEST_CHECKLIST.md) | 698ee44ca0305b75e04edde9a58e48d752e26739 |
| [work/github-prior-art/toy_checks/run_toy_checks.py](https://github.com/Josh-Temple/systematic-trading-research/blob/c756805692658c99394ca71f88203ba224e78c3c/work/github-prior-art/toy_checks/run_toy_checks.py) | 4fdc64d059b52117163d5b75eb03f1eff83d102f |
| [work/github-prior-art/toy_checks/TOY_CHECK_OUTPUT.txt](https://github.com/Josh-Temple/systematic-trading-research/blob/c756805692658c99394ca71f88203ba224e78c3c/work/github-prior-art/toy_checks/TOY_CHECK_OUTPUT.txt) | a99ef2794c45a2fb58efcfb91fc1ce13af4df90b |

### C — head 9870c710c3cba7bb9226c9eee8ec36687b96fd9d

| Remote path | Blob SHA-1 |
|---|---|
| RESULT.md | 12fa171cd7fa05287068a955567b886e067dd793 |
| SOURCE_MATRIX.csv | b7651b2aa9b150cf79d20821d545424ca89d5f8b |
| source-lock.json | 81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf |
| expected-calendar.json | 6ed720353472ba6f35391936c536d46fb6ae8c66 |
| PROBE_RECEIPT.md | bd6d5faefe223c7bc14bd9181842ac5a821c4d83 |
| probe-metadata.json | 21aa9149b7b7db9b07f1aa3f4bf0312675a166bd |
| build_expected_calendar.py | fa16529fadb9e30c2f4156550914934814090bd2 |
| probe_ecb_metadata.py | adee4fd46c152d5b2a9e7a49442b71e47fdf2ddd |
| SHA256SUMS.txt | 4fa436ae9c3b7029da0902cdd1e446d7927f26a2 |

All C paths above are prefixed by research/lines/currency-strength-momentum-v0.1/work/source-qualification/.

### D — head 2271ce68039e295aa3cd50b5b2431e1a03d5dfdc

| Remote path | Blob SHA-1 |
|---|---|
| RESULT.md | 2f966d8eac4843a017eb2845629697b504e7394a |
| csm.py | 11e4fa7729e5ec1c271a9b4b54c76de4cf049466 |
| test_csm.py | 965e8f49ee9d5678d1022dfb45a313d79b4655b8 |
| fixtures/toy_cases.json | 4e925eabb4d88772806f0e109c15680f17d73a31 |
| config.json | a1e49571ae30d48a502c4964c14f36cf556d15bb |
| RUNBOOK.md | 74919fb26becdc9d59525d5f4765e2052512c527 |
| ENVIRONMENT.md | f6f65eaad9d45a5ad4d746254d90daff714fd3ba |
| TEST_MATRIX.md | e14ae87edf91e91b88ec7d8c7cefc93e2dd34cb8 |
| TEST_LOG.txt | 0d168ef8f5d3f73a5c98cf542e109e3d9697b094 |

All D paths above are prefixed by research/lines/currency-strength-momentum-v0.1/work/implementation/.



---

## 2026-10-04 integration amendment — hardened D/E and source-readiness boundary

### D/E status

Packet D head `3695f0a8ed085669ec3644826889f9fc953a6808` and E audit `AUDIT-CSM-E-20261004-REAUDIT-02` supersede the prior active code-level findings for exact-current D.

- D exact suite independently rerun: 56/56 PASS.
- non-circular signed I/E binding: independently PASS.
- signed E binding to exact current D bytes: independently PASS.
- prior compound final-fsync + rollback-delete false-success receipt: independently re-injected and PASS; no final SUCCESS receipt remains.
- E overall remains PARTIAL_WITH_GAPS / BLOCKED because source and production-operational evidence remain open.

Prior negative audit files are preserved under E `history/`.

### Additional exposure disclosure — 2026-10-04

During official ECB web verification of the calendar/publication methodology, a search-result representation of an official ECB reference-rate page incidentally included individual current exchange-rate observations.

Disposition at this stage:
- the observations were not copied into repository artifacts;
- they are not reproduced in this reconciliation;
- they were not compared across currencies;
- they were not used to calculate a rank, return, signal, result or parameter choice;
- the event is nevertheless recorded as an exposure disclosure and remains subject to the same explicit human-disposition gate as the earlier disclosures.

No inference that this exposure is harmless or equivalent to no exposure is made.

### Metadata-only source readiness

`DEC-CSM-004-METADATA-SOURCE-READINESS-20261004` authorizes an isolated source-readiness run that may receive full ECB CSV bytes but may emit only dates/status/schema/count/hash metadata. OBS_VALUE contents may not be printed, persisted, uploaded or used analytically.

This does not open I2 or Packet X.
