"""Real pyswisseph calls, no mock. Skips cleanly if the [swisseph] extra
is not installed — see docs/oracles.md."""

import pytest

pytest.importorskip("swisseph")

from vedaksha_parity.oracles.base import OracleUnsupported
from vedaksha_parity.oracles.swisseph_oracle import SwissephOracle

J2000 = 2451545.0


@pytest.fixture(scope="module")
def oracle():
    return SwissephOracle()


def test_position_returns_the_expected_fields(oracle):
    sun = oracle.answer({"kind": "position", "jd_ut": J2000, "body": "Sun"})
    assert set(sun) >= {"longitude", "latitude", "distance", "speed"}


def test_backend_is_undetermined_before_any_call():
    fresh = SwissephOracle()
    assert fresh.settings()["backends_used"] == "no cases run yet"
    assert "not yet determined" in fresh.NAME


def test_backend_is_recorded_after_a_real_call(oracle):
    oracle.answer({"kind": "position", "jd_ut": J2000, "body": "Sun"})
    backends = oracle.settings()["backends_used"]
    assert isinstance(backends, dict) and sum(backends.values()) >= 1
    assert set(backends) <= {"SWIEPH", "MOSEPH", "JPLEPH", "UNKNOWN"}


def test_require_swieph_raises_when_the_true_backend_is_unavailable():
    # This environment has no .se1 data files installed (confirmed
    # directly), so swisseph silently falls back to Moshier — exactly the
    # case require_swieph=True exists to catch instead of hiding.
    strict = SwissephOracle(require_swieph=True)
    with pytest.raises(OracleUnsupported, match="require_swieph"):
        strict.answer({"kind": "position", "jd_ut": J2000, "body": "Sun"})


def test_tropical_position_equals_sidereal_plus_true_ayanamsha_exactly(oracle):
    # TRUE ayanamsha (default): gap is exactly 0.0" — FLG_SIDEREAL already
    # has nutation-in-longitude baked in. MEAN alone leaves a ~14" gap.
    sidereal = oracle.answer({"kind": "position", "jd_ut": J2000, "body": "Sun"})
    tropical = oracle.answer({"kind": "tropical_position", "jd_ut": J2000, "body": "Sun"})
    true_ayanamsha = oracle.answer({"kind": "ayanamsha", "jd_ut": J2000})["value"]
    assert tropical["longitude"] == pytest.approx(
        (sidereal["longitude"] + true_ayanamsha) % 360.0, abs=1e-9
    )


def test_mean_ayanamsha_mode_differs_from_true_by_nutation_in_longitude(oracle):
    mean_oracle = SwissephOracle(ayanamsha_mode="mean")
    true_value = oracle.answer({"kind": "ayanamsha", "jd_ut": J2000})["value"]
    mean_value = mean_oracle.answer({"kind": "ayanamsha", "jd_ut": J2000})["value"]
    # Nutation in longitude is small and oscillating, not zero or huge.
    delta_arcsec = (true_value - mean_value) * 3600.0
    assert 1.0 < abs(delta_arcsec) < 30.0


def test_answer_refuses_an_unknown_ayanamsha_mode():
    with pytest.raises(OracleUnsupported):
        SwissephOracle(ayanamsha_mode="chitrapaksha")


def test_answer_refuses_an_unmapped_body(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "position", "jd_ut": J2000, "body": "Pluto"})


def test_answer_refuses_an_unknown_case_kind(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "koota", "jd_ut": J2000})


def test_ayanamsha_is_a_plausible_lahiri_value_at_j2000(oracle):
    result = oracle.answer({"kind": "ayanamsha", "jd_ut": J2000})
    assert 23.0 < result["value"] < 24.0


def test_settings_reports_the_ayanamsha_mode(oracle):
    assert oracle.settings()["ayanamsha_mode"] == "true"
    assert SwissephOracle(ayanamsha_mode="mean").settings()["ayanamsha_mode"] == "mean"


def test_houses_returns_asc_mc_and_twelve_cusps(oracle):
    result = oracle.answer(
        {"kind": "houses", "jd_ut": J2000, "latitude": 28.6139, "longitude": 77.2090}
    )
    assert set(result) == {"asc", "mc", "cusps"}
    assert len(result["cusps"]) == 12
    assert 0.0 <= result["asc"] < 360.0


def test_houses_refuses_an_unmapped_house_system(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer(
            {
                "kind": "houses", "jd_ut": J2000, "latitude": 28.6139, "longitude": 77.2090,
                "house_system": "Koch",
            }
        )
