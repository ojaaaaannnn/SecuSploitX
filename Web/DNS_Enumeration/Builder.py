# Web/DNS_Enumeration/Builder.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Web.DNS_Enumeration.dns_enumeration import DNSEnumerator

class DNSEnumerationBuilder:
    def __init__(self, domain):
        if domain.startswith("http://") or domain.startswith("https://"):
            self.domain = domain.split("://")[1].split("/")[0]
        else:
            self.domain = domain

    def run(self):
        try:
            enumerator = DNSEnumerator(self.domain)
            results = enumerator.enumerate_dns()
            return results
        except Exception as e:
            return {'error': f"DNS Enumeration failed: {str(e)}"}
