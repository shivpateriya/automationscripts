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

# Iterate over each log file
for file in log_files:
    capture_data = False
    tabular_data = []  # Store tabular data lines

    # Open the log file and search for lines containing "Unsuccessfully published"
    with open(file, encoding="utf-8") as f:
        for line in f:
            if "Unsuccessfully published" in line:
                capture_data = True
            elif capture_data:
                if line.strip() and not line.startswith("sensorID"):
                    tabular_data.append(line.strip())  # Add the line to tabular_data
                else:
                    capture_data = False

    if tabular_data:
        # Construct the CSV file name
        current_date = datetime.today().strftime('%Y%m%d')
        csv_file_name = f"PbcExportUnpublishedTabularData{current_date}dyamanica.csv"

        # Create CSV file from the tabular data with the specified header
        with open(csv_file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['sensorID', 'smpID', 'startTs', 'endTs', 'serialNo', 'MDL_REF_smpID'])
            for line in tabular_data:
                columns = line.split()
                if len(columns) == 6:
                    csv_writer.writerow(columns)

        # Send alert to Teams
        message = f"CSV file '{csv_file_name}' is stored in this location: {os.path.abspath(csv_file_name)}"
        teams_payload = {"text": message}
        requests.post(teams_webhook_url, json=teams_payload)

        print(f"CSV file created and alert sent: {csv_file_name}")
        print("-" * 100)
