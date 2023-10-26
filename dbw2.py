import os

# Define the name of the input file
input_file = "dbw.dat"

# Read the list of file locations from the input file
with open(input_file, "r") as file:
    file_locations = file.read().splitlines()

new_file_locations = []

for location in file_locations:
    location = location + ".0" if os.path.exists(location) else location + ".1"
    new_file_locations.append(location)

# Write the modified list of file locations back to the input file
with open(input_file, "w") as file:
    file.writelines("\n".join(new_file_locations))

# Now, let's check which directories don't exist
non_existent_directories = []

for location in file_locations:
    if not os.path.exists(location):
        non_existent_directories.append(location)

if non_existent_directories:
    print("Directories that don't exist:")
    for directory in non_existent_directories:
        print(directory)
else:
    print("All directories exist.")

