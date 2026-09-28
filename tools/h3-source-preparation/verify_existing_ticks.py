#!/usr/bin/env python3
"""Re-fetch existing Tick responses to recover missing retrieval-time evidence.

The original raw bytes remain unchanged. Each re-fetch is independently hashed
and compared with the stored response; a receipt is written immediately. A
mismatch is a source-identity HOLD, never an instruction to replace the file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


def verify(record: dict, root: Path) -> dict:
    name = f"{record['date']}_{record['hour']:02d}.json"
    receipt_path = root / "tick_retrieval_verification" / name
    if receipt_path.exists():
        prior = json.loads(receipt_path.read_text())
        if prior.get("stored_sha256") == record["sha256"] and prior.get("status") == "EXACT_MATCH":
            return prior
        return {"date": record["date"], "hour": record["hour"], "status": "HOLD_EXISTING_RECEIPT"}
    original = (root / record["relative_path"]).read_bytes()
    if hashlib.sha256(original).hexdigest() != record["sha256"]:
        return {"date": record["date"], "hour": record["hour"], "status": "HOLD_LOCAL_HASH_MISMATCH"}
    try:
        with urllib.request.urlopen(urllib.request.Request(record["url"], headers={"User-Agent": "h3-source-retrieval-verify/1"}), timeout=60) as response:
            fresh = response.read()
        verified_at = datetime.now(timezone.utc).isoformat()
    except (TimeoutError, urllib.error.URLError) as exc:
        return {"date": record["date"], "hour": record["hour"], "status": "HOLD_REFETCH", "error": str(exc)}
    fresh_hash = hashlib.sha256(fresh).hexdigest()
    receipt = {
        "date": record["date"], "hour": record["hour"], "source_url": record["url"],
        "stored_relative_path": record["relative_path"], "stored_sha256": record["sha256"],
        "verified_retrieval_at_utc": verified_at, "verified_response_bytes": len(fresh),
        "verified_response_sha256": fresh_hash,
        "status": "EXACT_MATCH" if fresh_hash == record["sha256"] and len(fresh) == record["byte_count"] else "HOLD_SOURCE_CHANGED",
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    with receipt_path.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=24)
    args = parser.parse_args()
    records = []
    for path in sorted(args.source_root.glob("tick_source_manifest_2026-*.json")):
        if path.stem.endswith("_initial"):
            continue
        records.extend(record for record in json.loads(path.read_text())["records"] if record["retrieved_at_utc"] is None)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = [future.result() for future in as_completed([pool.submit(verify, record, args.source_root) for record in records])]
    print(json.dumps({"missing_original_retrieval_timestamps": len(records),
                      "exact_refetch_matches": sum(r["status"] == "EXACT_MATCH" for r in results),
                      "hold": sum(r["status"] != "EXACT_MATCH" for r in results)}))


if __name__ == "__main__":
    main()
