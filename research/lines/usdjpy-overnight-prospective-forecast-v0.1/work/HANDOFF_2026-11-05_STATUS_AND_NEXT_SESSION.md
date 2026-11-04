# USDJPY Overnight Prospective Forecast v0.1 — Next-Session Handoff (2026-11-05 JST)

**Purpose:** hand over the current state without implying validation, rewriting past forecast artifacts, or adding outcomes to the formal cohort.

**Snapshot/as-of:** 2026-11-05 around 08:22 JST. **Authority:** GitHub fresh read at the start of the preparing session (details below). This handoff is a snapshot, **not** proof of the repository's state when a new session starts. The next session MUST fresh-read GitHub.

## 1. Canonical repo and checked refs

- Repository: `Josh-Temple/systematic-trading-research`.
- Research line: `research/lines/usdjpy-overnight-prospective-forecast-v0.1/`.
- Working branch: `research/usdjpy-overnight-prospective-forecast-v0.1`.
- PR: https://github.com/Josh-Temple/systematic-trading-research/pull/57 — **OPEN / DRAFT** when checked.
- **Pre-handoff branch head (before the documentation-only commit):** `e0d1b13234ba5e6eb407bbd537dd35d0bf0b4336`, authored/committed at 2026-10-27T12:49:36Z (21:49:36 JST). The handoff commit itself necessarily changes this head. Always check actual head on resumption.
- **Main at snapshot:** `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3` (observed; not a future guarantee).
- Key source qualification result: `work/source-qualification/RESULT.md`, blob `9c1ab2cac0fd6394783a8a7cb2ef2f055aa523b4`.
- Current projection: `CURRENT.md`, blob `db9cbf831191c4b58a611cd6850bf293296901ba`.

## 2. What is actually complete / incomplete

- Scientific status: **UNTESTED**. Overnight `SPEC-USDJPY-FORECAST-001-v01` and weekly `SPEC-USDJPY-WEEKLY-001-v01` remain **PROPOSED_NOT_FROZEN**.
- **Source gate:** `BLOCKED_RETRIEVAL_ENVIRONMENT / LOCAL_JFOREX_ROUTE_PREPARED`; `NOT PASSED`; formal prospective outcome access is `CLOSED`.
- A limited JForex Java export approach and a Python CSV inspector are available. Synthetic-only suites passed **14/14** CSV and **10/10** .bi5 tests (**24/24** total). This is **not** real JForex platform/API compilation or a successful live historical tick retrieval.
- No real qualified USDJPY best Bid/Ask tick sample or 22:00/08:00 bounded endpoint qualification was demonstrated in this research line. Missing evidence includes local demo-session retrieval, source receipt, UTC/bid/ask semantics, raw-file hash, structure audit, export/retention rights, endpoint 60-second tolerance, mandated news/input snapshots, and explicit human scientific spec freeze.
- **Formal scored forecasts: 0**. No broker/paper trading authorization. All ad-hoc forecasts are exploratory and **NOT_IN_COHORT**. Do not infer tested trading edge.
- Live-state journal: 20 entries, last dated 2026-10-08 at this snapshot; observational only.

## 3. Forecast inventory and operations

As of the snapshot, the `forecasts/exploratory/` index contained **10 `_OVERNIGHT.json` forecasts**, **one** `NO_FORECAST.json` event, and an `evaluations/` subfolder.

Overnight forecast filenames:
- `20261005T215400+0900_OVERNIGHT.json`
- `20261007T214634+0900_OVERNIGHT.json`
- `20261008T214701+0900_OVERNIGHT.json`
- `20261012T215621+0900_OVERNIGHT.json`
- `20261013T214732+0900_OVERNIGHT.json`
- `20261020T214714+0900_OVERNIGHT.json`
- `20261021T215821+0900_OVERNIGHT.json`
- `20261022T215538+0900_OVERNIGHT.json`
- `20261026T215917+0900_OVERNIGHT.json`
- `20261027T214827+0900_OVERNIGHT.json`

Other: `20261006T220000+0900_NO_FORECAST.json` is a documented missed cutoff. No 22:00 forecasts were present for Oct 28, Oct 29, Nov 2, Nov 3, or Nov 4 at the snapshot. **Do not create these retroactively.** The absence is a recorded operational limitation, not proof of a particular market outcome.

Latest forecast (#10) `XPF-USDJPY-20261027-214827`:
- Target: 2026-10-27 22:00 JST → 2026-10-28 08:00 JST.
- `information_cutoff=2026-10-27T21:47:43+09:00`; `issued_at=21:48:27 JST`.
- `p_up=0.51`, point prediction `+2bps`, `NEAR_NEUTRAL_SLIGHT_USDJPY_UP`, LOW confidence.
- Pre-cutoff forecast commit: `e0d1b13234ba5e6eb407bbd537dd35d0bf0b4336` at **21:49:36 JST**, verified before 22:00.
- Forecast original blob: `81c2dab734f1ac3a166cd2a8a46cc32ff10bac52`.
- Formal observed outcome and formal score **not available**; prior chat had only indicative, mixed public timestamps.

Forecast #9 (Oct 26 evening):
- `p_up=0.51` and `+2bps`. GitHub commit **22:00:04 JST**, **4 seconds past cutoff** even though prior chat showed forecast values before 22:00. Preserve this distinction.
- Late-persistence audit: `forecasts/exploratory/evaluations/20261026T220004+0900_ISSUANCE_TIMING_AUDIT.json`.
- Status: `LATE_GITHUB_PERSISTENCE`, exploratory, excluded from formal cohort.

`evaluations/` contained **four** files: the Oct 5 and Oct 7 exploratory evaluations, an Oct 8 source provenance correction, and the Oct 26 timing audit. This means **two exploratory evaluation files, not four formally scored forecasts**. There was no post-endpoint evaluation for #10 as of snapshot.

## 4. Current public market context, NOT an outcome in this study

- OANDA's **2026-11-05 07:24 JST** report quotes USDJPY around **158.318**, after the Nov 4 session ranged **157.378–158.742** and ended **158.424** on OANDA's particular MT5 context.
- https://www.oanda.jp/lab-education/market_news/report_usdjpy_20261105/
- Separately, a Central Tanshi FX / Diamond quote updated at **06:53 JST** was **158.42**; its quote timing, source, and aggregation differ. https://diamond.jp/list/market/chart-detail
- Neither observation is a qualified 08:00 endpoint. **No Nov 4 22:00 forecast exists in the repo**, so do not score Nov 4→5 from these prices.
- Prices and news in this handoff are time-stamped historical context, never proof of today's or another session's live market.

## 5. Hard integrity rules for the next session

1. **Fresh read** repo, PR head, `CURRENT.md`, relevant source qualification, forecast index and evaluations BEFORE making current-state claims.
2. Distinguish **hypothesis / specification / data qualification / implementation / experiment / observed result / interpretation / decision**.
3. Never backfill a missed 22:00 forecast or adjust prediction values after cutoff. Preserve immutable original JSON; corrections and outcome reviews are separate append-only artifacts.
4. Do not turn noncanonical, differently timed public quotes into an exact endpoint return, Brier score, or measured predictive edge. The qualified reference is USDJPY best Bid/Ask midpoint-to-midpoint log return at the specified endpoints, with predeclared selection tolerance.
5. Stop at real-data source gate; do not substitute synthetic fixture success, a third-party approximate feed, or guessed Dukascopy prices for actual qualified source data.
6. No trading/broker action, strategy profitability claim, protocol tuning from observed market outcomes, or formal cohort scoring without the independent gates and human spec freeze.
7. For issuance, check local JST before the deadline. Mon–Thu 22:00→next 08:00 are the candidate overnight windows. If the deadline is missed, record a `NO_FORECAST` / operational miss if appropriate, rather than issuing a retroactive forecast. Aim to save and verify materially **before** the cutoff.

## 6. Priority work on resumption

**A. Source readiness (highest scientific priority):** In a locally controlled JForex demo environment, establish actual API compilation and bounded 2024-01-15 USDJPY tick retrieval; locally preserve raw source/receipt/hash and audit USDJPY symbol/time UTC/best bid/ask/duplicates/range/crossed sides; assess lawful retention and endpoint 60-second feasibility. Remain **outcome-blind** throughout. Do not upload unapproved raw market files into cloud sessions.

**B. Protocol readiness:** After a real source qualification PASS and complete input/news source snapshots, seek **explicit human approval and freeze** of the exact candidate design. Only subsequently begin prospective formal scoring.

**C. Operational continuity:** Decide whether to set separate scheduled issuance and morning review tasks, leaving enough lead time for the GitHub commit and read-back. A suggested operating window is Mon–Thu 21:40–21:45 JST, with morning checks after 08:00; this is a recommendation, **not** evidence that an automation exists or is running.

**D. Reporting:** Show the latest fixed prediction, issue time versus actual GitHub commit time, public indicative observations only when provenance and clock time are clear, assessment limitations, and outstanding blockers. Record all unsuccessful runs and missing data as research findings.

## 7. Minimum next-session initial query

> Read `Josh-Temple/systematic-trading-research` and PR #57 / branch `research/usdjpy-overnight-prospective-forecast-v0.1` fresh. Read `CURRENT.md`, `work/source-qualification/RESULT.md`, `forecasts/exploratory/` and `evaluations/`, plus this handoff. Confirm any new commits and source gate. Distinguish public indicative USDJPY quotes from qualified Dukascopy outcomes. Do not backfill missed forecasts, rewrite original predictions, or score the cohort. Report the actual state and the next defensible action.

**Preparation note:** This is documentation only. No specifications, forecasts, scores or source-qualification status were changed when producing this handoff.
