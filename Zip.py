import zipfile
import os

def create_zip(zip_name, file_list):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_list:
            zipf.write(file, os.path.basename(file))
    return zip_name

# Example usage
files_to_zip = ['file1.txt', 'file2.txt']  # Replace with your files
zip_filename = 'files.zip'
create_zip(zip_filename, files_to_zip)
