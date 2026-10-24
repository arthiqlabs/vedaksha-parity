# vedaksha-parity run report

**Tier:** `t1-tropical`  
**Engine:** Vedaksha 10.0.0  
**Oracle:** Astronomy Engine 2.1.19  
**Generated:** 2026-10-24T20:21:06.952725+00:00  
**Python:** 3.14.8

## Case parameters

- **birth_bank:** source_size=15790, count=200, seed=42, source=data/vedastro-15000-famous-births.csv

## Engine settings

| Setting | Value |
|---|---|
| ayanamsha | IndianOfficial |
| karaka_scheme | 7 |

## Oracle settings

| Setting | Value |
|---|---|
| provenance | truncated VSOP87 + NOVAS C 3.1, no external ephemeris dependencies of any kind — no swisseph, no JPL kernels, no data files (published documentation; never read from source) |
| frame | GeoVector(aberration=True) -> Ecliptic() = apparent geocentric ecliptic of date, tropical |
| stated_accuracy | approximately 1 arcminute (published documentation) |
| position | unsupported — this library is tropical-only; this harness's position case asks for sidereal. Answers tropical_position instead. |
| ayanamsha | unsupported — not an astronomical quantity this library exposes |
| nodes | unsupported — no lunar-node body in this library's interface |
| speed | not provided — no angular-rate quantity exposed by this interface |

## Results

1800 cases

| Disposition | Count | % |
|---|---|---|
| pass | 1156 | 64.2% |
| review | 209 | 11.6% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 400 | 22.2% |
| oracle_error | 0 | 0.0% |
| engine_error | 35 | 1.9% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| distance_delta_au | 1365 | 0.0000 | 0.0000 | 0.0001 | 0.0002 | 0.0003 | 0.0005 | 0.0006 |
| latitude_delta_arcsec | 1365 | 1.9907 | 0.8586 | 3.6658 | 4.8525 | 8.1298 | 16.3682 | 21.1483 |
| longitude_delta_arcsec | 1365 | 1.9013 | 1.3184 | 2.6672 | 4.5465 | 5.6684 | 8.4537 | 12.8145 |

### Oracle-unsupported reasons (400)

| Reason | Count |
|---|---|
| Astronomy Engine adapter has no body mapping for 'MeanNode' — it answers ['Jupiter', 'Mars', 'Mercury', 'Moon', 'Saturn', 'Sun', 'Venus'] only; it has no lunar-node body in its interface | 200 |
| Astronomy Engine adapter has no body mapping for 'TrueNode' — it answers ['Jupiter', 'Mars', 'Mercury', 'Moon', 'Saturn', 'Sun', 'Venus'] only; it has no lunar-node body in its interface | 200 |

### Engine-error reasons (35)

| Reason | Count |
|---|---|
| ToolError('[-32602] Julian Day 2368785.921527778 is outside valid range [2378496.5, 2597641.5]') | 7 |
| ToolError('[-32602] Julian Day 2371045.0881944443 is outside valid range [2378496.5, 2597641.5]') | 7 |
| ToolError('[-32602] Julian Day 2343443.4381944444 is outside valid range [2378496.5, 2597641.5]') | 7 |
| ToolError('[-32602] Julian Day 2356889.4291666667 is outside valid range [2378496.5, 2597641.5]') | 7 |
| ToolError('[-32602] Julian Day 2373813.3173611113 is outside valid range [2378496.5, 2597641.5]') | 7 |

