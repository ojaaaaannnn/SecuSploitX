# advanced_subdomain.py
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os

class AdvancedSubdomainEnumerator:
    def __init__(self, domain, wordlist_file=None, timeout=3, threads=20, verbose=True, use_https=True):
        self.domain = domain
        self.timeout = timeout
        self.threads = threads
        self.verbose = verbose
        self.use_https = use_https
        self.found = []

        self.wordlist = self._load_wordlist(wordlist_file)

    def _load_wordlist(self, filename):
        if filename and os.path.isfile(filename):
            try:
                with open(filename, "r") as f:
                    lines = [line.strip() for line in f if line.strip()]
                    if self.verbose:
                        print(f"[+] Loaded {len(lines)} entries from {filename}")
                    return lines
            except Exception as e:
                print(f"[!] Failed to read {filename}: {e}")
        else:
            if filename:
                print(f"[!] File {filename} not found, using default wordlist")
            return ["www", "mail", "dev", "test", "api", "staging", "beta"]

    def _check_subdomain(self, sub):
        protocols = ["http://"]
        if self.use_https:
            protocols.append("https://")

        for proto in protocols:
            url = f"{proto}{sub}.{self.domain}"
            try:
                r = requests.get(url, timeout=self.timeout)
                if r.status_code < 400:
                    if self.verbose:
                        print(f"[+] Found: {url} (Status: {r.status_code})")
                    return url
            except requests.RequestException:
                continue
        return None

    def enumerate(self):
        if self.verbose:
            print(f"Starting subdomain enumeration for {self.domain} with {len(self.wordlist)} entries...")

        self.found = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._check_subdomain, sub): sub for sub in self.wordlist}

            for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning", unit="subdomain"):
                result = future.result()
                if result:
                    self.found.append(result)

        if self.verbose:
            print(f"Enumeration completed. Found {len(self.found)} subdomains.")
        return self.found

    def save_results(self, filepath="subdomains.txt"):
        try:
            with open(filepath, "w") as f:
                for sub in self.found:
                    f.write(sub + "\n")
            if self.verbose:
                print(f"[+] Results saved to {filepath}")
        except Exception as e:
            print(f"[!] Failed to save results: {e}")


if __name__ == "__main__":
    domain = input("Enter target domain: ")
    enumerator = AdvancedSubdomainEnumerator(domain, wordlist_file="subdomains-top1million-5000.txt", threads=50)
    enumerator.enumerate()
    enumerator.save_results("found_subdomains.txt")
