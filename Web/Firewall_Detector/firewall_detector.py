import socket
import subprocess
import platform
from urllib.parse import urlparse

class FirewallDetector:
    def __init__(self, target="127.0.0.1", tcp_ports=None, udp_ports=None):
        self.target_input = target
        self.tcp_ports = tcp_ports if tcp_ports else [
            20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 111, 135, 137, 138, 139,
            143, 161, 162, 389, 443, 445, 465, 587, 636, 993, 995, 1433, 1521, 1723,
            2049, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9000, 9090
        ]

        self.udp_ports = udp_ports if udp_ports else [
            53, 67, 68, 69, 123, 161, 162, 500, 514, 520, 623, 33434
        ]
        self.results = {}
        self.target_ip = self.resolve_target(target)

    def resolve_target(self, target):
        try:
            parsed = urlparse(target)
            host = parsed.netloc or parsed.path
            ip = socket.gethostbyname(host)
            return ip
        except Exception as e:
            raise ValueError(f"Cannot resolve target '{target}': {e}")

    def check_tcp_ports(self):
        for port in self.tcp_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            try:
                sock.connect((self.target_ip, port))
                self.results[f"TCP {port}"] = "Open"
            except (socket.timeout, ConnectionRefusedError, OSError):
                self.results[f"TCP {port}"] = "Blocked/Closed"
            finally:
                sock.close()

    def check_udp_ports(self):
        for port in self.udp_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.5)
            try:
                sock.sendto(b"test", (self.target_ip, port))
                self.results[f"UDP {port}"] = "Open/Filtered"
            except Exception:
                self.results[f"UDP {port}"] = "Blocked"
            finally:
                sock.close()

    def check_icmp(self):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", self.target_ip]
        try:
            subprocess.check_output(command)
            self.results["ICMP"] = "Allowed"
        except subprocess.CalledProcessError:
            self.results["ICMP"] = "Blocked"

    def scan(self):
        self.check_tcp_ports()
        self.check_udp_ports()
        self.check_icmp()
        return self.results
