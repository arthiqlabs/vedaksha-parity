"""Julian Day conversion — textbook arithmetic, not sourced from any
oracle or engine. Shared by birth_bank.py (CSV birth times) and any oracle
adapter that reaches its library through a Python datetime rather than a
raw Julian Day (e.g. jyotishganit's dasha boundaries)."""

from __future__ import annotations

from datetime import datetime


def julian_day_ut(dt_utc: datetime) -> float:
    """Meeus, *Astronomical Algorithms*, ch. 7 — Gregorian-calendar Julian
    Day, valid for any date after 1582-10-15."""
    year, month = dt_utc.year, dt_utc.month
    day_fraction = (
        dt_utc.day
        + dt_utc.hour / 24.0
        + dt_utc.minute / 1440.0
        + dt_utc.second / 86400.0
    )
    if month <= 2:
        year -= 1
        month += 12
    a = year // 100
    b = 2 - a + a // 4
    return (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + day_fraction
        + b
        - 1524.5
    )
