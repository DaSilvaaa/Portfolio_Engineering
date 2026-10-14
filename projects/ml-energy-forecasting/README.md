# ml-energy-forecasting

Previsão horária de produção fotovoltaica (day-ahead) com salvaguardas rigorosas contra fuga de dados temporais:

- **Sem antecipação de informação (No look-ahead):** Todas as *features* derivadas de potência possuem um desfasamento de pelo menos 24 horas. Inclui teste unitário que perturba o futuro e valida que as observações passadas permanecem inalteradas.
- **Divisão estritamente cronológica:** O conjunto de teste situa-se exclusivamente após o de treino; a validação cruzada utiliza janelas expansivas com `TimeSeriesSplit`.
- **Estimadores de referência (Baselines):** Comparação face à persistência (t-24h) e sazonal ingénua (t-168h), com avaliação diurna dedicada para evitar distorções induzidas pelos zeros noturnos.

## Execução

```bash
python -m enfc.cli --days 730 --seed 42 --out reports
pytest tests