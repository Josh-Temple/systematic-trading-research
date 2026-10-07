"""Verify all issued JP225 forecast records against the frozen record contract.

This is an offline structural and integrity check, not market-outcome evaluation.
No market data or broker routes are accessed.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from forecast_core import canonical_sha256
from record_contract import validate_forecast_record


def main() -> None:
    directory = Path(__file__).resolve().parents[2] / "forecasts"
    paths = sorted(directory.glob("20??-??-??_A?_forecast.json"))
    if not paths:
        raise ValueError("No issued forecast JSON files found")

    by_event: dict[str, set[str]] = defaultdict(set)
    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        validate_forecast_record(record)

        fields = path.name.split("_")
        date_text, system_id = fields[0], fields[1]
        expected_event = "XPF-JP225-" + date_text.replace("-", "")
        if record["event_id"] != expected_event or record["system_id"] != system_id:
            raise ValueError(f"{path.name}: path/event/system identity mismatch")
        if system_id in by_event[expected_event]:
            raise ValueError(f"{path.name}: duplicate system for event")
        by_event[expected_event].add(system_id)

        declared_hash = record.get("canonical_sha256")
        if not isinstance(declared_hash, str) or len(declared_hash) != 64:
            raise ValueError(f"{path.name}: canonical_sha256 missing or malformed")
        actual_hash = canonical_sha256(
            {k: v for k, v in record.items() if k != "canonical_sha256"}
        )
        if declared_hash != actual_hash:
            raise ValueError(f"{path.name}: canonical_sha256 mismatch")
        print(f"PASS {path.name}: contract / event identity / SHA-256")

    for event_id, systems in sorted(by_event.items()):
        if systems != {"A1", "A2", "A3"}:
            raise ValueError(f"{event_id}: incomplete A1/A2/A3 event: {sorted(systems)}")
    print(f"PASS: {len(paths)} issued forecast records / {len(by_event)} complete events")


if __name__ == "__main__":
    main()
