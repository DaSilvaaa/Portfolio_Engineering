import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ids.data import ATTACK_TYPES, generate_flows  # noqa: E402
from ids.features import FEATURES, add_features  # noqa: E402
from ids.model import train_eval  # noqa: E402


def test_generator_is_deterministic_and_seed_sensitive():
    a, b, c = generate_flows(500, seed=1), generate_flows(500, seed=1), generate_flows(500, seed=2)
    assert a.equals(b)
    assert not a.equals(c)


def test_generator_attack_fraction_and_types():
    df = generate_flows(1000, attack_fraction=0.3, seed=0)
    assert len(df) == 1000
    assert df["label"].sum() == 300
    assert set(df.loc[df.label == 1, "attack_type"]) == set(ATTACK_TYPES)


def test_generator_validates_arguments():
    with pytest.raises(ValueError):
        generate_flows(5)
    with pytest.raises(ValueError):
        generate_flows(100, attack_fraction=1.5)


def test_features_are_finite_and_leak_free():
    df = add_features(generate_flows(500, seed=3))
    assert np.isfinite(df[FEATURES].to_numpy()).all()
    assert "label" not in FEATURES and "attack_type" not in FEATURES


@pytest.fixture(scope="module")
def result():
    return train_eval(n=3000, seed=0, cv=3)


def test_supervised_model_detects_all_attack_families(result):
    s = result["metrics"]["supervised_random_forest"]
    assert s["precision"] >= 0.95 and s["recall"] >= 0.95
    assert s["false_positive_rate"] <= 0.03
    assert all(v >= 0.9 for v in s["recall_by_attack_type"].values())


def test_unsupervised_baseline_is_better_than_chance(result):
    assert result["metrics"]["unsupervised_isolation_forest"]["roc_auc"] >= 0.85


def test_training_is_reproducible(result):
    again = train_eval(n=3000, seed=0, cv=3)
    assert again["metrics"] == result["metrics"]