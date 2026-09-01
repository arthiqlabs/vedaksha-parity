# vedaksha-parity run report

**Tier:** `karakas`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** PyJHora 4.8.7  
**Generated:** 2026-09-01T16:19:40.054634+00:00  
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

200 cases

| Disposition | Count | % |
|---|---|---|
| pass | 152 | 76.0% |
| review | 34 | 17.0% |
| fail | 9 | 4.5% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 0 | 0.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 5 | 2.5% |

### Failures (9)

| Case | Comparison |
|---|---|
| kind=karakas, jd_ut=2401344.785416667 | compared=8, mismatched_karakas=['Amatyakaraka', 'Atmakaraka', 'Bhratrikaraka'] |
| kind=karakas, jd_ut=2447991.18125 | compared=8, mismatched_karakas=['Gnatikaraka', 'Pitrikaraka', 'Putrakaraka'] |
| kind=karakas, jd_ut=2425703.423611111 | compared=8, mismatched_karakas=['Amatyakaraka', 'Atmakaraka', 'Bhratrikaraka', 'Darakaraka', 'Gnatikaraka', 'Matrikaraka', 'Pitrikaraka', 'Putrakaraka'] |
| kind=karakas, jd_ut=2428819.625 | compared=8, mismatched_karakas=['Matrikaraka', 'Pitrikaraka', 'Putrakaraka'] |
| kind=karakas, jd_ut=2413238.9791666665 | compared=8, mismatched_karakas=['Amatyakaraka', 'Bhratrikaraka', 'Darakaraka', 'Gnatikaraka', 'Matrikaraka', 'Pitrikaraka', 'Putrakaraka'] |
| kind=karakas, jd_ut=2409311.1923611113 | compared=8, mismatched_karakas=['Amatyakaraka', 'Atmakaraka', 'Bhratrikaraka', 'Darakaraka', 'Gnatikaraka', 'Matrikaraka', 'Pitrikaraka', 'Putrakaraka'] |
| kind=karakas, jd_ut=2431941.1902777776 | compared=8, mismatched_karakas=['Amatyakaraka', 'Atmakaraka', 'Bhratrikaraka', 'Darakaraka', 'Gnatikaraka', 'Matrikaraka', 'Pitrikaraka', 'Putrakaraka'] |
| kind=karakas, jd_ut=2417801.03125 | compared=8, mismatched_karakas=['Amatyakaraka', 'Atmakaraka', 'Bhratrikaraka', 'Darakaraka', 'Gnatikaraka', 'Matrikaraka', 'Pitrikaraka', 'Putrakaraka'] |
| kind=karakas, jd_ut=2413840.722916667 | compared=8, mismatched_karakas=['Amatyakaraka', 'Atmakaraka', 'Bhratrikaraka', 'Darakaraka', 'Gnatikaraka', 'Matrikaraka', 'Pitrikaraka', 'Putrakaraka'] |

### Engine-error reasons (5)

| Reason | Count |
|---|---|
| ToolError('[-32602] Julian Day 2368785.921527778 is outside valid range [2378496.5, 2597641.5]') | 1 |
| ToolError('[-32602] Julian Day 2371045.0881944443 is outside valid range [2378496.5, 2597641.5]') | 1 |
| ToolError('[-32602] Julian Day 2343443.4381944444 is outside valid range [2378496.5, 2597641.5]') | 1 |
| ToolError('[-32602] Julian Day 2356889.4291666667 is outside valid range [2378496.5, 2597641.5]') | 1 |
| ToolError('[-32602] Julian Day 2373813.3173611113 is outside valid range [2378496.5, 2597641.5]') | 1 |

