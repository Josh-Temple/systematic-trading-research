# Literature review result — currency-strength momentum v0.1

**Result status:** PARTIAL_WITH_GAPS  
**Review date:** 2026-10-01  
**Role:** Literature / scientific prior art only  
**Scientific status:** NOT_APPLICABLE — no market outcomes were computed in this review.

## Scope and provenance

- Packet: [PACKET_A_LITERATURE.md](https://github.com/Josh-Temple/systematic-trading-research/blob/36240da15fc83120d12d081c227f3e0dd8badaaa/research/lines/currency-strength-momentum-v0.1/work/packets/PACKET_A_LITERATURE.md), blob b995deb8430a681afd119050804e8bd79a212428.
- Proposal reference reviewed: research/csm-architecture-review-20261001 at 36240da15fc83120d12d081c227f3e0dd8badaaa.
- Main reference read at review start: 1bba695ea252863c3b7366b8b910aa36e211c325.
- The currency-strength line and architecture proposal are present on the proposal branch, not on main. The proposal is not frozen; the market-outcome gate is closed.
- Work is limited to literature synthesis. No FX observations, signal ranks, forward returns, strategy returns, costs, Sharpe ratios, subgroup results, or holdout results were computed. No specification or shared/canonical file was changed.

## Executive finding

The literature establishes that several distinct currency momentum constructs have appeared in research: cross-sectional winner-minus-loser portfolios, own-series time-series trend signals, conditional portfolios, and factor/basis strategies. They differ in the input return (spot change versus forward/excess return), the comparison set, currency universe, USD treatment, holding horizon, and transaction-cost model. Results from one construct do not identify the outcome of another.

The closest foundational cross-sectional evidence (Menkhoff et al., 2012) uses six currency baskets sorted across a broad and changing set of currencies. It reports separate spot-change and excess-return sorts. Its 15-developed-country net results are much weaker: the one-month formation / one-month holding excess-return portfolio is 0.79% annualized with t = 0.44 after quoted costs. The paper’s universe, period, and portfolio design do not match the proposed eight-currency, single-extreme, monthly ECB spot-reference association.

Modern evidence is mixed and design-dependent. Hutchinson et al. (2022) report that performance in their replication/out-of-sample setting disappears after publication of earlier predictability evidence. Iwanaga and Sakemoto (2025) state that conventional momentum portfolios have not generated positive average returns after the GFC, then report improvement from conditioning a multi-currency portfolio on forward discount, volatility, and dispersion. Fan et al. (2025) find that their separate basis-momentum strategy remains positive from 2011–2020, while their ordinary one-month currency-momentum benchmark is positive but statistically insignificant in that subperiod. These papers disagree less than their headlines suggest: they study different portfolios, conditioning rules, inputs, and evaluation windows.

**Implication for the fixed proposal:** retain a closed outcome gate. Literature supports treating the proposal as a testable, narrow association hypothesis; it does not validate a present-day net return, a single pair, or a tradable edge. No recommendation in the proposal is changed by this review.

## 1. Menkhoff, Sarno, Schmeling & Schrimpf (2012), “Currency Momentum Strategies”

Primary source: [BIS working-paper PDF](https://www.bis.org/publications/working-paper-366-currency-momentum-strategies.pdf); published in the Journal of Financial Economics 103(3), 624–640 (2012).

- **Data and universe (§3, pp. 9–12):** month-end spot and one-month forward quotes from BBI and Reuters via Datastream; January 1976–January 2010. The cross-section contains up to 48 countries over the sample, but observations vary as currencies enter, disappear, or become available. Extending the early history required combining USD-quoted BBI series with Reuters series quoted against GBP and converting to USD quotations. The effective number never reaches all 48; the paper reports a maximum below 40. This is broader than a stable major-currency panel and includes non-developed currencies.
- **Return definitions (§3, pp. 10–12):** for a USD investor, monthly excess return is approximately the one-month forward log rate minus the next month’s spot log rate, with the paper’s quote convention being foreign-currency units per USD. Spot log-rate change is also tracked separately. The two return concepts are therefore not interchangeable.
- **Signal and portfolio (§3, pp. 12–14):** at each month end, currencies are sorted into six equal-count portfolios using lagged returns over formation windows f = 1, 3, 6, 9, or 12 months. The paper separately sorts on past excess returns and past spot-rate changes, then generally evaluates High minus Low portfolios. Holding periods h = 1, 3, 6, 9, or 12 months are examined. This is a diversified cross-sectional basket design, not a single best-versus-worst bilateral pair.
- **Spot/excess distinction (§4.1, pp. 14–17):** both excess-return and spot-change sorts show momentum in the broad sample. The authors report that spot moves visibly contribute to their momentum portfolio; this does not make their forward/excess-return payoff identical to a spot-only outcome.
- **Transaction costs (§4.1, pp. 29–30; Table A.4, pp. 75–76):** turnover for the one-month formation/one-month holding High and Low baskets is 74.3% and 72.2% per month. Winners and losers carry about 2.5–7 basis points/month higher bid-ask spreads than the cross-sectional average. The paper cautions that BBI/Reuters quotes are indicative and relatively wide, so its net estimates understate profitability versus effective spreads; these are not modern executable-cost estimates.
- **Developed-country check (§6, p. 37; Tables A.12–A.13, p. 84):** the 15-developed-country subset has materially smaller momentum, described by the authors as basically nonexistent after costs. For the one-month formation / one-month holding sort, net excess return is 0.79% annualized, t = 0.44. The subperiod ends in 2010, so it is adverse context, not a test of the proposed 2010–2026 sample.
- **Limits to arbitrage (§5, pp. 29–35; §6, pp. 33–37):** the paper relates stronger returns to currency risk, volatility, and less developed/less liquid markets, and discusses limits to arbitrage. This motivates caution about transferring the broad-sample result to major currencies; it does not prove a particular mechanism for the proposed panel.

## 2. Moskowitz, Ooi & Pedersen (2012), “Time Series Momentum”

Primary source: [author/university-hosted journal PDF](https://fairmodel.econ.yale.edu/ec439/mosk.pdf), Journal of Financial Economics 104(2), 228–250.

- **Signal:** each instrument’s own past excess return determines its direction. The benchmark strategy uses the sign of that instrument’s prior 12-month excess return, holds for one month, and scales its position inversely with lagged ex-ante volatility. The volatility estimate is an exponentially weighted measure of lagged daily squared returns with a 60-day center of mass, applied with a one-period lag to avoid look-ahead (§2.4 and §3.2, pp. 232–234; §4.1, pp. 235–236).
- **Payoff/sample:** the paper studies futures/forward excess returns in 58 liquid instruments across asset classes, including currency forwards; the reported strategy evaluation is January 1985–December 2009. The monthly currency portfolio is not a cross-sectional rank of currencies against each other.
- **Spot and roll:** §6.3 (pp. 246–247) decomposes futures returns into underlying spot-price change and roll return and finds that both contribute to time-series momentum. This is another reason not to equate an own-series futures/forward excess-return result with a monthly spot-reference strength association.
- **Relevance:** supports keeping CS momentum, TS momentum, spot movement, and forward/roll payoff as separate evidence categories. It provides no direct result for the proposed one-month cross-sectional single-pair design.

## 3. Zhang (2022), “Dissecting Currency Momentum”

Primary routes: [publisher abstract](https://www.sciencedirect.com/science/article/abs/pii/S0304405X21002282); [author’s research-data page](https://sites.google.com/view/zhangshaojun/data); [SSRN working-paper record](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3643855).

- The publisher abstract says carry and dollar factors are strongly autocorrelated; cross-sectional and time-series currency momentum summarize that factor autocorrelation; factor momentum explains currency momentum; idiosyncratic currency returns contain little momentum; and factor volatility helps explain the pattern.
- **Full-text attempt:** author/SSRN PDF routes returned HTTP 403 in this review; the publisher surfaced the abstract only. The author’s page confirms that a December 2020 spreadsheet contains factor-momentum, momentum, time-series-momentum test portfolios, and carry/dollar factors, but the data were not downloaded or analyzed.
- **Not verified:** exact estimation window/timing, sample dates, developed/G10 decomposition, static-regression specifications and residual diagnostics, and whether/when the factor estimates are point-in-time. No conclusions about those details are inferred from the abstract.
- **Relevance:** this is a reason to treat common carry/USD-factor movement as an alternative explanation, not evidence that the proposal has been factor-neutralized or that a single-pair spot signal is explained by these factors.

## 4. Iwanaga & Sakemoto (2025), “Conditional currency momentum portfolios”

Primary source: [publisher article/abstract](https://www.sciencedirect.com/science/article/abs/pii/S1057521925000511), International Review of Financial Analysis 99, 103964, DOI 10.1016/j.irfa.2025.103964; [author-listed SSRN version](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4411616).

- Publisher abstract: conventional currency momentum portfolios have not generated positive average returns after the GFC. The authors condition a one-month momentum portfolio on average forward discount, currency-market volatility, and portfolio return dispersion; they report going long only when the forward discount is positive and volatility and dispersion are low.
- Publisher/author indexed text describes a USD-investor portfolio over the ten most liquid currencies, using monthly portfolio formation, daily spot and one-month forward data, and bid/ask-cost adjustments.
- **Full-text attempt:** SSRN PDF and publisher full-text routes were not retrievable in this review. Exact sample dates, post-GFC split definition, currency membership, cost magnitudes, and whether conditioning thresholds were fixed ex ante, estimated in a training set, or evaluated on the same sample remain unverified. The headline improvement is an abstract-level report about a conditional portfolio, not a net return estimate for one currency pair.

## 5. 2020–2026 replication, reassessment, and adjacent candidates

The screen below distinguishes direct replication/reassessment from related but different portfolio designs.

| Study | Regime/sample evidence visible in primary source | Relation to proposed question | Retrieval boundary |
|---|---|---|---|
| Hutchinson, Kyziropoulos, O’Brien, O’Reilly & Sharma (2022), “Are carry, momentum and value still there in currencies?” [publisher](https://www.sciencedirect.com/science/article/pii/S1057521922002058) | Abstract reports a replication/out-of-sample average Sharpe decline from +0.39 to −0.32 after publication of evidence on currency predictability and no excess-return autocorrelation in the later period. | Direct reassessment of currency carry/momentum/value families, but not an identified test of this exact 8-currency spot-only single pair. | Abstract available; accepted manuscript/PDF route returned 403. Exact dates, universe, and cost assumptions not verified here. |
| Harris, Shen & Yilmaz (2022), “Maximally predictable currency portfolios” [publisher](https://www.sciencedirect.com/science/article/pii/S026156062200105X) | Publisher/author-repository abstract describes an out-of-sample G10 USD-investor portfolio from February 1994 to December 2020 and says MPP outperformed simple momentum and equal-weight comparators; indexed full-text snippet says MPP did particularly well after 2008 while the momentum portfolio declined. | Counterpoint that some G10 currency portfolio predictability can persist, but MPP is a multivariate optimized portfolio, not ordinary CS momentum or a max/min pair. | Publisher and university repository abstract/snippet available; university PDF returned 403, so details beyond indexed text are not audited. |
| Fan, Han, Li & Liu (2025), “Understanding the Performance of Currency Basis-Momentum” [full text](https://onlinelibrary.wiley.com/doi/full/10.1111/eufm.12555) | 48-currency, quintile WML basis-momentum portfolios; spot/1m/2m forwards; strategy returns begin December 1986 and end October 2020. For Jan 2011–Oct 2020, BM-3 is 0.62% monthly (t = 5.36), while the ordinary one-month momentum benchmark is 0.27% (t = 1.42). | Relevant post-GFC counterevidence, but basis-momentum uses forward-curve information and a diversified five-portfolio WML spread. Even its ordinary momentum comparator is a basket strategy and is not significant at conventional 5% levels in that subperiod. | Full text retrieved. It does not cover the post-2020 policy-normalization period. The 2011–2020 split overlaps the low-rate/ZIRP era and cannot isolate monetary-policy regimes. |
| Zeng (2025), “Currency Carry, Momentum, and Global Interest Rate Volatility” [publisher](https://doi.org/10.1017/S0022109023001485) | Publisher abstract argues that carry and momentum returns compensate for global interest-rate-volatility exposure. | Factor-risk interpretation, not a single-pair spot-momentum replication. | Abstract only; sample, universe, and cost detail not verified in this review. |
| Liu (2026), “How to maximize momentum returns in foreign exchange markets?” [publisher](https://www.sciencedirect.com/science/article/abs/pii/S0261560626000513); [SSRN record](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5321067) | Publisher abstract/search excerpt describes 42 countries, six-month holding periods, momentum followed by reversal, and double sorts based on past winners/losers’ skewness or kurtosis. | Recent broad currency-momentum/reversal candidate with a different holding horizon and portfolio refinement; it does not establish a one-month single-pair spot result. | Publisher abstract and SSRN indexed excerpt available; full PDF open returned 403. Exact sample dates, G10/post-GFC breakdown, costs, and point-in-time conditioning are unverified. |
| Iwanaga & Sakemoto (2024), “Cross-momentum strategies in the equity futures and currency markets” [publisher](https://www.sciencedirect.com/science/article/pii/S0261560624001578) | Publisher page describes a cross-asset portfolio approach linking equity-futures and currency momentum. | Related cross-asset strategy, not currency-only single-pair strength. | Publisher abstract/page and an author-hosted working-paper result were found; no full cost/regime audit in this task. |
| Sakemoto & Suda (2026), “Cross-sectional currency momentum and order flow” [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6618279) | Authors’ abstract says momentum spreads vary with spot/forward/swap order flow and maturity, with higher spread in a double sort using short-term swap buying pressure and past return. | New conditional WML working paper; not an unconditioned spot-strength pair test. | Working-paper abstract only; not peer reviewed at review time; sample, costs, and full design not independently checked. |
| Della Corte & Riddiough, “Currency Factors” companion data [author site](https://sites.google.com/view/currencyfactors/home) | First-party factor-data page advertises gross/net excess-return factors and 1/3/6/12-month momentum WML portfolios through June 2026. | Useful source-availability and factor-definition lead; it is not an independent replication and its excess-return WML series is not the proposed spot association. | Dataset values were not downloaded or analyzed, consistent with the packet’s no-outcomes rule. |

### Regime coverage

- **Pre-GFC / broad historical:** Menkhoff et al. use 1976–2010; most of that sample predates the post-GFC and post-2010 periods now at issue.
- **Post-GFC:** Iwanaga–Sakemoto’s abstract reports conventional portfolio weakness after the GFC. Fan et al. show a different post-GFC result for basis-momentum through October 2020 and a weak/insignificant ordinary one-month momentum basket over Jan 2011–Oct 2020.
- **Post-2010:** Fan’s Jan 2011–Oct 2020 split is the clearest retrieved, dated post-2010 comparison among the reviewed primary full texts.
- **ZIRP / low-rate era:** the 2011–2020 window overlaps a prolonged low-rate era, but none of the retrieved comparisons here identifies a clean ZIRP-only estimate for the proposed spot statistic.
- **Policy normalization / post-2021:** no retrieved full-text replication here isolates the 2021–2026 normalization period for the proposed 8-currency, one-month spot-strength association. A 2026 article or factor dataset with a later end date does not establish that regime result unless its exact sample and construction are verified.

## 6. Design comparison matrix

| Dimension | Main literature constructs | Proposed fixed question | Transfer limit |
|---|---|---|---|
| Portfolio shape | Menkhoff et al.: six equal-count baskets and High minus Low. Other modern work often uses quintile/WML portfolios or conditional portfolios. | A single extreme currency pair/relative comparison within eight currencies. | A basket spread averages many currencies; a single extreme pair has less diversification and can be dominated by one currency. Basket evidence is not a pair-level estimate. |
| Ranking input | Separate sorts on lagged spot changes and lagged excess returns (Menkhoff); factor or basis-momentum uses carry, forward, or factor inputs. | ECB reference spot changes define the narrow spot-strength association. | Forward discount, interest, roll, and funding components are absent from spot-only ranking/payoff; conversely, a spot association is not the literature’s investable forward excess return. |
| USD treatment | Many studies define all foreign currencies from a USD-investor perspective; dollar-neutral WML spreads cancel a common USD component. | USD is itself one of the eight currencies (AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD) and serves in bilateral comparisons. | Including USD as a ranked currency is not identical to using USD as a common numeraire or benchmark. The literature’s dollar-neutrality does not automatically carry over. |
| Common factors | Carry and dollar factors; factor momentum; time-series trend; basis/forward-curve components; conditional risk states. | No causal or factor-neutral claim is authorized by the fixed spot-association question. | A raw association may reflect common USD, carry, or other shared drivers. Literature provides candidate explanations, not an estimate for this proposal. |
| Payoff and horizon | Monthly portfolio sorting may be combined with forward excess returns and overlapping holding windows; TSMOM uses own-series sign with vol scaling; basis momentum uses first/second forward maturities. | One calendar-month formation and one calendar-month target using reference spot series, fixed Discovery sample 2010-01 through 2026-09. | Signal horizon can match while return definition, portfolio, data timing, cost basis, or tradability remains different. |

## 7. Evidence balance and effect on the proposal

**Support for a narrow research question**
- Foundational and later work documents return continuation in some currency portfolios and spot changes.
- The literature shows that spot and forward/excess-return results can be reported separately; a spot-only descriptive question is scientifically legible if it stays distinct from a tradable return claim.
- Modern work continues to study FX momentum and its conditional, factor, and cross-asset variants.

**Contrary evidence**
- Developed-country net results in Menkhoff et al. are weak, and their strongest historical broad-sample results rely on a much larger and more heterogeneous universe.
- Hutchinson et al. report a deterioration/disappearance of strategy performance in their replication and later out-of-sample period.
- Iwanaga and Sakemoto’s abstract says conventional momentum portfolios were not positive after the GFC.
- In Fan et al., the regular one-month momentum WML comparator is not statistically significant over Jan 2011–Oct 2020, despite positive basis-momentum results.

**Uncertainty that remains**
- The exact proposed eight-currency panel, one-month single-extreme association, ECB reference observation convention, and 2010–2026 period have not been directly established by the retrieved papers.
- Full-text gaps prevent checking Zhang’s regression/timing/sample details and Iwanaga–Sakemoto’s conditioning/evaluation separation. Several 2025–2026 candidates were available only as abstracts or indexed excerpts.
- No reviewed source establishes an independent, prospective, untouched test of this exact statistic or its performance after implementation costs.
- Publication effects, sample selection, limited full-text access, indexing gaps, and the literature’s emphasis on publishable positive results can bias a rapid prior-art screen.

**Recommendation to the fixed proposal:** keep the proposal and its gate as written. Treat this review as support for a careful hypothesis and taxonomy, not as a result or an authorization to calculate outcomes. Any later outcome work requires the separately specified human freeze and audit/gate process. Use an independent unused or prospective evaluation segment if that later gate is opened; do not tune the fixed question on the literature screen.

## 8. Search and model limits

This is a dated, source-traceable screen rather than an exhaustive systematic review. Search-engine indexing is incomplete and changes over time. Publisher or SSRN access controls prevented full-text review of several studies. Literature retrieval can miss working papers, non-English sources, unpublished null results, or differently named research.

No claim is made from unverified model memory. All factual statements above are tied to a linked paper, publisher/author abstract, or cited section. Abstract-level findings are labelled as such; inaccessible full-text details are marked unverified rather than inferred. The review does not derive, reproduce, or validate any market outcome, and does not replace an independent replication or prospective test.

## References

- Menkhoff, L., Sarno, L., Schmeling, M., & Schrimpf, A. (2012). “Currency Momentum Strategies.” Journal of Financial Economics 103(3), 624–640. [BIS working-paper PDF](https://www.bis.org/publications/working-paper-366-currency-momentum-strategies.pdf).
- Moskowitz, T. J., Ooi, Y. H., & Pedersen, L. H. (2012). “Time Series Momentum.” Journal of Financial Economics 104(2), 228–250. [University-hosted PDF](https://fairmodel.econ.yale.edu/ec439/mosk.pdf).
- Zhang, S. (2022). “Dissecting Currency Momentum.” Journal of Financial Economics 144(1), 154–173. [Publisher abstract](https://www.sciencedirect.com/science/article/abs/pii/S0304405X21002282).
- Iwanaga, Y., & Sakemoto, R. (2025). “Conditional currency momentum portfolios.” International Review of Financial Analysis 99, 103964. [Publisher page](https://www.sciencedirect.com/science/article/abs/pii/S1057521925000511).
- Hutchinson, M. C., Kyziropoulos, P. E., O’Brien, J., O’Reilly, P., & Sharma, T. (2022). “Are carry, momentum and value still there in currencies?” International Review of Financial Analysis 83, 102245. [Publisher page](https://www.sciencedirect.com/science/article/pii/S1057521922002058).
- Harris, R. D. F., Shen, J., & Yilmaz, F. (2022). “Maximally predictable currency portfolios.” Journal of International Money and Finance 128. [Publisher page](https://www.sciencedirect.com/science/article/pii/S026156062200105X).
- Fan, M., Han, X., Li, A., & Liu, J. (2025). “Understanding the Performance of Currency Basis-Momentum.” European Financial Management 31(5), 1652–1678. [Full text](https://onlinelibrary.wiley.com/doi/full/10.1111/eufm.12555).
- Zeng, Y. (2025). “Currency Carry, Momentum, and Global Interest Rate Volatility.” Journal of Financial and Quantitative Analysis 60(2), 839–873. [Publisher page](https://doi.org/10.1017/S0022109023001485).
- Liu, Y. (2026). “How to maximize momentum returns in foreign exchange markets?” Journal of International Money and Finance 164, 103566. [Publisher page](https://www.sciencedirect.com/science/article/abs/pii/S0261560626000513).
- Iwanaga, Y., & Sakemoto, R. (2024). “Cross-momentum strategies in the equity futures and currency markets.” Journal of International Money and Finance 148, 103170. [Publisher page](https://www.sciencedirect.com/science/article/pii/S0261560624001578).
- Sakemoto, R., & Suda, S. (2026). “Cross-sectional currency momentum and order flow.” [SSRN working-paper record](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6618279).
