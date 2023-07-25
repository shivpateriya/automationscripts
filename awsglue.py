import boto3
from datetime import datetime, date

# List of AWS Glue job names
glue_job_names = ["job_name_1", "job_name_2", "job_name_3"]
aws_region = "<your_aws_region>"

def get_failed_glue_jobs(job_names):
    glue_client = boto3.client("glue", region_name=aws_region)

    failed_jobs = []

    for job_name in job_names:
        try:
            response = glue_client.get_job_runs(JobName=job_name, MaxResults=100)
            if "JobRuns" in response:
                for job_run in response["JobRuns"]:
                    run_date = datetime.strptime(job_run["StartedOn"], "%Y-%m-%d %H:%M:%S.%f").date()
                    if run_date == date.today():
                        status = job_run["JobRunState"]

                        if status == "FAILED":
                            failed_jobs.append({"JobName": job_name, "JobRunId": job_run["JobRunId"]})
                        else:
                            print(f"Job '{job_name}' status: {status}")
            else:
                print(f"No job runs found for the Glue job '{job_name}'.")
        except Exception as e:
            print(f"Error: {e}")

    return failed_jobs

if __name__ == "__main__":
    failed_jobs = get_failed_glue_jobs(glue_job_names)
    if failed_jobs:
        print("Failed Glue Jobs:")
        for job in failed_jobs:
            print(f"Job Name: {job['JobName']}, Job Run Id: {job['JobRunId']}")
    else:
        print("No failed Glue jobs found.")
