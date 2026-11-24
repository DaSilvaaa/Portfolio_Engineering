# Software Engineering & Defensive Security Portfolio

Eighteen standalone, tested projects in **Python, Rust, C++, Java and C#**, demonstrating software architecture, concurrent programming, defensive security and Machine Learning. Each project has its own test suite, independent technical documentation and continuous integration on GitHub Actions.

**Author:** Diogo Silva · Computer Engineering & MSc in Sustainable Energy Systems, University of Aveiro  
📄 **Curriculum Vitae:** [Download CV (PDF)](../../releases/latest/download/cv.pdf) *(generated automatically from the source code in [`cv/cv.tex`](cv/cv.tex))*
---

## Featured projects

Three projects published in their own repositories, with tests and CI:

| Project | What it shows |
|---|---|
| [secure-auth-api](https://github.com/DaSilvaaa/secure-auth-api) | Authentication backend (Argon2id, JWT, 2FA, password reset, Docker) |
| [solar-forecast-dashboard](https://github.com/DaSilvaaa/solar-forecast-dashboard) | ML for photovoltaic forecasting with real data and a dashboard |
| [site-security-auditor](https://github.com/DaSilvaaa/site-security-auditor) | Web security audit with a PDF report |

The rest of this repository is my engineering lab: experiments in several languages, each with tests.

---

## Lab: project structure

### 1. Defensive Security and Audit Tools
| Project | Technology | Main Focus |
|---|---|---|
| [secure-web-api](projects/secure-web-api) | Python / FastAPI | Authentication with Argon2id, validated JWT HS256 (anti `alg:none`), enumeration mitigation, rate limiting and STRIDE model |
| [site-auditor](projects/site-auditor) | Python / ReportLab | Header, cookie and TLS audit of a website with a client-ready PDF report |
| [sast-mini](projects/sast-mini) | Python (AST) | Static analyzer with 8 security rules (injection, insecure deserialization, secrets) |
| [port-scanner](projects/port-scanner) | Python (Asyncio) | Concurrent, non-blocking TCP port scanning and banner detection |
| [log-analyzer-siem](projects/log-analyzer-siem) | Python | Detection of SQL injection, path traversal and brute force in web logs, with severity-based alerts |
| [password-auditor](projects/password-auditor) | Python | Password entropy assessment based on character classes |
| [rust-secrets-scanner](projects/rust-secrets-scanner) | Rust | Credential detection via regular expressions and Shannon entropy calculation |
| [rust-integrity-monitor](projects/rust-integrity-monitor) | Rust | File integrity monitoring (FIM) with SHA-256 baselines and tamper detection |
| [csharp-tls-inspector](projects/csharp-tls-inspector) | C# (.NET 8) | Remote audit of X.509 certificates, ciphers and TLS protocol versions |
| [csharp-auth-log-analyzer](projects/csharp-auth-log-analyzer) | C# (.NET 8) | SSH brute-force attack detection using sliding time windows |

### 2. Systems Programming and Concurrency
| Project | Technology | Main Focus |
|---|---|---|
| [cpp-thread-pool](projects/cpp-thread-pool) | C++17 | Generic thread pool with `std::future` and a thread-safe LRU cache (CI with ThreadSanitizer/ASan) |
| [cpp-packet-parser](projects/cpp-packet-parser) | C++17 | PCAP file traffic analysis with strict memory bounds checking and SYN scan detection |
| [java-aes-vault](projects/java-aes-vault) | Java 17 | Secure file encryption with AES-256-GCM, PBKDF2 key derivation and authenticated headers |
| [java-rate-limiter](projects/java-rate-limiter) | Java 17 | Concurrent Token Bucket rate limiter with an injectable clock and per-key isolation |

### 3. Machine Learning & MLOps
| Project | Technology | Main Focus |
|---|---|---|
| [ml-intrusion-detection](projects/ml-intrusion-detection) | Python / Scikit-Learn | Network intrusion detection with Random Forest (supervised) and Isolation Forest (unsupervised) |
| [ml-tabular-pipeline](projects/ml-tabular-pipeline) | Python / Scikit-Learn / FastAPI | Leak-free pipeline, CV-based selection, Model Card and Pydantic API |
| [ml-from-scratch](projects/ml-from-scratch) | Python / NumPy | Linear algebra algorithms implemented from scratch (Linear, Logistic, K-Means, PCA) validated against scikit-learn |
| [`ml-energy-forecasting`](projects/ml-energy-forecasting) | Python / Scikit-Learn | Hourly day-ahead photovoltaic forecasting: look-ahead-free features, chronological time split, naive baselines and skill score. |

---

## Engineering Practices Adopted
- **Unit Tests:** Dozens of automated tests across Pytest, Cargo Test, CTest, Maven Surefire and xUnit.
- **Memory and Data-Race Sanitizers:** C++ thread pool validated in CI with ThreadSanitizer (TSan) and AddressSanitizer (ASan).
- **Secure by Default:** Strict schema validation, modern authenticated ciphers and CI-compatible exit codes.
- **Engineering Documentation:**
  - [Architecture Overview](docs/architecture/overview.md)
  - [Architecture Decision Record (ADR 0001 — Monorepo)](docs/adr/0001-monorepo.md)
  - [STRIDE Threat Modelling of the Web API](docs/threat-models/secure-web-api.md)
  - [Technical Write-up: JWT Pitfalls](docs/writeups/jwt-pitfalls.md)
  - [Technical Write-up: Machine Learning Evaluation Pitfalls](docs/writeups/ml-evaluation-pitfalls.md)

---

## Running the Tests Locally
```bash
# Runs the full suite for the toolchains with a compiler installed locally
bash scripts/verify.sh
```
