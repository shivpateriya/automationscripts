import glob
import os
import requests
import csv
import re
from datetime import datetime

# Define the directory containing the log files
log_dir = "/path/to/log/dir"

# Construct the pattern to match the log files for the current day
pattern = f"{log_dir}/*ngest*{datetime.today().strftime('%Y%m%d')}dyamanica*"

# Define the Teams webhook URL
teams_webhook_url = "YOUR_TEAMS_WEBHOOK_URL"

# Get the list of log files matching the pattern
log_files = glob.glob(pattern)

# Create a list to store tabular data as dictionaries
tabular_data = []

# Iterate over each log file
for file in log_files:
    capture_data = False
    file_name = None

    # Open the log file and search for lines containing both "ERROR" and "Unsuccessfully published" in the same line
    with open(file, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line and "Unsuccessfully published" in line:
                capture_data = True
                # Extract the filename using regular expressions
                match = re.search(r'\{(.+?)\}', line)
                if match:
                    file_name = match.group(1).split('#')[0].strip()
                continue
            if capture_data and line.strip():
                if not line.startswith("sensorID smpID startTS endTS serialNo MDL_REF_smpID"):
                    data = line.strip().split()  # Split the line into columns
                    if len(data) == 6:  # Assuming 6 columns in the tabular data
                        data_dict = {
                            'filename': file_name,
                            'sensorID': data[0],
                            'smpID': data[1],
                            'startTS': data[2],
                            'endTS': data[3],
                            'serialNo': data[4],
                            'MDL_REF_smpID': data[5]
                        }
                        tabular_data.append(data_dict)

# Construct the CSV file name
current_date = datetime.today().strftime('%Y%m%d')
csv_file_name = f"PbcExportUnpublishedTabularData{current_date}dyamanica.csv"

# Create CSV file from the tabular data with the specified header
with open(csv_file_name, 'w', newline='') as csv_file:
    fieldnames = ['filename', 'sensorID', 'smpID', 'startTS', 'endTS', 'serialNo', 'MDL_REF_smpID']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(tabular_data)

# Send alert to Teams
message = f"CSV file '{csv_file_name}' is stored in this location: {os.path.abspath(csv_file_name)}"
teams_payload = {"text": message}
requests.post(teams_webhook_url, json=teams_payload)

print(f"CSV file created and alert sent: {csv_file_name}")
print("-" * 100)
