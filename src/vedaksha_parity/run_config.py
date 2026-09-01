"""Modular run configuration: which oracles, which tiers, any per-oracle
ayanamsha override, and how much (if any) of the birth-data bank to draw
from — loaded from one YAML file rather than assembled from repeated CLI
flags, so every bias a run applies is visible in one place, not buried in
code. See docs/oracles.md and docs/birth-data.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from vedaksha_parity.birth_bank import DEFAULT_SOURCE


@dataclass(frozen=True)
class OracleRunConfig:
    name: str
    # None = engine default. Set when an oracle's own convention differs
    # (e.g. jyotishganit is fixed to True Chitrapaksha) to avoid a
    # mismatch masquerading as a divergence.
    ayanamsha: str | None = None
    # None = engine default ("7"). Set to "8" for PyJHora's 8-wide ranking.
    karaka_scheme: str | None = None
    # None = no limit. Caps distinct instants queried, so a run against a
    # slow oracle (e.g. jyotishganit) fails loudly instead of hanging.
    max_charts: int | None = None
    # None = oracle default ("true" for swisseph). "mean" compares against
    # a mean-only ayanamsha instead — see oracles/swisseph_oracle.py.
    ayanamsha_mode: str | None = None


@dataclass(frozen=True)
class SweepConfig:
    jd_from: float
    jd_to: float
    step_days: float = 30.0


@dataclass(frozen=True)
class BirthBankConfig:
    source: Path = DEFAULT_SOURCE
    # None = every record in `source` — full-file coverage, not a sample.
    count: int | None = None
    # Only consulted when count is set. None = a seed is generated and
    # recorded in case_params, so a sampled run stays reproducible.
    seed: int | None = None


@dataclass(frozen=True)
class RunConfig:
    oracles: list[OracleRunConfig]
    tiers: list[str]
    sweep: SweepConfig | None = None
    birth_bank: BirthBankConfig | None = None


def load_run_config(path: Path) -> RunConfig:
    data = yaml.safe_load(path.read_text()) or {}

    oracles_raw = data.get("oracles") or []
    if not oracles_raw:
        raise ValueError(f"{path}: 'oracles' must list at least one oracle")
    oracles = [
        OracleRunConfig(
            name=o["name"],
            ayanamsha=o.get("ayanamsha"),
            karaka_scheme=o.get("karaka_scheme"),
            max_charts=o.get("max_charts"),
            ayanamsha_mode=o.get("ayanamsha_mode"),
        )
        if isinstance(o, dict)
        else OracleRunConfig(name=o)
        for o in oracles_raw
    ]

    tiers = data.get("tiers") or []
    if not tiers:
        raise ValueError(f"{path}: 'tiers' must list at least one tier")

    sweep_raw = data.get("sweep")
    sweep = (
        SweepConfig(
            jd_from=sweep_raw["from"],
            jd_to=sweep_raw["to"],
            step_days=sweep_raw.get("step", 30.0),
        )
        if sweep_raw
        else None
    )

    bb_raw = data.get("birth_bank")
    birth_bank = (
        BirthBankConfig(
            source=Path(bb_raw.get("source", DEFAULT_SOURCE)),
            count=bb_raw.get("count"),
            seed=bb_raw.get("seed"),
        )
        if bb_raw is not None
        else None
    )

    if sweep is None and birth_bank is None:
        raise ValueError(
            f"{path}: at least one of 'sweep' or 'birth_bank' must be set — "
            "a run with neither has no case source"
        )

    return RunConfig(oracles=oracles, tiers=tiers, sweep=sweep, birth_bank=birth_bank)
