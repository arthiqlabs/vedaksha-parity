"""These tests call the real, published `vedaksha` package — the same one
docs/oracles.md and FIREWALL.md describe as the engine under test. No mock."""

import re
import tomllib
from itertools import pairwise
from pathlib import Path

import pytest

from vedaksha_parity.engine import Engine

J2000 = 2451545.0


@pytest.fixture(scope="module")
def engine():
    return Engine()


def test_installed_vedaksha_matches_the_pinned_version(engine):
    # Catches the environment silently drifting from the pin (e.g. a stale install).
    pyproject = tomllib.loads(Path(__file__).parent.parent.joinpath("pyproject.toml").read_text())
    deps = pyproject["project"]["dependencies"]
    pin = next(d for d in deps if d.startswith("vedaksha=="))
    pinned_version = re.fullmatch(r"vedaksha==([\w.]+)", pin).group(1)
    assert engine.VERSION == pinned_version


def test_position_returns_the_expected_fields(engine):
    sun = engine.position(J2000, "Sun")
    assert set(sun) >= {"longitude", "latitude", "distance", "speed"}
    assert 0.0 <= sun["longitude"] < 360.0


def test_position_raises_a_clean_error_for_an_unknown_body(engine):
    with pytest.raises(KeyError):
        engine.position(J2000, "Pluto")


def test_ayanamsha_is_a_plausible_lahiri_value_at_j2000(engine):
    # Sanity band only — confirms "this is Lahiri," not precision.
    value = engine.ayanamsha(J2000)
    assert 23.0 < value < 24.0


def test_tropical_position_equals_sidereal_plus_ayanamsha(engine):
    sidereal = engine.position(J2000, "Sun")
    tropical = engine.tropical_position(J2000, "Sun")
    ayanamsha = engine.ayanamsha(J2000)
    assert tropical["longitude"] == pytest.approx(
        (sidereal["longitude"] + ayanamsha) % 360.0, abs=1e-9
    )
    # Longitude-shift-invariant fields carry over unchanged.
    assert tropical["latitude"] == sidereal["latitude"]
    assert tropical["distance"] == sidereal["distance"]
    assert tropical["speed"] == sidereal["speed"]


def test_ayanamsha_override_changes_the_reported_settings_and_the_value():
    default_engine = Engine()
    overridden_engine = Engine(ayanamsha="TrueChitra")
    assert default_engine.settings()["ayanamsha"] == "IndianOfficial"
    assert overridden_engine.settings()["ayanamsha"] == "TrueChitra"
    assert default_engine.ayanamsha(J2000) != overridden_engine.ayanamsha(J2000)


def test_karakas_returns_seven_ranked_grahas(engine):
    karakas = engine.karakas(J2000)
    assert len(karakas) == 7
    assert {k["karaka"] for k in karakas} == {
        "Atmakaraka", "Amatyakaraka", "Bhratrikaraka", "Matrikaraka",
        "Putrakaraka", "Gnatikaraka", "Darakaraka",
    }
    assert {k["planet"] for k in karakas} == {
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    }


def test_karaka_scheme_eight_adds_rahu_and_pitrikaraka():
    # scheme="8" is what compares against PyJHora's 8-wide ranking.
    eight_scheme_engine = Engine(karaka_scheme="8")
    assert eight_scheme_engine.settings()["karaka_scheme"] == "8"
    karakas = eight_scheme_engine.karakas(J2000)
    assert len(karakas) == 8
    assert {k["karaka"] for k in karakas} == {
        "Atmakaraka", "Amatyakaraka", "Bhratrikaraka", "Matrikaraka",
        "Pitrikaraka", "Putrakaraka", "Gnatikaraka", "Darakaraka",
    }
    assert {k["planet"] for k in karakas} == {
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu",
    }


def test_combustion_returns_a_state_for_the_requested_body(engine):
    result = engine.combustion(J2000, "Mercury")
    assert result["planet"] == "Mercury"
    assert result["state"] in {"Combust", "DeeplyCombust", "None"}


def test_combustion_raises_a_clean_error_for_the_sun(engine):
    # Sun is not one of the six bodies compute_combustion returns.
    with pytest.raises(KeyError):
        engine.combustion(J2000, "Sun")


def test_drishti_returns_aspects_for_all_nine_grahas(engine):
    aspects = engine.drishti(J2000)
    assert len(aspects) > 0
    # compute_drishti names it "Rahu", not natal_chart's "MeanNode".
    assert {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"} <= {
        a["aspecting_planet"] for a in aspects
    }


def test_dasha_returns_the_nine_graha_lords_in_a_full_cycle(engine):
    result = engine.dasha(J2000)
    lords = [p["lord"] for p in result["maha_dashas"]]
    assert set(lords) == {
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
    }
    # Vimshottari periods run consecutively with no gap.
    for prev, cur in pairwise(result["maha_dashas"]):
        assert prev["end_jd"] == cur["start_jd"]


def test_houses_returns_asc_mc_and_twelve_cusps(engine):
    result = engine.houses(J2000, 28.6139, 77.2090)  # New Delhi
    assert set(result) == {"asc", "mc", "cusps", "system", "polar_fallback"}
    assert len(result["cusps"]) == 12
    assert 0.0 <= result["asc"] < 360.0


def test_houses_differs_by_location_unlike_position(engine):
    # Houses DO depend on real location, unlike position/ayanamsha.
    delhi = engine.houses(J2000, 28.6139, 77.2090)
    london = engine.houses(J2000, 51.5074, -0.1278)
    assert delhi["asc"] != london["asc"]


def test_vargas_returns_lagna_and_nine_bodies_as_sign_indices(engine):
    result = engine.vargas(J2000, 28.6139, 77.2090, "D9")
    assert "Lagna" in result
    assert set(result) - {"Lagna"} == {
        "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "MeanNode", "TrueNode",
    }
    assert all(0 <= v < 12 for v in result.values())


def test_bhavas_returns_twelve_houses(engine):
    result = engine.bhavas(J2000, 28.6139, 77.2090)
    assert len(result) == 12
    assert {h["bhava"] for h in result} == set(range(1, 13))


def test_ashtakavarga_returns_twelve_sign_bindu_counts(engine):
    result = engine.ashtakavarga(J2000, 28.6139, 77.2090)
    assert len(result) == 12
    assert all(isinstance(v, int) for v in result)


def test_panchanga_returns_five_limbs(engine):
    result = engine.panchanga(J2000, 28.6139, 77.2090)
    assert set(result) == {"tithi", "nakshatra", "yoga", "karana", "vara"}


def test_chara_dasha_returns_twelve_sign_periods(engine):
    result = engine.chara_dasha(J2000, 28.6139, 77.2090)
    assert len(result) == 12
    assert all(0 <= p["sign_index"] < 12 for p in result)
    for prev, cur in pairwise(result):
        assert prev["end_jd"] == cur["start_jd"]


def test_position_is_independent_of_the_placeholder_observer_location(engine):
    # Two different real-world coordinates must not change a geocentric value.
    from vedaksha_parity.config import PLACEHOLDER_LATITUDE, PLACEHOLDER_LONGITUDE

    a = engine._client.natal_chart(
        julian_day=J2000, latitude=PLACEHOLDER_LATITUDE, longitude=PLACEHOLDER_LONGITUDE,
        ayanamsha="IndianOfficial",
    )
    b = engine._client.natal_chart(
        julian_day=J2000, latitude=51.5, longitude=-0.1, ayanamsha="IndianOfficial",
    )
    sun_a = next(p for p in a["planets"] if p["name"] == "Sun")
    sun_b = next(p for p in b["planets"] if p["name"] == "Sun")
    assert sun_a["longitude"] == sun_b["longitude"]
