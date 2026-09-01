"""IMCCE INPOP adapter (via Skyfield's generic kernel loader). Optional
extra: `pip install vedaksha-parity[inpop]`. MIT (Skyfield) — no license
question, unlike a calcephpy-based route; see docs/oracles.md.

Interface only, per FIREWALL.md rule 1: everything below comes from
Skyfield's public function surface and its own published documentation,
never from reading any C source or the kernel's internal format beyond what
Skyfield's loader exposes.

INPOP is IMCCE's own planetary ephemeris — a separate institution,
integration, and data reduction from JPL's DE series entirely. Every
other astronomical oracle here traces to JPL lineage, so INPOP is the one
source that tests whether agreement means more than "two things built
from the same data agree."

Answers `tropical_position` only — INPOP has no native ayanamsha, so a
sidereal value would mean subtracting someone else's, comparing against
partly-derived arithmetic rather than an independent source.

**Citation required by the distributor:** A. Fienga et al., *inpop21a
planetary ephemerides*, 2021.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from vedaksha_parity.kernel_manifest import verify_kernel
from vedaksha_parity.oracles.base import OracleUnsupported

try:
    import skyfield
    from skyfield.api import load, load_file
except ImportError as exc:  # pragma: no cover - exercised via the raising path
    skyfield = None
    load = None
    load_file = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

# INPOP21a, +/-100-year TDB SPICE kernel: inpop21a_TDB_m100_p100_spice.tar.gz
# from IMCCE (~18MB compressed). Not bundled with this repo — fetch it
# yourself and point DEFAULT_KERNEL_PATH (or a constructor argument) at the
# extracted .bsp file. See docs/oracles.md.
DEFAULT_KERNEL_PATH = Path("vendor/kernels/inpop21a.bsp")

# The kernel's own hard span, read from its segments rather than assumed
# from prose — outside this range the adapter refuses rather than
# extrapolating past a Chebyshev segment's fit.
_MIN_JD = 2414105.0
_MAX_JD = 2488985.0

# This kernel carries no body-center segment for any planet; every planet
# here is answered from its SYSTEM BARYCENTER. For Mercury and Venus that
# is the body itself to well under a milliarcsecond (no moons); for
# Mars/Jupiter/Saturn it is a small, known offset from the true body
# center.
_TARGETS = {
    "Sun": "sun",
    "Moon": "moon",
    "Mercury": "mercury barycenter",
    "Venus": "venus barycenter",
    "Mars": "mars barycenter",
    "Jupiter": "jupiter barycenter",
    "Saturn": "saturn barycenter",
}


class InpopOracle:
    NAME = "IMCCE INPOP21a"

    def __init__(self, kernel_path: Path | None = None) -> None:
        if load_file is None:
            raise OracleUnsupported(
                "skyfield is not installed — pip install vedaksha-parity[inpop]"
            ) from _IMPORT_ERROR
        self._kernel_path = kernel_path or DEFAULT_KERNEL_PATH
        if not self._kernel_path.exists():
            raise OracleUnsupported(
                f"INPOP21a kernel not found at {self._kernel_path} — see "
                f"docs/oracles.md for where to fetch it"
            )
        verify_kernel(self._kernel_path)
        self._ts = load.timescale()
        # `load_file`, never `load`: the latter can silently download a
        # different kernel from a JPL mirror if not found locally.
        self._eph = load_file(str(self._kernel_path))
        self._earth = self._eph["earth"]
        self.VERSION = f"skyfield {skyfield.__version__} + INPOP21a ({self._kernel_path.name})"

    def settings(self) -> dict[str, Any]:
        return {
            "kernel": str(self._kernel_path),
            "kernel_coverage": f"JD {_MIN_JD:.1f}-{_MAX_JD:.1f} (1897-06-30 to 2102-07-05)",
            "frame": "apparent geocentric ecliptic OF DATE (epoch='date')",
            "time_scale": "case jd_ut treated as UT1 via ts.ut1_jd(jd_ut)",
            "planet_targets": (
                "all seven bodies answered from their SYSTEM BARYCENTER — this "
                "kernel carries no body-center segment for any of them"
            ),
            "citation": "A. Fienga et al., inpop21a planetary ephemerides, 2021",
            "position": "unsupported — INPOP has no ayanamsha to derive a "
            "sidereal value from. Answers tropical_position instead.",
            "ayanamsha": "unsupported — a Jyotish construct, not an astronomical one",
        }

    def answer(self, case: dict[str, Any]) -> dict[str, Any]:
        kind = case.get("kind")
        if kind == "tropical_position":
            return self._tropical_position(case["jd_ut"], case["body"])
        if kind == "position":
            raise OracleUnsupported(
                "IMCCE INPOP21a adapter: cannot answer a sidereal position without "
                "subtracting an ayanamsha it does not itself define — that would "
                "compare the engine against partly-derived arithmetic, not an "
                "independent source. Answers tropical_position instead."
            )
        if kind == "ayanamsha":
            raise OracleUnsupported(
                "IMCCE INPOP21a adapter: ayanamsha is a Jyotish construct, not an "
                "astronomical one — INPOP has no opinion on it."
            )
        raise OracleUnsupported(f"IMCCE INPOP21a adapter does not answer kind={kind!r}")

    def _tropical_position(self, jd_ut: float, body: str) -> dict[str, float]:
        if not (_MIN_JD <= jd_ut <= _MAX_JD):
            raise OracleUnsupported(
                f"IMCCE INPOP21a adapter: jd_ut={jd_ut} is outside the shipped "
                f"kernel's span ({_MIN_JD:.1f}-{_MAX_JD:.1f})"
            )
        target = _TARGETS.get(body)
        if target is None:
            raise OracleUnsupported(
                f"IMCCE INPOP21a adapter has no body mapping for {body!r} — this "
                f"kernel carries no lunar nodes"
            )
        t = self._ts.ut1_jd(jd_ut)
        apparent = self._earth.at(t).observe(self._eph[target]).apparent()
        lat, lon, _ = apparent.ecliptic_latlon(epoch="date")
        return {"longitude": float(lon.degrees) % 360.0, "latitude": float(lat.degrees)}
