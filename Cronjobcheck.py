import os
import subprocess
import requests
from datetime import datetime

log_file = "/path/to/logfile"
webhook_url = "<webhook_url>"

# Extract the script name from the log file path
script_name = os.path.splitext(os.path.basename(log_file))[0]

# Get today's date
today = datetime.now().date()

# Check if the log file exists
if os.path.isfile(log_file):
    # Check if the log file contains any error messages for today's date
    with open(log_file, 'r') as file:
        log_content = file.read().lower()
        if today.isoformat() in log_content and "error" in log_content:
            print(f"Script '{script_name}' failed today! Sending alert...")
            # Use requests library to send an alert to the webhook
            response = requests.post(webhook_url, json={"message": f"Cron job '{script_name}' failed today!"})
            if response.status_code == 200:
                print("Alert sent successfully.")
            else:
                print("Failed to send alert.")
        else:
            print(f"Script '{script_name}' executed successfully today.")
else:
    print("Log file not found.")
