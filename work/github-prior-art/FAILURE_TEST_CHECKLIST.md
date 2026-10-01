# Failure / regression-test checklist for later CSM implementation and audit

Status: prepared from code, tests, issue records, and commit history. No market outcome was accessed. Recommendations below are not claims that any external project implements them.

## Shared tests

| Test | Synthetic setup | Required assertion | Failure meaning |
|---|---|---|---|
| Prefix invariance | Compute a signal on a full synthetic series, then on each prefix ending at t; perturb all values after t | Every signal through t is unchanged; future suffix never affects earlier values | Temporal leakage or a signal function that reads future rows |
| Availability time | Give each observation event/open time and known/available time; include 15m/1h boundary case | Signal input available_at is no later than decision time; candle close is not available at candle open | Unclosed or delayed source data entered too early |
| Month endpoint | Fixed monthly calendar plus one missing operating-day quote | Endpoint comes from the predeclared calendar; a missing required currency makes the slot unavailable; no per-currency previous-day fallback | Asynchronous cross-rate or endpoint selected from observed data |
| Currency quote inversion | Generate positive direct and inverse quotes for the same currencies | Reciprocal conversion reverses individual quote return and preserves algebraically equivalent cross-pair relative log return | Sign or units are inconsistent |
| Max/min identity | Unique synthetic currency scores, all 56 directed pairs | Maximum directed pair difference equals max score minus min score; selected pair is unique max/min | Pair selector, ranking, or pair universe differs from contract |
| Missing / invalid values | Duplicate date/key, zero, negative, NaN, infinity, holiday and unexpected missing date | Invalid identity/nonfinite input fails closed; expected holiday differs from missing operating-day row; no horizon compression | Silent repair or altered calendar |
| Cost path | One trade with separate transaction fee and held-position cost; add nested/dynamic/paper portfolio copy | Each configured cost applies on each path; return/fee decomposition matches independent toy amount; holding-cost date index matches price index | Cost silently omitted, double counted, or shifted |
| Cost finite / state safety | NaN, ±infinity and overflow in volume, volatility, commission, long/short cost | Reject before position, fee, or portfolio state mutates | Invalid cost leaves partial state |
| Outcomes and roles | Synthetic run manifest with fixed input role | No source qualification or code test is labeled as strategy outcome; consumed data is never reset to unused | Operational validation is mistaken for scientific evidence |

## Repository-specific regression targets

### Nate Emma FX framework

- Keep 63-day price momentum, carry-level signal, rate-differential-change carry momentum, and time-series trend as different predictors.
- Assert the one-row weight lag: a new target weight does not earn the same row's return; it affects the following return row.
- Assert turnover fee is applied on rebalance and held financing is applied for the correct long/short position and dates.
- Test missing/forward-filled price behavior, quote inversion, and valid currency coverage explicitly. Existing FRED USD-per-foreign quotes differ from proposed ECB currency-per-EUR data.
- Test raw signal separately from top-N/bottom-N basket. Top-3/bottom-3 results do not establish the single strongest/weakest pair.
- Keep the bfill regression on the HAR warmup path separate from momentum tests. Broad causality does not prove the exact old failing input has its own assertion.

### pmorissette/bt

- Test the exact date window and lag at the signal point, including a final row whose close is unavailable until after the decision boundary.
- Include no-fee, flat fee, nonlinear impact, holding-long, holding-short, dynamic subtree, and paper copy paths.
- Require cost/volume/volatility index alignment. Inject nonfinite and overflow values and assert rejection before transaction state changes.
- Keep trade cost and per-period holding/funding cost in separate ledgers.
- Do not use the liquid-US-equity half-spread, volume, or impact coefficients as FX calibration.

### Freqtrade

- Test raw merge_asof as a negative control with an unclosed HTF candle; verify it exposes a future close too early.
- Test current merge helper at 15m/1h and calendar boundaries: prior closed informative bar is used and availability timestamps are explicit.
- Add event/known-at time checks because equal full/cut indicator values can both contain the same unavailable value.
- Trigger every distinct entry/exit signal type; a pass with untriggered signal paths remains unverified.
- Test cross-sectional/ranked strategies as a whole. A single-pair diagnostic can remove the cross-section being tested.
- Record that default lookahead analysis forces market orders. Separately test custom price callbacks, fees, slippage, and dry-run/live parity.

### QuantConnect/Lean screen

- Treat QuoteBar/bid-ask, broker FeeModel, fill model, slippage, account-currency conversion, margin, and financing as separate inputs.
- Verify selected brokerage model overrides security defaults in the run configuration.
- Pin fee-model source/version and current venue schedule. The examined FXCM model contains an old dated schedule.
- Do not infer strategy performance from order validation, regression algorithms, or exchange-hours tests.

## Choices not to copy

- Do not use Nate Emma's daily lookback, 63-day default, three-long/three-short basket, FRED panels, parameter sweep, or market results to fill an unspecified CSM contract.
- Do not use rate-differential-change carry-momentum results as price-momentum evidence.
- Do not use US-equity commission, volume, or impact assumptions from bt for FX.
- Do not treat Freqtrade lookahead-analysis PASS as proof of zero temporal leakage, live parity, or realistic execution.
- Do not treat the prior review's Freqtrade component reproduction as a new reproduction in this task.
- Do not use Lean's old FXCM fee schedule as a current broker quote.
- Do not access strategy outcomes before the human contract, source lock, implementation, independent audit, and outcome gate are complete.

## Current verification status

- These are proposed tests for later implementation/audit, not CSM strategy results.
- Four toy checks in toy_checks/run_toy_checks.py passed with synthetic inputs.
- External repository test suites and any full backtest were not run.
