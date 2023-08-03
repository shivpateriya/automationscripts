import boto3
from datetime import datetime, timedelta, timezone

# Replace with your S3 bucket name
bucket_name = 'askdevops'

def check_for_new_files():
    s3_client = boto3.client('s3')

    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='shivam/')
    except Exception as e:
        print(f"Error: {e}")
        return

    objects = response.get('Contents', [])
    if not objects:
        print("No files found.")
        return

    current_time = datetime.now(timezone.utc)
    five_minutes_ago = current_time - timedelta(minutes=5)

    for obj in objects:
        last_modified_time = obj['LastModified'].astimezone(timezone.utc)
        if last_modified_time >= five_minutes_ago:
            print(f"Rejectbucket:", obj['Key'])  

if __name__ == "__main__":
    check_for_new_files()
