import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from main import USERS_DB, app

client = TestClient(app)


def setup_function():
    USERS_DB.clear()


def test_register_and_login_flow():
    # 1. Registar novo utilizador
    reg_res = client.post("/register", json={"username": "diogo", "password": "SafePassword123!"})
    assert reg_res.status_code == 201

    # 2. Login correto
    login_res = client.post("/token", json={"username": "diogo", "password": "SafePassword123!"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert token is not None

    # 3. Aceder a endpoint protegido com o token
    me_res = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "diogo"


def test_login_invalid_credentials():
    client.post("/register", json={"username": "diogo", "password": "SafePassword123!"})
    bad_login = client.post("/token", json={"username": "diogo", "password": "WrongPassword"})
    assert bad_login.status_code == 401


def test_security_headers_present():
    res = client.post("/register", json={"username": "testuser", "password": "SafePassword123!"})
    assert res.headers["X-Frame-Options"] == "DENY"
    assert res.headers["X-Content-Type-Options"] == "nosniff"