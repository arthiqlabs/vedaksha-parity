# vedaksha-parity run report

**Tier:** `houses`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** Swiss Ephemeris (backend not yet determined — no cases run) 2.10.03  
**Generated:** 2026-09-01T16:20:13.786475+00:00  
**Python:** 3.14.6

## Case parameters

- **sweep:** from=2451545.0, to=2453365.0, step_days=60.0

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
| backends_used | no cases run yet |

## Results

930 cases

| Disposition | Count | % |
|---|---|---|
| pass | 883 | 94.9% |
| review | 47 | 5.1% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 0 | 0.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| worst_delta_arcsec | 930 | 1.7529 | 1.2996 | 2.4574 | 4.0457 | 5.0065 | 7.7048 | 14.2055 |

