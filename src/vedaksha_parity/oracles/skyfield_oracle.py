"""Skyfield + JPL DE440 adapter. Optional extra: `pip install
vedaksha-parity[skyfield]`. MIT — see docs/oracles.md.

Interface only, per FIREWALL.md rule 1: everything below comes from
Skyfield's public documented API (`load()`, `.apparent()`,
`.ecliptic_latlon()`, `Timescale.ut1_jd()`) and its own published
documentation, never from reading Skyfield's implementation source.

Answers `tropical_position` only. DE440 is a purely tropical, JPL-frame
ephemeris with no ayanamsha concept; deriving a sidereal value by
subtracting this harness's own ayanamsha would compare Vedaksha against
its own arithmetic, not an independent source.

Two time/frame details this adapter gets right on purpose:

- `ecliptic_latlon()` with no argument projects into the FIXED J2000
  ecliptic. Pass `epoch="date"` explicitly — the difference is tens of
  arcseconds at century range.
- A case's `jd_ut` is UT1-scale — feed it to `Timescale.ut1_jd()`, never
  `Timescale.tdb_jd()`. TDB trails UT1 by ~60-70 seconds, moving a
  planet's apparent position by close to an arcsecond.

**Delta-T validity bound.** Outside roughly 1800-2100, Skyfield's
tabulated delta-T is extrapolated rather than observed, which can diverge
from another independent extrapolation by tens of arcseconds. This
adapter refuses outside that window.

Mars, Jupiter and Saturn are answered from their DE440 SYSTEM BARYCENTER
— the kernel carries no body-center segment for them. Jupiter's Galilean
moons can shift its barycenter by ~1-2 arcseconds from its true body
center at Earth's distance; disclosed in `settings()`.

No speed is returned: a central-difference estimate would mirror
whatever method Vedaksha uses, biasing the comparison toward agreement.

Kernel data: DE440 covers 1550-2650. Skyfield's own `load()` downloads it
(once, then caches it) from NASA JPL's public kernel archive the first time
this adapter runs — no kernel binary is bundled with this repo. See
https://ssd.jpl.nasa.gov/planets/eph_export.html for the underlying data and
its terms.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from vedaksha_parity.oracles.base import OracleUnsupported

try:
    import skyfield
    from skyfield.api import load
    from skyfield.errors import EphemerisRangeError
except ImportError as exc:  # pragma: no cover - exercised via the raising path
    skyfield = None
    load = None
    EphemerisRangeError = Exception
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

_DEFAULT_KERNEL = "vendor/kernels/de440.bsp"

_TARGETS = {
    "Sun": "sun",
    "Moon": "moon",
    "Mercury": "mercury",
    "Venus": "venus",
    "Mars": "mars barycenter",
    "Jupiter": "jupiter barycenter",
    "Saturn": "saturn barycenter",
}

_UNSUPPORTED_BODIES = {"MeanNode", "TrueNode"}

# Approximate calendar-year bounds — a delta-T validity window, not a
# kernel-coverage limit. See module docstring.
_DT_MIN_JD = 2378495.0  # ~1800-01-01
_DT_MAX_JD = 2488070.0  # ~2100-01-01


class SkyfieldOracle:
    NAME = "Skyfield + JPL DE440"

    def __init__(self, kernel: str | Path = _DEFAULT_KERNEL) -> None:
        if load is None:
            raise OracleUnsupported(
                "skyfield is not installed — pip install vedaksha-parity[skyfield]"
            ) from _IMPORT_ERROR
        self._kernel_name = str(kernel)
        self._ts = load.timescale()
        self._eph = load(self._kernel_name)
        self._earth = self._eph["earth"]
        self.VERSION = f"skyfield {skyfield.__version__} + {Path(self._kernel_name).name}"

    def settings(self) -> dict[str, Any]:
        return {
            "kernel": self._kernel_name,
            "kernel_coverage": "1550-2650 (DE440)",
            "delta_t_validity_window": "~1800-2100 (approximate calendar years) — see module docstring",
            "frame": "apparent geocentric ecliptic of date (epoch='date')",
            "time_scale": "case jd_ut treated as UT1 via Timescale.ut1_jd(); "
            "Skyfield applies its own UT1->TT->TDB tables internally",
            "outer_planet_targets": "Mars/Jupiter/Saturn answered from their DE440 "
            "system barycenter — no separate body-center segment exists in this "
            "kernel for them",
            "speed": "not provided",
            "position": "unsupported — DE440 is tropical-only; this harness's "
            "position case asks for sidereal. Answers tropical_position instead.",
            "ayanamsha": "unsupported — not an astronomical quantity; DE440 has "
            "no opinion on it",
        }

    def answer(self, case: dict[str, Any]) -> dict[str, Any]:
        kind = case.get("kind")
        if kind == "tropical_position":
            return self._tropical_position(case["jd_ut"], case["body"])
        if kind == "position":
            raise OracleUnsupported(
                "Skyfield + DE440 adapter does not answer the sidereal `position` "
                "case kind — DE440 is tropical-only. Answers `tropical_position` instead."
            )
        if kind == "ayanamsha":
            raise OracleUnsupported(
                "Skyfield + DE440 adapter does not answer ayanamsha — not an "
                "astronomical quantity, DE440 has no opinion on it"
            )
        raise OracleUnsupported(f"Skyfield + DE440 adapter does not answer kind={kind!r}")

    def _tropical_position(self, jd_ut: float, body: str) -> dict[str, float]:
        if not (_DT_MIN_JD <= jd_ut <= _DT_MAX_JD):
            raise OracleUnsupported(
                f"jd_ut={jd_ut} is outside this adapter's delta-T validity window "
                f"({_DT_MIN_JD:.1f}-{_DT_MAX_JD:.1f}, ~1800-2100) — see module docstring"
            )
        if body in _UNSUPPORTED_BODIES:
            raise OracleUnsupported(
                f"Skyfield + DE440 adapter has no lunar-node data for {body!r} — "
                "DE440 contains no lunar nodes"
            )
        target = _TARGETS.get(body)
        if target is None:
            raise OracleUnsupported(f"Skyfield + DE440 adapter has no body mapping for {body!r}")
        t = self._ts.ut1_jd(jd_ut)
        try:
            astrometric = self._earth.at(t).observe(self._eph[target])
        except EphemerisRangeError as exc:
            raise OracleUnsupported(
                f"jd_ut={jd_ut} is outside the loaded kernel's coverage for {body!r}: {exc}"
            ) from exc
        apparent = astrometric.apparent()
        lat, lon, _ = apparent.ecliptic_latlon(epoch="date")
        return {"longitude": float(lon.degrees) % 360.0, "latitude": float(lat.degrees)}
