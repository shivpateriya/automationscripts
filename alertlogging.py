import datetime
import requests

# Define the webhook URL for sending alerts
webhook_url = "https://harveynashvn.webhook.office.com/webhookb2/b294e964-378d-4614-809d-63e00418c752@f4308c54-0208-43d3-afad-1f8df2f678b7/IncomingWebhook/21581f962ee1423ba16975d5048a6287/2182c001-bd16-4d62-bd9b-d7b387e4a431"

# Get the current date
current_date = datetime.date.today().strftime("%Y-%m-%d")

# Create the log file name for today's date
log_filename = f"{current_date}.log"

# Read the log file
with open(log_filename, "r") as log_file:
    log_content = log_file.read()

# Check if the log file contains the "completed" message
if "completed" not in log_content:
    # Create the alert message
    alert_message = f"Logging file for {current_date} does not contain 'completed'."

    # Send the alert to the webhook
    response = requests.post(webhook_url, json={"message": alert_message})

    # Check the response status
    if response.status_code == 200:
        print("Alert sent successfully.")
    else:
        print(f"Failed to send alert. Status code: {response.status_code}")
else:
    print("Logging file is complete.")
