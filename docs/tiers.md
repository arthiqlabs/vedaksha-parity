# Tiers — what this harness tests, and what it deliberately doesn't

Vedaksha's published package exposes 17 tools (`Vedaksha().list_tools()`).
This file inventories all 17, classifies each in or out of scope per
`CLAUDE.md`'s rule ("deterministic quantities only... interpretation is
out of scope"), and states current, reproducible results for every tier
that is built.

**Vedaksha version tested: `vedaksha==10.0.0`**, unless a result below
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
| T1-adversarial | sidereal position, adversarially-sampled instants | `position` | same oracles as T1 |
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

PyJHora's sidereal longitude has been observed to differ from Swiss
Ephemeris's by a small, stable, body-specific offset with both pinned to
the same Lahiri ayanamsha. That measurement is recorded in the adapter
(`pyjhora_oracle.py`'s module docstring) and is not part of the canonical
artifacts under `results/canonical/`, so no figure from it is quoted here.
A stable offset rules out a directly relabeled value, but is equally
consistent with the same underlying engine run with a different flag
(aberration, light-time correction): independence from Swiss Ephemeris
is not confirmed. Comparisons against PyJHora should be read with that
caveat; `settings()` in every PyJHora artifact records it.

### T1 / T1-tropical / T2 — sidereal and tropical position, ayanamsha

Against Swiss Ephemeris (`SwissephOracle(ayanamsha_mode="true")`, matching
Vedaksha's own true — mean plus nutation — ayanamsha convention), 200 real
birth records, 9 bodies each: **T1 sidereal position 1624 pass / 131
review / 0 fail / 45 engine_error; T1-tropical the same split; T2
ayanamsha 195 pass / 0 review / 0 fail / 5 engine_error.** Every
engine_error is one of the same 5 birth records, each outside Vedaksha's
supported date range (5 records × 9 bodies = 45). The count of 5 comes from
the sample, not the engine: the seed-42 draw of the unchanged birth bank
(`configs/all-tiers-200-birthbank-v2.yaml`) holds 5 records outside
`[JD 2378496.5, 2597641.5]`, where the seed-20260829 draw
(`configs/all-tiers-200-birthbank.yaml`) holds 2, and Vedaksha 9.1.0
refused exactly the same 5 Julian Days in this config. All 131 review
cases are TrueNode (TrueNode: 64 pass / 131 review; longitude delta mean
+0.07″, range −37.8″ to +32.2″), an inherently higher-variance,
perturbation-including quantity, not a distinct issue; every other body
passes on all 195 evaluable records. No `.se1` files were installed, so
these are Moshier-fallback Swiss Ephemeris positions; the backend tally in
these artifacts' oracle names is cumulative across tiers and counts MeanNode
under SWIEPH, so read it with `results/canonical/README.md`'s corrections.
`ayanamsha_mode` is `"mean"`-selectable too, for
comparing against a mean-only ayanamsha convention if that's ever needed;
`"true"` is the default and what the figures above use.

Reproduce: `vedaksha-parity run-config configs/all-tiers-200-birthbank-v2.yaml`

### T1-adversarial — same quantity as T1, deliberately hard instants

T1's uniform stride grid is reproducible, but a fixed step can
systematically undersample the numerically difficult regimes where a real
divergence is most likely to actually surface: station points,
perigee/apogee, longitude wraparound, same-instant conjunctions. Case kind
and comparators are identical to T1 — only case *selection* differs:
`build_cases_t1_adversarial` (`src/vedaksha_parity/pathological_cases.py`)
runs its own dense scan of Vedaksha's own output over the requested
`(from, to, step)` and flags instants directly from that output (a
speed-sign change, a local distance extremum, proximity to the 0/360
boundary, cross-body proximity) — never from a reference's internals, per
`FIREWALL.md` rule 1. `--step` here means scan density, not case spacing:
a smaller step is a more thorough (and slower) scan, not more output.

Not yet part of a committed canonical run — added as a second case source
alongside T1's grid, not yet exercised against a real oracle roster at
scale. Reproduce (once run): `vedaksha-parity run --tier t1-adversarial
--oracle swisseph --from <jd> --to <jd> --step <days>`.

### Karakas

PyJHora's `get_chara_karakas` against Vedaksha's `compute_karakas(scheme="8")`
(`Engine(karaka_scheme="8")`), 200 real birth records: **152 pass / 34
review / 9 fail / 5 engine_error.** A single adjacent-rank swap changes
two karaka titles at once, so this comparator's review threshold is 2
mismatches (`KARAKA_REVIEW_MISMATCH_MAX` in `config.py`), not the 1 used
elsewhere. All 34 review cases are a single adjacent-rank swap. The 9
fails are larger reorderings: 5 mismatch all eight titles, 1 mismatches
seven, and 3 mismatch three. In the six cases with seven or eight
mismatched titles, Vedaksha's own computed Rahu degree-in-sign sits
within 1.1° of a sign boundary, a boundary-sensitivity pattern; in the
three three-title cases it does not (it sits 1.4° to 14.5° from the
nearest boundary). The mechanism for either group is not established.

Reproduce: `vedaksha-parity run-config configs/all-tiers-200-birthbank-v2.yaml`

### Combustion

Against PyJHora, 200 real birth records (6 bodies: Moon, Mars, Mercury,
Jupiter, Venus, Saturn): **1,053 pass / 0 review / 117 fail / 30
engine_error** out of 1,200 cases (the 30 engine_errors are the same 5
out-of-range birth records as T1, × 6 bodies). The 117 fails split into
two categories. 69 are a documented granularity gap: Vedaksha reports
`DeeplyCombust` as a distinct state, PyJHora's states are binary
`Combust`/`None`; Mercury carries 30 of the 69. The other 48 are genuine
`Combust`/`None` disagreements. These sit in bands several degrees wide
next to Vedaksha's own stated orb for each body (its tool description
lists the orbs): Vedaksha `None`, PyJHora `Combust` for Mercury at 14.0°
to 16.8° from the Sun (29 cases), the Moon at 12.2° to 14.8° (6) and
Jupiter at 11.5° to 13.8° (3); Vedaksha `Combust`, PyJHora `None` for
Mars at 10.9° to 16.1° (6), Saturn at 11.3° to 12.3° (3) and Mercury at
6.8° (1). Bands degrees wide are far wider than the small longitude
offset noted above could account for; they are consistent with the two engines applying different
orbs, which this harness has not measured on the PyJHora side.

Reproduce: `vedaksha-parity run-config configs/all-tiers-200-birthbank-v2.yaml`

### Drishti

Against jyotishganit (`Engine(ayanamsha="TrueChitra")`), 200 real birth
records: **0 pass / 0 review / 154 fail / 46 oracle_unsupported**
(outside jyotishganit's own DE421-backed date range, 1899-07-29 to
2053-10-09). jyotishganit grades no aspect strength, so the comparator
reduces Vedaksha's aspects to its `Full` ones and compares the sets of
aspected signs only (`compared_strength: false` on every row). Every
failing case has exactly 6 mismatches, always confined to Rahu/Ketu: the
seven classical grahas agree on every evaluable chart. This is a
documented convention difference,
not an open question: Vedaksha treats the nodes as ordinary grahas for
aspect purposes (universal 7th aspect at full strength, graduated partial
strength at 3rd/4th/5th/8th/9th/10th); jyotishganit gives them
Jupiter-like special aspects instead (5th and 9th) and no 7th aspect at
all. Missing 7th × 2 nodes + extra {5th, 9th} × 2 nodes = 6, matching the
measured count exactly on every chart. In 152 of the 154 the two extra
signs are the 5th and 9th from Vedaksha's node sign; in the other 2 they
are the 4th and 8th, which is what the same rule gives if jyotishganit
places the nodes one sign earlier than Vedaksha does (inferred from the
aspect sets; the nodes' own signs were not compared in this run).

Reproduce: `vedaksha-parity run-config configs/all-tiers-200-birthbank-v2.yaml`

### Dasha (Vimshottari)

Against jyotishganit, 200 real birth records: **0 pass / 43 review / 111
fail / 46 oracle_unsupported** (the same out-of-range records as
Drishti). The lord sequence matches on all 154 evaluable cases. The
worst boundary-date delta per case runs from 0.35 to 3.84 days (median
1.58 days); against the provisional band (`dasha_start_delta_days`: pass
0.01 day, review 1 day) that puts the 43 cases between 0.35 and 0.98 days
in review and the 111 above 1 day in fail. The drift is a documented
convention difference, not an accuracy problem: Vedaksha uses the Julian
year (365.250000 days) for dasha-period arithmetic; jyotishganit uses the
sidereal year (365.256360 days). That gap accounts for the drift's
linear growth with elapsed time: a fit over all 1,386 matched period boundaries gives a
slope of −0.00645 days per year of elapsed time, against −0.00636 from
the year-length gap alone. The scatter about that fit (1.54-day standard
deviation) is not further isolated. The tolerance band is still the
provisional placeholder and has not been recalibrated against this
measured distribution, a real limitation of the current disposition
counts, not of the underlying comparison.

Reproduce: `vedaksha-parity run-config configs/all-tiers-200-birthbank-v2.yaml`

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
full set of aspected signs match between the two sides, and, when both
sides grade strength, each one's strength? Against a binary reference,
only the graded side's `Full` aspects are compared.

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
concentrated at higher-latitude/diaspora cities (London 10, Toronto 8,
New York 6) and mostly on the ascendant specifically (the worst of the 14
points in 34 of the 47), consistent with ordinary numerical precision at
the most latitude-sensitive point in a chart.

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
with an ascendant-sign disagreement: at those three instants and places
(Lucknow, Ahmedabad, Kolkata), the house-cusp run puts Vedaksha's
ascendant within 0.08° of a sign boundary. That run uses the
IndianOfficial ayanamsha and this one TrueChitra, so the 0.08° is
indicative, not this run's own margin.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`

### Ashtakavarga

Against jyotishganit's own per-sign bindu counts (Sarvashtakavarga
totals), same grid and sweep: **0 pass / 0 review / 928 fail / 2
oracle_error.** 925 of the 928 fails mismatch exactly two adjacent signs,
one by +1 bindu and the other by −1, so one bindu sits in a neighbouring
sign, and in all 925 jyotishganit's bindu is the one in the later sign of
the pair (Pisces to Aries in the 30 cases that wrap); the most frequent pairs (signs indexed 0 = Aries) are 1/2 (150
cases) and 10/11 (120 cases). The other 3 fails are the same three
charts as the Bhavas fails (Lucknow, Ahmedabad, Kolkata), with 10 or 11
signs mismatched by up to 6 bindus, consistent with the lagna sign
differing. In all 928 both sides total 337 bindus. Vedaksha's own tool
description states `compute_ashtakavarga` does not apply
Trikona/Ekadhipatya Shodhana or Pinda Sadhana corrections; since
jyotishganit's totals are equal to Vedaksha's, a reduction on its side
does not explain this pattern either. The cause of the one-bindu shift is
not established.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`

### Panchanga

Against jyotishganit's `tithi`/`nakshatra`/`yoga`/`karana`/`vara`, same
grid and sweep: **578 pass / 281 review / 69 fail / 2 oracle_error.**
Tithi never mismatches. Across the 350 review and fail cases, vara
mismatches in 223, yoga in 90, karana in 89 and nakshatra in 30. Vara
is the largest single source and depends on local sunrise (the same
location/timing sensitivity documented under house cusps); karana is the
narrowest limb (half a tithi). Why yoga and nakshatra disagree as often
as they do is not isolated here.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`

### Chara dasha

Against PyJHora's `chara.get_dhasa_antardhasa`
(`compare_sign_dasha` — sign sequence plus boundaries), full 30-city grid
at 31 instants (930 cases): **sign sequence matches 930/930 (100%)** —
starting sign and direction both agree at every one of the 12 lagna
categories. Disposition: **0 pass / 187 review / 743 fail.** Boundary
accuracy: median worst-boundary delta 730 days (~2 years); 187/930 cases
(20.1%) match to within 1 day; 202/930 (21.7%) are off by more than
1,000 days. The spread comes from period durations: 728 of the 930 cases
have at least one period whose length in whole years differs between the
two engines (1 to 7 such periods per case). Of the 2,033 differing
periods, 1,831 differ by exactly one year, 163 by two, and 39 by three to
eight. A difference that common and that large is not explained by a
small longitude offset; its cause is not established here.

Reproduce: `vedaksha-parity run-config configs/all-phase-b-tiers.yaml`
(no ayanamsha override needed — PyJHora is pinned to Lahiri, matching
Vedaksha's default `IndianOfficial`.)

### MeanNode sidereal drift against jyotishganit

Vedaksha's `TrueChitra`-sidereal MeanNode, compared against jyotishganit's
own MeanNode in the canonical T1 run (154 evaluable birth records, 153
fail / 1 pass), shows an apparent divergence of −50.40 arcsec/year
(linear fit of the longitude delta against time, |r| = 0.9999), close to
the standard general-precession rate (~50.29″/yr). The seven classical
grahas in the same run show no such trend (slopes from −0.022 to
−0.035″/yr), so the divergence is specific to the node.

A check of both engines' tropical mean node against a physical
reference (the Moon's osculating ascending node computed from DE440
state vectors, with a deliberately uncorrected J2000-frame control) is
not part of the canonical artifacts under `results/canonical/`, so no
figure or conclusion from it is quoted here.

jyotishganit's ayanamsha does not precess: its adapter records it as
fixed (`settings()` in every jyotishganit artifact, and
`jyotishganit_oracle.py`'s module docstring). A sidereal node computed
against a fixed ayanamsha would move at very nearly the tropical rate
rather than a precession-corrected sidereal rate, which is consistent
with a gap of about the general-precession rate. This is an output-level
reading of jyotishganit specifically; why its sidereal node behaves this
way while its planets do not is not established, and this project does
not read its source to find out.

## Nakshatra is not a natal-chart field

In `vedaksha==10.0.0`, `compute_natal_chart` returns per-planet fields
`dignity, distance, house, latitude, longitude, name, retrograde, sign,
sign_index, speed`, and no nakshatra field anywhere, top-level or
per-planet; its tool description does not list one either. The real
nakshatra+pada value only appears via `compute_panchanga` (Phase B). A nakshatra classification could be
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
