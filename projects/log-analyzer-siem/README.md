# Log Analyzer (mini-SIEM)

Analisa entradas de logs web e deteta SQL injection, path traversal e força bruta por IP (limiar configurável), devolvendo alertas `SecurityAlert` com severidade.

```python
from analyzer import LogAnalyzer
LogAnalyzer(brute_force_threshold=5).analyze_web_log_entry("1.2.3.4", "/?q=' OR '1'='1", 200)
```

```bash
python -m pytest projects/log-analyzer-siem/tests -q
```

**Limitação:** deteção baseada em expressões regulares; sujeita a falsos positivos/negativos.
