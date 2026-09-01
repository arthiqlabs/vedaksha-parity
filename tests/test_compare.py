import pytest

from vedaksha_parity.compare import (
    circular_diff_deg,
    classify,
    compare_ashtakavarga,
    compare_ayanamsha,
    compare_bhavas,
    compare_combustion,
    compare_dasha,
    compare_drishti,
    compare_houses,
    compare_karakas,
    compare_panchanga,
    compare_position,
    compare_sign_dasha,
    compare_vargas,
)


def test_circular_diff_handles_the_360_0_wraparound():
    # 0.5 is 1 degree ahead of 359.5 through 0, not 359 the other way.
    assert circular_diff_deg(0.5, 359.5) == pytest.approx(1.0)


def test_circular_diff_is_signed_and_symmetric():
    assert circular_diff_deg(10.0, 5.0) == 5.0
    assert circular_diff_deg(5.0, 10.0) == -5.0


def test_classify_bands():
    band = {"pass": 5.0, "review": 60.0}
    assert classify(0.0, band) == "pass"
    assert classify(5.0, band) == "pass"
    assert classify(5.001, band) == "review"
    assert classify(60.0, band) == "review"
    assert classify(60.001, band) == "fail"


def test_compare_position_reports_arcsec_deltas_and_a_disposition():
    engine = {"longitude": 100.0, "latitude": 1.0}
    oracle = {"longitude": 100.001, "latitude": 1.0}
    result = compare_position(engine, oracle)
    assert result["longitude_delta_arcsec"] == pytest.approx(-3.6)
    assert result["longitude_disposition"] == "pass"  # 3.6" is inside the 5" pass band


def test_compare_position_handles_an_oracle_with_no_latitude():
    # Absence must be skipped, never fabricated as 0.0.
    engine = {"longitude": 100.0, "latitude": 1.0}
    oracle = {"longitude": 100.001}
    result = compare_position(engine, oracle)
    assert "latitude_delta_arcsec" not in result
    assert "latitude_disposition" not in result
    assert result["disposition"] == result["longitude_disposition"]


def test_compare_position_overall_disposition_is_the_worst_component():
    # Longitude alone passes (3.6"), but latitude is off by 2 degrees --
    # the overall disposition must reflect that, not just longitude.
    # This is the exact "vacuous position pass" gap flagged in review.
    engine = {"longitude": 100.0, "latitude": 1.0}
    oracle = {"longitude": 100.001, "latitude": 3.0}
    result = compare_position(engine, oracle)
    assert result["longitude_disposition"] == "pass"
    assert result["latitude_disposition"] == "fail"
    assert result["disposition"] == "fail"


def test_compare_position_reports_distance_and_speed_deltas_unclassified():
    # No calibrated tolerance band exists for either yet -- reported as
    # raw deltas only, never folded into disposition.
    engine = {"longitude": 100.0, "latitude": 1.0, "distance": 1.5, "speed": 0.9}
    oracle = {"longitude": 100.001, "latitude": 1.0, "distance": 1.6, "speed": 1.1}
    result = compare_position(engine, oracle)
    assert result["distance_delta_au"] == pytest.approx(-0.1)
    assert result["speed_delta_deg_per_day"] == pytest.approx(-0.2)
    assert "distance_disposition" not in result
    assert "speed_disposition" not in result
    assert result["longitude_disposition"] == "pass"


def test_compare_ayanamsha_reports_arcsec_delta():
    result = compare_ayanamsha({"value": 23.857092}, {"value": 23.857091})
    assert result["delta_arcsec"] == pytest.approx(0.0036, abs=1e-3)


_KARAKAS_ATMAKARAKA_MOON = [
    {"karaka": "Atmakaraka", "planet": "Moon", "degrees_in_sign": 19.5},
    {"karaka": "Amatyakaraka", "planet": "Saturn", "degrees_in_sign": 16.5},
]


def test_compare_karakas_passes_on_full_agreement():
    result = compare_karakas(_KARAKAS_ATMAKARAKA_MOON, _KARAKAS_ATMAKARAKA_MOON)
    assert result["mismatched_karakas"] == []
    assert result["disposition"] == "pass"


def test_compare_karakas_below_the_coverage_floor_is_comparison_invalid():
    # An oracle that answers nothing must not read as "0 mismatches, pass".
    result = compare_karakas(_KARAKAS_ATMAKARAKA_MOON, [])
    assert result["disposition"] == "comparison_invalid"


def test_compare_karakas_reviews_a_single_rank_swap():
    # A swap changes two titles at once — this must land in review, not fail.
    oracle = [
        {"karaka": "Atmakaraka", "planet": "Saturn", "degrees_in_sign": 16.5},
        {"karaka": "Amatyakaraka", "planet": "Moon", "degrees_in_sign": 19.5},
    ]
    result = compare_karakas(_KARAKAS_ATMAKARAKA_MOON, oracle)
    assert result["mismatched_karakas"] == ["Amatyakaraka", "Atmakaraka"]
    assert result["disposition"] == "review"


def test_compare_karakas_fails_a_three_way_reorder():
    oracle = [
        {"karaka": "Atmakaraka", "planet": "Saturn", "degrees_in_sign": 16.5},
        {"karaka": "Amatyakaraka", "planet": "Jupiter", "degrees_in_sign": 10.0},
        {"karaka": "Bhratrikaraka", "planet": "Moon", "degrees_in_sign": 19.5},
    ]
    engine = [
        {"karaka": "Atmakaraka", "planet": "Moon", "degrees_in_sign": 19.5},
        {"karaka": "Amatyakaraka", "planet": "Saturn", "degrees_in_sign": 16.5},
        {"karaka": "Bhratrikaraka", "planet": "Jupiter", "degrees_in_sign": 10.0},
    ]
    result = compare_karakas(engine, oracle)
    assert len(result["mismatched_karakas"]) == 3
    assert result["disposition"] == "fail"


def test_compare_combustion_matches_state():
    engine = {"planet": "Mercury", "state": "Combust", "degrees_from_sun": 8.5}
    oracle = {"planet": "Mercury", "state": "Combust", "degrees_from_sun": 8.4}
    assert compare_combustion(engine, oracle)["disposition"] == "pass"


def test_compare_combustion_fails_a_state_mismatch():
    engine = {"planet": "Mercury", "state": "Combust", "degrees_from_sun": 8.5}
    oracle = {"planet": "Mercury", "state": "None", "degrees_from_sun": 8.5}
    assert compare_combustion(engine, oracle)["disposition"] == "fail"


_DRISHTI_ONE = [{"aspecting_planet": "Sun", "aspecting_sign": 8, "aspected_sign": 2, "houses_away": 7, "strength": "Full"}]


def test_compare_drishti_passes_on_identical_sets():
    result = compare_drishti(_DRISHTI_ONE, _DRISHTI_ONE)
    assert result["disposition"] == "pass"


def test_compare_drishti_both_empty_is_comparison_invalid_not_pass():
    # Two empty sets are mathematically identical -- but Vedaksha's own
    # drishti output is never legitimately empty for a real chart, so
    # this is a broken-adapter signature, not agreement.
    result = compare_drishti([], [])
    assert result["disposition"] == "comparison_invalid"


def test_compare_drishti_reports_missing_and_extra():
    oracle = []
    result = compare_drishti(_DRISHTI_ONE, oracle)
    assert len(result["missing_in_oracle"]) == 1
    assert result["extra_in_oracle"] == []
    assert result["disposition"] == "review"  # one mismatch


def test_compare_drishti_ignores_strength_when_the_oracle_has_none():
    # A binary source has no strength gradation — comparing it against
    # graduated strength would manufacture a false mismatch.
    engine = [{"aspecting_planet": "Sun", "aspecting_sign": 8, "aspected_sign": 2, "houses_away": 7, "strength": "Full"}]
    oracle = [{"aspecting_planet": "Sun", "aspected_sign": 2}]  # no strength field at all
    result = compare_drishti(engine, oracle)
    assert result["compared_strength"] is False
    assert result["disposition"] == "pass"


_VIMSHOTTARI_LORDS = ["Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun", "Moon", "Mars"]


def _dasha_periods(start_offsets_days, lords=_VIMSHOTTARI_LORDS):
    periods = []
    jd = 2451545.0
    for lord, offset in zip(lords, start_offsets_days, strict=True):
        periods.append({"lord": lord, "start_jd": jd + offset, "end_jd": jd + offset + 100.0})
    return {"maha_dashas": periods}


_NINE_OFFSETS = [float(i * 100) for i in range(9)]


def test_compare_dasha_passes_on_matching_boundaries():
    periods = _dasha_periods(_NINE_OFFSETS)
    assert compare_dasha(periods, periods)["disposition"] == "pass"


def test_compare_dasha_fails_on_a_different_lord_sequence():
    engine = _dasha_periods(_NINE_OFFSETS)
    reversed_lords = list(reversed(_VIMSHOTTARI_LORDS))
    oracle = _dasha_periods(_NINE_OFFSETS, lords=reversed_lords)
    result = compare_dasha(engine, oracle)
    assert result["lord_sequence_match"] is False
    assert result["disposition"] == "fail"


def test_compare_dasha_reviews_a_small_boundary_drift():
    engine = _dasha_periods(_NINE_OFFSETS)
    oracle = _dasha_periods([o + 0.5 for o in _NINE_OFFSETS])  # half a day off, same lords
    result = compare_dasha(engine, oracle)
    assert result["lord_sequence_match"] is True
    assert result["disposition"] == "review"


def test_compare_dasha_below_the_coverage_floor_is_comparison_invalid():
    # A short (or empty) lord list must not vacuously equal another short
    # list and read as agreement -- a full Vimshottari cycle is always 9.
    engine = _dasha_periods(_NINE_OFFSETS)
    oracle = {"maha_dashas": []}
    result = compare_dasha(engine, oracle)
    assert result["disposition"] == "comparison_invalid"


def _houses(asc=100.0, mc=10.0, cusp_shift=0.0):
    return {"asc": asc + cusp_shift, "mc": mc + cusp_shift, "cusps": [(i * 30.0 + cusp_shift) % 360.0 for i in range(12)]}


def test_compare_houses_passes_on_identical_charts():
    houses = _houses()
    result = compare_houses(houses, houses)
    assert result["disposition"] == "pass"
    assert result["worst_delta_arcsec"] == pytest.approx(0.0)


def test_compare_houses_flags_the_single_worst_point():
    engine = _houses()
    oracle = dict(engine, cusps=list(engine["cusps"]))
    oracle["cusps"][5] = (oracle["cusps"][5] + 0.5) % 360.0  # one cusp off by 0.5 deg = 1800"
    result = compare_houses(engine, oracle)
    assert result["worst_point"] == "cusp_6"
    assert result["disposition"] == "fail"


def _varga_signs(with_nodes=True):
    signs = {"Lagna": 10, "Sun": 4, "Moon": 11, "Mercury": 2, "Venus": 7,
             "Mars": 0, "Jupiter": 9, "Saturn": 5}
    if with_nodes:
        signs.update({"MeanNode": 6, "TrueNode": 6})
    return signs


def test_compare_vargas_passes_on_full_agreement():
    signs = _varga_signs()
    result = compare_vargas(signs, signs)
    assert result["disposition"] == "pass"


def test_compare_vargas_only_compares_bodies_present_on_both_sides():
    # Lagna + all 7 classical grahas (the coverage floor) agree; only the
    # nodes are missing from the oracle side -- a genuine, legitimate
    # partial-coverage case (like jyotishganit lacking node vargas), not
    # a broken adapter, so this must still pass, not comparison_invalid.
    engine = _varga_signs(with_nodes=True)
    oracle = _varga_signs(with_nodes=False)
    result = compare_vargas(engine, oracle)
    assert result["compared"] == 8
    assert result["disposition"] == "pass"


def test_compare_vargas_below_the_coverage_floor_is_comparison_invalid():
    # An oracle answering almost nothing (well under Lagna + 7 grahas)
    # must not read as agreement just because zero of the few compared
    # bodies happened to mismatch.
    engine = _varga_signs(with_nodes=True)
    oracle = {"Lagna": 10, "Sun": 4}
    result = compare_vargas(engine, oracle)
    assert result["compared"] == 2
    assert result["disposition"] == "comparison_invalid"


def test_compare_vargas_fails_on_a_sign_mismatch():
    engine = _varga_signs(with_nodes=False)
    oracle = dict(engine, Sun=5)
    result = compare_vargas(engine, oracle)
    assert result["mismatched_bodies"] == ["Sun"]
    assert result["disposition"] == "review"  # single mismatch


def _bhava(n, sign, kendra=False, trikona=False, dusthana=False, upachaya=False):
    return {"bhava": n, "sign": sign, "is_kendra": kendra, "is_trikona": trikona,
            "is_dusthana": dusthana, "is_upachaya": upachaya}


def test_compare_bhavas_passes_on_identical_charts():
    houses = [_bhava(1, 0, kendra=True, trikona=True)]
    assert compare_bhavas(houses, houses)["disposition"] == "pass"


def test_compare_bhavas_below_the_coverage_floor_is_comparison_invalid():
    engine = [_bhava(1, 0), _bhava(2, 1)]
    result = compare_bhavas(engine, [])
    assert result["disposition"] == "comparison_invalid"


def test_compare_bhavas_flags_a_single_field_mismatch():
    engine = [_bhava(10, 6, upachaya=True)]
    oracle = [_bhava(10, 6, upachaya=False)]
    result = compare_bhavas(engine, oracle)
    assert result["mismatched_fields"] == ["bhava_10.is_upachaya"]
    assert result["disposition"] == "review"


def test_compare_ashtakavarga_passes_on_identical_counts():
    counts = [25] * 12
    assert compare_ashtakavarga(counts, counts)["disposition"] == "pass"


def test_compare_ashtakavarga_fails_on_multiple_sign_mismatches():
    engine = [25] * 12
    oracle = list(engine)
    oracle[1] += 1
    oracle[2] -= 1
    result = compare_ashtakavarga(engine, oracle)
    assert result["mismatched_signs"] == [1, 2]
    assert result["disposition"] == "fail"


_PANCHANGA_ENGINE = {
    "tithi": {"name": "Krishna Ekadashi"}, "nakshatra": {"name": "Swati"},
    "yoga": {"name": "Dhriti"}, "karana": {"name": "Bava"}, "vara": {"weekday": "Saturday"},
}
_PANCHANGA_ORACLE = {
    "tithi": "Krishna Ekadashi", "nakshatra": "Swati",
    "yoga": "Dhriti", "karana": "Bava", "vara": "Saturday",
}


def test_compare_panchanga_passes_on_full_agreement():
    result = compare_panchanga(_PANCHANGA_ENGINE, _PANCHANGA_ORACLE)
    assert result["disposition"] == "pass"


def test_compare_panchanga_flags_a_single_limb_mismatch():
    oracle = dict(_PANCHANGA_ORACLE, tithi="Shukla Panchami")
    result = compare_panchanga(_PANCHANGA_ENGINE, oracle)
    assert result["mismatched_limbs"] == ["tithi"]
    assert result["disposition"] == "review"


def _sign_dasha_periods(signs, durations=None):
    jd = 2451545.0
    durations = durations or [1.0] * len(signs)
    return [
        {
            "sign_index": s, "duration_years": d,
            "start_jd": jd + i * 100.0, "end_jd": jd + (i + 1) * 100.0,
        }
        for i, (s, d) in enumerate(zip(signs, durations, strict=True))
    ]


_TWELVE_SIGNS = list(range(12))


def test_compare_sign_dasha_passes_on_matching_signs_and_boundaries():
    periods = _sign_dasha_periods(_TWELVE_SIGNS)
    assert compare_sign_dasha(periods, periods)["disposition"] == "pass"


def test_compare_sign_dasha_fails_on_a_different_sign_sequence():
    engine = _sign_dasha_periods(_TWELVE_SIGNS)
    oracle = _sign_dasha_periods(list(reversed(_TWELVE_SIGNS)))
    result = compare_sign_dasha(engine, oracle)
    assert result["sign_sequence_match"] is False
    assert result["disposition"] == "fail"


def test_compare_sign_dasha_below_the_coverage_floor_is_comparison_invalid():
    engine = _sign_dasha_periods(_TWELVE_SIGNS)
    result = compare_sign_dasha(engine, [])
    assert result["disposition"] == "comparison_invalid"


def test_compare_sign_dasha_reports_which_signs_duration_disagrees():
    # max_boundary_delta_days alone can't tell "tiny drift" from "a few
    # signs disagree" — mismatched_durations makes that visible.
    durations_e = [9.0, 4.0, 3.0] + [1.0] * 9
    durations_o = [8.0, 4.0, 2.0] + [1.0] * 9
    engine = _sign_dasha_periods(_TWELVE_SIGNS, durations=durations_e)
    oracle = _sign_dasha_periods(_TWELVE_SIGNS, durations=durations_o)
    result = compare_sign_dasha(engine, oracle)
    assert result["sign_sequence_match"] is True
    assert result["mismatched_durations"] == [0, 2]
