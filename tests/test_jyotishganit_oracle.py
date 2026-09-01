"""Real jyotishganit calls, no mock. Skips cleanly if the [jyotishganit]
extra is not installed — see docs/oracles.md."""

import pytest

pytest.importorskip("jyotishganit")

from vedaksha_parity.oracles.base import OracleUnsupported
from vedaksha_parity.oracles.jyotishganit_oracle import JyotishganitOracle

J2000 = 2451545.0


@pytest.fixture(scope="module")
def oracle():
    return JyotishganitOracle()


def test_position_returns_longitude_only_never_fabricated_fields(oracle):
    sun = oracle.answer({"kind": "position", "jd_ut": J2000, "body": "Sun"})
    assert set(sun) == {"longitude", "is_retrograde"}
    assert 0.0 <= sun["longitude"] < 360.0


def test_answer_refuses_ayanamsha(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "ayanamsha", "jd_ut": J2000})


def test_answer_refuses_tropical_position(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "tropical_position", "jd_ut": J2000, "body": "Sun"})


def test_answer_refuses_true_node(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "position", "jd_ut": J2000, "body": "TrueNode"})


def test_mean_node_maps_to_rahu(oracle):
    rahu = oracle.answer({"kind": "position", "jd_ut": J2000, "body": "MeanNode"})
    assert 0.0 <= rahu["longitude"] < 360.0


def test_drishti_returns_sign_based_aspects_with_no_strength_field(oracle):
    aspects = oracle.answer({"kind": "drishti", "jd_ut": J2000})
    assert len(aspects) > 0
    assert all(set(a) == {"aspecting_planet", "aspected_sign"} for a in aspects)
    assert all(0 <= a["aspected_sign"] < 12 for a in aspects)


def test_vargas_returns_sign_indices_including_lagna(oracle):
    result = oracle.answer(
        {"kind": "vargas", "jd_ut": J2000, "latitude": 28.6139, "longitude": 77.2090, "division": "D9"}
    )
    assert "Lagna" in result
    assert all(0 <= v < 12 for v in result.values())
    assert "TrueNode" not in result  # jyotishganit exposes only the mean node


def test_vargas_refuses_a_division_it_does_not_compute(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer(
            {"kind": "vargas", "jd_ut": J2000, "latitude": 28.6139, "longitude": 77.2090, "division": "D1"}
        )


def test_bhavas_returns_twelve_houses_with_classification_flags(oracle):
    result = oracle.answer(
        {"kind": "bhavas", "jd_ut": J2000, "latitude": 28.6139, "longitude": 77.2090}
    )
    assert len(result) == 12
    assert {h["bhava"] for h in result} == set(range(1, 13))
    assert all(0 <= h["sign"] < 12 for h in result)


def test_ashtakavarga_returns_twelve_sign_bindu_counts(oracle):
    result = oracle.answer(
        {"kind": "ashtakavarga", "jd_ut": J2000, "latitude": 28.6139, "longitude": 77.2090}
    )
    assert len(result) == 12
    assert all(isinstance(v, int) for v in result)


def test_panchanga_returns_five_limb_names(oracle):
    result = oracle.answer(
        {"kind": "panchanga", "jd_ut": J2000, "latitude": 28.6139, "longitude": 77.2090}
    )
    assert set(result) == {"tithi", "nakshatra", "yoga", "karana", "vara"}
    assert all(isinstance(v, str) for v in result.values())


def test_dasha_returns_nine_periods_in_classical_vimshottari_order(oracle):
    result = oracle.answer({"kind": "dasha", "jd_ut": J2000})
    lords = [p["lord"] for p in result["maha_dashas"]]
    assert set(lords) == {
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
    }
    # Continuous, no gap — period 0's start convention is separate (compare.py).
    periods = result["maha_dashas"]
    from itertools import pairwise

    for prev, cur in pairwise(periods):
        assert prev["end_jd"] == pytest.approx(cur["start_jd"], abs=1e-6)
