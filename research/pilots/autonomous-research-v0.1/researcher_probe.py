#!/usr/bin/env python3
"""Researcher-side probe used by the Unix process-boundary integration test."""

from __future__ import annotations

import argparse
import json
import socket
from pathlib import Path


def request(socket_path: str, payload: bytes) -> dict:
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(socket_path)
    with client:
        client.sendall(payload)
        client.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            data += chunk
    return json.loads(data.decode("utf-8"))


def candidate() -> dict:
    return {
        "candidate_id": "BOUNDARY-VALID",
        "feature": {"source": "feature_a", "transform": "identity", "lag": 0},
        "operator": "gt",
        "threshold": 0.0,
        "side": "long",
        "position_size": 1.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", required=True)
    parser.add_argument("--hidden-dataset", required=True)
    parser.add_argument("--expected-dataset-id", required=True)
    args = parser.parse_args()

    hidden = Path(args.hidden_dataset)

    direct_read_denied = False
    try:
        hidden.read_bytes()
    except PermissionError:
        direct_read_denied = True

    if not direct_read_denied:
        raise AssertionError("researcher could directly read hidden dataset")

    valid = request(
        args.socket,
        json.dumps(candidate(), separators=(",", ":")).encode("utf-8"),
    )
    if valid.get("status") != "EVALUATED":
        raise AssertionError(f"valid candidate was not evaluated: {valid}")

    receipt = valid["receipt"]
    if receipt["dataset_id"] != args.expected_dataset_id:
        raise AssertionError("host did not bind receipt to hidden dataset id")
    if not receipt.get("dataset_hash"):
        raise AssertionError("hidden dataset hash missing from receipt")
    if receipt["scientific_status"] != "NOT_APPLICABLE":
        raise AssertionError("Phase A result was misclassified as scientific evidence")

    injected = candidate()
    injected["dataset_path"] = args.hidden_dataset
    denied_dataset_selection = request(
        args.socket,
        json.dumps(injected, separators=(",", ":")).encode("utf-8"),
    )
    if denied_dataset_selection.get("status") != "REJECTED":
        raise AssertionError("dataset selection injection was not rejected")
    if denied_dataset_selection.get("metrics") != {}:
        raise AssertionError("rejected dataset injection returned metrics")

    future = candidate()
    future["feature"]["source"] = "next_return"
    denied_future_source = request(
        args.socket,
        json.dumps(future, separators=(",", ":")).encode("utf-8"),
    )
    if denied_future_source.get("status") != "REJECTED":
        raise AssertionError("future outcome source was not rejected")
    if denied_future_source.get("metrics") != {}:
        raise AssertionError("rejected future source returned metrics")

    print(
        json.dumps(
            {
                "direct_hidden_read": "DENIED",
                "valid_candidate_api": "AVAILABLE",
                "dataset_selection_injection": "REJECTED",
                "future_outcome_source": "REJECTED",
                "dataset_id": receipt["dataset_id"],
                "validity_status": receipt["validity_status"],
                "scientific_status": receipt["scientific_status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
