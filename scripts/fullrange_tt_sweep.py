"""TT-addressed full-range sweep: the "by distance from J2000" table published
in the engine's technical report and docs/accuracy/<date>-parity-results.json.

43 instants at 25-year spacing, DE440 only, both sides addressed in TT, the
reference side Skyfield's apparent place of date. The published table uses:

  python -I scripts/fullrange_tt_sweep.py vendor/kernels/de440.bsp 2292184.5 9131.25 43 out.json

Usage: python -I fullrange_tt_sweep.py <kernel.bsp> <start_jd_tt> <step_days> <n> <out.json>
"""

import json
import sys

import vedaksha
from skyfield.api import load, load_file

BODIES = {
    "Sun": "sun",
    "Moon": "moon",
    "Mercury": "mercury",
    "Venus": "venus",
    "Mars": "mars barycenter",
    "Jupiter": "jupiter barycenter",
    "Saturn": "saturn barycenter",
    "Uranus": "uranus barycenter",
    "Neptune": "neptune barycenter",
}
BANDS = [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500), (500, 600)]


def main() -> None:
    kernel, start, step, n, out = (
        sys.argv[1],
        float(sys.argv[2]),
        float(sys.argv[3]),
        int(sys.argv[4]),
        sys.argv[5],
    )
    ts = load.timescale()
    eph = load_file(kernel)
    earth = eph["earth"]
    v = vedaksha.Vedaksha()
    rows = []
    for i in range(n):
        jd = start + i * step
        years = (jd - 2451545.0) / 365.25
        t = ts.tt_jd(jd)
        for name, target in BODIES.items():
            ref = (
                earth.at(t).observe(eph[target]).apparent().ecliptic_latlon(epoch="date")[1].degrees
                % 360.0
            )
            eng = v.analytical_position(name, jd)["longitude"] % 360.0
            d = (eng - ref + 180.0) % 360.0 - 180.0
            rows.append(
                {
                    "jd_tt": jd,
                    "years_from_j2000": years,
                    "body": name,
                    "engine_lon": eng,
                    "ref_lon": float(ref),
                    "delta_arcsec": d * 3600.0,
                }
            )
    bands = []
    for lo, hi in BANDS:
        sel = [r for r in rows if lo <= abs(r["years_from_j2000"]) < hi]
        inst = sorted({r["jd_tt"] for r in sel})
        cell = {}
        for name in BODIES:
            ds = [abs(r["delta_arcsec"]) for r in sel if r["body"] == name]
            cell[name] = {"mean": sum(ds) / len(ds), "max": max(ds)} if ds else None
        bands.append({"band": f"{lo}-{hi}", "n": len(inst), "bodies": cell})
    with open(out, "w") as f:
        json.dump(
            {
                "engine_version": vedaksha.__version__,
                "start_jd_tt": start,
                "step_days": step,
                "n_instants": n,
                "bands": bands,
                "rows": rows,
            },
            f,
            indent=1,
        )
    for b in bands:
        print(
            b["band"],
            b["n"],
            " ".join(f"{k}:{c['mean']:.3f}/{c['max']:.3f}" for k, c in b["bodies"].items() if c),
        )


if __name__ == "__main__":
    main()
