"""Swiss Ephemeris adapter (`pyswisseph`). Optional extra: `pip install
vedaksha-parity[swisseph]`. AGPL-3.0-only — see CLAUDE.md and README.md's
License section.

Interface only, per FIREWALL.md rule 1: everything below comes from
`swisseph`'s public function surface and its own published documentation,
never from reading any C source.
"""

from __future__ import annotations

from typing import Any

from vedaksha_parity.oracles.base import OracleUnsupported

try:
    import swisseph as swe
except ImportError as exc:  # pragma: no cover - exercised via the raising path
    swe = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

_BODY_IDS = {
    "Sun": "SUN",
    "Moon": "MOON",
    "Mercury": "MERCURY",
    "Venus": "VENUS",
    "Mars": "MARS",
    "Jupiter": "JUPITER",
    "Saturn": "SATURN",
    "MeanNode": "MEAN_NODE",
    "TrueNode": "TRUE_NODE",
}

# swisseph's own documented single-byte house-system codes. Only the one
# this harness's case generation actually requests (Vedaksha's own default)
# is mapped — add more here, never guess a code for one that isn't tested.
_HOUSE_SYSTEMS = {"Placidus": b"P"}


_AYANAMSHA_MODES = ("mean", "true")


class SwissephOracle:
    NAME = "Swiss Ephemeris"

    def __init__(self, ayanamsha_mode: str = "true") -> None:
        if swe is None:
            raise OracleUnsupported(
                "pyswisseph is not installed — "
                "pip install vedaksha-parity[swisseph]"
            ) from _IMPORT_ERROR
        if ayanamsha_mode not in _AYANAMSHA_MODES:
            raise OracleUnsupported(
                f"Swiss Ephemeris adapter has no ayanamsha_mode {ayanamsha_mode!r} — "
                f"answers {_AYANAMSHA_MODES} only"
            )
        self.VERSION = str(swe.version)
        self._ayanamsha_mode = ayanamsha_mode
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        self._body_ids = {name: getattr(swe, const) for name, const in _BODY_IDS.items()}

    def settings(self) -> dict[str, Any]:
        return {
            "sidereal_mode": "SIDM_LAHIRI",
            "ayanamsha_mode": self._ayanamsha_mode,
            "flags": "FLG_SIDEREAL | FLG_SPEED, FLG_SWIEPH preferred, "
            "FLG_MOSEPH fallback with no ephemeris files installed",
        }

    def answer(self, case: dict[str, Any]) -> dict[str, Any]:
        kind = case.get("kind")
        if kind == "position":
            return self._position(case, sidereal=True)
        if kind == "tropical_position":
            return self._position(case, sidereal=False)
        if kind == "ayanamsha":
            return self._ayanamsha(case)
        if kind == "houses":
            return self._houses(case)
        raise OracleUnsupported(f"Swiss Ephemeris adapter does not answer kind={kind!r}")

    def _position(self, case: dict[str, Any], *, sidereal: bool) -> dict[str, Any]:
        body = case["body"]
        if body not in self._body_ids:
            raise OracleUnsupported(f"Swiss Ephemeris adapter has no body mapping for {body!r}")
        jd_ut = case["jd_ut"]
        # The same library, the same call, with FLG_SIDEREAL simply omitted
        # for the tropical case — swisseph is dual-mode natively, unlike
        # every other oracle in this roster, which is why it is the only
        # source that can answer both `position` and `tropical_position`.
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED
        if sidereal:
            flags |= swe.FLG_SIDEREAL
        try:
            (lon, lat, dist, lon_speed, _lat_speed, _dist_speed), _ret_flags = swe.calc_ut(
                jd_ut, self._body_ids[body], flags
            )
        except swe.Error as exc:
            raise OracleUnsupported(f"swisseph raised for {body!r} at jd_ut={jd_ut}: {exc}") from exc
        return {
            "longitude": lon,
            "latitude": lat,
            "distance": dist,
            "speed": lon_speed,
        }

    def _ayanamsha(self, case: dict[str, Any]) -> dict[str, Any]:
        jd_ut = case["jd_ut"]
        mean_value = swe.get_ayanamsa_ut(jd_ut)
        if self._ayanamsha_mode == "mean":
            return {"value": mean_value}
        # "true" — mean ayanamsha plus nutation-in-longitude, matching
        # Vedaksha's own true_ayanamsha_value (docs/tiers.md). SE_ECL_NUT
        # index 2 is nutation in longitude, in degrees.
        (_true_obliquity, _mean_obliquity, nutation_in_longitude, *_rest), _ret_flags = swe.calc_ut(
            jd_ut, swe.ECL_NUT, 0
        )
        return {"value": mean_value + nutation_in_longitude}

    def _houses(self, case: dict[str, Any]) -> dict[str, Any]:
        house_system = case.get("house_system", "Placidus")
        hsys = _HOUSE_SYSTEMS.get(house_system)
        if hsys is None:
            raise OracleUnsupported(
                f"Swiss Ephemeris adapter has no house-system mapping for {house_system!r}"
            )
        try:
            cusps, ascmc = swe.houses_ex(
                case["jd_ut"], case["latitude"], case["longitude"], hsys=hsys, flags=swe.FLG_SIDEREAL
            )
        except swe.Error as exc:
            raise OracleUnsupported(f"swisseph houses_ex raised: {exc}") from exc
        return {"asc": ascmc[0], "mc": ascmc[1], "cusps": list(cusps)}
