"""Real geographic locations as a case source for location-dependent
quantities (house cusps, vargas, panchanga, bhavas, ashtakavarga,
lagna-based dasha) — see docs/tiers.md's "Phase B" section.

Crossed with a sweep of instants, not the birth bank: Phase B tests the
house/location math itself, so controlled geographic coverage matters
more than real-person sampling.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from vedaksha_parity.cases import jd_grid

DEFAULT_SOURCE = Path("data/location-grid.csv")


@dataclass(frozen=True)
class Location:
    name: str
    category: str
    latitude: float
    longitude: float


def load_location_grid(source: Path = DEFAULT_SOURCE) -> list[Location]:
    """Parse every row in file order — deterministic, matching
    birth_bank.load_birth_bank's own discipline."""
    with source.open(newline="", encoding="utf-8") as f:
        return [
            Location(
                name=row["name"],
                category=row["category"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
            )
            for row in csv.DictReader(f)
        ]


def build_cases_houses(
    locations: list[Location], jd_from: float, jd_to: float, step_days: float
) -> list[dict[str, Any]]:
    """One case per (location, instant) pair — house cusps depend on both,
    unlike every case kind built before Phase B."""
    return [
        {
            "kind": "houses",
            "jd_ut": jd_ut,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "location_name": loc.name,
        }
        for jd_ut in jd_grid(jd_from, jd_to, step_days)
        for loc in locations
    ]


def build_cases_vargas(
    locations: list[Location], jd_from: float, jd_to: float, step_days: float, division: str = "D9"
) -> list[dict[str, Any]]:
    """One case per (location, instant) pair, one division per case —
    matching houses' shape plus the division this quantity is asked
    about."""
    return [
        {
            "kind": "vargas",
            "jd_ut": jd_ut,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "location_name": loc.name,
            "division": division,
        }
        for jd_ut in jd_grid(jd_from, jd_to, step_days)
        for loc in locations
    ]


def build_cases_vargas_default_grid(
    jd_from: float, jd_to: float, step_days: float
) -> list[dict[str, Any]]:
    """D9 (Navamsa) — the most commonly tested division — against the
    default full location grid. Matches TIER_BUILDERS' (from, to, step)
    signature; use build_cases_vargas directly for a different division
    or a narrower grid."""
    return build_cases_vargas(load_location_grid(), jd_from, jd_to, step_days, division="D9")


def _build_location_instant_cases(
    kind: str, locations: list[Location], jd_from: float, jd_to: float, step_days: float
) -> list[dict[str, Any]]:
    """Shared shape for the Phase B tiers that need only (kind, jd_ut,
    latitude, longitude, location_name) — bhavas, ashtakavarga, panchanga.
    houses/vargas keep their own builders since they carry extra fields
    (house_system, division)."""
    return [
        {
            "kind": kind,
            "jd_ut": jd_ut,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "location_name": loc.name,
        }
        for jd_ut in jd_grid(jd_from, jd_to, step_days)
        for loc in locations
    ]


def build_cases_bhavas(
    locations: list[Location], jd_from: float, jd_to: float, step_days: float
) -> list[dict[str, Any]]:
    return _build_location_instant_cases("bhavas", locations, jd_from, jd_to, step_days)


def build_cases_bhavas_default_grid(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    return build_cases_bhavas(load_location_grid(), jd_from, jd_to, step_days)


def build_cases_ashtakavarga(
    locations: list[Location], jd_from: float, jd_to: float, step_days: float
) -> list[dict[str, Any]]:
    return _build_location_instant_cases("ashtakavarga", locations, jd_from, jd_to, step_days)


def build_cases_ashtakavarga_default_grid(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    return build_cases_ashtakavarga(load_location_grid(), jd_from, jd_to, step_days)


def build_cases_panchanga(
    locations: list[Location], jd_from: float, jd_to: float, step_days: float
) -> list[dict[str, Any]]:
    return _build_location_instant_cases("panchanga", locations, jd_from, jd_to, step_days)


def build_cases_panchanga_default_grid(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    return build_cases_panchanga(load_location_grid(), jd_from, jd_to, step_days)


def build_cases_chara_dasha(
    locations: list[Location], jd_from: float, jd_to: float, step_days: float
) -> list[dict[str, Any]]:
    return _build_location_instant_cases("chara_dasha", locations, jd_from, jd_to, step_days)


def build_cases_chara_dasha_default_grid(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    return build_cases_chara_dasha(load_location_grid(), jd_from, jd_to, step_days)


def build_cases_houses_default_grid(
    jd_from: float, jd_to: float, step_days: float
) -> list[dict[str, Any]]:
    """Matches TIER_BUILDERS' (from, to, step) signature with the default
    grid. Use build_cases_houses directly for a narrower grid."""
    return build_cases_houses(load_location_grid(), jd_from, jd_to, step_days)
