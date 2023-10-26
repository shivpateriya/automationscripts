import os

# Define the name of the input file
input_file = "dbw.dat"

# Read the list of file locations from the input file
with open(input_file, "r") as file:
    file_locations = file.read().splitlines()

# Function to check if a directory with .0 or .1 exists
def directory_exists_with_extension(location, extension):
    directory = os.path.join(location, extension)
    return os.path.exists(directory)

# Modify the file locations and add to dbw.dat based on the criteria
new_file_locations = []
for location in file_locations:
    parts = location.rsplit('.', 1)
    if len(parts) == 2:  # If there's a dot in the location
        name, extension = parts
        if extension == '0' or extension == '1':
            if directory_exists_with_extension(name, extension):
                new_file_locations.append(location)
            else:
                new_file_locations.append(name)
        else:
            new_file_locations.append(location)
    else:
        new_file_locations.append(location)

# Write the modified list of file locations back to the input file
with open(input_file, "w") as file:
    file.writelines("\n".join(new_file_locations))

print("File locations have been modified in", input_file)
