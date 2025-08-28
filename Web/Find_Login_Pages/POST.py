# Builder.py
import requests
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def Find_Admin(stop_flag=None, base_url=None):
    if base_url is None:
        base_url = input("Enter your site URL (e.g., https://example.com): ").strip()

    wordlist_file = os.path.join(BASE_DIR, "urls.txt")
    try:
        with open(wordlist_file, "r", encoding="utf-8", errors="ignore") as f:
            admin_paths = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Failed to load wordlist {wordlist_file}: {e}")
        return

    print(f"Loaded {len(admin_paths)} paths from {wordlist_file}.")

    log_file = os.path.join(BASE_DIR, "results_log.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        log.write(f"Scan started at {datetime.now()}\n")
        log.write(f"Target: {base_url}\n\n")

        for path in admin_paths:
            if stop_flag and stop_flag.get("stop"):
                print("[!] Scan stopped by user")
                break

            url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
            try:
                response = requests.get(url, timeout=5)
                status = response.status_code
                print(f"{url} -> {status}")
                log.write(f"{url} -> {status}\n")

                if status == 200:
                    print(f" [✅✅] Found 200 OK at {url}! Stopping scan.")
                    log.write(f"Found 200 OK at {url}! Stopping scan.\n")
                    break
            except Exception as e:
                print(f"{url} -> Error: {e}")
                log.write(f"{url} -> Error: {e}\n")

        log.write(f"\nScan ended at {datetime.now()}\n")

    print(f"Scan complete. Results saved in {log_file}")
