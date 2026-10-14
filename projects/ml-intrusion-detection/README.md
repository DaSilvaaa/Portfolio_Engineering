# ml-intrusion-detection

Deteção de intrusões em fluxos de rede combinando duas abordagens complementares:

- **Supervisionada:** Random Forest com pesos balanceados para identificação de varrimentos de portas, DoS e força bruta SSH.
- **Não-Supervisionada:** Isolation Forest treinado exclusivamente com tráfego benigno, emulando um cenário operacional onde rótulos de novos ataques não existem.

A avaliação afere precisão, cobertura (recall), F1, ROC-AUC, taxa de falsos positivos e validação cruzada estratificada.

## Utilização
```bash
pip install -r requirements.txt
python -m ids.cli --n 6000 --seed 42 --out reports
pytest tests