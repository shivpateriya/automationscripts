import boto3
import requests
import datetime
import logging
import os

def setup_logging():
    log_folder = "logs"  # Specify the folder where logs should be saved
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, "glue_job_logs.log")

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log_file
    )

    # Add a file handler to enable appending logs
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
    logging.getLogger().addHandler(file_handler)

def check_glue_job_status(job_names, region, webhook_url):
    glue_client = boto3.client('glue', region_name=region)
    failed_jobs = {}
    current_time = datetime.datetime.utcnow()
    one_hour_ago = current_time - datetime.timedelta(hours=1)
    today = current_time.date()

    for job_name in job_names:
        try:
            response = glue_client.get_job_runs(JobName=job_name)
            job_runs = response['JobRuns']

            if len(job_runs) > 0:
                failed_count = 0
                for job_run in job_runs:
                    job_run_state = job_run['JobRunState']
                    job_run_time = job_run['StartedOn'].replace(tzinfo=None)  # Convert to naive datetime

                    if job_run_state == 'FAILED' and job_run_time >= one_hour_ago:
                        failed_count += 1

                if failed_count > 0:
                    # Check failed count for today
                    response = glue_client.get_job_run(JobName=job_name, RunId={'PrevRunId': 'PREV_SUCCESSFUL'})
                    today_failed_count = response['JobRun']['Attempt']

                    failed_jobs[job_name] = (failed_count, today_failed_count)

            else:
                logging.info(f"No job runs found for the job '{job_name}'.")

        except glue_client.exceptions.EntityNotFoundException:
            logging.error(f"The job '{job_name}' does not exist.")

        except Exception as e:
            logging.error(f"An error occurred while checking the job status for '{job_name}': {str(e)}")

    if failed_jobs:
        send_webhook(webhook_url, failed_jobs)

def send_webhook(webhook_url, failed_jobs):
    message = "**AWS Glue Job Status**\n\nThese jobs have failed in the last 1 hour:\n\n"
    for job_name, (failed_count, today_failed_count) in failed_jobs.items():
        message += f"Job Name: {job_name}\n"
        message += f"Number of Failures in the Last 1 Hour: {failed_count}\n"
        message += f"Number of Failures Today: {today_failed_count}\n\n"

    data = {
        "text": message,
        "mrkdwn": True
    }

    logging.info("Sending webhook message:")
    logging.info(message)

    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            logging.info("Webhook sent successfully.")
        else:
            logging.error("Failed to send webhook. Status code: %d", response.status_code)

    except requests.exceptions.RequestException as e:
        logging.error("An error occurred while sending the webhook: %s", str(e))

# Setup logging
setup_logging


# Usage: Provide a list of Glue job names, the region, and the webhook URL as arguments to the function
job_names = [""]
region = "us-east-1"
webhook_url = "https://your_webhook_url_here"
check_glue_job_status(job_names, region, webhook_url)
