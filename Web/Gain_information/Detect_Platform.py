# detect_platform.py
import requests
from urllib.parse import urljoin

COMMON_CMS_PATHS = {
    "WordPress": ["wp-login.php", "wp-admin", "wp-content"],
    "Joomla": ["administrator", "index.php?option=com_"],
    "Drupal": ["user/login", "sites/default"],
    "Django": ["admin/", "csrfmiddlewaretoken"],
    "Laravel": ["login", "register"]
}

def detect_cms(base_url, timeout=5):
    detected = []
    for cms, paths in COMMON_CMS_PATHS.items():
        for path in paths:
            try:
                r = requests.get(urljoin(base_url, path), timeout=timeout)
                if r.status_code == 200:
                    detected.append(cms)
                    break
            except:
                continue
    return detected if detected else ["Unknown"]

if __name__ == "__main__":
    url = input("Enter site URL: ").strip()
    cms = detect_cms(url)
    print("Detected CMS / Framework:", cms)
