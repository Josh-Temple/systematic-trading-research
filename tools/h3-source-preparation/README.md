# H3 source inventory (outcome blind)

This directory contains acquisition and basic validation tools for the first-party
Dukascopy source named by `SPEC-HR-003-v01` and `DEC-HR-004`. It is not a new
research specification or an H3 Run. The programs never generate touches,
confirmation groups, returns, or bootstrap output.

Run only through a **fully completed UTC day**:

```sh
python tools/h3-source-preparation/fetch_m1.py --through YYYY-MM-DD --output /path/to/new/source-folder
python tools/h3-source-preparation/fetch_ticks.py --through YYYY-MM-DD --output /path/to/same/source-folder
```

The Tick inventory requests all 24 UTC hour buckets on each weekday. Empty
market-break responses are preserved. It does not select hours using touches.
Each exact HTTP response is saved once. The manifests record URL, time, byte
count, SHA-256, decode metadata, basic validation, and independent local
readback. Existing bytes are not replaced on a later run.

If an interrupted run left raw Tick responses before its daily manifests were
written, their original retrieval timestamps are unavailable. Run:

```sh
python tools/h3-source-preparation/verify_existing_ticks.py --source-root /path/to/source-folder
```

This re-fetches only responses with missing original retrieval timestamps,
compares exact bytes by size and SHA-256, and saves an immediate per-hour
verification receipt with the **new** retrieval time. It never fills in an
unknown original timestamp or replaces a stored response. A changed response
is a HOLD for separate source-identity review.

The M1 decoder is copied from the byte-identified legacy `run_v01.py` with
SHA-256 `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`.
That decoder is used only for source validation. This inventory does not run
the legacy event generator or correct its Gamma time dependency.

**The basic validation is narrower than the frozen source gate.** In
particular, the accepted official trading-minute convention still needs to
be applied; Tick source coverage and full H2-prefix continuation also need
separate checks. No row in these manifests is a frozen selected session.
`DATA-HR-003` remains `FINAL_HOLDOUT / UNUSED`. Do not promote the inventories
to source-gate PASS or access outcomes from them.

For the acquired 2026-07-10–2026-09-25 summer dates, the separate
`classify_m1_structure.py` applies an explicit reconstructed minute set:
Monday–Thursday 00:00–20:59 and 22:00–23:59 UTC, Friday 00:00–20:59 UTC.
The H1 frozen sample records expected counts of 1,380/1,260 and excludes a
1,229-row summer Monday for 151 missing expected minutes. It does not itself
enumerate the minute set, so this reconstruction's schedule provenance is
still open. Run it only on the verified raw M1 inventory:

```sh
python tools/h3-source-preparation/classify_m1_structure.py --source /path/to/source-folder --output /path/to/new/structural-manifest.json
```

The script verifies raw hashes before classifying dates and does not alter
the source inventory, freeze a sample or evaluate the Tick source gate.

Persist raw responses and the manifests together. Recompute each raw SHA-256
from the persisted copy, rather than accepting a manifest alone. The eventual
60-session sample must be fixed by the frozen structural gate in chronological
order before any outcome calculation.
