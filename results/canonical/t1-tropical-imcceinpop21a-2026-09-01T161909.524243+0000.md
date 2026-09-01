# vedaksha-parity run report

**Tier:** `t1-tropical`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** IMCCE INPOP21a skyfield 1.55 + INPOP21a (inpop21a.bsp)  
**Generated:** 2026-09-01T16:19:09.524243+00:00  
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
| kernel | vendor/kernels/inpop21a.bsp |
| kernel_coverage | JD 2414105.0-2488985.0 (1897-06-30 to 2102-07-05) |
| frame | apparent geocentric ecliptic OF DATE (epoch='date') |
| time_scale | case jd_ut treated as UT1 via ts.ut1_jd(jd_ut) |
| planet_targets | all seven bodies answered from their SYSTEM BARYCENTER — this kernel carries no body-center segment for any of them |
| citation | A. Fienga et al., inpop21a planetary ephemerides, 2021 |
| position | unsupported — INPOP has no ayanamsha to derive a sidereal value from. Answers tropical_position instead. |
| ayanamsha | unsupported — a Jyotish construct, not an astronomical one |

## Results

1800 cases

| Disposition | Count | % |
|---|---|---|
| pass | 1085 | 60.3% |
| review | 0 | 0.0% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 715 | 39.7% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| latitude_delta_arcsec | 1085 | 0.0310 | 0.0303 | 0.0373 | 0.0526 | 0.0613 | 0.0787 | 0.2540 |
| longitude_delta_arcsec | 1085 | 0.1152 | 0.0915 | 0.1464 | 0.2029 | 0.2641 | 0.4970 | 0.8154 |

### Oracle-unsupported reasons (715)

| Reason | Count |
|---|---|
| IMCCE INPOP21a adapter has no body mapping for 'MeanNode' — this kernel carries no lunar nodes | 155 |
| IMCCE INPOP21a adapter has no body mapping for 'TrueNode' — this kernel carries no lunar nodes | 155 |
| IMCCE INPOP21a adapter: jd_ut=2411318.0243055555 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412291.871527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2401344.785416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2392437.4520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2391641.046527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2399043.546527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400263.0048611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2387419.5048611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2384758.0256944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409010.9736111113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406667.8958333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2388516.5770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405193.36875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2368785.921527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409034.4520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2401041.671527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408443.910416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2371045.0881944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2381702.8270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2399177.1770833335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407273.3541666665 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413238.9791666665 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407134.9520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2343443.4381944444 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2390920.99375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405638.8506944445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406353.829861111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2403672.202777778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409311.1923611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406971.4520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2387454.7020833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2414031.75 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405057.11875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2414003.4520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2356889.4291666667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405740.36875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413840.722916667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2392481.1958333333 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2399089.722916667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2401745.8270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400506.910416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411893.6006944445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2373813.3173611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405821.6319444445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2395469.948611111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |

