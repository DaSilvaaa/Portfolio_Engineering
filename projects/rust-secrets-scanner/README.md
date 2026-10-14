# rust-secrets-scanner

Scanner recursivo em Rust para deteção de segredos expostos em repositórios de código.

## Funcionalidades
- **Deteção por Padrão:** Chaves de API AWS (`AKIA...`), tokens do GitHub (`ghp_...`), Slack e blocos de chave privada PEM.
- **Deteção por Entropia:** Cálculo de Entropia de Shannon em strings atribuídas a chaves comuns (`secret`, `token`, `password`).
- **Sanitização de Saída:** Segredos são redigidos no terminal para evitar fugas acidentais em logs de CI.
- **Supressão:** Comentários com `scanner:ignore` na mesma linha ignoram o alerta.

## Utilização
```bash
# Executar auditoria recursiva (exit code 1 se encontrar segredos)
cargo run --release -- .

# Executar testes unitários
cargo test