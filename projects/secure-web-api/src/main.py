import time
from collections import defaultdict
from fastapi import FastAPI, HTTPException, Request, Response, status
from pydantic import BaseModel, Field

from security import (
    create_access_token,
    hash_password,
    verify_access_token,
    verify_password,
)

app = FastAPI(title="Secure Web API", version="1.0.0")

# Base de dados em memória para demonstração
USERS_DB: dict[str, str] = {}
RATE_LIMIT_DB: dict[str, list[float]] = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 20


class UserAuth(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """Aplica rate limiting e injeta Security Headers (OWASP)."""
    ip = request.client.host if request.client else "unknown"
    now = time.time()

    # Limpar tentativas com mais de 60 segundos
    RATE_LIMIT_DB[ip] = [t for t in RATE_LIMIT_DB[ip] if now - t < 60]
    if len(RATE_LIMIT_DB[ip]) >= MAX_REQUESTS_PER_MINUTE:
        return Response(content="Demasiados pedidos. Tente mais tarde.", status_code=429)
    RATE_LIMIT_DB[ip].append(now)

    response = await call_next(request)
    # Security Headers recomendados pela OWASP
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'none'"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserAuth):
    if user.username in USERS_DB:
        raise HTTPException(status_code=400, detail="Utilizador já registado.")
    USERS_DB[user.username] = hash_password(user.password)
    return {"message": "Utilizador registado com sucesso."}


@app.post("/token")
def login(user: UserAuth):
    stored_hash = USERS_DB.get(user.username)
    if not stored_hash or not verify_password(stored_hash, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}


@app.get("/me")
def get_current_user(request: Request):
    authorization = request.headers.get("authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou mal formatado.")

    token = authorization.split(" ")[1]
    username = verify_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    return {"username": username, "status": "authenticated"}