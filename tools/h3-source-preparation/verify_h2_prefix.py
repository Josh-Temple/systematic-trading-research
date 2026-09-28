#!/usr/bin/env python3
"""Re-fetch the frozen H2 M1 generator prefix and verify exact raw identities.

This checks source bytes only. It does not decode events or run the generator.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


MANIFEST_SHA256 = "1232af3b557a9559ca22f03e7c21ff748d467794cdaec5b32ddd9c0b437fcec3"
ROUTE_PREFIX = "https://jetta.dukascopy.com/v1/candles/minute/XAU-USD/BID/"


def verify(row: dict, root: Path) -> dict:
    day = row["session_date_utc"]
    url = row["exact_retrieval_route"]
    if not url.startswith(ROUTE_PREFIX) or row["raw_payload_archive_path"] != f"m1_raw/{day}.json":
        raise ValueError(f"unexpected_route_or_path:{day}")
    path = root / "m1_raw" / f"{day}.json"
    retrieved_at = None
    if path.exists():
        raw = path.read_bytes()
        origin = "EXISTING_READBACK"
    else:
        for attempt in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "h3-prefix-identity/1"}), timeout=45) as response:
                    raw = response.read()
                retrieved_at = datetime.now(timezone.utc).isoformat()
                break
            except (TimeoutError, OSError):
                if attempt == 2:
                    raise
                time.sleep(1 + attempt)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("xb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            origin = "NEW_DOWNLOAD"
        except FileExistsError:
            raw = path.read_bytes()
            origin = "CONCURRENT_EXISTING_READBACK"
    digest = hashlib.sha256(raw).hexdigest()
    passed = (
        len(raw) == int(row["raw_payload_byte_size"])
        and digest == row["raw_payload_sha256"] == row["manifest_sha256"]
        and hashlib.sha256(path.read_bytes()).hexdigest() == digest
    )
    return {
        "date": day, "sample_role": row["sample_role"], "source_batch": row["source_batch"],
        "route": url, "relative_path": f"m1_raw/{day}.json",
        "retrieved_at_utc": retrieved_at, "origin": origin,
        "byte_count": len(raw), "sha256": digest,
        "expected_sha256": row["raw_payload_sha256"],
        "expected_byte_count": int(row["raw_payload_byte_size"]),
        "identity": "PASS" if passed else "HOLD_MISMATCH",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frozen-manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    manifest_bytes = args.frozen_manifest.read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256:
        raise ValueError("frozen_manifest_identity_mismatch")
    rows = list(csv.DictReader(manifest_bytes.decode("utf-8").splitlines()))
    dates = [row["session_date_utc"] for row in rows]
    if len(rows) != 135 or len(set(dates)) != 135 or dates != sorted(dates):
        raise ValueError("frozen_prefix_order_or_count_mismatch")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(verify, row, args.output) for row in rows]
        records = [future.result() for future in as_completed(futures)]
    records.sort(key=lambda record: record["date"])
    passed = all(record["identity"] == "PASS" for record in records)
    result = {
        "scope": "H3_OUTCOME_BLIND_H2_FIXED_PREFIX_SOURCE_IDENTITY",
        "frozen_manifest_url": "https://drive.google.com/file/d/1Zu0xNyLfSABItcAgZqKtxmaAi-nzEWvR/view",
        "frozen_manifest_sha256": MANIFEST_SHA256,
        "first_date": records[0]["date"], "last_date": records[-1]["date"],
        "record_count": len(records),
        "identity": "PASS_135_EXACT_RAW_MATCH" if passed else "HOLD_MISMATCH",
        "generator_run": False, "outcome_computed": False,
        "records": records,
    }
    target = args.output / "h2_prefix_source_identity.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"identity": result["identity"], "records": len(records), "manifest": str(target)}))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
