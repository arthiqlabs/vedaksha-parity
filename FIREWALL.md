# FIREWALL — the isolation contract

Read this before writing anything in this repo.

## The asset being protected

Vedaksha is a clean-room ephemeris: pure Rust, implemented from published
astronomical theory (VSOP87A, ELP/MPP02, IAU 2006, Meeus, Chapront, Capitaine),
with no Swiss Ephemeris code, headers, constants, algorithms or design patterns
in its lineage. That property is legal and commercial, not aesthetic — it is
what lets Vedaksha be licensed BUSL-1.1 independently of Astrodienst's
AGPL/commercial terms, and it is unrecoverable once lost. A single copied
coefficient table, or a plausible claim that one was copied, contaminates the
whole derivation history of a codebase that took years to build.

Comparing *outputs* does not endanger it. Reading *implementations* does. This
document draws that line concretely, and it holds regardless of whether this
repo is local or public — going public is the plan, not a reason to relax it.

## What this repo is

An independent oracle-parity harness for Vedaksha alone. It installs and
calls reference engines — including Swiss Ephemeris — and compares their
numeric output against Vedaksha's, calling Vedaksha itself through its
published PyPI package, the same way any external consumer would. It is not
a fork, not a rewrite, and not an engine; it computes nothing of its own
beyond arithmetic on two sets of numbers.

It carries no dependency on, and no reference to, any other ArthIQ Labs
product. Findings here are Vedaksha's alone to accept or reject.

## ALLOWED here

- Installing, running and calling Swiss Ephemeris, Skyfield, JPL Horizons,
  jyotishganit, jyotisha, Astronomy Engine, or any other reference engine.
- Naming them openly, in code, docs, commit messages and any published
  report — unlike a private lab, this repo's whole purpose is an open,
  reproducible comparison, so there is no neutral-ID scheme here.
- Recording their numeric output as fixtures, and their configuration
  (ayanamsha selection, node type, house system, year length).
- Citing their published documentation for what a setting means — e.g. which
  ayanamsha variant a flag selects — because that is interface, not internals.
- Reporting that a value and Vedaksha's differ, and by how much.

## FORBIDDEN, here and everywhere

1. **Never read a reference engine's source to learn how it computes.** Not
   to "understand the divergence," not to "check the sign convention," not
   once. Treat every oracle as a sealed box that emits numbers. This includes
   any open-source engine in the roster — open source is the higher hazard,
   not the lower one, because reading it is frictionless and the licence is
   viral.
2. **Never copy a constant, coefficient, polynomial, epoch or table** out of
   a reference engine into anything — not into this repo, not into a note,
   not into a chat message, not into a report. Fixtures record computed
   positions for a given moment, never the machinery that produced them.
3. **Never fix Vedaksha "to match" an oracle.** A divergence is a question.
   The answer is re-derived from published theory or the classical source,
   and the fix cites that. "swisseph says 23.8560" is not a justification
   that may appear in a Vedaksha commit; "IAU 2006 precession applied to the
   Lahiri reference epoch gives ..." is. If the only reason a value looks
   wrong is that an oracle disagrees, the correct next step is to derive it
   independently, not to adopt the oracle's.

## Crossing the boundary

A divergence report may cross from this repo into `vedaksha` itself, and it
must already be laundered when it is written — not laundered on the way out.

- A report states: quantity, Vedaksha's value, the reference value, the
  delta, and the published-theory question the delta raises. It never states
  a reference engine's method.
- Anything that gets filed in `vedaksha` (an issue, a changelog entry, a
  commit) is written from the report, by hand, in that vocabulary, never
  copy-pasted from this repo's own working notes.

## Working directory discipline

This repo does not modify `vedaksha`. It calls Vedaksha's published package
exactly like any external consumer would; it does not check out or edit the
`vedaksha` repository. A fix, if one is warranted, is made in `vedaksha`
itself from the laundered report — never directly from here, which is
exactly the contamination path this document exists to prevent.

## If you are unsure

Stop and check before proceeding. The cost of asking is a message. The
cost of guessing wrong is the clean-room status of the whole ephemeris.
