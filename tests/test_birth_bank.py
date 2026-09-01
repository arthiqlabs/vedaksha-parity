"""Real, no mock: parses the actual bundled dataset. See docs/birth-data.md."""

from __future__ import annotations

import pytest

from vedaksha_parity.birth_bank import (
    DEFAULT_SOURCE,
    build_cases_from_birth_bank,
    load_birth_bank,
    select_birth_bank,
)

pytestmark = pytest.mark.skipif(
    not DEFAULT_SOURCE.exists(), reason="bundled birth-data CSV not present"
)


@pytest.fixture(scope="module")
def records():
    return load_birth_bank()


def test_load_birth_bank_parses_every_row_except_known_placeholder_entries(records):
    # 15807 total rows minus 17 "Empty" placeholder entries — see
    # docs/birth-data.md's "Data quality" section.
    assert len(records) == 15807 - 17
    assert all(r.name != "Empty" for r in records)
    first = records[0]
    assert first.row_key
    assert first.name
    assert 0.0 < first.jd_ut
    assert -90.0 <= first.latitude <= 90.0
    assert -180.0 <= first.longitude <= 180.0


def test_select_with_no_count_returns_every_record_unchanged(records):
    selected, provenance = select_birth_bank(records)
    assert selected == records
    assert provenance == {"source_size": len(records), "count": None, "seed": None}


def test_select_with_a_seed_is_deterministic(records):
    a, prov_a = select_birth_bank(records, count=10, seed=42)
    b, prov_b = select_birth_bank(records, count=10, seed=42)
    assert a == b
    assert prov_a["seed"] == 42 == prov_b["seed"]


def test_select_without_a_seed_still_records_the_seed_actually_used(records):
    _, provenance = select_birth_bank(records, count=10)
    assert provenance["seed"] is not None


def test_select_rejects_a_count_larger_than_the_source():
    with pytest.raises(ValueError):
        select_birth_bank([], count=1)


def test_build_cases_from_birth_bank_t1_is_one_case_per_body_per_record(records):
    sample, _ = select_birth_bank(records, count=3, seed=1)
    cases = build_cases_from_birth_bank(sample, "t1")
    assert len(cases) == 3 * 9
    assert all(c["kind"] == "position" for c in cases)


def test_build_cases_from_birth_bank_t2_is_one_case_per_record(records):
    sample, _ = select_birth_bank(records, count=3, seed=1)
    cases = build_cases_from_birth_bank(sample, "t2")
    assert len(cases) == 3
    assert all(c["kind"] == "ayanamsha" for c in cases)


def test_build_cases_from_birth_bank_rejects_an_unknown_tier(records):
    with pytest.raises(ValueError):
        build_cases_from_birth_bank(records[:1], "t99")
