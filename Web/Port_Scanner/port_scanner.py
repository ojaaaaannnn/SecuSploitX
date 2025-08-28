# port_scanner.py
import asyncio
from typing import List, Dict

class AsyncPortScanner:
    def __init__(self, target: str, ports: List[int] = None, timeout: float = 1.0):
        self.target = target
        self.ports = ports or list(range(1, 1025))
        self.timeout = timeout
        self.results: List[Dict] = []

    async def _scan_port(self, port: int):
        try:
            conn = asyncio.open_connection(self.target, port)
            reader, writer = await asyncio.wait_for(conn, timeout=self.timeout)
            writer.close()
            await writer.wait_closed()
            self.results.append({"port": port, "status": "open"})
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            self.results.append({"port": port, "status": "closed"})

    async def run_scan(self):
        tasks = [self._scan_port(port) for port in self.ports]
        await asyncio.gather(*tasks)
        return {"target": self.target, "results": self.results}
