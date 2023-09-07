import glob
import os
import requests
import csv
from datetime import datetime
import re

# Define the directory containing the log files
log_dir = "/path/to/log/dir"

# Construct the pattern to match the log files for the current day
pattern = f"{log_dir}/*ngest*{datetime.today().strftime('%Y%m%d')}dyamanica*"

# Define the Teams webhook URL
teams_webhook_url = "YOUR_TEAMS_WEBHOOK_URL"

# Get the list of log files matching the pattern
log_files = glob.glob(pattern)

# Create a list to store tabular data
tabular_data = []

# Regular expressions to match relevant lines
error_pattern = re.compile(r"ERROR")
unsuccessful_pattern = re.compile(r"Unsuccessfully published")
filename_pattern = re.compile(r"{ConfigurationExport_(.*?)\}")

# Iterate over each log file
for file in log_files:
    capture_data = False
    current_filename = None

    # Open the log file
    with open(file, encoding="utf-8") as f:
        for line in f:
            if error_pattern.search(line) and unsuccessful_pattern.search(line):
                capture_data = True
            elif capture_data:
                filename_match = filename_pattern.search(line)
                if filename_match:
                    current_filename = filename_match.group(1)
                    capture_data = False
                elif "serialNo extSensorID meterStatusIEE startTs endTs sensorID status deviceOperationalStatus meterProgramID" in line:
                    capture_data = False  # Skip the header line
                elif line.strip():
                    # Split the tabular data
                    data = line.strip().split()
                    if len(data) == 9:  # Assuming 9 columns in the tabular data
                        tabular_data.append([current_filename] + data)

# Construct the CSV file name
current_date = datetime.today().strftime('%Y%m%d')
csv_file_name = f"PbcExportUnpublishedTabularData{current_date}dyamanica.csv"

# Create CSV file from the tabular data with the specified header
with open(csv_file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['filename', 'serialNo', 'extSensorID', 'meterStatusIEE', 'startTs', 'endTs', 'sensorID', 'status', 'deviceOperationalStatus', 'meterProgramID'])
    csv_writer.writerows(tabular_data)

# Send alert to Teams
message = f"CSV file '{csv_file_name}' is stored in this location: {os.path.abspath(csv_file_name)}"
teams_payload = {"text": message}
requests.post(teams_webhook_url, json=teams_payload)

print(f"CSV file created and alert sent: {csv_file_name}")
print("-" * 100)
