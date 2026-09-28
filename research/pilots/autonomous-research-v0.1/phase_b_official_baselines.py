"""Official Phase B non-AI baseline batch runner.

This creates synthetic-only baseline results under the frozen ARP-B-v0.1 protocol
plus ARP-B-v0.1.1-A1 amendment. Metric-bearing results are written to files and
are not printed by this module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
from pathlib import Path
from typing import Any

import evaluator
import phase_b_baselines
import phase_b_core

HERE = Path(__file__).resolve().parent
AMENDMENT_PATH = HERE / "phase_b_protocol_amendment_v0.1.1.json"
OFFICIAL_WORLD_SPECS = (
    ("STABLE-01", "STABLE"),
    ("STABLE-02", "STABLE"),
    ("WEAKENING-01", "WEAKENING"),
    ("WEAKENING-02", "WEAKENING"),
    ("BREAK-01", "BREAK"),
    ("BREAK-02", "BREAK"),
)
OFFICIAL_RANDOM_REPETITIONS = 200


class OfficialBaselineError(RuntimeError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def load_amendment() -> dict[str, Any]:
    return json.loads(AMENDMENT_PATH.read_text(encoding="utf-8"))


def validate_frozen_protocol() -> None:
    protocol = phase_b_core.load_protocol()
    amendment = load_amendment()

    if protocol["protocol_id"] != "ARP-B-v0.1":
        raise OfficialBaselineError("unexpected parent protocol")
    if protocol["status"] != "FROZEN_BEFORE_PHASE_B_RESULTS":
        raise OfficialBaselineError("parent protocol is not frozen")
    if protocol["market_data_allowed"] is not False:
        raise OfficialBaselineError("market data must remain forbidden")
    if protocol["baselines"]["random_repetitions_per_world"] != OFFICIAL_RANDOM_REPETITIONS:
        raise OfficialBaselineError("random baseline repetition count drift")
    if protocol["worlds"]["total_worlds"] != len(OFFICIAL_WORLD_SPECS):
        raise OfficialBaselineError("world count drift")

    if amendment["amendment_id"] != "ARP-B-v0.1.1-A1":
        raise OfficialBaselineError("unexpected protocol amendment")
    if amendment["parent_protocol_id"] != protocol["protocol_id"]:
        raise OfficialBaselineError("amendment parent mismatch")
    if amendment["status"] != "FROZEN_BEFORE_OFFICIAL_PHASE_B_RESULTS":
        raise OfficialBaselineError("amendment is not frozen")
    if amendment["changes"]["baseline_result_visibility_to_ai"] is not False:
        raise OfficialBaselineError("baseline results must remain hidden from AI")
    if amendment["changes"]["host_state_visibility_to_ai"] is not False:
        raise OfficialBaselineError("host state must remain hidden from AI")


def derive_random_baseline_seed(world_seed: bytes, repetition: int) -> int:
    digest = hashlib.sha256(
        world_seed
        + b"|ARP-B-v0.1|random-baseline|"
        + str(repetition).encode("ascii")
    ).digest()
    return int.from_bytes(digest[:8], "big")


def make_host_state(run_label: str) -> dict[str, Any]:
    worlds = []
    for world_id, archetype in OFFICIAL_WORLD_SPECS:
        seed = secrets.token_bytes(32)
        worlds.append(
            {
                "world_id": world_id,
                "archetype": archetype,
                "seed_hex": seed.hex(),
                "seed_commitment": phase_b_core.seed_commitment(seed),
            }
        )
    return {
        "state_version": "0.1",
        "run_label": run_label,
        "protocol_id": "ARP-B-v0.1",
        "amendment_id": "ARP-B-v0.1.1-A1",
        "checkpoint_key_hex": secrets.token_bytes(32).hex(),
        "worlds": worlds,
    }


def public_commitments(host_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "manifest_version": "0.1",
        "run_label": host_state["run_label"],
        "protocol_id": host_state["protocol_id"],
        "amendment_id": host_state["amendment_id"],
        "generator_version": phase_b_core.GENERATOR_VERSION,
        "host_state_hash": sha256_json(host_state),
        "worlds": [
            {
                "world_id": item["world_id"],
                "archetype": item["archetype"],
                "seed_commitment": item["seed_commitment"],
            }
            for item in host_state["worlds"]
        ],
    }


def _write_json(path: Path, value: Any, *, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json(value) + b"\n")
    if mode is not None:
        os.chmod(path, mode)


def _append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as f:
        f.write(canonical_json(value) + b"\n")


def run_batch(
    *,
    output_root: str | Path,
    host_state: dict[str, Any],
    random_repetitions: int,
    print_progress: bool = False,
) -> dict[str, Any]:
    if random_repetitions < 1:
        raise OfficialBaselineError("random_repetitions must be positive")

    output_root = Path(output_root)
    host_dir = output_root / "host_state"
    public_dir = output_root / "public"
    results_dir = output_root / "results"
    ledgers_dir = results_dir / "ledgers"
    summaries_path = results_dir / "baseline_summaries.jsonl"

    commitments = public_commitments(host_state)
    _write_json(host_dir / "host_state.json", host_state, mode=0o600)
    _write_json(public_dir / "commitments.json", commitments, mode=0o644)

    checkpoint_key = bytes.fromhex(host_state["checkpoint_key_hex"])
    if len(checkpoint_key) != 32:
        raise OfficialBaselineError("checkpoint key must be 32 bytes")

    world_counts = []
    total_runs = 0

    for item in host_state["worlds"]:
        seed = bytes.fromhex(item["seed_hex"])
        if phase_b_core.seed_commitment(seed) != item["seed_commitment"]:
            raise OfficialBaselineError("seed commitment mismatch in host state")

        world = phase_b_core.generate_world(
            world_id=item["world_id"],
            archetype=item["archetype"],
            seed=seed,
        )

        random_count = 0
        for repetition in range(random_repetitions):
            baseline_seed = derive_random_baseline_seed(seed, repetition)
            ledger_path = (
                ledgers_dir
                / item["world_id"]
                / f"random-{repetition:03d}.jsonl"
            )
            summary = phase_b_baselines.run_random_search(
                world=world,
                run_id=f"{host_state['run_label']}:{item['world_id']}:RANDOM:{repetition:03d}",
                baseline_seed=baseline_seed,
                ledger_path=ledger_path,
                checkpoint_key=checkpoint_key,
            )
            summary.update(
                {
                    "protocol_id": host_state["protocol_id"],
                    "amendment_id": host_state["amendment_id"],
                    "world_archetype": item["archetype"],
                    "seed_commitment": item["seed_commitment"],
                    "random_repetition": repetition,
                    "ledger_path": str(
                        ledger_path.relative_to(output_root)
                    ),
                }
            )
            _append_jsonl(summaries_path, summary)
            random_count += 1
            total_runs += 1

        deterministic_ledger = (
            ledgers_dir / item["world_id"] / "deterministic-adaptive.jsonl"
        )
        deterministic = phase_b_baselines.run_deterministic_adaptive(
            world=world,
            run_id=f"{host_state['run_label']}:{item['world_id']}:DETERMINISTIC_ADAPTIVE",
            ledger_path=deterministic_ledger,
            checkpoint_key=checkpoint_key,
        )
        deterministic.update(
            {
                "protocol_id": host_state["protocol_id"],
                "amendment_id": host_state["amendment_id"],
                "world_archetype": item["archetype"],
                "seed_commitment": item["seed_commitment"],
                "random_repetition": None,
                "ledger_path": str(
                    deterministic_ledger.relative_to(output_root)
                ),
            }
        )
        _append_jsonl(summaries_path, deterministic)
        total_runs += 1

        world_counts.append(
            {
                "world_id": item["world_id"],
                "archetype": item["archetype"],
                "random_runs": random_count,
                "deterministic_runs": 1,
            }
        )
        if print_progress:
            print(
                f"world={item['world_id']} "
                f"random_runs={random_count} deterministic_runs=1 complete"
            )

    manifest = {
        "manifest_version": "0.1",
        "run_kind": "OFFICIAL_NON_AI_BASELINES",
        "run_label": host_state["run_label"],
        "protocol_id": host_state["protocol_id"],
        "amendment_id": host_state["amendment_id"],
        "generator_version": phase_b_core.GENERATOR_VERSION,
        "host_state_hash": commitments["host_state_hash"],
        "world_count": len(host_state["worlds"]),
        "random_repetitions_per_world": random_repetitions,
        "total_method_world_runs": total_runs,
        "ai_researcher_run": False,
        "market_data_used": False,
        "metric_results_in_workflow_log": False,
        "world_counts": world_counts,
    }
    _write_json(results_dir / "results_manifest.json", manifest, mode=0o644)

    # Verify every persisted ledger/checkpoint before declaring the batch complete.
    summary_lines = summaries_path.read_text(encoding="utf-8").splitlines()
    if len(summary_lines) != total_runs:
        raise OfficialBaselineError("summary count mismatch")
    for line in summary_lines:
        summary = json.loads(line)
        ledger = output_root / summary["ledger_path"]
        evaluator.verify_ledger_checkpoint(
            ledger,
            summary["ledger_checkpoint"],
            checkpoint_key,
        )

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--run-label", required=True)
    args = parser.parse_args()

    validate_frozen_protocol()
    host_state = make_host_state(args.run_label)
    commitments = public_commitments(host_state)

    # Safe pre-result output: commitments contain no raw seed or metric.
    print(
        json.dumps(
            {
                "phase_b_official_baselines": "START",
                "run_label": args.run_label,
                "protocol_id": commitments["protocol_id"],
                "amendment_id": commitments["amendment_id"],
                "host_state_hash": commitments["host_state_hash"],
                "world_commitments": commitments["worlds"],
            },
            sort_keys=True,
        )
    )

    manifest = run_batch(
        output_root=args.output_root,
        host_state=host_state,
        random_repetitions=OFFICIAL_RANDOM_REPETITIONS,
        print_progress=True,
    )

    # Safe post-result output: counts/status only, no candidate/metric/seed.
    print(
        json.dumps(
            {
                "phase_b_official_baselines": "COMPLETE",
                "run_label": manifest["run_label"],
                "world_count": manifest["world_count"],
                "random_repetitions_per_world": manifest[
                    "random_repetitions_per_world"
                ],
                "total_method_world_runs": manifest["total_method_world_runs"],
                "market_data_used": manifest["market_data_used"],
                "metric_results_in_workflow_log": manifest[
                    "metric_results_in_workflow_log"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
