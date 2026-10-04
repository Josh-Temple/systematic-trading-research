# Stage 1 validator PASS contract

`python validate_stage1.py <raw-folder> --out <receipt.json>`

## FAIL

Missing/empty input; schema/manifest/hash/byte mismatch; metadata outside the privacy allowlist; wrong exact symbol; missing server; invalid instrument numerics; unexpected M1 minute alignment/order/duplicates/OHLC; nonfinite/unparseable values; crossed/zero quotes; tick order errors; inconsistent raw seconds/milliseconds; unexpected probes/request bounds; or **any raw 2026 timestamp**.

Boundary failures return only FAIL + boundary code, without market values, row counts, first/last times, event counts, or charts. Rows are not silently dropped.

## PARTIAL_WITH_GAPS

Structurally valid bytes but unresolved source semantics/coverage, fewer than 1,000 pre-2025 warm-up rows, warm-up starting after December 1, missing 2025 calendar months, incomplete fixed probe windows (>60s observed tick gaps or endpoint shortfall), or exact tick duplicates requiring review.

M1 missing-minute count includes session/weekend/holiday closures. It is diagnostic only. A month appearing in the file is not proof of complete history.

## PASS

All structural checks above pass, each fixed probe has coverage, and an independent `source_review.json` supplies:

```json
{
  "status": "PASS",
  "raw_sha256": {
    "metadata.json": "<original SHA-256>",
    "m1_warmup_2025_raw.csv": "<original SHA-256>",
    "tick_probes_raw.csv": "<original SHA-256>"
  },
  "server": "<exact original server>",
  "reviewer": "<independent reviewer identity>",
  "evidence": ["<time/DST receipt>", "<BID M1 identity receipt>", "<calendar coverage receipt>"],
  "timestamp_mapping": "UTC_RAW_SECONDS",
  "m1_identity": "BID_M1_BAR_OPEN",
  "coverage": "PASS",
  "xm_identity": true
}
```

These are evidence requirements, not values to guess. Reviewer assertions must be reviewed against referenced evidence; hashes alone are not authenticity proof. The original collector metadata remains immutable and UNVERIFIED/UNKNOWN. `chart_mode` must equal BID mode 0. No decoder is assumed for a different raw timestamp domain.

Stage 1 PASS permits **signal-only manifest construction**, not Discovery results. `packet_a_execution_pass` remains false. Stage 2 raw quote qualification must pass before Packet A's execution source PASS.
