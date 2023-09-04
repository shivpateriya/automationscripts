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

# Define the header for the CSV file
csv_header = ['sensorID', 'smpID', 'startTs', 'endTs', 'serialNo', 'MDL_REF_smpID']

# Iterate over each log file
for file in log_files:
    capture_data = False
    captured_data = set()  # Use a set to store unique rows
    error_line = None

    # Open the log file and search for lines containing "Error"
    with open(file, encoding="utf-8") as f:
        for line in f:
            if "Unsuccessfully published" in line:
                capture_data = True
                error_line = line.strip()
            elif capture_data:
                if line.strip():
                    columns = line.split()
                    # Check if the line has the expected number of columns
                    if len(columns) == len(csv_header):
                        captured_data.add(tuple(columns))  # Add the line as a tuple to the set
                else:
                    capture_data = False

    if error_line and captured_data:
        # Construct the file name
        current_date = datetime.today().strftime('%Y%m%d')
        file_name = f"PbcExportUnpublishedError{current_date}dyamanica.txt"

        # Write the captured error line and tabular data to the file
        with open(file_name, 'w') as output_file:
            output_file.write(f"{error_line}\n")
            for row in captured_data:
                output_file.write(" ".join(row) + "\n")

        # Create CSV file from the tabular data with the specified header
        csv_file_name = f"PbcExportUnpublishedError{current_date}dyamanica.csv"
        with open(csv_file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(csv_header)
            csv_writer.writerows(captured_data)

        # Send alert to Teams
        message = f"CSV file '{csv_file_name}' is stored in this location: {os.path.abspath(csv_file_name)}"
        teams_payload = {"text": message}
        requests.post(teams_webhook_url, json=teams_payload)

        print(f"CSV file created and alert sent: {csv_file_name}")
        print("-" * 100)
