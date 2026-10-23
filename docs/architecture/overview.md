# Visão Geral de Arquitetura

Monorepo poliglota (ver [ADR 0001](../adr/0001-monorepo.md)): cada projeto em `projects/<nome>` é autónomo, com dependências, testes e README próprios.

| Área | Projetos | Linguagens |
|---|---|---|
| Segurança defensiva | secure-web-api, sast-mini, port-scanner, password-auditor, log-analyzer-siem, rust-*, csharp-* | Python, Rust, C# |
| Sistemas e concorrência | cpp-thread-pool, cpp-packet-parser, java-* | C++, Java |
| Machine Learning | ml-* | Python |

## Princípios
- **Isolamento:** sem código partilhado entre projetos; cada um compila e testa sozinho.
- **CI por projeto** (`.github/workflows/ci.yml`) mais lint (`ruff`) e verificações de segurança (`security.yml`: gitleaks, Trivy, pip-audit, cargo-audit).
- **Execução local:** `scripts/verify.sh` corre as suites cujas ferramentas estejam instaladas.
