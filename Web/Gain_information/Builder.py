# Builder.py
from .Detect_Platform import detect_cms
from .wp_scan import WordPressScanner
from .admin_panel_info import find_login_pages, extract_form_elements
from .deep_scan import crawl_site
from .whois_scan import WhoisScanner


class SiteScanner:
    def __init__(self, url):
        self.url = url.rstrip("/") + "/"

    def run_platform_scan(self):
        return detect_cms(self.url)

    def run_wp_scan(self):
        wp = WordPressScanner(self.url)
        return wp.scan_all()

    def run_admin_scan(self):
        login_pages = find_login_pages(self.url)
        forms_info = {}
        for page in login_pages:
            full_url = self.url + page
            forms_info[page] = extract_form_elements(full_url)
        return {"login_pages": login_pages, "forms": forms_info}

    def run_deep_scan(self):
        emails, usernames, elements = crawl_site(self.url)
        return {"emails": emails, "usernames": usernames, "html_elements": elements}

    def run_whois_scan(self):
        domain = self.url.replace("http://", "").replace("https://", "").split("/")[0]
        scanner = WhoisScanner(domain)
        return scanner.full_scan()

    def run_all(self):
        return {
            "platform": self.run_platform_scan(),
            "wordpress": self.run_wp_scan(),
            "admin_panel": self.run_admin_scan(),
            "deep_scan": self.run_deep_scan(),
            "whois": self.run_whois_scan()
        }


def pretty_print(data, indent=0, file=None):
    space = "    " * indent
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"{space}{k}:", file=file)
            pretty_print(v, indent + 1, file=file)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                pretty_print(item, indent + 1, file=file)
            else:
                print(f"{space}- {item}", file=file)
    else:
        print(f"{space}{data}", file=file)


if __name__ == "__main__":
    url = input("Enter site URL: ").strip()
    scanner = SiteScanner(url)
    results = scanner.run_all()

    print("\n" + "="*60)
    print("        🌐 FULL SITE SCAN RESULTS 🌐")
    print("="*60)
    for section, data in results.items():
        print(f"\n--- {section.upper()} ---")
        pretty_print(data)
    print("\n" + "="*60)

    with open("scan_results.txt", "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("        🌐 FULL SITE SCAN RESULTS 🌐\n")
        f.write("="*60 + "\n")
        for section, data in results.items():
            f.write(f"\n--- {section.upper()} ---\n")
            pretty_print(data, file=f)
        f.write("\n" + "="*60 + "\n")
