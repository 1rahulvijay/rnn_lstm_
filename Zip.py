import zipfile
import os

def create_zip(zip_name, file_list, output_folder):
    zip_path = os.path.join(output_folder, zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in file_list:
            # Write the file to the zip archive with its basename to avoid including the directory structure
            zipf.write(file, os.path.basename(file))
    return zip_path

# Example usage
output_folder = 'output_folder'  # Folder where the zip file will be saved

# Full paths to the files you want to zip
files_to_zip = [
    'folder1/file1.txt', 
    'folder1/file3.txt',
    'folder2/file2.txt'
]

zip_filename = 'files.zip'
create_zip(zip_filename, files_to_zip, output_folder)
