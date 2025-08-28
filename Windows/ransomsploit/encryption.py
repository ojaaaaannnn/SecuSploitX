# encryption.py
import os
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText

key = Fernet.generate_key()
cipher = Fernet(key)

skip_paths = ["Windows","AppData"]

target_exts = [".txt", ".pdf", ".jpg", ".png", "gif" , "jpeg", "wav", "mp3", "mp4"]

def encrypt_file(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        encrypted = cipher.encrypt(data)
        with open(filepath, "wb") as f:
            f.write(encrypted)
        print(f"✅ Encrypted: {filepath}")
    except Exception as e:
        print(f"❌ Skipped {filepath}: {e}")

def encrypt_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        if any(skip in root for skip in skip_paths):
            print(f"⏩ Skipped system folder: {root}")
            continue

        for filename in files:
            file_path = os.path.join(root, filename)
            if any(filename.endswith(ext) for ext in target_exts):
                encrypt_file(file_path)
            else:
                print(f"⏩ Skipped (unsupported type): {file_path}")

path = input("Enter path to encrypt: ").strip()

if os.path.isdir(path):
    encrypt_folder(path)
elif os.path.isfile(path):
    encrypt_file(path)
else:
    print("❌ Invalid path")

choice = input("\nDo you want to send the key to your email? (yes/no): ").strip().lower()

if choice == "yes":
    sender_email = input("Enter sender Gmail: ").strip()
    sender_pass = input("Enter sender app password: ").strip()
    receiver_email = input("Enter receiver email: ").strip()

    try:
        subject = "Your Encryption Key"
        body = f"Here is your key:\n\n{key.decode()}"
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_pass)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print(f"📩 Key sent successfully to {receiver_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if choice == "no":
    print("okay Save the Key for your decryption Please .")
    print(key.decode())

