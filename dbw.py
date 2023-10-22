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

# Modify the file locations and save them to dbw_modified.dat
new_file_locations = []
for location in file_locations:
    new_location = location.rsplit('.', 1)[0]
    new_file_locations.append(new_location)

# Define the name of the output file
output_file = "dbw_modified.dat"

# Write the modified list of file locations to the output file
with open(output_file, "w") as file:
    file.writelines("\n".join(new_file_locations))

print("File locations have been modified and saved to", output_file)

if matching_files:
    print("Matching files found:")
    for file in matching_files:
        print(file)
else:
    print("No matching files found.")
