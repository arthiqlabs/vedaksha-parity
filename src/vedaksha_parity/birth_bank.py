"""Real, third-party-verified birth instants as a case source, alongside
`cases.py`'s synthetic sweep grid. See docs/birth-data.md for provenance,
license, and the `birth_bank` config schema this module implements.

Local birth date + time + timezone offset -> UTC -> Julian Day, using the
standard published Julian Date conversion (Meeus, *Astronomical
Algorithms*) — textbook arithmetic, not anything sourced from an oracle. No
third-party ephemeris library is required for this step.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import re
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from vedaksha_parity.config import BODIES, COMBUSTION_BODIES, NODES
from vedaksha_parity.julian_day import julian_day_ut

DEFAULT_SOURCE = Path("data/vedastro-15000-famous-births.csv")

_STD_TIME_RE = re.compile(
    r"^(?P<hour>\d{2}):(?P<minute>\d{2})\s+"
    r"(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})\s+"
    r"(?P<sign>[+-])(?P<off_hour>\d{2}):(?P<off_minute>\d{2})$"
)


@dataclass(frozen=True)
class BirthRecord:
    row_key: str
    name: str
    jd_ut: float
    location_name: str
    latitude: float
    longitude: float


def _parse_std_time(std_time: str) -> float:
    m = _STD_TIME_RE.match(std_time.strip())
    if not m:
        raise ValueError(f"unrecognised StdTime format: {std_time!r}")
    g = m.groupdict()
    offset_minutes = int(g["off_hour"]) * 60 + int(g["off_minute"])
    if g["sign"] == "-":
        offset_minutes = -offset_minutes
    local_dt = datetime(
        int(g["year"]), int(g["month"]), int(g["day"]),
        int(g["hour"]), int(g["minute"]),
        tzinfo=timezone(timedelta(minutes=offset_minutes)),
    )
    dt_utc = local_dt.astimezone(UTC)
    return julian_day_ut(dt_utc)


def load_birth_bank(source: Path = DEFAULT_SOURCE) -> list[BirthRecord]:
    """Parse every record in file order — deterministic, never shuffled at
    load time. A row this parser cannot make sense of is skipped with a
    clear reason, never silently dropped without a trace."""
    records: list[BirthRecord] = []
    with source.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # 17 rows are literal placeholder entries (Name/Location both
            # "Empty") — an upstream data-quality issue, not a parsing bug.
            # See docs/birth-data.md.
            if row["Name"] == "Empty":
                continue
            try:
                birth = json.loads(row["BirthTime"])
                jd_ut = _parse_std_time(birth["StdTime"])
                location = birth["Location"]
            except (KeyError, ValueError, json.JSONDecodeError) as exc:
                raise ValueError(
                    f"{source}: row {row.get('RowKey', '?')!r} could not be parsed: {exc}"
                ) from exc
            records.append(
                BirthRecord(
                    row_key=row["RowKey"],
                    name=row["Name"],
                    jd_ut=jd_ut,
                    location_name=location["Name"],
                    latitude=float(location["Latitude"]),
                    longitude=float(location["Longitude"]),
                )
            )
    return records


def select_birth_bank(
    records: list[BirthRecord], count: int | None = None, seed: int | None = None
) -> tuple[list[BirthRecord], dict[str, Any]]:
    """count=None (the default) selects every record — 100% of the source,
    what this repo's own published runs use, no sampling at all. A tester
    who sets count gets a seeded sample: any seed they choose, or one
    generated here if they leave it blank — either way, the seed actually
    used is always returned for the caller to record in `case_params`, so a
    sampled run stays exactly reproducible from what it reports."""
    if count is None:
        return records, {"source_size": len(records), "count": None, "seed": None}
    if count > len(records):
        raise ValueError(f"count={count} exceeds the source's {len(records)} records")
    actual_seed = seed if seed is not None else random.SystemRandom().randrange(2**32)
    sampled = random.Random(actual_seed).sample(records, count)
    return sampled, {"source_size": len(records), "count": count, "seed": actual_seed}


_DEFAULT_SPLIT_SEED = 20260901  # a fixed, published constant — see split_birth_bank


def _split_key(row_key: str, seed: int) -> float:
    # A stable, deterministic pseudo-position in [0, 1) for one record —
    # a function of the record's own identity, never its position in the
    # source file, so re-sorting or extending the CSV can't silently move
    # a record between buckets. Not cryptographic; sha256 is just a
    # convenient, well-distributed, dependency-free hash.
    digest = hashlib.sha256(f"{seed}:{row_key}".encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def split_birth_bank(
    records: list[BirthRecord], *, ratios: dict[str, float], seed: int = _DEFAULT_SPLIT_SEED
) -> dict[str, list[BirthRecord]]:
    """A permanent, once-and-forever partition of the birth bank — e.g.
    {"dev": 0.34, "validation": 0.33, "holdout": 0.33} — for exactly the
    reason review item 7 raised: a fixed 200-record sample that gets
    re-examined and fixed against repeatedly stops behaving like an
    independent validation set and starts behaving like a training
    corpus. `dev` is safe to inspect routinely; `holdout` is meant to be
    run but not read case-by-case during normal implementation work, so
    it keeps evidentiary weight a repeatedly-inspected sample no longer
    has. The partition is a pure function of each record's own row_key
    and `seed` — deterministic and reproducible without storing an
    explicit ID list, and stable even if the source CSV is later
    resorted, filtered, or has new rows appended."""
    if abs(sum(ratios.values()) - 1.0) > 1e-9:
        raise ValueError(f"ratios must sum to 1.0, got {ratios}")
    boundaries: list[tuple[str, float]] = []
    cumulative = 0.0
    for name, ratio in ratios.items():
        cumulative += ratio
        boundaries.append((name, cumulative))
    buckets: dict[str, list[BirthRecord]] = {name: [] for name in ratios}
    for record in records:
        position = _split_key(record.row_key, seed)
        for name, threshold in boundaries:
            if position < threshold:
                buckets[name].append(record)
                break
        else:
            buckets[boundaries[-1][0]].append(record)  # floating-point edge at exactly 1.0
    return buckets


def build_cases_from_birth_bank(records: list[BirthRecord], tier: str) -> list[dict[str, Any]]:
    """Case shape matches cases.py's sweep-grid builders exactly, so the
    runner and compare.py treat a birth-bank case no differently from a
    swept one."""
    if tier == "t1":
        return [
            {"kind": "position", "jd_ut": r.jd_ut, "body": body}
            for r in records
            for body in (*BODIES, *NODES)
        ]
    if tier == "t1-tropical":
        return [
            {"kind": "tropical_position", "jd_ut": r.jd_ut, "body": body}
            for r in records
            for body in (*BODIES, *NODES)
        ]
    if tier == "t2":
        return [{"kind": "ayanamsha", "jd_ut": r.jd_ut} for r in records]
    if tier == "karakas":
        return [{"kind": "karakas", "jd_ut": r.jd_ut} for r in records]
    if tier == "combustion":
        return [
            {"kind": "combustion", "jd_ut": r.jd_ut, "body": body}
            for r in records
            for body in COMBUSTION_BODIES
        ]
    if tier == "drishti":
        return [{"kind": "drishti", "jd_ut": r.jd_ut} for r in records]
    if tier == "dasha":
        return [{"kind": "dasha", "jd_ut": r.jd_ut} for r in records]
    raise ValueError(f"birth_bank does not know tier={tier!r}")
