"""A second, deliberately adversarial case source — see review item 8.
`cases.py`'s uniform stride grid is reproducible, but a fixed step can
systematically undersample the numerically difficult regimes where a
real divergence is most likely to actually show up: station points,
perigee/apogee, longitude wraparound, conjunctions. This module finds
those instants directly from Vedaksha's own output (dense sampling +
sign-change/extremum/proximity detection on real values already
returned by `Engine.position()`), never from reading any reference's
source or internals — the same FIREWALL rule 1 discipline as everywhere
else in this project.

Detection is split from sampling on purpose: `sample_body` is the only
function that calls the engine (expensive, one real call per instant);
every `find_*` function is a pure function over already-computed
samples, so the detection logic itself is fully testable with synthetic
data, no engine or network access required.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise
from typing import Any

from vedaksha_parity.compare import circular_diff_deg
from vedaksha_parity.config import BODIES, NODES


@dataclass(frozen=True)
class Sample:
    jd_ut: float
    longitude: float
    speed: float
    distance: float


def sample_body(
    engine: Any, body: str, jd_from: float, jd_to: float, step_days: float, *, tropical: bool = False
) -> list[Sample]:
    """One real engine call per instant — the only expensive part. Kept
    separate from every detector below so a detector can be tested
    without needing Vedaksha at all."""
    if step_days <= 0:
        raise ValueError("step_days must be positive")
    method = engine.tropical_position if tropical else engine.position
    samples = []
    jd = jd_from
    while jd <= jd_to:
        answer = method(jd, body)
        samples.append(Sample(jd_ut=jd, longitude=answer["longitude"], speed=answer["speed"], distance=answer["distance"]))
        jd += step_days
    return samples


def find_station_points(samples: list[Sample]) -> list[float]:
    """Direct-to-retrograde or retrograde-to-direct — the instant a
    body's own apparent motion crosses zero. Returns the earlier sample's
    jd_ut of each bracketing pair (a real instant close to the true
    station, not the true station itself — refining further would need
    a root-finder this project doesn't have a reason to build yet)."""
    stations = []
    for prev, cur in pairwise(samples):
        if prev.speed == 0.0 or (prev.speed > 0) != (cur.speed > 0):
            stations.append(prev.jd_ut)
    return stations


def find_distance_extrema(samples: list[Sample]) -> dict[str, list[float]]:
    """Local minima (perigee-like closest approach) and maxima
    (apogee-like farthest point) of a body's own distance series."""
    minima, maxima = [], []
    for prev, cur, nxt in zip(samples, samples[1:], samples[2:], strict=False):
        if cur.distance < prev.distance and cur.distance < nxt.distance:
            minima.append(cur.jd_ut)
        elif cur.distance > prev.distance and cur.distance > nxt.distance:
            maxima.append(cur.jd_ut)
    return {"perigee": minima, "apogee": maxima}


def find_wraparound_instants(samples: list[Sample], threshold_deg: float = 2.0) -> list[float]:
    """Instants where longitude sits within threshold_deg of the 0/360
    boundary — where a circular-difference or modulo bug is most likely
    to surface, and where a naive linear interpolation would be wrong."""
    return [s.jd_ut for s in samples if s.longitude <= threshold_deg or s.longitude >= 360.0 - threshold_deg]


def find_conjunctions(
    samples_a: list[Sample], samples_b: list[Sample], threshold_deg: float = 2.0
) -> list[float]:
    """Instants where two bodies' own longitudes are within
    threshold_deg of each other — same-instant samples only, matched by
    jd_ut, since the two series need not share exactly the same grid."""
    by_jd_b = {s.jd_ut: s for s in samples_b}
    return [
        s_a.jd_ut
        for s_a in samples_a
        if s_a.jd_ut in by_jd_b
        and abs(circular_diff_deg(s_a.longitude, by_jd_b[s_a.jd_ut].longitude)) <= threshold_deg
    ]


def build_pathological_cases(
    engine: Any,
    bodies: list[str],
    jd_from: float,
    jd_to: float,
    step_days: float = 1.0,
    *,
    kind: str = "position",
    wraparound_threshold_deg: float = 2.0,
    conjunction_threshold_deg: float = 2.0,
) -> list[dict[str, Any]]:
    """Samples every body once over (jd_from, jd_to, step_days), runs
    every detector, and returns one case per (flagged instant, body) pair
    for every body in `bodies` — not just the body whose own event
    flagged that instant, since a station/wraparound/conjunction is a
    property of the whole chart at that moment, not of one body alone.
    Same case shape as cases.py's builders, so this drops straight into
    the existing runner/comparators with no special handling."""
    tropical = kind == "tropical_position"
    samples_by_body = {b: sample_body(engine, b, jd_from, jd_to, step_days, tropical=tropical) for b in bodies}

    flagged: set[float] = set()
    for body, samples in samples_by_body.items():
        flagged.update(find_station_points(samples))
        flagged.update(find_wraparound_instants(samples, threshold_deg=wraparound_threshold_deg))
        if body == "Moon":
            extrema = find_distance_extrema(samples)
            flagged.update(extrema["perigee"])
            flagged.update(extrema["apogee"])
    for i, body_a in enumerate(bodies):
        for body_b in bodies[i + 1 :]:
            flagged.update(
                find_conjunctions(
                    samples_by_body[body_a], samples_by_body[body_b], threshold_deg=conjunction_threshold_deg
                )
            )

    return [
        {"kind": kind, "jd_ut": jd_ut, "body": body}
        for jd_ut in sorted(flagged)
        for body in bodies
    ]


def build_cases_t1_adversarial(jd_from: float, jd_to: float, step_days: float) -> list[dict[str, Any]]:
    """T1-adversarial — same `(jd_from, jd_to, step_days)` shape as every
    other tier builder in `cases.py`, so it drops straight into
    `cli.TIER_BUILDERS`, but `step_days` here means something different: the
    density of the internal scan used to *find* pathological instants, not
    the spacing of the resulting cases (a smaller step means a more
    thorough, more expensive scan, not more cases). Builds its own throwaway
    `Engine()` to do that scan — a case builder in this project never takes
    an engine argument, and the real engine `run_cases` compares against is
    built separately by the caller, so this one is deliberately query-only
    and discarded afterward."""
    from vedaksha_parity.engine import Engine

    engine = Engine()
    return build_pathological_cases(engine, [*BODIES, *NODES], jd_from, jd_to, step_days)
