import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from advanced_subdomain import AdvancedSubdomainEnumerator

if __name__ == "__main__":
    domain = input("Enter target domain: ")
    enumerator = AdvancedSubdomainEnumerator(domain, wordlist_file="subdomains-top1million-5000.txt", threads=50)
    enumerator.enumerate()
    enumerator.save_results("found_subdomains.txt")