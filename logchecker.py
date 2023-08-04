import glob
import os
import requests
from datetime import datetime

# Define the directory containing the log files
log_dir = "/path/to/log/dir"

# Construct the pattern to match the log files for the current day
pattern = f"{log_dir}/*ngest*{datetime.today().strftime('%Y%m%d')}"

# Define the Teams webhook URL
teams_webhook_url = "YOUR_TEAMS_WEBHOOK_URL"

# Get the list of log files matching the pattern
log_files = glob.glob(pattern)

# Iterate over each log file
for file in log_files:
    capture_data = False
    print_filename = True
    captured_data = []
    
    # Open the log file and search for lines containing "Error"
    with open(file, encoding="utf-8") as f:
        for line in f:
            if "Unsuccessfully published" in line:
                capture_data = True
                print_filename = True
                captured_data.append(line.strip())  # Append the error line
            elif capture_data and line.strip() == "":
                capture_data = False
            elif capture_data:
                if "sensorID" in line and "smpID" in line and "startTs" in line and "endTs" in line and "serialNo" in line and "MDL_REF_smpID" in line:
                    if print_filename:
                        current_date = datetime.today().strftime('%Y%m%d')
                        file_name = f"PbcExportUnpublishedError{current_date}.txt"
                        print_filename = False
                    captured_data.append(line.strip())

    if captured_data:
        # Write the captured data to a new file
        with open(file_name, 'w') as output_file:
            output_file.write("\n".join(captured_data))

        # Send alert to Teams
        message = f"File '{file_name}' is stored in this location: {os.path.abspath(file_name)}"
        teams_payload = {"text": message}
        requests.post(teams_webhook_url, json=teams_payload)

        print(f"Captured data and error saved to: {file_name}")
        print("-" * 100)
