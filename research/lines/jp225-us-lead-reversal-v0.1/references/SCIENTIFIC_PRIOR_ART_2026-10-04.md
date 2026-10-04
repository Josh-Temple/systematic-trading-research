# Scientific prior art — JP225 US-lead opening reversal

Created: 2026-10-04

## Primary motivating study

Yasuhiro Iwanaga (2026), "How the prior day's S&P 500 returns influence the intraday returns of Nikkei 225 futures", Finance Research Open 2(2), 100108.

DOI:
https://doi.org/10.1016/j.finr.2026.100108

Reported design:
- Nikkei 225 futures one-minute data;
- S&P 500 index;
- January 2001 through December 2024;
- 5,716 Japanese trading days;
- prior U.S. return significantly predicts the first 30-minute Japanese return negatively and the last 30-minute return positively;
- transaction costs reduce profitability but the reported opening-reversal timing strategy remains positive in the study.

The paper uses futures and licensed LSEG Tick History. This repository does not reproduce that exact source.

## Historical JPX session evidence

JPX Derivatives Market Highlights for 2015 records Nikkei 225 futures auction day-session trading hours as 09:00–15:15 JST.

Source:
https://www.jpx.co.jp/english/derivatives/market-report/market-highlights/tvdivq0000004khi-att/2015_0101_0630_E.pdf

Therefore the proxy discovery fixes 09:00–09:30 JST for calendar 2015.

## Boundary

This prior art motivates the direction and window before OANDA 2015 outcomes are accessed.

It does not justify:
- threshold selection on S&P return magnitude;
- volatility filters;
- sign-agreement filters with overnight JP225;
- close-window testing in this packet;
- EMA filters;
- parameter optimization.
