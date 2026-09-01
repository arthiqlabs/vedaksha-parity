# vedaksha-parity

Copyright (C) 2026 ArthIQ Labs LLC

A reproducible oracle-parity harness for [Vedaksha](https://github.com/arthiqlabs/vedaksha) —
a clean-room ephemeris and Vedic-astrology engine — measured against a
roster of independent reference ephemerides and Jyotish engines, including
Swiss Ephemeris.

**This is a measuring instrument, not a validation stamp.** It generates a
report from whatever it actually finds — agreement, a documented convention
where two legitimate answers differ (ayanamsha choice, node type, year
length), or a genuine open question — and it never fixes Vedaksha to match a
reference. See `FIREWALL.md`.

**Status: active development.** All 13 in-scope tiers are built and have
been run at real scale; `docs/tiers.md` is the living record of every
result — exact figures, the Vedaksha version tested, era bounds, and open
questions, updated as new tiers or Vedaksha releases land. Nothing in this
README itself should be read as an accuracy claim independent of that
record — check `docs/tiers.md` for the actual numbers, not this file.

**Who built this.** ArthIQ Labs LLC — Vedaksha's own vendor — wrote this
harness. "Independent" describes the reference engines it compares
against (Swiss Ephemeris, JPL/IMCCE kernels, jyotishganit, PyJHora — each
built by an unrelated team), not third-party authorship of this
repository. What should be checked is the methodology (`FIREWALL.md`:
every reference is a sealed box, outputs only, never fixed to match), not
who wrote the harness — and the repo is designed so anyone can clone it
and re-run the same comparisons themselves rather than take any of this
on faith.

## Why this exists

Vedaksha publishes its own accuracy figures, measured against JPL kernels,
in its own repository. This harness exists to check the same and a broader
question independently — including against Swiss Ephemeris, the reference
implementation most people ask about first — in a repo anyone can clone and
re-run for themselves against a named Vedaksha release. "Don't trust us,
verify us" only works if the methodology is public and the run is genuinely
reproducible; that is the design constraint behind every choice below.

## Install

```bash
pip install vedaksha-parity
# optional oracle backends, one extra per engine — see docs/oracles.md
pip install vedaksha-parity[swisseph]
```

Nothing beyond `vedaksha` itself (a core dependency) is required to install
the base package. Each comparison oracle is opt-in.

## Scope

Deterministic quantities only: positions, ayanamsha, cusps, nakshatra,
vargas, dasha boundaries, panchanga, koota cells. Interpretive quantities —
yoga qualification, life-event scoring, remedies — have no accuracy oracle
and are out of scope by design; see `CLAUDE.md`.

## License

**AGPL-3.0-or-later** for this repository, including the optional swisseph
adapter (pyswisseph is itself AGPL-3.0-only, so the two are compatible
in-process with no isolation needed — see `CLAUDE.md` for the full
reasoning).

**Vedaksha itself is licensed separately, under BUSL-1.1** — free for
non-commercial use, a one-time commercial fee for organizations using it
commercially. This repository does not vendor or redistribute Vedaksha's
source; it depends on the published `vedaksha` PyPI package exactly as any
external consumer would, under Vedaksha's own terms. Using this harness
does not grant any right to use Vedaksha commercially beyond what
Vedaksha's own license already grants — see
[vedaksha's LICENSE](https://github.com/arthiqlabs/vedaksha/blob/main/LICENSE).
This is a one-directional relationship, not a licensing entanglement: an
AGPL work depending on a separately-licensed package via its published
package-manager interface (not vendored, not modified, not distributed
together) is the same situation as any AGPL project depending on a
proprietary database driver or SaaS SDK — copyleft binds this program's
own distribution, not what a user separately installs alongside it.

**The bundled birth-data sample (`data/vedastro-15000-famous-births.csv`)
is third-party, MIT-licensed data by [VedAstro](https://vedastro.org)**,
not this project's own — see `docs/birth-data.md` for the full
attribution and source link.

## How to reproduce a result

Every figure this harness ever publishes comes from a committed case list,
a frozen set of oracle answers, and a Vedaksha version whose identity is
recorded in the run's own provenance — never a hand-typed number. Clone
this repo, install the extras for the oracles you want (`pip install
vedaksha-parity[swisseph,skyfield,jyotishganit,...]`), then run any of the
committed configs under `configs/` (e.g. `vedaksha-parity run-config
configs/all-tiers-200-birthbank-v2.yaml`) to reproduce the exact figures
in `docs/tiers.md` against the Vedaksha version pinned in `pyproject.toml`.
