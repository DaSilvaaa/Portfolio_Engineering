# File Integrity Monitor (Rust)

Monitor de integridade de ficheiros recursivo baseado em SHA-256 com deteção de alterações de estado.

## Objetivo
Criar uma baseline criptográfica do sistema de ficheiros e auditar desvios de integridade (ficheiros adicionados, modificados ou removidos).

## Utilização
```bash
# Registar o estado inicial (baseline)
cargo run --release -- baseline ./alvo baseline.txt

# Verificar se houve adulterações (exit code 1 se houver alterações)
cargo run --release -- verify ./alvo baseline.txt

# Executar testes unitários
cargo test