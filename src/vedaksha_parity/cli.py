"""Command-line entry point: `vedaksha-parity run --tier t1 --oracle swisseph`,
or `vedaksha-parity run-config path/to/run.yaml` for a full oracle x tier
matrix driven by one config file — see docs/oracles.md and
docs/birth-data.md."""

from __future__ import annotations

import argparse
import inspect
from pathlib import Path
from typing import Any

from vedaksha_parity.birth_bank import (
    build_cases_from_birth_bank,
    load_birth_bank,
    select_birth_bank,
)
from vedaksha_parity.cases import (
    build_cases_combustion,
    build_cases_dasha,
    build_cases_drishti,
    build_cases_karakas,
    build_cases_t1,
    build_cases_t1_tropical,
    build_cases_t2,
)
from vedaksha_parity.engine import Engine
from vedaksha_parity.location_grid import (
    build_cases_ashtakavarga_default_grid,
    build_cases_bhavas_default_grid,
    build_cases_chara_dasha_default_grid,
    build_cases_houses_default_grid,
    build_cases_panchanga_default_grid,
    build_cases_vargas_default_grid,
)
from vedaksha_parity.report import build_run_record, print_summary, write_run, write_run_markdown
from vedaksha_parity.run_config import OracleRunConfig, load_run_config
from vedaksha_parity.runner import run as run_cases

TIER_BUILDERS = {
    "t1": build_cases_t1,
    "t1-tropical": build_cases_t1_tropical,
    "t2": build_cases_t2,
    "karakas": build_cases_karakas,
    "combustion": build_cases_combustion,
    "drishti": build_cases_drishti,
    "dasha": build_cases_dasha,
    "houses": build_cases_houses_default_grid,
    "vargas": build_cases_vargas_default_grid,
    "bhavas": build_cases_bhavas_default_grid,
    "ashtakavarga": build_cases_ashtakavarga_default_grid,
    "panchanga": build_cases_panchanga_default_grid,
    "chara-dasha": build_cases_chara_dasha_default_grid,
}

ORACLE_FACTORIES = {}


def _register_oracles() -> None:
    # Import lazily: an oracle's dependency being absent must not break the
    # CLI's --help or its other oracles.
    factories = {
        "swisseph": ("vedaksha_parity.oracles.swisseph_oracle", "SwissephOracle"),
        "skyfield": ("vedaksha_parity.oracles.skyfield_oracle", "SkyfieldOracle"),
        "inpop": ("vedaksha_parity.oracles.inpop_oracle", "InpopOracle"),
        "astronomy-engine": ("vedaksha_parity.oracles.astronomy_engine_oracle", "AstronomyEngineOracle"),
        "jyotishganit": ("vedaksha_parity.oracles.jyotishganit_oracle", "JyotishganitOracle"),
        "pyjhora": ("vedaksha_parity.oracles.pyjhora_oracle", "PyJHoraOracle"),
    }
    for name, (module_path, class_name) in factories.items():
        try:
            import importlib

            module = importlib.import_module(module_path)
            ORACLE_FACTORIES[name] = getattr(module, class_name)
        except ImportError:
            pass


def main(argv: list[str] | None = None) -> int:
    _register_oracles()
    parser = argparse.ArgumentParser(prog="vedaksha-parity")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="run one tier against one oracle")
    run_parser.add_argument("--tier", choices=sorted(TIER_BUILDERS), required=True)
    run_parser.add_argument("--oracle", choices=sorted(ORACLE_FACTORIES) or ["<none installed>"], required=True)
    run_parser.add_argument("--from", dest="jd_from", type=float, required=True)
    run_parser.add_argument("--to", dest="jd_to", type=float, required=True)
    run_parser.add_argument("--step", dest="step_days", type=float, default=30.0)
    run_parser.add_argument("--out", type=Path, default=Path("results"))

    config_parser = sub.add_parser(
        "run-config", help="run the full oracle x tier matrix described by one YAML config file"
    )
    config_parser.add_argument("config_path", type=Path)
    config_parser.add_argument("--out", type=Path, default=Path("results"))

    args = parser.parse_args(argv)

    if args.command == "run":
        if args.oracle not in ORACLE_FACTORIES:
            parser.error(
                f"oracle {args.oracle!r} is not installed — "
                f"pip install vedaksha-parity[{args.oracle}]"
            )
        cases = TIER_BUILDERS[args.tier](args.jd_from, args.jd_to, args.step_days)
        engine = Engine()
        oracle = ORACLE_FACTORIES[args.oracle]()
        result = run_cases(cases, engine, oracle)
        run_record = build_run_record(
            tier=args.tier,
            engine=engine,
            oracle=oracle,
            case_params={"from": args.jd_from, "to": args.jd_to, "step_days": args.step_days},
            result=result,
        )
        print_summary(run_record)
        path = write_run(run_record, result, args.out)
        md_path = write_run_markdown(run_record, result, args.out)
        print(f"wrote {path}")
        print(f"wrote {md_path}")
    elif args.command == "run-config":
        _run_config(args.config_path, args.out)
    return 0


def _instantiate_oracle(factory: type, oracle_cfg: OracleRunConfig) -> Any:
    # Only pass a field through when the oracle's own constructor declares
    # it (e.g. ayanamsha_mode currently means something only to SwissephOracle).
    kwargs = {}
    params = inspect.signature(factory).parameters
    if oracle_cfg.ayanamsha_mode is not None and "ayanamsha_mode" in params:
        kwargs["ayanamsha_mode"] = oracle_cfg.ayanamsha_mode
    return factory(**kwargs)


def _run_config(config_path: Path, out_dir: Path) -> None:
    config = load_run_config(config_path)

    for oracle_cfg in config.oracles:
        if oracle_cfg.name not in ORACLE_FACTORIES:
            raise SystemExit(
                f"oracle {oracle_cfg.name!r} is not installed — "
                f"pip install vedaksha-parity[{oracle_cfg.name}]"
            )
    for tier in config.tiers:
        if tier not in TIER_BUILDERS:
            raise SystemExit(f"unknown tier {tier!r} — known tiers: {sorted(TIER_BUILDERS)}")

    birth_records = None
    birth_bank_provenance: dict = {}
    if config.birth_bank is not None:
        all_records = load_birth_bank(config.birth_bank.source)
        birth_records, birth_bank_provenance = select_birth_bank(
            all_records, count=config.birth_bank.count, seed=config.birth_bank.seed
        )
        birth_bank_provenance["source"] = str(config.birth_bank.source)

    for oracle_cfg in config.oracles:
        engine = Engine(ayanamsha=oracle_cfg.ayanamsha, karaka_scheme=oracle_cfg.karaka_scheme)
        oracle = _instantiate_oracle(ORACLE_FACTORIES[oracle_cfg.name], oracle_cfg)
        for tier in config.tiers:
            cases = []
            case_params: dict = {}
            if config.sweep is not None:
                cases += TIER_BUILDERS[tier](
                    config.sweep.jd_from, config.sweep.jd_to, config.sweep.step_days
                )
                case_params["sweep"] = {
                    "from": config.sweep.jd_from,
                    "to": config.sweep.jd_to,
                    "step_days": config.sweep.step_days,
                }
            if birth_records is not None:
                cases += build_cases_from_birth_bank(birth_records, tier)
                case_params["birth_bank"] = birth_bank_provenance
            if oracle_cfg.ayanamsha:
                case_params["ayanamsha_override"] = oracle_cfg.ayanamsha

            if oracle_cfg.max_charts is not None:
                distinct_charts = {c["jd_ut"] for c in cases}
                if len(distinct_charts) > oracle_cfg.max_charts:
                    raise SystemExit(
                        f"oracle {oracle_cfg.name!r}, tier {tier!r}: this run would query "
                        f"{len(distinct_charts)} distinct instants, over its configured "
                        f"max_charts={oracle_cfg.max_charts}. Reduce sweep/birth_bank size, "
                        f"or raise max_charts in the config if you deliberately want the "
                        f"larger, slower run."
                    )

            result = run_cases(cases, engine, oracle)
            run_record = build_run_record(
                tier=tier, engine=engine, oracle=oracle, case_params=case_params, result=result
            )
            print_summary(run_record)
            path = write_run(run_record, result, out_dir)
            md_path = write_run_markdown(run_record, result, out_dir)
            print(f"wrote {path}")
            print(f"wrote {md_path}")


if __name__ == "__main__":
    raise SystemExit(main())
