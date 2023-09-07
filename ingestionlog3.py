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

# Create a set to store unique tabular data as tuples
unique_tabular_data = set()

# Iterate over each log file
for file in log_files:
    capture_data = False
    filename = ""

    # Open the log file and search for lines containing "ERROR"
    with open(file, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line and "Unsuccesfully published" in line:
                capture_data = True
                filename = line.split("LOG")[1].strip()  # Extract the filename
            elif capture_data and not line.startswith("serialNo extSensorID meterStatusIEE"):
                data = line.strip().split()  # Split the line into columns
                if len(data) == 9:  # Assuming 9 columns in the tabular data
                    data_tuple = tuple(data)  # Convert the data list to a tuple
                    unique_tabular_data.add((filename,) + data_tuple)  # Add filename as the first element

# Construct the CSV file name
current_date = datetime.today().strftime('%Y%m%d')
csv_file_name = f"PbcExportUnpublishedTabularData{current_date}dyamanica.csv"

# Create CSV file from the unique tabular data with the specified header
with open(csv_file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['filename', 'serialNo', 'extSensorID', 'meterStatusIEE', 'startTs', 'endTs', 'sensorID', 'status', 'deviceOperationalStatus', 'meterProgramID'])
    csv_writer.writerows(unique_tabular_data)

# Send alert to Teams
message = f"CSV file '{csv_file_name}' is stored in this location: {os.path.abspath(csv_file_name)}"
teams_payload = {"text": message}
requests.post(teams_webhook_url, json=teams_payload)

print(f"CSV file created and alert sent: {csv_file_name}")
print("-" * 100)
