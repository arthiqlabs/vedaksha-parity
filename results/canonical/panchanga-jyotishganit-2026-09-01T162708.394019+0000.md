# vedaksha-parity run report

**Tier:** `panchanga`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** jyotishganit 0.1.3  
**Generated:** 2026-09-01T16:27:08.394019+00:00  
**Python:** 3.14.6

## Case parameters

- **sweep:** from=2451545.0, to=2453365.0, step_days=60.0
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

930 cases

| Disposition | Count | % |
|---|---|---|
| pass | 578 | 62.2% |
| review | 281 | 30.2% |
| fail | 69 | 7.4% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 0 | 0.0% |
| oracle_error | 2 | 0.2% |
| engine_error | 0 | 0.0% |

### Failures (69)

| Case | Comparison |
|---|---|
| kind=panchanga, jd_ut=2451725.0, latitude=28.6139, longitude=77.209, location_name=New Delhi | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=19.076, longitude=72.8777, location_name=Mumbai | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=22.5726, longitude=88.3639, location_name=Kolkata | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=13.0827, longitude=80.2707, location_name=Chennai | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=12.9716, longitude=77.5946, location_name=Bengaluru | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=17.385, longitude=78.4867, location_name=Hyderabad | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=23.0225, longitude=72.5714, location_name=Ahmedabad | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=18.5204, longitude=73.8567, location_name=Pune | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=26.9124, longitude=75.7873, location_name=Jaipur | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=26.8467, longitude=80.9462, location_name=Lucknow | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=25.3176, longitude=82.9739, location_name=Varanasi | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=31.634, longitude=74.8723, location_name=Amritsar | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=34.0837, longitude=74.7973, location_name=Srinagar | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=8.5241, longitude=76.9366, location_name=Thiruvananthapuram | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=26.1445, longitude=91.7362, location_name=Guwahati | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=23.2599, longitude=77.4126, location_name=Bhopal | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=25.5941, longitude=85.1376, location_name=Patna | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=21.1458, longitude=79.0882, location_name=Nagpur | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=30.7333, longitude=76.7794, location_name=Chandigarh | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=9.9312, longitude=76.2673, location_name=Kochi | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=40.7128, longitude=-74.006, location_name=New York | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=51.5074, longitude=-0.1278, location_name=London | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=43.6532, longitude=-79.3832, location_name=Toronto | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=25.2048, longitude=55.2708, location_name=Dubai | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=1.3521, longitude=103.8198, location_name=Singapore | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=-33.8688, longitude=151.2093, location_name=Sydney | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=37.7749, longitude=-122.4194, location_name=San Francisco | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2451725.0, latitude=-29.8587, longitude=31.0218, location_name=Durban | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=10.6549, longitude=-61.5019, location_name=Port of Spain | mismatched_limbs=['yoga', 'karana'] |
| kind=panchanga, jd_ut=2451725.0, latitude=3.139, longitude=101.6869, location_name=Kuala Lumpur | mismatched_limbs=['yoga', 'karana', 'vara'] |
| kind=panchanga, jd_ut=2452265.0, latitude=40.7128, longitude=-74.006, location_name=New York | mismatched_limbs=['karana', 'vara'] |
| kind=panchanga, jd_ut=2452265.0, latitude=43.6532, longitude=-79.3832, location_name=Toronto | mismatched_limbs=['karana', 'vara'] |
| kind=panchanga, jd_ut=2452265.0, latitude=1.3521, longitude=103.8198, location_name=Singapore | mismatched_limbs=['karana', 'vara'] |
| kind=panchanga, jd_ut=2452265.0, latitude=-33.8688, longitude=151.2093, location_name=Sydney | mismatched_limbs=['karana', 'vara'] |
| kind=panchanga, jd_ut=2452265.0, latitude=37.7749, longitude=-122.4194, location_name=San Francisco | mismatched_limbs=['karana', 'vara'] |
| kind=panchanga, jd_ut=2452265.0, latitude=3.139, longitude=101.6869, location_name=Kuala Lumpur | mismatched_limbs=['karana', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=28.6139, longitude=77.209, location_name=New Delhi | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=22.5726, longitude=88.3639, location_name=Kolkata | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=26.8467, longitude=80.9462, location_name=Lucknow | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=25.3176, longitude=82.9739, location_name=Varanasi | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=31.634, longitude=74.8723, location_name=Amritsar | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=34.0837, longitude=74.7973, location_name=Srinagar | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=26.1445, longitude=91.7362, location_name=Guwahati | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=25.5941, longitude=85.1376, location_name=Patna | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=30.7333, longitude=76.7794, location_name=Chandigarh | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=1.3521, longitude=103.8198, location_name=Singapore | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=-33.8688, longitude=151.2093, location_name=Sydney | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=37.7749, longitude=-122.4194, location_name=San Francisco | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452445.0, latitude=3.139, longitude=101.6869, location_name=Kuala Lumpur | mismatched_limbs=['yoga', 'vara'] |
| kind=panchanga, jd_ut=2452505.0, latitude=22.5726, longitude=88.3639, location_name=Kolkata | mismatched_limbs=['nakshatra', 'vara'] |

...and 19 more — see the JSON report for the complete set.

### Oracle-error reasons (2)

| Reason | Count |
|---|---|
| TypeError("'<' not supported between instances of 'float' and 'NoneType'") | 1 |
| TypeError("'<=' not supported between instances of 'NoneType' and 'float'") | 1 |

