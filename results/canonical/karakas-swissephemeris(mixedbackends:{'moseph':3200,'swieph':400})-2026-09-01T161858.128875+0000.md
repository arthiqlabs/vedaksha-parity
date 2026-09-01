# vedaksha-parity run report

**Tier:** `karakas`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** Swiss Ephemeris (mixed backends: {'MOSEPH': 3200, 'SWIEPH': 400}) 2.10.03  
**Generated:** 2026-09-01T16:18:58.128875+00:00  
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
| pass | 0 | 0.0% |
| review | 0 | 0.0% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 200 | 100.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Oracle-unsupported reasons (200)

| Reason | Count |
|---|---|
| Swiss Ephemeris adapter does not answer kind='karakas' | 200 |

