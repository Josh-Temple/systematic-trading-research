# Source Qualification — USD/JPY Daily Breakout

確認日: 2026-10-03 JST
Status: SOURCE_QUALIFICATION_ONLY / PARTIAL
Market outcome access: NO

## Conclusion

The research can proceed with a two-layer data architecture, but broker-specific historical execution is not yet qualified.

1. **Reference research layer — candidate PASS pending bounded sample retrieval:** use Dukascopy JForex historical USD/JPY ticks containing best Bid/Ask. Aggregate New York 17:00 daily Bid OHLC deterministically from ticks; do not rely on vendor daily-bar boundary semantics for the signal.
2. **Broker translation layer — PARTIAL:** use XM Micro and Matsui official current contract/size/trading-condition metadata plus broker-native prospective observations. Do not claim that Dukascopy historical fills equal XM or Matsui fills.

This separation is required by source identity. It is not a choice made from strategy returns.

## Dukascopy reference-feed evidence

- Current JForex API documentation lists `Instrument.USDJPY`.
- `IHistory` provides historical bars and historical ticks.
- Current history-tick documentation exposes tick Ask and Bid values; Dukascopy support documentation describes downloaded tick rows as timestamp, Ask, Bid, Ask volume, Bid volume.
- JForex documentation says historical data accessed from DEMO returns LIVE historical data, while DEMO realtime ticks differ from LIVE realtime ticks.

Official sources:
- https://www.dukascopy.com/client/javadoc3/com/dukascopy/api/Instrument.html
- https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/overview-historical-data/
- https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/history-ticks/
- https://www.dukascopy.com/client/javadoc3/com/dukascopy/api/IHistory.html

### Boundary decision

The strategy requires a New York 17:00 daily boundary and intraday executable path for entry/stop/Friday exit. Therefore the candidate source input is raw historical ticks, not a provider DAILY candle.

Reason:
- raw Bid/Ask ticks can support both deterministic NY17 daily aggregation and intraday path replay;
- current API documentation does not establish that provider DAILY bars use the strategy's required New York 17:00 boundary;
- historical Dukascopy support records contain prior reports of bar/download timezone or DST inconsistencies, so accepting a ready-made daily bar without boundary verification is unnecessarily risky.

This is a data-semantics decision, not evidence that the strategy works.

## Matsui FX execution feasibility

Official rule/Q&A pages currently establish:

- USD/JPY minimum unit: 1 currency unit.
- Order/execution hours: Monday 07:00 onward; Tuesday-Friday sessions cover 20:00 JST and Friday 23:00 JST under both U.S. daylight-saving and standard-time schedules, except separately announced interruptions.
- For USD/JPY, the current reduced-spread table covers 09:00 through 03:00 for qualifying small market orders, but the spread is described as principle-fixed with exceptions. A current spread table is not a historical execution record.
- Matsui publishes a monthly historical swap-point calendar; swap is generated when a position is held through New York close into the next trading day.

Official sources:
- https://www.matsui.co.jp/fx/rule/index.html
- https://support.matsui.co.jp/faq/show/1904?site_domain=faq
- https://www.matsui.co.jp/fx/market/past-swap/

Qualification:
- WEEKEND_FLAT schedule feasibility: PASS for the published normal trading-hours framework.
- Exact historical Bid/Ask execution replay from public Matsui data: NOT_ESTABLISHED.
- Historical swap data: available as a broker-specific cost input, subject to exact date/unit parsing before use.

## XM Micro MT5 execution feasibility

Official XM pages currently establish:

- Micro: 1 micro lot = 1,000 currency units.
- Micro minimum size in the FAQ: 0.1 lot on MT5; step 0.01 lot.
- Micro has no trading commission and is not swap-free by default.
- XM's platform comparison states MT5 has tick history and no server search-period limit for past bar data.
- Public pages reviewed here do not establish an exact historical Micro-account Bid/Ask export, historical spread series, or a broker-native historical fill series suitable for this strategy.

Official sources:
- https://www.xmtrading.com/jp/account-types/micro
- https://www.xmtrading.com/jp/platforms
- https://www.xmtrading.com/jp/trading-fees

Qualification:
- Quantity feasibility metadata: PASS subject to live symbol-specification readback before any live use.
- Broker-native historical execution replay: UNVERIFIED.
- A PC MT5 export or other broker-native history may be inspected later if available, but its content and timestamp/side semantics must be qualified before use.

## What can be frozen now

The research data architecture can be fixed as:

- Signal/reference identity: Dukascopy USD/JPY historical best-Bid/Ask ticks, with daily Bid OHLC derived by project code using America/New_York 17:00 boundaries.
- Reference execution replay: the same Dukascopy Bid/Ask tick stream, explicitly labeled **reference-feed execution**, not XM/Matsui execution.
- Broker translation: separate Matsui and XM quantity/cost/availability feasibility. Do not substitute current published spread minima for historical actual spreads and call them observed costs.

## Remaining source gate

Before calculating strategy outcomes:

1. Retrieve a small bounded USD/JPY Dukascopy tick sample without computing signals or returns.
2. Record exact retrieval route, timestamp semantics, first/last tick, Bid/Ask fields, missingness, byte hash, and permitted persistence boundary.
3. Prove the NY17 daily aggregation and DST transition behavior on synthetic plus source timestamps.
4. Freeze the historical evaluation period and warm-up only after source coverage is known, without inspecting price outcomes.
5. Freeze how broker-specific costs are reported: observed historical broker cost where available versus clearly labeled stress/current-condition scenarios.

Until the bounded raw sample passes, source status remains PARTIAL.