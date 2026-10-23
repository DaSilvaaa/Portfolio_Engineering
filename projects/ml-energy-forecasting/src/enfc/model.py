import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

from enfc.data import generate_pv_load
from enfc.features import FEATURES, build_features


def _scores(y, p, daylight) -> dict:
    err = y - p
    return {
        "mae": float(np.abs(err).mean()),
        "rmse": float(np.sqrt((err**2).mean())),
        "mae_daylight": float(np.abs(err[daylight]).mean()),
    }


def make_model(seed: int) -> HistGradientBoostingRegressor:
    return HistGradientBoostingRegressor(
        max_iter=200, learning_rate=0.05, early_stopping=False, random_state=seed
    )


def evaluate(days: int = 730, seed: int = 42, test_frac: float = 0.2, cv: int = 3, df=None) -> dict:
    """Avalia o modelo; usa `df` (dados reais) se fornecido, senão gera dados sintéticos."""
    data = generate_pv_load(days, seed) if df is None else df
    days = len(data) // 24
    feat = build_features(data)
    cut = int(len(feat) * (1 - test_frac))
    tr, te = feat.iloc[:cut], feat.iloc[cut:]

    cv_mae = -cross_val_score(
        make_model(seed),
        tr[FEATURES],
        tr["target"],
        cv=TimeSeriesSplit(cv),
        scoring="neg_mean_absolute_error",
    )
    model = make_model(seed).fit(tr[FEATURES], tr["target"])
    pred = np.clip(model.predict(te[FEATURES]), 0.0, None)

    y = te["target"].to_numpy()
    day = ((te["hour"] >= 7) & (te["hour"] <= 18)).to_numpy()
    m = {
        "model": _scores(y, pred, day),
        "persistence_24h": _scores(y, te["pv_lag_24"].to_numpy(), day),
        "seasonal_naive_168h": _scores(y, te["pv_lag_168"].to_numpy(), day),
    }
    m["skill_vs_persistence_rmse"] = float(1 - m["model"]["rmse"] / m["persistence_24h"]["rmse"])
    m.update(
        cv_mae_mean=float(cv_mae.mean()),
        cv_mae_std=float(cv_mae.std()),
        n_train=int(len(tr)),
        n_test=int(len(te)),
        days=int(days),
        seed=int(seed),
    )
    return {"metrics": m, "model": model, "test": te.assign(pred=pred)}
