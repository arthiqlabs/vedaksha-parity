"""Real astronomy-engine calls, no mock. Skips cleanly if the
[astronomy-engine] extra is not installed — see docs/oracles.md."""

import pytest

pytest.importorskip("astronomy")

from vedaksha_parity.oracles.astronomy_engine_oracle import AstronomyEngineOracle
from vedaksha_parity.oracles.base import OracleUnsupported

J2000 = 2451545.0


@pytest.fixture(scope="module")
def oracle():
    return AstronomyEngineOracle()


def test_tropical_position_returns_the_expected_fields(oracle):
    sun = oracle.answer({"kind": "tropical_position", "jd_ut": J2000, "body": "Sun"})
    assert set(sun) >= {"longitude", "latitude", "distance"}
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
