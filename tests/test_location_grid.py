"""Real, no mock: parses the actual bundled location grid. See docs/tiers.md."""

from __future__ import annotations

import pytest

from vedaksha_parity.location_grid import (
    DEFAULT_SOURCE,
    build_cases_ashtakavarga_default_grid,
    build_cases_bhavas_default_grid,
    build_cases_chara_dasha_default_grid,
    build_cases_houses,
    build_cases_houses_default_grid,
    build_cases_panchanga_default_grid,
    build_cases_vargas,
    build_cases_vargas_default_grid,
    load_location_grid,
)

pytestmark = pytest.mark.skipif(
    not DEFAULT_SOURCE.exists(), reason="bundled location grid CSV not present"
)


@pytest.fixture(scope="module")
def locations():
    return load_location_grid()


def test_load_location_grid_parses_all_thirty_cities(locations):
    assert len(locations) == 30
    assert {loc.category for loc in locations} == {"india", "diaspora"}
    assert sum(1 for loc in locations if loc.category == "india") == 20
    assert sum(1 for loc in locations if loc.category == "diaspora") == 10


def test_build_cases_houses_is_one_case_per_location_per_instant(locations):
    cases = build_cases_houses(locations[:3], 2451545.0, 2451545.0, 30.0)
    assert len(cases) == 3
    assert all(c["kind"] == "houses" for c in cases)
    assert {c["location_name"] for c in cases} == {loc.name for loc in locations[:3]}


def test_build_cases_houses_default_grid_uses_all_thirty_cities():
    cases = build_cases_houses_default_grid(2451545.0, 2451545.0, 30.0)
    assert len(cases) == 30


def test_build_cases_vargas_defaults_to_d9(locations):
    cases = build_cases_vargas(locations[:2], 2451545.0, 2451545.0, 30.0)
    assert len(cases) == 2
    assert all(c["kind"] == "vargas" and c["division"] == "D9" for c in cases)


def test_build_cases_vargas_default_grid_uses_all_thirty_cities():
    cases = build_cases_vargas_default_grid(2451545.0, 2451545.0, 30.0)
    assert len(cases) == 30


@pytest.mark.parametrize(
    ("builder", "kind"),
    [
        (build_cases_bhavas_default_grid, "bhavas"),
        (build_cases_ashtakavarga_default_grid, "ashtakavarga"),
        (build_cases_panchanga_default_grid, "panchanga"),
        (build_cases_chara_dasha_default_grid, "chara_dasha"),
    ],
)
def test_location_instant_builders_use_all_thirty_cities(builder, kind):
    cases = builder(2451545.0, 2451545.0, 30.0)
    assert len(cases) == 30
    assert all(c["kind"] == kind for c in cases)
