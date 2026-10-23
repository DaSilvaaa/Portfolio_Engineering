import numpy as np


class PCA:
    """Principal component analysis via SVD of the centred data."""

    def __init__(self, n_components: int):
        self.n_components = n_components

    def fit(self, X):
        X = np.asarray(X, float)
        self.mean_ = X.mean(axis=0)
        _, S, Vt = np.linalg.svd(X - self.mean_, full_matrices=False)
        var = S ** 2 / (len(X) - 1)
        k = self.n_components
        self.components_ = Vt[:k]
        self.explained_variance_ = var[:k]
        self.explained_variance_ratio_ = var[:k] / var.sum()
        return self

    def transform(self, X):
        return (np.asarray(X, float) - self.mean_) @ self.components_.T

    def inverse_transform(self, Z):
        return np.asarray(Z, float) @ self.components_ + self.mean_
