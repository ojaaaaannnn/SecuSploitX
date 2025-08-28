# wp_scan.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

DEFAULT_TIMEOUT = 5

class WordPressScanner:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/") + "/"

    def detect_version(self):
        version = "Unknown"
        try:
            # readme.html
            r = requests.get(urljoin(self.base_url, "readme.html"), timeout=DEFAULT_TIMEOUT)
            if r.status_code == 200:
                match = re.search(r"Version (\d+\.\d+(\.\d+)*)", r.text)
                if match:
                    version = match.group(1)
                    return version
            r = requests.get(self.base_url, timeout=DEFAULT_TIMEOUT)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                meta = soup.find("meta", {"name": "generator"})
                if meta and "WordPress" in meta.get("content", ""):
                    version_match = re.search(r"WordPress (\d+\.\d+(\.\d+)*)", meta["content"])
                    if version_match:
                        version = version_match.group(1)
        except:
            pass
        return version

    def detect_theme(self):
        theme_name = "Unknown"
        try:
            r = requests.get(self.base_url, timeout=DEFAULT_TIMEOUT)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                for link in soup.find_all("link", href=True):
                    if "wp-content/themes/" in link["href"]:
                        match = re.search(r"wp-content/themes/([^/]+)/", link["href"])
                        if match:
                            theme_name = match.group(1)
                            break
        except:
            pass
        return theme_name

    def detect_plugins(self, plugins_list=None):
        found_plugins = []
        if not plugins_list:
            plugins_list = [
                "akismet", "contact-form-7", "woocommerce",
                "elementor", "yoast-seo", "jetpack",
                "wp-super-cache", "all-in-one-seo-pack"
            ]
        for plugin in plugins_list:
            url = urljoin(self.base_url, f"wp-content/plugins/{plugin}/")
            try:
                r = requests.get(url, timeout=DEFAULT_TIMEOUT)
                if r.status_code == 200:
                    found_plugins.append(plugin)
            except:
                continue
        return found_plugins

    def scan_all(self, plugins_list=None):
        return {
            "version": self.detect_version(),
            "theme": self.detect_theme(),
            "plugins": self.detect_plugins(plugins_list)
        }

if __name__ == "__main__":
    url = input("Enter WordPress site URL: ").strip()
    scanner = WordPressScanner(url)

    info = scanner.scan_all()
    print("\n=== WordPress Scan Result ===")
    print("Version:", info["version"])
    print("Active Theme:", info["theme"])
    print("Detected Plugins:", info["plugins"])
