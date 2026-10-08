#!/usr/bin/env python3
"""Run FXNS synthetic tests only. No market data, HTTP, or broker endpoints.

This driver applies a process-level socket deny before importing project code.
It is not a security sandbox against arbitrary malicious Python; the tested
source and workflow should still be reviewed before execution.
"""
from __future__ import annotations

import socket
import sys
import unittest
from pathlib import Path


def _deny_network(*args, **kwargs):
    raise RuntimeError("FXNS_OFFLINE_TEST_NETWORK_FORBIDDEN")


socket.socket.connect = _deny_network
socket.socket.connect_ex = _deny_network
socket.create_connection = _deny_network

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "research/lines/fx-news-sentiment-v0.1/work"
SUITES = ("implementation", "source-probe")


def main() -> int:
    if not WORK.is_dir():
        raise SystemExit("Missing exact FXNS work tree; no fake PASS")
    combined = unittest.TestSuite()
    for section in SUITES:
        folder = WORK / section
        if not folder.is_dir():
            raise SystemExit(f"Missing suite directory: {section}")
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir=str(folder), pattern="test_*.py")
        count = suite.countTestCases()
        if count < 1:
            raise SystemExit(f"Empty suite: {section}")
        print(f"FXNS_OFFLINE_SUITE: {section}, discovered={count}", flush=True)
        combined.addTests(suite)

    count = combined.countTestCases()
    print(f"FXNS_OFFLINE_TOTAL_DISCOVERED: {count}", flush=True)
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(combined)
    print(
        f"FXNS_OFFLINE_RESULT: run={result.testsRun}; "
        f"failures={len(result.failures)}; errors={len(result.errors)}; "
        f"skipped={len(result.skipped)}; successful={result.wasSuccessful()}",
        flush=True,
    )
    return 0 if result.wasSuccessful() and result.testsRun == count else 1


if __name__ == "__main__":
    raise SystemExit(main())
