import os

# Specify the path to your dbw.dat file
dbw_file = 'dbw.dat'

# Read the directories from the file
with open(dbw_file, 'r') as file:
    directories = file.read().splitlines()

# Check if each directory exists
for directory in directories:
    if os.path.exists(directory):
        print(f"Directory '{directory}' exists.")
    else:
        print(f"Directory '{directory}' does not exist.")
