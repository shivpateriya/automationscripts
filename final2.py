import os
import glob
import re

# Define the name of the input file
input_file = "dbw.dat"

# Read the list of file locations from the input file
with open(input_file, "r") as file:
    file_locations = file.read().splitlines()

# Now, let's check which directories don't exist
new_file_locations = []

for location in file_locations:
    # Replace "hdb", "hdb2", "hdb3", or "hdb4" with "hdb*"
    location_with_wildcard = re.sub(r"hdb[2-4]?", "hdb*", location)

    # Use glob to check if any files or directories match the wildcard location
    matching_files = glob.glob(location_with_wildcard + ".*")

    if matching_files:
        # If matching files exist, use the first matching file's absolute path
        location = os.path.abspath(matching_files[0])
    else:
        location = os.path.abspath(location)  # Use the original location if no matches found

    new_file_locations.append(location)

# Write the modified absolute paths back to the input file
with open(input_file, "w") as file:
    file.writelines("\n".join(new_file_locations))

print("File locations have been updated in", input_file)
