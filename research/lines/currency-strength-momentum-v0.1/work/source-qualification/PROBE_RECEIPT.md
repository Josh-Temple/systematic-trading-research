# ECB bounded probe receipt

Probe ID: CSM-C-PROBE-2009-11  
Retrieved: 2026-10-01T08:20:40.683106+00:00  
Fixed request interval: 2009-11-01 through 2009-11-30 only  
Transport: official ECB EXR SDMX REST API, CSV data representation  
Expected calendar SHA-256: 6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4  
Outcome: **PASS for bounded route/schema/calendar identity only**; no full-history claim.

## Probe results

| Series | HTTP | Rows | Expected dates | Status | Source agency | Unit metadata | Bytes | Raw response SHA-256 |
|---|---:|---:|---:|---|---|---|---:|---|
| D.AUD.EUR.SP00.A | 200 | 21 | 2009-11-02 through 2009-11-30 (21) | A | 4F0 | AUD x 10^0 | 5008 | 19c96d0161204fbaa64625c29585d62212f30fb904b2b0da1b5f29e11b9d934c |
| D.CAD.EUR.SP00.A | 200 | 21 | 2009-11-02 through 2009-11-30 (21) | A | 4F0 | CAD x 10^0 | 4925 | 5a377ea79598074f04b821a3a375215da3bdc76ba2ab2d8cad0709f03dc248bc |
| D.CHF.EUR.SP00.A | 200 | 21 | 2009-11-02 through 2009-11-30 (21) | A | 4F0 | CHF x 10^0 | 4756 | d675912a6a683a656c420265871a5363a225e32d1a0e0ccdc5b3436e414451c1 |
| D.GBP.EUR.SP00.A | 200 | 21 | 2009-11-02 through 2009-11-30 (21) | A | 4F0 | GBP x 10^0 | 4888 | eaba637b40ba3539c802f6b7bd351ca318817540846dc9082fedfce492c7772c |
| D.JPY.EUR.SP00.A | 200 | 21 | 2009-11-02 through 2009-11-30 (21) | A | 4F0 | JPY x 10^0 | 4794 | d9caa2ca5d50193431cae621bed005f51e482ba1a5c2d35b13ba46c4107c25bb |
| D.NZD.EUR.SP00.A | 200 | 21 | 2009-11-02 through 2009-11-30 (21) | A | 4F0 | NZD x 10^0 | 5049 | fe9f9d705a331a1623632473e974cd315dbe08ae9d24adee77afe46af7a497a0 |
| D.USD.EUR.SP00.A | 200 | 21 | 2009-11-02 through 2009-11-30 (21) | A | 4F0 | USD x 10^0 | 4673 | e5055a18b2f4c177c8eaf0ba950547734d2028d03c6c6baee064b4d4c155c0d8 |

Each series matched the expected 21 November 2009 TARGET operating dates and the locked 32-column CSV schema. The dimension checks returned the requested currency, EUR denominator, daily frequency, Spot type SP00, and suffix code A. The official organization codelist maps agency 4F0 to the European Central Bank. The date-list SHA-256 for each series was 1ac4300aee6f072732b97b5e4c05c9b19787a87514efe2b242231c26835e83cf.

## Value handling

The CSV schema contains an OBS_VALUE column, but the probe did not extract, compare, calculate with, or emit any OBS_VALUE content. Raw response bytes were saved byte-for-byte in local scratch under `csm-source-qualification/probe-snapshot/`; their byte counts and hashes are above. The CSV files are not committed to the public GitHub branch. The standard ECB CSV format is eligible for public reuse under the cited ECB/ESCB policy when kept unchanged and attributed; this qualification commits the hashes and metadata receipt only.

An unrelated search-result exposure incident is recorded in RESULT.md: source-discovery snippets showed individual current observations. No such values are reproduced in this receipt or used in analysis.

## Reproduction boundary

The script `probe_ecb_metadata.py` is restricted to the fixed November 2009 interval. It emits metadata, dates, status, dimensions, series metadata, byte counts, and hashes. It does not calculate rankings, returns, P/L, or performance. Running the script again performs the same bounded source probe and is not a full-history test.

