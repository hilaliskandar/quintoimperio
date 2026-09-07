"""Regressões sentinela da baseline qualitativa P3 wave20."""
from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from simulate_p3_archetype import PLAYTEST_ARCHETYPES, run_player  # noqa: E402


def completed_for(seed: int) -> set[str]:
    return {
        archetype
        for i, archetype in enumerate(PLAYTEST_ARCHETYPES, start=1)
        if run_player(i, archetype, seed, wave=20)["completed"]
    }


def test_seed_24019_remains_extreme_tail() -> None:
    assert completed_for(24019) == set()


def test_seed_24010_distinguishes_survivalist_reserve() -> None:
    assert completed_for(24010) == {"SURVIVALIST"}


def test_seeds_24001_24002_require_high_robustness() -> None:
    expected = {"COMPLETIONIST", "SURVIVALIST"}
    assert completed_for(24001) == expected
    assert completed_for(24002) == expected


def test_seed_24004_is_low_stress_but_not_strategy_free() -> None:
    assert completed_for(24004) == set(PLAYTEST_ARCHETYPES) - {"ROGUELIKE", "SPEEDRUNNER"}
