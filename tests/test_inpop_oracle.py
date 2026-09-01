"""Real Skyfield + INPOP21a calls, no mock. Skips cleanly if the [inpop]
extra is not installed, or if the INPOP21a kernel hasn't been fetched yet
(large download, not bundled — see docs/oracles.md and the module
docstring for the source)."""

import pytest

pytest.importorskip("skyfield")

from vedaksha_parity.oracles.base import OracleUnsupported
from vedaksha_parity.oracles.inpop_oracle import InpopOracle

J2000 = 2451545.0


@pytest.fixture(scope="module")
def oracle():
    try:
        return InpopOracle()
    except OracleUnsupported as exc:
        pytest.skip(f"INPOP21a kernel not available: {exc}")


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


def test_answer_refuses_outside_the_kernel_span(oracle):
    with pytest.raises(OracleUnsupported):
        oracle.answer({"kind": "tropical_position", "jd_ut": 1000000.0, "body": "Sun"})
