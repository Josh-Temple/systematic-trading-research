#!/usr/bin/env python3
"""Verify the observable boundary from the Phase A OS-user isolation check."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FORBIDDEN_ENV_MARKERS = ("TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "API_KEY")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--hidden-sentinel", required=True)
    args = ap.parse_args()

    report_text = Path(args.report).read_text(encoding="utf-8")
    receipt_text = Path(args.receipt).read_text(encoding="utf-8")
    report = json.loads(report_text)
    receipt = json.loads(receipt_text)

    if report["hidden_readable"] is not False:
        raise SystemExit("researcher unexpectedly read hidden data")
    if report["hidden_read_error"] not in {"PermissionError", "OSError"}:
        raise SystemExit(f"unexpected hidden-read error: {report['hidden_read_error']}")
    if report["evaluator_source_readable"] is not True:
        raise SystemExit("researcher could not read the public evaluator contract")
    if report["evaluator_source_writable"] is not False:
        raise SystemExit("researcher unexpectedly modified evaluator source")
    if args.hidden_sentinel in report_text:
        raise SystemExit("hidden sentinel leaked into researcher report")

    exposed = [
        key for key in report.get("environment_keys", [])
        if any(marker in key.upper() for marker in FORBIDDEN_ENV_MARKERS)
    ]
    if exposed:
        raise SystemExit(f"sensitive-looking environment keys exposed: {exposed}")

    if receipt["execution_status"] != "SUCCESS":
        raise SystemExit("receipt execution status is not SUCCESS")
    if receipt["validity_status"] != "VALID":
        raise SystemExit("receipt validity status is not VALID")
    if receipt["scientific_status"] != "NOT_APPLICABLE":
        raise SystemExit("isolation test must remain scientifically NOT_APPLICABLE")
    if receipt["dataset_id"] != "SYNTHETIC-PROCESS-ISOLATION-v01":
        raise SystemExit("unexpected hidden dataset identity")
    if args.hidden_sentinel in receipt_text:
        raise SystemExit("sentinel should not be echoed into result receipt")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
