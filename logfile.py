import os
import glob
import re
import subprocess
from datetime import datetime

def process_logs_and_update_dbw_dat(user_input):
    os.chdir("/apps/kx/delta-data/DeltaControlData/logdir")

    current_date = datetime.now()
    year = current_date.year
    month = current_date.month

    Eod_month = f"{year}{month:02}"

    pattern = f"*DBW*{Eod_month}*"
    print(pattern)

    grep_command = f'grep EOD {pattern} | grep elapsed | grep {user_input}'

    output = os.popen(grep_command).read()
    exit_code = os.system(grep_command)

    if output:
        print("Logs found for this date:")
        logs = [line.split('.log')[0] + '.log' for line in output.split('\n')]
        logs = logs[0]

        create_dbw_dat = f"grep 'DBW Write :' {logs} | grep kxsReading | grep complete | awk '{{print $7}}' | sed 's/://' | sed 's/\/$//' | grep -v apps > ~/Guardians/shivam/dbw.dat"
        os.system(create_dbw_dat)
    else:
        print("No logs found for this date.")

# Call the function with user input
user_input = input("Enter the date (format: 2023.11.02): ")
process_logs_and_update_dbw_dat(user_input)

# Rest of your original code
input_file = "dbw.dat"
# ... (the rest of your code remains unchanged)





#---------------------

# Directory where the eod*.csv files are located
directory_path = "eeec"

# Initialize the output file with a header
output_filename = "EOD_Analysis_2023_10_31.csv"
with open(output_filename, 'w') as output_file:
    output_file.write("Filename, Data\n")

# Loop over the input files in the specific directory
for filename in glob.glob(os.path.join(directory_path, 'eod*.csv')):
    d = filename.replace(os.path.join(directory_path, 'eod_analysis_'), '').replace('.csv', '').replace('.', '-')
    dat = subprocess.check_output(['cat', filename], universal_newlines=True).replace('\n', ' ')
    
    # Append the data to the output file
    with open(output_filename, 'a') as output_file:
        output_file.write(f'{d}, {dat}\n')

# Now, run the sed command
subprocess.run(['sed', '-i', 's/\/.*//g', os.path.join(directory_path, 'eod*')])

# Finally, run the loop
for filename in glob.glob(os.path.join(directory_path, 'eod*.csv')):
    d = filename.replace(os.path.join(directory_path, 'eod_analysis_'), '').replace('.csv', '').replace('.', '-')
    dat = subprocess.check_output(['cat', filename], universal_newlines=True).replace('\n', ' ')
    with open(output_filename, 'a') as output_file:
        output_file.write(f'{d}, {dat}\n')
