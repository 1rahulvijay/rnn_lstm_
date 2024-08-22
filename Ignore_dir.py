import os
import pandas as pd

def read_file_ignore_case(directory, filename):
    # List all files in the given directory
    all_files = os.listdir(directory)
    
    # Find the file in a case-insensitive manner
    matched_file = None
    for file in all_files:
        if file.lower() == filename.lower():
            matched_file = file
            break
    
    if matched_file is None:
        raise FileNotFoundError(f"File '{filename}' not found in directory '{directory}'")
    
    # Construct the full file path
    file_path = os.path.join(directory, matched_file)
    
    # Read the file using pandas (assuming it's a CSV file; adjust as needed)
    df = pd.read_csv(file_path)
    
    return df

# Example usage:
directory = "/path/to/your/directory"
filename = "yourfile.csv"
df = read_file_ignore_case(directory, filename)
print(df)
