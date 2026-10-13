# PCAP Packet Parser & SYN Scan Detector (C++17)

Parser binário de tráfego de rede PCAP de baixo nível para agregação de fluxos e deteção de varrimentos TCP SYN.

## Objetivo
Analisar capturas de tráfego de rede (formato `.pcap`) sem recurso a bibliotecas externas pesadas, dissecando frames Ethernet, pacotes IPv4 e datagramas TCP/UDP diretamente a partir dos bytes brutos.

## Funcionalidades
- **Parser Binário PCAP:** Suporta ordenação de bytes nativa e invertida (*endianness* swap).
- **Agregação de Sessões:** Mapeamento de fluxos bidirecionais por endereços IP, portas de origem/destino e protocolo de transporte.
- **Detetor de Reconhecimento:** Alerta automático se um endereço IP de origem enviar pacotes TCP SYN para 20 ou mais portas distintas.

## Compilação e Execução
```bash
# Configurar e compilar com CMake
cmake -S . -B build && cmake --build build

# Analisar um ficheiro de captura
./build/packet_parser captura.pcap