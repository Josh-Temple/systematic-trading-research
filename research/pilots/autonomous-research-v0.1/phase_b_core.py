"""Phase B synthetic benchmark core for Autonomous Research Pilot v0.1.

Synthetic data only. This module does not load market data.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import evaluator

GENERATOR_VERSION = "ARP-B-GEN-v0.1"
PROTOCOL_PATH = Path(__file__).with_name("phase_b_protocol.json")


def load_protocol() -> dict[str, Any]:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def hash_json(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def seed_commitment(seed: bytes) -> str:
    if not isinstance(seed, bytes) or len(seed) < 16:
        raise ValueError("world seed must be at least 16 bytes")
    return hashlib.sha256(seed).hexdigest()


def _rng(seed: bytes, label: str) -> random.Random:
    digest = hashlib.sha256(seed + b"|" + label.encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:16], "big"))


def enumerate_strategy_space() -> list[dict[str, Any]]:
    protocol = load_protocol()
    space = protocol["candidate_space"]
    out: list[dict[str, Any]] = []
    index = 0
    transform_lags: list[tuple[str, int]] = []
    for item in space["transforms"]:
        for lag in item["lags"]:
            transform_lags.append((item["name"], lag))

    for source in space["sources"]:
        for transform, lag in transform_lags:
            for operator in space["operators"]:
                for threshold in space["thresholds"]:
                    for side in space["sides"]:
                        for position_size in space["position_sizes"]:
                            out.append(
                                {
                                    "candidate_id": f"SPACE-{index:03d}",
                                    "feature": {
                                        "source": source,
                                        "transform": transform,
                                        "lag": lag,
                                    },
                                    "operator": operator,
                                    "threshold": float(threshold),
                                    "side": side,
                                    "position_size": float(position_size),
                                }
                            )
                            index += 1

    expected = int(space["strategy_count"])
    if len(out) != expected:
        raise RuntimeError(
            f"candidate space mismatch: generated {len(out)} expected {expected}"
        )

    fingerprints = [evaluator.strategy_fingerprint(c) for c in out]
    if len(set(fingerprints)) != len(fingerprints):
        raise RuntimeError("candidate space contains duplicate strategy fingerprints")
    return out


def _rows_with_features(
    seed: bytes,
    label: str,
    count: int,
    start: datetime,
) -> list[dict[str, Any]]:
    rng = _rng(seed, label)
    x_a = rng.gauss(0.0, 0.5)
    x_b = rng.gauss(0.0, 0.5)
    rows: list[dict[str, Any]] = []

    for i in range(count):
        eps_a = rng.gauss(0.0, 1.0)
        eps_b = rng.gauss(0.0, 1.0)
        x_a = 0.62 * x_a + 0.78 * eps_a
        x_b = 0.48 * x_b + 0.30 * x_a + 0.70 * eps_b
        rows.append(
            {
                "timestamp": (start + timedelta(minutes=i)).isoformat(),
                "feature_a": x_a,
                "feature_b": x_b,
                "next_return": 0.0,
            }
        )
    return rows


def _signal_active_fraction(
    candidate: dict[str, Any],
    rows: list[dict[str, Any]],
) -> float:
    signal = evaluator.compile_signal(candidate, rows)
    usable = [float(x) for x in signal if x is not None]
    if not usable:
        return 0.0
    return sum(1 for x in usable if x != 0.0) / len(usable)


def _choose_planted_candidate(
    seed: bytes,
    adaptive_features: list[dict[str, Any]],
    final_features: list[dict[str, Any]],
) -> dict[str, Any]:
    candidates = [
        c
        for c in enumerate_strategy_space()
        if c["threshold"] in {-0.5, 0.0, 0.5}
    ]
    rng = _rng(seed, "plant-choice")
    order = list(range(len(candidates)))
    rng.shuffle(order)

    for idx in order:
        candidate = candidates[idx]
        adaptive_fraction = _signal_active_fraction(candidate, adaptive_features)
        final_fraction = _signal_active_fraction(candidate, final_features)
        if 0.15 <= adaptive_fraction <= 0.85 and 0.15 <= final_fraction <= 0.85:
            planted = json.loads(json.dumps(candidate))
            planted["candidate_id"] = "PLANTED"
            return planted

    raise RuntimeError("no suitable planted candidate found")


def _flip_side(candidate: dict[str, Any]) -> dict[str, Any]:
    flipped = json.loads(json.dumps(candidate))
    flipped["candidate_id"] = "PLANTED-FINAL"
    flipped["side"] = "short" if candidate["side"] == "long" else "long"
    return flipped


def _inject_outcomes(
    seed: bytes,
    label: str,
    rows: list[dict[str, Any]],
    planted: dict[str, Any],
    effect: float,
    noise_sigma: float,
) -> list[dict[str, Any]]:
    rng = _rng(seed, label)
    signal = evaluator.compile_signal(planted, rows)
    out: list[dict[str, Any]] = []

    for row, position in zip(rows, signal):
        p = 0.0 if position is None else float(position)
        next_return = effect * p + rng.gauss(0.0, noise_sigma)
        if not math.isfinite(next_return):
            raise RuntimeError("non-finite generated outcome")
        new_row = dict(row)
        new_row["next_return"] = next_return
        out.append(new_row)
    evaluator.validate_dataset(out)
    return out


@dataclass(frozen=True)
class HiddenWorld:
    world_id: str
    archetype: str
    seed_hex: str
    seed_commitment: str
    generator_version: str
    adaptive_rows: tuple[dict[str, Any], ...]
    final_rows: tuple[dict[str, Any], ...]
    adaptive_planted_candidate: dict[str, Any]
    final_planted_candidate: dict[str, Any]

    def public_manifest(self) -> dict[str, Any]:
        return {
            "world_id": self.world_id,
            "archetype": self.archetype,
            "seed_commitment": self.seed_commitment,
            "generator_version": self.generator_version,
            "adaptive_rows": len(self.adaptive_rows),
            "final_rows": len(self.final_rows),
        }


def generate_world(
    *,
    world_id: str,
    archetype: str,
    seed: bytes,
) -> HiddenWorld:
    protocol = load_protocol()
    allowed = set(protocol["worlds"]["archetypes"])
    if archetype not in allowed:
        raise ValueError(f"unknown archetype: {archetype}")
    if not isinstance(world_id, str) or not world_id:
        raise ValueError("world_id must be non-empty")

    adaptive_count = int(protocol["worlds"]["adaptive_rows"])
    final_count = int(protocol["worlds"]["final_rows"])

    adaptive_features = _rows_with_features(
        seed,
        "adaptive-features",
        adaptive_count,
        datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    final_features = _rows_with_features(
        seed,
        "final-features",
        final_count,
        datetime(2026, 2, 1, tzinfo=timezone.utc),
    )

    adaptive_plant = _choose_planted_candidate(
        seed, adaptive_features, final_features
    )

    if archetype == "BREAK":
        final_plant = _flip_side(adaptive_plant)
        final_effect = 0.012
    elif archetype == "WEAKENING":
        final_plant = json.loads(json.dumps(adaptive_plant))
        final_plant["candidate_id"] = "PLANTED-FINAL"
        final_effect = 0.0045
    else:
        final_plant = json.loads(json.dumps(adaptive_plant))
        final_plant["candidate_id"] = "PLANTED-FINAL"
        final_effect = 0.012

    adaptive_rows = _inject_outcomes(
        seed,
        "adaptive-noise",
        adaptive_features,
        adaptive_plant,
        effect=0.012,
        noise_sigma=0.020,
    )
    final_rows = _inject_outcomes(
        seed,
        "final-noise",
        final_features,
        final_plant,
        effect=final_effect,
        noise_sigma=0.020,
    )

    return HiddenWorld(
        world_id=world_id,
        archetype=archetype,
        seed_hex=seed.hex(),
        seed_commitment=seed_commitment(seed),
        generator_version=GENERATOR_VERSION,
        adaptive_rows=tuple(adaptive_rows),
        final_rows=tuple(final_rows),
        adaptive_planted_candidate=adaptive_plant,
        final_planted_candidate=final_plant,
    )


def dataset_hash(rows: tuple[dict[str, Any], ...] | list[dict[str, Any]]) -> str:
    return evaluator.dataset_hash(rows)


def evaluate_on_adaptive(
    world: HiddenWorld,
    candidate: dict[str, Any],
    *,
    known_strategy_fingerprints: set[str] | None = None,
) -> dict[str, Any]:
    return evaluator._evaluate_on_rows(
        candidate,
        world.adaptive_rows,
        dataset_id=f"{world.world_id}:ADAPTIVE_VALIDATION",
        known_strategy_fingerprints=known_strategy_fingerprints,
    )


def evaluate_on_final(
    world: HiddenWorld,
    candidate: dict[str, Any],
) -> dict[str, Any]:
    return evaluator._evaluate_on_rows(
        candidate,
        world.final_rows,
        dataset_id=f"{world.world_id}:FINAL_SYNTHETIC_HOLDOUT",
    )


def reveal_world(world: HiddenWorld) -> dict[str, Any]:
    """Post-final reproduction packet. Never expose this to the researcher pre-final."""
    return {
        **world.public_manifest(),
        "seed_hex": world.seed_hex,
        "adaptive_planted_strategy_fingerprint": evaluator.strategy_fingerprint(
            world.adaptive_planted_candidate
        ),
        "final_planted_strategy_fingerprint": evaluator.strategy_fingerprint(
            world.final_planted_candidate
        ),
        "adaptive_dataset_hash": dataset_hash(world.adaptive_rows),
        "final_dataset_hash": dataset_hash(world.final_rows),
    }
