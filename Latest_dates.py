import os
from datetime import datetime

def get_latest_file(directory):
    # List to store file names and their modification times
    files_with_dates = []

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        # Check if it's a file (not a directory)
        if os.path.isfile(filepath):
            # Get the last modification time and convert it to a datetime object
            mod_time = os.path.getmtime(filepath)
            mod_time = datetime.fromtimestamp(mod_time)
            files_with_dates.append((filename, mod_time))

    # If no files found, return None
    if not files_with_dates:
        return None, None

    # Sort the list by modification date, newest first
    files_with_dates.sort(key=lambda x: x[1], reverse=True)

    # Get the latest file
    latest_file, latest_date = files_with_dates[0]

    return latest_file, latest_date

# Example usage:
directory = '/path/to/your/files'
latest_file, latest_date = get_latest_file(directory)
if latest_file:
    print(f"The latest file is: {latest_file}")
    print(f"Modification date: {latest_date}")
else:
    print("No files found in the directory.")
