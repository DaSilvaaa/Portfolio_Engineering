# Auth Log Brute-Force Detector (C# .NET 8)

Deteção de ataques de força bruta em logs de autenticação SSH (`auth.log`) através de janelas deslizantes (*sliding window*).

## Objetivo
Analisar tentativas falhadas de autenticação por IP, correlacionando o número de infrações dentro de um intervalo de tempo configurável (por exemplo, 5 falhas em 60 segundos).

## Utilização
```bash
# Executar análise num ficheiro auth.log
dotnet run -- /var/log/auth.log 5 60

# Executar a suite de testes unitários xUnit
dotnet test tests