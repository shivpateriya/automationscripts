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
    capture_data = False
    print_filename = True
    
    # Open the log file and search for lines containing "Error"
    with open(file, encoding="utf-8") as f:
        for line in f:
            if "Unsuccessfully published" in line:
                capture_data = True
                print_filename = True
            elif capture_data and line.strip() == "":
                capture_data = False
            elif capture_data:
                if print_filename:
                    print(f"File: {os.path.basename(file)}")
                    print_filename = False
                if "sensorID" in line and "smpID" in line and "startTs" in line and "endTs" in line and "serialNo" in line and "MDL_REF_smpID" in line:
                    print(line.strip())
                else:
                    print(line.strip())
    print("-" * 100)
