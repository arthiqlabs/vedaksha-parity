"""Real PyJHora calls, no mock. Skips cleanly if the [pyjhora] extra is
not installed — see docs/oracles.md."""

import pytest

pytest.importorskip("jhora")

from vedaksha_parity.oracles.base import OracleUnsupported
from vedaksha_parity.oracles.pyjhora_oracle import PyJHoraOracle

J2000 = 2451545.0


@pytest.fixture(scope="module")
def oracle():
    return PyJHoraOracle()


def test_answer_refuses_position_and_ayanamsha(oracle):
    # Not circular (see module docstring) — just not built, a scope choice.
    for kind in ("position", "tropical_position", "ayanamsha"):
        with pytest.raises(OracleUnsupported):
            oracle.answer({"kind": kind, "jd_ut": J2000, "body": "Sun"})


def test_combustion_returns_a_state_for_each_answerable_body(oracle):
    for body in ("Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        result = oracle.answer({"kind": "combustion", "jd_ut": J2000, "body": body})
        assert result["planet"] == body
        assert result["state"] in {"Combust", "None"}  # never DeeplyCombust — see settings()


def test_combustion_refuses_the_sun(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "combustion", "jd_ut": J2000, "body": "Sun"})


def test_settings_documents_the_measured_independence_uncertainty(oracle):
    settings = oracle.settings()
    assert "Measured" in settings["independence_from_swisseph"]
    assert "DeeplyCombust" in settings["combustion"]


def test_karakas_returns_eight_ranked_grahas_in_vedakshas_own_titles(oracle):
    # Vedaksha's own 8-scheme titles, not PyJHora's (differs at rank 4 — module docstring).
    result = oracle.answer({"kind": "karakas", "jd_ut": J2000})
    assert [k["karaka"] for k in result] == [
        "Atmakaraka", "Amatyakaraka", "Bhratrikaraka", "Matrikaraka",
        "Pitrikaraka", "Putrakaraka", "Gnatikaraka", "Darakaraka",
    ]
    assert {k["planet"] for k in result} == {
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu",
    }


def test_settings_documents_the_karaka_scheme_and_naming_variant(oracle):
    settings = oracle.settings()
    assert "8" in settings["karakas"]
    assert "Matrikaraka" in settings["karakas"]


def test_chara_dasha_returns_twelve_sign_periods(oracle):
    result = oracle.answer(
        {"kind": "chara_dasha", "jd_ut": J2000, "latitude": 28.6139, "longitude": 77.2090}
    )
    assert len(result) == 12
    assert all(0 <= p["sign_index"] < 12 for p in result)
    assert all(p["start_jd"] < p["end_jd"] for p in result)
