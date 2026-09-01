from vedaksha_parity.cases import build_cases_t1, build_cases_t1_tropical, build_cases_t2, jd_grid


def test_jd_grid_is_deterministic_and_inclusive_of_the_endpoints_it_lands_on():
    grid = jd_grid(2451545.0, 2451545.0 + 60.0, 30.0)
    assert grid == [2451545.0, 2451575.0, 2451605.0]


def test_jd_grid_rejects_a_backwards_range():
    import pytest

    with pytest.raises(ValueError):
        jd_grid(10.0, 5.0, 1.0)


def test_build_cases_t1_covers_every_body_at_every_grid_point():
    cases = build_cases_t1(2451545.0, 2451545.0, 30.0)
    bodies = {c["body"] for c in cases}
    assert bodies == {
        "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
        "MeanNode", "TrueNode",
    }
    assert all(c["kind"] == "position" for c in cases)


def test_build_cases_t1_tropical_covers_every_body_at_every_grid_point_as_tropical():
    cases = build_cases_t1_tropical(2451545.0, 2451545.0, 30.0)
    bodies = {c["body"] for c in cases}
    assert bodies == {
        "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
        "MeanNode", "TrueNode",
    }
    assert all(c["kind"] == "tropical_position" for c in cases)


def test_build_cases_t2_is_one_case_per_grid_point():
    cases = build_cases_t2(2451545.0, 2451545.0 + 60.0, 30.0)
    assert len(cases) == 3
    assert all(c["kind"] == "ayanamsha" for c in cases)
