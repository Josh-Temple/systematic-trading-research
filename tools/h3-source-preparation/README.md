# H3 source preparation (outcome blind)

This directory prepares the frozen `SPEC-HR-003-v01` / `DEC-HR-004`
confirmation-selection test without opening `DATA-HR-003` outcomes.

Until the first 60 structurally eligible sessions are frozen and every source /
independence gate passes, these tools must not compute or view:

- touch-to-+15-minute outcomes;
- CONFIRMED-vs-UNCONFIRMED performance;
- the primary contrast;
- bootstrap output.

`DATA-HR-003` remains `FINAL_HOLDOUT / UNUSED` until the gated one-shot run
actually begins.

## 1. Acquire only fully completed UTC dates

Use first-party Dukascopy routes only:

```sh
python tools/h3-source-preparation/fetch_m1.py \
  --through YYYY-MM-DD \
  --output /path/to/source-root

python tools/h3-source-preparation/fetch_ticks.py \
  --through YYYY-MM-DD \
  --output /path/to/source-root
```

The Tick inventory requests all 24 UTC hour buckets for every candidate weekday,
independent of any touch or confirmation. Empty market-break responses are
preserved. Existing raw bytes are never silently replaced.

If an interrupted Tick acquisition left original retrieval timestamps unknown,
run:

```sh
python tools/h3-source-preparation/verify_existing_ticks.py \
  --source-root /path/to/source-root
```

This does not invent the missing original timestamp. It re-fetches the same
first-party response, compares byte count and SHA-256, and writes a separate
verification receipt with the new retrieval time. A mismatch is a HOLD.

## 2. Apply the frozen structural M1 gate

`classify_m1_structure.py` applies the already documented summer UTC minute
set:

- Monday-Thursday: 00:00-20:59 and 22:00-23:59 UTC;
- Friday: 00:00-20:59 UTC.

These are the prior sealed Stage A summer hours and the H1 expected counts of
1,380 / 1,260 minutes. The code is currently outcome-blind scoped through
2026-10-02, covering exactly the five candidate weekdays after 2026-09-25 that
would be sufficient for maturity if all five pass:

```sh
python tools/h3-source-preparation/classify_m1_structure.py \
  --source /path/to/source-root \
  --output /path/to/structural-manifest.json
```

If 60 eligible sessions have not been reached by 2026-10-02, do not silently
extend the date bound. Perform a new outcome-blind review of the applicable
trading-hours convention first, then extend the structural scope without looking
at H3 outcomes.

## 3. Verify the frozen H2 generator prefix

The legacy generator identity is:

```text
run_v01.py
SHA-256 9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd
```

The frozen H2 generator input contains 135 M1 files: 75 context files plus 60
selected H2 sessions, ending 2026-07-09. Re-fetch / verify it with:

```sh
python tools/h3-source-preparation/verify_h2_prefix.py \
  --frozen-manifest /path/to/H2_M1_Generator_Input_Manifest_135files_v1.csv \
  --output /path/to/h2-prefix-root
```

H3 must retain this exact prefix and append post-2026-07-09 first-party BID M1
chronologically. Expanding Gamma is never reset at 2026-07-10.

## 4. Build the full outcome-blind source / maturity gate

`build_h3_source_gate.py` independently rechecks the raw source rather than
trusting inventory labels alone. It verifies:

- exact legacy generator SHA-256;
- all 135 H2-prefix raw identities;
- post-H2 M1 raw identities;
- structural-manifest binding to the exact M1 manifest;
- raw Tick hour identity and raw Tick decoding/quality;
- either an original Tick retrieval timestamp or an exact first-party re-fetch
  receipt for each hour;
- continuous H2 -> H3 M1 ordering with no Gamma-history reset;
- the frozen H3 runner identity;
- once maturity exists, a fresh independence attestation bound to the exact
  selected 60-session list.

Before maturity, omit the independence attestation:

```sh
python tools/h3-source-preparation/build_h3_source_gate.py \
  --m1-root /path/to/source-root \
  --h2-prefix-root /path/to/h2-prefix-root \
  --tick-root /path/to/source-root \
  --tick-verification-root /path/to/source-root \
  --structural-manifest /path/to/structural-manifest.json \
  --legacy-generator /path/to/run_v01.py \
  --h3-runner tools/h3-source-preparation/run_h3_once.py \
  --output /path/to/h3-source-gate.json
```

With fewer than 60 eligible sessions the required result is:

```text
status = WAITING_FOR_MATURITY
source_gate = NOT_EVALUATED_PENDING_MATURITY
frozen_selected_count = 0
freeze_packet = null
```

The chronological eligible prefix is recorded for audit, but it is not described
as a frozen H3 sample.

## 5. Maturity-time independence review

Only after the first 60 structurally eligible dates are known, conduct the
existing preregistered independence review without opening the H3 outcome. The
attestation must be machine-readable and include:

```json
{
  "scope": "H3_EXACT_OUTCOME_INDEPENDENCE_REVIEW",
  "status": "PASS_NO_PRIOR_EXACT_H3_OUTCOME_FOUND",
  "selected_dates_sha256": "<sha256 of exact 60 dates, newline-delimited>",
  "outcome_accessed": false,
  "reviewed_at_utc": "<UTC timestamp>"
}
```

If the exact H3 outcome has already been analyzed, or the review cannot pass,
do not produce a passing freeze packet. Stop under the preregistered
independence hold.

Re-run the full gate with the attestation. A passing gate binds the exact first
60 dates, M1/Tick source identities, H2-prefix chain, generator SHA, runner SHA,
independence-attestation SHA, bootstrap seed `20260913`, 10,000 replications,
and the bootstrap engine into a single freeze packet.

Any runner edit after that freeze invalidates the packet.

## 6. Validate H3 classification using consumed H2 M1 only

Before H3 outcome access, classifier identity can be tested against already
consumed H2 M1:

```sh
python tools/h3-source-preparation/validate_h3_classifier_h2.py \
  --h2-prefix-root /path/to/h2-prefix-root \
  --legacy-generator /path/to/run_v01.py \
  --output /path/to/h2-classifier-validation.json
```

This checks that the H3 classifier reproduces the exact legacy touch population
and the legacy clean confirmation output, while retaining mechanically qualifying
same-confirmation-bar events as `CONFIRMED` before the execution-ambiguity
filter, as required by `DEC-HR-004`.

It does not read H3 post-2026-07-09 data or compute a market outcome.

## 7. One-shot H3 execution

`run_h3_once.py` exists so no new design decision is needed after maturity. It
must **not** be run while H3 is waiting for maturity.

It refuses to start unless:

- a full 60-session freeze packet exists;
- the current source gate still passes;
- the packet still matches the current raw source;
- the runner's own SHA-256 matches the frozen runner SHA;
- the exact independence attestation still matches;
- the frozen seed / replication count / bootstrap engine match.

After those checks, it writes a run-start receipt before accessing the holdout,
rechecks the exact legacy touch/classification behavior, then performs the
preregistered outcome and bootstrap exactly once in a new output directory.

Do not use the runner to test alternative thresholds, dates, horizons, source
providers, quote rules, bootstrap choices, or subsets.

## 8. CI

The dedicated workflow:

```text
.github/workflows/h3-source-preparation.yml
```

runs the source-preparation boundary tests. The tests assert, among other things,
that 55 eligible sessions cannot freeze a sample, 60 sessions are required, raw
Tick defects fail closed, exact re-fetch receipts are handled without inventing
original timestamps, independence is bound to the exact sample, and the one-shot
runner cannot start without a freeze packet.

These are engineering/source-boundary tests, not H3 scientific evidence.
