"""Phase B non-AI baselines under the frozen search budget."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any

import evaluator
import phase_b_core
from phase_b_search import SearchHost


def _strategy_key(candidate: dict[str, Any]) -> tuple[Any, ...]:
    feature = candidate["feature"]
    return (
        feature["source"],
        (feature["transform"], feature["lag"]),
        candidate["operator"],
        candidate["threshold"],
        candidate["side"],
    )


def _one_field_neighbor(a: dict[str, Any], b: dict[str, Any]) -> bool:
    ka = _strategy_key(a)
    kb = _strategy_key(b)
    return sum(x != y for x, y in zip(ka, kb)) == 1


def run_random_search(
    *,
    world: phase_b_core.HiddenWorld,
    run_id: str,
    baseline_seed: int,
    ledger_path: str | Path,
    checkpoint_key: bytes,
) -> dict[str, Any]:
    protocol = phase_b_core.load_protocol()
    budget = int(protocol["search"]["submissions_per_world_method"])
    per_round = int(protocol["search"]["max_proposals_per_round"])
    rounds = int(protocol["search"]["rounds"])

    space = phase_b_core.enumerate_strategy_space()
    rng = random.Random(baseline_seed)
    selected = rng.sample(space, budget)

    host = SearchHost(
        run_id=run_id,
        method="RANDOM",
        world=world,
        ledger_path=ledger_path,
        checkpoint_key=checkpoint_key,
    )

    cursor = 0
    for round_number in range(1, rounds + 1):
        for _ in range(per_round):
            host.submit(round_number=round_number, candidate=selected[cursor])
            cursor += 1
        host.close_round(round_number)

    summary = host.finalize()
    summary["baseline_seed"] = baseline_seed
    return summary


def _unseen_neighbors(
    best_candidate: dict[str, Any],
    seen_fingerprints: set[str],
) -> list[dict[str, Any]]:
    neighbors = []
    for candidate in phase_b_core.enumerate_strategy_space():
        fp = evaluator.strategy_fingerprint(candidate)
        if fp in seen_fingerprints:
            continue
        if _one_field_neighbor(best_candidate, candidate):
            neighbors.append(candidate)
    return neighbors


def run_deterministic_adaptive(
    *,
    world: phase_b_core.HiddenWorld,
    run_id: str,
    ledger_path: str | Path,
    checkpoint_key: bytes,
) -> dict[str, Any]:
    protocol = phase_b_core.load_protocol()
    per_round = int(protocol["search"]["max_proposals_per_round"])
    rounds = int(protocol["search"]["rounds"])
    space = phase_b_core.enumerate_strategy_space()

    host = SearchHost(
        run_id=run_id,
        method="DETERMINISTIC_ADAPTIVE",
        world=world,
        ledger_path=ledger_path,
        checkpoint_key=checkpoint_key,
    )

    # Frozen interpretation of "protocol-defined ordering": canonical space order.
    proposals = list(space[:per_round])

    for round_number in range(1, rounds + 1):
        if round_number > 1:
            best = host.best_adaptive_record()["candidate"]
            seen = {
                r["strategy_fingerprint"]
                for r in host.records
                if r["strategy_fingerprint"]
            }
            proposals = _unseen_neighbors(best, seen)[:per_round]
            if len(proposals) < per_round:
                existing = {
                    evaluator.strategy_fingerprint(c) for c in proposals
                } | seen
                for candidate in space:
                    fp = evaluator.strategy_fingerprint(candidate)
                    if fp not in existing:
                        proposals.append(candidate)
                        existing.add(fp)
                    if len(proposals) == per_round:
                        break

        for candidate in proposals:
            host.submit(round_number=round_number, candidate=candidate)
        host.close_round(round_number)

    return host.finalize()
