import subprocess
import os
from datetime import datetime

# Change the current working directory to "cdl"
os.chdir("cdl")

# Get the current year and month
current_date = datetime.now()
year = current_date.year
month = current_date.month

# Construct the date in the format "YYYYMM" (e.g., "202311" for November 2023)
user_date = f"{year}{month:02}"

# Construct the grep command
pattern = f"*DBW*{user_date}*"
grep_command = f'grep EOD {pattern} | grep elapsed | grep date'
subprocess.run(["bash", "-c", grep_command], shell=True)
