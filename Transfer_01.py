
import os
from datetime import datetime, timedelta
import shutil
import time
from tqdm import tqdm

    
def list_files_with_mod_time(folder_path):
    """
    List all files in the given folder along with their modification times.

    Args:
        folder_path (str): Path to the folder to list files from.

    Returns:
        list: A list of tuples containing file names and their modification times.
    """
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return []

    files_with_mod_time = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            files_with_mod_time.append((mod_time, file_name))
            files_with_mod_time.sort(reverse=True, key=lambda x: x[0])

    # print(files_with_mod_time)       
    return files_with_mod_time


def process_files_by_modification_date(files, folder_path):
    """
    Process files based on their modification date, separating them into weekdays and weekends.

    Args:
        files (list): List of tuples containing modification times and file names.
        folder_path (str): Path to the folder containing the files.

    Returns:
        dict: A dictionary containing the latest weekday and weekend files, and all files modified on the last day.
    """
    last_day_files = [
        file for mod_time, file in files 
        if datetime.fromtimestamp(mod_time).date() == (datetime.now().date() )
    ]

    # Separate files into weekdays and weekends
    weekday_files = [
        file for file in last_day_files 
        if datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_path, file))).weekday() < 5
    ]
    weekend_files = [
        file for file in last_day_files 
        if datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_path, file))).weekday() >= 5
    ]

    # Get the latest file from weekdays
    latest_weekday_file = weekday_files[0] if weekday_files else None

    # Get the latest file from weekends
    latest_weekend_file = weekend_files[0] if weekend_files else None

    return {
        "latest_weekday_file": latest_weekday_file,
        "latest_weekend_file": latest_weekend_file,
        "last_day_files": last_day_files
    }

# Find the last modified file in Folders/Folder_01
def copy_last_modified_file(source_folder, destination_folder):
    """
    Copy the most recently modified file from the source folder to the destination folder with a progress bar.

    Args:
        source_folder (str): Path to the source folder.
        destination_folder (str): Path to the destination folder.
    """

    files = list_files_with_mod_time(source_folder)
    if files:
        last_modified_file = files[0][1]  # Get the file name of the most recently modified file
        source_path = os.path.join(source_folder, last_modified_file)
        destination_path = os.path.join(destination_folder, last_modified_file)

        # Check if the file already exists in the destination folder
        if os.path.exists(destination_path):
            print(f"The file '{last_modified_file}' already exists in '{destination_folder}'.")
        else:
            # Copy the file to the destination folder with a progress bar
            os.makedirs(destination_folder, exist_ok=True)
            file_size = os.path.getsize(source_path)
            with open(source_path, 'rb') as src, open(destination_path, 'wb') as dst:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Copying {last_modified_file}") as pbar:
                    while chunk := src.read(1024 * 1024):  # Read in chunks of 1MB
                        dst.write(chunk)
                        pbar.update(len(chunk))
            print(f"Copied '{last_modified_file}' to '{destination_folder}'.")
    else:
        print(f"No files found in '{source_folder}'.")

# Example usage
files = list_files_with_mod_time("Folders/Folder_01")
result = process_files_by_modification_date(files, "Folders/Folder_01")
if result["latest_weekday_file"]:
    print(f"Latest file from the last weekday: {result['latest_weekday_file']}")
else:
    print("No files were modified on the last weekday.")

if result["latest_weekend_file"]:
    print(f"Latest file from the last weekend: {result['latest_weekend_file']}")
else:
    print("No files were modified on the last weekend.")

copy_last_modified_file("Folders/Folder_01", "Folders/Folder_02")

# print(result["last_day_files"])



