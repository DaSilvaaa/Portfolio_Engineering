import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tabpipe.pipeline import candidates, load_data, run, save  # noqa: E402


@pytest.fixture(scope="module")
def result():
    return run(seed=0, cv=3, n_estimators=100)


def test_best_model_is_a_candidate_with_lowest_cv_rmse(result):
    assert result["best_model"] in candidates(0)
    best = result["cv"][result["best_model"]]["cv_rmse_mean"]
    assert best == min(v["cv_rmse_mean"] for v in result["cv"].values())


def test_model_beats_mean_baseline_on_holdout(result):
    assert result["holdout"]["rmse"] < result["baseline_rmse"]
    assert result["holdout"]["r2"] > 0.3


def test_run_is_reproducible(result):
    again = run(seed=0, cv=3, n_estimators=100)
    assert again["holdout"] == result["holdout"] and again["best_model"] == result["best_model"]


def test_pipeline_handles_unseen_category(result):
    X, _ = load_data()
    row = X.iloc[[0]].copy()
    row["bmi_band"] = "unknown"
    assert len(result["pipeline"].predict(row)) == 1


def test_save_writes_artifacts(result, tmp_path):
    save(result, str(tmp_path))
    assert {"model.joblib", "metrics.json", "MODEL_CARD.md"} <= {p.name for p in tmp_path.iterdir()}
    assert "pipeline" not in (tmp_path / "metrics.json").read_text()