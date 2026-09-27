#!/usr/bin/env python3
"""Host-side evaluator for Phase A process-isolation integration check."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

PILOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PILOT_DIR))

import evaluator  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hidden", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--receipt-out", required=True)
    args = ap.parse_args()

    hidden = json.loads(Path(args.hidden).read_text(encoding="utf-8"))
    if not isinstance(hidden, dict):
        raise SystemExit("hidden dataset envelope must be an object")
    dataset_id = hidden.get("dataset_id")
    rows = hidden.get("rows")
    if not isinstance(dataset_id, str) or not dataset_id:
        raise SystemExit("hidden dataset_id missing")
    if not isinstance(rows, list):
        raise SystemExit("hidden rows missing")

    candidate_text = Path(args.candidate).read_text(encoding="utf-8")
    candidate = evaluator.load_candidate_json(candidate_text)
    receipt = evaluator._evaluate_on_rows(
        candidate,
        rows,
        dataset_id=dataset_id,
    )

    if receipt["execution_status"] != "SUCCESS":
        raise SystemExit("host evaluation did not execute successfully")
    if receipt["validity_status"] != "VALID":
        raise SystemExit("researcher candidate was not valid")
    if receipt["scientific_status"] != "NOT_APPLICABLE":
        raise SystemExit("Phase A isolation check must not produce a scientific result")
    if not math.isfinite(receipt["metrics"]["mean_return"]):
        raise SystemExit("host metric is not finite")

    Path(args.receipt_out).write_text(
        json.dumps(receipt, sort_keys=True, indent=2),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
