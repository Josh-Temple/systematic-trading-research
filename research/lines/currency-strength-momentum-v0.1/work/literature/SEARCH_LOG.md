# Search log — currency-strength momentum literature packet

Review date: 2026-10-01  
Repository: Josh-Temple/systematic-trading-research  
Reviewed proposal commit: 36240da15fc83120d12d081c227f3e0dd8badaaa  
Main snapshot read at start: 1bba695ea252863c3b7366b8b910aa36e211c325  
Search mode: web search for discovery and primary-source retrieval. Secondary-index pages were used only to locate publication or author records; factual findings in RESULT.md are attributed to paper/publisher/author records. No market dataset was downloaded or calculated.

## Search queries run on 2026-10-01

The following exact query strings were sent to the web search service. System 1 and System 2 are separate search passes.

### System 1

1. `currency momentum replication post 2010 post global financial crisis 2022 currency carry momentum value still there`
   - Found Hutchinson et al. (2022) publisher abstract, which reports a replication/out-of-sample Sharpe decline and later-period loss of currency excess-return autocorrelation.
2. `site:sciencedirect.com "Conditional currency momentum portfolios" Iwanaga Sakemoto 2025`
   - Found the Elsevier article page/abstract for Iwanaga & Sakemoto (2025), article 103964; full text was not retrievable.
3. `2025 basis momentum currency momentum 2026 foreign exchange momentum paper publisher`
   - Found Wiley full text for Fan et al. (2025) and publisher-indexed 2026 FX momentum article by Yi Liu.
4. `2026 currency momentum FX order flow cross-sectional currency momentum primary paper`
   - Found the 2026 Sakemoto & Suda SSRN working-paper abstract.

### System 2

1. `"Dissecting Currency Momentum" Zhang 2022 abstract factor momentum carry dollar`
   - Found the publisher abstract, SSRN record, author research-data page, and institutional working-paper record for Zhang (2022).
2. `"Maximally predictable currency portfolios" G10 out of sample 1994 2020 publisher`
   - Found the publisher page and University of Bristol record/PDF for Harris, Shen & Yilmaz (2022).
3. `"How to maximize momentum returns in foreign exchange Markets" 2026 Liu publisher`
   - Found the publisher article page and SSRN working-paper version; publisher and SSRN full-PDF retrieval was not achieved.
4. `"Cross-momentum strategies in equity futures and currency markets" 2024 publisher`
   - Found the publisher page and an author-hosted working-paper result for Iwanaga & Sakemoto (2024).

## Primary-source retrieval and access log

| Source | Primary/first-party route checked | Retrieval outcome | Use in result |
|---|---|---|---|
| Menkhoff et al. (2012), Currency Momentum Strategies | BIS working-paper PDF, https://www.bis.org/publications/working-paper-366-currency-momentum-strategies.pdf | Full PDF retrieved and searched; sections 3, 4.1, 5, 6 and appendix tables A.4, A.12-A.14 reviewed. | Core historical CS, spot/excess, turnover/cost and developed-subset evidence. |
| Moskowitz, Ooi & Pedersen (2012), Time Series Momentum | Yale/university-hosted journal PDF, https://fairmodel.econ.yale.edu/ec439/mosk.pdf | Full PDF retrieved and searched; §§2.1-2.4, 3.2, 4.1, 6.3 reviewed. | TS signal/payoff, lagged volatility scaling and spot/roll decomposition. |
| Zhang (2022), Dissecting Currency Momentum | ScienceDirect publisher abstract; author page https://sites.google.com/view/zhangshaojun/data; SSRN PDF attempt at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3643855 | Publisher abstract and author data page retrieved; SSRN PDF returned 403. | Abstract-only summary; sample, regression and estimation-timing details marked unverified. |
| Iwanaga & Sakemoto (2025), Conditional currency momentum portfolios | ScienceDirect publisher article/abstract; SSRN #4411616 attempted. | Publisher abstract and indexed preview retrieved; publisher/SSRN full-text routes unavailable in this review. | Abstract-level strategy and post-GFC claim; all unverified method details flagged. |
| Hutchinson et al. (2022), Are carry, momentum and value still there in currencies? | ScienceDirect publisher page; university repository record/PDF route attempted. | Publisher abstract/repository record found; PDF retrieval returned 403. | Abstract-level reassessment only. |
| Harris, Shen & Yilmaz (2022), Maximally predictable currency portfolios | ScienceDirect publisher page; University of Bristol publication page and PDF. | Publisher/repository abstract and indexed text found; PDF retrieval returned 403. | G10 counterpoint; details beyond abstract/indexed text not audited. |
| Fan et al. (2025), Understanding the Performance of Currency Basis-Momentum | Full Wiley Online Library article, https://onlinelibrary.wiley.com/doi/full/10.1111/eufm.12555 | Full HTML text retrieved; data/sample and Tables 1-2/post-2011 split inspected. | Full-text adjacent basis-momentum and ordinary momentum benchmark evidence. |
| Zeng (2025), Currency Carry, Momentum, and Global Interest Rate Volatility | Cambridge University Press article page. | Publisher abstract retrieved; full text not retrieved. | Abstract-level factor-risk context only. |
| Liu (2026), How to maximize momentum returns in foreign exchange markets? | ScienceDirect publisher page and SSRN record/PDF URL. | Publisher abstract/indexed text retrieved; full PDF returned 403. | Abstract-level 42-country, six-month and reversal candidate; dates/costs unverified. |
| Iwanaga & Sakemoto (2024), Cross-momentum strategies in the equity futures and currency markets | ScienceDirect publisher page; author-hosted paper route. | Publisher abstract/page and working-paper search result retrieved; full methodological cost/regime audit not completed. | Adjacent cross-asset candidate only. |
| Sakemoto & Suda (2026), Cross-sectional currency momentum and order flow | SSRN record, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6618279; author page. | Author abstract/metadata retrieved; no full-text audit. | Unreviewed working-paper candidate only. |
| Della Corte & Riddiough, Currency Factors companion data | Author site, https://sites.google.com/view/currencyfactors/home. | First-party page describing factors and data coverage retrieved; data not downloaded. | Availability lead only; no data values or results used. |

## Search boundaries and interpretation rules

- The exact 2020-2026 query set above is a targeted screen, not an exhaustive search of every finance journal, working-paper repository, or non-English database.
- Full-text gaps are explicit. Abstracts and search snippets were not used to invent sample dates, train/evaluation separation, cost details, or point-in-time estimation methods.
- One 2026 paper and several modern candidates remain abstract-only or indexed-snippet-only; their reported results are leads, not independently audited estimates.
- Historical evidence is kept separate by construct: cross-sectional basket WML, own-series TSMOM, conditional WML, basis momentum, optimized multivariate portfolios, and spot-only single-pair association.
- The search did not download FX data, calculate any current rank, form a backtest, estimate a strategy return, select a parameter, or inspect a holdout outcome.
- The proposal was read as a fixed but not frozen design on a branch ahead of main. This literature review did not modify its specification or open its outcome gate.
