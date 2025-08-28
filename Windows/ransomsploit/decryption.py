# decryption.py
import os
from cryptography.fernet import Fernet


key_input = input("Enter the decryption key: ").strip()

try:
    cipher = Fernet(key_input.encode())
except Exception as e:
    print(f"❌ Invalid key format: {e}")
    exit(1)

skip_paths = ["Windows", "AppData"]

target_exts = [".txt", ".pdf", ".jpg", ".png", ".gif", ".jpeg", ".wav", ".mp3", ".mp4"]

def decrypt_file(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        decrypted = cipher.decrypt(data)
        with open(filepath, "wb") as f:
            f.write(decrypted)
        print(f"✅ Decrypted: {filepath}")
    except Exception as e:
        print(f"❌ Skipped {filepath}: {e}")

def decrypt_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        if any(skip in root for skip in skip_paths):
            print(f"⏩ Skipped system folder: {root}")
            continue

        for filename in files:
            file_path = os.path.join(root, filename)
            if any(filename.endswith(ext) for ext in target_exts):
                decrypt_file(file_path)
            else:
                print(f"⏩ Skipped (unsupported type): {file_path}")

path = input("Enter path to decrypt: ").strip()

if os.path.isdir(path):
    decrypt_folder(path)
elif os.path.isfile(path):
    decrypt_file(path)
else:
    print("❌ Invalid path")
