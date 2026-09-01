"""Runs a case list against the engine and one oracle, and accounts for
every case's disposition — an oracle refusal is recorded, never dropped."""

from __future__ import annotations

from typing import Any

from vedaksha_parity.compare import (
    compare_ashtakavarga,
    compare_ayanamsha,
    compare_bhavas,
    compare_combustion,
    compare_dasha,
    compare_drishti,
    compare_houses,
    compare_karakas,
    compare_panchanga,
    compare_position,
    compare_sign_dasha,
    compare_vargas,
)
from vedaksha_parity.engine import Engine
from vedaksha_parity.oracles.base import OracleUnsupported


def run(cases: list[dict[str, Any]], engine: Engine, oracle: Any) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    counts = {
        "pass": 0, "review": 0, "fail": 0,
        "oracle_unsupported": 0, "oracle_error": 0, "engine_error": 0,
    }

    for case in cases:
        try:
            oracle_answer = oracle.answer(case)
        except OracleUnsupported as exc:
            counts["oracle_unsupported"] += 1
            rows.append({"case": case, "disposition": "oracle_unsupported", "reason": str(exc)})
            continue
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            # An oracle's internal crash, distinct from a deliberate
            # OracleUnsupported refusal or Vedaksha's own errors below —
            # recorded separately so failure sources stay attributable.
            counts["oracle_error"] += 1
            rows.append({"case": case, "disposition": "oracle_error", "reason": repr(exc)})
            continue

        try:
            if case["kind"] == "position":
                engine_answer = engine.position(case["jd_ut"], case["body"])
                comparison = compare_position(engine_answer, oracle_answer)
                disposition = comparison["longitude_disposition"]
            elif case["kind"] == "tropical_position":
                engine_answer = engine.tropical_position(case["jd_ut"], case["body"])
                comparison = compare_position(engine_answer, oracle_answer)
                disposition = comparison["longitude_disposition"]
            elif case["kind"] == "ayanamsha":
                engine_answer = {"value": engine.ayanamsha(case["jd_ut"])}
                comparison = compare_ayanamsha(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "karakas":
                engine_answer = engine.karakas(case["jd_ut"])
                comparison = compare_karakas(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "combustion":
                engine_answer = engine.combustion(case["jd_ut"], case["body"])
                comparison = compare_combustion(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "drishti":
                engine_answer = engine.drishti(case["jd_ut"])
                comparison = compare_drishti(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "dasha":
                engine_answer = engine.dasha(case["jd_ut"])
                comparison = compare_dasha(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "houses":
                engine_answer = engine.houses(case["jd_ut"], case["latitude"], case["longitude"])
                comparison = compare_houses(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "vargas":
                engine_answer = engine.vargas(
                    case["jd_ut"], case["latitude"], case["longitude"], case["division"]
                )
                comparison = compare_vargas(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "bhavas":
                engine_answer = engine.bhavas(case["jd_ut"], case["latitude"], case["longitude"])
                comparison = compare_bhavas(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "ashtakavarga":
                engine_answer = engine.ashtakavarga(case["jd_ut"], case["latitude"], case["longitude"])
                comparison = compare_ashtakavarga(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "panchanga":
                engine_answer = engine.panchanga(case["jd_ut"], case["latitude"], case["longitude"])
                comparison = compare_panchanga(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            elif case["kind"] == "chara_dasha":
                engine_answer = engine.chara_dasha(case["jd_ut"], case["latitude"], case["longitude"])
                comparison = compare_sign_dasha(engine_answer, oracle_answer)
                disposition = comparison["disposition"]
            else:
                raise ValueError(f"runner does not know case kind={case['kind']!r}")
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            counts["engine_error"] += 1
            rows.append({"case": case, "disposition": "engine_error", "reason": repr(exc)})
            continue

        counts[disposition] = counts.get(disposition, 0) + 1
        rows.append(
            {
                "case": case,
                "engine_answer": engine_answer,
                "oracle_answer": oracle_answer,
                "comparison": comparison,
                "disposition": disposition,
            }
        )

    assert sum(counts.values()) == len(cases), "every case must land in exactly one disposition bucket"
    return {"counts": counts, "rows": rows}
