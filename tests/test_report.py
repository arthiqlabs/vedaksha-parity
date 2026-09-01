"""_render_delta_stats: raw statistical distributions, independent of any
disposition threshold — see review P1 item 3."""

from vedaksha_parity.report import _numeric_stats, _percentile, _render_delta_stats


def test_percentile_of_a_single_value_is_that_value():
    assert _percentile([5.0], 90) == 5.0


def test_percentile_matches_known_values_on_a_sorted_list():
    values = [0.0, 10.0, 20.0, 30.0, 40.0]
    assert _percentile(values, 0) == 0.0
    assert _percentile(values, 50) == 20.0
    assert _percentile(values, 100) == 40.0


def test_numeric_stats_reports_all_fields():
    stats = _numeric_stats([1.0, 2.0, 3.0, 4.0, 5.0])
    assert stats["n"] == 5
    assert stats["mean"] == 3.0
    assert stats["median"] == 3.0
    assert stats["max"] == 5.0
    assert stats["rms"] > stats["mean"]  # RMS >= mean for any non-constant series


def test_numeric_stats_uses_absolute_value():
    # A signed delta series (e.g. distance_delta_au can be negative) must
    # not let positive and negative deltas cancel out in the reported
    # magnitude statistics.
    stats = _numeric_stats([-10.0, 10.0])
    assert stats["mean"] == 10.0
    assert stats["max"] == 10.0


def test_render_delta_stats_gathers_every_delta_field_across_rows():
    rows = [
        {"comparison": {"longitude_delta_arcsec": 1.0, "latitude_delta_arcsec": 2.0, "disposition": "pass"}},
        {"comparison": {"longitude_delta_arcsec": 3.0, "disposition": "review"}},
    ]
    table = _render_delta_stats(rows)
    assert "longitude_delta_arcsec" in table
    assert "latitude_delta_arcsec" in table
    assert "| longitude_delta_arcsec | 2 |" in table  # n=2 across both rows
    assert "| latitude_delta_arcsec | 1 |" in table  # n=1, only the first row has it


def test_render_delta_stats_ignores_non_delta_and_boolean_fields():
    rows = [{"comparison": {"lord_sequence_match": True, "compared": 8, "disposition": "pass"}}]
    assert _render_delta_stats(rows) == ""


def test_render_delta_stats_skips_rows_with_no_comparison():
    # oracle_unsupported/oracle_error/engine_error rows carry no comparison.
    rows = [{"disposition": "oracle_unsupported", "reason": "x"}]
    assert _render_delta_stats(rows) == ""
