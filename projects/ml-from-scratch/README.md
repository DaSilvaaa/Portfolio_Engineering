# ml-from-scratch

Implementações puras em NumPy dos algoritmos fundamentais de Machine Learning, cada um **rigorosamente validado contra o scikit-learn** nos testes unitários:

| Algoritmo | Implementação Matemática | Validação de Equivalência |
|---|---|---|
| Regressão Linear / Ridge | Equações normais (`lstsq` / `solve`) | Coeficientes e R² iguais ao scikit-learn a 1e-6 |
| Regressão Logística | Batch Gradient Descent com penalização L2 | Acurácia dentro de 2% do scikit-learn, loss monotonicamente decrescente |
| K-Means | Algoritmo de Lloyd com seeding k-means++ | ARI > 0.95 em clusters separados, inércia a <5% do scikit-learn |
| PCA | SVD de dados centrados | Razões de variância e projeções idênticas, reconstrução exata em rank completo |

## Utilização
```bash
pip install -r requirements.txt
pytest tests