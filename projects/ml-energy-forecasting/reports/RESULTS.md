# Results (synthetic data, day-ahead PV forecast)

Train 13881 h · test 3471 h (strictly later in time) · seed 42

| Forecaster | MAE (kW) | RMSE (kW) | MAE daylight (kW) |
|---|---|---|---|
| HistGradientBoosting | 0.128 | 0.250 | 0.254 |
| Persistence (t-24h) | 0.262 | 0.528 | 0.523 |
| Seasonal naive (t-168h) | 0.348 | 0.692 | 0.694 |

RMSE skill vs persistence: **52.6%**
Time-series CV MAE (3 expanding folds): 0.168 ± 0.041
