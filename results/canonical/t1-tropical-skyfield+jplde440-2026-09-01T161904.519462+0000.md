# vedaksha-parity run report

**Tier:** `t1-tropical`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** Skyfield + JPL DE440 skyfield 1.55 + de440.bsp  
**Generated:** 2026-09-01T16:19:04.519462+00:00  
**Python:** 3.14.6

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

1800 cases

| Disposition | Count | % |
|---|---|---|
| pass | 1365 | 75.8% |
| review | 0 | 0.0% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 435 | 24.2% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| latitude_delta_arcsec | 1365 | 0.0313 | 0.0300 | 0.0387 | 0.0530 | 0.0635 | 0.1208 | 0.2540 |
| longitude_delta_arcsec | 1365 | 0.1324 | 0.0881 | 0.2349 | 0.2076 | 0.3714 | 1.1230 | 2.1677 |

### Oracle-unsupported reasons (435)

| Reason | Count |
|---|---|
| Skyfield + DE440 adapter has no lunar-node data for 'MeanNode' — DE440 contains no lunar nodes | 195 |
| Skyfield + DE440 adapter has no lunar-node data for 'TrueNode' — DE440 contains no lunar nodes | 195 |
| jd_ut=2368785.921527778 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2371045.0881944443 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2343443.4381944444 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2356889.4291666667 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |
| jd_ut=2373813.3173611113 is outside this adapter's delta-T validity window (2378495.0-2488070.0, ~1800-2100) — see module docstring | 9 |

