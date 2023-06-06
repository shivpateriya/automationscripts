#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta
from pytz import timezone
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler and set the log file path
log_file = 'Reject_bucket.log'
file_handler = logging.FileHandler(log_file)

# Set the format for the file handler
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add the file handler to the root logger
logging.getLogger('').addHandler(file_handler)

def send_notification(new_files):
    # Replace <webhook_url> with the actual webhook URL
    webhook_url = ''
    message = f"The following new files were found in the S3 bucket:\n\n{', '.join(new_files)}"
    try:
        # Make an HTTP POST request to the webhook URL
        response = requests.post(webhook_url, json={'message': message})
        response.raise_for_status()  # Raise an exception if the request fails
        logging.info("Notification sent successfully!")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send notification: {str(e)}")

def check_new_files(bucket_name, prefixes):
    s3 = boto3.client('s3')

    # Get the current time and calculate the time 5 minutes ago
    current_time = datetime.now(timezone('UTC'))
    five_minutes_ago = current_time - timedelta(minutes=5)

    new_files = []  # List to store the new files found

    for prefix in prefixes:
        # List objects in the bucket with the specified prefix
        response = s3.list_objects(Bucket=bucket_name, Prefix=prefix)

        logging.debug(f"S3 Response for prefix '{prefix}': {response}")

        # Check if any file was modified within the last 5 minutes
        if 'Contents' in response:
            for obj in response['Contents']:
                last_modified = obj['LastModified'].replace(tzinfo=timezone('UTC'))
                logging.debug(f"Object Key: {obj['Key']}")
                logging.debug(f"Last Modified: {last_modified}")
                if last_modified > five_minutes_ago:
                    logging.info(f"New file found: {obj['Key']}")
                    new_files.append(obj['Key'])  # Add new file to the list

    if new_files:
        send_notification(new_files)  # Send notification with the list of new files
    else:
        logging.info("No new files found.")

# Specify your S3 bucket name and prefixes here
bucket_name = ''
prefixes = ['/', '/','']

logging.debug(f"Bucket Name: {bucket_name}")
logging.debug(f"Prefixes: {prefixes}")

check_new_files(bucket_name, prefixes)
