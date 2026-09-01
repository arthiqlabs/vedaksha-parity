"""Astronomy Engine adapter (`astronomy-engine`). Optional extra: `pip
install vedaksha-parity[astronomy-engine]`. MIT.

Interface only, per FIREWALL.md rule 1: everything below comes from
`astronomy-engine`'s public function surface, never from reading its
source. Structurally independent — a truncated VSOP87 + NOVAS C 3.1
implementation with no swisseph, JPL kernels, or ephemeris files of any
kind — so it cannot be a correlated opinion with any other oracle here.

Answers `tropical_position` only — no ayanamsha concept, so a sidereal
value would mean subtracting this harness's own arithmetic, not an
independent source.

Stated accuracy is ~1 arcminute per the library's own documentation.
Answers the full classical seven grahas; pass/review/fail is left
entirely to `compare.py`, never guessed in advance.
"""

from __future__ import annotations

from typing import Any

from vedaksha_parity.oracles.base import OracleUnsupported

try:
    import astronomy
except ImportError as exc:  # pragma: no cover - exercised via the raising path
    astronomy = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

_BODY_NAMES = {
    "Sun": "Sun",
    "Moon": "Moon",
    "Mercury": "Mercury",
    "Venus": "Venus",
    "Mars": "Mars",
    "Jupiter": "Jupiter",
    "Saturn": "Saturn",
}


class AstronomyEngineOracle:
    NAME = "Astronomy Engine"

    def __init__(self) -> None:
        if astronomy is None:
            raise OracleUnsupported(
                "astronomy-engine is not installed — "
                "pip install vedaksha-parity[astronomy-engine]"
            ) from _IMPORT_ERROR
        import importlib.metadata

        self.VERSION = importlib.metadata.version("astronomy-engine")
        self._bodies = {name: getattr(astronomy.Body, const) for name, const in _BODY_NAMES.items()}

    def settings(self) -> dict[str, Any]:
        return {
            "provenance": (
                "truncated VSOP87 + NOVAS C 3.1, no external ephemeris "
                "dependencies of any kind — no swisseph, no JPL kernels, no "
                "data files (published documentation; never read from source)"
            ),
            "frame": (
                "GeoVector(aberration=True) -> Ecliptic() = apparent geocentric "
                "ecliptic of date, tropical"
            ),
            "stated_accuracy": "approximately 1 arcminute (published documentation)",
            "position": "unsupported — this library is tropical-only; this "
            "harness's position case asks for sidereal. Answers "
            "tropical_position instead.",
            "ayanamsha": "unsupported — not an astronomical quantity this library exposes",
            "nodes": "unsupported — no lunar-node body in this library's interface",
            "speed": "not provided — no angular-rate quantity exposed by this interface",
        }

    def answer(self, case: dict[str, Any]) -> dict[str, Any]:
        kind = case.get("kind")
        if kind == "tropical_position":
            return self._tropical_position(case)
        if kind == "position":
            raise OracleUnsupported(
                "Astronomy Engine adapter does not answer the sidereal `position` "
                "case kind — this library is tropical-only. Answers "
                "`tropical_position` instead."
            )
        if kind == "ayanamsha":
            raise OracleUnsupported(
                "Astronomy Engine adapter does not answer kind='ayanamsha' — "
                "ayanamsha is a Jyotish construct, not an astronomical one this "
                "library has any opinion on"
            )
        raise OracleUnsupported(f"Astronomy Engine adapter does not answer kind={kind!r}")

    def _tropical_position(self, case: dict[str, Any]) -> dict[str, Any]:
        body = case["body"]
        if body not in self._bodies:
            raise OracleUnsupported(
                f"Astronomy Engine adapter has no body mapping for {body!r} — "
                f"it answers {sorted(self._bodies)} only; it has no lunar-node "
                "body in its interface"
            )
        jd_ut = case["jd_ut"]
        time = astronomy.Time(jd_ut - 2451545.0)  # days since J2000, UT
        vector = astronomy.GeoVector(self._bodies[body], time, True)
        ecliptic = astronomy.Ecliptic(vector)
        return {
            "longitude": ecliptic.elon % 360.0,
            "latitude": ecliptic.elat,
            "distance": vector.Length(),
        }
