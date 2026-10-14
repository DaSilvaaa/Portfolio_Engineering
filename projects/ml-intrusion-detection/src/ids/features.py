import numpy as np
import pandas as pd

RAW = ["duration", "src_bytes", "dst_bytes", "packets", "distinct_ports", "syn_ratio", "failed_logins"]
FEATURES = RAW + ["bytes_per_packet", "byte_ratio", "log_packets"]


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["bytes_per_packet"] = (out["src_bytes"] + out["dst_bytes"]) / out["packets"].clip(lower=1)
    out["byte_ratio"] = out["src_bytes"] / (out["dst_bytes"] + 1.0)
    out["log_packets"] = np.log1p(out["packets"])
    return out