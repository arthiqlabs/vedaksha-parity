"""Comparison + classification. A case's disposition is always exactly one
of: pass, review, fail, comparison_invalid, oracle_unsupported,
oracle_error, engine_error. comparison_invalid means the coverage floor a
comparator requires (e.g. all 8 karakas, all 12 bhavas) wasn't met -- a
distinct thing from disagreement, never silently counted as pass. See
runner.py's disposition accounting."""

from __future__ import annotations

from typing import Any

from vedaksha_parity.config import (
    CATEGORICAL_REVIEW_MISMATCH_MAX,
    KARAKA_REVIEW_MISMATCH_MAX,
    TOLERANCES,
)


def circular_diff_deg(a: float, b: float) -> float:
    """Shortest signed angular distance a-b on a 360-degree circle, in [-180, 180]."""
    d = (a - b) % 360.0
    if d > 180.0:
        d -= 360.0
    return d


def classify(delta_arcsec: float, band: dict[str, float]) -> str:
    delta = abs(delta_arcsec)
    if delta <= band["pass"]:
        return "pass"
    if delta <= band["review"]:
        return "review"
    return "fail"


_DISPOSITION_SEVERITY = {"pass": 0, "review": 1, "fail": 2}


def _worst_disposition(dispositions: list[str]) -> str:
    return max(dispositions, key=lambda d: _DISPOSITION_SEVERITY[d])


def compare_position(engine_answer: dict[str, float], oracle_answer: dict[str, float]) -> dict[str, Any]:
    """"Position" is not "longitude" — a case that agrees on longitude but
    disagrees badly on latitude must not be counted pass. `disposition`
    is the worst of every sub-metric this comparator can actually
    classify (currently longitude, and latitude when the oracle answers
    it); it is the field callers should use as the case's overall
    disposition, not `longitude_disposition` alone.

    Distance and speed are reported as raw deltas only, never classified
    — there is no externally-calibrated tolerance band for either yet
    (see TOLERANCES' own "provisional" note), and inventing one here
    would be exactly the researcher-degrees-of-freedom problem this
    project's own tolerance policy already flags. They do not affect
    `disposition` until a real band exists."""
    lon_delta_deg = circular_diff_deg(engine_answer["longitude"], oracle_answer["longitude"])
    lon_delta_arcsec = lon_delta_deg * 3600.0
    longitude_disposition = classify(lon_delta_arcsec, TOLERANCES["position_longitude_arcsec"])
    result: dict[str, Any] = {
        "longitude_delta_arcsec": lon_delta_arcsec,
        "longitude_disposition": longitude_disposition,
    }
    dispositions = [longitude_disposition]
    # Some oracles answer only longitude — absence is a disclosed gap,
    # never fabricated as 0.0. Latitude fields are simply omitted.
    if "latitude" in oracle_answer:
        lat_delta_arcsec = (engine_answer["latitude"] - oracle_answer["latitude"]) * 3600.0
        latitude_disposition = classify(lat_delta_arcsec, TOLERANCES["position_latitude_arcsec"])
        result["latitude_delta_arcsec"] = lat_delta_arcsec
        result["latitude_disposition"] = latitude_disposition
        dispositions.append(latitude_disposition)
    if "distance" in oracle_answer:
        result["distance_delta_au"] = engine_answer["distance"] - oracle_answer["distance"]
    if "speed" in oracle_answer:
        result["speed_delta_deg_per_day"] = engine_answer["speed"] - oracle_answer["speed"]
    result["disposition"] = _worst_disposition(dispositions)
    return result


def compare_ayanamsha(engine_answer: dict[str, float], oracle_answer: dict[str, float]) -> dict[str, Any]:
    delta_deg = engine_answer["value"] - oracle_answer["value"]
    delta_arcsec = delta_deg * 3600.0
    return {
        "delta_arcsec": delta_arcsec,
        "disposition": classify(delta_arcsec, TOLERANCES["ayanamsha_arcsec"]),
    }


def _categorical_disposition(
    mismatch_count: int,
    *,
    max_review: int = CATEGORICAL_REVIEW_MISMATCH_MAX,
    compared_count: int | None = None,
    min_required: int | None = None,
) -> str:
    # Fail-closed coverage floor, checked before mismatch counting: a
    # comparator built on set intersection (karakas/vargas/bhavas) would
    # otherwise report a spurious "pass" if an oracle silently answered
    # nothing at all -- common = [], mismatches = [], 0 mismatches reads
    # as agreement. comparison_invalid means the comparison itself never
    # happened at the expected scale, not that the two sides agreed.
    if min_required is not None and (compared_count is None or compared_count < min_required):
        return "comparison_invalid"
    if mismatch_count == 0:
        return "pass"
    if mismatch_count <= max_review:
        return "review"
    return "fail"


def compare_karakas(
    engine_answer: list[dict[str, Any]], oracle_answer: list[dict[str, Any]]
) -> dict[str, Any]:
    """A ranking, not a value — does the same planet hold each karaka rank?
    A single swap is the case worth reviewing (plausibly two planets tied
    within a fraction of a degree of each other), not a numeric threshold.
    A swap always changes two karaka titles at once, so the review ceiling
    here is 2 mismatches, not the shared 1-mismatch default — see
    config.KARAKA_REVIEW_MISMATCH_MAX."""
    engine_map = {k["karaka"]: k["planet"] for k in engine_answer}
    oracle_map = {k["karaka"]: k["planet"] for k in oracle_answer}
    common = sorted(set(engine_map) & set(oracle_map))
    mismatched = [k for k in common if engine_map[k] != oracle_map[k]]
    return {
        "compared": len(common),
        "mismatched_karakas": mismatched,
        "disposition": _categorical_disposition(
            len(mismatched),
            max_review=KARAKA_REVIEW_MISMATCH_MAX,
            compared_count=len(common),
            min_required=len(engine_map),
        ),
    }


def compare_combustion(engine_answer: dict[str, Any], oracle_answer: dict[str, Any]) -> dict[str, Any]:
    """Per-body, matching cases.py's one-case-per-body shape — unlike
    karakas/drishti, a body's combustion state is independently meaningful."""
    match = engine_answer["state"] == oracle_answer["state"]
    return {
        "engine_state": engine_answer["state"],
        "oracle_state": oracle_answer["state"],
        "disposition": "pass" if match else "fail",
    }


def _drishti_key(entry: dict[str, Any], *, with_strength: bool) -> tuple[str, ...]:
    if with_strength:
        return (entry["aspecting_planet"], entry["aspected_sign"], entry["strength"])
    return (entry["aspecting_planet"], entry["aspected_sign"])


def compare_drishti(
    engine_answer: list[dict[str, Any]], oracle_answer: list[dict[str, Any]]
) -> dict[str, Any]:
    # Not every source grades aspect strength — a binary source's aspects
    # correspond to the graduated side's "Full" entries only, so when one
    # side has no strength concept, both are reduced to that Full subset
    # before comparing presence (else the binary side's absence looks like
    # a false "missing").
    engine_has_strength = all("strength" in e for e in engine_answer)
    oracle_has_strength = all("strength" in e for e in oracle_answer)
    with_strength = engine_has_strength and oracle_has_strength

    def _reduce(answers: list[dict[str, Any]], has_strength: bool) -> list[dict[str, Any]]:
        if with_strength or not has_strength:
            return answers
        return [a for a in answers if a["strength"] == "Full"]

    engine_reduced = _reduce(engine_answer, engine_has_strength)
    oracle_reduced = _reduce(oracle_answer, oracle_has_strength)
    engine_set = {_drishti_key(e, with_strength=with_strength) for e in engine_reduced}
    oracle_set = {_drishti_key(e, with_strength=with_strength) for e in oracle_reduced}
    missing = sorted(map(str, engine_set - oracle_set))
    extra = sorted(map(str, oracle_set - engine_set))
    return {
        "compared_strength": with_strength,
        "missing_in_oracle": missing,
        "extra_in_oracle": extra,
        # Two empty answer sets are mathematically identical, but that's a
        # broken-adapter signature, not agreement — Vedaksha's own drishti
        # output is never legitimately empty for a real chart, so require
        # the engine side to have actually answered something.
        "disposition": _categorical_disposition(
            len(missing) + len(extra), compared_count=len(engine_set), min_required=1
        ),
    }


def compare_vargas(engine_answer: dict[str, int], oracle_answer: dict[str, int]) -> dict[str, Any]:
    """Categorical, per body: does the varga sign match? {body: 0-indexed
    sign} on both sides — only bodies present on BOTH sides are compared,
    same discipline as karakas/combustion for a source that can't answer
    every body (e.g. no node) — a genuine, legitimate partial-coverage
    case, unlike an oracle silently answering nothing at all. The
    coverage floor is Lagna + the 7 classical grahas (8), never the
    nodes, since node coverage varies legitimately by oracle."""
    common = sorted(set(engine_answer) & set(oracle_answer))
    mismatched = [b for b in common if engine_answer[b] != oracle_answer[b]]
    return {
        "compared": len(common),
        "mismatched_bodies": mismatched,
        "disposition": _categorical_disposition(
            len(mismatched), compared_count=len(common), min_required=min(8, len(engine_answer))
        ),
    }


def compare_bhavas(
    engine_answer: list[dict[str, Any]], oracle_answer: list[dict[str, Any]]
) -> dict[str, Any]:
    """Per bhava (1-12): sign plus the four kendra/trikona/dusthana/upachaya
    classifications, matched by bhava number."""
    engine_map = {b["bhava"]: b for b in engine_answer}
    oracle_map = {b["bhava"]: b for b in oracle_answer}
    common = sorted(set(engine_map) & set(oracle_map))
    fields = ("sign", "is_kendra", "is_trikona", "is_dusthana", "is_upachaya")
    mismatched = [
        f"bhava_{n}.{field}"
        for n in common
        for field in fields
        if engine_map[n].get(field) != oracle_map[n].get(field)
    ]
    return {
        "compared": len(common),
        "mismatched_fields": mismatched,
        "disposition": _categorical_disposition(
            len(mismatched), compared_count=len(common), min_required=len(engine_map)
        ),
    }


def compare_ashtakavarga(engine_answer: list[int], oracle_answer: list[int]) -> dict[str, Any]:
    """Sarvashtakavarga bindu count per sign (12 values, index = sign) —
    a mechanical BPHS computation with no convention room, so any
    disagreement is a real one, not a classical-tradition choice."""
    mismatched = [
        i for i, (e, o) in enumerate(zip(engine_answer, oracle_answer, strict=True)) if e != o
    ]
    return {
        "mismatched_signs": mismatched,
        # Sarvashtakavarga is exactly 12 sign counts, always -- zip(strict)
        # would already raise on a length mismatch, but two empty lists
        # would otherwise pass vacuously.
        "disposition": _categorical_disposition(
            len(mismatched), compared_count=len(engine_answer), min_required=12
        ),
    }


def compare_panchanga(engine_answer: dict[str, Any], oracle_answer: dict[str, Any]) -> dict[str, Any]:
    """Five limbs, compared as plain names — tithi/nakshatra/yoga/karana
    name and the weekday name. Sub-fields some sources don't carry
    (pada, kalam windows, degrees remaining) are not compared here."""
    pairs = [
        ("tithi", engine_answer["tithi"]["name"], oracle_answer["tithi"]),
        ("nakshatra", engine_answer["nakshatra"]["name"], oracle_answer["nakshatra"]),
        ("yoga", engine_answer["yoga"]["name"], oracle_answer["yoga"]),
        ("karana", engine_answer["karana"]["name"], oracle_answer["karana"]),
        ("vara", engine_answer["vara"]["weekday"], oracle_answer["vara"]),
    ]
    mismatched = [name for name, e, o in pairs if e != o]
    return {
        "mismatched_limbs": mismatched,
        "disposition": _categorical_disposition(len(mismatched)),
    }


def compare_houses(engine_answer: dict[str, Any], oracle_answer: dict[str, Any]) -> dict[str, Any]:
    """Asc, MC, and all 12 cusps compared as circular longitude deltas,
    same units (arcsec) and tolerance band as position — classified by the
    worst of the 14, since a single badly-off cusp matters regardless of
    how well the other 13 agree."""
    points = [("asc", engine_answer["asc"], oracle_answer["asc"]), ("mc", engine_answer["mc"], oracle_answer["mc"])]
    points += [
        (f"cusp_{i + 1}", e, o)
        for i, (e, o) in enumerate(zip(engine_answer["cusps"], oracle_answer["cusps"], strict=True))
    ]
    deltas_arcsec = {name: circular_diff_deg(e, o) * 3600.0 for name, e, o in points}
    worst_name = max(deltas_arcsec, key=lambda k: abs(deltas_arcsec[k]))
    worst_delta = deltas_arcsec[worst_name]
    return {
        "deltas_arcsec": deltas_arcsec,
        "worst_point": worst_name,
        "worst_delta_arcsec": worst_delta,
        "disposition": classify(worst_delta, TOLERANCES["position_longitude_arcsec"]),
    }


def compare_dasha(engine_answer: dict[str, Any], oracle_answer: dict[str, Any]) -> dict[str, Any]:
    """Dates, not angles — tolerance in days, and the lord sequence itself
    must match before a date delta means anything.

    `compute_dasha` anchors period 0's start_jd to the query instant (the
    remaining-balance view), not the true historical start — a convention
    difference, not a divergence. Only period 0's end_jd and every other
    period's full start/end are compared."""
    engine_periods = engine_answer["maha_dashas"]
    oracle_periods = oracle_answer["maha_dashas"]
    engine_lords = [p["lord"] for p in engine_periods]
    oracle_lords = [p["lord"] for p in oracle_periods]
    # A full Vimshottari cycle is always exactly 9 lords -- an empty (or
    # short) list on either side must not reach the equality check below,
    # where two empty lists would compare equal and read as agreement.
    if len(engine_lords) < 9 or len(oracle_lords) < 9:
        return {
            "lord_sequence_match": False,
            "engine_lords": engine_lords,
            "oracle_lords": oracle_lords,
            "disposition": "comparison_invalid",
        }
    if engine_lords != oracle_lords:
        return {
            "lord_sequence_match": False,
            "engine_lords": engine_lords,
            "oracle_lords": oracle_lords,
            "disposition": "fail",
        }
    deltas_days = []
    for i, (e, o) in enumerate(zip(engine_periods, oracle_periods, strict=True)):
        if i > 0:
            deltas_days.append(abs(e["start_jd"] - o["start_jd"]))
        deltas_days.append(abs(e["end_jd"] - o["end_jd"]))
    max_delta = max(deltas_days) if deltas_days else 0.0
    return {
        "lord_sequence_match": True,
        "max_boundary_delta_days": max_delta,
        "disposition": classify(max_delta, TOLERANCES["dasha_start_delta_days"]),
    }


def compare_sign_dasha(
    engine_answer: list[dict[str, Any]], oracle_answer: list[dict[str, Any]]
) -> dict[str, Any]:
    """Chara/Narayana dasha — a flat list, not the {maha_dashas: [...]}
    wrapper Vimshottari-family systems use, and cycling through the 12
    SIGNS rather than graha lords. Chara's own period 0 also anchors
    start_jd to the query instant, same convention as Vimshottari's — see
    compare_dasha's docstring for why that's skipped rather than
    compared."""
    engine_signs = [p["sign_index"] for p in engine_answer]
    oracle_signs = [p["sign_index"] for p in oracle_answer]
    # Always exactly 12 signs -- same vacuous-empty-list risk as
    # compare_dasha above.
    if len(engine_signs) < 12 or len(oracle_signs) < 12:
        return {
            "sign_sequence_match": False,
            "engine_signs": engine_signs,
            "oracle_signs": oracle_signs,
            "disposition": "comparison_invalid",
        }
    if engine_signs != oracle_signs:
        return {
            "sign_sequence_match": False,
            "engine_signs": engine_signs,
            "oracle_signs": oracle_signs,
            "disposition": "fail",
        }
    deltas_days = []
    # mismatched_durations exposes which signs' durations disagree, since
    # max_boundary_delta_days alone can't distinguish "tiny rounding noise"
    # from "a few signs disagree, compounding into a large drift". Additive
    # only — never changes disposition.
    mismatched_durations = [
        e["sign_index"]
        for e, o in zip(engine_answer, oracle_answer, strict=True)
        if e["duration_years"] != o["duration_years"]
    ]
    for i, (e, o) in enumerate(zip(engine_answer, oracle_answer, strict=True)):
        if i > 0:
            deltas_days.append(abs(e["start_jd"] - o["start_jd"]))
        deltas_days.append(abs(e["end_jd"] - o["end_jd"]))
    max_delta = max(deltas_days) if deltas_days else 0.0
    return {
        "sign_sequence_match": True,
        "mismatched_durations": mismatched_durations,
        "max_boundary_delta_days": max_delta,
        "disposition": classify(max_delta, TOLERANCES["dasha_start_delta_days"]),
    }
