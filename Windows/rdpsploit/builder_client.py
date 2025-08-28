# builder.py
import subprocess
import re
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from datetime import datetime

started_time = datetime.now()
print("Started Time :", started_time)


from client import run_client


ended_time = datetime.now()
print("Ended Time :", ended_time)


