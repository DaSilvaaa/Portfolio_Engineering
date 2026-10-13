# Software Engineering & Cybersecurity Portfolio

[![CI](https://github.com/DaSilvaaa/Portfolio_Engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/DaSilvaaa/Portfolio_Engineering/actions/workflows/ci.yml)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

Monorepo focado no desenvolvimento de ferramentas defensivas de cibersegurança, criptografia aplicada, análise de tráfego de rede e arquiteturas de software seguras.

---

## 🛠️ Matriz de Projetos

| Projeto | Linguagem / Stack | Domínio de Segurança | Testes Automatizados |
|---|---|---|:---:|
| [secure-web-api](projects/secure-web-api) | Python / FastAPI, Pydantic | AppSec, OWASP Hardening, Rate Limiting, JWT | `pytest` |
| [port-scanner](projects/port-scanner) | Python / `asyncio`, Sockets | Network Recon, Concorrência TCP, Banner Grabbing | `pytest` |
| [log-analyzer-siem](projects/log-analyzer-siem) | Python / Regex, Dataclasses | Threat Detection, SQLi, Path Traversal, Brute Force | `pytest` |
| [password-auditor](projects/password-auditor) | Python / Math, CLI | Entropia de Shannon, Avaliação de Força Bruta | `pytest` |
| [rust-integrity-monitor](projects/rust-integrity-monitor) | Rust / SHA-256, BTreeMap | File Integrity Monitoring (FIM), Baseline & Diff | `cargo test` |
| [csharp-auth-log-analyzer](projects/csharp-auth-log-analyzer) | C# (.NET 8) / LINQ, Regex | Análise Forense de Logs SSH, Sliding Window | `xUnit` |
| [cpp-packet-parser](projects/cpp-packet-parser) | C++17 / CMake, POSIX | Dissecação Binária PCAP, Deteção de SYN Scans | Compilação CMake |
| [java-aes-vault](projects/java-aes-vault) | Java 17 / JCA, Maven | Cifra Autenticada AES-256-GCM, PBKDF2, AAD | `JUnit 5` |

---

## 🚀 Integração Contínua (CI/CD)

O repositório possui uma pipeline automatizada no **GitHub Actions** que valida a integridade de todas as suites de testes a cada alteração:
- **Python:** Execução de testes unitários e de integração com `pytest`.
- **Rust:** Verificação de integridade e suites unitárias com `cargo test`.
- **C#:** Validação de regras de janela deslizante com `xUnit`.
- **C++:** Compilação com flags rigorosas (`-Wall -Wextra -Wpedantic`).
- **Java:** Testes criptográficos de cifra, autenticação e resistência a adulteração com `JUnit 5`.

---

## 📬 Contacto
- **Autor:** Diogo Silva
- **Email:** diogo.eduardo.taveira.silva@gmail.com
- **GitHub:** [@DaSilvaaa](https://github.com/DaSilvaaa)