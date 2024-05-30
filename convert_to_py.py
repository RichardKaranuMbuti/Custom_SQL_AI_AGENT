import glob
import os
import shutil


def convert_and_rename(folder_path):
    # Iterate through all files and folders recursively
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if file has .pyx extension
            if file.endswith(".pyx"):
                file_path = os.path.join(root, file)

                # Rename .pyx to .py
                new_file_path = file_path[:-4] + ".py"
                shutil.move(file_path, new_file_path)
                print(f"Converted '{file}' to '{new_file_path}'")


# Replace 'folder_path' with the path to your target folder
folder_path = "panafrican_ai"
convert_and_rename(folder_path)
