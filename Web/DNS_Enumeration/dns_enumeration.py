import dns.resolver
import dns.reversename
import socket


class DNSEnumerator:
    def __init__(self, domain):
        self.domain = domain
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5

    def enumerate_dns(self):
        results = {
            'domain': self.domain,
            'a_records': self.get_a_records(),
            'aaaa_records': self.get_aaaa_records(),
            'mx_records': self.get_mx_records(),
            'ns_records': self.get_ns_records(),
            'txt_records': self.get_txt_records(),
            'cname_records': self.get_cname_records(),
            'soa_record': self.get_soa_record(),
            'ptr_records': self.get_ptr_records(),
            'srv_records': self.get_srv_records()
        }
        return results

    def get_a_records(self):
        try:
            answers = self.resolver.resolve(self.domain, 'A')
            return [str(r) for r in answers]
        except:
            return []

    def get_aaaa_records(self):
        try:
            answers = self.resolver.resolve(self.domain, 'AAAA')
            return [str(r) for r in answers]
        except:
            return []

    def get_mx_records(self):
        try:
            answers = self.resolver.resolve(self.domain, 'MX')
            return [f"{r.preference} {r.exchange}" for r in answers]
        except:
            return []

    def get_ns_records(self):
        try:
            answers = self.resolver.resolve(self.domain, 'NS')
            return [str(r) for r in answers]
        except:
            return []

    def get_txt_records(self):
        try:
            answers = self.resolver.resolve(self.domain, 'TXT')
            return [str(r) for r in answers]
        except:
            return []

    def get_cname_records(self):
        try:
            answers = self.resolver.resolve(self.domain, 'CNAME')
            return [str(r) for r in answers]
        except:
            return []

    def get_soa_record(self):
        try:
            answers = self.resolver.resolve(self.domain, 'SOA')
            return str(answers[0])
        except:
            return None

    def get_ptr_records(self):
        try:
            ptr_records = {}
            a_records = self.get_a_records()
            for ip in a_records:
                try:
                    ptr = dns.reversename.from_address(ip)
                    answers = self.resolver.resolve(ptr, 'PTR')
                    ptr_records[ip] = [str(r) for r in answers]
                except:
                    ptr_records[ip] = []
            return ptr_records
        except:
            return {}

    def get_srv_records(self):
        common_services = [
            '_ldap._tcp', '_kerberos._tcp', '_https._tcp',
            '_sip._tcp', '_sip._udp', '_xmpp-client._tcp'
        ]

        srv_records = {}
        for service in common_services:
            try:
                srv_domain = f"{service}.{self.domain}"
                answers = self.resolver.resolve(srv_domain, 'SRV')
                srv_records[service] = [str(r) for r in answers]
            except:
                continue

        return srv_records


if __name__ == "__main__":
    enumerator = DNSEnumerator("example.com")
    results = enumerator.enumerate_dns()
    print(results)