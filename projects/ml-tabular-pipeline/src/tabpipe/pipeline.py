"""Reproducible regression pipeline: preprocessing, model selection by CV, honest hold-out evaluation."""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CATEGORICAL = ["bmi_band"]
_BMI_CUTS = np.quantile(load_diabetes().data[:, 2], [1 / 3, 2 / 3])


def add_bmi_band(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["bmi_band"] = np.select(
        [out["bmi"] < _BMI_CUTS[0], out["bmi"] < _BMI_CUTS[1]],
        ["low", "mid"],
        default="high",
    )
    return out


def load_data():
    d = load_diabetes(as_frame=True)
    return add_bmi_band(d.data), d.target


def build_pipeline(model, X: pd.DataFrame) -> Pipeline:
    numeric = [c for c in X.columns if c not in CATEGORICAL]
    prep = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    return Pipeline([("prep", prep), ("model", model)])


def candidates(seed: int, n_estimators: int = 200) -> dict:
    return {
        "ridge": Ridge(alpha=1.0),
        "random_forest": RandomForestRegressor(n_estimators=n_estimators, min_samples_leaf=3, random_state=seed, n_jobs=1),
        "gradient_boosting": GradientBoostingRegressor(random_state=seed),
    }


def _rmse(y, p) -> float:
    return float(np.sqrt(mean_squared_error(y, p)))


def run(seed: int = 42, cv: int = 5, n_estimators: int = 200) -> dict:
    X, y = load_data()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=seed)
    folds = KFold(cv, shuffle=True, random_state=seed)

    cv_results = {}
    for name, model in candidates(seed, n_estimators).items():
        s = cross_val_score(build_pipeline(model, Xtr), Xtr, ytr, cv=folds, scoring="neg_root_mean_squared_error")
        cv_results[name] = {"cv_rmse_mean": float(-s.mean()), "cv_rmse_std": float(s.std())}

    best = min(cv_results, key=lambda k: cv_results[k]["cv_rmse_mean"])
    pipe = build_pipeline(candidates(seed, n_estimators)[best], Xtr).fit(Xtr, ytr)
    pred = pipe.predict(Xte)
    baseline = DummyRegressor().fit(Xtr, ytr).predict(Xte)

    perm = permutation_importance(
        pipe,
        Xte,
        yte,
        n_repeats=10,
        random_state=seed,
        scoring="neg_root_mean_squared_error",
        n_jobs=1,
    )
    top = sorted(zip(Xte.columns, perm.importances_mean), key=lambda t: -t[1])[:5]

    return {
        "cv": cv_results,
        "best_model": best,
        "holdout": {
            "rmse": _rmse(yte, pred),
            "mae": float(mean_absolute_error(yte, pred)),
            "r2": float(r2_score(yte, pred)),
        },
        "baseline_rmse": _rmse(yte, baseline),
        "permutation_importance_rmse": {k: float(v) for k, v in top},
        "seed": seed,
        "pipeline": pipe,
    }


def save(result: dict, outdir: str = "reports") -> None:
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    joblib.dump(result["pipeline"], out / "model.joblib")
    metrics = {k: v for k, v in result.items() if k != "pipeline"}
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    h = result["holdout"]
    lines = [
        "# Model card (diabetes progression regression)",
        "",
        f"Selected model: **{result['best_model']}** (by {len(result['cv'])}-candidate cross-validated RMSE) · seed {result['seed']}",
        "",
        "| Candidate | CV RMSE (mean ± std) |",
        "|---|---|",
    ]
    lines += [f"| {k} | {v['cv_rmse_mean']:.2f} ± {v['cv_rmse_std']:.2f} |" for k, v in result["cv"].items()]
    lines += [
        "",
        f"Hold-out: RMSE {h['rmse']:.2f} · MAE {h['mae']:.2f} · R² {h['r2']:.3f}",
        f"Mean-predictor baseline RMSE: {result['baseline_rmse']:.2f}",
        "",
        "Top features (permutation importance, RMSE increase):",
    ]
    lines += [f"- {k}: {v:.2f}" for k, v in result["permutation_importance_rmse"].items()]
    lines += ["", "Intended use: demonstration of a reproducible pipeline. Not a clinical tool."]
    (out / "MODEL_CARD.md").write_text("\n".join(lines) + "\n")