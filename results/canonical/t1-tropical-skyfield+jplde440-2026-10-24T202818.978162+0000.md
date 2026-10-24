# vedaksha-parity run report

**Tier:** `t1-tropical`  
**Engine:** Vedaksha 10.0.0  
**Oracle:** Skyfield + JPL DE440 skyfield 1.55 + de440.bsp  
**Generated:** 2026-10-24T20:28:18.978162+00:00  
**Python:** 3.14.8

## Case parameters

- **birth_bank:** source_size=15790, count=2000, seed=42, source=data/vedastro-15000-famous-births.csv

## Engine settings

| Setting | Value |
|---|---|
| ayanamsha | IndianOfficial |
| karaka_scheme | 7 |

## Oracle settings

| Setting | Value |
|---|---|
| kernel | vendor/kernels/de440.bsp |
| kernel_coverage | 1550-2650 (DE440) |
| delta_t_validity_window | ~1800-2100 (approximate calendar years) — see module docstring |
| frame | apparent geocentric ecliptic of date (epoch='date') |
| time_scale | case jd_ut treated as UT1 via Timescale.ut1_jd(); Skyfield applies its own UT1->TT->TDB tables internally |
| outer_planet_targets | Mars/Jupiter/Saturn answered from their DE440 system barycenter — no separate body-center segment exists in this kernel for them |
| speed | not provided |
| position | unsupported — DE440 is tropical-only; this harness's position case asks for sidereal. Answers tropical_position instead. |
| ayanamsha | unsupported — not an astronomical quantity; DE440 has no opinion on it |

## Results

18000 cases

| Disposition | Count | % |
|---|---|---|
| pass | 13832 | 76.8% |
| review | 0 | 0.0% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 4168 | 23.2% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| latitude_delta_arcsec | 13832 | 0.0192 | 0.0139 | 0.0284 | 0.0456 | 0.0661 | 0.0837 | 0.7879 |
| longitude_delta_arcsec | 13832 | 0.0299 | 0.0100 | 0.0573 | 0.0934 | 0.1321 | 0.2365 | 0.6947 |

### Oracle-unsupported reasons (4168)

| Reason | Count |
|---|---|
| Skyfield + DE440 adapter has no lunar-node data for 'MeanNode' — DE440 contains no lunar nodes | 1976 |
| Skyfield + DE440 adapter has no lunar-node data for 'TrueNode' — DE440 contains no lunar nodes | 1976 |
| jd_ut=2368785.921527778 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2371045.0881944443 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2343443.4381944444 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2356889.4291666667 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2373813.3173611113 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2377277.74375 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2373438.359027778 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2360583.410416667 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2373925.882638889 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2259865.5381944445 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2372825.1298611113 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2377998.11875 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2370811.709027778 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2378270.9520833334 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2372458.292361111 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2342601.6923611113 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2377232.55625 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2357424.163888889 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2372380.5597222224 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2377854.6923611113 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2365016.1298611113 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2360993.777777778 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2373320.952777778 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2349876.6256944444 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |

