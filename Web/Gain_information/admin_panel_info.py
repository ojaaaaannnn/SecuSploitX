# admin_panel_info.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

COMMON_LOGIN_PATHS = ["admin/", "login", "wp-login.php", "user/login"]

def find_login_pages(base_url, timeout=5):
    found = []
    for path in COMMON_LOGIN_PATHS:
        try:
            r = requests.get(urljoin(base_url, path), timeout=timeout)
            if r.status_code == 200:
                found.append(path)
        except:
            continue
    return found

def extract_form_elements(page_url, timeout=5):
    elements = []
    try:
        r = requests.get(page_url, timeout=timeout)
        soup = BeautifulSoup(r.text, "html.parser")
        for form in soup.find_all("form"):
            form_info = {"action": form.get("action"), "method": form.get("method"), "inputs": []}
            for inp in form.find_all("input", {"name": True}):
                form_info["inputs"].append({"name": inp["name"], "type": inp.get("type")})
            elements.append(form_info)
    except:
        pass
    return elements

if __name__ == "__main__":
    base_url = input("Enter site URL: ").strip()
    login_pages = find_login_pages(base_url)
    print("Login pages:", login_pages)
    for page in login_pages:
        full_url = urljoin(base_url, page)
        forms = extract_form_elements(full_url)
        print(f"\nForms in {page}:")
        for f in forms:
            print(f)
