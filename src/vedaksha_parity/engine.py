"""The engine under test: Vedaksha, called through its published PyPI
package exactly as any external consumer would. See FIREWALL.md's Working
directory discipline — this module never touches the `vedaksha` repository.
"""

from __future__ import annotations

from typing import Any

import vedaksha

from vedaksha_parity.config import (
    BODIES,
    NODES,
    PLACEHOLDER_LATITUDE,
    PLACEHOLDER_LONGITUDE,
    VEDAKSHA_AYANAMSHA,
    VEDAKSHA_KARAKA_SCHEME,
)

_VARGA_BODIES = frozenset((*BODIES, *NODES))


class Engine:
    NAME = "Vedaksha"

    def __init__(self, ayanamsha: str | None = None, karaka_scheme: str | None = None) -> None:
        # Overridable so a run can match an oracle's own fixed convention
        # (e.g. jyotishganit's ayanamsha, PyJHora's 8-karaka scheme) without
        # a mismatch masquerading as a divergence. Recorded in settings().
        self._client = vedaksha.Vedaksha()
        self.VERSION = getattr(vedaksha, "__version__", "unknown")
        self._ayanamsha = ayanamsha or VEDAKSHA_AYANAMSHA
        self._karaka_scheme = karaka_scheme or VEDAKSHA_KARAKA_SCHEME

    def settings(self) -> dict[str, Any]:
        return {"ayanamsha": self._ayanamsha, "karaka_scheme": self._karaka_scheme}

    def _chart(self, jd_ut: float) -> dict[str, Any]:
        # Geocentric quantities don't depend on location (config.py); the
        # placeholder exists only because natal_chart requires one.
        return self._client.natal_chart(
            julian_day=jd_ut,
            latitude=PLACEHOLDER_LATITUDE,
            longitude=PLACEHOLDER_LONGITUDE,
            ayanamsha=self._ayanamsha,
        )

    @staticmethod
    def _find_planet(chart: dict[str, Any], body: str) -> dict[str, Any]:
        for planet in chart["planets"]:
            if planet["name"] == body:
                return planet
        raise KeyError(f"Vedaksha's natal_chart did not return a body named {body!r}")

    def position(self, jd_ut: float, body: str) -> dict[str, float]:
        planet = self._find_planet(self._chart(jd_ut), body)
        return {
            "longitude": planet["longitude"],
            "latitude": planet["latitude"],
            "distance": planet["distance"],
            "speed": planet["speed"],
        }

    def tropical_position(self, jd_ut: float, body: str) -> dict[str, float]:
        # sidereal + ayanamsha = tropical by definition — Vedaksha's own two
        # outputs, never an oracle's.
        chart = self._chart(jd_ut)
        planet = self._find_planet(chart, body)
        return {
            "longitude": (planet["longitude"] + chart["true_ayanamsha_value"]) % 360.0,
            "latitude": planet["latitude"],
            "distance": planet["distance"],
            "speed": planet["speed"],
        }

    def ayanamsha(self, jd_ut: float) -> float:
        return self._chart(jd_ut)["true_ayanamsha_value"]

    def houses(
        self, jd_ut: float, latitude: float, longitude: float, house_system: str = "Placidus"
    ) -> dict[str, Any]:
        # Real location required — house cusps depend on it, unlike
        # `_chart()`'s geocentric quantities.
        chart = self._client.natal_chart(
            julian_day=jd_ut,
            latitude=latitude,
            longitude=longitude,
            ayanamsha=self._ayanamsha,
            house_system=house_system,
        )
        return chart["houses"]

    def bhavas(self, jd_ut: float, latitude: float, longitude: float) -> list[dict[str, Any]]:
        asc = self.houses(jd_ut, latitude, longitude)["asc"]
        return self._client.call_tool("compute_bhavas", ascendant=asc)["houses"]

    def ashtakavarga(self, jd_ut: float, latitude: float, longitude: float) -> list[int]:
        chart = self.houses(jd_ut, latitude, longitude)
        lon = self._graha_longitudes(self._chart(jd_ut))
        signs = {name: int(value // 30.0) for name, value in lon.items()}
        lagna_sign = int(chart["asc"] // 30.0)
        result = self._client.call_tool(
            "compute_ashtakavarga",
            sun=signs["Sun"], moon=signs["Moon"], mars=signs["Mars"], mercury=signs["Mercury"],
            jupiter=signs["Jupiter"], venus=signs["Venus"], saturn=signs["Saturn"], lagna=lagna_sign,
        )
        return result["sarvashtakavarga"]

    def panchanga(self, jd_ut: float, latitude: float, longitude: float) -> dict[str, Any]:
        lon = self._graha_longitudes(self._chart(jd_ut))
        return self._client.call_tool(
            "compute_panchanga", jd=jd_ut, sun=lon["Sun"], moon=lon["Moon"],
            latitude=latitude, longitude=longitude,
        )

    def vargas(
        self, jd_ut: float, latitude: float, longitude: float, division: str
    ) -> dict[str, int]:
        # Returns {body: 0-indexed sign}; "Lagna" included alongside the
        # nine grahas/nodes since the varga ascendant is itself testable.
        result = self._client.call_tool(
            "compute_vargas",
            julian_day=jd_ut, latitude=latitude, longitude=longitude,
            divisions=[division], ayanamsha=self._ayanamsha,
        )
        varga = result["vargas"][0]
        signs = {"Lagna": varga["lagna_sign"]}
        for p in varga["placements"]:
            if p["planet"] in _VARGA_BODIES:
                signs[p["planet"]] = p["varga_sign"]
        return signs

    def _graha_longitudes(self, chart: dict[str, Any]) -> dict[str, float]:
        return {p["name"]: p["longitude"] for p in chart["planets"]}

    def _graha_signs(self, chart: dict[str, Any]) -> dict[str, int]:
        return {p["name"]: p["sign_index"] for p in chart["planets"]}

    def karakas(self, jd_ut: float) -> list[dict[str, Any]]:
        lon = self._graha_longitudes(self._chart(jd_ut))
        kwargs = {
            "sun": lon["Sun"], "moon": lon["Moon"], "mars": lon["Mars"], "mercury": lon["Mercury"],
            "jupiter": lon["Jupiter"], "venus": lon["Venus"], "saturn": lon["Saturn"],
        }
        if self._karaka_scheme == "8":
            # Rahu only enters under the 8-scheme (compute_karakas's own schema).
            kwargs["rahu"] = lon["MeanNode"]
            kwargs["scheme"] = "8"
        return self._client.call_tool("compute_karakas", **kwargs)

    def combustion(self, jd_ut: float, body: str) -> dict[str, Any]:
        # compute_combustion answers all six bodies at once; cases are
        # per-body (cases.py), so this filters the one requested.
        lon = self._graha_longitudes(self._chart(jd_ut))
        results = self._client.call_tool(
            "compute_combustion",
            sun=lon["Sun"], moon=lon["Moon"], mars=lon["Mars"], mercury=lon["Mercury"],
            jupiter=lon["Jupiter"], venus=lon["Venus"], saturn=lon["Saturn"],
        )
        for entry in results:
            if entry["planet"] == body:
                return entry
        raise KeyError(f"compute_combustion did not return a body named {body!r}")

    def drishti(self, jd_ut: float) -> list[dict[str, Any]]:
        lon = self._graha_longitudes(self._chart(jd_ut))
        # Ketu is always exactly opposite Rahu by definition — arithmetic,
        # not a separate Vedaksha-computed value.
        ketu = (lon["MeanNode"] + 180.0) % 360.0
        return self._client.call_tool(
            "compute_drishti",
            sun=lon["Sun"], moon=lon["Moon"], mars=lon["Mars"], mercury=lon["Mercury"],
            jupiter=lon["Jupiter"], venus=lon["Venus"], saturn=lon["Saturn"],
            rahu=lon["MeanNode"], ketu=ketu,
        )

    def dasha(self, jd_ut: float, system: str = "Vimshottari") -> dict[str, Any]:
        lon = self._graha_longitudes(self._chart(jd_ut))
        return self._client.call_tool(
            "compute_dasha", birth_jd=jd_ut, moon_longitude=lon["Moon"], system=system, levels=1,
        )

    def chara_dasha(self, jd_ut: float, latitude: float, longitude: float) -> list[dict[str, Any]]:
        # Lagna-based, unlike Vimshottari — needs the ascendant. `lagna_sign`
        # is 0-indexed. `graha_signs` (Rahu only; Vedaksha derives Ketu
        # internally) is required — period durations are chart-dependent,
        # keyed to which sign each lord actually occupies.
        asc = self.houses(jd_ut, latitude, longitude)["asc"]
        lagna_sign = int(asc // 30.0)
        signs = self._graha_signs(self._chart(jd_ut))
        result = self._client.call_tool(
            "compute_dasha",
            birth_jd=jd_ut, lagna_sign=lagna_sign, system="Chara", levels=1,
            graha_signs={
                "sun": signs["Sun"], "moon": signs["Moon"], "mars": signs["Mars"],
                "mercury": signs["Mercury"], "jupiter": signs["Jupiter"],
                "venus": signs["Venus"], "saturn": signs["Saturn"], "rahu": signs["MeanNode"],
            },
        )
        return result["periods"]
