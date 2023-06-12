import subprocess

def check_cronjob_status():
    # Replace 'cronjob_command' with the actual command of your cron job
    cronjob_command = 'python3 /home/knoldus/pythonscripts/alertS3/helllp.py'
    
    # Run the cron job command and capture the output
    try:
        result = subprocess.run(cronjob_command, capture_output=True, text=True, shell=True)
        
        # Check the command's return code
        if result.returncode == 0:
            print("Cron job executed successfully.")
        else:
            print("Cron job failed.")
            
        # Check the output for error messages
        if result.stderr:
            print("Error message:", result.stderr)
    
    except subprocess.CalledProcessError as e:
        print("Error occurred while running cron job:")
        print(e)

check_cronjob_status()
