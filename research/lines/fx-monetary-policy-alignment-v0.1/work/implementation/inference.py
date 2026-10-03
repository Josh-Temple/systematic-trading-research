"""Outcome-side inference primitives for RL-FXMP-001.

This module is implemented and tested only on synthetic values before any
market-outcome access. It does not load market data or policy data itself.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterable

ALIGNED = "ALIGNED"
OPPOSED = "OPPOSED"
NEUTRAL = "NEUTRAL"
VALID_CLASSES = {ALIGNED, OPPOSED, NEUTRAL, None}


class InferenceError(RuntimeError):
    pass


@dataclass(frozen=True)
class InferenceConfig:
    block_length: int = 12
    replicates: int = 10_000
    seed: int = 20_261_004
    min_aligned: int = 24
    min_opposed: int = 24


def _finite_float(value):
    if value is None:
        return None
    x = float(value)
    if not math.isfinite(x):
        raise InferenceError("nonfinite outcome")
    return x


def type7_percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        raise InferenceError("empty percentile input")
    if not 0.0 <= p <= 1.0:
        raise InferenceError("percentile p outside [0,1]")
    n = len(sorted_values)
    if n == 1:
        return sorted_values[0]
    h = (n - 1) * p
    lo = math.floor(h)
    hi = math.ceil(h)
    frac = h - lo
    if lo == hi:
        return sorted_values[lo]
    return sorted_values[lo] + frac * (sorted_values[hi] - sorted_values[lo])


def normalize_grid(slots: Iterable[dict]) -> list[dict]:
    out = []
    for idx, slot in enumerate(slots):
        classification = slot.get("classification")
        if classification not in VALID_CLASSES:
            raise InferenceError(f"invalid classification at slot {idx}: {classification!r}")
        y = _finite_float(slot.get("y"))
        out.append({
            "slot_id": slot.get("slot_id", idx),
            "classification": classification,
            "y": y,
        })
    if not out:
        raise InferenceError("empty calendar grid")
    return out


def group_values(grid: list[dict], indices: Iterable[int] | None = None) -> tuple[list[float], list[float]]:
    aligned: list[float] = []
    opposed: list[float] = []
    iterable = range(len(grid)) if indices is None else indices
    for i in iterable:
        slot = grid[i]
        y = slot["y"]
        if y is None:
            continue
        if slot["classification"] == ALIGNED:
            aligned.append(y)
        elif slot["classification"] == OPPOSED:
            opposed.append(y)
    return aligned, opposed


def mean(values: list[float]) -> float:
    if not values:
        raise InferenceError("empty mean group")
    return math.fsum(values) / len(values)


def difference(grid: list[dict], indices: Iterable[int] | None = None) -> tuple[float, int, int]:
    aligned, opposed = group_values(grid, indices)
    if not aligned or not opposed:
        raise InferenceError("aligned or opposed group empty")
    return mean(aligned) - mean(opposed), len(aligned), len(opposed)


def draw_circular_indices(n: int, block_length: int, rng: random.Random) -> list[int]:
    if n <= 0:
        raise InferenceError("n must be positive")
    if block_length <= 0:
        raise InferenceError("block length must be positive")
    blocks = math.ceil(n / block_length)
    indices: list[int] = []
    for _ in range(blocks):
        start = rng.randrange(n)
        indices.extend((start + j) % n for j in range(block_length))
    return indices[:n]


def evaluate(grid_input: Iterable[dict], config: InferenceConfig = InferenceConfig()) -> dict:
    grid = normalize_grid(grid_input)

    observed_d, n_aligned, n_opposed = difference(grid)
    if n_aligned < config.min_aligned or n_opposed < config.min_opposed:
        return {
            "status": "INSUFFICIENT_EVIDENCE",
            "observed_d": observed_d,
            "n_aligned": n_aligned,
            "n_opposed": n_opposed,
            "bootstrap": None,
        }

    if config.replicates <= 0:
        raise InferenceError("replicates must be positive")

    rng = random.Random(config.seed)
    boot: list[float] = []
    for replicate in range(config.replicates):
        indices = draw_circular_indices(len(grid), config.block_length, rng)
        try:
            d, _, _ = difference(grid, indices)
        except InferenceError as exc:
            raise InferenceError(f"bootstrap replicate {replicate} has empty primary group") from exc
        boot.append(d)

    boot.sort()
    lower = type7_percentile(boot, 0.025)
    median = type7_percentile(boot, 0.5)
    upper = type7_percentile(boot, 0.975)

    if observed_d <= 0:
        decision = "NOT_SUPPORTED"
    elif lower <= 0:
        decision = "INCONCLUSIVE"
    else:
        decision = "PROMISING_EXPLORATORY"

    return {
        "status": "OK",
        "observed_d": observed_d,
        "n_aligned": n_aligned,
        "n_opposed": n_opposed,
        "bootstrap": {
            "method": "circular_moving_block",
            "block_length": config.block_length,
            "replicates": config.replicates,
            "seed": config.seed,
            "lower_95": lower,
            "median": median,
            "upper_95": upper,
            "percentile_method": "type7_linear",
        },
        "decision": decision,
    }
