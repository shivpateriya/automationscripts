import glob
import os

# Define the directory containing the log files
log_dir = "/path/to/log/dir"

# Construct the pattern to match the log files for the current day
pattern = f"{log_dir}/*ngest*20230717*"

# Get the list of log files matching the pattern
log_files = glob.glob(pattern)

# Iterate over each log file
for file in log_files:
    errors = []
    capture_next_lines = False
    captured_data = []
    
    # Open the log file and search for lines containing "Error"
    with open(file, encoding="utf-8") as f:
        for line in f:
            if "Error" in line:
                errors.append(line.strip())
                capture_next_lines = True
            elif capture_next_lines and line.strip() == "":
                capture_next_lines = False
                if captured_data:
                    print(f"Data after 'Unsuccessfully published' in {os.path.basename(file)}:")
                    for data_line in captured_data:
                        print(data_line)
                    captured_data = []
            elif capture_next_lines:
                captured_data.append(line.strip())
    
    # If the file contains errors, print its name and the error lines
    if errors:
        print(f"Errors in {os.path.basename(file)}:")
        for error in errors:
            print(error)
