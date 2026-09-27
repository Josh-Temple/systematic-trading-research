#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PILOT_DIR="$(cd "${HERE}/.." && pwd)"
RESEARCHER_USER="phasea_researcher"
HIDDEN_DIR="$(mktemp -d)"
PUBLIC_DIR="$(mktemp -d)"
EXCHANGE_DIR="$(mktemp -d)"
SENTINEL="HIDDEN_PHASE_A_SENTINEL_20260927"

cleanup() {
  sudo userdel "${RESEARCHER_USER}" >/dev/null 2>&1 || true
  rm -rf "${HIDDEN_DIR}" "${PUBLIC_DIR}" "${EXCHANGE_DIR}"
}
trap cleanup EXIT

if id "${RESEARCHER_USER}" >/dev/null 2>&1; then
  sudo userdel "${RESEARCHER_USER}" >/dev/null 2>&1 || true
fi
sudo useradd --system --no-create-home --shell /usr/sbin/nologin "${RESEARCHER_USER}"

HIDDEN_FILE="${HIDDEN_DIR}/hidden_dataset.json"
PUBLIC_EVALUATOR="${PUBLIC_DIR}/evaluator.py"
CANDIDATE_FILE="${EXCHANGE_DIR}/candidate.json"
REPORT_FILE="${EXCHANGE_DIR}/researcher_report.json"
RECEIPT_FILE="${EXCHANGE_DIR}/receipt.json"

python3 - "${HIDDEN_FILE}" "${SENTINEL}" <<'PY'
import json
import sys
from pathlib import Path

hidden_path = Path(sys.argv[1])
sentinel = sys.argv[2]
payload = {
    "dataset_id": "SYNTHETIC-PROCESS-ISOLATION-v01",
    "sentinel": sentinel,
    "rows": [
        {"timestamp": "2026-02-01T00:00:00+00:00", "feature_a": -1.0, "feature_b": 0.4, "next_return": -0.012},
        {"timestamp": "2026-02-01T00:01:00+00:00", "feature_a": 0.3, "feature_b": -0.2, "next_return": 0.004},
        {"timestamp": "2026-02-01T00:02:00+00:00", "feature_a": 0.8, "feature_b": -0.3, "next_return": 0.010},
        {"timestamp": "2026-02-01T00:03:00+00:00", "feature_a": -0.4, "feature_b": 0.5, "next_return": -0.005},
        {"timestamp": "2026-02-01T00:04:00+00:00", "feature_a": 1.2, "feature_b": -0.7, "next_return": 0.015}
    ]
}
hidden_path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
PY

cp "${PILOT_DIR}/evaluator.py" "${PUBLIC_EVALUATOR}"

chmod 700 "${HIDDEN_DIR}"
chmod 755 "${PUBLIC_DIR}"
chmod 444 "${PUBLIC_EVALUATOR}"
chmod 777 "${EXCHANGE_DIR}"

# Deliberately disclose the exact hidden path. Access must fail because of OS permissions,
# not because the researcher does not know where the data are.
sudo -u "${RESEARCHER_USER}" env -i   PATH="/usr/local/bin:/usr/bin:/bin"   HOME="${EXCHANGE_DIR}"   LANG="C.UTF-8"   python3 "${HERE}/researcher_probe.py"   --hidden "${HIDDEN_FILE}"   --evaluator-source "${PUBLIC_EVALUATOR}"   --candidate-out "${CANDIDATE_FILE}"   --report-out "${REPORT_FILE}"

python3 "${HERE}/host_eval.py"   --hidden "${HIDDEN_FILE}"   --candidate "${CANDIDATE_FILE}"   --receipt-out "${RECEIPT_FILE}"

python3 "${HERE}/verify_isolation.py"   --report "${REPORT_FILE}"   --receipt "${RECEIPT_FILE}"   --hidden-sentinel "${SENTINEL}"

echo "PROCESS_ISOLATION_CHECK=PASS"
