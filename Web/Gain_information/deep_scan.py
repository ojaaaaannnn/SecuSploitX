# deep_scan.py
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time

DEFAULT_DELAY = 0.3
MAX_PAGES = 20

def extract_emails_usernames(url, timeout=5):
    emails, usernames = set(), set()
    try:
        r = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(r.text, "html.parser")
        emails.update(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", r.text))
        for form in soup.find_all("form"):
            inputs = form.find_all("input", {"name": True})
            for inp in inputs:
                usernames.add(inp["name"])
        for a in soup.find_all("a", href=True):
            if "user" in a["href"] or "author" in a["href"]:
                usernames.add(a["href"])
    except:
        pass
    return list(emails), list(usernames)

def list_html_elements(url, timeout=5):
    elements = set()
    try:
        r = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup.find_all(True):
            elements.add(tag.name)
    except:
        pass
    return list(elements)

def crawl_site(base_url, max_pages=MAX_PAGES, delay=DEFAULT_DELAY):
    visited = set()
    to_visit = [base_url]
    all_emails, all_usernames, all_elements = set(), set(), set()

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        print("Scanning:", url)
        time.sleep(delay)

        emails, usernames = extract_emails_usernames(url)
        all_emails.update(emails)
        all_usernames.update(usernames)
        elements = list_html_elements(url)
        all_elements.update(elements)

        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True):
                link = urljoin(base_url, a["href"])
                if urlparse(link).netloc == urlparse(base_url).netloc:
                    if link not in visited and link not in to_visit:
                        to_visit.append(link)
        except:
            continue

    return list(all_emails), list(all_usernames), list(all_elements)

if __name__ == "__main__":
    base_url = input("Enter site URL: ").strip()
    emails, usernames, elements = crawl_site(base_url)
    print("Emails found:", emails)
    print("Usernames found:", usernames)
    print("HTML Elements:", elements)
