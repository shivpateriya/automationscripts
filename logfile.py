import os
from datetime import datetime

# Run the "cdl" command if it's a valid executable
os.system("cdl")  # Replace this with the correct command and its arguments

# Get the current year and month
current_date = datetime.now()
year = current_date.year
month = current_date.month

# Construct the date in the format "YYYYMM" (e.g., "202311" for November 2023)
user_date = f"{year}{month:02}"

# Construct the grep command
pattern = f"*DBW*{user_date}*"
grep_command = f'grep EOD {pattern} | grep elapsed | grep date'

# Run the grep command using os.popen() to capture its output
output = os.popen(grep_command).read()

# Check if there's any output and print accordingly
if output:
    print("Logs found for this date:")
    # Extract the part of the output until ".log"
    logs = [line.split('.log')[0] + '.log' for line in output.split('\n')]
    print("\n".join(logs))
else:
    print("No logs found for this date.")
