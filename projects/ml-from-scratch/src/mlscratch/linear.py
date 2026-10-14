import numpy as np


class LinearRegression:
    """Ordinary / ridge least squares (intercept is never penalised)."""

    def __init__(self, l2: float = 0.0):
        self.l2 = l2

    def fit(self, X, y):
        X, y = np.asarray(X, float), np.asarray(y, float)
        Xb = np.hstack([np.ones((len(X), 1)), X])
        if self.l2 == 0.0:
            theta = np.linalg.lstsq(Xb, y, rcond=None)[0]
        else:
            reg = self.l2 * np.eye(Xb.shape[1])
            reg[0, 0] = 0.0
            theta = np.linalg.solve(Xb.T @ Xb + reg, Xb.T @ y)
        self.intercept_, self.coef_ = float(theta[0]), theta[1:]
        return self

    def predict(self, X):
        return np.asarray(X, float) @ self.coef_ + self.intercept_

    def score(self, X, y):
        y = np.asarray(y, float)
        ss_res = ((y - self.predict(X)) ** 2).sum()
        return 1.0 - ss_res / ((y - y.mean()) ** 2).sum()