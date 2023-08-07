import os
from datetime import datetime, date, timezone

def get_creation_time(file_path):
    stat = os.stat(file_path)
    file_creation_time = datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).date()
    return file_creation_time

def find_files_created_today(directory_path):
    today = date.today()
    file_list = []

    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        file_creation_time = get_creation_time(file_path)
        if file_creation_time == today:
            file_list.append(file_path)

    return file_list

if __name__ == "__main__":
    directory_path = "/path/to/directory"  # Replace this with the actual directory path
    today_files = find_files_created_today(directory_path)

    if today_files:
        print("Files created today:")
        for file_path in today_files:
            print(file_path)
    else:
        print("No files created today in the specified directory.")
