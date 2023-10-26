import os
import re

# Define the name of the input file
input_file = "dbw.dat"

# Read the list of file locations from the input file
with open(input_file, "r") as file:
    file_locations = file.read().splitlines()

# Function to find matching files in a directory
def find_matching_files_in_directory(directory):
    dynamic_file_pattern = re.compile(r"(kxsReadingDelta|kxsReadingHistoryDelta)\.([01])")
    matching_files = []

    for file_name in os.listdir(directory):
        match = dynamic_file_pattern.match(file_name)
        if match:
            matching_files.append(match.group(0))

    return matching_files

# Modify the file locations in dbw.dat based on matching files
with open(input_file, "w") as file:
    for location in file_locations:
        # Extract the directory path from the location
        dir_path = os.path.dirname(location)
        
        # Find matching files in the directory
        matching_files = find_matching_files_in_directory(dir_path)

        if matching_files:
            # Use the first matching file found
            modified_location = os.path.join(dir_path, re.sub(r'\.\d$', '', matching_files[0]))
        else:
            # If no matching file is found, append ".0" by default
            modified_location = re.sub(r'\.\d$', '.0', location)
        
        file.write(modified_location + "\n")

print("File locations have been modified in", input_file)
