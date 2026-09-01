# vedaksha-parity run report

**Tier:** `dasha`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** jyotishganit 0.1.3  
**Generated:** 2026-09-01T16:19:39.165308+00:00  
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
| review | 44 | 22.0% |
| fail | 110 | 55.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 46 | 23.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| max_boundary_delta_days | 154 | 1.6903 | 1.5628 | 1.9100 | 2.9712 | 3.2538 | 3.6236 | 3.8529 |

### Failures (110)

| Case | Comparison |
|---|---|
| kind=dasha, jd_ut=2437779.85 | lord_sequence_match=True, max_boundary_delta_days=3.852909527719021 |
| kind=dasha, jd_ut=2437293.826388889 | lord_sequence_match=True, max_boundary_delta_days=1.1263783699832857 |
| kind=dasha, jd_ut=2439430.6354166665 | lord_sequence_match=True, max_boundary_delta_days=1.457083048298955 |
| kind=dasha, jd_ut=2436655.667361111 | lord_sequence_match=True, max_boundary_delta_days=2.9788458147086203 |
| kind=dasha, jd_ut=2423148.3958333335 | lord_sequence_match=True, max_boundary_delta_days=1.75567108951509 |
| kind=dasha, jd_ut=2427159.1666666665 | lord_sequence_match=True, max_boundary_delta_days=1.841234558261931 |
| kind=dasha, jd_ut=2424214.4583333335 | lord_sequence_match=True, max_boundary_delta_days=2.8084707795642316 |
| kind=dasha, jd_ut=2427549.1569444444 | lord_sequence_match=True, max_boundary_delta_days=3.4467876171693206 |
| kind=dasha, jd_ut=2425935.888888889 | lord_sequence_match=True, max_boundary_delta_days=2.216830907855183 |
| kind=dasha, jd_ut=2449336.0694444445 | lord_sequence_match=True, max_boundary_delta_days=1.4428673768416047 |
| kind=dasha, jd_ut=2427112.59375 | lord_sequence_match=True, max_boundary_delta_days=1.7332013482227921 |
| kind=dasha, jd_ut=2420900.1666666665 | lord_sequence_match=True, max_boundary_delta_days=2.1592710725963116 |
| kind=dasha, jd_ut=2426510.6631944445 | lord_sequence_match=True, max_boundary_delta_days=1.5182382203638554 |
| kind=dasha, jd_ut=2431960.7805555556 | lord_sequence_match=True, max_boundary_delta_days=3.067934462800622 |
| kind=dasha, jd_ut=2442215.3229166665 | lord_sequence_match=True, max_boundary_delta_days=2.2804062590003014 |
| kind=dasha, jd_ut=2447991.18125 | lord_sequence_match=True, max_boundary_delta_days=2.3132706405594945 |
| kind=dasha, jd_ut=2427329.8958333335 | lord_sequence_match=True, max_boundary_delta_days=2.29454931570217 |
| kind=dasha, jd_ut=2425779.6305555557 | lord_sequence_match=True, max_boundary_delta_days=1.7650706516578794 |
| kind=dasha, jd_ut=2430120.3229166665 | lord_sequence_match=True, max_boundary_delta_days=1.7853781594894826 |
| kind=dasha, jd_ut=2430325.09375 | lord_sequence_match=True, max_boundary_delta_days=1.8710101144388318 |
| kind=dasha, jd_ut=2427004.972222222 | lord_sequence_match=True, max_boundary_delta_days=2.906581435818225 |
| kind=dasha, jd_ut=2423022.6666666665 | lord_sequence_match=True, max_boundary_delta_days=2.379185773432255 |
| kind=dasha, jd_ut=2430842.6666666665 | lord_sequence_match=True, max_boundary_delta_days=1.7999830418266356 |
| kind=dasha, jd_ut=2440923.7708333335 | lord_sequence_match=True, max_boundary_delta_days=1.024883150588721 |
| kind=dasha, jd_ut=2431992.0416666665 | lord_sequence_match=True, max_boundary_delta_days=1.5075680571608245 |
| kind=dasha, jd_ut=2423912.548611111 | lord_sequence_match=True, max_boundary_delta_days=1.6876430199481547 |
| kind=dasha, jd_ut=2425703.423611111 | lord_sequence_match=True, max_boundary_delta_days=3.552027814555913 |
| kind=dasha, jd_ut=2434675.3541666665 | lord_sequence_match=True, max_boundary_delta_days=1.4353255052119493 |
| kind=dasha, jd_ut=2423393.0833333335 | lord_sequence_match=True, max_boundary_delta_days=1.1238782568834722 |
| kind=dasha, jd_ut=2424301.9583333335 | lord_sequence_match=True, max_boundary_delta_days=2.374627297744155 |
| kind=dasha, jd_ut=2420463.25 | lord_sequence_match=True, max_boundary_delta_days=2.1110413488931954 |
| kind=dasha, jd_ut=2424389.9166666665 | lord_sequence_match=True, max_boundary_delta_days=2.1381152495741844 |
| kind=dasha, jd_ut=2424469.1041666665 | lord_sequence_match=True, max_boundary_delta_days=2.7970355530269444 |
| kind=dasha, jd_ut=2416541.5770833334 | lord_sequence_match=True, max_boundary_delta_days=2.953473167028278 |
| kind=dasha, jd_ut=2423876.7916666665 | lord_sequence_match=True, max_boundary_delta_days=3.2831088695675135 |
| kind=dasha, jd_ut=2441787.2395833335 | lord_sequence_match=True, max_boundary_delta_days=1.7343210526742041 |
| kind=dasha, jd_ut=2427739.4583333335 | lord_sequence_match=True, max_boundary_delta_days=2.5151642938144505 |
| kind=dasha, jd_ut=2417514.982638889 | lord_sequence_match=True, max_boundary_delta_days=1.309417111799121 |
| kind=dasha, jd_ut=2432127.375 | lord_sequence_match=True, max_boundary_delta_days=1.128336497116834 |
| kind=dasha, jd_ut=2431711.871527778 | lord_sequence_match=True, max_boundary_delta_days=2.634734308347106 |
| kind=dasha, jd_ut=2436707.5416666665 | lord_sequence_match=True, max_boundary_delta_days=2.022996840532869 |
| kind=dasha, jd_ut=2416611.3625 | lord_sequence_match=True, max_boundary_delta_days=3.149055495392531 |
| kind=dasha, jd_ut=2418418.625 | lord_sequence_match=True, max_boundary_delta_days=1.5524651105515659 |
| kind=dasha, jd_ut=2428444.875 | lord_sequence_match=True, max_boundary_delta_days=2.8955028960481286 |
| kind=dasha, jd_ut=2437337.472222222 | lord_sequence_match=True, max_boundary_delta_days=1.1080056140199304 |
| kind=dasha, jd_ut=2427545.5 | lord_sequence_match=True, max_boundary_delta_days=2.205890820361674 |
| kind=dasha, jd_ut=2433413.8694444443 | lord_sequence_match=True, max_boundary_delta_days=3.275678259320557 |
| kind=dasha, jd_ut=2424665.1666666665 | lord_sequence_match=True, max_boundary_delta_days=1.464035399723798 |
| kind=dasha, jd_ut=2430135.9756944445 | lord_sequence_match=True, max_boundary_delta_days=2.897008955013007 |
| kind=dasha, jd_ut=2422761.0104166665 | lord_sequence_match=True, max_boundary_delta_days=1.6285538435913622 |

...and 60 more — see the JSON report for the complete set.

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

