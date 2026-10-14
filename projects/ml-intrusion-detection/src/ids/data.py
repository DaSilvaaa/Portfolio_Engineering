"""Synthetic network-flow generator (benign traffic + three attack families)."""
import numpy as np
import pandas as pd

ATTACK_TYPES = ("portscan", "dos", "bruteforce")


def _benign(rng: np.random.Generator, n: int) -> pd.DataFrame:
    return pd.DataFrame({
        "duration": rng.gamma(2.0, 2.0, n),
        "src_bytes": rng.lognormal(7.0, 1.0, n),
        "dst_bytes": rng.lognormal(8.0, 1.2, n),
        "packets": rng.poisson(20, n) + 1,
        "distinct_ports": rng.integers(1, 4, n),
        "syn_ratio": rng.beta(2, 20, n),
        "failed_logins": rng.poisson(0.1, n),
        "label": 0,
        "attack_type": "benign",
    })


def _attack(rng: np.random.Generator, kind: str, n: int) -> pd.DataFrame:
    if kind == "portscan":
        d = dict(
            duration=rng.gamma(1.0, 0.5, n),
            src_bytes=rng.lognormal(4.5, 0.5, n),
            dst_bytes=rng.lognormal(3.5, 0.8, n),
            packets=rng.poisson(60, n) + 1,
            distinct_ports=rng.integers(30, 500, n),
            syn_ratio=rng.beta(20, 2, n),
            failed_logins=rng.poisson(0.05, n),
        )
    elif kind == "dos":
        d = dict(
            duration=rng.gamma(1.5, 0.5, n),
            src_bytes=rng.lognormal(11.0, 0.7, n),
            dst_bytes=rng.lognormal(4.0, 1.0, n),
            packets=rng.poisson(5000, n) + 1,
            distinct_ports=np.ones(n, dtype=int),
            syn_ratio=rng.beta(10, 3, n),
            failed_logins=np.zeros(n, dtype=int),
        )
    elif kind == "bruteforce":
        d = dict(
            duration=rng.gamma(3.0, 3.0, n),
            src_bytes=rng.lognormal(7.5, 0.5, n),
            dst_bytes=rng.lognormal(7.0, 0.5, n),
            packets=rng.poisson(40, n) + 1,
            distinct_ports=np.ones(n, dtype=int),
            syn_ratio=rng.beta(2, 15, n),
            failed_logins=rng.poisson(25, n) + 5,
        )
    else:
        raise ValueError(f"tipo de ataque desconhecido: {kind}")

    d["label"] = np.ones(n, dtype=int)
    d["attack_type"] = [kind] * n
    return pd.DataFrame(d)


def generate_flows(n: int = 6000, attack_fraction: float = 0.2, seed: int = 42) -> pd.DataFrame:
    if n < 10:
        raise ValueError("n deve ser >= 10")
    if not 0.0 < attack_fraction < 1.0:
        raise ValueError("attack_fraction deve estar em (0, 1)")

    rng = np.random.default_rng(seed)
    n_att = int(n * attack_fraction)
    base = n_att // 3
    counts = [base, base, n_att - 2 * base]
    frames = [_benign(rng, n - n_att)]
    frames += [_attack(rng, k, c) for k, c in zip(ATTACK_TYPES, counts)]

    df = pd.concat(frames, ignore_index=True)
    return df.sample(frac=1.0, random_state=seed).reset_index(drop=True)