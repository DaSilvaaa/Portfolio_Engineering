# Model card (diabetes progression regression)

Selected model: **ridge** (by 3-candidate cross-validated RMSE) · seed 42

| Candidate | CV RMSE (mean ± std) |
|---|---|
| ridge | 55.57 ± 1.83 |
| random_forest | 58.38 ± 1.63 |
| gradient_boosting | 61.23 ± 2.65 |

Hold-out: RMSE 53.71 · MAE 42.39 · R² 0.456
Mean-predictor baseline RMSE: 73.22

Top features (permutation importance, RMSE increase):
- s1: 18.89
- s5: 18.01
- bmi: 8.01
- s2: 7.52
- sex: 3.36

Intended use: demonstration of a reproducible pipeline. Not a clinical tool.
