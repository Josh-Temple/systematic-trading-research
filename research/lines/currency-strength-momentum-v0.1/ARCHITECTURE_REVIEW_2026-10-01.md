---
id: REVIEW-CSM-002
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PRE_OUTCOME_REVIEW_COMPLETE_WITH_GAPS
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: NOT_APPLICABLE
relations: []
---

# Research Architecture Review

## 判断

最小費用の月次spot現象screenを設計する価値はある。ただし、このideaの本体は **extreme cross-sectional currency momentum** である。一般的なcurrency momentumの過去の成功を、現在の8通貨・単一ペア・net収益へ外挿しない。最初の結果は戦略採用判断ではなく、次の研究へ資源を使うかの判断材料とする。

推奨: AUD/CAD/CHF/EUR/GBP/JPY/NZD/USD、1 calendar month formation、1 calendar month reference-to-reference target、2010-01〜2026-09をtarget月とする固定Discovery。ECB latest-vintage spot reference ratesを使用。全期間平均の符号と依存を考慮したintervalだけで進行判断し、horizon/universe/eraを探索しない。

**現在のgateはCLOSED。** 月次・8通貨・post-2010・参考値上の同一境界・進行ruleには一意の科学的正解がない。後述の具体契約を人間が確定する必要がある。準備作業の継続は既に依頼範囲内であり、その都度承認を求める必要はない。

## Fresh-read receipt

- 開始main: `1bba695ea252863c3b7366b8b910aa36e211c325`、tree `bb8be2549f7f2e62e04778ee614b847b1e0c0063`。
- README、docs/RESEARCH_PRINCIPLES、ROADMAP、schema/v0.1/README、prior-art/README、SYNTHESIS_V0.2、freqtrade、Horizontal Reaction CURRENTをこのmainから読んだ。
- Autonomous Pilot: docs/AUTONOMOUS_RESEARCH_PILOT_V0.1_DRAFT、Phase B protocol、amendment v0.1.1を読んだ。draftとfrozen Phase Bを区別した。
- mainのrecursive treeにcurrency-strength lineは存在しない。repo内AGENTS.mdは見つからなかった。
- branch一覧に `research/currency-strength-momentum-v0.1`、head `4b0a6e54f7186308c2e9b1e14a6605fae018c42e`。mainとのcompareはahead、変更は当該lineの9 Markdownファイルのみ。
- all-state PR一覧30件（最新#30）に関連title/body/headの一致なし。既存案にPRは確認できなかった。branchに書かれた「approved」「FROZEN」「DISCOVERY_READY」はmainの権限・状態として採用しない。
- compareで9ファイル全文を確認し、仕様はlocal Gitでもreadbackした。既存branchは変更していない。

mainの原則: negative、null、invalid、execution failureを分離し、結果後の変更は新しい仕様へ残す。Pilotから採用する原則は、研究契約・data visibility・scientific decision rights・全attempt記録・final holdoutをadaptive loopの外へ置くこと。**Phase B成功を新lineのmarket access許可にしない。** 今回は単一固定実験であり、240候補探索やPilotのインフラは移植しない。

## 用語と仮説の違い

| 用語 | 数学・研究対象 | 今回との関係 |
|---|---|---|
| Cross-sectional currency momentum | 同時点の通貨間の過去return順位で将来を比較 | 本体。zero-net currency exposureでもfactor-neutralではない |
| Relative strength | 他の通貨に対する相対的変化。用語だけではsignal未定義 | raw common-numeraire returnなら同じ順位 |
| Winner-minus-loser portfolio | 上位・下位複数通貨のbasket | single extremeはk=1という特殊例。分散・turnover・tail riskは異なる |
| Single strongest-minus-weakest pair | maxとminの1組 | 今回。全directed pairの最大formation log returnと一致 |
| Time-series momentum | 各固定instrument自身の過去return符号等に従う | 全体順位とは異なる。quote方向、基準、vol scalingも定義が必要 |
| Common-factor / factor momentum | 共通factor自身の過去returnに従う | 似たspot収益を説明し得る別の仮説 |
| Dollar factor | 通貨excess returnに共通するUSD関連成分 | USDをrankingに含めることとも、broad USD indexとも同一ではない |
| Carry factor | 金利/forward discountでsortするfactor | spot momentumとは別signal。spot収益にfactor exposureがあってもcarry受取額ではない |
| Idiosyncratic currency momentum | factorを除いた残差のcontinuation | raw rankingがpositiveでも成立を示さない |
| Intraday currency-strength ranking | 分・時間の定義・同期quote・session・microstructure | 月次を支持してもintradayを支持しない |
| Medium-horizon / monthly momentum | calendar formation/holding | 今回は1/1のみ。12/1や6/1のreplicationではない |

## 数学的同値性の条件と証明

currency iの共通numeraireでの価値をV_i(d)>0、log価値v_i=log(V_i)。同期したa,bでs_i=v_i(b)-v_i(a)。iを買いjを売るpair価格P_ij=V_i/V_j（j units per i）。そのlog returnは r_ij=s_i-s_j。

従って全ordered pairs i≠jが選択可能なら max r_ij=max s_i-min s_j。unique extremaなら選択identityも同じ。別numeraireへの変更は全s_iから同じ量を引くだけで、順位もpair差も不変。EUR=0、USDは普通の1通貨として含める。

単純return R_iでもpair returnは `(1+R_i)/(1+R_j)-1` なので正価格・共通期間ならmax/minの**選択**は一致する。ただし `R_i-R_j` はそのpairの単純returnではない。currency basketのdollar P/L、leveraged CFD収益、forward excess returnもこのlog比率とは同一でない。

必要条件: 同期endpoint、同じformation horizon、common-numeraire整合性、全8通貨を含む、56 ordered pairsの両方向を許す、pair別の費用/vol/liquidity filterなし、raw returnの単調共通変換。28慣例pairのlong方向だけの最大値選択では一般に一致しない。非同期quote、三角関係のずれ、brokerに存在しないcrossも別問題。

Pair-average log strength `A_i=(1/7)Σ(j≠i)(s_i-s_j)=(8/7)(s_i-mean(s))` は完全な等weight networkでは**同じ順位**。全対戦でのrank-win数もunique raw scoresなら同じ順序になり得る。名前を変えても情報は増えない。

Vol normalization、unequal/incomplete pair averages、multi-horizon、pair-specific smoothing/weight、独立したbreadth・dispersion conditioningは別signalになり得る。ただし共通の単調変換や同じlinear filterを各通貨に適用してpair差を取るだけなら、対応するfiltered pairのidentityが残る。全て「別情報」と一括扱いしない。v0.1には追加しない。

## Provisional案の批判的レビュー

| 条件 | 評価 | 本計画の提案と理由 |
|---|---|---|
| 8通貨 | 実務的なmajor subset。ただしG10全体ではない（NOK/SEKなし） | 維持を推奨。user ideaのscope・research efficiency。結果でEM等を追加しない |
| 1/1 calendar month | 最小で原研究にも存在するが最良horizonの証拠なし | 維持。prior evidence・research efficiency。intraday不調だけを月次選択の根拠にしない |
| ECB reference | 公的でcross計算に適するが約定値でなくrevisionもある | 維持はphenomenon用途のみ。source semantics |
| EUR numeraire、USD含む | `-log(q)`の符号は正しい。EUR=0は弱さの固定ではない | 維持。mathematical reason。USDを削除/常時cash化しない |
| 月末 | currency別last availableでは非同期crossが生じる | expected final TARGET operating dayを共通endpoint。欠けたcurrencyだけ前日へ戻さない。source semantics |
| missing date | material portion等が未数値化。holidayとunexpected gapが未分離 | deterministic calendar、skip cascade、coverage gateを仕様へ。research efficiency |
| 1999〜2026 pooled | EUR開始で便利だがpost-GFC弱化を旧時代が覆う可能性 | target2010以降のみを推奨。prior evidence。pre2010をsecondary勝者探しに使わない |
| 同一month-endからtarget開始 | 数学的conditional returnには使えるが公表後取引できたことにならない | **retrospective reference association**として明示。約定を偽装しない。causal executionは別契約。source semantics |
| calendar-year bootstrap | 年内依存に対応しても年境界の依存を切る。partial year weighting未定義 | calendar grid上の12-month circular moving-block bootstrapを固定提案。mathematical reason |
| positive進行 | net edgeを意味しない点は妥当 | evidence validity/data insufficiencyを先に判定。promoteは別screen設計のみ |
| 直ちに一回実行 | source/code/test/権限のgateが不足 | A–D → E → I → human freeze/readiness → X → R。research efficiencyと権限分離 |

本案は結果を見ずに作成した。変更理由は上表の4種類に限定。provisionalを正本化せず、新しいIDで推奨仕様を保存する。

## 最大のリスク

Scientific: 古い広い通貨basketのexcess returnを、post-2010 major単一pairのspot continuationに置き換えること。positiveでもtime-varying risk premium、factor loading、極端値の集中で説明可能。一般的momentumや「strength indicatorの独自edge」を立証しない。

shared endpointのreference rounding/measurement errorはformationとtargetへ逆符号で入るため、特にextreme選択で見かけのreversalを生む可能性もある。これは数学的な懸念であり本dataで確認した結果ではない。negativeを直ちにreversal機構の証拠にしない。反対に通貨別のpersistent unconditional driftだけでもselection meanがpositiveになり得るので、positiveを純粋なautocorrelationの証明にしない。

Data/execution: 観測日・14:10付近のrate setting・16:00付近のpublication・retrieval vintage・実行可能BID/ASKを同一時刻として扱うこと。最新のECB frameworkだけでは全historical日のavailabilityや無revisionを証明できない。

## 最小funnelとgate

1. **Pre-outcome qualification:** literature、failure、source、synthetic implementationを並列。重要contradiction未解決ならBLOCKED/HUMAN_BOUNDARY。adverse priorsだけでも独立した準備項目は最後まで処理。
2. **Fixed Discovery:** gate PASS後、一度のreference phenomenon screen。valid negativeはterminal for exact specification、weakはHOLD、不足はINSUFFICIENT_EVIDENCE。positiveを採用しない。
3. **Economic screen:** positiveの場合に限り別のoutcome-blind契約を作り、公表後のentry/exit、direct vs synthetic cross、BID/ASK、commission、slippage、financing/carryを確認。source不足ならBLOCKED、net不支持ならそのexecution仕様を終結。
4. **Factor decomposition:** economic screenと同時に仕様準備は可能。市場計算と判断はserial。carry/dollarの静的regressionだけでなくfactor momentumと残差continuationを区別。必要series/point-in-timeがなければHOLD。idiosyncratic根拠なしなら独自機構claimを拒否。
5. **Independent confirmation:** humanがunused sample/期間・最小効果・power・一回のruleを新しく固定。既存Discovery期間は消費済み。将来存在するdataによるprospective方式を優先し、LLM pretraining contaminationも限界として残す。
6. **Prospective shadow:** 別許可と契約がある場合のみ。今回は計画上の位置づけに留め、paper/live order、position sizingは含まない。

新規仮説を後から作るなら記録できるが、同一sampleのrescueや検証済み扱いは不可。negativeが出るたびにhorizonを変更するfunnelにしない。

## 比較の優先順位

| 比較 | 時期 | 判断 |
|---|---|---|
| A random pair | 最初に必要、解析的baselineのみ | uniform 56 ordered log pairsの平均は各月厳密0。Monte Carlo不要。risk-matched superiorityとは異なる |
| B pair-level momentum | 最初のdeterministic identity | 同じraw endpointなら同一選択。別戦略として重複検定しない |
| C top-k/bottom-k basket | positiveなら後続design候補 | kの事後探索禁止。diversification目的で別仕様/unused証拠が必要 |
| D vol-adjusted ranking | 現時点で不要 | 仮説変更。raw不調のrescueにしない |
| E time-series momentum | 現時点でempirical比較不要 | literature上区別し、fixed pair universe/sign/carry/riskを決めた別仮説が必要 |
| F spot vs carry-inclusive | positiveなら経済screenに必須 | carryによるsignal ranking変更は別仮説。政策金利を実際のrolloverと同一扱いしない |
| G pre-cost vs execution-aware | positiveなら最初に必要 | ECBへ想像のspreadを載せない。netが成立しなければconfirmationへの投資を止める |
| H factor-unadjusted vs controlled | positiveなら必須 | risk-factor exposureとfactor momentumの説明を分離。残差が無いなら独自signal claimは不可 |

## 人間が確定する具体契約

推奨仕様全文 `SPEC-CSM-002-v01` の承認が必要。特に (1) monthly・8通貨のbounded question、(2) target2010-01〜2026-09、(3) 同時境界reference associationのみでcausal executionを主張しないこと、(4) block length12・coverage80%/120 observations・sign/intervalのprogress rule を確定する。これらをworkerが変更して埋めない。

公開mainへのmergeや本計画の受領は、**それだけで市場outcome gate PASSにならない**。source/code identitiesと独立監査は後続成果が必要。将来holdout、broker economics、capital riskは本契約に含まれない。

## 未取得範囲と効率上の判断

原研究とTSMOMは原文を取得。Zhangのpublisher abstractとauthor factor-data案内、Iwanaga/Sakemotoのindexed publisher abstract/著者書誌まで確認したがfull text取得は403等で未完。Aに方法・sample・cost・G10の表を確認させる。ECB API docs/series画面は503、7 seriesの実データ取得・coverage確認は未実施。CはAPIと歴史的methodology/availabilityをqualifyする。GitHubコードは実行していない。negative記録は第三者報告であり独立replicationではない。

tick infrastructure、dashboard、MCP、broker接続は不要。ECB7 seriesの小さな固定snapshotと標準ライブラリ中心のscriptで十分。document保存・source metadata・合成testsに先に投資する。
