#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

struct Stat {
    uint64_t pkts = 0;
    uint64_t bytes = 0;
};

static std::string ip4(const uint8_t* p) {
    char b[16];
    std::snprintf(b, sizeof b, "%u.%u.%u.%u", p[0], p[1], p[2], p[3]);
    return b;
}

static uint16_t be16(const uint8_t* p) {
    return static_cast<uint16_t>((p[0] << 8) | p[1]);
}

static uint32_t swap32(uint32_t v) {
    return ((v & 0x000000FFu) << 24) |
           ((v & 0x0000FF00u) << 8)  |
           ((v & 0x00FF0000u) >> 8)  |
           ((v & 0xFF000000u) >> 24);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "uso: " << argv[0] << " <captura.pcap>\n";
        return 2;
    }

    std::ifstream f(argv[1], std::ios::binary);
    if (!f) {
        std::cerr << "erro: não foi possível abrir o ficheiro " << argv[1] << "\n";
        return 2;
    }

    // Leitura do cabeçalho global do PCAP (24 bytes)
    uint8_t gh[24];
    if (!f.read(reinterpret_cast<char*>(gh), sizeof gh)) {
        std::cerr << "erro: cabeçalho pcap inválido ou corrompido\n";
        return 2;
    }

    uint32_t magic = 0, link = 0;
    std::memcpy(&magic, gh, 4);
    bool swapped = (magic == 0xd4c3b2a1u);

    if (magic != 0xa1b2c3d4u && !swapped) {
        std::cerr << "erro: formato pcap não suportado\n";
        return 2;
    }

    std::memcpy(&link, gh + 20, 4);
    if (swapped) link = swap32(link);
    if (link != 1) {
        std::cerr << "erro: apenas linktype Ethernet (1) é suportado\n";
        return 2;
    }

    std::map<std::string, Stat> flows;
    std::map<std::string, std::set<uint16_t>> syn_targets;
    uint64_t total = 0;
    uint8_t ph[16];

    // Iterar por cada pacote no ficheiro
    while (f.read(reinterpret_cast<char*>(ph), sizeof ph)) {
        uint32_t incl = 0;
        std::memcpy(&incl, ph + 8, 4);
        if (swapped) incl = swap32(incl);
        if (incl > 262144) break;

        std::vector<uint8_t> pkt(incl);
        if (!f.read(reinterpret_cast<char*>(pkt.data()), incl)) break;
        ++total;

        // Validar tamanho mínimo para cabeçalho Ethernet + IPv4 e EtherType IPv4 (0x0800)
        if (incl < 34 || be16(&pkt[12]) != 0x0800) continue;

        const uint8_t* ip = &pkt[14];
        size_t ihl = static_cast<size_t>(ip[0] & 0x0f) * 4;
        if (ihl < 20 || 14 + ihl + 4 > incl) continue;

        uint8_t proto = ip[9];
        std::string src = ip4(ip + 12);
        std::string dst = ip4(ip + 16);
        const uint8_t* l4 = ip + ihl;
        uint16_t sp = 0, dp = 0;
        const char* name = "OTHER";

        if (proto == 6 || proto == 17) {
            sp = be16(l4);
            dp = be16(l4 + 2);
            name = (proto == 6) ? "TCP" : "UDP";
        }

        // Deteção de flag TCP SYN (apenas SYN ativo, sem ACK)
        if (proto == 6 && (14 + ihl + 14 <= incl) && ((l4[13] & 0x12) == 0x02)) {
            syn_targets[src].insert(dp);
        }

        std::string flow_key = src + ":" + std::to_string(sp) + " -> " + dst + ":" + std::to_string(dp) + " " + name;
        auto& s = flows[flow_key];
        s.pkts++;
        s.bytes += incl;
    }

    std::cout << "Pacotes lidos: " << total << " | Fluxos identificados: " << flows.size() << "\n\n";
    std::cout << "Top 10 fluxos por bytes transferidos:\n";

    std::vector<std::pair<std::string, Stat>> v(flows.begin(), flows.end());
    std::sort(v.begin(), v.end(), [](const auto& a, const auto& b) {
        return a.second.bytes > b.second.bytes;
    });

    for (size_t i = 0; i < v.size() && i < 10; ++i) {
        std::cout << "  " << v[i].first
                  << "  pkts=" << v[i].second.pkts
                  << "  bytes=" << v[i].second.bytes << "\n";
    }

    bool alert = false;
    for (const auto& [src, ports] : syn_targets) {
        if (ports.size() >= 20) {
            if (!alert) std::cout << "\nALERTAS DE SEGURANÇA:\n";
            alert = true;
            std::cout << "  [!] Possível SYN scan detetado de " << src
                      << " (" << ports.size() << " portas distintas visadas)\n";
        }
    }

    return alert ? 1 : 0;
}