# Secure Web API (FastAPI & OWASP Hardening)

API RESTful segura construída com FastAPI focada em boas práticas de Application Security (AppSec).

## Funcionalidades de Segurança
- **PBKDF2-HMAC-SHA256:** Hashing de passwords com salts criptográficos únicos e 100.000 iterações.
- **Timing Attack Mitigation:** Comparação constante com `hmac.compare_digest`.
- **HMAC Access Tokens:** Tokens de autorização assinados digitalmente com expiração.
- **HTTP Security Headers:** Injeção de cabeçalhos recomendados pela OWASP (`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `HSTS`).
- **Rate Limiting:** Prevenção básica de força bruta baseada no IP de origem.

## Execução e Testes

```bash
# Executar a suite de testes automatizados
python -m pytest projects/secure-web-api/tests/