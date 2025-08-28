import os
import sys
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ssl_tls_checker import SSLChecker

class SSLCheckerBuilder:
    def __init__(self, hostname):
        # Normalize URL
        parsed = urlparse(hostname)
        if parsed.netloc:
            self.hostname = parsed.netloc
        else:
            self.hostname = parsed.path

    def run(self):
        checker = SSLChecker(self.hostname)
        return checker.check_ssl()


if __name__ == "__main__":
    builder = SSLCheckerBuilder("https://donyapc.ir")
    results = builder.run()
    print(results)
