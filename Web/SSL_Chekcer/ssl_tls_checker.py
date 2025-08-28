import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse


class SSLChecker:
    def __init__(self, hostname):
        parsed = urlparse(hostname)
        if parsed.netloc:
            self.hostname = parsed.netloc
        else:
            self.hostname = parsed.path

        self.context = ssl.create_default_context()

    def check_ssl(self):
        try:
            with socket.create_connection((self.hostname, 443), timeout=10) as sock:
                with self.context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()

                    cert_info = self.parse_certificate(cert)

                    ssl_version = ssock.version()
                    cipher = ssock.cipher()

                    return {
                        'hostname': self.hostname,
                        'ssl_version': ssl_version,
                        'cipher': cipher,
                        'certificate': cert_info,
                        'valid': True,
                        'error': None
                    }

        except ssl.SSLError as e:
            return {
                'hostname': self.hostname,
                'valid': False,
                'error': f"SSL Error: {str(e)}"
            }
        except socket.error as e:
            return {
                'hostname': self.hostname,
                'valid': False,
                'error': f"Connection Error: {str(e)}"
            }
        except Exception as e:
            return {
                'hostname': self.hostname,
                'valid': False,
                'error': f"Unexpected Error: {str(e)}"
            }

    def parse_certificate(self, cert):
        cert_info = {}

        subject = dict(x[0] for x in cert.get('subject', []))
        cert_info['subject'] = subject

        issuer = dict(x[0] for x in cert.get('issuer', []))
        cert_info['issuer'] = issuer

        not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
        not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        cert_info['valid_from'] = not_before.isoformat()
        cert_info['valid_to'] = not_after.isoformat()
        cert_info['days_until_expiry'] = (not_after - datetime.now()).days

        san = []
        for field in cert.get('subjectAltName', []):
            san.append(field[1])
        cert_info['subject_alt_names'] = san

        return cert_info


if __name__ == "__main__":
    checker = SSLChecker("https://example.com")
    results = checker.check_ssl()
    print(results)
