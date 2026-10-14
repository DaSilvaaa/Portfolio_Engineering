import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from enfc.model import evaluate  # noqa: E402


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Previsão day-ahead de produção fotovoltaica")
    ap.add_argument("--days", type=int, default=730)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="reports")
    a = ap.parse_args(argv)
    r = evaluate(days=a.days, seed=a.seed)
    m, out = r["metrics"], Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(m, indent=2))

    rows = [
        "# Results (synthetic data, day-ahead PV forecast)",
        "",
        f"Train {m['n_train']} h · test {m['n_test']} h (strictly later in time) · seed {m['seed']}",
        "",
        "| Forecaster | MAE (kW) | RMSE (kW) | MAE daylight (kW) |",
        "|---|---|---|---|",
    ]
    for k, label in [
        ("model", "HistGradientBoosting"),
        ("persistence_24h", "Persistence (t-24h)"),
        ("seasonal_naive_168h", "Seasonal naive (t-168h)"),
    ]:
        s = m[k]
        rows.append(f"| {label} | {s['mae']:.3f} | {s['rmse']:.3f} | {s['mae_daylight']:.3f} |")
    rows += [
        "",
        f"RMSE skill vs persistence: **{m['skill_vs_persistence_rmse']:.1%}**",
        f"Time-series CV MAE (3 expanding folds): {m['cv_mae_mean']:.3f} ± {m['cv_mae_std']:.3f}",
    ]
    (out / "RESULTS.md").write_text("\n".join(rows) + "\n")

    week = r["test"].iloc[:168]
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.plot(week.index, week["target"], label="actual")
    ax.plot(week.index, week["pred"], label="forecast", linestyle="--")
    ax.set_ylabel("PV power (kW)")
    ax.set_title("Day-ahead forecast, first test week")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "forecast_week.png", dpi=120)
    print(json.dumps(m, indent=2))


if __name__ == "__main__":
    main()