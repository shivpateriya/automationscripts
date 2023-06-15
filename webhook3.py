import requests
import json


messages = ['message1', 'message2', 'message3']

# Format the messages with line breaks
formatted_message = '\n'.join(messages)

# Create the payload
payload = {
    "text": formatted_message
}

# Convert the payload to JSON
payload_json = json.dumps(payload)

# Send the POST request to the webhook URL
response = requests.post(webhook_url, data=payload_json, headers={'Content-Type': 'application/json'})

# Check the response status
if response.status_code == 200:
    print("Messages sent successfully!")
else:
    print("Failed to send messages.")
