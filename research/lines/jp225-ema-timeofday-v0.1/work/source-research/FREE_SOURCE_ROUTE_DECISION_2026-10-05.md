# JP225 Free-Source Route Decision — 2026-10-05

Status: **DECISION / NO_PAID_MARKET_DATA**

Scientific result: **NONE**

Market outcomes accessed for this decision: **NO NEW TARGET OUTCOMES**

## 1. Decision context

The research owner has decided that the project should, for now, avoid paid market-data services.

This decision changes source priority only. It does not change any frozen hypothesis, EMA parameter, time window, horizon, advancement rule, or holdout boundary.

The JPX/J-Quants DataCube route remains preserved as prior source research, but paid acquisition is deferred.

## 2. Canonical free-source hierarchy

### Route A — exact XM MT5 JP225Cash

Classification:

**PRIMARY / EXACT-BROKER SOURCE / NO SEPARATE PAID DATA SERVICE**

Reason:

- the target instrument of RL-JP225-EMA-001 is exact XM MT5 JP225Cash;
- the existing Stage 1 collector is already restricted to exact symbol JP225Cash;
- existing code requests warm-up + 2025 M1 and fixed 2025 tick probes only;
- 2026 is mechanically excluded;
- Stage 1 calculates no EMA, return, regression, strategy P/L or holdout result;
- the existing validator emits structural/source diagnostics rather than market-price values.

The source still requires access to the intended XM MT5 terminal and whatever account/server access is necessary for that terminal. This decision means there is no separate paid historical-data purchase.

Exact XM remains the only route that can eventually unlock the existing XM Packet C gate.

### Route B — Dukascopy JPN.IDX/JPY

Classification:

**REJECTED_AS_JP225_PROXY / DIFFERENT_INSTRUMENT**

Official Dukascopy material currently describes JPN.IDX/JPY as the "Japan 200+ Index", comprising more than 200 leading Japanese firms.

It is not identified by Dukascopy as Nikkei 225 and must not be relabeled as:

- Nikkei 225;
- OSE Nikkei 225 mini;
- XM JP225Cash;
- an instrument-equivalent JP225 proxy.

Dukascopy historical data is still technically attractive:

- historical data export is available without a separate data purchase;
- JForex historical history supports bars and ticks;
- tick history exposes BID and ASK;
- Dukascopy documents that historical data requested from DEMO uses LIVE historical data.

Those properties may justify a future, separately preregistered **Japan broad-index** research line. They do not justify using JPN.IDX/JPY to rescue or validate a JP225 hypothesis.

No Dukascopy market data is authorized or needed for the current JP225 lines.

Official references reviewed:

- https://www.dukascopy.com/swiss/english/marketwatch/historical/
- https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/overview-historical-data/
- https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/history-ticks/
- https://www.dukascopy.com/swiss/chinese/cfd/range-of-markets/cfd-indices/
- https://www.dukascopy.com/media/pdf/japan/manual/historical-data.pdf

### Route C — JPX/J-Quants DataCube

Classification:

**DEFERRED_NO_PAID_DATA / PRESERVE_ONLY**

The DataCube source remains a higher-fidelity OSE futures source than prior public CFD midpoint proxies, but acquisition currently conflicts with the owner's no-paid-data policy.

Do not:

- purchase 2025 DataCube files;
- send the prepared license inquiry merely to advance this line;
- use the quarantined 2025 intraday-momentum line as a reason to purchase data.

Preserve PR #59, source research, validator, incident record and specifications as reusable infrastructure.

### Route D — consumed OANDA midpoint proxy

Classification:

**NO_FURTHER_USE_FOR_RESCUE**

Existing consumed negative/weak proxy results remain valid historical research records.

Do not mine additional filters, time windows, persistence lengths, or years merely because paid data is unavailable.

## 3. Operational priority

1. Exact XM Stage 1 when a Windows XM MT5 session is available.
2. Complete source qualification from the already frozen Stage 1 protocol.
3. Only after exact source PASS, freeze the signal-only 2025 event manifest and proceed to minimal Stage 2 tick acquisition.
4. Keep 2026 locked.
5. Do not start a substitute Japan-index outcome study merely to keep activity going.

## 4. Outcome-blindness hardening after the DataCube incident

The DataCube intraday-momentum branch recorded an accidental public search-result exposure to a 2025 quotation snippet.

That incident does not provide evidence about the XM EMA hypothesis, but it reinforces a stricter operating rule:

- source research should prefer documentation pages, APIs and metadata pages over searches likely to surface price snippets;
- do not manually inspect Stage 1 market-value files;
- run collector and validator locally;
- communicate validation receipts, hashes and metadata rather than copying price rows into chat;
- any future accidental target-outcome exposure must be recorded append-only.

The existing XM protocol remains scientifically separate from PR #59.

## 5. Decision

Current project source policy for JP225:

**FREE_SOURCE_ROUTE = XM_EXACT_FIRST**

**DUKASCOPY_JPN_IDX = NOT_A_JP225_PROXY**

**DATACUBE = DEFERRED_NO_PAID_DATA**

No scientific result changes because of this decision.
