import glob
import os
import requests
import csv
from datetime import datetime

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

# Iterate over each log file
for file in log_files:
    capture_data = False
    current_filename = None

    # Open the log file
    with open(file, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line and "Unsuccessfully published" in line:
                capture_data = True
            elif capture_data and "LOG {" in line:
                # Extract the filename from the line
                filename_parts = line.split('{', 1)[1].split('}')[0].split('#')
                if len(filename_parts) == 2:
                    current_filename = filename_parts[0].strip()
                capture_data = False
            elif capture_data and "sensorID" in line:
                # Skip the header line
                continue
            elif capture_data and line.strip():
                # Split the tabular data
                data = line.strip().split()
                if len(data) == 6:
                    tabular_data.append([current_filename] + data)

# Construct the CSV file name
current_date = datetime.today().strftime('%Y%m%d')
csv_file_name = f"PbcExportUnpublishedTabularData{current_date}dyamanica.csv"

# Create CSV file from the tabular data with the specified header
with open(csv_file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['filename', 'sensorID', 'smpID', 'startTS', 'endTS', 'serialNo', 'MDL_REF_smpID'])
    csv_writer.writerows(tabular_data)

# Send alert to Teams
message = f"CSV file '{csv_file_name}' is stored in this location: {os.path.abspath(csv_file_name)}"
teams_payload = {"text": message}
requests.post(teams_webhook_url, json=teams_payload)

print(f"CSV file created and alert sent: {csv_file_name}")
print("-" * 100)
