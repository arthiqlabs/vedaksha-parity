# vedaksha-parity run report

**Tier:** `combustion`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** Astronomy Engine 2.1.19  
**Generated:** 2026-09-01T16:19:15.253487+00:00  
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
| provenance | truncated VSOP87 + NOVAS C 3.1, no external ephemeris dependencies of any kind — no swisseph, no JPL kernels, no data files (published documentation; never read from source) |
| frame | GeoVector(aberration=True) -> Ecliptic() = apparent geocentric ecliptic of date, tropical |
| stated_accuracy | approximately 1 arcminute (published documentation) |
| position | unsupported — this library is tropical-only; this harness's position case asks for sidereal. Answers tropical_position instead. |
| ayanamsha | unsupported — not an astronomical quantity this library exposes |
| nodes | unsupported — no lunar-node body in this library's interface |
| speed | not provided — no angular-rate quantity exposed by this interface |

## Results

1200 cases

| Disposition | Count | % |
|---|---|---|
| pass | 0 | 0.0% |
| review | 0 | 0.0% |
| fail | 0 | 0.0% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 1200 | 100.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Oracle-unsupported reasons (1200)

| Reason | Count |
|---|---|
| Astronomy Engine adapter does not answer kind='combustion' | 1200 |

