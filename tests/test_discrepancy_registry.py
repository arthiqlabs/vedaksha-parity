"""Structural validation of docs/discrepancy-registry.yaml -- the schema
itself must hold, even though the entries' actual content is a finding,
not something a test asserts on."""

from pathlib import Path

import pytest
import yaml

_PATH = Path("docs/discrepancy-registry.yaml")
_VALID_CLASSIFICATIONS = {
    "agreement",
    "expected_convention",
    "reference_limitation",
    "vedaksha_defect",
    "oracle_defect",
    "unresolved",
}
_REQUIRED_FIELDS = {
    "id", "quantity", "vedaksha_behavior", "oracle_behavior",
    "classification", "primary_source_basis", "date_classified", "evidence",
}


@pytest.fixture(scope="module")
def entries():
    return yaml.safe_load(_PATH.read_text())


def test_registry_is_a_non_empty_list(entries):
    assert isinstance(entries, list)
    assert len(entries) > 0


def test_every_entry_has_all_required_fields(entries):
    for entry in entries:
        missing = _REQUIRED_FIELDS - set(entry)
        assert not missing, f"{entry.get('id', '?')} missing fields: {missing}"


def test_every_id_is_unique(entries):
    ids = [e["id"] for e in entries]
    assert len(ids) == len(set(ids))


def test_every_classification_is_a_known_value(entries):
    for entry in entries:
        assert entry["classification"] in _VALID_CLASSIFICATIONS, (
            f"{entry['id']}: unknown classification {entry['classification']!r}"
        )


def test_expected_convention_entries_require_a_primary_source_basis(entries):
    # The whole point of this classification: it must cite the reasoning
    # that justified it, never stand alone as an assertion.
    for entry in entries:
        if entry["classification"] == "expected_convention":
            assert entry["primary_source_basis"], (
                f"{entry['id']}: expected_convention with no primary_source_basis"
            )


def test_unresolved_entries_have_no_primary_source_basis_claimed():
    # An "unresolved" entry that also carries a confident-sounding basis
    # would be misclassified -- the two are meant to be mutually exclusive.
    entries = yaml.safe_load(_PATH.read_text())
    for entry in entries:
        if entry["classification"] == "unresolved":
            assert entry["primary_source_basis"] is None, (
                f"{entry['id']}: unresolved but has a primary_source_basis -- "
                "should this actually be expected_convention?"
            )
