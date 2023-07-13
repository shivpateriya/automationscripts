import datetime
import os

# Define the log folder path
log_folder = "path/to/log/folder"  # Replace with the actual log folder path

# Define the shared log file name
log_file_name = "shared_log.log"  # Replace with the actual shared log file name

# Define the list of script names to check
script_names_to_check = ["file_name1", "file_name2", "file_name3"]  # Replace with your script names

# Get the current date
current_date = datetime.date.today()

# Initialize a list to store the names of scripts that didn't complete
incomplete_scripts = []

# Construct the path to the shared log file
log_file_path = os.path.join(log_folder, log_file_name)

# Check if the shared log file exists
if not os.path.isfile(log_file_path):
    print(f"Shared log file '{log_file_name}' does not exist.")
else:
    # Read the contents of the shared log file
    with open(log_file_path, "r") as file:
        log_content = file.readlines()

    # Check if the completion status exists for each script name
    for script_name in script_names_to_check:
        completion_status = f"{current_date} {script_name} has successfully completed"
        found = False

        # Check if the completion status is found in the log content
        for line in log_content:
            if line.startswith(completion_status):
                found = True
                break

        if not found:
            incomplete_scripts.append(script_name)

# Print the names of scripts that didn't complete
if incomplete_scripts:
    print("Scripts that didn't complete:")
    for script_name in incomplete_scripts:
        print(script_name)
else:
    print("All scripts are completed.")
