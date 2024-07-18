import os
import zipfile
import subprocess

# Define the directory to be zipped and the zip file name
directory_to_zip = 'amplify'
zip_file_name = 'my_app.zip'

# Remove the old zip file if it exists
if os.path.exists(zip_file_name):
    os.remove(zip_file_name)
    print(f"Deleted old zip file: {zip_file_name}")

# Create a new zip file with the contents of the specified directory
with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(directory_to_zip):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, directory_to_zip))

print(f"Created new zip file: {zip_file_name}")
