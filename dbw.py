# Define the name of the input file
input_file = "dbw.dat"

# Read the list of file locations from the input file
with open(input_file, "r") as file:
    file_locations = file.read().splitlines()

# Modify the file locations in-place
for i in range(len(file_locations)):
    file_locations[i] = file_locations[i].rsplit('.', 1)[0]

# Write the modified list of file locations back to the input file
with open(input_file, "w") as file:
    file.write("\n".join(file_locations))

print("File locations have been modified in-place in", input_file)
