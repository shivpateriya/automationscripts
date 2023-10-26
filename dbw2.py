import os

# Define the name of the input file and the not_found file
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

    if not os.path.exists(location):
        non_existent_directories.append(location)

# Write the modified list of file locations back to the input file
with open(input_file, "w") as file:
    file.writelines("\n".join(new_file_locations)

# Save the non-existent directories to not_found.txt
if non_existent_directories:
    with open(not_found_file, "w") as not_found:
        not_found.writelines("\n".join(non_existent_directories))

# Now, remove the non-existent directories from the original list
file_locations = [location for location in file_locations if location not in non_existent_directories]

# Write the cleaned list of file locations back to the input file
with open(input_file, "w") as file:
    file.writelines("\n".join(file_locations))

print("Directories that don't exist have been saved in not_found.txt and removed from", input_file)
