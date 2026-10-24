# vedaksha-parity run report

**Tier:** `t1-tropical`  
**Engine:** Vedaksha 10.0.0  
**Oracle:** IMCCE INPOP21a skyfield 1.55 + INPOP21a (inpop21a.bsp)  
**Generated:** 2026-10-24T20:28:48.101672+00:00  
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
| kernel | vendor/kernels/inpop21a.bsp |
| kernel_coverage | JD 2414105.0-2488985.0 (1897-06-30 to 2102-07-05) |
| frame | apparent geocentric ecliptic OF DATE (epoch='date') |
| time_scale | case jd_ut treated as UT1 via ts.ut1_jd(jd_ut) |
| planet_targets | all seven bodies answered from their SYSTEM BARYCENTER — this kernel carries no body-center segment for any of them |
| citation | A. Fienga et al., inpop21a planetary ephemerides, 2021 |
| position | unsupported — INPOP has no ayanamsha to derive a sidereal value from. Answers tropical_position instead. |
| ayanamsha | unsupported — a Jyotish construct, not an astronomical one |

## Results

18000 cases

| Disposition | Count | % |
|---|---|---|
| pass | 11788 | 65.5% |
| review | 0 | 0.0% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 6212 | 34.5% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| latitude_delta_arcsec | 11788 | 0.0191 | 0.0139 | 0.0286 | 0.0453 | 0.0658 | 0.0828 | 0.7884 |
| longitude_delta_arcsec | 11788 | 0.0251 | 0.0078 | 0.0510 | 0.0858 | 0.1159 | 0.1952 | 0.6956 |

### Oracle-unsupported reasons (6212)

| Reason | Count |
|---|---|
| IMCCE INPOP21a adapter has no body mapping for 'MeanNode' — this kernel carries no lunar nodes | 1684 |
| IMCCE INPOP21a adapter has no body mapping for 'TrueNode' — this kernel carries no lunar nodes | 1684 |
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
| IMCCE INPOP21a adapter: jd_ut=2390920.5048611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409622.05 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411113.2256944445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409385.2756944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405075.065972222 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2385595.61875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412690.9520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405235.279166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406429.1125 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400544.0069444445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2404703.904166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2398825.7916666665 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2379076.61875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411447.984722222 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2392487.0770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413474.095138889 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411199.8270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2388886.8270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2403799.74375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407114.984027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2384026.8208333333 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408845.0770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413787.4520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2382492.9520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406072.8381944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411868.2236111113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410277.654166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413261.6354166665 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2391945.6298611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2388550.410416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413555.3958333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2395051.3270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2388760.99375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2377277.74375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2396021.9520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2397588.154166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413348.8333333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2389592.61875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405654.925 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412665.68125 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405236.609027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410417.173611111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2396507.7756944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2403880.8270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2379866.660416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2378704.99375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406573.8270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409854.9375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2401117.910416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400984.410416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405652.0770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406674.785416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2387960.285416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411733.1923611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407982.25 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2373438.359027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2360583.410416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393862.035416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2391771.0256944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407254.986111111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400524.296527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410918.796527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406331.3270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413934.3333333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413069.21875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413036.827777778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2373925.882638889 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2395336.5256944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412895.1395833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2397942.9458333333 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2383630.6298611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2402436.2548611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407765.590277778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409380.625 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2399570.3625 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412261.7548611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2401491.601388889 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2259865.5381944445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2391569.404166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393253.684027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409278.5069444445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407753.8798611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2372825.1298611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2390288.2548611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410398.535416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412781.6770833335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412346.0770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407652.0881944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408601.3381944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2404392.160416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411667.9444444445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2404234.4520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407090.1041666665 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413828.1666666665 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400186.704861111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409580.5048611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408379.4791666665 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2403268.171527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407407.160416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411035.86875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413999.1333333333 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2389172.61875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2402444.3381944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2403780.9520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393892.535416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409140.109027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409976.24375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2399282.7861111113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411459.5694444445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410418.7131944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407011.2756944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413476.3625 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409162.61875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2389338.1819444443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393091.61875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2383937.4736111113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409417.535416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408201.785416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408159.109027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2388933.74375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2382588.484027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408224.0881944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407849.6506944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413017.7291666665 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2388688.36875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2390068.160416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409749.3270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393912.785416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2379366.796527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393550.6298611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2394672.785416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2389847.86875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412167.1506944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408173.6319444445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410505.722916667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409662.423611111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411439.8381944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2404798.984027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2389426.61875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413031.7083333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410015.5881944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410176.785416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411767.785416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408439.509722222 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2378626.4520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407940.6875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409684.3680555555 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408788.734027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410629.7020833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2396072.410416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2382053.285416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408710.546527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2402827.298611111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413981.285416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393187.5145833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413541.9520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409779.99375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413637.222916667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2405999.734027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2398008.2430555555 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2413919.8020833335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409655.74375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2395759.546527778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2404892.9520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393937.654166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2402284.5256944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406849.275 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2403492.4423611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2391553.660416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2404903.1923611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2403113.9375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406442.8798611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2377998.11875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400806.535416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406045.890277778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2394778.785416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2398784.8270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412466.74375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411869.660416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411903.923611111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2399855.74375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412497.6125 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411414.2548611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409453.7020833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411301.0770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411879.3270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412321.8958333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410407.6611111113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2389883.1298611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2382188.74375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412958.216666667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2370811.709027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409416.24375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2401070.404166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410687.86875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406645.779166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2383661.99375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2378270.9520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2404791.2083333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406152.3381944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2386313.222916667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2379357.785416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409949.076388889 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2384534.86875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2404887.7020833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409270.93125 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407751.316666667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412548.472222222 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2401227.93125 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2372458.292361111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2385896.660416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2389120.7548611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2342601.6923611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2397141.779166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408565.4520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2387936.910416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2379639.24375 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2403533.0069444445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2377232.55625 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2357424.163888889 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2401408.8270833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406945.43125 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2372380.5597222224 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2384788.11875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2404702.3819444445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2377854.6923611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400504.029166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393095.5909722224 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2389919.904166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2365016.1298611113 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2390292.9895833335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408301.2131944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2360993.777777778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409171.109027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2385139.86875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407953.673611111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408298.5833333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2392635.6333333333 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2392090.4659722224 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2373320.952777778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2399849.0208333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2409972.5770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2412655.513888889 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2385688.5770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408846.0208333335 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2381658.7131944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411368.535416667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410247.048611111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2393491.86875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2396976.11875 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2403482.7020833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2382871.984027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2349876.6256944444 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407979.309027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2380933.0770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2402303.3625 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2388294.173611111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408966.90625 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400055.6125 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2406906.1125 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2410681.2020833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2407824.5770833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2408246.8381944443 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2401873.40625 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2388589.109027778 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2385214.538888889 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2396073.529166667 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2411445.43125 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2400399.9520833334 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2382370.204861111 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |
| IMCCE INPOP21a adapter: jd_ut=2395395.6319444445 is outside the shipped kernel's span (2414105.0-2488985.0) | 9 |

