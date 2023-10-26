import os

# Define the name of the input file
input_file = "dbw.dat"

# Read the list of file locations from the input file
with open(input_file, "r") as file:
    file_locations = file.read().splitlines()

# Function to check if a directory exists
def directory_exists(location):
    return os.path.exists(location)

# Process each file location
new_file_locations = []

for location in file_locations:
    location_with_1 = f"{location}.1"
    if directory_exists(location_with_1):
        new_file_locations.append(location_with_1)
    else:
        location_with_0 = f"{location}.0"
        if directory_exists(location_with_0):
            new_file_locations.append(location_with_0)
        else:
            new_file_locations.append(location)

# Write the modified list of file locations back to the input file
with open(input_file, "w") as file:
    file.writelines("\n".join(new_file_locations))

print("File locations have been modified in", input_file)
