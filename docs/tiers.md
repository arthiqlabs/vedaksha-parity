# Tiers — what this harness tests, and what it deliberately doesn't

Vedaksha's published package exposes 17 tools (`Vedaksha().list_tools()`).
This file inventories all 17, classifies each in or out of scope per
`CLAUDE.md`'s rule ("deterministic quantities only... interpretation is
out of scope"), and states current, reproducible results for every tier
that is built.

**Vedaksha version tested: `vedaksha==9.1.0`**, unless a result below
states a different version explicitly. Re-run any `vedaksha-parity
run-config` command in this file to reproduce the same figures against
that pin, or a newer one to see whether they still hold.

Every discrepancy discussed below that has an actual classification —
documented convention, reference limitation, or genuinely unresolved —
has a structured, evidence-carrying entry in
`docs/discrepancy-registry.yaml`: one immutable record per finding, set
once, never silently moved into a friendlier category without a trace.

## Currently implemented

| Tier | Quantity | Case kind(s) | Oracles that answer it |
|---|---|---|---|
| T1 | sidereal position | `position` | Swiss Ephemeris, jyotishganit |
| T1-tropical | tropical position | `tropical_position` | Swiss Ephemeris, Skyfield+DE440, INPOP21a, Astronomy Engine |
| T2 | ayanamsha | `ayanamsha` | Swiss Ephemeris |
| Karakas | Jaimini karaka ranking (8-scheme) | `karakas` | PyJHora (`horoscope.main.get_chara_karakas`) |
| Combustion | per-body combustion state | `combustion` | PyJHora |
| Drishti | sign-to-sign aspects | `drishti` | jyotishganit |
| Dasha (Vimshottari) | period boundaries | `dasha` | jyotishganit |
| House cusps (Phase B) | Asc, MC, 12 cusps | `houses` | Swiss Ephemeris |
| Vargas (Phase B, D9) | divisional-chart signs | `vargas` | jyotishganit |
| Bhavas (Phase B) | whole-sign house classification | `bhavas` | jyotishganit |
| Ashtakavarga (Phase B) | Sarvashtakavarga bindu counts | `ashtakavarga` | jyotishganit |
| Panchanga (Phase B) | tithi/nakshatra/yoga/karana/vara | `panchanga` | jyotishganit |
| Chara dasha (Phase B) | sign-cycling period boundaries | `chara-dasha` | PyJHora |

Every case lands in exactly one disposition: `pass`, `review`, `fail`,
`oracle_unsupported` (the reference can't answer — e.g. outside its own
supported date range), `oracle_error` (the reference crashed on a valid
input), or `engine_error` (Vedaksha itself raised, most commonly outside
its own supported date range, `[JD 2378496.5, 2597641.5]`, roughly
1800–2400 CE). Run provenance (Vedaksha version, every oracle's settings,
case-generation parameters) is always recorded with the result.

### PyJHora's independence from Swiss Ephemeris

PyJHora's sidereal longitude differs from Swiss Ephemeris's by a small,
stable, body-specific offset (Sun ~20.84″, Saturn ~26.2–26.7″), constant
across three epochs spanning B1900 to 2035, with both pinned to the same
Lahiri ayanamsha. That rules out a directly relabeled value, but a
constant offset is equally consistent with the same underlying engine run
with a different flag (aberration, light-time correction) — independence
from Swiss Ephemeris is not confirmed. Comparisons against PyJHora should
be read with that caveat; it's documented in the adapter itself
(`pyjhora_oracle.py`'s module docstring and `settings()`).

### T1 / T1-tropical / T2 — sidereal and tropical position, ayanamsha

Against Swiss Ephemeris (`SwissephOracle(ayanamsha_mode="true")`, matching
Vedaksha's own true — mean plus nutation — ayanamsha convention), 200 real
birth records, 9 bodies each: **T1 sidereal position 1653 pass / 129
review / 18 engine_error; T1-tropical the same split; T2 ayanamsha 198
pass / 0 review / 0 fail / 2 engine_error.** The only body carrying any
review-band spread is TrueNode (mean −2.5″, range roughly ±30″) — an
inherently higher-variance, perturbation-including quantity, not a
distinct issue. `ayanamsha_mode` is `"mean"`-selectable too, for
comparing against a mean-only ayanamsha convention if that's ever needed;
`"true"` is the default and what the figures above use.

Reproduce: `vedaksha-parity run-config configs/all-tiers-200-birthbank-v2.yaml`

### Karakas

PyJHora's `get_chara_karakas` against Vedaksha's `compute_karakas(scheme="8")`
(`Engine(karaka_scheme="8")`), 200 real birth records: **156 pass / 33
review / 9 fail / 2 engine_error.** A single adjacent-rank swap changes
two karaka titles at once, so this comparator's review threshold is 2
mismatches (`KARAKA_REVIEW_MISMATCH_MAX` in `config.py`), not the 1 used
elsewhere. 33 of the 42 non-passing cases are a single adjacent-rank swap
(now correctly "review"); the rest are larger reorderings. Most
reordering cases correlate with Vedaksha's own computed Rahu
degree-in-sign sitting within about a degree of a sign boundary — a
boundary-sensitivity pattern, not a scattered disagreement — though the
exact mechanism for the small remaining set of near-total reorders isn't
fully resolved.

Reproduce: `vedaksha-parity run-config configs/pyjhora-karakas-200.yaml`

### Combustion

Against PyJHora, 200 real birth records (6 bodies: Moon, Mars, Mercury,
Jupiter, Venus, Saturn): **1,089 pass / 99 fail / 12 engine_error** out of
1,200 cases. The 99 fails split into two categories: 57 are a documented
granularity gap (Vedaksha reports `DeeplyCombust` as a distinct state;
PyJHora's states are binary `Combust`/`None`, concentrated in Mercury,
which sits closest to the Sun); 42 are genuine boundary-crossing
disagreements, consistent with PyJHora's own small stable longitude
offset (above) occasionally placing a planet on the opposite side of the
combustion threshold from Vedaksha.

Reproduce: `vedaksha-parity run-config configs/pyjhora-combustion-200.yaml`

### Drishti

Against jyotishganit (`Engine(ayanamsha="TrueChitra")`), 100 real birth
records: **0 pass / 83 fail / 17 oracle_unsupported** (jyotishganit's own
DE421-backed date range, 1899–2053). Every failing case has exactly 6
mismatches, always confined to Rahu/Ketu — the seven classical grahas
agree perfectly, every time. This is a documented convention difference,
not an open question: Vedaksha treats the nodes as ordinary grahas for
aspect purposes (universal 7th aspect at full strength, graduated partial
strength at 3rd/4th/5th/8th/9th/10th); jyotishganit gives them
Jupiter-like special aspects instead (5th and 9th) and no 7th aspect at
all. Missing 7th × 2 nodes + extra {5th, 9th} × 2 nodes = 6, matching the
measured count exactly on every chart.

Reproduce: `vedaksha-parity run-config configs/jyotishganit-dasha-drishti-100.yaml`

### Dasha (Vimshottari)

Against jyotishganit, 100 real birth records: lord sequence matches on
every evaluable case, with a boundary-date drift of 1.0–6.05 days
(median ~2.1 days) under the current provisional 1-day tolerance band.
The drift is a documented convention difference, not an accuracy problem:
Vedaksha uses the Julian year (365.250000 days) for dasha-period
arithmetic; jyotishganit uses the sidereal year (365.256360 days). The
systematic component of the drift (period boundary delta growing roughly
linearly with elapsed time) is fully explained by that year-length gap; a
smaller near-constant residual (~1.5-day stdev) is not further isolated.
The tolerance band (`dasha_start_delta_days`) is still the provisional
placeholder and has not been recalibrated against this measured
distribution — a real limitation of the current disposition counts, not
of the underlying comparison.

Reproduce: `vedaksha-parity run-config configs/jyotishganit-dasha-drishti-100.yaml`

## Full tool inventory and scope classification

Vedaksha tool → in/out of scope, per `CLAUDE.md`'s existing rule
("yoga qualification, life-event scoring, strength narratives, remedies,
chat... have no accuracy oracle; correctness there is faithfulness to the
classical source, verified by reading — not something this harness
measures").

| Tool | In/out | Why |
|---|---|---|
| `compute_natal_chart` | **in** | T1/T1-tropical/T2's source; houses/aspects fields feed Phase B |
| `compute_dasha` | **in** | deterministic period boundaries |
| `compute_karakas` | **in** | the ranking is deterministic; the significance names are descriptive labels, not scored interpretation |
| `compute_combustion` | **in** | mechanical distance-from-Sun threshold rule |
| `compute_vargas` | **in** | deterministic divisional positions |
| `compute_ashtakavarga` | **in** | mechanical bindu tables from BPHS rules |
| `compute_drishti` | **in** | mechanical sign-to-sign rule |
| `compute_bhavas` | **in** | deterministic whole-sign house assignment |
| `compute_panchanga` | **in** | five deterministic limbs |
| `compute_shadbala` | **out** | "six-fold strength" — a strength narrative |
| `compute_gochara` | **out** | returns a "favourable/unfavourable verdict" — life-event scoring |
| `search_muhurta` | **out** | "quality scores" for auspicious windows — scored interpretation |
| `compute_synastry` | **out** | relationship interpretation |
| `compute_composite` | **out** | relationship interpretation |
| `compute_transit` | **out** | position math already covered by T1/T1-tropical at a different instant — not a new quantity |
| `search_transits` | **out** | a search/timing utility built on positions already tested, not a quantity of its own |
| `emit_graph` | **out** | a data-format converter, not an astrological quantity |

Koota (Ashtakoota compatibility) is not a Vedaksha tool by that name —
PyJHora computes it, but testing it needs a **pairwise** case (two birth
records), which no Vedaksha tool currently accepts as a single call. Not
built: blocked at the tool-inventory level, not an oracle-availability
problem.

## Phase A — no real geographic location needed

Each of these takes only quantities T1 already produces (sidereal
longitudes) or `birth_jd`/`moon_longitude`.

### Karakas (`compute_karakas`)

Input: the seven grahas' sidereal longitudes (Rahu optional, for the
8-karaka scheme). Output:

```json
[{"karaka": "Atmakaraka", "planet": "Moon", "degrees_in_sign": 19.4667}, ...]
```

Compared with a **rank-order comparator**: do the two sides agree on
which planet holds each karaka rank?

### Combustion (`compute_combustion`)

Input: the same seven longitudes, each body's own distance from the Sun
(Sun itself excluded — 6 bodies: Moon, Mars, Mercury, Jupiter, Venus,
Saturn). Output:

```json
[{"planet": "Mercury", "state": "Combust", "degrees_from_sun": 8.4796}, ...]
```

Compared with a **categorical comparator**: do the two sides' `state`
match (`Combust`/`DeeplyCombust`/`None`)? The `degrees_from_sun` value is
carried for context; the disposition keys off the category.

### Drishti (`compute_drishti`)

Input: nine graha longitudes (seven grahas + Rahu + Ketu). Output, one
entry per aspecting/aspected sign pair:

```json
[{"aspecting_planet": "Sun", "aspecting_sign": 8, "aspected_sign": 2, "houses_away": 7, "strength": "Full"}, ...]
```

Compared with a **set/categorical comparator**: for each planet, does the
full set of aspected signs (and each one's strength) match between the
two sides?

### Dasha — Vimshottari/Ashtottari/Yogini (`compute_dasha`)

Input: `birth_jd` + `moon_longitude` (no location). Output (`levels=1`
shown; `sub_periods` nests recursively for `levels>1`):

```json
{
  "initial_balance": 0.04000054327167535,
  "maha_dashas": [
    {"lord": "Rahu", "start_jd": 2451545.0, "end_jd": 2451807.98, "duration_days": 262.98, "level": 1, "sub_periods": []},
    ...
  ]
}
```

Compared with a **date-boundary comparator**: does each period's `lord`
sequence match, and do `start_jd`/`end_jd` agree within a tolerance
expressed in days? Chara and Narayana dasha need `lagna_sign` — Phase B.

### Koota (pairwise compatibility)

Not built. Needs a new case shape (`{kind: "koota", record_a:
BirthRecord, record_b: BirthRecord}`, not `{kind, jd_ut, body}`), a
birth-bank pairing strategy, and a compatibility comparator (per-koota-
category match, not a single scalar) — and, per the scope note above, no
Vedaksha tool currently exposes this as a single call.

## Phase B — needs real geographic location

`Engine`/`config.py` use a fixed placeholder location
(`PLACEHOLDER_LATITUDE`/`PLACEHOLDER_LONGITUDE = 0.0, 0.0`) for T1/
T1-tropical/T2, which are geocentric and location-independent. Every
quantity below needs the real location as an actual input, either
directly or transitively through the ascendant.

| Tool | Needs | Why |
|---|---|---|
| House cusps (`compute_natal_chart`'s `houses` field) | real lat/lon | direct |
| Vargas (`compute_vargas`) | real lat/lon | direct |
| Panchanga (`compute_panchanga`) | real lat/lon | required directly — vara is reckoned from local sunrise |
| Bhavas (`compute_bhavas`) | `ascendant` input | transitively, via houses |
| Ashtakavarga (`compute_ashtakavarga`) | `lagna` input | transitively, via houses |
| Dasha, Chara/Narayana systems | `lagna_sign` input | transitively, via houses |

### The location grid

`data/location-grid.csv` — 20 major Indian cities spanning the
subcontinent's latitude range (8.5°N Thiruvananthapuram to 34.1°N
Srinagar) plus 10 Indian-diaspora hubs abroad: Southern Hemisphere
(Sydney, Durban), high northern latitude (Toronto, London, ~44–51°N), and
near-equator (Singapore, Kuala Lumpur). Columns: `name, category
(india|diaspora), latitude, longitude`.

Phase B tiers iterate this grid crossed with a sweep of instants, not
birth-bank records — testing the house/location math itself with
controlled, known geographic coverage. (T1/T1-tropical/T2 keep using the
birth bank.) Add a city by appending a row to the CSV — no code change
needed.

### House cusps

Against Swiss Ephemeris (`houses_ex(..., flags=FLG_SIDEREAL)`),
compared on Asc + MC + 12 cusps as circular longitude deltas, classified
by the worst of the 14: **883 pass / 47 review / 0 fail** (31-instant
sweep across the full 30-city grid, 930 cases). The 47 review cases are
concentrated at higher-latitude/diaspora cities (London, Toronto, New
York) and mostly on the ascendant specifically — consistent with
ordinary numerical precision at the most latitude-sensitive point in a
chart.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`

### Vargas (D9)

Against jyotishganit's own `divisional_charts['d9']`
(`Engine(ayanamsha="TrueChitra")`), full 30-city grid at 31 instants (930
cases): **916 pass / 12 review / 0 fail / 2 oracle_error.** Every review
mismatch is Lagna-only — a varga sign is only 3.33° wide (30/9 for D9),
far narrower than a whole rashi, and the ascendant is the fastest-moving,
most boundary-sensitive quantity in a chart. The 2 `oracle_error` cases
are a jyotishganit robustness issue (a `TypeError` inside its own
sunrise/sunset computation) at specific real locations, not a
Vedaksha-side problem.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`

### Bhavas

Against jyotishganit's `d1_chart.houses`, compared on sign plus four
boolean roles (kendra/trikona/dusthana/upachaya), same grid and sweep:
**0 pass / 925 review / 3 fail / 2 oracle_error.** Every review case
carries exactly one mismatched field, always `bhava_10.is_upachaya` — a
genuine, live classical ambiguity: the 10th house is simultaneously a
kendra (quadrant) and, by count-from-lagna, an upachaya house
(3rd/6th/10th/11th); whether the two roles are mutually exclusive is a
question in the tradition itself, not a computation bug. The 3 fail cases
are a distinct pattern (all 12 bhava signs mismatched at once), consistent
with the same ascendant-boundary effect documented under house cusps.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`

### Ashtakavarga

Against jyotishganit's own per-sign bindu counts (Sarvashtakavarga
totals), same grid and sweep: **0 pass / 0 review / 928 fail / 2
oracle_error.** Every mismatched sign's delta is exactly ±1 bindu,
concentrated on a small recurring subset of sign pairs (most often
10th/11th). Vedaksha's own tool description states `compute_ashtakavarga`
does not apply Trikona/Ekadhipatya Shodhana or Pinda Sadhana corrections
— a shodhana step is exactly a ±1-bindu-per-sign adjustment, consistent
with this pattern.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`

### Panchanga

Against jyotishganit's `tithi`/`nakshatra`/`yoga`/`karana`/`vara`, same
grid and sweep: **578 pass / 281 review / 69 fail / 2 oracle_error.**
Every mismatch concentrates in vara, yoga, or karana — never tithi or
nakshatra. Vara depends on local sunrise (the same location/timing
sensitivity documented under house cusps); yoga and karana are narrow,
fast-moving divisions (1/60th and 1/30th of the lunar-solar cycle) where
a small residual timing difference crosses a boundary far more often
than in the wider tithi/nakshatra divisions.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`

### Chara dasha

Against PyJHora's `chara.get_dhasa_antardhasa`
(`compare_sign_dasha` — sign sequence plus boundaries), full 30-city grid
at 31 instants (930 cases): **sign sequence matches 930/930 (100%)** —
starting sign and direction both agree at every one of the 12 lagna
categories. Boundary accuracy: median delta ~730 days (~2 years);
185/930 cases (19.9%) match to within 1 day; 228/930 (24.5%) are off by
more than 1,000 days. The remaining spread traces to individual sign-lord
assignments landing on opposite sides of a sign boundary — consistent
with PyJHora's own small stable longitude offset from Vedaksha (see
"PyJHora's independence from Swiss Ephemeris" above) occasionally placing
a slow-moving ruling planet across a boundary between the two engines,
each such case shifting every later period's boundary by up to a year.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`
(no ayanamsha override needed — PyJHora is pinned to Lahiri, matching
Vedaksha's default `IndianOfficial`.)

### MeanNode sidereal drift — resolved against a physical arbiter

Vedaksha's `TrueChitra`-sidereal MeanNode, compared against jyotishganit's
own MeanNode, shows an apparent divergence of −50.35 arcsec/year (linear,
r=1.00) — close to the standard general-precession figure (~50.29″/yr).
Resolved by checking both sides against an independent physical
reference: the Moon's real, instantaneous (osculating) ascending-node
longitude, computed directly from DE440's own state vectors via standard
orbital mechanics (not any node theory or implementation), expressed in
the properly precession-corrected mean ecliptic and equinox of date. A
control (the same osculating node left in the fixed J2000 frame,
deliberately not precession-corrected) recovers ~−50.4″/yr against both
engines, confirming the method detects a precession-frame error of this
size. Against the corrected physical reference, both engines' tropical
mean node come back flat: **−0.036 ± 2.11″/yr against Vedaksha's tropical
mean node, −0.065 ± 2.11″/yr against jyotishganit's** — both within noise
and over 700× smaller than the control. **Vedaksha's mean node does not
drift against the physical kernel geometry.**

The apparent divergence traces to jyotishganit's own separately-reported
ayanamsha value being nearly frozen over time (measured at −0.026″/yr to
−0.16″/yr across two independent samples spanning 1899–2050, against an
expected ~1.83° movement for a genuinely precessing ayanamsha over a
comparable span — documented in `jyotishganit_oracle.py`'s module
docstring). Since jyotishganit's own tropical mean node tracks the
physical node correctly, and its reported ayanamsha barely moves, its
sidereal Rahu output itself moves at very nearly the tropical rate rather
than a precession-corrected sidereal rate — accounting for very nearly
the exact −50.35″/yr gap. This is an output-level fact about jyotishganit
specifically; why its own reported ayanamsha behaves this way is not
established, and this project does not read its source to find out.

## Known gap in Vedaksha's own tool metadata

`compute_natal_chart`'s own tool description promises output "containing
planetary positions, house cusps, aspects, nakshatras, and dignities" —
the actual returned per-planet fields are `dignity, distance, house,
latitude, longitude, name, retrograde, sign, sign_index, speed`. No
nakshatra field anywhere, top-level or per-planet, despite the
description. The real per-planet nakshatra+pada value only appears via
`compute_panchanga` (Phase B). A nakshatra classification could be
computed from Vedaksha's own already-tested sidereal longitude using the
standard published 27-fold division, but that would mostly restate T1's
finer-grained longitude test except at classification-boundary cases, so
it isn't treated as a first-class tier.

## Comparison primitives

`compare.py` has five comparator shapes:

- **Longitude-delta** (T1/T1-tropical/T2, houses): a numeric arcsecond
  delta against pass/review/fail tolerance bands.
- **Rank-order** (karakas): agreement on an ordering, not a value.
- **Categorical** (combustion, drishti, bhavas): agreement on a discrete
  label/set, with the underlying numeric margin carried for context.
- **Date-boundary** (dasha, chara dasha): agreement on a sequence of
  `(lord/sign, start_jd, end_jd)` tuples, tolerance in days.
- **Bindu-count** (ashtakavarga): agreement on per-sign integer counts.

Koota (pairwise/compatibility) would need a sixth, once a matching
two-chart Vedaksha tool exists to test it against.

## Reproducing results

Every figure quoted anywhere in this file traces to a committed, unedited
raw run record under `results/canonical/` (see that directory's own
`README.md`) — never a hand-typed number. That directory's own note
states plainly what environment produced it (in particular: whether real
Swiss Ephemeris `.se1` data files were installed, since their absence
silently degrades Swiss comparisons to the Moshier analytical fallback —
see docs/oracles.md).

```python
import vedaksha
v = vedaksha.Vedaksha()
v.list_tools()                          # full tool inventory + input/output schemas
v.call_tool("compute_karakas", **args)  # etc.
```

Re-verifying a specific pinned version needs `pip install
--force-reinstall --no-cache-dir vedaksha==X.Y.Z`, not a plain `pip
install` — a pinned version number is not a safe proxy for "same wheel
content" for this dependency; it can be republished under an unchanged
tag, and a plain install may silently no-op against an already-installed,
possibly-stale copy.

## Adding a tier

1. Add the case kind to `cases.py` (sweep-based) and/or `birth_bank.py`
   (birth-bank-based) and/or a location-grid builder (Phase B).
2. Add the `Engine` method that calls the relevant Vedaksha tool.
3. Add the oracle-side `answer()` branch to whichever adapter(s) can
   honestly answer it — never all of them by default.
4. Add the comparator in `compare.py` if the existing ones don't fit —
   check the primitives above first; most new tiers need one of the five
   already identified, not a new one.
5. Register the tier in `cli.py`'s `TIER_BUILDERS`.
6. Update the "Currently implemented" table at the top of this file.
