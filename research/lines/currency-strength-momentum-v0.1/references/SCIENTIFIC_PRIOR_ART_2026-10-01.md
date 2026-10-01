---
id: REF-CSM-SCI-002
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PARTIAL_PRIMARY_SOURCE_REVIEW
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: NOT_APPLICABLE
relations: []
---

# Scientific prior-art result

一次資料の確認範囲を示す初回結果。網羅的reviewやreplicationではない。Worker Aは残るfull-text gapと近年研究を完了する。第三者論文のoutcome閲覧は許可されるが、本lineのmarket data/outcomeは未取得・未計算。

## Menkhoff, Sarno, Schmeling, Schrimpf (2012)

Currency Momentum Strategies, JFE 106(3), 660–684. DOI: 10.1016/j.jfineco.2012.06.009。

Source: [institutional full text](https://openaccess.city.ac.uk/id/eprint/3296/1/Currency%20Momentum%20Strategies.pdf)、[BIS working paper](https://www.bis.org/publications/working-paper-366-currency-momentum-strategies)。institutional版はfinal published versionとの相違の可能性が明記されている。

**FACT:** Broad historical cross-sectionのlagged excess returnでwinner/loser portfoliosを構築。formation/holdingの複数horizon、spot contribution、取引費用も検討。本文§3のsampleは1976:1–2010:1。§developed countriesとAppendix A.12–A.14ではdeveloped subsetの効果・net収益が弱い。

**INTERPRETATION:** 一般的currency momentumに根拠はあるが、major-onlyへの外挿に原論文自身が注意を与える。1/1は低費用screenのpriorとして使える。

**LIMITATION:** excess-return sorting、広いbasket、古い期間、indicative bid/askによる費用は、ECB spot ranking、8通貨k=1、近年retail executionとは異なる。本文のfactor regressionで未説明という結果を、factor momentum不存在の証明にしない。

## Moskowitz, Ooi, Pedersen (2012)

Time Series Momentum, JFE 104(2), 228–250. DOI: 10.1016/j.jfineco.2011.11.003。

Source: [author-hosted paper](https://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf)。原文取得。

**FACT:** 多assetのfutures/forwardsを対象とするown-return signal。12-month excess-return sign、volatility-scaled positionの例があり、spotとroll yield contributionも分ける。

**INTERPRETATION:** 中期continuationの研究文脈になる。cross-sectionのmax/minを選ぶ本testとはsignalもpayoffも違う。

**LIMITATION:** pooled evidence、diversification、contract returnを8通貨spot単一crossに持ち込まない。1-month rankingが同じ効果を持つとは示していない。

## Zhang (2022)

Dissecting currency momentum, JFE 144(1), 154–173. DOI: 10.1016/j.jfineco.2021.05.035。

Source: [publisher abstract](https://www.sciencedirect.com/science/article/abs/pii/S0304405X21002282)、[author data page](https://sites.google.com/view/zhangshaojun/data)。full textは未取得（publisher/SSRN access failure）。data downloadはしていない。

**FACT:** abstractはcarry/dollar factorのautocorrelationがcross-sectional/TS currency momentumを説明するという主張を示す。著者はfactor momentum、momentum、TSMOM、carry/dollar factor seriesのDecember2020更新版を案内。

**INTERPRETATION:** static factor alphaだけではmechanism切り分けが不十分。positiveならfactor momentum・残差を別途検討すべき。

**LIMITATION:** exact sample、G10限定表、return construction、estimationのpoint-in-time性はfull textから未確認。本lineのpositiveをこの論文だけでfactor-onlyと断定できない。

## Iwanaga, Sakemoto (2025)

Conditional currency momentum portfolios, IRFA 99, 103964. DOI route [publisher](https://www.sciencedirect.com/science/article/pii/S1057521925000511)、[author bibliography](https://sites.google.com/site/rsakemotohomepage/reserach)、[working paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4411616)。publisher indexed abstractと著者書誌を確認、full text未取得。

**FACT:** abstractはpost-GFCで通常のmomentum portfolioがpositive returnを生成しなかったと報告し、conditional portfolioを提案する。

**INTERPRETATION:** 原研究以降の時代変化を明示的に扱う必要がある。post-2010を第一screenの対象にする推奨理由。

**LIMITATION:** exact crisis split、currency coverage、cost、conditioningの学習/評価分離は未確認。post-GFCとZIRPとpost-2010は同義ではない。conditional手法を模倣して同じsampleを救済しない。


## Hutchinson et al. (2022) — post-2010 adverse prior

Are carry, momentum and value still there in currencies? *International Review of Financial Analysis* 83 (2022), 102245. DOI: 10.1016/j.irfa.2022.102245. [Author-accepted full text at Queen's University Belfast](https://pureadmin.qub.ac.uk/ws/portalfiles/portal/359418115/1_s2.0_S1057521922002058_main.pdf).

**FACT:** The study examines highly liquid G11 currencies against USD and reports that the performance of currency carry, cross-sectional momentum and time-series momentum weakens/disappears out of sample. Its post-publication analysis includes January 2010–April 2020; its cross-sectional momentum signal sorts cumulative currency excess returns and constructs currency portfolios, with a three-month formation/one-month holding core specification and a broader set of parameterizations. The authors also report no relation between past and future currency excess returns in their out-of-sample pooled tests.

**INTERPRETATION:** This is a material adverse prior for a post-2010 momentum proposition. The planned 2010–2026 window overlaps known published outcome evidence, so it is a narrow historical replication/translation of the single-extreme spot-reference question, not an independent or novel confirmation. The reason to retain one fixed screen is to examine this materially different definition at low cost.

**LIMITATION:** The study's portfolio construction, excess-return predictor/payoff, USD reference, data sources, and portfolio aggregation are not the exact raw spot strongest-versus-weakest pair on ECB reference rates. Its aggregate deterioration and currency-level regressions do not directly settle the planned single-extreme specification. Worker A must report the precise specifications and avoid treating the published aggregate result as the exact answer here.

## Recent-study search receipt

2026-10-01、"currency momentum" + post/2010/2024/2025、"G10"、原論文名を検索。2025のbasis-momentum、currency carry/global interest-rate volatility、conditional momentum、2026のmaximizing FX momentumの候補が見つかった。いずれも今回の8通貨1/1単一pairの最新replicationとして確認できていない。title/snippetからscopeを推測して結果を採用しない。

Worker Aは上記候補を一次資料でscreenし、G10/major-only、post-GFC/ZIRP/利上げ後、transaction cost、negative/nullを別項目で最後まで調べる。未発見は「不存在」ではなくSEARCH_GAP。

## Spot、carry、total return

今回yはpairのspot log price change。実際のfunded spot tradeの損益ではない。共通quoteでlog spot changeをr、観測したforeign/domestic deposit growth differentialをcとすればfrictionlessのexcess-return近似/構成はr+c。USD per foreign単位のforward Fならlong foreign forward log excess returnは `log(S_next)-log(F_now)`。counterquoteなら符号が逆。forward points、deposit rates、broker rolloverは同じ観測値ではない。

carryをoutcomeに含めることと、carryでpredictorをsortすることは異なる。BISのtrade-weighted effective exchange rateやFed broad dollar indexをそのまま学術的carry/dollar factorへ代用しない。

## Evidence conclusion

**FACT:** 文献上のmotivation、major-onlyのadverse evidence、factor explanation、近年の弱化を扱う研究がある。

**INTERPRETATION:** 現在の8通貨にedgeがあるというpriorは弱い。低費用の固定screenは情報を増やせるが、large infrastructureを先行する根拠はない。

**LIMITATION:** 最新文献を網羅したとは主張しない。本lineの市場結果、統計量、現在のstrongest/weakestは計算していない。
