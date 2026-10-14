import sys
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans as SkKMeans
from sklearn.datasets import make_blobs, make_classification, make_regression
from sklearn.decomposition import PCA as SkPCA
from sklearn.linear_model import LinearRegression as SkLinear
from sklearn.linear_model import LogisticRegression as SkLogistic
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler

# Caminho absoluto robusto para sistemas Windows/Linux
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from mlscratch.kmeans import KMeans  # noqa: E402
from mlscratch.linear import LinearRegression  # noqa: E402
from mlscratch.logistic import LogisticRegression  # noqa: E402
from mlscratch.pca import PCA  # noqa: E402


def test_linear_regression_matches_sklearn():
    X, y = make_regression(n_samples=200, n_features=5, noise=5.0, random_state=0)
    ours, ref = LinearRegression().fit(X, y), SkLinear().fit(X, y)
    assert np.allclose(ours.coef_, ref.coef_, atol=1e-6)
    assert np.isclose(ours.intercept_, ref.intercept_, atol=1e-6)
    assert np.isclose(ours.score(X, y), ref.score(X, y))


def test_ridge_shrinks_coefficients():
    X, y = make_regression(n_samples=100, n_features=5, noise=5.0, random_state=1)
    assert np.linalg.norm(LinearRegression(l2=50.0).fit(X, y).coef_) < np.linalg.norm(LinearRegression().fit(X, y).coef_)


def test_logistic_regression_converges_and_matches_sklearn_accuracy():
    X, y = make_classification(n_samples=500, n_features=5, n_informative=3, random_state=0)
    X = StandardScaler().fit_transform(X)
    ours = LogisticRegression(lr=0.2, n_iter=5000).fit(X, y)
    ref = SkLogistic(C=1e6, max_iter=1000).fit(X, y)
    assert abs((ours.predict(X) == y).mean() - (ref.predict(X) == y).mean()) < 0.02
    assert np.all(np.diff(ours.losses_) <= 1e-12)


def test_kmeans_recovers_well_separated_clusters():
    centers = [[0, 0], [6, 6], [-6, 6]]
    X, y = make_blobs(n_samples=300, centers=centers, cluster_std=0.5, random_state=1)
    km = KMeans(3, n_init=5, seed=0).fit(X)
    assert adjusted_rand_score(y, km.labels_) > 0.95
    assert km.inertia_ <= SkKMeans(3, n_init=10, random_state=0).fit(X).inertia_ * 1.05
    assert (km.predict(X) == km.labels_).all()


def test_pca_matches_sklearn_up_to_sign():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, 6)) @ rng.normal(size=(6, 6))
    ours, ref = PCA(3).fit(X), SkPCA(3).fit(X)
    assert np.allclose(ours.explained_variance_ratio_, ref.explained_variance_ratio_)
    assert np.allclose(np.abs(ours.transform(X)), np.abs(ref.transform(X)), atol=1e-6)


def test_pca_full_rank_reconstruction_is_exact():
    X = np.random.default_rng(1).normal(size=(50, 4))
    p = PCA(4).fit(X)
    assert np.allclose(p.inverse_transform(p.transform(X)), X)