# Dukascopy JPN.IDX/JPY Source Qualification — 2026-10-05

Status: **COMPLETE / NO-GO_FOR_JP225**

Market outcomes accessed: **NO**

## Question

Can Dukascopy JPN.IDX/JPY serve as a free replacement or sufficiently close proxy for the project's JP225/Nikkei 225 research lines?

## Source facts

Official Dukascopy documentation provides a free historical-data route through its historical export/JForex environment and supports historical bars and ticks.

The JForex historical tick API exposes best BID and ASK.

Dukascopy also states that DEMO real-time ticks differ from LIVE, while historical data returned in DEMO is sourced from LIVE history.

However, Dukascopy's official CFD index list identifies JPN.IDX/JPY as:

**Japan 200+ Index — over 200 leading Japanese firms.**

It is not documented there as Nikkei 225.

## Qualification decision

Classification:

**REJECTED_AS_JP225_PROXY / ELIGIBLE_ONLY_FOR_SEPARATE_BROAD-JAPAN-INDEX_RESEARCH**

Reasons:

1. instrument constituency/identity is not the target Nikkei 225;
2. it is not XM JP225Cash;
3. it is not an OSE Nikkei 225 futures contract;
4. strong historical-data mechanics cannot repair instrument mismatch;
5. using its outcomes to support a JP225 claim would conflate source quality with instrument identity.

## What this rejection does not mean

It does not mean Dukascopy data is low quality.

For a separately frozen question about the Dukascopy Japan 200+ CFD itself, it may be attractive because it provides a reproducible no-separate-data-fee historical source with BID/ASK tick access.

That is outside the present JP225 research scope.

## Stop rule

Do not download or analyze JPN.IDX/JPY outcomes for the purpose of rescuing:

- JP225 EMA5/EMA200;
- JP225 intraday momentum;
- U.S.-lead JP225 reversal;
- any consumed OANDA result.

A future broad-Japan-index line requires a new hypothesis and preregistration before outcome access.
