# form_tester.py
import requests

def load_sql_errors(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]

def test_form(form, payload, sql_errors, debug=True):
    data = {}
    for k, v in form['inputs'].items():
        data[k] = payload if v == "" else v

    method = form['method']
    url = form['action']

    try:
        if method == "post":
            response = requests.post(url, data=data, timeout=10)
        else:
            response = requests.get(url, params=data, timeout=10)
    except Exception as e:
        if debug:
            print(f"[!] Request failed for {url}: {e}")
        return False, None

    detected_error = None
    for error in sql_errors:
        if error.lower() in response.text.lower():
            detected_error = error
            if debug:
                print(f"[!!!] Possible SQL Injection detected at {url} using payload: {payload}")
                print(f"    Detected error: {error}")
            return True, detected_error

    if debug:
        print(f"[*] No obvious SQL error detected at {url} using payload: {payload}")
    return False, None
