# csharp-tls-inspector

Auditoria de endpoints TLS: verificação de expiração, tamanho de chaves criptográficas, algoritmo de assinatura, protocolo negociado e integridade da cadeia de certificação.

## Funcionalidades
- **Inspeção de Handshake:** Suporte para verificação remota de múltiplos alvos em simultâneo.
- **Deteção de Vulnerabilidades:** Alertas sobre protocolos legados (TLS 1.0, 1.1) e algoritmos de hash fracos (MD5, SHA-1).
- **Relatório JSON:** Formato estruturado para integração contínua e monitorização defensiva.

## Utilização
```bash
# Auditar servidores remotos (exit code 1 se houver problemas de segurança)
dotnet run -- example.com github.com:443

# Executar suite de testes unitários xUnit
dotnet test tests