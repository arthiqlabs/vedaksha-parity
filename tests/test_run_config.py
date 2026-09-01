import pytest

from vedaksha_parity.run_config import load_run_config


def _write(tmp_path, text):
    path = tmp_path / "run.yaml"
    path.write_text(text)
    return path


def test_load_run_config_parses_oracles_tiers_sweep_and_birth_bank(tmp_path):
    path = _write(
        tmp_path,
        """
        oracles:
          - name: swisseph
            ayanamsha_mode: mean
          - name: jyotishganit
            ayanamsha: TrueChitra
            max_charts: 200
          - name: pyjhora
            karaka_scheme: "8"
        tiers: [t1, t2]
        sweep:
          from: 2451545.0
          to: 2451575.0
          step: 30.0
        birth_bank:
          count: 10
          seed: 7
        """,
    )
    config = load_run_config(path)
    assert [o.name for o in config.oracles] == ["swisseph", "jyotishganit", "pyjhora"]
    assert config.oracles[0].ayanamsha is None
    assert config.oracles[0].max_charts is None
    assert config.oracles[0].karaka_scheme is None
    assert config.oracles[0].ayanamsha_mode == "mean"
    assert config.oracles[1].ayanamsha == "TrueChitra"
    assert config.oracles[1].max_charts == 200
    assert config.oracles[2].karaka_scheme == "8"
    assert config.tiers == ["t1", "t2"]
    assert config.sweep.jd_from == 2451545.0
    assert config.sweep.jd_to == 2451575.0
    assert config.sweep.step_days == 30.0
    assert config.birth_bank.count == 10
    assert config.birth_bank.seed == 7


def test_load_run_config_defaults_birth_bank_count_to_full_file(tmp_path):
    path = _write(
        tmp_path,
        """
        oracles: [swisseph]
        tiers: [t1]
        birth_bank: {}
        """,
    )
    config = load_run_config(path)
    assert config.birth_bank.count is None
    assert config.sweep is None


def test_load_run_config_requires_at_least_one_oracle(tmp_path):
    path = _write(tmp_path, "oracles: []\ntiers: [t1]\nsweep: {from: 1.0, to: 2.0}\n")
    with pytest.raises(ValueError):
        load_run_config(path)


def test_load_run_config_requires_at_least_one_tier(tmp_path):
    path = _write(tmp_path, "oracles: [swisseph]\ntiers: []\nsweep: {from: 1.0, to: 2.0}\n")
    with pytest.raises(ValueError):
        load_run_config(path)


def test_load_run_config_requires_sweep_or_birth_bank(tmp_path):
    path = _write(tmp_path, "oracles: [swisseph]\ntiers: [t1]\n")
    with pytest.raises(ValueError):
        load_run_config(path)
