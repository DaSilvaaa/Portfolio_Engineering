# Armadilhas de Avaliação em Machine Learning e Como Evitá-las

Modelos raramente falham devido ao algoritmo em si; falham pela forma como foram medidos. Os projetos deste monorepo aplicam princípios de avaliação rigorosos para mitigar os vieses mais frequentes em ambientes de produção.

## 1. Fuga de Dados (Data Leakage)
Ajustar transformadores (*scalers*, imputadores ou codificadores) antes da divisão entre treino e validação contamina os dados com informação do futuro. No `ml-tabular-pipeline`, o pré-processamento é encapsulado integralmente dentro de um `Pipeline` do scikit-learn: cada *fold* de validação cruzada reajusta transformadores exclusivamente no seu conjunto de treino, tocando no conjunto de teste independente (*hold-out*) uma única vez no final. No `ml-intrusion-detection`, testes unitários asseguram que identificadores e rótulos (`label`, `attack_type`) são excluídos da matriz de atributos.

## 2. Ilusão de Acurácia em Classes Desbalanceadas
Em fluxos de intrusão onde o tráfego malicioso representa apenas 20% do total, um estimador trivial que preveja sempre "tráfego legítimo" obtém 80% de acurácia. O detetor reporta precisão, cobertura (*recall*), $F_1$, ROC-AUC e a taxa de falsos positivos (FPR). Em operações reais de segurança (SOC), a taxa de falsos positivos é prioritária para evitar a saturação de alertas nos analistas.

## 3. Estimadores Basais (Baselines)
Métricas isoladas carecem de significado analítico. O pipeline tabular confronta sempre o modelo final contra um estimador da média (*DummyRegressor*), enquanto o detetor de intrusões compara o modelo supervisionado (*Random Forest*) com um detetor não-supervisionado (*Isolation Forest*) condicionado exclusivamente a tráfego benigno.

## 4. Reprodutibilidade e Rastreabilidade
Sementes pseudoaleatórias (`seed`) são fixadas em todas as rotinas estocásticas, e testes unitários validam a estabilidade das métricas entre execuções distintas. Modelos, métricas estruturadas em JSON e *Model Cards* são gerados através de um único comando.

## 5. Limitações de Dados Sintéticos
A separabilidade perfeita observada em tráfego de rede gerado serve para atestar a robustez do fluxo de treino e teste, e não uma garantia de eficácia operacional face a tráfego real com desvio de distribuição (*concept drift*).

## 6. Verificação Numérica das Implementações
O módulo `ml-from-scratch` testa cada algoritmo desenvolvido em NumPy contra o scikit-learn: coeficientes de regressão com tolerância de $10^{-6}$, projeções PCA invariantes ao sinal e agrupamentos K-Means via *Adjusted Rand Index*.