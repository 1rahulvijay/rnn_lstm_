import subprocess
import os

def set_permissions_to_777(folder_path):
    """
    Check the current permissions of a folder and set them to 777 if not already set.

    :param folder_path: Path to the folder
    """
    try:
        # Get the current permissions of the folder
        current_permissions = oct(os.stat(folder_path).st_mode)[-3:]

        # Check if the permissions are not already 777
        if current_permissions != "777":
            # Execute the chmod command to change permissions
            subprocess.run(["chmod", "777", folder_path], check=True)
            print(f"Permissions changed to 777 for {folder_path}")
        else:
            print(f"Permissions are already 777 for {folder_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
folder_path = "/path/to/your/folder"
set_permissions_to_777(folder_path)
