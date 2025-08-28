from firewall_detector import FirewallDetector
from datetime import datetime

class ReportBuilder:
    def __init__(self, target_ip="127.0.0.1"):
        self.detector = FirewallDetector(target_ip)
        self.report = {}

    def build_report(self):
        print(f"\n🔥 Starting firewall scan on {self.detector.target_ip}...\n")
        self.report = self.detector.scan()
        self.display_report()

    def display_report(self):
        print("===== FIREWALL REPORT =====")
        for k, v in self.report.items():
            print(f"{k:<10} : {v}")
        print(f"===== Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====\n")

if __name__ == "__main__":
    builder = ReportBuilder()
    builder.build_report()
