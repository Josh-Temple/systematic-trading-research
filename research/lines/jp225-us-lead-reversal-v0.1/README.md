# JP225 US-Lead Opening Reversal v0.1

A separate historical proxy research line motivated by published evidence that the prior U.S. equity-market return predicts the first 30 minutes of Nikkei 225 futures in the opposite direction.

This line is **not** a rescue of EMA5/EMA200 and is **not** XM execution evidence.

Current stage: pre-outcome 2015 discovery specification frozen. No 2015 price outcomes had been read when the specification was committed.

Target research question:

> If the previous completed U.S. regular session is positive, is shorting the next eligible JP225 09:00–09:30 JST window profitable on average, and vice versa when the U.S. session is negative?

Historical proxy sources:
- OANDA-derived midpoint `SPX500_USD` M1
- OANDA-derived midpoint `JP225_USD` M1
- public repository `FutureSharks/financial-data`

Exact XM JP225Cash remains a separate locked research question.
