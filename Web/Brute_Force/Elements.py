import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from urllib.parse import urljoin

COMMON_LOGIN_PATHS = [
    "wp-login.php",
    "admin/login/",
    "login",
    "user/login",
    "phpmyadmin",
    "administrator/index.php"
]

def find_login_url(base_url):
    session = requests.Session()
    for path in COMMON_LOGIN_PATHS:
        test_url = urljoin(base_url, path)
        try:
            res = session.get(test_url, timeout=5)
            if res.status_code == 200 and "password" in res.text.lower():
                return test_url
        except requests.RequestException:
            continue
    return base_url

def extract_form_fields(url: str, save_to: str = None):
    session = requests.Session()

    login_url = find_login_url(url)
    res = session.get(login_url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    forms = soup.find_all("form")
    if not forms:
        raise ValueError("No form found on page")

    form = None
    for f in forms:
        if f.find("input", {"type": "password"}):
            form = f
            break
    if not form:
        form = forms[0]

    action = form.get("action")
    method = form.get("method", "get").lower()

    inputs = form.find_all("input")

    form_data = {}
    username_field = None
    password_field = None

    for inp in inputs:
        name = inp.get("name")
        input_type = inp.get("type", "text").lower()

        if input_type == "password":
            password_field = name
        elif input_type in ["text", "email"]:
            if not username_field:
                username_field = name
        elif name and any(kw in name.lower() for kw in ["user", "email", "log"]):
            username_field = name
        elif name and any(kw in name.lower() for kw in ["pass", "pwd"]):
            password_field = name
        elif input_type == "hidden" and name:
            form_data[name] = inp.get("value", "")

    result = {
        "url": login_url,
        "action": action,
        "method": method,
        "username_field": username_field,
        "password_field": password_field,
        "hidden_fields": form_data
    }

    if save_to:
        save_path = Path(save_to)
        save_path.write_text(json.dumps(result, indent=4, ensure_ascii=False))

    return result
