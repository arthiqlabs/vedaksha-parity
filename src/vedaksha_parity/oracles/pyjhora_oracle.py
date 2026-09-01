"""PyJHora adapter (`PyJHora`). Optional extra: `pip install
vedaksha-parity[pyjhora]`. AGPL-3.0 — see CLAUDE.md and README.md's
License section.

PyJHora is a Python reimplementation, from a published book, of the
Jagannatha Hora methodology — not the desktop program itself; there is no
automatable interface to that program, so it is never cross-checked against
it here. Interface only, per FIREWALL.md rule 1: everything below comes
from PyJHora's own public function signatures, docstrings and documented
constants, never from reading its `.py` source.

**Independence from Swiss Ephemeris is measured, not confirmed.** With
both sides pinned to the same ayanamsha, PyJHora's sidereal longitude
differs from swisseph's by a small, stable, body-specific offset (Sun
~20.84", Saturn ~26.2-26.7", constant across three epochs) — that rules
out a relabeled circular value, but is equally consistent with the same
underlying engine run with a different flag. Read comparisons
accordingly.

Combustion is coarser than Vedaksha's: a binary in/not-in list, no
`DeeplyCombust` distinction — see `settings()`.

`divisional_chart()`'s `jd_at_dob` is LOCAL time relative to the `Place`'s
timezone; a neutral `Place` with `timezone=0.0` makes local time equal
UT, so `jd_ut` passes through unchanged.

`drik.set_ayanamsa_mode` is global/module-level state — set once at
construction. Not a concern for this harness's single-oracle-at-a-time
runner.

position/ayanamsha stay out of scope — a separate scope decision, not a
circularity finding.

Karakas answers via `horoscope.main.get_chara_karakas` (not
`dhasa/graha/karaka.py`, a different Jaimini concept). Returns 8 ranked
planet indices; matches Vedaksha's `compute_karakas(scheme="8")`.
PyJHora's rank-4 title is "Maitrikaraka" (friend), Vedaksha's is
"Matrikaraka" (mother) — same rank, different classical label. This
adapter emits Vedaksha's own titles so `compare_karakas` covers all 8
ranks instead of dropping the one whose label differs.
"""

from __future__ import annotations

import contextlib
import io
import sys
from typing import Any

from vedaksha_parity.oracles.base import OracleUnsupported

# Importing `jhora` appends to `sys.path` and prints to stdout as side
# effects — snapshot/restore sys.path and swallow stdout around the
# import only; stderr stays live so a real import error still surfaces.
_sys_path_before_import = list(sys.path)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        from jhora import utils
        from jhora.horoscope.chart import charts
        from jhora.horoscope.dhasa.raasi import chara
        from jhora.horoscope.main import get_chara_karakas
        from jhora.panchanga import drik
except ImportError as exc:  # pragma: no cover - exercised via the raising path
    drik = None
    charts = None
    chara = None
    utils = None
    get_chara_karakas = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None
finally:
    sys.path[:] = _sys_path_before_import


def _hour_decimal_to_hms(hour_decimal: float) -> tuple[int, int, float]:
    hour = int(hour_decimal)
    minute_decimal = (hour_decimal - hour) * 60.0
    minute = int(minute_decimal)
    second = (minute_decimal - minute) * 60.0
    return (hour, minute, second)

# 0-indexed, per utils.PLANET_NAMES / const.SUN_TO_KETU — PyJHora's own
# published constants, not inferred.
_BODY_INDEX = {
    "Sun": 0, "Moon": 1, "Mars": 2, "Mercury": 3,
    "Jupiter": 4, "Venus": 5, "Saturn": 6, "MeanNode": 7,
}
_D1_CHART_FACTOR = 1  # Raasi — the birth chart itself, per divisional_chart's own docstring

# get_chara_karakas' index 7 is _BODY_INDEX's "MeanNode", but
# compute_karakas names it "Rahu" — kept separate so each map stays
# honest about the vocabulary its own call site uses.
_KARAKA_PLANET_NAMES = {
    0: "Sun", 1: "Moon", 2: "Mars", 3: "Mercury",
    4: "Jupiter", 5: "Venus", 6: "Saturn", 7: "Rahu",
}

# Vedaksha's own compute_karakas(scheme="8") titles, in rank order — see
# module docstring on the rank-4 naming variant this sidesteps.
_KARAKA_TITLES_8 = [
    "Atmakaraka", "Amatyakaraka", "Bhratrikaraka", "Matrikaraka",
    "Pitrikaraka", "Putrakaraka", "Gnatikaraka", "Darakaraka",
]


class PyJHoraOracle:
    NAME = "PyJHora"

    def __init__(self) -> None:
        if (
            drik is None or charts is None or chara is None or utils is None
            or get_chara_karakas is None
        ):
            raise OracleUnsupported(
                "PyJHora is not installed — pip install vedaksha-parity[pyjhora]"
            ) from _IMPORT_ERROR
        import importlib.metadata

        self.VERSION = importlib.metadata.version("PyJHora")
        # Global/module-level, per this module's docstring — set once here.
        drik.set_ayanamsa_mode("LAHIRI")
        self._place = drik.Place("neutral (geocentric quantities only)", 0.0, 0.0, 0.0)

    def settings(self) -> dict[str, Any]:
        return {
            "ayanamsha": "LAHIRI — global module state, see module docstring",
            "independence_from_swisseph": "Measured, not confirmed — see module docstring",
            "combustion": "Binary (Combust/None only), no DeeplyCombust distinction",
            "location": "synthetic/neutral (0.0 deg, 0.0 deg, UTC)",
            "chara_dasha": "Real location required. Narayana dasha exists in PyJHora but is not wired — Chara is the pilot",
            "karakas": "8-scheme via get_chara_karakas — compare against Engine(karaka_scheme=\"8\"); rank 4 emitted as Vedaksha's own \"Matrikaraka\", not PyJHora's \"Maitrikaraka\"",
            "scope": "position/ayanamsha not built here — a separate scope decision, not a circularity finding",
        }

    def answer(self, case: dict[str, Any]) -> dict[str, Any]:
        kind = case.get("kind")
        if kind == "combustion":
            return self._combustion(case)
        if kind == "chara_dasha":
            return self._chara_dasha(case)
        if kind == "karakas":
            return self._karakas(case)
        raise OracleUnsupported(
            f"PyJHora adapter does not answer kind={kind!r} — see settings()."
        )

    def _karakas(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        ranked_indices = get_chara_karakas(case["jd_ut"], self._place)
        return [
            {"karaka": title, "planet": _KARAKA_PLANET_NAMES[index]}
            for title, index in zip(_KARAKA_TITLES_8, ranked_indices, strict=True)
        ]

    def _chara_dasha(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        # Lagna-based, real location required — unlike combustion, this
        # cannot use the neutral placeholder Place.
        place = drik.Place("vedaksha-parity probe location", case["latitude"], case["longitude"], 0.0)
        year, month, day, hour_decimal = utils.jd_to_gregorian(case["jd_ut"])
        dob, tob = (year, month, day), _hour_decimal_to_hms(hour_decimal)
        periods = chara.get_dhasa_antardhasa(dob, tob, place, dhasa_level_index=1)
        result = []
        for sign_tuple, (y, m, d, h), duration_years in periods:
            start_jd = utils.julian_day_number((y, m, d), _hour_decimal_to_hms(h))
            result.append({"sign_index": sign_tuple[0], "start_jd": start_jd, "duration_years": duration_years})
        for i, period in enumerate(result):
            period["end_jd"] = (
                result[i + 1]["start_jd"] if i + 1 < len(result)
                else period["start_jd"] + period["duration_years"] * 365.25
            )
        return result

    def _combustion(self, case: dict[str, Any]) -> dict[str, Any]:
        body = case["body"]
        index = _BODY_INDEX.get(body)
        if index is None or body == "Sun":
            raise OracleUnsupported(
                f"PyJHora combustion adapter has no mapping for {body!r} — "
                f"answers {sorted(k for k in _BODY_INDEX if k != 'Sun')} only"
            )
        planet_positions = charts.divisional_chart(case["jd_ut"], self._place, _D1_CHART_FACTOR)
        combust_indices = charts.planets_in_combustion(planet_positions)
        return {"planet": body, "state": "Combust" if index in combust_indices else "None"}
