# Password Auditor

Estima a entropia de palavras-passe (em bits) a partir das classes de caracteres usadas e classifica-as como fraca, razoável, forte ou muito forte.

```bash
printf 'abc123\nCorrectHorse!Battery9\n' | python projects/password-auditor/src/audit.py
python -m pytest projects/password-auditor/tests -q
```

**Limitação:** a entropia por classes é uma estimativa otimista; não deteta palavras de dicionário nem padrões previsíveis.
