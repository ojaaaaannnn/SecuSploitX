# Found_TXT.py
import time
import requests
from datetime import datetime

# mynameismama6zaa
# 8/19/2025
# AUX-441

started_time = datetime.now()
print("Started Time:", started_time)

class Founded:
    def SUBDOMAINS(self, delay=0.3):
        try:
            base_url = input("ENTER URL HERE (https://example.com/) : ").strip()

            with open("Hidden_urls.txt", "r", encoding="utf-8", errors="ignore") as f:
                paths = [line.strip() for line in f if line.strip()]

            with open("Found_Success.txt", "w", encoding="utf-8") as output_file:

                for path in paths:
                    final = base_url + path
                    try:
                        response = requests.get(final, timeout=5)
                        if response.status_code == 200:
                            print(f"[+ ✅✅] Found: {final}")
                            output_file.write(final + "\n")
                        else:
                            print(f"[-] {final} - Status {response.status_code}")
                    except Exception as req_err:
                        print(f"[-] Error fetching {final} => {req_err}")

                    time.sleep(delay)

        except Exception as e:
            print(f"Failed To Load Wordlist or URL: {e}")


if __name__ == "__main__":
    C = Founded()
    C.SUBDOMAINS(delay=0.3)

ended_time = datetime.now()
print("Ended Time:", ended_time)
