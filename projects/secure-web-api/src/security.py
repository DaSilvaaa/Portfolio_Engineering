import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Optional

SECRET_KEY = "super-secret-key-change-in-production"
TOKEN_EXPIRY_SECONDS = 3600  # 1 hora


def hash_password(password: str) -> str:
    """Gera hash seguro com PBKDF2-HMAC-SHA256 e salt de 16 bytes."""
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return f"{salt.hex()}:{key.hex()}"


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Valida a password com comparação em tempo constante (mitiga timing attacks)."""
    try:
        salt_hex, key_hex = stored_password.split(":")
        salt = bytes.fromhex(salt_hex)
        expected_key = bytes.fromhex(key_hex)
        test_key = hashlib.pbkdf2_hmac("sha256", provided_password.encode(), salt, 100_000)
        return hmac.compare_digest(expected_key, test_key)
    except Exception:
        return False


def create_access_token(username: str) -> str:
    """Cria um token HMAC assinado com expiração."""
    payload = {
        "sub": username,
        "exp": int(time.time()) + TOKEN_EXPIRY_SECONDS,
    }
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    signature = hmac.new(SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{signature}"


def verify_access_token(token: str) -> Optional[str]:
    """Verifica a assinatura do token e valida o prazo de expiração."""
    try:
        payload_b64, signature = token.split(".")
        expected_signature = hmac.new(SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_signature, signature):
            return None

        # Recompor padding de Base64 se necessário
        padded = payload_b64 + "=" * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())

        if time.time() > payload["exp"]:
            return None

        return payload["sub"]
    except Exception:
        return None