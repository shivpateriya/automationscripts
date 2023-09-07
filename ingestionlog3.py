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

# Create a list to store tabular data as dictionaries
tabular_data = []

# Iterate over each log file
for file in log_files:
    capture_data = False
    current_filename = None
    log_data = []

    # Open the log file
    with open(file, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line and "Unsuccessfully published" in line:
                capture_data = True
                # Extract the filename from the line
                current_filename = re.search(r'\{(.+?)\}', line).group(1).split('#')[0].strip()
            elif capture_data and "LOG {" in line:
                # Reset data for a new entry
                log_data = []
                log_data.append(current_filename)
            elif capture_data and line.strip() and not line.startswith("sensorID smpID startTS endTS serialNo MDL_REF_smpID"):
                data = line.strip().split()  # Split the line into columns
                if len(data) == 6:  # Assuming 6 columns in the tabular data
                    log_data.extend(data)
                    if len(log_data) == 7:  # We've collected all the data for this entry
                        tabular_data.append({
                            'filename': log_data[0],
                            'sensorID': log_data[1],
                            'smpID': log_data[2],
                            'startTS': log_data[3],
                            'endTS': log_data[4],
                            'serialNo': log_data[5],
                            'MDL_REF_smpID': log_data[6]
                        })
                        # Reset for the next entry
                        log_data = []

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
