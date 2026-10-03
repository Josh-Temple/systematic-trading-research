# Source clarification — OANDA proxy candles are midpoint candles

During the 2019 source read, the external repository's generator `pyfinancialdata/oanda_prices.py` was inspected.

It calls the OANDA candles endpoint and then explicitly expands:

`candle['mid']`

into OHLC columns.

Therefore the OANDA `JP225_USD` files used for the 2020 proxy exploration and 2019 replication must be described as **midpoint OHLCV proxy data**, not BID bars and not executable BID/ASK history.

This note clarifies source semantics without changing any prior result.

Consequences:

- gross directional movement can be studied;
- actual broker spread cannot be reconstructed;
- XM short-term profitability cannot be inferred;
- the gross mean is at most a break-even budget for all unmeasured round-trip costs.
