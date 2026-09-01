# vedaksha-parity run report

**Tier:** `combustion`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** PyJHora 4.8.7  
**Generated:** 2026-09-01T16:19:45.243813+00:00  
**Python:** 3.14.6

## Case parameters

- **birth_bank:** source_size=15790, count=200, seed=42, source=data/vedastro-15000-famous-births.csv

## Engine settings

| Setting | Value |
|---|---|
| ayanamsha | IndianOfficial |
| karaka_scheme | 8 |

## Oracle settings

| Setting | Value |
|---|---|
| ayanamsha | LAHIRI — global module state, see module docstring |
| independence_from_swisseph | Measured, not confirmed — see module docstring |
| combustion | Binary (Combust/None only), no DeeplyCombust distinction |
| location | synthetic/neutral (0.0 deg, 0.0 deg, UTC) |
| chara_dasha | Real location required. Narayana dasha exists in PyJHora but is not wired — Chara is the pilot |
| karakas | 8-scheme via get_chara_karakas — compare against Engine(karaka_scheme="8"); rank 4 emitted as Vedaksha's own "Matrikaraka", not PyJHora's "Maitrikaraka" |
| scope | position/ayanamsha not built here — a separate scope decision, not a circularity finding |

## Results

1200 cases

| Disposition | Count | % |
|---|---|---|
| pass | 1047 | 87.2% |
| review | 0 | 0.0% |
| fail | 123 | 10.2% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 0 | 0.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 30 | 2.5% |

### Failures (123)

| Case | Comparison |
|---|---|
| kind=combustion, jd_ut=2437293.826388889, body=Saturn | engine_state=Combust, oracle_state=None |
| kind=combustion, jd_ut=2411318.0243055555, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2439430.6354166665, body=Venus | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2436655.667361111, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2392437.4520833334, body=Mars | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2392437.4520833334, body=Venus | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2424214.4583333335, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2391641.046527778, body=Mars | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2427549.1569444444, body=Mars | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2425935.888888889, body=Mars | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2425935.888888889, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2449336.0694444445, body=Mars | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2427112.59375, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2427112.59375, body=Saturn | engine_state=Combust, oracle_state=None |
| kind=combustion, jd_ut=2400263.0048611113, body=Mars | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2400263.0048611113, body=Saturn | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2420900.1666666665, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2423425.25, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2442215.3229166665, body=Saturn | engine_state=Combust, oracle_state=None |
| kind=combustion, jd_ut=2418673.954861111, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2427430.96875, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2427329.8958333335, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2430120.3229166665, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2430120.3229166665, body=Saturn | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2427004.972222222, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2422580.673611111, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2422580.673611111, body=Saturn | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2423022.6666666665, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2418301.159722222, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2388516.5770833334, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2423912.548611111, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2425703.423611111, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2434675.3541666665, body=Saturn | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2423393.0833333335, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2429093.3125, body=Mars | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2420463.25, body=Venus | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2401041.671527778, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2401041.671527778, body=Saturn | engine_state=Combust, oracle_state=None |
| kind=combustion, jd_ut=2424389.9166666665, body=Mars | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2424389.9166666665, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2424469.1041666665, body=Saturn | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2441787.2395833335, body=Venus | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2427739.4583333335, body=Jupiter | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2432127.375, body=Jupiter | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2431711.871527778, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2431711.871527778, body=Jupiter | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2426551.075, body=Jupiter | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2436707.5416666665, body=Mercury | engine_state=None, oracle_state=Combust |
| kind=combustion, jd_ut=2416611.3625, body=Mars | engine_state=DeeplyCombust, oracle_state=Combust |
| kind=combustion, jd_ut=2416611.3625, body=Mercury | engine_state=DeeplyCombust, oracle_state=Combust |

...and 73 more — see the JSON report for the complete set.

### Engine-error reasons (30)

| Reason | Count |
|---|---|
| ToolError('[-32602] Julian Day 2368785.921527778 is outside valid range [2378496.5, 2597641.5]') | 6 |
| ToolError('[-32602] Julian Day 2371045.0881944443 is outside valid range [2378496.5, 2597641.5]') | 6 |
| ToolError('[-32602] Julian Day 2343443.4381944444 is outside valid range [2378496.5, 2597641.5]') | 6 |
| ToolError('[-32602] Julian Day 2356889.4291666667 is outside valid range [2378496.5, 2597641.5]') | 6 |
| ToolError('[-32602] Julian Day 2373813.3173611113 is outside valid range [2378496.5, 2597641.5]') | 6 |

