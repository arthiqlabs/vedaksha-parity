"""Detectors are pure functions over pre-computed samples -- tested here
with synthetic data, no engine or network access needed. One real,
end-to-end test at the bottom proves the wiring against the actual
engine."""

from __future__ import annotations

import pytest

from vedaksha_parity.engine import Engine
from vedaksha_parity.pathological_cases import (
    Sample,
    build_cases_t1_adversarial,
    build_pathological_cases,
    find_conjunctions,
    find_distance_extrema,
    find_station_points,
    find_wraparound_instants,
    sample_body,
)


def _samples(*rows: tuple[float, float, float, float]) -> list[Sample]:
    return [Sample(jd_ut=jd, longitude=lon, speed=speed, distance=dist) for jd, lon, speed, dist in rows]


def test_find_station_points_detects_a_sign_change():
    samples = _samples(
        (1.0, 10.0, 0.9, 1.0),
        (2.0, 10.9, 0.5, 1.0),
        (3.0, 11.2, -0.3, 1.0),  # speed flips negative here
        (4.0, 10.8, -0.6, 1.0),
    )
    stations = find_station_points(samples)
    assert stations == [2.0]  # the sample just before the sign flip


def test_find_station_points_ignores_a_series_with_no_sign_change():
    samples = _samples((1.0, 10.0, 0.9, 1.0), (2.0, 10.9, 0.5, 1.0), (3.0, 11.2, 0.3, 1.0))
    assert find_station_points(samples) == []


def test_find_station_points_catches_an_exact_zero():
    samples = _samples((1.0, 10.0, 0.5, 1.0), (2.0, 10.5, 0.0, 1.0), (3.0, 10.5, -0.5, 1.0))
    assert 1.0 in find_station_points(samples)


def test_find_distance_extrema_finds_a_local_minimum_and_maximum():
    # distance dips at jd=2 (perigee-like) then peaks at jd=4 (apogee-like)
    samples = _samples(
        (1.0, 0.0, 0.0, 1.0),
        (2.0, 0.0, 0.0, 0.5),
        (3.0, 0.0, 0.0, 0.8),
        (4.0, 0.0, 0.0, 1.2),
        (5.0, 0.0, 0.0, 0.9),
    )
    extrema = find_distance_extrema(samples)
    assert extrema["perigee"] == [2.0]
    assert extrema["apogee"] == [4.0]


def test_find_wraparound_instants_flags_longitude_near_the_boundary():
    samples = _samples(
        (1.0, 1.5, 0.0, 1.0),    # near 0
        (2.0, 180.0, 0.0, 1.0),  # nowhere near a boundary
        (3.0, 358.7, 0.0, 1.0),  # near 360
    )
    flagged = find_wraparound_instants(samples, threshold_deg=2.0)
    assert flagged == [1.0, 3.0]


def test_find_conjunctions_matches_close_longitudes_at_the_same_instant():
    a = _samples((1.0, 100.0, 0.0, 1.0), (2.0, 200.0, 0.0, 1.0))
    b = _samples((1.0, 101.5, 0.0, 1.0), (2.0, 50.0, 0.0, 1.0))
    assert find_conjunctions(a, b, threshold_deg=2.0) == [1.0]


def test_find_conjunctions_handles_the_0_360_wraparound_correctly():
    # 359 and 1 degree are 2 degrees apart on the circle, not 358.
    a = _samples((1.0, 359.0, 0.0, 1.0))
    b = _samples((1.0, 1.0, 0.0, 1.0))
    assert find_conjunctions(a, b, threshold_deg=3.0) == [1.0]
    assert find_conjunctions(a, b, threshold_deg=1.0) == []


def test_find_conjunctions_only_compares_matching_instants():
    a = _samples((1.0, 100.0, 0.0, 1.0))
    b = _samples((2.0, 100.0, 0.0, 1.0))  # different jd_ut -- must not match
    assert find_conjunctions(a, b, threshold_deg=5.0) == []


def test_sample_body_rejects_a_non_positive_step():
    with pytest.raises(ValueError):
        sample_body(engine=None, body="Sun", jd_from=0.0, jd_to=10.0, step_days=0.0)


# --- real, end-to-end (needs the actual Vedaksha engine) ---

J2000 = 2451545.0


def test_build_pathological_cases_end_to_end_against_the_real_engine():
    engine = Engine()
    cases = build_pathological_cases(
        engine, ["Sun", "Moon"], J2000, J2000 + 40.0, step_days=2.0
    )
    assert all(c["kind"] == "position" and c["body"] in ("Sun", "Moon") for c in cases)
    # Moon moves ~13 deg/day and the Sun ~1 deg/day over a 40-day, 2-day-step
    # window -- real longitude data over this span should trip at least the
    # wraparound-proximity or Moon-distance-extremum detectors.
    assert len(cases) > 0


def test_build_cases_t1_adversarial_matches_the_tier_builder_signature():
    # (jd_from, jd_to, step_days) -- the exact shape cli.TIER_BUILDERS calls
    # every tier builder with; this one also builds its own throwaway
    # Engine() internally, unlike cases.py's builders.
    cases = build_cases_t1_adversarial(J2000, J2000 + 40.0, 2.0)
    assert all(c["kind"] == "position" and "jd_ut" in c and "body" in c for c in cases)


def test_t1_adversarial_is_registered_in_the_cli_tier_builders():
    from vedaksha_parity.cli import TIER_BUILDERS

    assert TIER_BUILDERS["t1-adversarial"] is build_cases_t1_adversarial
