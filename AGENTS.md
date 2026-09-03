# AGENTS.md — vedaksha-parity

Operating instructions for any coding agent working in this repository.
`CLAUDE.md` in this directory is a symlink to this file. The ArthIQ Labs
operating model applies as always; this file adds what is specific to this
repo.

## Read first, every session

1. **`FIREWALL.md`** — non-negotiable, and the reason this repo's methodology
   can be trusted.
2. `docs/oracles.md` — before configuring or debugging any reference oracle.

## What this repo is

A reproducible oracle-parity harness for **Vedaksha alone**. It calls
Vedaksha through its published PyPI package (`pip install vedaksha`, the
same install path any external consumer uses) and compares its output
against a roster of independent reference ephemerides and Jyotish
engines — "independent" describes those references, not the authorship
of this repo (see README.md's "Who built this"). It carries no
dependency on, and no reference to, any other ArthIQ Labs product — this
is a fresh codebase, not an export of any private repo's history.

Purpose: a repository anyone can clone and re-run against a named Vedaksha
release, to verify its accuracy claims independently rather than take them
on faith.

## Hard rules here

- **Never modify the `vedaksha` repository from here.** Reading it is fine
  — this project owns it — but every write lands here. If a divergence is
  confirmed and worth fixing, the fix is made in `vedaksha` itself, from a
  laundered report (`FIREWALL.md`), never directly from this repo.
- **Never read a reference engine's source code.** Sealed boxes, all of
  them, and the open-source ones most of all. `FIREWALL.md` rule 1.
- **Never copy a constant, coefficient or table out of a reference engine.**
  Vectors hold computed positions for a moment, never machinery.
- **Never fix Vedaksha to match an oracle.** A divergence is a question
  answered from published theory or the classical text — never from what a
  reference returned.
- **Never state a claim more broadly than what was actually measured.** An
  era bound, a body-set limit, or an open/unresolved item is part of the
  result, not a footnote to omit. This repo exists to be re-run and checked,
  not taken on faith — every generated report states exactly what it did and
  did not test.
- **Never put a secret in argv or commit it.** No API keys are needed for
  the core roster; if one ever is, it goes in `.env`, gitignored.

## Scope discipline

Deterministic quantities only — positions, ayanamsha, cusps, nakshatra,
vargas, dasha boundaries, panchanga, koota cells. Interpretation is out of
scope: yoga qualification, life-event scoring, strength narratives, remedies,
chat. Those have no accuracy oracle; correctness there is faithfulness to the
classical source, verified by reading — not something this harness measures.

## Conventions

- **Python 3.11+.** Matches Vedaksha's own published Python surface
  (`pip install vedaksha`, wasm-backed, `py3-none-any`) and the oracle
  ecosystem, which is Python throughout.
- Type-annotate the public seams. `ruff` + `pytest`.
- An oracle adapter implements the `Oracle` protocol (`src/vedaksha_parity/
  oracles/base.py`) and **raises** on anything it cannot answer. It must
  never return a default — a silent default is indistinguishable from
  agreement, which is the worst possible failure mode for a measuring
  instrument.
- Every run records the Vedaksha version + every oracle's full settings. A
  divergence table without them is uninterpretable a week later.
- Classify every divergence: a documented convention (the two sides answer a
  different, equally legitimate question — ayanamsha choice, node type, year
  length) or genuinely under investigation. Zero divergence on a tier is a
  result to explain, not a reassurance — ask what the tier would have caught
  if something were wrong, and if the answer is nothing, it is not yet a
  test.

## Why the optional AGPL dependencies are compatible

Two of this repo's optional oracle adapters depend on AGPL-licensed
packages in-process (`pyswisseph`, AGPL-3.0-only; `PyJHora`, AGPL-3.0 —
PyPI's own classifier metadata mislabels the latter MIT; the GitHub
repo's About section and license badge are unambiguous and are what this
repo relies on instead). This repo is itself AGPL-3.0-or-later, so
AGPL-on-AGPL is license-compatible with no isolation needed.

This does not affect Vedaksha's own BUSL-1.1 commercial posture: this
repo does not vendor or redistribute Vedaksha's source, only depends on
the published PyPI package like any other consumer, under Vedaksha's own
terms. Copyleft binds this program's own distribution, not a separately-
licensed dependency reached via its published package-manager interface
— the same relationship as any AGPL project depending on a proprietary
database driver or SDK.

## Cleanroom approvals

```yaml
- kind: license
  spdx: AGPL-3.0-only
  reason: >
    `pyswisseph` (AGPL-3.0-only) and `PyJHora` (AGPL-3.0; PyPI's classifier
    metadata mislabels it MIT — the GitHub licence badge is what this repo
    relies on) are optional oracle adapters imported in-process. This repo is
    itself AGPL-3.0-or-later, so AGPL-on-AGPL is natively compatible with no
    subprocess isolation needed — that compatibility is precisely why the repo
    is AGPL rather than the MIT originally asked for.
    It does NOT touch Vedaksha's BUSL-1.1 posture: this repo never vendors or
    redistributes Vedaksha's source, only depends on the published PyPI package
    like any other consumer, under Vedaksha's own terms. Copyleft binds this
    program's own distribution, not a separately-licensed dependency reached
    through its package-manager interface.
    The workspace-wide `forbidden_licenses` gate blocks AGPL to protect that
    BUSL position, which is correct as a default and wrong for this one repo —
    hence a per-repo approval here rather than any change to the global policy.
  approved_by: Amit (originally ratified 2026-08-28 when the AGPL direction was
    chosen; re-ratified 2026-09-03 after this block was found missing from the
    tracked tree — it was recorded in local memory as added-and-verified but
    was lost in one of the three history rewrites this repo went through)
  approved_at: 2026-09-03
```
