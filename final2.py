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
    
    # Add ".0" and ".1" to the location
    location_with_0 = location_with_wildcard + ".0"
    location_with_1 = location_with_wildcard + ".1"

    # Check if the location with "0" exists
    if os.path.exists(location_with_0):
        new_file_locations.append(os.path.abspath(location_with_0))
    # Check if the location with "1" exists
    elif os.path.exists(location_with_1):
        new_file_locations.append(os.path.abspath(location_with_1))
    # If neither "0" nor "1" exists, use the original location
    else:
        new_file_locations.append(os.path.abspath(location))

# Write the modified absolute paths back to the input file
with open(input_file, "w") as file:
    file.writelines("\n".join(new_file_locations))

print("File locations have been updated in", input_file)
