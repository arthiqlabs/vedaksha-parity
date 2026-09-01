# vedaksha-parity run report

**Tier:** `drishti`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** jyotishganit 0.1.3  
**Generated:** 2026-09-01T16:19:38.483484+00:00  
**Python:** 3.14.6

## Case parameters

- **birth_bank:** source_size=15790, count=200, seed=42, source=data/vedastro-15000-famous-births.csv
- **ayanamsha_override:** TrueChitra

## Engine settings

| Setting | Value |
|---|---|
| ayanamsha | TrueChitra |
| karaka_scheme | 7 |

## Oracle settings

| Setting | Value |
|---|---|
| ayanamsha | true_chitrapaksha, fixed, does not precess — see module docstring |
| node_type | MEAN node only ('Rahu') — TrueNode cases raise |
| date_range | 1899-07-29 to 2053-10-09 (DE421 span) — raises OracleUnsupported outside it |
| location | synthetic/neutral (0.0 deg, 0.0 deg) — every quantity this adapter exposes is geocentric |
| dasha | Vimshottari only — calculate_birth_chart has no system parameter |
| drishti | Binary special-aspect model, no strength gradation; sign-based, location-independent |
| vargas | d2/d3/d4/d7/d9/d10/d12/d16/d20/d24/d27/d30/d40/d45/d60 — no D1, D5, D6, D8, D11 |
| bhavas | 'Trik' (6/8/12) maps to is_dusthana — not 'Trikona' (1/5/9), a different label |
| ashtakavarga | Sarvashtakavarga only — Bhinna per-planet tables not read |
| panchanga | Plain names only, no pada/kalam/degrees-remaining; real location required |

## Results

200 cases

| Disposition | Count | % |
|---|---|---|
| pass | 0 | 0.0% |
| review | 0 | 0.0% |
| fail | 154 | 77.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 46 | 23.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Failures (154)

| Case | Comparison |
|---|---|
| kind=drishti, jd_ut=2437779.85 | compared_strength=False, missing_in_oracle=["('Ketu', 3)", "('Rahu', 9)"], extra_in_oracle=["('Ketu', 1)", "('Ketu', 5)", "('Rahu', 11)", "('Rahu', 7)"] |
| kind=drishti, jd_ut=2437293.826388889 | compared_strength=False, missing_in_oracle=["('Ketu', 4)", "('Rahu', 10)"], extra_in_oracle=["('Ketu', 2)", "('Ketu', 6)", "('Rahu', 0)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2439430.6354166665 | compared_strength=False, missing_in_oracle=["('Ketu', 0)", "('Rahu', 6)"], extra_in_oracle=["('Ketu', 10)", "('Ketu', 2)", "('Rahu', 4)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2436655.667361111 | compared_strength=False, missing_in_oracle=["('Ketu', 5)", "('Rahu', 11)"], extra_in_oracle=["('Ketu', 3)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2423148.3958333335 | compared_strength=False, missing_in_oracle=["('Ketu', 5)", "('Rahu', 11)"], extra_in_oracle=["('Ketu', 3)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2425450.3680555555 | compared_strength=False, missing_in_oracle=["('Ketu', 1)", "('Rahu', 7)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 3)", "('Rahu', 5)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2427159.1666666665 | compared_strength=False, missing_in_oracle=["('Ketu', 10)", "('Rahu', 4)"], extra_in_oracle=["('Ketu', 0)", "('Ketu', 8)", "('Rahu', 2)", "('Rahu', 6)"] |
| kind=drishti, jd_ut=2424214.4583333335 | compared_strength=False, missing_in_oracle=["('Ketu', 3)", "('Rahu', 9)"], extra_in_oracle=["('Ketu', 1)", "('Ketu', 5)", "('Rahu', 11)", "('Rahu', 7)"] |
| kind=drishti, jd_ut=2427549.1569444444 | compared_strength=False, missing_in_oracle=["('Ketu', 9)", "('Rahu', 3)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 5)"] |
| kind=drishti, jd_ut=2425935.888888889 | compared_strength=False, missing_in_oracle=["('Ketu', 0)", "('Rahu', 6)"], extra_in_oracle=["('Ketu', 10)", "('Ketu', 2)", "('Rahu', 4)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2449336.0694444445 | compared_strength=False, missing_in_oracle=["('Ketu', 7)", "('Rahu', 1)"], extra_in_oracle=["('Ketu', 5)", "('Ketu', 9)", "('Rahu', 11)", "('Rahu', 3)"] |
| kind=drishti, jd_ut=2427112.59375 | compared_strength=False, missing_in_oracle=["('Ketu', 10)", "('Rahu', 4)"], extra_in_oracle=["('Ketu', 0)", "('Ketu', 8)", "('Rahu', 2)", "('Rahu', 6)"] |
| kind=drishti, jd_ut=2420900.1666666665 | compared_strength=False, missing_in_oracle=["('Ketu', 9)", "('Rahu', 3)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 5)"] |
| kind=drishti, jd_ut=2423425.25 | compared_strength=False, missing_in_oracle=["('Ketu', 5)", "('Rahu', 11)"], extra_in_oracle=["('Ketu', 3)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2426510.6631944445 | compared_strength=False, missing_in_oracle=["('Ketu', 11)", "('Rahu', 5)"], extra_in_oracle=["('Ketu', 1)", "('Ketu', 9)", "('Rahu', 3)", "('Rahu', 7)"] |
| kind=drishti, jd_ut=2431960.7805555556 | compared_strength=False, missing_in_oracle=["('Ketu', 1)", "('Rahu', 7)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 3)", "('Rahu', 5)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2442215.3229166665 | compared_strength=False, missing_in_oracle=["('Ketu', 7)", "('Rahu', 1)"], extra_in_oracle=["('Ketu', 5)", "('Ketu', 9)", "('Rahu', 11)", "('Rahu', 3)"] |
| kind=drishti, jd_ut=2447991.18125 | compared_strength=False, missing_in_oracle=["('Ketu', 9)", "('Rahu', 3)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 5)"] |
| kind=drishti, jd_ut=2418673.954861111 | compared_strength=False, missing_in_oracle=["('Ketu', 1)", "('Rahu', 7)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 3)", "('Rahu', 5)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2439706.236111111 | compared_strength=False, missing_in_oracle=["('Ketu', 0)", "('Rahu', 6)"], extra_in_oracle=["('Ketu', 10)", "('Ketu', 2)", "('Rahu', 4)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2427430.96875 | compared_strength=False, missing_in_oracle=["('Ketu', 9)", "('Rahu', 3)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 5)"] |
| kind=drishti, jd_ut=2430185.3333333335 | compared_strength=False, missing_in_oracle=["('Ketu', 5)", "('Rahu', 11)"], extra_in_oracle=["('Ketu', 3)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2427329.8958333335 | compared_strength=False, missing_in_oracle=["('Ketu', 10)", "('Rahu', 4)"], extra_in_oracle=["('Ketu', 0)", "('Ketu', 8)", "('Rahu', 2)", "('Rahu', 6)"] |
| kind=drishti, jd_ut=2447009.290972222 | compared_strength=False, missing_in_oracle=["('Ketu', 11)", "('Rahu', 5)"], extra_in_oracle=["('Ketu', 1)", "('Ketu', 9)", "('Rahu', 3)", "('Rahu', 7)"] |
| kind=drishti, jd_ut=2425779.6305555557 | compared_strength=False, missing_in_oracle=["('Ketu', 0)", "('Rahu', 6)"], extra_in_oracle=["('Ketu', 10)", "('Ketu', 2)", "('Rahu', 4)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2431283.0069444445 | compared_strength=False, missing_in_oracle=["('Ketu', 3)", "('Rahu', 9)"], extra_in_oracle=["('Ketu', 1)", "('Ketu', 5)", "('Rahu', 11)", "('Rahu', 7)"] |
| kind=drishti, jd_ut=2430382.9444444445 | compared_strength=False, missing_in_oracle=["('Ketu', 4)", "('Rahu', 10)"], extra_in_oracle=["('Ketu', 2)", "('Ketu', 6)", "('Rahu', 0)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2430120.3229166665 | compared_strength=False, missing_in_oracle=["('Ketu', 5)", "('Rahu', 11)"], extra_in_oracle=["('Ketu', 3)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2430325.09375 | compared_strength=False, missing_in_oracle=["('Ketu', 4)", "('Rahu', 10)"], extra_in_oracle=["('Ketu', 2)", "('Ketu', 6)", "('Rahu', 0)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2427004.972222222 | compared_strength=False, missing_in_oracle=["('Ketu', 10)", "('Rahu', 4)"], extra_in_oracle=["('Ketu', 0)", "('Ketu', 8)", "('Rahu', 2)", "('Rahu', 6)"] |
| kind=drishti, jd_ut=2422580.673611111 | compared_strength=False, missing_in_oracle=["('Ketu', 6)", "('Rahu', 0)"], extra_in_oracle=["('Ketu', 4)", "('Ketu', 8)", "('Rahu', 10)", "('Rahu', 2)"] |
| kind=drishti, jd_ut=2423022.6666666665 | compared_strength=False, missing_in_oracle=["('Ketu', 5)", "('Rahu', 11)"], extra_in_oracle=["('Ketu', 3)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2418301.159722222 | compared_strength=False, missing_in_oracle=["('Ketu', 2)", "('Rahu', 8)"], extra_in_oracle=["('Ketu', 0)", "('Ketu', 4)", "('Rahu', 10)", "('Rahu', 6)"] |
| kind=drishti, jd_ut=2430842.6666666665 | compared_strength=False, missing_in_oracle=["('Ketu', 3)", "('Rahu', 9)"], extra_in_oracle=["('Ketu', 1)", "('Ketu', 5)", "('Rahu', 11)", "('Rahu', 7)"] |
| kind=drishti, jd_ut=2440923.7708333335 | compared_strength=False, missing_in_oracle=["('Ketu', 10)", "('Rahu', 4)"], extra_in_oracle=["('Ketu', 0)", "('Ketu', 8)", "('Rahu', 2)", "('Rahu', 6)"] |
| kind=drishti, jd_ut=2431992.0416666665 | compared_strength=False, missing_in_oracle=["('Ketu', 1)", "('Rahu', 7)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 3)", "('Rahu', 5)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2423912.548611111 | compared_strength=False, missing_in_oracle=["('Ketu', 4)", "('Rahu', 10)"], extra_in_oracle=["('Ketu', 2)", "('Ketu', 6)", "('Rahu', 0)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2418481.3625 | compared_strength=False, missing_in_oracle=["('Ketu', 1)", "('Rahu', 7)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 3)", "('Rahu', 5)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2425703.423611111 | compared_strength=False, missing_in_oracle=["('Ketu', 1)", "('Rahu', 7)"], extra_in_oracle=["('Ketu', 10)", "('Ketu', 2)", "('Rahu', 4)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2434675.3541666665 | compared_strength=False, missing_in_oracle=["('Ketu', 9)", "('Rahu', 3)"], extra_in_oracle=["('Ketu', 11)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 5)"] |
| kind=drishti, jd_ut=2423393.0833333335 | compared_strength=False, missing_in_oracle=["('Ketu', 5)", "('Rahu', 11)"], extra_in_oracle=["('Ketu', 3)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 9)"] |
| kind=drishti, jd_ut=2429093.3125 | compared_strength=False, missing_in_oracle=["('Ketu', 7)", "('Rahu', 1)"], extra_in_oracle=["('Ketu', 5)", "('Ketu', 9)", "('Rahu', 11)", "('Rahu', 3)"] |
| kind=drishti, jd_ut=2424301.9583333335 | compared_strength=False, missing_in_oracle=["('Ketu', 3)", "('Rahu', 9)"], extra_in_oracle=["('Ketu', 1)", "('Ketu', 5)", "('Rahu', 11)", "('Rahu', 7)"] |
| kind=drishti, jd_ut=2428819.625 | compared_strength=False, missing_in_oracle=["('Ketu', 7)", "('Rahu', 1)"], extra_in_oracle=["('Ketu', 5)", "('Ketu', 9)", "('Rahu', 11)", "('Rahu', 3)"] |
| kind=drishti, jd_ut=2420463.25 | compared_strength=False, missing_in_oracle=["('Ketu', 10)", "('Rahu', 4)"], extra_in_oracle=["('Ketu', 0)", "('Ketu', 8)", "('Rahu', 2)", "('Rahu', 6)"] |
| kind=drishti, jd_ut=2424389.9166666665 | compared_strength=False, missing_in_oracle=["('Ketu', 3)", "('Rahu', 9)"], extra_in_oracle=["('Ketu', 1)", "('Ketu', 5)", "('Rahu', 11)", "('Rahu', 7)"] |
| kind=drishti, jd_ut=2432887.7708333335 | compared_strength=False, missing_in_oracle=["('Ketu', 0)", "('Rahu', 6)"], extra_in_oracle=["('Ketu', 10)", "('Ketu', 2)", "('Rahu', 4)", "('Rahu', 8)"] |
| kind=drishti, jd_ut=2424469.1041666665 | compared_strength=False, missing_in_oracle=["('Ketu', 3)", "('Rahu', 9)"], extra_in_oracle=["('Ketu', 1)", "('Ketu', 5)", "('Rahu', 11)", "('Rahu', 7)"] |
| kind=drishti, jd_ut=2440959.923611111 | compared_strength=False, missing_in_oracle=["('Ketu', 10)", "('Rahu', 4)"], extra_in_oracle=["('Ketu', 0)", "('Ketu', 8)", "('Rahu', 2)", "('Rahu', 6)"] |
| kind=drishti, jd_ut=2416541.5770833334 | compared_strength=False, missing_in_oracle=["('Ketu', 5)", "('Rahu', 11)"], extra_in_oracle=["('Ketu', 3)", "('Ketu', 7)", "('Rahu', 1)", "('Rahu', 9)"] |

...and 104 more — see the JSON report for the complete set.

### Oracle-unsupported reasons (46)

| Reason | Count |
|---|---|
| jd=2411318.0243055555 (utc 1889-11-11 12:34:13.945546) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2412291.871527778 (utc 1892-07-12 08:54:13.272055) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2401344.785416667 (utc 1862-07-23 06:50:26.819746) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2392437.4520833334 (utc 1838-03-03 22:50:25.615700) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2391641.046527778 (utc 1835-12-28 13:06:26.050399) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2399043.546527778 (utc 1856-04-04 01:06:27.924069) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2400263.0048611113 (utc 1859-08-06 12:06:26.917480) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2387419.5048611113 (utc 1824-06-07 00:06:32.320841) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2384758.0256944443 (utc 1817-02-22 12:36:34.481871) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2409010.9736111113 (utc 1883-07-19 11:21:13.540397) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2406667.8958333335 (utc 1877-02-17 09:29:15.748697) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2388516.5770833334 (utc 1827-06-09 01:50:30.299941) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2405193.36875 (utc 1873-02-03 20:50:17.661181) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2368785.921527778 (utc 1773-05-31 10:06:38.869224) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2409034.4520833334 (utc 1883-08-11 22:50:13.529994) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2401041.671527778 (utc 1861-09-23 04:06:26.822332) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2408443.910416667 (utc 1881-12-29 09:50:13.910490) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2371045.0881944443 (utc 1779-08-07 14:06:39.225990) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2381702.8270833334 (utc 1808-10-12 07:50:33.556578) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2399177.1770833335 (utc 1856-08-15 16:14:27.816283) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2407273.3541666665 (utc 1878-10-15 20:29:15.073229) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2413238.9791666665 (utc 1895-02-14 11:29:12.804240) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2407134.9520833334 (utc 1878-05-30 10:50:15.223832) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2343443.4381944444 (utc 1704-01-11 22:30:31.071594) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2390920.99375 (utc 1834-01-07 11:50:26.670098) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2405638.8506944445 (utc 1874-04-25 08:24:17.014884) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2406353.829861111 (utc 1876-04-09 07:54:16.117509) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2403672.202777778 (utc 1868-12-05 16:51:21.493115) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2409311.1923611113 (utc 1884-05-14 16:36:13.443492) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2406971.4520833334 (utc 1877-12-17 22:50:15.404554) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2387454.7020833334 (utc 1824-07-12 04:50:32.260138) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2414031.75 (utc 1897-04-17 05:59:13.498797) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2405057.11875 (utc 1872-09-20 14:50:17.886377) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2414003.4520833334 (utc 1897-03-19 22:50:13.455046) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2356889.4291666667 (utc 1740-11-03 22:17:32.699761) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2405740.36875 (utc 1874-08-04 20:50:16.881195) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2414217.4895833335 (utc 1897-10-19 23:44:13.819327) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2413840.722916667 (utc 1896-10-08 05:20:13.230013) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2392481.1958333333 (utc 1838-04-16 16:41:25.599340) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2399089.722916667 (utc 1856-05-20 05:20:27.888136) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2401745.8270833334 (utc 1863-08-28 07:50:26.676337) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2400506.910416667 (utc 1860-04-06 09:50:26.830730) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2411893.6006944445 (utc 1891-06-10 02:24:13.618448) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2373813.3173611113 (utc 1787-03-06 19:36:38.950381) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2405821.6319444445 (utc 1874-10-25 03:09:16.776416) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |
| jd=2395469.948611111 (utc 1846-06-22 10:45:26.148642) is outside jyotishganit's date range (1899-07-29 to 2053-10-09 (DE421 span)): ephemeris segment only covers dates 1899-07-29 through 2053-10-09 | 1 |

