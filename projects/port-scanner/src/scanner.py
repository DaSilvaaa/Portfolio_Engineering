import argparse
import asyncio
from typing import Optional


COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy",
}


async def grab_banner(reader: asyncio.StreamReader) -> Optional[str]:
    """Tenta ler o banner de apresentação do serviço."""
    try:
        data = await asyncio.wait_for(reader.read(1024), timeout=1.5)
        return data.decode("utf-8", errors="ignore").strip()
    except (asyncio.TimeoutError, Exception):
        return None


async def scan_port(
    host: str,
    port: int,
    semaphore: asyncio.Semaphore,
    timeout: float = 1.0,
) -> Optional[dict]:
    """Tenta estabelecer ligação TCP a uma porta específica com controlo de concorrência."""
    async with semaphore:
        try:
            conn = asyncio.open_connection(host, port)
            reader, writer = await asyncio.wait_for(conn, timeout=timeout)
            banner = await grab_banner(reader)
            writer.close()
            await writer.wait_closed()

            service = COMMON_PORTS.get(port, "Desconhecido")
            return {"port": port, "service": service, "banner": banner}
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return None


async def run_scanner(
    host: str,
    ports: list[int],
    max_concurrency: int = 100,
    timeout: float = 1.0,
) -> list[dict]:
    """Orquestra o scan concorrente sobre uma lista de portas."""
    semaphore = asyncio.Semaphore(max_concurrency)
    tasks = [scan_port(host, port, semaphore, timeout) for port in ports]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Async Port Scanner com deteção de serviços e banners."
    )
    parser.add_argument("host", help="Endereço IP ou hostname alvo (ex: 127.0.0.1)")
    parser.add_argument(
        "--ports",
        "-p",
        default="1-1024",
        help="Gama de portas a analisar (ex: 80,443 ou 1-1024)",
    )
    parser.add_argument(
        "--concurrency",
        "-c",
        type=int,
        default=100,
        help="Número máximo de conexões simultâneas",
    )
    args = parser.parse_args()

    # Converter argumento de portas para lista de inteiros
    port_list = []
    if "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        port_list = list(range(start, end + 1))
    else:
        port_list = [int(p.strip()) for p in args.ports.split(",")]

    print(f"[*] A iniciar scan em {args.host} ({len(port_list)} portas)...")
    open_ports = asyncio.run(run_scanner(args.host, port_list, args.concurrency))

    print(f"\n[+] Portas abertas encontradas ({len(open_ports)}):")
    print(f"{'PORTA':<8} {'SERVIÇO':<15} {'BANNER'}")
    print("-" * 50)
    for p in sorted(open_ports, key=lambda x: x["port"]):
        banner_display = p["banner"] or "N/D"
        print(f"{p['port']:<8} {p['service']:<15} {banner_display[:30]}")


if __name__ == "__main__":
    main()
