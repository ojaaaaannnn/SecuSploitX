# main.py
import os

from form_finder import find_forms
from form_tester import test_form, load_sql_errors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_payloads(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    url = input("Enter URL Here: ").strip()
    payload_file = "payloads.txt"
    sql_errors_file = "sql_errors.txt"

    payloads = load_payloads(payload_file)
    sql_errors = load_sql_errors(sql_errors_file)

    print(f"[+] Loaded {len(payloads)} payload(s) from {payload_file}")
    print(f"[+] Loaded {len(sql_errors)} SQL error patterns from {sql_errors_file}")

    forms = find_forms(url, debug=True)

    for form in forms:
        for payload in payloads:
            found, error = test_form(form, payload, sql_errors, debug=True)
            if found:
                print(f"[!!!] Form #{form['form_number']} at {form['action']} is vulnerable to payload: {payload} (Error: {error})")
