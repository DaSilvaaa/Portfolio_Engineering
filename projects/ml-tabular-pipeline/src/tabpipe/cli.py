import argparse
import json

from tabpipe.pipeline import run, save


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Treina, seleciona e avalia o pipeline de regressão")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--cv", type=int, default=5)
    ap.add_argument("--out", default="reports")
    a = ap.parse_args(argv)
    r = run(seed=a.seed, cv=a.cv)
    save(r, a.out)
    print(json.dumps({k: v for k, v in r.items() if k != "pipeline"}, indent=2))


if __name__ == "__main__":
    main()