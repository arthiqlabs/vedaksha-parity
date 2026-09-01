"""Pinned settings for every comparison this harness runs.

Nothing here may be silently defaulted by an oracle library. A setting an
oracle cannot be pinned to (see docs/oracles.md's per-oracle notes as they
are written) makes that oracle unable to answer the affected case kind, not
a reason to relax the pin.
"""

from __future__ import annotations

# Vedaksha's ayanamsha name, and the classical convention it corresponds to.
# `vedaksha.Vedaksha.natal_chart(..., ayanamsha=...)` takes this string.
VEDAKSHA_AYANAMSHA = "IndianOfficial"  # Lahiri / Chitrapaksha, epoch-anchored

# compute_karakas's own default scheme (7 classical grahas, Sun-Saturn). "8"
# adds Rahu + Pitrikaraka — needed to compare against an oracle whose own
# karaka ranking is 8-wide, like PyJHora's.
VEDAKSHA_KARAKA_SCHEME = "7"

# The seven classical grahas plus both lunar-node conventions, reported
# separately and never conflated (Vedaksha's own surface keeps them apart).
BODIES: tuple[str, ...] = (
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
)
NODES: tuple[str, ...] = ("MeanNode", "TrueNode")

# compute_combustion never tests the Sun against itself — six bodies, not
# seven, per its own required-parameters list.
COMBUSTION_BODIES: tuple[str, ...] = (
    "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
)

# Geocentric quantities don't depend on observer location — a fixed
# placeholder keeps position/ayanamsha cases free of location resolution.
PLACEHOLDER_LATITUDE = 0.0
PLACEHOLDER_LONGITUDE = 0.0

# Provisional tolerance bands in arcseconds, pending real-run calibration.
# These are starting points, not a validated claim about achievable
# precision — recalibrate from measured data before quoting them anywhere.
TOLERANCES = {
    "position_longitude_arcsec": {"pass": 5.0, "review": 60.0},
    "position_latitude_arcsec": {"pass": 5.0, "review": 60.0},
    "ayanamsha_arcsec": {"pass": 1.0, "review": 10.0},
    # Dasha boundaries are dates, not angles — tolerance in days. Provisional,
    # same discipline as the arcsec bands above: not a validated claim about
    # achievable precision, a starting point pending real-run calibration.
    "dasha_start_delta_days": {"pass": 0.01, "review": 1.0},
}

# Categorical comparators (drishti, vargas, bhavas, ashtakavarga, panchanga)
# classify by mismatch count, not a continuous delta — a single flipped
# rank/state/aspect lands in review (plausibly a near-tie or boundary case),
# more than one is a fail. Provisional, same as the numeric bands above.
CATEGORICAL_REVIEW_MISMATCH_MAX = 1

# Karakas is a permutation — swapping two ranks always changes two titles
# at once, so the minimum real mismatch is 2, never 1.
KARAKA_REVIEW_MISMATCH_MAX = 2
