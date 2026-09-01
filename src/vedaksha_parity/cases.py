"""Deterministic case generation. A stride grid, never random sampling — a
run must be exactly reproducible from its recorded (from, to, step)."""

from __future__ import annotations

from typing import Any

from vedaksha_parity.config import BODIES, COMBUSTION_BODIES, NODES


def jd_grid(jd_from: float, jd_to: float, step_days: float) -> list[float]:
    if step_days <= 0:
        raise ValueError("step_days must be positive")
    if jd_to < jd_from:
        raise ValueError("jd_to must be >= jd_from")
    out = []
    jd = jd_from
    while jd <= jd_to:
        out.append(jd)
        jd += step_days
    return out


def build_cases_t1(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    """T1 — raw sidereal position, classical grahas + both node conventions."""
    cases = []
    for jd_ut in jd_grid(jd_from, jd_to, step_days):
        for body in (*BODIES, *NODES):
            cases.append({"kind": "position", "jd_ut": jd_ut, "body": body})
    return cases


def build_cases_t2(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    """T2 — ayanamsha value."""
    return [{"kind": "ayanamsha", "jd_ut": jd_ut} for jd_ut in jd_grid(jd_from, jd_to, step_days)]


def build_cases_t1_tropical(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    """T1-tropical — tropical (sayana) position, classical grahas + both node
    conventions. A separate case kind from T1's sidereal one, never derived
    from it: several oracles (Skyfield+DE440/INPOP/Astronomy Engine) have no
    ayanamsha of their own and can only be compared tropical-to-tropical."""
    cases = []
    for jd_ut in jd_grid(jd_from, jd_to, step_days):
        for body in (*BODIES, *NODES):
            cases.append({"kind": "tropical_position", "jd_ut": jd_ut, "body": body})
    return cases


def build_cases_karakas(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    """Karakas — one case per instant, not per body: the answer is a full
    ranking over all seven grahas, not a per-body value."""
    return [{"kind": "karakas", "jd_ut": jd_ut} for jd_ut in jd_grid(jd_from, jd_to, step_days)]


def build_cases_combustion(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    """Combustion — six bodies, never the Sun (see config.COMBUSTION_BODIES)."""
    cases = []
    for jd_ut in jd_grid(jd_from, jd_to, step_days):
        for body in COMBUSTION_BODIES:
            cases.append({"kind": "combustion", "jd_ut": jd_ut, "body": body})
    return cases


def build_cases_drishti(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    """Drishti — one case per instant: the answer is the full aspect set
    across all nine grahas, not a per-body value."""
    return [{"kind": "drishti", "jd_ut": jd_ut} for jd_ut in jd_grid(jd_from, jd_to, step_days)]


def build_cases_dasha(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    """Dasha — one case per instant, Vimshottari system (the only one
    answerable without a real ascendant — see docs/tiers.md's Phase B)."""
    return [{"kind": "dasha", "jd_ut": jd_ut} for jd_ut in jd_grid(jd_from, jd_to, step_days)]
