"""Run provenance + report. Every claim this harness can ever make traces
back to a run.json — engine version, oracle version and settings, the exact
case-generation parameters, and disposition counts. Nothing is hand-typed."""

from __future__ import annotations

import json
import math
import platform
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def build_run_record(
    *,
    tier: str,
    engine: Any,
    oracle: Any,
    case_params: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "tier": tier,
        "case_params": case_params,
        "engine": {"name": engine.NAME, "version": engine.VERSION, "settings": engine.settings()},
        "oracle": {"name": oracle.NAME, "version": oracle.VERSION, "settings": oracle.settings()},
        "counts": result["counts"],
        "case_count": len(result["rows"]),
    }


def write_run(run_record: dict[str, Any], result: dict[str, Any], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = run_record["generated_at"].replace(":", "").replace("+00:00", "Z")
    run_path = out_dir / f"{run_record['tier']}-{run_record['oracle']['name'].lower().replace(' ', '')}-{stamp}.json"
    run_path.write_text(json.dumps({**run_record, "rows": result["rows"]}, indent=2, default=str))
    return run_path


def write_run_markdown(run_record: dict[str, Any], result: dict[str, Any], out_dir: Path) -> Path:
    """A human-readable companion to write_run's JSON, generated FROM the
    same run record — never a replacement for it. The JSON stays the
    full-fidelity, reproducible record every claim traces back to (a birth-
    bank run can carry 100k+ rows, unreadable as a table); this is the
    digest suited for a person actually reading a result."""
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = run_record["generated_at"].replace(":", "").replace("+00:00", "Z")
    md_path = (
        out_dir / f"{run_record['tier']}-{run_record['oracle']['name'].lower().replace(' ', '')}-{stamp}.md"
    )
    md_path.write_text(_render_markdown(run_record, result))
    return md_path


def _render_markdown(run_record: dict[str, Any], result: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# vedaksha-parity run report")
    lines.append("")
    lines.append(f"**Tier:** `{run_record['tier']}`  ")
    lines.append(
        f"**Engine:** {run_record['engine']['name']} {run_record['engine']['version']}  "
    )
    lines.append(
        f"**Oracle:** {run_record['oracle']['name']} {run_record['oracle']['version']}  "
    )
    lines.append(f"**Generated:** {run_record['generated_at']}  ")
    lines.append(f"**Python:** {run_record['python']}")
    lines.append("")

    lines.append("## Case parameters")
    lines.append("")
    lines.append(_render_kv_block(run_record["case_params"]))
    lines.append("")

    lines.append("## Engine settings")
    lines.append("")
    lines.append(_render_kv_table(run_record["engine"]["settings"]))
    lines.append("")

    lines.append("## Oracle settings")
    lines.append("")
    lines.append(_render_kv_table(run_record["oracle"]["settings"]))
    lines.append("")

    lines.append("## Results")
    lines.append("")
    total = run_record["case_count"]
    lines.append(f"{total} cases")
    lines.append("")
    lines.append("| Disposition | Count | % |")
    lines.append("|---|---|---|")
    for disposition in (
        "pass", "review", "fail", "comparison_invalid",
        "oracle_unsupported", "oracle_error", "engine_error",
    ):
        count = run_record["counts"].get(disposition, 0)
        pct = (count / total * 100.0) if total else 0.0
        lines.append(f"| {disposition} | {count} | {pct:.1f}% |")
    lines.append("")

    rows = result["rows"]

    stats_block = _render_delta_stats(rows)
    if stats_block:
        lines.append("### Raw delta statistics")
        lines.append("")
        lines.append(
            "Disposition counts depend on this project's own provisional "
            "tolerance bands. These distributions do not -- they are "
            "computed directly from every row's raw delta, independent of "
            "any pass/review/fail threshold, and are the primary evidence "
            "a disposition count only summarizes."
        )
        lines.append("")
        lines.append(stats_block)
        lines.append("")

    fails = [r for r in rows if r["disposition"] == "fail"]
    if fails:
        lines.append(f"### Failures ({len(fails)})")
        lines.append("")
        # Position/tropical_position failures get dedicated columns; every
        # other case kind falls back to a generic case/comparison dump.
        cap = 50
        if all("longitude_delta_arcsec" in r["comparison"] for r in fails):
            lines.append("| Body | jd_ut | Engine longitude | Oracle longitude | Δ longitude (arcsec) |")
            lines.append("|---|---|---|---|---|")
            for row in fails[:cap]:
                case = row["case"]
                comparison = row["comparison"]
                lines.append(
                    f"| {case.get('body', '—')} | {case['jd_ut']} | "
                    f"{row['engine_answer']['longitude']:.6f} | {row['oracle_answer']['longitude']:.6f} | "
                    f"{comparison['longitude_delta_arcsec']:.2f} |"
                )
        else:
            lines.append("| Case | Comparison |")
            lines.append("|---|---|")
            for row in fails[:cap]:
                case_str = ", ".join(f"{k}={v}" for k, v in row["case"].items())
                comparison_str = ", ".join(
                    f"{k}={v}" for k, v in row["comparison"].items() if k != "disposition"
                )
                lines.append(f"| {_escape_pipes(case_str)} | {_escape_pipes(comparison_str)} |")
        if len(fails) > cap:
            lines.append("")
            lines.append(f"...and {len(fails) - cap} more — see the JSON report for the complete set.")
        lines.append("")

    for disposition, label in (
        ("oracle_unsupported", "Oracle-unsupported reasons"),
        ("oracle_error", "Oracle-error reasons"),
        ("engine_error", "Engine-error reasons"),
    ):
        grouped = _group_reasons(rows, disposition)
        if grouped:
            lines.append(f"### {label} ({sum(grouped.values())})")
            lines.append("")
            lines.append("| Reason | Count |")
            lines.append("|---|---|")
            for reason, count in sorted(grouped.items(), key=lambda kv: -kv[1]):
                lines.append(f"| {_escape_pipes(reason)} | {count} |")
            lines.append("")

    return "\n".join(lines) + "\n"


def _percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = p / 100.0 * (len(sorted_values) - 1)
    lo, hi = math.floor(rank), math.ceil(rank)
    if lo == hi:
        return sorted_values[lo]
    frac = rank - lo
    return sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * frac


def _numeric_stats(values: list[float]) -> dict[str, float]:
    n = len(values)
    ordered = sorted(abs(v) for v in values)
    mean = sum(ordered) / n
    rms = math.sqrt(sum(v * v for v in ordered) / n)
    return {
        "n": n,
        "mean": mean,
        "median": _percentile(ordered, 50),
        "rms": rms,
        "p90": _percentile(ordered, 90),
        "p95": _percentile(ordered, 95),
        "p99": _percentile(ordered, 99),
        "max": ordered[-1],
    }


def _render_delta_stats(rows: list[dict[str, Any]]) -> str:
    # Any comparison-dict field whose name contains "delta" and whose
    # value is numeric (never a bool -- Python's bool is an int subclass)
    # is treated as a raw magnitude series, gathered across every row
    # that has one — independent of tier, independent of disposition, and
    # independent of whatever tolerance band that field is also classified
    # against.
    series: dict[str, list[float]] = {}
    for row in rows:
        comparison = row.get("comparison") or {}
        for key, value in comparison.items():
            if "delta" in key and isinstance(value, (int, float)) and not isinstance(value, bool):
                series.setdefault(key, []).append(float(value))
    if not series:
        return ""
    lines = ["| Field | n | mean | median | RMS | P90 | P95 | P99 | max |", "|---|---|---|---|---|---|---|---|---|"]
    for field in sorted(series):
        s = _numeric_stats(series[field])
        lines.append(
            f"| {field} | {s['n']} | {s['mean']:.4f} | {s['median']:.4f} | {s['rms']:.4f} | "
            f"{s['p90']:.4f} | {s['p95']:.4f} | {s['p99']:.4f} | {s['max']:.4f} |"
        )
    return "\n".join(lines)


def _escape_pipes(value: Any) -> str:
    # A literal "|" in a value (e.g. swisseph's own flags string) would
    # otherwise be read as a table column delimiter and corrupt the row.
    return str(value).replace("|", "\\|")


def _render_kv_block(d: dict[str, Any]) -> str:
    if not d:
        return "*(none)*"
    lines = []
    for key, value in d.items():
        if isinstance(value, dict):
            lines.append(f"- **{key}:** " + ", ".join(f"{k}={v}" for k, v in value.items()))
        else:
            lines.append(f"- **{key}:** {value}")
    return "\n".join(lines)


def _render_kv_table(d: dict[str, Any]) -> str:
    if not d:
        return "*(none)*"
    lines = ["| Setting | Value |", "|---|---|"]
    for key, value in d.items():
        lines.append(f"| {key} | {_escape_pipes(value)} |")
    return "\n".join(lines)


def _group_reasons(rows: list[dict[str, Any]], disposition: str) -> dict[str, int]:
    grouped: dict[str, int] = {}
    for row in rows:
        if row["disposition"] != disposition:
            continue
        reason = row.get("reason", "(no reason recorded)")
        grouped[reason] = grouped.get(reason, 0) + 1
    return grouped


def print_summary(run_record: dict[str, Any]) -> None:
    print(f"tier {run_record['tier']}  engine {run_record['engine']['name']} "
          f"{run_record['engine']['version']}  oracle {run_record['oracle']['name']} "
          f"{run_record['oracle']['version']}")
    print(f"cases: {run_record['case_count']}")
    for disposition, count in run_record["counts"].items():
        if count:
            print(f"  {disposition}: {count}")
