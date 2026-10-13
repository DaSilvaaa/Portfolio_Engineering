import asyncio
import sys
from pathlib import Path

# Adicionar pasta src ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scanner import scan_port, run_scanner


async def _run_server_and_test(test_callback):
    """Cria um servidor TCP temporário e executa a verificação."""
    async def handle_client(reader, writer):
        writer.write(b"SSH-2.0-OpenSSH_9.0\r\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    server = await asyncio.start_server(handle_client, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    try:
        await test_callback("127.0.0.1", port)
    finally:
        server.close()
        await server.wait_closed()


def test_scan_port_open():
    async def verify(host, port):
        semaphore = asyncio.Semaphore(10)
        result = await scan_port(host, port, semaphore, timeout=1.0)
        assert result is not None
        assert result["port"] == port
        assert "SSH-2.0" in (result["banner"] or "")

    asyncio.run(_run_server_and_test(verify))


def test_scan_port_closed():
    async def verify():
        semaphore = asyncio.Semaphore(10)
        # Testa uma porta que tipicamente está fechada
        return await scan_port("127.0.0.1", 1, semaphore, timeout=0.2)

    result = asyncio.run(verify())
    assert result is None


def test_run_scanner():
    async def verify(host, open_port):
        ports = [open_port, 1, 3]
        results = await run_scanner(host, ports, max_concurrency=5, timeout=0.5)
        assert len(results) == 1
        assert results[0]["port"] == open_port

    asyncio.run(_run_server_and_test(verify))