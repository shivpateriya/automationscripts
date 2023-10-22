import os

# Define the name of the input file
input_file = "dbw.dat"

# Read the list of file locations from the input file
with open(input_file, "r") as file:
    file_locations = file.read().splitlines()

# Function to check for .0 or .1 files and add them to a list
def find_matching_files(locations):
    matching_files = []

    for location in locations:
        for ext in ['.0', '.1']:
            file_path = f"{location}{ext}"
            if os.path.exists(file_path):
                matching_files.append(file_path)

    return matching_files

# Find matching files in the locations from dbw.dat
matching_files = find_matching_files(file_locations)

# Modify the file locations in dbw.dat based on matching files
with open(input_file, "w") as file:
    for location in file_locations:
        if location in matching_files:
            modified_location = f"{location}.1"
        else:
            modified_location = f"{location}.0"
        file.write(modified_location + "\n")

if matching_files:
    print("Matching files found:")
    for file in matching_files:
        print(file)
else:
    print("No matching files found.")
