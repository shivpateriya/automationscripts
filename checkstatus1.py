import datetime
import os
import requests

# Define the log folder path
log_folder = "path/to/log/folder"  # Replace with the actual log folder path

# Define the webhook URL for sending alerts
webhook_url = "https://your-webhook-url"  # Replace with the actual webhook URL

# Get the current date
current_date = datetime.date.today()

# Define the script names
script_names = ["script1.py", "script2.py", "script3.py", "script4.py", "script5.py",
                "script6.py", "script7.py", "script8.py", "script9.py", "script10.py"]

# Delete log entries older than 10 days and send alerts for incomplete scripts
for script_name in script_names:
    log_file = f"{script_name}_{current_date}.log"

    # Construct the log file path
    log_file_path = os.path.join(log_folder, log_file)

    # Check if the log file exists
    if os.path.isfile(log_file_path):
        # Read the contents of the log file
        with open(log_file_path, "r") as file:
            lines = file.readlines()

        # Remove log entries older than 10 days
        cutoff_date = current_date - datetime.timedelta(days=10)
        filtered_lines = [line for line in lines if not line.startswith(tuple(map(str, range(1, cutoff_date.day + 1))))]

        # Write the filtered lines back to the log file
        with open(log_file_path, "w") as file:
            file.writelines(filtered_lines)

        # Check if the log file contains the completion message
        completion_message = f"{current_date} - {script_name} has successfully completed"
        if completion_message not in filtered_lines:
            # Create the alert message
            alert_message = f"Logging file '{log_file_path}' does not contain completion message for '{script_name}'."

            # Send the alert to the webhook
            response = requests.post(webhook_url, json={"message": alert_message})

            # Check the response status
            if response.status_code == 200:
                print(f"Alert sent successfully for '{script_name}'.")
            else:
                print(f"Failed to send alert for '{script_name}'. Status code: {response.status_code}")
        else:
            print(f"Logging file '{log_file_path}' is complete for '{script_name}'.")
