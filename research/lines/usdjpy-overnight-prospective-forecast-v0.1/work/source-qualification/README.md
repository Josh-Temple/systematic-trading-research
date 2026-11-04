# USDJPY Dukascopy reference feed — source-only qualification
Date: 2026-10-08 JST

**Current status: BLOCKED_RETRIEVAL_ENVIRONMENT / LOCAL_JFOREX_ROUTE_PREPARED**

Research line: `research/lines/usdjpy-overnight-prospective-forecast-v0.1/`.
Primary source packet: `work/packets/PACKET_SOURCE_DUKASCOPY_REFERENCE_GATE.md`.
PR: https://github.com/Josh-Temple/systematic-trading-research/pull/57

## 1. Verified provider documentation

- Official Japan JForex/widget historical exports (demo login): https://www.dukascopy.jp/marketwatch/historical/
- `IHistory.getTicks(Instrument.USDJPY, from, to)`: https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/history-ticks/
- `ITick.getTime/getBid/getAsk/getBidVolume/getAskVolume`: https://www.dukascopy.com/client/javadoc3/com/dukascopy/api/ITick.html
- Official JForex strategy compilation/running: https://www.dukascopy.com/wiki/en/development/get-started-api/use-in-jforex/create-strategy/
- Official S3 daily .bi5: https://www.dukascopy.com/wiki/en/development/data-export/ — `Requester Pays`, AWS authentication/billing required; **not accessed**.

## 2. Local PC procedure / ローカルPCでの操作

1. Access Dukascopy Japan's official JForex **demo** route; sign in locally. Never share passwords or account identifiers with ChatGPT/GitHub.
2. In the JForex strategy editor import `JForexUsdJpyBoundedSource.java` with the exact class `jforex.JForexUsdJpyBoundedSource`. Compile. Preserve a credential-free build log and JForex platform version. The strategy has only a compilation check against mock Java stubs here; **it has not run in a real JForex runtime**.
3. Choose a **new** local output filename and run once, observing the local console. The strategy retrieves `Instrument.USDJPY` with `IHistory.getTicks` for the **predeclared** interval **2024-01-15 12:59:00–13:01:00 UTC** (21:59–22:01 JST). It emits six-column CSV, stops immediately, and contains no trading orders. On invalid/empty source it records a BLOCKED message; on existing filename it refuses overwrite.
4. On the same PC run:

```bash
python -m unittest -v test_probe_jforex_csv.py
python probe_jforex_csv.py --file USDJPY_20240115_1259-1301_UTC.csv --receipt SAMPLE_RECEIPT_jforex_local.json
```

5. Preserve CSV locally. Record the SHA256 and the non-secret fields in `SOURCE_ACQUISITION_ATTESTATION_TEMPLATE.json`; preserve retrieval time, JForex version, instrument/session verification and applicable rights/retention conditions.
6. Do not upload raw ticks to the public repo until licensing/persistence rights are determined. The structural receipt alone can be reviewed without disclosing raw prices.

**IMPORTANT**: The Python CSV probe recognizes only the exact six-column layout emitted by the Java strategy. The generic GUI/widget's CSV columns, time basis and sidedness are **not** assumed compatible. Do not pass a generic export into the validator.

## 3. Limits and scientific boundary

The local two-minute sample is solely for schema/source-structure qualification; it does **not** establish a ten-hour overnight endpoint pair, whole-week endpoint availability, or historical continuity. Endpoints retain the candidate frozen 60-second tolerance. The exact source and platform session must be independently established. A clean receipt returns `STRUCTURE_PASS_SOURCE_GATE_STILL_BLOCKED`, **never** a source PASS.

Official S3 `Requester Pays` was not accessed. Older time-relative, hourly datafeed .bi5 is distinct from the official S3 daily .bi5 path. Do not conflate the formats.

No forecast outcome, direction, return, P/L, performance or Brier was calculated. Both scientific specifications remain `PROPOSED_NOT_FROZEN`; formal outcome access is CLOSED. Explicit human freeze and additional input/news gates are required before scored prediction.

## 4. Evidence and tests

- `RESULT.md`: work performed, distinctions, blockers.
- `SAMPLE_RECEIPT.json`: explicit missing-real-sample placeholder.
- `SOURCE_ACQUISITION_ATTESTATION_TEMPLATE.json`: metadata to complete locally, without secrets.
- `TEST_LOG.md`: synthetic tests and Java mock-stub compile result.
- `probe_jforex_csv.py` and `test_probe_jforex_csv.py`: offline fail-closed validation and synthetic tests.
- `JForexUsdJpyBoundedSource.java`: unexecuted-in-platform, API-verified collector source.

The earlier standalone local .bi5 ZIP kit is a separate offline fallback. Only the JForex route files above are committed under this directory; no S3 .bi5 real data was read.
