# ml-tabular-pipeline

Pipeline supervisionado de regressão ponta a ponta com o dataset *diabetes* do scikit-learn:

1. **Pré-processamento Isolado:** `ColumnTransformer` (imputação pela mediana + normalização com `StandardScaler` para numéricas, e codificação `OneHotEncoder` com tolerância a categorias desconhecidas).
2. **Seleção de Modelos sem Leakage:** Comparação entre Ridge, Random Forest e Gradient Boosting através de validação cruzada exclusivamente nos dados de treino.
3. **Avaliação Fidedigna:** Teste único do modelo selecionado num conjunto *hold-out* independente comparado com um estimador de média basal (*DummyRegressor*).
4. **Governação e Explicabilidade:** Importância por permutação das variáveis e criação de `MODEL_CARD.md`.
5. **Serviço de Inferência FastAPI:** Endpoint com validação restrita de esquemas em Pydantic (bloqueio de atributos extra e limites de rajada em lote).

## Utilização
```bash
pip install -r requirements.txt
python -m tabpipe.cli --seed 42 --cv 5 --out reports
pytest tests