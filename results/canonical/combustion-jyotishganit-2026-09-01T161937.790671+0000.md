# vedaksha-parity run report

**Tier:** `combustion`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** jyotishganit 0.1.3  
**Generated:** 2026-09-01T16:19:37.790671+00:00  
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
| jyotishganit adapter does not answer kind='combustion' | 1200 |

