"""End-to-end: real Vedaksha, real Swiss Ephemeris, one small case list."""

import pytest

pytest.importorskip("swisseph")

from vedaksha_parity.cases import build_cases_t1, build_cases_t1_tropical, build_cases_t2
from vedaksha_parity.engine import Engine
from vedaksha_parity.oracles.swisseph_oracle import SwissephOracle
from vedaksha_parity.runner import run

J2000 = 2451545.0


@pytest.fixture(scope="module")
def engine():
    return Engine()


@pytest.fixture(scope="module")
def oracle():
    return SwissephOracle()


def test_every_case_lands_in_exactly_one_disposition_bucket(engine, oracle):
    cases = build_cases_t1(J2000, J2000, 30.0)
    result = run(cases, engine, oracle)
    assert sum(result["counts"].values()) == len(cases) == len(result["rows"])


def test_sun_at_j2000_is_within_the_review_band_against_swisseph(engine, oracle):
    cases = [{"kind": "position", "jd_ut": J2000, "body": "Sun"}]
    result = run(cases, engine, oracle)
    row = result["rows"][0]
    assert row["disposition"] in {"pass", "review"}, row


def test_tropical_position_runs_end_to_end_against_swisseph(engine, oracle):
    cases = build_cases_t1_tropical(J2000, J2000, 30.0)
    result = run(cases, engine, oracle)
    assert sum(result["counts"].values()) == len(cases) == len(result["rows"])
    row = next(r for r in result["rows"] if r["case"]["body"] == "Sun")
    assert row["disposition"] in {"pass", "review"}, row


def test_ayanamsha_t2_runs_end_to_end(engine, oracle):
    # Asserts a real disposition occurred, not which one — the exact value
    # can shift between Vedaksha releases; that's a docs/tiers.md finding,
    # not something this plumbing test should pin down.
    cases = build_cases_t2(J2000, J2000, 30.0)
    result = run(cases, engine, oracle)
    assert result["counts"]["pass"] + result["counts"]["review"] + result["counts"]["fail"] == 1


def test_an_oracle_crash_is_recorded_not_left_to_crash_the_run(engine):
    # An oracle can raise from inside its own computation (e.g.
    # jyotishganit's sunrise/sunset logic, at some real locations) — this
    # must be recorded, not propagate uncaught and take down the entire run.
    class _CrashingOracle:
        NAME = "Crashing"
        VERSION = "0"

        def settings(self):
            return {}

        def answer(self, case):
            raise TypeError("simulated internal oracle crash")

    cases = [{"kind": "position", "jd_ut": J2000, "body": "Sun"}]
    result = run(cases, engine, _CrashingOracle())
    assert result["counts"]["oracle_error"] == 1
    assert result["rows"][0]["disposition"] == "oracle_error"
