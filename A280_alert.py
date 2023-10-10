import boto3
import requests
import json
import datetime

# AWS S3 and Microsoft Teams webhook configuration
s3_bucket_name = "your-s3-bucket-name"
s3_prefix = "268/"
teams_webhook_url = "your-teams-webhook-url"

# Initialize S3 and Teams webhook
s3_client = boto3.client("s3")
message = {"text": "No new files with prefix '268' were added to the S3 bucket today."}

def send_alert():
    response = requests.post(
        teams_webhook_url,
        data=json.dumps(message),
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()  # This may raise an exception for non-200 HTTP status codes

def main():
    current_date = datetime.date.today()
    
    # List objects in the S3 bucket with the specified prefix and created today
    objects_created_today = [
        obj for obj in s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=s3_prefix).get("Contents", [])
        if obj["LastModified"].date() == current_date
    ]

    # Check if no objects were created today
    if not objects_created_today:
        # No new files were added today, send an alert
        send_alert()

if __name__ == "__main__":
    main()
