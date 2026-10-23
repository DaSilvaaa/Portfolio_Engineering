# Secure Web API (FastAPI & OWASP Hardening)

API de autenticação em FastAPI focada em Application Security. Modelo de ameaças: [`docs/threat-models/secure-web-api.md`](../../docs/threat-models/secure-web-api.md).

## Funcionalidades de segurança
- **Argon2id** (`argon2-cffi`) para hashing de passwords.
- **JWT HS256 real** (`pyjwt`) com `algorithms=["HS256"]` explícito (bloqueia `alg: none`), claims `exp`, `sub`, `iat` e `jti` obrigatórios/gerados, TTL de 15 minutos.
- **Chave por variável de ambiente:** `SECRET_KEY` (≥ 32 caracteres). A aplicação recusa arrancar sem ela.
- **Sem enumeração de utilizadores:** `/register` responde sempre igual; `/token` executa sempre o Argon2 (hash simulado quando o utilizador não existe).
- **Rate limiting** por IP (20 pedidos/min) com memória limitada (`MAX_TRACKED_IPS`).
- **Security headers:** `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy`, `HSTS`.

## Executar
```bash
cd projects/secure-web-api
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
uvicorn main:app --app-dir src
```

## Testes
```bash
python -m pytest projects/secure-web-api/tests/
```
Cobrem: fluxo registo/login, `alg: none`, token expirado, adulterado, assinado com outra chave, sem `exp`, enumeração no registo, igualização de tempo no login, Argon2id, chave em falta e rate limit.

## Docker
```bash
docker build -t secure-web-api .
docker run -e SECRET_KEY="$SECRET_KEY" -p 8000:8000 secure-web-api
```

## Limitações conhecidas
Armazenamento em memória (demonstração), rate limiter por processo e sem revogação de tokens. Em produção: base de dados, Redis para rate limit/revogação por `jti`.
