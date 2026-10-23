"""Synthetic hourly PV generation with a noisy day-ahead weather forecast."""
import numpy as np
import pandas as pd


def generate_pv_load(days: int = 730, seed: int = 42) -> pd.DataFrame:
    if days < 30:
        raise ValueError("days deve ser >= 30")
    rng = np.random.default_rng(seed)
    n = days * 24
    idx = pd.date_range("2024-01-01", periods=n, freq=pd.Timedelta(hours=1))
    hour, doy = idx.hour.to_numpy(), idx.dayofyear.to_numpy()

    shape = np.clip(np.sin(np.pi * (hour - 6) / 12), 0.0, None)
    season = 1.0 + 0.4 * np.sin(2 * np.pi * (doy - 80) / 365)

    cloud = np.empty(days)
    cloud[0] = 0.7
    for i in range(1, days):
        cloud[i] = np.clip(0.7 + 0.6 * (cloud[i - 1] - 0.7) + rng.normal(0, 0.2), 0.1, 1.0)
    cloud_h = np.repeat(cloud, 24)

    pv = np.clip(5.0 * shape * season * cloud_h * rng.normal(1.0, 0.05, n), 0.0, None)
    forecast = np.clip(cloud_h + np.repeat(rng.normal(0, 0.1, days), 24), 0.0, 1.0)
    temp = (
        15
        + 8 * np.sin(2 * np.pi * (doy - 110) / 365)
        + 4 * np.sin(2 * np.pi * (hour - 9) / 24)
        + 3 * (cloud_h - 0.7)
        + rng.normal(0, 1.0, n)
    )
    return pd.DataFrame({"pv_kw": pv, "cloud_forecast": forecast, "temp_c": temp}, index=idx)
