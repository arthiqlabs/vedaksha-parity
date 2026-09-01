"""Real, no mock: parses the actual bundled dataset. See docs/birth-data.md."""

from __future__ import annotations

import pytest

from vedaksha_parity.birth_bank import (
    DEFAULT_SOURCE,
    BirthRecord,
    build_cases_from_birth_bank,
    load_birth_bank,
    select_birth_bank,
    split_birth_bank,
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


def test_split_birth_bank_partitions_every_record_exactly_once(records):
    buckets = split_birth_bank(records, ratios={"dev": 0.34, "validation": 0.33, "holdout": 0.33})
    assert sum(len(b) for b in buckets.values()) == len(records)
    all_keys = [r.row_key for bucket in buckets.values() for r in bucket]
    assert len(all_keys) == len(set(all_keys))  # no record in two buckets


def test_split_birth_bank_matches_the_requested_ratios_roughly(records):
    buckets = split_birth_bank(records, ratios={"dev": 0.5, "holdout": 0.5})
    dev_fraction = len(buckets["dev"]) / len(records)
    assert 0.45 < dev_fraction < 0.55  # a hash-based split, not exact, but close


def test_split_birth_bank_is_deterministic_across_calls(records):
    first = split_birth_bank(records, ratios={"a": 0.5, "b": 0.5})
    second = split_birth_bank(records, ratios={"a": 0.5, "b": 0.5})
    assert [r.row_key for r in first["a"]] == [r.row_key for r in second["a"]]


def test_split_birth_bank_depends_on_identity_not_file_order():
    # Shuffling the input list must not move any record between buckets --
    # the partition is a function of row_key, never position.
    records_a = [
        BirthRecord(row_key=f"r{i}", name="x", jd_ut=0.0, location_name="", latitude=0.0, longitude=0.0)
        for i in range(50)
    ]
    records_b = list(reversed(records_a))
    split_a = split_birth_bank(records_a, ratios={"dev": 0.5, "holdout": 0.5})
    split_b = split_birth_bank(records_b, ratios={"dev": 0.5, "holdout": 0.5})
    assert {r.row_key for r in split_a["dev"]} == {r.row_key for r in split_b["dev"]}


def test_split_birth_bank_rejects_ratios_that_do_not_sum_to_one():
    with pytest.raises(ValueError):
        split_birth_bank([], ratios={"dev": 0.5, "holdout": 0.6})


def test_split_birth_bank_a_different_seed_gives_a_different_partition(records):
    default = split_birth_bank(records[:200], ratios={"dev": 0.5, "holdout": 0.5})
    other_seed = split_birth_bank(records[:200], ratios={"dev": 0.5, "holdout": 0.5}, seed=1)
    dev_default = {r.row_key for r in default["dev"]}
    dev_other = {r.row_key for r in other_seed["dev"]}
    assert dev_default != dev_other
