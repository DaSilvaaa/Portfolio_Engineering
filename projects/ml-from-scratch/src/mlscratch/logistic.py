import numpy as np


def sigmoid(z):
    return 0.5 * (1.0 + np.tanh(0.5 * z))


class LogisticRegression:
    """Binary logistic regression trained with batch gradient descent."""

    def __init__(self, lr: float = 0.1, n_iter: int = 2000, l2: float = 0.0, tol: float = 1e-10):
        self.lr, self.n_iter, self.l2, self.tol = lr, n_iter, l2, tol

    def fit(self, X, y):
        X, y = np.asarray(X, float), np.asarray(y, float)
        n, d = X.shape
        w, b = np.zeros(d), 0.0
        eps, losses = 1e-12, []
        for _ in range(self.n_iter):
            p = sigmoid(X @ w + b)
            loss = -np.mean(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps)) + 0.5 * self.l2 * (w @ w)
            if losses and abs(losses[-1] - loss) < self.tol:
                losses.append(loss)
                break
            losses.append(loss)
            w -= self.lr * (X.T @ (p - y) / n + self.l2 * w)
            b -= self.lr * np.mean(p - y)
        self.coef_, self.intercept_, self.losses_ = w, b, np.array(losses)
        return self

    def predict_proba(self, X):
        return sigmoid(np.asarray(X, float) @ self.coef_ + self.intercept_)

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)
