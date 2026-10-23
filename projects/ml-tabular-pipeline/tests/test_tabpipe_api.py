import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sklearn.linear_model import Ridge

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tabpipe.api import create_app  # noqa: E402
from tabpipe.pipeline import build_pipeline, load_data  # noqa: E402

VALID = {
    "age": 0.03, "sex": 0.05, "bmi": 0.06, "bp": 0.02, "s1": -0.04,
    "s2": -0.03, "s3": -0.04, "s4": 0.0, "s5": 0.02, "s6": -0.02
}


@pytest.fixture(scope="module")
def client():
    X, y = load_data()
    return TestClient(create_app(build_pipeline(Ridge(), X).fit(X, y)))


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_predict_batch(client):
    r = client.post("/predict", json={"instances": [VALID, {**VALID, "bmi": -0.05}]})
    assert r.status_code == 200 and len(r.json()["predictions"]) == 2


@pytest.mark.parametrize("payload", [
    {"instances": []},
    {"instances": [VALID] * 101},
    {"instances": [{**VALID, "bmi": 9.0}]},
    {"instances": [{**VALID, "extra": 1}]},
    {"instances": [{k: v for k, v in VALID.items() if k != "bp"}]},
    {"unexpected": 1},
])
def test_invalid_payloads_rejected(client, payload):
    assert client.post("/predict", json=payload).status_code == 422
