import os

# Define the name of the input file
input_file = "dbw.dat"

# Read the list of file locations from the input file
with open(input_file, "r") as file:
    file_locations = file.read().splitlines()

# Function to check if a directory with extension exists
def directory_exists_with_extension(location, extension):
    directory = os.path.join(location, extension)
    return os.path.exists(directory)

# Process each file location
new_file_locations = []

for location in file_locations:
    parts = location.rsplit('.', 1)
    
    if len(parts) == 2:
        name, _ = parts
        if directory_exists_with_extension(name, '1'):
            new_file_locations.append(f"{name}.1")
        else:
            new_file_locations.append(f"{name}.0")
    else:
        new_file_locations.append(location)

# Write the modified list of file locations back to the input file
with open(input_file, "w") as file:
    file.writelines("\n".join(new_file_locations))

print("File locations have been modified in", input_file)
