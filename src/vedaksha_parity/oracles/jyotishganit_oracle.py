"""jyotishganit adapter. Optional extra: `pip install vedaksha-parity[jyotishganit]`.
MIT — see docs/oracles.md.

Interface only, per FIREWALL.md rule 1: everything below comes from
jyotishganit's public function surface (`calculate_birth_chart`'s signature
and its returned `VedicBirthChart` dataclass's field names) and structural
introspection of its public data model, never from reading its module
source.

jyotishganit is Skyfield/DE421-backed rather than Swiss-Ephemeris-descended
— see docs/oracles.md — which is what makes it a useful second opinion on a
Vedic quantity without sharing the swisseph adapter's own positions.

Two measured constraints, from comparing this adapter's own output across
instants (output-vs-output, per FIREWALL.md rule 1):

1. Its ayanamsha does not precess (1903: 23.8376 deg, 2035: 23.8433 deg —
   ~0.01 deg total, where a genuine one moves ~1.83 deg over that span), so
   ayanamsha cases always raise `OracleUnsupported`; positions stay in
   scope. This near-frozen value is also what explains the MeanNode
   sidereal drift finding in docs/tiers.md.
2. It exposes only the MEAN lunar node, as `celestial_body="Rahu"`, with no
   parameter to request the true node — so a `TrueNode` case always raises.

Its date range is 1899-07-29 to 2053-10-09 (the span of its DE421 backing);
outside it, `calculate_birth_chart` raises and this adapter surfaces that as
`OracleUnsupported` rather than letting it escape as a crash.
"""

from __future__ import annotations

from typing import Any

from vedaksha_parity.julian_day import julian_day_ut
from vedaksha_parity.oracles.base import OracleUnsupported

try:
    import jyotishganit
    from skyfield.api import load
    from skyfield.errors import EphemerisRangeError
except ImportError as exc:  # pragma: no cover - exercised via the raising path
    jyotishganit = None
    load = None
    EphemerisRangeError = Exception
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

# Classical rashi order — common to every Vedic astrology source, not
# derived from jyotishganit's own implementation. Its PlanetPosition reports
# {sign name, degrees within sign}; this reconstructs the absolute sidereal
# longitude in [0, 360).
_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Explicit and exhaustive — a silent default here would misread an
# unrecognised value (a library rename, a new "stationary" state) as direct
# motion with nothing to say otherwise.
_MOTION_TYPES = {"direct": False, "retrograde": True}

# Every quantity this adapter exposes is geocentric, so a synthetic
# location is safe — calculate_birth_chart requires one, but
# houses/ascendant (which would depend on it) are never exposed here.
_NEUTRAL_LAT = 0.0
_NEUTRAL_LON = 0.0
_DATE_RANGE_MSG = "1899-07-29 to 2053-10-09 (DE421 span)"

# Reaching jyotishganit requires a Python `datetime`, which has no year 0 or
# negative years — jd 1721425.5 is 1 Jan, 1 CE. That floor comes from the
# conversion, not the ephemeris underneath, which may answer further back.
_MIN_DATETIME_JD = 1721425.5


class JyotishganitOracle:
    NAME = "jyotishganit"

    def __init__(self) -> None:
        if jyotishganit is None or load is None:
            raise OracleUnsupported(
                "jyotishganit is not installed — "
                "pip install vedaksha-parity[jyotishganit]"
            ) from _IMPORT_ERROR
        import importlib.metadata

        self.VERSION = importlib.metadata.version("jyotishganit")
        self._ts = load.timescale()
        # Per-instance, not @lru_cache: that would leak a strong reference
        # to `self` for the life of the process.
        self._chart_cache: dict[float, Any] = {}

    def settings(self) -> dict[str, Any]:
        return {
            "ayanamsha": "true_chitrapaksha, fixed, does not precess — see module docstring",
            "node_type": "MEAN node only ('Rahu') — TrueNode cases raise",
            "date_range": f"{_DATE_RANGE_MSG} — raises OracleUnsupported outside it",
            "location": f"synthetic/neutral ({_NEUTRAL_LAT} deg, {_NEUTRAL_LON} deg) — every quantity this adapter exposes is geocentric",
            "dasha": "Vimshottari only — calculate_birth_chart has no system parameter",
            "drishti": "Binary special-aspect model, no strength gradation; sign-based, location-independent",
            "vargas": "d2/d3/d4/d7/d9/d10/d12/d16/d20/d24/d27/d30/d40/d45/d60 — no D1, D5, D6, D8, D11",
            "bhavas": "'Trik' (6/8/12) maps to is_dusthana — not 'Trikona' (1/5/9), a different label",
            "ashtakavarga": "Sarvashtakavarga only — Bhinna per-planet tables not read",
            "panchanga": "Plain names only, no pada/kalam/degrees-remaining; real location required",
        }

    def answer(self, case: dict[str, Any]) -> dict[str, Any]:
        kind = case.get("kind")
        if kind == "position":
            return self._position(case)
        if kind == "ayanamsha":
            return self._ayanamsha(case)
        if kind == "dasha":
            return self._dasha(case)
        if kind == "drishti":
            return self._drishti(case)
        if kind == "vargas":
            return self._vargas(case)
        if kind == "bhavas":
            return self._bhavas(case)
        if kind == "ashtakavarga":
            return self._ashtakavarga(case)
        if kind == "panchanga":
            return self._panchanga(case)
        raise OracleUnsupported(f"jyotishganit adapter does not answer kind={kind!r}")

    def _ayanamsha(self, case: dict[str, Any]) -> dict[str, Any]:
        raise OracleUnsupported(
            "jyotishganit's ayanamsha does not precess — see module docstring"
        )

    def _position(self, case: dict[str, Any]) -> dict[str, Any]:
        body = case["body"]
        if body == "TrueNode":
            raise OracleUnsupported(
                "jyotishganit exposes only the mean lunar node — no true node"
            )
        lookup_body = "Rahu" if body == "MeanNode" else body
        chart = self._chart(case["jd_ut"])
        planet = self._planet(chart, lookup_body)
        # Only {sign, sign_degrees, motion_type} per planet — no tropical
        # frame, latitude, or speed. Absent fields, never fabricated.
        return {
            "longitude": self._absolute_longitude(planet.sign, planet.sign_degrees),
            "is_retrograde": self._is_retrograde(planet.motion_type),
        }

    def _dasha(self, case: dict[str, Any]) -> dict[str, Any]:
        # calculate_birth_chart has no system parameter — this is its only
        # dasha computation, matching Vedaksha's Vimshottari default.
        chart = self._chart(case["jd_ut"])
        mahadashas = chart.dashas.all["mahadashas"]
        periods = [
            {
                "lord": lord,
                "start_jd": julian_day_ut(period["start"]),
                "end_jd": julian_day_ut(period["end"]),
            }
            for lord, period in mahadashas.items()
        ]
        return {"maha_dashas": periods}

    def _vargas(self, case: dict[str, Any]) -> dict[str, int]:
        # Real location required — the varga lagna needs the ascendant.
        division = case["division"].lower()  # Vedaksha "D9" -> jyotishganit "d9"
        chart = self._chart_at(case["jd_ut"], case["latitude"], case["longitude"])
        if division not in chart.divisional_charts:
            raise OracleUnsupported(
                f"jyotishganit does not compute {case['division']!r} — it has "
                f"{sorted(chart.divisional_charts)}"
            )
        d_chart = chart.divisional_charts[division]
        signs = {"Lagna": _SIGNS.index(d_chart.ascendant.sign)}
        for house in d_chart.houses:
            for occupant in house.occupants:
                if occupant.celestial_body in ("Sun", "Moon", "Mercury", "Venus", "Mars",
                                                "Jupiter", "Saturn", "Rahu"):
                    name = "MeanNode" if occupant.celestial_body == "Rahu" else occupant.celestial_body
                    signs[name] = _SIGNS.index(occupant.sign)
        return signs

    def _bhavas(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        # "Trik" (6/8/12) maps to is_dusthana — not "Trikona" (1/5/9, trine houses).
        chart = self._chart_at(case["jd_ut"], case["latitude"], case["longitude"])
        return [
            {
                "bhava": house.number,
                "sign": _SIGNS.index(house.sign),
                "is_kendra": "Kendra" in house.purposes,
                "is_trikona": "Trikona" in house.purposes,
                "is_dusthana": "Trik" in house.purposes,
                "is_upachaya": "Upachaya" in house.purposes,
            }
            for house in chart.d1_chart.houses
        ]

    def _ashtakavarga(self, case: dict[str, Any]) -> list[int]:
        chart = self._chart_at(case["jd_ut"], case["latitude"], case["longitude"])
        sav = chart.ashtakavarga.sav
        return [sav[sign] for sign in _SIGNS]

    def _panchanga(self, case: dict[str, Any]) -> dict[str, str]:
        chart = self._chart_at(case["jd_ut"], case["latitude"], case["longitude"])
        p = chart.panchanga
        return {"tithi": p.tithi, "nakshatra": p.nakshatra, "yoga": p.yoga, "karana": p.karana, "vara": p.vaara}

    def _drishti(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        # `to_house` is ascendant-relative (location-dependent) — use
        # `aspect_type` (the classical Nth-aspect number) with the
        # aspecting planet's own SIGN instead, to stay location-independent
        # and match Vedaksha's sign-based compute_drishti. No strength
        # gradation in this model; compare_drishti compares it only when
        # both sides report it.
        chart = self._chart(case["jd_ut"])
        aspects = []
        for planet in chart.d1_chart.planets:
            own_sign_index = _SIGNS.index(planet.sign)
            for entry in planet.aspects["gives"]:
                aspect_type = int(entry["aspect_type"])
                aspected_sign = (own_sign_index + aspect_type - 1) % 12
                aspects.append(
                    {"aspecting_planet": planet.celestial_body, "aspected_sign": aspected_sign}
                )
        return aspects

    def _chart(self, jd_ut: float) -> Any:
        # ~142ms/call — its only entry point computes a full chart even for
        # one planet's longitude, so this cache turns nine per-body calls
        # per instant into one. Neutral placeholder location — safe since
        # every case kind reaching this method is location-independent;
        # Phase B quantities needing a real location use `_chart_at`.
        if jd_ut in self._chart_cache:
            return self._chart_cache[jd_ut]
        chart = self._compute_chart(jd_ut, _NEUTRAL_LAT, _NEUTRAL_LON)
        self._chart_cache[jd_ut] = chart
        return chart

    def _chart_at(self, jd_ut: float, latitude: float, longitude: float) -> Any:
        # Not cached: each Phase B case is already a single real chart.
        return self._compute_chart(jd_ut, latitude, longitude)

    def _compute_chart(self, jd_ut: float, latitude: float, longitude: float) -> Any:
        if jd_ut < _MIN_DATETIME_JD:
            raise OracleUnsupported(
                f"jd={jd_ut} is before 1 CE (jd {_MIN_DATETIME_JD}) — this "
                "adapter reaches jyotishganit through a Python datetime, "
                "which has no year 0 or negative years, so the conversion "
                "cannot represent the instant."
            )
        t = self._ts.ut1_jd(jd_ut)
        try:
            utc_dt = t.utc_datetime().replace(tzinfo=None)
        except ValueError as exc:
            raise OracleUnsupported(
                f"jd={jd_ut} could not be converted to a Python datetime: {exc}"
            ) from exc
        try:
            return jyotishganit.calculate_birth_chart(
                utc_dt, latitude, longitude,
                timezone_offset=0.0,
                location_name="vedaksha-parity probe location",
                name="vedaksha-parity probe",
            )
        except EphemerisRangeError as exc:
            raise OracleUnsupported(
                f"jd={jd_ut} (utc {utc_dt}) is outside jyotishganit's date "
                f"range ({_DATE_RANGE_MSG}): {exc}"
            ) from exc

    @staticmethod
    def _planet(chart: Any, body: str) -> Any:
        for p in chart.d1_chart.planets:
            if p.celestial_body == body:
                return p
        raise OracleUnsupported(f"jyotishganit returned no body named {body!r}")

    @staticmethod
    def _absolute_longitude(sign: str, sign_degrees: float) -> float:
        try:
            index = _SIGNS.index(sign)
        except ValueError:
            raise OracleUnsupported(f"jyotishganit: unrecognised sign {sign!r}") from None
        return (index * 30.0 + float(sign_degrees)) % 360.0

    @staticmethod
    def _is_retrograde(motion_type: str) -> bool:
        try:
            return _MOTION_TYPES[motion_type]
        except KeyError:
            raise OracleUnsupported(
                f"jyotishganit: unrecognised motion_type {motion_type!r} — "
                "expected 'direct' or 'retrograde'"
            ) from None
