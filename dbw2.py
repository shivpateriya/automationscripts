import os

# Define the name of the input file
input_file = "dbw.dat"
not_found_file = "not_found.txt"

# Read the list of file locations from the input file
with open(input_file, "r") as file:
    file_locations = file.read().splitlines()

new_file_locations = []
non_existent_directories = []

for location in file_locations:
    location = location + ".0" if os.path.exists(location) else location + ".1"
    new_file_locations.append(location)

# Now, let's check which directories don't exist
for location in new_file_locations:
    if not os.path.exists(location):
        non_existent_directories.append(location)

# Write the non-existent directories to not_found.txt
if non_existent_directories:
    with open(not_found_file, "w") as not_found:
        not_found.writelines("\n".join(non_existent_directories))

# Remove non-existent directories from dbw.dat
new_file_locations = [location for location in new_file_locations if os.path.exists(location)]

# Write the modified list of file locations back to the input file
with open(input_file, "w") as file:
    file.writelines("\n".join(new_file_locations))

print("Directories that don't exist have been saved in not_found.txt and removed from", input_file)
