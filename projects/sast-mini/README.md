# sast-mini

Analisador estático de segurança (SAST) para código Python baseado na árvore sintática abstrata (`ast`).

## Regras Implementadas
- **SAST001:** `eval()` / `exec()` (execução arbitrária de código)
- **SAST002:** `os.system()` (risco de injeção de comandos)
- **SAST003:** `subprocess` com `shell=True`
- **SAST004:** `pickle` e `marshal` (desserialização insegura)
- **SAST005:** Algoritmos de hash vulneráveis (`md5`, `sha1`)
- **SAST006:** `yaml.load()` sem SafeLoader
- **SAST007:** Validação TLS desativada (`verify=False`)
- **SAST008:** Segredos e senhas hardcoded em variáveis

## Utilização
```bash
# Analisar código e devolver relatório em JSON
python src/sast.py . --fail-on medium --json

# Executar testes unitários
python -m pytest tests/