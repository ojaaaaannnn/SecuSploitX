# Builder.py
import asyncio
import os
import sys
from typing import List, Union
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from port_scanner import AsyncPortScanner

class PortScannerBuilder:
    def __init__(self, target: str, ports: Union[List[int], int, None] = None, timeout: float = 1.0):
        self.target = target
        self.timeout = timeout

        if ports is None:
            self.ports = list(range(1, 1025))
        elif isinstance(ports, int):
            self.ports = list(range(1, ports + 1))
        else:
            self.ports = ports

    def run(self):
        scanner = AsyncPortScanner(target=self.target, ports=self.ports, timeout=self.timeout)
        return asyncio.run(scanner.run_scan())
