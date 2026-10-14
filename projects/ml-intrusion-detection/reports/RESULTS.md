# Results (synthetic data)

Samples: 6000 · seed: 42

| Model | Precision | Recall | F1 | ROC-AUC | FPR |
|---|---|---|---|---|---|
| Random Forest (supervised) | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| Isolation Forest (benign-only) | - | - | - | 0.995 | - |

5-fold CV F1: 0.998 ± 0.002

| Attack type | Recall |
|---|---|
| portscan | 1.000 |
| dos | 1.000 |
| bruteforce | 1.000 |
