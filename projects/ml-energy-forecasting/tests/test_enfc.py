import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from enfc.data import generate_pv_load  # noqa: E402
from enfc.features import FEATURES, build_features  # noqa: E402
from enfc.model import evaluate  # noqa: E402


def test_generator_is_deterministic_nonnegative_and_dark_at_midnight():
    a, b = generate_pv_load(60, seed=1), generate_pv_load(60, seed=1)
    assert a.equals(b) and len(a) == 60 * 24
    assert (a["pv_kw"] >= 0).all()
    assert (a.loc[a.index.hour == 0, "pv_kw"] == 0).all()


def test_generator_validates_days():
    with pytest.raises(ValueError):
        generate_pv_load(5)


def test_features_have_no_lookahead():
    df = generate_pv_load(120, seed=0)
    k = 80 * 24
    df2 = df.copy()
    df2.iloc[k:, df2.columns.get_loc("pv_kw")] += 100.0
    f1, f2 = build_features(df), build_features(df2)
    cutoff = df.index[k] + pd.Timedelta(hours=24)
    a, b = f1.loc[f1.index < cutoff, FEATURES], f2.loc[f2.index < cutoff, FEATURES]
    assert len(a) > 0
    pd.testing.assert_frame_equal(a, b)


@pytest.fixture(scope="module")
def result():
    return evaluate(days=400, seed=0)


def test_model_beats_both_naive_baselines(result):
    m = result["metrics"]
    assert m["model"]["rmse"] < m["persistence_24h"]["rmse"]
    assert m["model"]["rmse"] < m["seasonal_naive_168h"]["rmse"]
    assert m["skill_vs_persistence_rmse"] > 0.1


def test_split_is_chronological(result):
    te = result["test"]
    n_train = result["metrics"]["n_train"]
    assert result["metrics"]["n_test"] == len(te) and n_train > 0
    assert te.index.is_monotonic_increasing


def test_evaluation_is_reproducible(result):
    assert evaluate(days=400, seed=0)["metrics"] == result["metrics"]
