import os
from datetime import datetime

def get_all_files_info(directory):
    files_info = {}

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath):
            mod_time = os.path.getmtime(filepath)
            mod_time = datetime.fromtimestamp(mod_time)
            files_info[filename] = mod_time

    return files_info

# Example usage:
directory = '/path/to/your/files'
all_files_info = get_all_files_info(directory)

for filename, mod_date in all_files_info.items():
    print(f"Filename: {filename}, Modification date: {mod_date}")
