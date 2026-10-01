---
id: SPEC-CSM-002-v01
type: Specification
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: HUMAN_BOUNDARY
freeze_status: PROPOSED_NOT_FROZEN
tests_hypothesis: HYP-CSM-002
data_roles_allowed:
  - EXPLORATORY_DISCOVERY
relations:
  - type: tests_hypothesis
    target: HYP-CSM-002
---

# One fixed monthly reference-rate Discovery screen — proposed contract

これは一意に指定した推奨案。人間確定と準備gate以前に実行しない。結果前の変更はreason/old/newを記録した別versionへ。結果後は本仕様を改変しない。

## 1. Question、scope、predictor、target

「固定8通貨において、前calendar monthのspot log appreciationが最大の通貨を最小の通貨に対して選んだ場合、翌calendar monthの同期ECB reference-to-reference spot log returnの平均は正か」。対象はretrospective latest-vintage association。public informationから実際にentryできた収益を問わない。

Universe: **AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD**（N=8）、全56 directed pairs i≠j、no restriction/filter。8通貨はG10 subsetでありG10全体ではない。

Target months: **2010-01 through 2026-09 inclusive**。formation monthは各targetの直前月、1 calendar month。source price boundaryは **2009-11-01 through 2026-09-30**。pre2010 target、Oct2026以降、era/subgroup別性能を計算しない。全期間を見て良い年代を選ばない。

Source family: ECB EXR daily、7 keys `D.CCY.EUR.SP00.A`、CCY=AUD/CAD/CHF/GBP/JPY/NZD/USD。EURはq=1のsynthetic numeraire constant（観測済み価格を作るという意味ではない）。source substitutionは不可。同じEXRの別公式transportはsource qualificationでidentityを確定しgate前にlockする。

## 2. Expected month-end date、holiday、missing

各月mのe_mは、そのcalendar monthにおける**最後の予定されたTARGET operating day**。calendar timezoneはEurope/Berlinによる日付ラベル、weekendと公式TARGET closing datesで決める。Cは2009-11〜2026-09のoperating-day calendarを公式資料で確認しhashをfreezeする。future価格の存在からe_mを選ばない。

calendarを確定できない、historical適用に重要な不一致がある場合はBLOCKED。worker独自のholiday推測や「最後に残った行」への置換は禁止。

e_mに7 non-EUR currencies全てが有効（numeric、finite、strictly positive、非欠測status）でなければ、month-end vectorをUNAVAILABLEとする。currency別前日rollback、他日から補完、monthly averageへの代用は不可。休日の欠行はexpected、operating dayの欠行はunexpectedとして数える。

duplicate date/key、currency/unit取り違え、negative/zero/nonfinite OBS_VALUE、unexpected schema/statusはfail-closed SOURCE_INVALID。許可するOBS_STATUS codeのexact mappingはCが公式定義からsource lockへ記録する。scientific missing rule変更権限ではない。

target monthkに必要なvectorはe_(k-2), e_(k-1), e_k。どれか欠ければtarget slotはskip、そのreasonをcalendar gridに残す。欠けたmonthをdropしてshiftを詰めることは禁止。whole missing monthでも以降のcalendar horizonは変えない。

first/last boundariesを勝手に切り直さない。sourceが想定より短ければ不足を記録し、provider/期間を変更しない。

## 3. Signalとpair construction

q_i(d)=currency i units per1EUR。non-EURについてv_i(d)=-ln(q_i(d))、v_EUR=0。

target monthkのformation score:

`s_i(k) = v_i(e_(k-1)) - v_i(e_(k-2))`。

strongest a=argmax s、weakest b=argmin s。unique extremaでなければslotをTIED_EXTREMEとしてskip。near-tieのeconomic thresholdを導入しない。

数学的exact tieは可能な限り入力decimalから形成したexact ratio `q_i(old)/q_i(new)` のcross-multiplicationで判定する（EUR ratio1）。log浮動小数点の偶然のroundingでtieを作らない。implementationはdecimal/rational parseとdeterministic orderingを使う。internal currency orderingは上記ISO順、tieのdiscretionary selectionはしない。

pair P_ab=q_b/q_a（b units per a）を買う方向。brokerの慣例quoteが逆ならsell逆pairに相当するが、本testはbroker symbolを必要としない。reference synthetic crossesを「取引可能な28cross」と主張しない。

## 4. Outcomeとtemporal boundary

`y_k = [v_a(e_k)-v_a(e_(k-1))] - [v_b(e_k)-v_b(e_(k-1))]`。

単位はlog return、reportは10000*y_kのlog basis points。pairのsimple return `exp(y)-1`、dollar-funded basket P/L、Sharpe、leveraged performanceへ変換しない。

selectionにe_kまたはその月内の情報を使わない。event ledger（a,b、formation endpoints、score identities、skip reasons）を先にpersist/hashしてからyを計算する。全時系列をdeterministic loaderが読む場合もsignal functionへfuture valuesを渡さない。未来suffixを極端に変えても過去signalが不変というtestを通す。

e_(k-1)のreferenceはformationの終点とtargetの始点を兼ねる。これは**同時境界の統計的associationを定義するための共有値**であり、そのrateの公表前に取引した仮定ではない。publication time>=setting timeなので同rateでのcausal entry claimは禁止。AVAILABLE_ATやhistorical original vintageが不明ならUNKNOWNとして保存し、DATEに16:00等を架空で付けない。

holding target intervalはcalendar隣接monthly endpoints、互いにoverlapしない。signal sharing、serial dependence、regime dependenceが消えるとはみなさない。

## 5. Baseline/comparator

Primary reference null: mean(y)<=0対positive continuationというscreen。観測meanはunconditional risk premium/exposureでも生じ得るため、pure serial predictabilityやcausal mechanismの証明としない。

Uniform random ordered pair（8*7=56）を同じendpointsのlog returnで評価した期待値は各slotで0：全方向のpair差は符号反転でcancel。sampled random backtestは不要。これはmean比較の解析的baselineであり、risk-matched profitability比較ではない。

Formationの全56 pair最大選択はa,bと一致することをsynthetic test/assertionで確認。独立strategy/comparatorとして重複計算しない。basket、TSMOM、vol-adjusted、carry rankingは計算しない。

## 6. Metrics、dependence、precision

Primary: eligible targetsのarithmetic mean spot log return（bps）。secondary descriptiveのみ: median、positive proportion(y>0、zeroはpositiveに含めない)、eligible count、scheduled count、skip count/reason、endpoint date/status coverage。per-period outcome ledgerは保存するがbest/worst periodやcurrency/subgroup performanceを集計しない。

Dependence interval: **circular moving-block bootstrap、block length12 calendar slots、10000 replicates、seed20261001**。

完全calendar gridのlengthNを維持しmissing slotはNone。Python stdlib `random.Random(20261001)`で各replicateにceil(N/12)個のstart indexを`randrange(N)`からdraw、startから12 slotsをmoduloNで連結しNに切り詰める。resampled gridのvalid yだけでmeanを計算。valid0のreplicateが一つでもあればinferenceをFAILEDとしrule判定しない。retry/different seed/blockは禁止。

10000 meansを昇順にsort、percentileはtype7 linear interpolation：h=(B-1)*p、floor(h)と次の値を小数部で補間、p=.025/.975。medianもtype7 p=.5。intervalは二側95%。bootstrap algorithm/runtime versionをlockする。12は年間をまたぐserial dependenceを保持するための固定設計であり、結果で選んだ最適blockではない。

このintervalにはweak stationarity/依存構造への近似がある。structural break、partial2026、rounded references、selection concentrationを解決しない。independent confirmationの代用にはしない。iid pair observationsや56pairをsample sizeとしない。1月が1観測。

## 7. Data sufficiencyとdecision rule

初期実装・source無効はscientific resultではない。raw snapshot/code/calendar mismatch、failed identity assertion、outcome exposure前のprotocol不一致、forbidden accessがあればSTOP、evidence INVALID/PARTIAL、scientific NOT_APPLICABLE。

有効n<120、eligible n/scheduled N<.80なら、metricsを予定通り保存して **INSUFFICIENT_EVIDENCE / HOLD**。これはpower保証でなくminimum operational sample基準。sample延長/period変更で救済しない。

有効coverageを満たす場合:

- mean<=0: exact specificationについて **NOT_SUPPORTED**、Decision **DEPRIORITIZE**。interval upper<0ならadverse continuation evidenceと記述できるがreversal strategyを検証済みにしない。
- mean>0かつlower<=0: **INCONCLUSIVE / HOLD**。
- mean>0かつlower>0: **PROMISING_EXPLORATORY**（line-local bounded label）、Decision **ADVANCE_TO_SEPARATE_ECONOMIC_SCREEN_DESIGN**。
- nonfinite metric、bootstrap失敗、必要artifact保存不成功: operational failureとしてSTOP。scientific判定をせずpreserve attempts。

「negativeでdeprioritize」は推定平均の符号による資源配分rule。低powerのnull結果から普遍的なedge不存在を断定しない。弱いpositiveが出たときだけsampleを延長して有意になるまで見ることは禁止。

## 8. Cost boundary

Spread, slippage, commission, financing, rollover, realised carry=**UNOBSERVED**。zero costを「実費0」と表示しない。fees控除やassumed spread threshold、annualized strategy return、Sharpe、position sizingは出さない。

monthly targetはrebalance cadenceのresearch analogueに過ぎない。同pair維持・turnover netting・funding daysは本screenに無い。positive後のeconomic contractで実際のtrade constructionをfreezeする。

## 9. Stopping / forbidden search

計画familyにempirical strategy1本、market outcome execution1回。horizon/universe/time-of-month/vol/smoothing/filter/subperiod/side/seed/block searchなし。source selectionを性能で選ばない。same sampleをnew ruleの選別へ使わない。

failed attemptがoutcomeを一切返さず科学inputs不変なら別attempt IDでtechnical retry可。metricや一部outcomeが計算/閲覧されればaccessを記録し、partial/consumed boundaryを保持する。code修正後のrerunは独立confirmatory evidenceではなくcorrection/reproduction。勝ちになるまでrerun禁止。

## 10. Freeze receipt必須fields

Human contract decision ID、spec bytes SHA256、hypothesis ID、source lock ID/transport/series/unit/status map、expected calendar hash、raw capture process、dataset role/time range/access ledger、code commit/file hashes、environment versions、synthetic tests/result hashes、E audit identity、I gate receipt、primary/comparator/decision rule、run ID、outcome access owner。

source readinessは最初にroute/schemaをqualifyし、Xのraw capture後・return計算前にactual hash/coverage/identitiesを再照合する二段階。新しいscience変更を発見したらgate無効。Integratorが黙って最終条件を選ばない。
