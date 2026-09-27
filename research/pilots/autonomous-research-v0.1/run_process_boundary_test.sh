#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
SOCKET_PATH="$TMP/evaluator.sock"
HIDDEN_PATH="$TMP/hidden_dataset.json"
DATASET_ID="SYNTHETIC-PHASE-A-HIDDEN-RUNTIME"

cleanup() {
  if [[ -n "${HOST_PID:-}" ]] && kill -0 "$HOST_PID" 2>/dev/null; then
    kill "$HOST_PID" 2>/dev/null || true
    wait "$HOST_PID" 2>/dev/null || true
  fi
  rm -rf "$TMP"
}
trap cleanup EXIT

chmod 755 "$TMP"
cp "$HERE/researcher_probe.py" "$TMP/researcher_probe.py"
chmod 644 "$TMP/researcher_probe.py"

python - "$HIDDEN_PATH" <<'PY'
import json
import secrets
import sys
from datetime import datetime, timedelta, timezone

path = sys.argv[1]
base = datetime(2026, 1, 1, tzinfo=timezone.utc)
rows = []
for i in range(12):
    sign = -1.0 if i % 2 == 0 else 1.0
    feature_a = sign * (1.0 + secrets.randbelow(1000000) / 1000000.0)
    feature_b = (secrets.randbelow(2000001) - 1000000) / 1000000.0
    next_return = (secrets.randbelow(20001) - 10000) / 1000000.0
    rows.append(
        {
            "timestamp": (base + timedelta(minutes=i)).isoformat(),
            "feature_a": feature_a,
            "feature_b": feature_b,
            "next_return": next_return,
        }
    )

with open(path, "w", encoding="utf-8") as f:
    json.dump(rows, f, separators=(",", ":"), allow_nan=False)
PY

chmod 600 "$HIDDEN_PATH"

(
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 python boundary_host.py     --socket "$SOCKET_PATH"     --dataset "$HIDDEN_PATH"     --dataset-id "$DATASET_ID"
) &
HOST_PID=$!

for _ in $(seq 1 100); do
  if [[ -S "$SOCKET_PATH" ]]; then
    break
  fi
  if ! kill -0 "$HOST_PID" 2>/dev/null; then
    echo "host process exited before socket became ready" >&2
    exit 1
  fi
  sleep 0.05
done

if [[ ! -S "$SOCKET_PATH" ]]; then
  echo "host socket did not become ready" >&2
  exit 1
fi

sudo -u nobody env PYTHONDONTWRITEBYTECODE=1   python "$TMP/researcher_probe.py"   --socket "$SOCKET_PATH"   --hidden-dataset "$HIDDEN_PATH"   --expected-dataset-id "$DATASET_ID"

python - "$SOCKET_PATH" <<'PY'
import socket
import sys

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(sys.argv[1])
with client:
    client.sendall(b"__PHASE_A_STOP__")
    client.shutdown(socket.SHUT_WR)
    client.recv(4096)
PY

wait "$HOST_PID"
unset HOST_PID
