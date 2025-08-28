# Save.py
from Elements import extract_form_fields

if __name__ == "__main__":
    url = input("Enter Admin URL Here: ")
    data = extract_form_fields(url, save_to="login_form.json")

    print("Form information Extracted ✅")
    print(data)
