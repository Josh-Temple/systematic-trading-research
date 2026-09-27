#!/usr/bin/env python3
"""Host-side Phase A evaluation service for the process-boundary test."""

from __future__ import annotations

import argparse
import json
import os
import socket
from pathlib import Path

import evaluator

MAX_REQUEST_BYTES = evaluator.MAX_CANDIDATE_JSON_BYTES + 1024


def send_json(conn: socket.socket, payload: dict) -> None:
    conn.sendall(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--dataset-id", required=True)
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    rows = json.loads(dataset_path.read_text(encoding="utf-8"))
    evaluator.validate_dataset(rows)

    socket_path = Path(args.socket)
    if socket_path.exists():
        socket_path.unlink()

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(str(socket_path))
    os.chmod(socket_path, 0o666)
    server.listen(8)

    try:
        while True:
            conn, _ = server.accept()
            with conn:
                raw = b""
                while len(raw) <= MAX_REQUEST_BYTES:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    raw += chunk

                if raw == b"__PHASE_A_STOP__":
                    send_json(conn, {"status": "STOPPING"})
                    return 0

                if len(raw) > MAX_REQUEST_BYTES:
                    send_json(
                        conn,
                        {
                            "status": "REJECTED",
                            "reason": "REQUEST_TOO_LARGE",
                            "metrics": {},
                        },
                    )
                    continue

                try:
                    text = raw.decode("utf-8", errors="strict")
                    candidate = evaluator.load_candidate_json(text)
                    receipt = evaluator._evaluate_on_rows(
                        candidate,
                        rows,
                        dataset_id=args.dataset_id,
                    )
                    send_json(
                        conn,
                        {
                            "status": "EVALUATED",
                            "receipt": receipt,
                        },
                    )
                except (UnicodeDecodeError, evaluator.CandidateInvalid) as exc:
                    send_json(
                        conn,
                        {
                            "status": "REJECTED",
                            "reason": type(exc).__name__,
                            "metrics": {},
                        },
                    )
    finally:
        server.close()
        if socket_path.exists():
            socket_path.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
