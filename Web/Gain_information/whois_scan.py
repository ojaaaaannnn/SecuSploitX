# whois_scan.py
import whois
import socket
import dns.resolver
import re


class WhoisScanner:
    def __init__(self, domain, timeout=20):
        self.domain = domain
        self.timeout = timeout
        socket.setdefaulttimeout(self.timeout)

    def basic_whois(self):
        for attempt in range(2):
            try:
                w = whois.whois(self.domain)
                data = {
                    "domain_name": w.domain_name,
                    "registrar": w.registrar,
                    "creation_date": w.creation_date,
                    "expiration_date": w.expiration_date,
                    "updated_date": w.updated_date,
                    "name_servers": w.name_servers,
                    "emails": w.emails
                }
                return data
            except Exception as e:
                if attempt == 1:
                    return {"error": f"Failed to fetch WHOIS info: {e}"}

    def dns_info(self):
        dns_data = {}
        try:
            a_records = socket.gethostbyname_ex(self.domain)[2]
            dns_data["A_records"] = a_records
        except Exception as e:
            dns_data["A_records"] = []
            dns_data["A_error"] = str(e)

        try:
            mx_records = []
            answers = dns.resolver.resolve(self.domain, "MX")
            for rdata in answers:
                mx_records.append(str(rdata.exchange))
            dns_data["MX_records"] = mx_records
        except Exception as e:
            dns_data["MX_records"] = []
            dns_data["MX_error"] = str(e)

        try:
            txt_records = []
            answers = dns.resolver.resolve(self.domain, "TXT")
            for rdata in answers:
                txt_records.append(rdata.to_text())
            dns_data["TXT_records"] = txt_records
        except Exception as e:
            dns_data["TXT_records"] = []
            dns_data["TXT_error"] = str(e)

        return dns_data

    def extract_emails(self):
        emails = set()
        try:
            whois_data = self.basic_whois()
            if whois_data.get("emails"):
                if isinstance(whois_data["emails"], list):
                    emails.update(whois_data["emails"])
                else:
                    emails.add(whois_data["emails"])

            txt_records = self.dns_info().get("TXT_records", [])
            for txt in txt_records:
                found = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", txt)
                emails.update(found)

        except Exception as e:
            print(f"Error extracting emails: {e}")
        return list(emails)

    def full_scan(self):
        return {
            "basic_whois": self.basic_whois(),
            "dns_info": self.dns_info(),
            "emails": self.extract_emails()
        }


if __name__ == "__main__":
    domain = input("Enter domain (example.com): ").strip()
    scanner = WhoisScanner(domain)

    info = scanner.full_scan()
    print("\n=== WHOIS & Domain Info ===")
    print("Basic WHOIS Info:", info["basic_whois"])
    print("\nDNS Records:", info["dns_info"])
    print("\nFound Emails:", info["emails"])
