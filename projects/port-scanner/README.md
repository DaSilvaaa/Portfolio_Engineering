# Async TCP Port Scanner

Scanner de portas TCP concorrente e não bloqueante desenvolvido em Python utilizando `asyncio`.

## Objetivo
Demonstrar a implementação de um utilitário de reconhecimento de rede com controlo de concorrência via semáforos assíncronos (`asyncio.Semaphore`) e recolha de banners de serviços em portas abertas.

## Características
- **Execução Concorrente:** Capaz de testar milhares de portas em segundos sem bloquear a thread principal.
- **Deteção de Banners:** Extração do handshake inicial de protocolos comuns (SSH, FTP, HTTP).
- **Controlo de Concorrência:** Evita sobrecarga de descritores de ficheiros e bloqueio da rede através de semáforos.

## Utilização

```bash
# Analisar as primeiras 1024 portas do localhost
python src/scanner.py 127.0.0.1 -p 1-1024

# Analisar portas específicas
python src/scanner.py 127.0.0.1 -p 80,443,22,8080