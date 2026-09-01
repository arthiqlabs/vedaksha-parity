# vedaksha-parity run report

**Tier:** `t1`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** Swiss Ephemeris (mixed backends: {'MOSEPH': 1600, 'SWIEPH': 200}) 2.10.03  
**Generated:** 2026-09-01T16:18:50.035475+00:00  
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
| sidereal_mode | SIDM_LAHIRI |
| ayanamsha_mode | true |
| flags | FLG_SIDEREAL \| FLG_SPEED, FLG_SWIEPH requested |
| require_swieph | False |
| backends_used | {'MOSEPH': 1600, 'SWIEPH': 200} |

## Results

1800 cases

| Disposition | Count | % |
|---|---|---|
| pass | 1624 | 90.2% |
| review | 131 | 7.3% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 0 | 0.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 45 | 2.5% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| distance_delta_au | 1755 | 0.0007 | 0.0001 | 0.0012 | 0.0026 | 0.0026 | 0.0027 | 0.0028 |
| latitude_delta_arcsec | 1755 | 0.0770 | 0.0272 | 0.1909 | 0.1527 | 0.4102 | 0.9041 | 1.8337 |
| longitude_delta_arcsec | 1755 | 1.1977 | 0.1133 | 3.8844 | 1.9386 | 9.1953 | 19.8408 | 37.8328 |
| speed_delta_deg_per_day | 1755 | 0.0005 | 0.0001 | 0.0014 | 0.0020 | 0.0032 | 0.0065 | 0.0107 |

### Engine-error reasons (45)

| Reason | Count |
|---|---|
| ToolError('[-32602] Julian Day 2368785.921527778 is outside valid range [2378496.5, 2597641.5]') | 9 |
| ToolError('[-32602] Julian Day 2371045.0881944443 is outside valid range [2378496.5, 2597641.5]') | 9 |
| ToolError('[-32602] Julian Day 2343443.4381944444 is outside valid range [2378496.5, 2597641.5]') | 9 |
| ToolError('[-32602] Julian Day 2356889.4291666667 is outside valid range [2378496.5, 2597641.5]') | 9 |
| ToolError('[-32602] Julian Day 2373813.3173611113 is outside valid range [2378496.5, 2597641.5]') | 9 |

