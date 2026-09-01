# vedaksha-parity run report

**Tier:** `chara-dasha`  
**Engine:** Vedaksha 9.1.0  
**Oracle:** PyJHora 4.8.7  
**Generated:** 2026-09-01T16:29:51.649105+00:00  
**Python:** 3.14.6

## Case parameters

- **sweep:** from=2451545.0, to=2453365.0, step_days=60.0

## Engine settings

| Setting | Value |
|---|---|
| ayanamsha | IndianOfficial |
| karaka_scheme | 7 |

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

930 cases

| Disposition | Count | % |
|---|---|---|
| pass | 0 | 0.0% |
| review | 185 | 19.9% |
| fail | 745 | 80.1% |
| comparison_invalid | 0 | 0.0% |
| oracle_unsupported | 0 | 0.0% |
| oracle_error | 0 | 0.0% |
| engine_error | 0 | 0.0% |

### Raw delta statistics

Disposition counts depend on this project's own provisional tolerance bands. These distributions do not -- they are computed directly from every row's raw delta, independent of any pass/review/fail threshold, and are the primary evidence a disposition count only summarizes.

| Field | n | mean | median | RMS | P90 | P95 | P99 | max |
|---|---|---|---|---|---|---|---|---|
| max_boundary_delta_days | 930 | 807.6335 | 730.3450 | 1135.9959 | 2190.6160 | 2556.1865 | 3286.6156 | 3286.9370 |

### Failures (745)

| Case | Comparison |
|---|---|
| kind=chara_dasha, jd_ut=2451545.0, latitude=28.6139, longitude=77.209, location_name=New Delhi | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.301286472939 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=19.076, longitude=72.8777, location_name=Mumbai | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012815834954 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=22.5726, longitude=88.3639, location_name=Kolkata | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012914787978 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=13.0827, longitude=80.2707, location_name=Chennai | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012866126373 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=12.9716, longitude=77.5946, location_name=Bengaluru | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012845637277 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=17.385, longitude=78.4867, location_name=Hyderabad | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012858442962 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=23.0225, longitude=72.5714, location_name=Ahmedabad | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012819327414 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=18.5204, longitude=73.8567, location_name=Pune | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012823285535 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=26.9124, longitude=75.7873, location_name=Jaipur | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012851458043 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=26.8467, longitude=80.9462, location_name=Lucknow | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012888478115 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=25.3176, longitude=82.9739, location_name=Varanasi | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012899421155 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=31.634, longitude=74.8723, location_name=Amritsar | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012852156535 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=34.0837, longitude=74.7973, location_name=Srinagar | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012855881825 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=8.5241, longitude=76.9366, location_name=Thiruvananthapuram | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012834694237 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=26.1445, longitude=91.7362, location_name=Guwahati | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012894997373 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=23.2599, longitude=77.4126, location_name=Bhopal | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012858442962 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=25.5941, longitude=85.1376, location_name=Patna | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012913623825 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=21.1458, longitude=79.0882, location_name=Nagpur | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012867756188 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=30.7333, longitude=76.7794, location_name=Chandigarh | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.301286496222 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=9.9312, longitude=76.2673, location_name=Kochi | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012830968946 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=40.7128, longitude=-74.006, location_name=New York | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.1979662682861 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=51.5074, longitude=-0.1278, location_name=London | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.2097152867354 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=43.6532, longitude=-79.3832, location_name=Toronto | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.1979659143835 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=25.2048, longitude=55.2708, location_name=Dubai | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.32511273399 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=1.3521, longitude=103.8198, location_name=Singapore | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012932250276 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=-33.8688, longitude=151.2093, location_name=Sydney | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3330867197365 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=37.7749, longitude=-122.4194, location_name=San Francisco | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.1820695698261 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=-29.8587, longitude=31.0218, location_name=Durban | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.2097640670836 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=10.6549, longitude=-61.5019, location_name=Port of Spain | sign_sequence_match=True, mismatched_durations=[9, 7, 10], max_boundary_delta_days=1095.4559143520892 |
| kind=chara_dasha, jd_ut=2451545.0, latitude=3.139, longitude=101.6869, location_name=Kuala Lumpur | sign_sequence_match=True, mismatched_durations=[10, 9], max_boundary_delta_days=730.3012941563502 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=28.6139, longitude=77.209, location_name=New Delhi | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450034488924 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=19.076, longitude=72.8777, location_name=Mumbai | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3449996351264 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=22.5726, longitude=88.3639, location_name=Kolkata | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450073534623 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=13.0827, longitude=80.2707, location_name=Chennai | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450035578571 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=12.9716, longitude=77.5946, location_name=Bengaluru | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450019597076 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=17.385, longitude=78.4867, location_name=Hyderabad | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.345002958551 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=23.0225, longitude=72.5714, location_name=Ahmedabad | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3449999075383 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=18.5204, longitude=73.8567, location_name=Pune | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450002162717 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=26.9124, longitude=75.7873, location_name=Jaipur | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450024137273 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=26.8467, longitude=80.9462, location_name=Lucknow | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.345005301293 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=25.3176, longitude=82.9739, location_name=Varanasi | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450061548501 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=31.634, longitude=74.8723, location_name=Amritsar | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450024682097 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=34.0837, longitude=74.7973, location_name=Srinagar | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450027587824 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=8.5241, longitude=76.9366, location_name=Thiruvananthapuram | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450011061504 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=26.1445, longitude=91.7362, location_name=Guwahati | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450058097951 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=23.2599, longitude=77.4126, location_name=Bhopal | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.345002958551 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=25.5941, longitude=85.1376, location_name=Patna | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450072626583 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=21.1458, longitude=79.0882, location_name=Nagpur | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450036849827 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=30.7333, longitude=76.7794, location_name=Chandigarh | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450034670532 |
| kind=chara_dasha, jd_ut=2451605.0, latitude=9.9312, longitude=76.2673, location_name=Kochi | sign_sequence_match=True, mismatched_durations=[9, 10], max_boundary_delta_days=730.3450008155778 |

...and 695 more — see the JSON report for the complete set.

