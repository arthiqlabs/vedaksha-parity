# vedaksha-parity run report

**Tier:** `t2`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** Swiss Ephemeris (mixed backends: {'MOSEPH': 3200, 'SWIEPH': 400}) 2.10.03  
**Generated:** 2026-09-01T16:18:58.127851+00:00  
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
| backends_used | {'MOSEPH': 3200, 'SWIEPH': 400} |

## Results

200 cases

| Disposition | Count | % |
|---|---|---|
| pass | 195 | 97.5% |
| review | 0 | 0.0% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 0 | 0.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 5 | 2.5% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| delta_arcsec | 195 | 0.0024 | 0.0022 | 0.0029 | 0.0047 | 0.0054 | 0.0059 | 0.0072 |

### Engine-error reasons (5)

| Reason | Count |
|---|---|
| ToolError('[-32602] Julian Day 2368785.921527778 is outside valid range [2378496.5, 2597641.5]') | 1 |
| ToolError('[-32602] Julian Day 2371045.0881944443 is outside valid range [2378496.5, 2597641.5]') | 1 |
| ToolError('[-32602] Julian Day 2343443.4381944444 is outside valid range [2378496.5, 2597641.5]') | 1 |
| ToolError('[-32602] Julian Day 2356889.4291666667 is outside valid range [2378496.5, 2597641.5]') | 1 |
| ToolError('[-32602] Julian Day 2373813.3173611113 is outside valid range [2378496.5, 2597641.5]') | 1 |

