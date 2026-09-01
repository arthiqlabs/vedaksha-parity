# The birth-data bank

Every run compares Vedaksha and an oracle at real, independently-verified
birth instants — not only the synthetic sweep grid `cases.py` already
generates. This is a second, complementary case source.

## Source and attribution

[`vedastro-org/15000-Famous-People-Birth-Date-Location`](https://huggingface.co/datasets/vedastro-org/15000-Famous-People-Birth-Date-Location)
on Hugging Face, created and published by **VedAstro** ([vedastro.org](https://vedastro.org)).
15,807 rows: name, gender, birth date/time/timezone-offset, location name,
latitude, longitude, and a Rodden reliability rating sourced from birth
certificates or birth records. The dataset's own card states each date,
location, and timezone was verified against paid geocoding APIs.

**License: MIT**, as stated on the dataset's own Hugging Face page and in
its README. Chosen deliberately: an MIT-licensed dataset carries no
copyleft obligation on this repo (itself AGPL-3.0-or-later) and no
restriction on redistributing it — verified before adoption, not assumed.
The dataset repository does not publish a separate `LICENSE` file or a
formal copyright-holder legal name beyond the MIT designation and the
VedAstro/vedastro.org branding shown throughout it — attribution here is
to VedAstro by that name, matching what the source itself publishes, not
a fabricated legal entity.

This dataset is bundled into this repo (`data/vedastro-15000-famous-births.csv`,
see Pinning below) rather than only linked, so this notice is the
attribution the MIT license calls for on redistribution — credit to
VedAstro for creating and publishing it, no claim of authorship by this
project.

This is data — computed positions of a moment in the outside world, birth
records of real people — never a reference engine's implementation.
`FIREWALL.md` rule 1 (never read a reference engine's source) does not apply
to it; it is not sourced from, and carries no lineage relationship to, any
oracle in `docs/oracles.md`.

## Data quality

The source has 17 of its 15,807 rows as literal placeholder entries
(`Name`/`Location` both `"Empty"`) that parse to a syntactically valid but
meaningless date — every one lands on the same instant, `jd_ut=1721425.5`,
near year 1 CE, nothing a "15,000 famous people" dataset would genuinely
contain. `load_birth_bank` filters these at load time; every other row is
passed through unfiltered. This is the harness's own dataset-hygiene
step, not a correction to the dataset itself — the bundled snapshot is
unmodified.

## Pinning

The CSV is bundled into this repo at `data/vedastro-15000-famous-births.csv`
as a **frozen snapshot**, not fetched at run time. If the upstream dataset on
Hugging Face changes or grows, this repo's copy does not silently drift —
any resync is a deliberate, reviewed update, same discipline as an oracle
version pin in `pyproject.toml`.

## Dev / validation / holdout split

`birth_bank.split_birth_bank(records, ratios={...}, seed=...)` partitions
the bank into named buckets (e.g. `dev`/`validation`/`holdout`) — a
permanent, once-and-forever split, not a fresh sample per run. This
exists because a fixed sample that gets repeatedly examined and fixed
against (this project's own canonical 200-record run, `seed=42`, is
exactly that) stops behaving like an independent validation set the more
it's used that way — a real methodological risk a rigor-focused harness
should name rather than let go unremarked. `dev` is safe to inspect
routinely during implementation work; `holdout` is meant to be run, not
read case-by-case, so it keeps evidentiary weight the others lose with
repeated use.

The partition is a pure function of each record's own `row_key` and
`seed` (SHA256-based, not cryptographic — just a stable, well-distributed
hash), never file order or position, so it's reproducible without storing
an explicit ID list and stays stable even if the source CSV is later
resorted or extended.

## Config schema

```yaml
birth_bank:
  source: data/vedastro-15000-famous-births.csv   # default: the bundled pinned snapshot.
                                                     # Point elsewhere to test against a
                                                     # different birth-data file entirely —
                                                     # any CSV with the same columns.
  count: null                                       # null/omitted = 100% of source. This is
                                                     # the default, and what this repo's own
                                                     # published runs use — full-file coverage,
                                                     # not a sample.
  seed: null                                        # only consulted when count < the source's
                                                     # full size. If blank, a seed is generated
                                                     # and recorded in the run's case_params —
                                                     # never silently used and thrown away —
                                                     # so a sampled run stays exactly
                                                     # reproducible from what it reports, the
                                                     # same standard `cases.py`'s sweep grid
                                                     # already holds itself to.
```

Sampling is never restricted — any tester can request any count with any
seed, or none at all, or point `source` at an entirely different file after
forking this repo. What is fixed is that whatever actually ran gets written
down: `count`, `seed`, and `source` all land in `case_params` in the run
record, next to `from`/`to`/`step` for the sweep grid.

## Converting a birth record to `jd_ut`

Local birth date + time + timezone offset → UTC → Julian Day, using the
standard published Julian Date conversion (Meeus, *Astronomical Algorithms*,
or any equivalent astronomical reference) — textbook arithmetic, not
anything sourced from an oracle. No third-party ephemeris library is
required for this step.
