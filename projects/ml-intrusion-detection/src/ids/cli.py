import argparse
import json
from pathlib import Path

import joblib

from ids.model import train_eval


def _results_md(m: dict) -> str:
    s, u = m["supervised_random_forest"], m["unsupervised_isolation_forest"]
    rows = [
        "# Results (synthetic data)",
        "",
        f"Samples: {m['n_samples']} · seed: {m['seed']}",
        "",
        "| Model | Precision | Recall | F1 | ROC-AUC | FPR |",
        "|---|---|---|---|---|---|",
        f"| Random Forest (supervised) | {s['precision']:.3f} | {s['recall']:.3f} | {s['f1']:.3f} | {s['roc_auc']:.3f} | {s['false_positive_rate']:.3f} |",
        f"| Isolation Forest (benign-only) | - | - | - | {u['roc_auc']:.3f} | - |",
        "",
        f"5-fold CV F1: {s['cv_f1_mean']:.3f} ± {s['cv_f1_std']:.3f}",
        "",
        "| Attack type | Recall |",
        "|---|---|",
    ]
    rows += [f"| {k} | {v:.3f} |" for k, v in s["recall_by_attack_type"].items()]
    return "\n".join(rows) + "\n"


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Treina e avalia o detetor de intrusões")
    ap.add_argument("--n", type=int, default=6000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="reports")
    a = ap.parse_args(argv)

    r = train_eval(n=a.n, seed=a.seed)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(r["metrics"], indent=2))
    (out / "RESULTS.md").write_text(_results_md(r["metrics"]))
    joblib.dump(r["model"], out / "ids_rf.joblib")
    print(json.dumps(r["metrics"], indent=2))


if __name__ == "__main__":
    main()