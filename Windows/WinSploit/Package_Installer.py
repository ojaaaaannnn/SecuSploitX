# Package_Installer.py
import subprocess
import sys
import importlib


class Install_Packages:
    def Installer(self):
        packages = {
            "opencv-python": "cv2",
            "pynput": "pynput",
            "requests": "requests",
            "pillow": "PIL"
        }

        for package, module_name in packages.items():
            try:
                importlib.import_module(module_name)
                print(f"{package} already installed")
            except ImportError:
                print(f"Installing {package}...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print(f"Installed {package}")
                except subprocess.CalledProcessError:
                    print(f"Failed to install {package}")


if __name__ == "__main__":
    Install_Packages.Installer()

