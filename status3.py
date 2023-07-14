import datetime
import os
import requests

# Define the log folder path
log_folder = "/home/knoldus/pythonscripts/CronjobAlert"  # Replace with the actual log folder path

# Define the shared log file name
log_file_name = "log.log"  # Replace with the actual shared log file name

# Define the list of script names to check
script_names_to_check = ["file_name1", "file_name2", "file_name3","shivam"]  # Replace with your script names

# Define the webhook URL for sending alerts
webhook_url = "https://harveynashvn.webhook.office.com/webhookb2/b294e964-378d-4614-809d-63e00418c752@f4308c54-0208-43d3-afad-1f8df2f678b7/IncomingWebhook/b2694466d1924746bdf7c5a9a7f6fe09/2182c001-bd16-4d62-bd9b-d7b387e4a431"  # Replace with your webhook URL

# Get the current date
current_date = datetime.date.today().strftime("%Y-%m-%d")

# Initialize a set to store the unique script names to check
unique_script_names = set(script_names_to_check)

# Initialize a set to store the completed script names
completed_scripts = set()

# Construct the path to the shared log file
log_file_path = os.path.join(log_folder, log_file_name)

# Check if the shared log file exists
if not os.path.isfile(log_file_path):
    print(f"Shared log file '{log_file_name}' does not exist.")
else:
    # Read the contents of the shared log file
    with open(log_file_path, "r") as file:
        log_content = file.readlines()

    # Iterate over each line in the log content
    for line in log_content:
        # Split the line into date, time, script name, and status
        parts = line.strip().split(" ")

        # Check if the line is for the current date and the script name is in the unique script names to check
        if parts[0] == current_date and parts[2] in unique_script_names:
            # Add the script name to the completed scripts set
            completed_scripts.add(parts[2])

# Get the names of scripts that didn't complete
incomplete_scripts = unique_script_names - completed_scripts

# Send the list of incomplete scripts to the webhook
if incomplete_scripts:
    alert_message = "Scripts that didn't complete:\n" + "\n".join(incomplete_scripts)
    print(alert_message)

    # Send the alert to the webhook
    response = requests.post(webhook_url, json={"message": alert_message})

    # Check the response status
    if response.status_code == 200:
        print("Alert sent successfully.")
    else:
        print(f"Failed to send alert. Status code: {response.status_code}")
else:
    print("All scripts are completed.")
