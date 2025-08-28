# form_finder.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_forms(url, debug=True):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if debug:
            print(f"[+] Fetched {url} successfully")
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    forms = soup.find_all("form")
    if debug:
        print(f"[+] Found {len(forms)} form(s) at {url}")

    form_list = []
    for idx, form in enumerate(forms, 1):
        form_info = {}
        action = form.get("action")
        method = form.get("method", "get").lower()
        inputs = form.find_all("input")

        data = {}
        for inp in inputs:
            name = inp.get("name")
            if not name:
                continue
            data[name] = inp.get("value", "")

        form_info['action'] = url if not action else urljoin(url, action)
        form_info['method'] = method
        form_info['inputs'] = data
        form_info['form_number'] = idx
        form_list.append(form_info)

    return form_list
