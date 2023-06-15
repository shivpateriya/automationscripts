import requests

data = ['message1', 'message2', 'message3']

# Create the payload
payload = {
    "text": "**Operational REPORT**\n\n" +"\n\n".join(data)
}

# Send the POST request to the webhook URL
response = requests.post(webhook_url, json=payload)
print(response)
# Check the response status
if response.status_code == 200:
    print("Messages sent successfully!")
else:
    print("Failed to send messages.")
