# server.py
from datetime import datetime
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

started_time = datetime.now()
print("Started Time :", started_time)


import server


ended_time = datetime.now()
print("Ended Time :", ended_time)


