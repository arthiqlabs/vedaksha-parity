# The oracles

Named openly — unlike a private lab, this repo's whole value depends on
anyone being able to see exactly what it compared Vedaksha against and
reproduce it. See `FIREWALL.md` for what "compares against" does and does
not permit.

No oracle here is "the truth." Where two oracles agree with each other and
not with Vedaksha, that is a strong signal. Where they disagree with each
other, the question is almost always a convention, not an error.

**Every oracle here runs locally — no live network dependency, ever.**
Deliberate, not incidental: this repo's reproducibility claim is "clone it
and re-run it," and a source that can be unreachable, rate-limited, or
silently change its answer over the network cannot honestly participate in
that claim. JPL Horizons was investigated and built, then removed for
exactly this reason — see "Considered, not pursuing" below. Its offline
equivalent, SPICE kernels via NAIF, is what Skyfield+DE440 already
provides.

| Oracle | Role | Case kinds answered | License |
|---|---|---|---|
| **Swiss Ephemeris** (`pyswisseph`) | Astronomical reference for positions and ayanamsha | `position`, `tropical_position`, `ayanamsha` | AGPL-3.0-only / commercial |
| **Skyfield + JPL DE440/DE441** | Authority at sweep scale, offline (local kernel file) | `tropical_position` only | MIT. Kernels: public data, not code |
| **IMCCE INPOP21a** (via Skyfield) | Institutionally independent astronomical authority — a separate numerical integration from Paris Observatory, not JPL-lineage like every other source above | `tropical_position` only | MIT (Skyfield's generic kernel loader reads the INPOP data file directly — no calcephpy dependency, no CeCILL license question at all) |
| **Astronomy Engine** | Structurally independent analytic engine — no swisseph, no JPL files | `tropical_position` only | MIT |
| **jyotishganit** | Independent implementation of Vedic calculation logic. Its own docs cite a JPL-lineage ephemeris underneath, so it is independent of swisseph but *not* astronomically independent of the JPL family | `position` only (own ayanamsha value doesn't precess — see its adapter's docstring; `ayanamsha` case kind always refused) | MIT |
| **PyJHora** | Programmatic proxy for Jagannatha Hora's own methodology, validated by its author against ~6,800 of JHora's own outputs | `combustion`, `chara_dasha`, `karakas` (8-scheme, via `horoscope.main.get_chara_karakas`, `Engine(karaka_scheme="8")`; see `docs/tiers.md` for the run). Independence from Swiss Ephemeris is not confirmed — see "PyJHora's independence from Swiss Ephemeris" in `docs/tiers.md`; `position`/`ayanamsha` stay unbuilt as a separate scope choice | AGPL-3.0 — see `CLAUDE.md`. PyPI's own classifier metadata mislabels this package MIT; the GitHub repo's license badge is unambiguous |

All six adapters are implemented; the last column above is each one's real,
current answering scope — several deliberately answer nothing yet, for
reasons documented in their own adapter docstrings, never silently.

### Independence is a graph, not a headcount

Six oracle *names* is not six independent statistical observations —
several trace to the same underlying astronomical data, and agreement
between two members of the same family is expected, not a separate
confirmation:

- **JPL family** — Skyfield+DE440 (the DE440 kernel directly), Vedaksha's
  own SPK path (also DE440-derived, per Vedaksha's own published README),
  and jyotishganit (its own docs cite a JPL-lineage ephemeris underneath —
  DE421 specifically, per its adapter's docstring). Agreement among these
  three says "this JPL-derived data is read the same way three times,"
  not three separate astronomical solutions agreeing.
- **IMCCE family** — INPOP21a alone. A separate institution, a separate
  numerical integration, a separate data reduction from JPL's DE series
  entirely — this is the one member of the roster that tests whether
  agreement with a JPL-lineage source means anything beyond "two things
  built from the same data agree."
- **Structurally independent, not necessarily astronomically independent**
  — Astronomy Engine (VSOP87A + ELP/MPP02 analytic theory, no swisseph or
  JPL kernel files at runtime). VSOP87 itself was historically fit against
  JPL ephemeris data during its own construction, so this is independent
  *software* (no shared code, no shared kernel file, no live dependency),
  not a guarantee of an independent underlying astronomical solution.
- **Own family** — Swiss Ephemeris (its own long-term numerical
  integration plus analytic extensions, not a direct JPL kernel read) and
  PyJHora (a from-a-book reimplementation of Jagannatha Hora's own
  methodology; independence from Swiss specifically is measured, not
  confirmed — see "PyJHora's independence from Swiss Ephemeris" in
  `docs/tiers.md`).

Reading a result: agreement across the JPL family alone is weak evidence.
Agreement that also includes IMCCE, or Astronomy Engine, or Swiss/PyJHora,
is the stronger signal — because at that point the sources genuinely stop
sharing a common origin.

## Case kinds

- **`position`** — sidereal (nirayana) longitude/latitude/distance/speed.
  Only an oracle with its own native ayanamsha concept can honestly answer
  this (Swiss Ephemeris, jyotishganit).
- **`tropical_position`** — tropical (sayana) longitude/latitude, same
  bodies. For oracles with no ayanamsha of their own (Skyfield+DE440,
  INPOP, Astronomy Engine), this is the only position case kind
  they can honestly answer — deriving a sidereal value from them by
  subtracting this harness's own ayanamsha would compare Vedaksha against
  partly-derived arithmetic, not an independent source. Vedaksha's own
  tropical longitude is constructed as `sidereal_longitude +
  ayanamsha_value (mod 360)` — its own two already-computed outputs summed,
  never borrowed from any oracle (`Engine.tropical_position`,
  `src/vedaksha_parity/engine.py`).
- **`ayanamsha`** — the ayanamsha value itself. Only Swiss Ephemeris answers
  this; jyotishganit's own ayanamsha field does not precess (measured
  ~0.01° total wander across a 132-year span where a genuine ayanamsha
  moves ~1.83°), so comparing it would measure Vedaksha's own precession
  against a near-constant, not a real divergence.

**Delta-T validity bound.** Any Skyfield-anchored `tropical_position`
comparison (Skyfield+DE440, and INPOP, which is also read through Skyfield)
is only trustworthy roughly 1800–2100. Outside that window Skyfield's
tabulated delta-T is extrapolated rather than observed, which can diverge
from another independent extrapolation by tens of arcseconds — a
documented property of the extrapolation itself, never an ephemeris
disagreement or an engine defect. Each affected adapter enforces this as a
refusal, not a silent wide tolerance.

**Per-oracle ayanamsha override.** jyotishganit is fixed to True
Chitrapaksha, not Vedaksha's Lahiri default — comparing its `position`
answers against a Lahiri-configured engine would produce a permanent,
misleading systematic offset. `Engine(ayanamsha=...)` accepts an override,
and the `run-config` YAML schema (`docs/birth-data.md`) exposes it per
oracle explicitly, so a run's exact configuration is always visible in the
config file itself, never buried as an assumption inside adapter code.
Vedaksha's own accepted name for this ayanamsha is `TrueChitra` — confirmed
by actually running it, not assumed from either library's naming — and its
own error message describes it as "re-derived from Spica at sidereal 180
degrees," which may not be bit-identical to jyotishganit's own derivation
of the same nominal ayanamsha. A `TrueChitra`-configured comparison removes
the gross systematic offset; any small residual is a genuine question for
this class of ayanamsha, not yet resolved as convention or divergence.

**Swiss Ephemeris `ayanamsha_mode`.** As of `vedaksha>=7.6.0`, Vedaksha's
own `ayanamsha` case kind reports the *true* ayanamsha (mean + nutation
in longitude), not the mean-only value it reported before. `SwissephOracle`
defaults to matching that (`ayanamsha_mode="true"` — its own mean
ayanamsha, `get_ayanamsa_ut`, plus swisseph's own published nutation call,
`SE_ECL_NUT`), and accepts `ayanamsha_mode="mean"` to compare against the
older, mean-only value instead — set per oracle in `run-config` YAML the
same way as the ayanamsha override above:
```yaml
oracles:
  - name: swisseph
    ayanamsha_mode: mean   # default is "true" — set explicitly to compare Vedaksha's true value against swisseph's mean-only one
```
Comparing Vedaksha's true value against swisseph's mean value (rather
than swisseph's own true value) produces a large, spurious-looking T2
divergence — a comparator mode mismatch, not a Vedaksha or swisseph
defect. See `docs/tiers.md`'s T1/T1-tropical/T2 result for the
correctly-matched figures.

### Considered, not pursuing

Deliberately excluded:

- **JPL Horizons** (`astroquery`) — built and working, then removed: it is
  a live NASA API with no offline/local execution path (JPL distributes no
  standalone Horizons binary — confirmed by checking, not assumed), the
  one oracle in the roster that couldn't honestly participate in "clone it
  and re-run it, no network required." Its offline equivalent — SPICE
  kernels via NAIF — is what Skyfield+DE440 already provides locally, so
  nothing capability-wise is lost.
- **jyotisha** (`jyotisham/jyotisha`) — hard-pins `pyswisseph` internally, so any agreement with it would be partly circular with the swisseph oracle already in the roster.
- **VedAstro** (engine and birth-bank timezone data alike) — heavier integration lift (Python binding to a .NET core is unconfirmed) or a live third-party network dependency, unlike every other candidate here.
- **US Naval Observatory Astronomical Applications API** — a third independent institutional authority, but couldn't confirm it exposes raw geocentric planetary longitude rather than almanac-style products only.
- **Maitreya** — original author inactive, codebase fragmented across divergent forks, GUI-only with no found CLI/API.
- **Jagannatha Hora itself** — GUI-only freeware, no scripting surface found; PyJHora is used instead as a validated programmatic proxy for the same methodology.
- **drik-panchanga**, **panchangam** — license-undetermined (`NOASSERTION`) or unlicensed; doesn't fit this harness's "anyone can clone and reproduce" design goal regardless of technical merit.

## `pyswisseph` — implemented

Contract implemented by `src/vedaksha_parity/oracles/swisseph_oracle.py`:

```
NAME, VERSION
sidereal_position(jd_ut, body) -> {longitude, latitude, distance, speed}   # kind="position"
tropical_position(jd_ut, body) -> {longitude, latitude, distance, speed}  # kind="tropical_position"
ayanamsha(jd_ut) -> float                                                 # kind="ayanamsha"
```

Configuration pinned explicitly and recorded in every run's settings block:
sidereal mode = Lahiri (`SIDM_LAHIRI`, matching Vedaksha's `IndianOfficial`),
geocentric apparent positions, `FLG_SPEED` for daily motion. The adapter
requests `FLG_SWIEPH` and falls back to the bundled Moshier analytical
ephemeris (`FLG_MOSEPH`) when no `.se1` data files are installed — lower
precision, but it means the harness runs with nothing beyond `pip install
pyswisseph`. Installing the full Swiss Ephemeris data files (`ephe/`,
gitignored, never committed) tightens the comparison.

**The actual backend is checked per call, not assumed from the request.**
swisseph's own returned flags — not the requested ones — determine
whether SWIEPH or MOSEPH really answered; `NAME` reflects this
("Swiss Ephemeris" only if every case in a run used true SWIEPH data,
otherwise labeled with the exact backend tally) and `settings()` reports
`backends_used` directly. `SwissephOracle(require_swieph=True)` fails a
run immediately, case by case, the moment a call doesn't use true SWIEPH
— the strict mode for a run whose figures will be published or cited.
The canonical artifacts under `results/canonical/` were generated in an
environment with no `.se1` files at all, and say so honestly in their own
oracle name.

⚠️ **Licensing.** Swiss Ephemeris is AGPL-3.0-only or commercial. This repo
depends on it as an optional extra (`pip install vedaksha-parity[swisseph]`),
never bundles or redistributes it, and is itself AGPL-3.0-or-later — see
`CLAUDE.md` for the reasoning.

## Bodies

The seven classical grahas (Sun, Moon, Mercury, Venus, Mars, Jupiter,
Saturn) plus the lunar nodes. Vedaksha's own public surface separates
`MeanNode` and `TrueNode` explicitly; both are in scope, reported
separately, never conflated.

## Birth-data bank

Real, third-party-verified birth instants — not just the synthetic sweep
grid — are also part of every run. See `docs/birth-data.md` for the source,
license, and the `birth_bank` config schema.

## Running a full matrix

`vedaksha-parity run-config path/to/run.yaml` runs every listed oracle
against every listed tier in one invocation, instead of one `--oracle
--tier` flag pair at a time:

```yaml
oracles:
  - name: swisseph
  - name: skyfield
  - name: jyotishganit
    ayanamsha: TrueChitra   # see "Per-oracle ayanamsha override" above — Vedaksha's
                            # own exact accepted name, confirmed by running it;
                            # not the same string jyotishganit itself uses
    max_charts: 200        # see "Per-oracle latency cap" below
tiers: [t1, t1-tropical, t2]
sweep:
  from: 2451545.0
  to: 2460310.0
  step: 30.0
birth_bank:
  count: null   # null/omitted = 100% of the bundled bank — see docs/birth-data.md
```

**Per-oracle latency cap.** jyotishganit is measured at ~142ms/call — its
one public entry point computes a full chart (every varga, panchanga limb,
dasha boundary) to answer even one planet's longitude, ~25,000x slower than
swisseph's ~0.005ms (see its adapter's docstring). `max_charts` on an
oracle entry fails the run loudly, before any real work starts, if the
tier's case list would query more distinct instants than that — never a
silent multi-minute wait a consumer didn't ask for. It counts distinct
`jd_ut` values, not raw cases: one "chart" regardless of how many bodies
are queried from it (the adapter itself caches per-instant for exactly
this reason — nine bodies at one instant is one real call, not nine).

`sweep` and `birth_bank` are both optional (at least one is required); when
both are present, a tier's cases are the sweep grid plus the birth-bank
records combined. One run record per oracle × tier is written to `--out`
(default `results/`), each carrying the exact config that produced it —
including any ayanamsha override and the birth-bank's actual seed — in its
`case_params`. Both `run` and `run-config` write two files per run: a
`.json` (the full-fidelity, reproducible record — every case, every
comparison, never truncated) and a companion `.md` generated from it (a
disposition summary, the full failures table, and unsupported/error
reasons grouped by cause) — the JSON is the record anything is ever
verified against; the markdown is what a person actually reads.

## Adding an oracle

1. Implement `src/vedaksha_parity/oracles/<name>.py` against the `Oracle`
   protocol.
2. Register it in `cli.py`'s `_register_oracles()`.
3. Add a row above, including anything it cannot answer — an oracle's blind
   spots matter as much as its values.
4. Do not claim an oracle answers a case kind before its adapter has real,
   run tests exercising it.
