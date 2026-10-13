# AES-256-GCM Vault (Java 17)

Cofre de ficheiros criptográfico com cifra autenticada AES-GCM e derivação com PBKDF2-HMAC-SHA256.

## Funcionalidades
- **Cifra Autenticada:** AES-256-GCM com IV aleatório de 96 bits por ficheiro (impede ataques de repetição e garante autenticidade dos dados).
- **Hardening de Chave:** PBKDF2 com 310.000 iterações e salt de 16 bytes.
- **AAD (Additional Authenticated Data):** Validação de cabeçalho mágico de aplicação (`VLT1`).

## Utilização
```bash
# Executar testes unitários JUnit
mvn test

# Encriptar ficheiro
java -cp target/classes Vault enc segredo.txt segredo.vlt

# Desencriptar ficheiro
java -cp target/classes Vault dec segredo.vlt segredo.txt