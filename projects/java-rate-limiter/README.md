# java-rate-limiter

Biblioteca de rate limiting baseada no algoritmo Token Bucket, thread-safe, com relógio injetável e suporte a limitação por chave (IP/utilizador).

## Funcionalidades
- **Token Bucket Thread-Safe:** Controlo preciso de rajadas e débito contínuo com operações atómicas.
- **Relógio Injetável:** Testes determinísticos rápidos através de `LongSupplier` sem recorrer a `Thread.sleep`.
- **Keyed Rate Limiting:** Mapeamento concorrente de quotas independentes por identificador único.

## Utilização
```bash
# Executar suite de testes unitários e de concorrência com Maven
mvn test