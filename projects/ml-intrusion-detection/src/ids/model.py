from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

from ids.data import ATTACK_TYPES, generate_flows
from ids.features import FEATURES, add_features


def _rf(seed: int) -> RandomForestClassifier:
    return RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=seed, n_jobs=1)


def train_eval(n: int = 6000, seed: int = 42, cv: int = 5) -> dict:
    df = add_features(generate_flows(n=n, seed=seed))
    X, y = df[FEATURES], df["label"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)

    rf = _rf(seed).fit(Xtr, ytr)
    proba = rf.predict_proba(Xte)[:, 1]
    pred = (proba >= 0.5).astype(int)

    # Modelo não-supervisionado: treinado exclusivamente com tráfego benigno
    iso = IsolationForest(n_estimators=200, random_state=seed).fit(Xtr[ytr == 0])
    anomaly = -iso.score_samples(Xte)

    types = df.loc[Xte.index, "attack_type"].to_numpy()
    folds = StratifiedKFold(cv, shuffle=True, random_state=seed)
    cv_f1 = cross_val_score(_rf(seed), Xtr, ytr, cv=folds, scoring="f1")
    imp = sorted(zip(FEATURES, rf.feature_importances_), key=lambda t: -t[1])[:5]

    metrics = {
        "n_samples": int(n),
        "seed": int(seed),
        "supervised_random_forest": {
            "precision": float(precision_score(yte, pred)),
            "recall": float(recall_score(yte, pred)),
            "f1": float(f1_score(yte, pred)),
            "roc_auc": float(roc_auc_score(yte, proba)),
            "false_positive_rate": float(pred[types == "benign"].mean()),
            "confusion_matrix": confusion_matrix(yte, pred).tolist(),
            "recall_by_attack_type": {t: float(pred[types == t].mean()) for t in ATTACK_TYPES},
            "cv_f1_mean": float(cv_f1.mean()),
            "cv_f1_std": float(cv_f1.std()),
        },
        "unsupervised_isolation_forest": {"roc_auc": float(roc_auc_score(yte, anomaly))},
        "top_features": {k: float(v) for k, v in imp},
    }
    return {"metrics": metrics, "model": rf, "isolation_forest": iso}