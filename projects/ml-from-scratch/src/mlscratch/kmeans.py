import numpy as np


class KMeans:
    """Lloyd's algorithm with k-means++ seeding and multiple restarts."""

    def __init__(self, k: int, n_init: int = 5, max_iter: int = 300, tol: float = 1e-6, seed: int = 0):
        self.k, self.n_init, self.max_iter, self.tol, self.seed = k, n_init, max_iter, tol, seed

    @staticmethod
    def _d2(X, C):
        return ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)

    def _seed_pp(self, X, rng):
        centers = [X[rng.integers(len(X))]]
        for _ in range(1, self.k):
            d2 = self._d2(X, np.array(centers)).min(axis=1)
            total = d2.sum()
            idx = rng.choice(len(X), p=d2 / total) if total > 0 else rng.integers(len(X))
            centers.append(X[idx])
        return np.array(centers)

    def _run(self, X, rng):
        C = self._seed_pp(X, rng)
        for _ in range(self.max_iter):
            labels = self._d2(X, C).argmin(axis=1)
            new = np.array([X[labels == j].mean(axis=0) if (labels == j).any() else C[j] for j in range(self.k)])
            shift = np.linalg.norm(new - C)
            C = new
            if shift < self.tol:
                break
        d2 = self._d2(X, C)
        return C, d2.argmin(axis=1), float(d2.min(axis=1).sum())

    def fit(self, X):
        X = np.asarray(X, float)
        if not 1 <= self.k <= len(X):
            raise ValueError("k inválido")
        rng = np.random.default_rng(self.seed)
        best = min((self._run(X, rng) for _ in range(self.n_init)), key=lambda r: r[2])
        self.cluster_centers_, self.labels_, self.inertia_ = best
        return self

    def predict(self, X):
        return self._d2(np.asarray(X, float), self.cluster_centers_).argmin(axis=1)