"""Real Skyfield + DE440 calls, no mock. Skips cleanly if the [skyfield]
extra is not installed, or if the DE440 kernel hasn't been fetched yet
(large download, not bundled — see docs/oracles.md and the module
docstring for the source)."""

import pytest

pytest.importorskip("skyfield")

from vedaksha_parity.oracles.base import OracleUnsupported
from vedaksha_parity.oracles.skyfield_oracle import SkyfieldOracle

J2000 = 2451545.0


@pytest.fixture(scope="module")
def oracle():
    try:
        return SkyfieldOracle()
    except OracleUnsupported as exc:
        pytest.skip(f"DE440 kernel not available: {exc}")


def test_tropical_position_returns_the_expected_fields(oracle):
    sun = oracle.answer({"kind": "tropical_position", "jd_ut": J2000, "body": "Sun"})
    assert set(sun) == {"longitude", "latitude"}
    assert isinstance(sun["longitude"], float)
    assert 0.0 <= sun["longitude"] < 360.0


def test_answer_refuses_sidereal_position(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "position", "jd_ut": J2000, "body": "Sun"})


def test_answer_refuses_ayanamsha(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "ayanamsha", "jd_ut": J2000})


def test_answer_refuses_a_lunar_node(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "tropical_position", "jd_ut": J2000, "body": "MeanNode"})


def test_answer_refuses_outside_the_delta_t_validity_window(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "tropical_position", "jd_ut": 2000000.0, "body": "Sun"})
