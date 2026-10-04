# JP225 / Nikkei 225 official-source route review — 2026-10-04

Status: **SOURCE_RESEARCH_ONLY / COMPLETE**

Scientific effect: **NONE**

XM Packet A effect: **NONE**

Market outcomes accessed for this work: **NO**

## Question

While exact XM MT5 `JP225Cash` Stage 1 remains unavailable, is there a materially better reproducible data source than the consumed OANDA midpoint proxy that is worth preserving as a future JP225/Nikkei 225 research route?

This review does **not** authorize substituting another instrument/feed for the frozen exact-XM research line.

## Source-of-truth boundary

The exact-XM line remains unchanged:

- target instrument: XM MT5 `JP225Cash`;
- exact source qualification remains `PARTIAL_WITH_GAPS`;
- Packet C 2025 Discovery remains locked;
- 2026 XM holdout remains untouched and locked.

A futures source may support a **separate preregistered futures experiment**. It cannot establish XM CFD BID/ASK execution economics.

## Official JPX findings

### 1. J-Quants DataCube / JPX historical derivatives data exists at useful intraday granularity

JPX states that historical OSE/TOCOM futures and options data are available through J-Quants DataCube as:

- OHLC;
- one-minute OHLC;
- tick data.

Files are delivered in CSV format.

Official sources:

- https://www.jpx.co.jp/markets/paid-info-derivatives/historical/01.html
- https://www.jpx.co.jp/markets/paid-info-derivatives/historical/index.html
- https://www.jpx.co.jp/markets/other-data-services/j-quants-datacube/index.html

The current price-list metadata also shows long historical availability for Nikkei 225 derivatives, including Nikkei 225 Futures, Nikkei 225 mini and Nikkei 225 micro. Exact product/date availability varies by dataset and must be checked before purchase.

Price-list source:

- https://db-ec.jpx.co.jp/client_info/JPX_DLSITE/html/datacube_price.pdf

### 2. DataCube tick data is transaction-price history, not an XM-style BID/ASK quote feed

A concrete JPX product page for Nikkei 225 Futures tick data states that it contains the movement of **executed prices** for each issue.

Example:

- https://db-ec.jpx.co.jp/item/C430508202502.html

Therefore DataCube tick data must not be relabeled as:

- BID/ASK quotes;
- XM execution ticks;
- XM spread evidence.

It is true-OSE transaction evidence.

### 3. One-minute futures data is trade-based OHLC

JPX DataCube product pages describe the one-minute derivatives files as one-minute OHLC and volume for times with trading volume.

Therefore:

- minutes without trades may be absent;
- the series is not automatically equivalent to an XM chart-equivalent BID M1 series;
- gaps must not be forward-filled merely to emulate XM bars.

This makes the data useful for a separately specified futures study, but not a drop-in input to `SPEC-JP225-EMA-001-v01`.

### 4. Retail J-Quants API does not solve the derivatives intraday requirement

JPX's 2026-01-19 J-Quants API announcement explicitly says its newly provided minute-bar/tick data is for equities and **does not include derivatives such as futures**.

Source:

- https://www.jpx.co.jp/english/corporate/news/news-releases/6020/20260119.html

### 5. J-Quants Pro's new derivatives dataset does not replace DataCube intraday history

The 2026-09-28 J-Quants Pro expansion adds futures/options OHLC by session/daily structure, while the new one-minute dataset described in that release is for cash equities.

Source:

- https://www.jpx.co.jp/corporate/news/news-releases/6020/20260928-01.html

Thus the verified official route for historical intraday OSE derivatives remains the historical-data/DataCube route, not the new Pro futures OHLC dataset.

### 6. A separate historical-data application route exists, but individual eligibility must not be assumed

JPX states that it may provide historical tick data for examining trading methodology to parties considering participation in its market, subject to requirements.

Source:

- https://www.jpx.co.jp/markets/paid-info-derivatives/historical/02.html

This is not an automatically available free dataset. Eligibility, permitted products/dates, retention and processing rights must be confirmed before relying on it.

## Prior GitHub research / implementation evidence

A search of public GitHub found no general-purpose repository dedicated to J-Quants DataCube ingestion.

One relevant prior research repository, `fishke22/jerry-backtest-lab`, independently records a similar source hierarchy:

- official OSE/DataCube tick and one-minute data as materially stronger than public proxy data;
- free/trial eligibility and storage rights kept unresolved until confirmed;
- explicit separation between source identity and substitute/proxy evidence;
- later commits preserve failures rather than repeatedly changing the source/mechanism.

Relevant examples observed:

- `research_notes/jnu_true_ose_free_access_paths_20260831.md`
- `config/jnu_data_source_registry.json`
- commit history around OSE source readiness and later negative OSE research.

This repository is **prior art only**, not authority for JPX terms or this project's scientific claims. Official JPX material controls the source facts above.

## Interpretation

### What improves relative to the OANDA proxy

A JPX/OSE DataCube Nikkei 225 futures dataset would materially improve:

- venue identity;
- product identity;
- timestamp/session provenance;
- historical reproducibility;
- separation from a third-party CFD midpoint generator.

This is a meaningful improvement for a **Nikkei 225 futures research line**.

### What it does not solve

It does not solve the frozen exact-XM problem because:

- futures and XM `JP225Cash` are different instruments;
- DataCube tick data is executed trades, not XM BID/ASK quotes;
- DataCube one-minute OHLC is trade-based and may omit no-trade minutes;
- futures require explicit contract-month / roll semantics;
- broker spread, markup and execution remain unobserved.

Therefore a positive futures result could not be promoted directly to XM profitability evidence.

## Decision

Classification:

**JPX_DATACUBE_OSE = QUALIFIED_BETTER_PROXY_CANDIDATE / NOT_XM_REPLACEMENT**

Do not feed JPX futures data into the frozen exact-XM v0.1 pipeline.

Do not use it to unlock Packet C or the 2026 XM holdout.

Do not buy data merely to continue the failed EMA5/EMA200 rescue family.

## Bounded next use

If a genuinely new mechanism with independent prior rationale is later selected, JPX DataCube should be preferred over the prior OANDA midpoint source for an OSE/Nikkei 225 futures experiment, subject to a new preregistration that fixes before outcome access:

- exact futures product (large / mini / micro);
- contract-month and roll rule;
- time/session semantics;
- one-minute versus transaction-tick role;
- missing/no-trade-minute handling;
- predictor/target/horizon;
- baseline/comparator;
- inference and kill rule;
- data license / storage boundary.

Before any purchase, first inspect the official sample file/schema or confirm the required fields through JPX. No purchase or credential action is authorized by this note.

## Current recommended priority

1. Exact XM Stage 1 remains the highest-value route when Windows access becomes available.
2. Until then, do not run further rescue variants on consumed OANDA EMA samples.
3. JPX DataCube is retained as the preferred official futures source for a future **independent** Nikkei 225 mechanism, not as an XM substitute.
