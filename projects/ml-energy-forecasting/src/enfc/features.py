import numpy as np
import pandas as pd

LAGS = (24, 48, 168)
FEATURES = (
    ["hour_sin", "hour_cos", "doy_sin", "doy_cos", "temp_c", "cloud_forecast"]
    + [f"pv_lag_{lag}" for lag in LAGS]
    + ["pv_roll24_lag24"]
)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Day-ahead features: every PV-derived column is lagged by at least 24 h (no look-ahead)."""
    out = pd.DataFrame(index=df.index)
    h, d = df.index.hour.to_numpy(), df.index.dayofyear.to_numpy()
    out["hour"] = h
    out["hour_sin"], out["hour_cos"] = np.sin(2 * np.pi * h / 24), np.cos(2 * np.pi * h / 24)
    out["doy_sin"], out["doy_cos"] = np.sin(2 * np.pi * d / 365), np.cos(2 * np.pi * d / 365)
    out["temp_c"], out["cloud_forecast"] = df["temp_c"], df["cloud_forecast"]
    for lag in LAGS:
        out[f"pv_lag_{lag}"] = df["pv_kw"].shift(lag)
    out["pv_roll24_lag24"] = df["pv_kw"].shift(24).rolling(24).mean()
    out["target"] = df["pv_kw"]
    return out.dropna()
