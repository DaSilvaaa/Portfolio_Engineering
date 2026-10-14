# Software Engineering & Defensive Security Portfolio

Quinze projetos autónomos e testados em **Python, Rust, C++, Java e C#**, demonstrando arquitetura de software, programação concorrente, segurança defensiva e Machine Learning. Cada projeto contém a sua própria suite de testes, documentação técnica independente e integração contínua no GitHub Actions.

**Autor:** Diogo Silva · Engenharia de Computadores e Informática / Engenharia Computacional, Universidade de Aveiro

---

## Estrutura do Portfólio

### 1. Segurança Defensiva e Ferramentas de Auditoria
| Projeto | Tecnologia | Foco Principal |
|---|---|---|
| [secure-web-api](projects/secure-web-api) | Python / FastAPI | Autenticação robusta (scrypt, mitigação de enumeração, rate limiting, JWT endurecido) e modelo STRIDE |
| [sast-mini](projects/sast-mini) | Python (AST) | Analisador estático com 8 regras de segurança (injeção, deserialização insegura, segredos) |
| [port-scanner](projects/port-scanner) | Python (Asyncio) | Varrimento concorrente não-bloqueante de portas TCP e deteção de banners |
| [password-auditor](projects/password-auditor) | Python | Avaliação de entropia de palavras-passe baseada em classes de carateres |
| [rust-secrets-scanner](projects/rust-secrets-scanner) | Rust | Deteção de credenciais via expressões regulares e cálculo de entropia de Shannon |
| [rust-integrity-monitor](projects/rust-integrity-monitor) | Rust | Monitorização de integridade de ficheiros (FIM) com baselines SHA-256 e deteção de adulterações |
| [csharp-tls-inspector](projects/csharp-tls-inspector) | C# (.NET 8) | Auditoria remota de certificados X.509, cifras e versões de protocolo TLS |
| [csharp-auth-log-analyzer](projects/csharp-auth-log-analyzer) | C# (.NET 8) | Deteção de ataques de força bruta SSH via janelas temporais deslizantes |

### 2. Programação de Sistemas e Concorrência
| Projeto | Tecnologia | Foco Principal |
|---|---|---|
| [cpp-thread-pool](projects/cpp-thread-pool) | C++17 | Thread pool genérico com `std::future` e cache LRU thread-safe (testado com ThreadSanitizer/ASan) |
| [cpp-packet-parser](projects/cpp-packet-parser) | C++17 | Análise de tráfego de ficheiros PCAP com verificação estrita de limites de memória e deteção de SYN scans |
| [java-aes-vault](projects/java-aes-vault) | Java 17 | Cifragem segura de ficheiros com AES-256-GCM, derivação PBKDF2 e cabeçalhos autenticados |
| [java-rate-limiter](projects/java-rate-limiter) | Java 17 | Limitador de débito (Token Bucket) concorrente com relógio injetável e isolamento por chave |

### 3. Machine Learning & MLOps
| Projeto | Tecnologia | Foco Principal |
|---|---|---|
| [ml-intrusion-detection](projects/ml-intrusion-detection) | Python / Scikit-Learn | Deteção de intrusões em rede via Random Forest (supervisionado) e Isolation Forest (não-supervisionado) |
| [ml-tabular-pipeline](projects/ml-tabular-pipeline) | Python / Scikit-Learn / FastAPI | Pipeline estanque sem fuga de dados (*leak-free*), seleção por CV, Model Card e API com Pydantic |
| [ml-from-scratch](projects/ml-from-scratch) | Python / NumPy | Algoritmos implementados de raiz em álgebra linear (Linear, Logistic, K-Means, PCA) validados contra scikit-learn |

---

## Boas Práticas de Engenharia Adotadas
- **Testes Unitários:** Mais de 60 testes automatizados distribuídos por Pytest, Cargo Test, CTest, Maven Surefire e xUnit.
- **Sanitizers de Memória e Corridas de Dados:** Validação de C++ com ThreadSanitizer (TSan) e AddressSanitizer (ASan).
- **Segurança por Defeito:** Validação estrita de esquemas, cifras modernas autenticadas e códigos de saída compatíveis com CI.
- **Documentação de Engenharia:**
  - [Visão Geral de Arquitetura](docs/architecture/overview.md)
  - [Registo de Decisão de Arquitetura (ADR 0001 — Monorepo)](docs/adr/0001-monorepo.md)
  - [Modelação de Ameaças STRIDE da Web API](docs/threat-models/secure-web-api.md)
  - [Ensaio Técnico: Armadilhas em JWT](docs/writeups/jwt-pitfalls.md)
  - [Ensaio Técnico: Armadilhas de Avaliação em Machine Learning](docs/writeups/ml-evaluation-pitfalls.md)

---

## Execução Local dos Testes
```bash
# Executa a suite completa em ferramentas com compilador instalado localmente
bash scripts/verify.sh