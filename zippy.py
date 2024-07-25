#!/usr/bin/python3

import boto3
import zipfile
import io
import fire

def zip_s3_files(bucket_name, file_list_path, output_dir):
    print("Starting zipper!")
    
    s3 = boto3.client('s3')
    zip_buffer = io.BytesIO()

    print("Creating zip file")

    with zipfile.ZipFile(zip_buffer, 'w') as z:
        with open(file_list_path, 'r') as file_list:
            for file_key in file_list:
                file_key = file_key.strip()
                if not file_key:
                    continue
                print(f"Processing {file_key}")
                # Downloading file
                file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
                # Writing file to the zip archive
                file_data = file_obj['Body'].read()
                z.writestr(file_key, file_data)

    zip_file_key = f'{output_dir}/zipped_files.zip'

    print("Uploading...")
    # Uploading the zip file to the bucket
    zip_buffer.seek(0)
    s3.put_object(Bucket=bucket_name, Key=zip_file_key, Body=zip_buffer.getvalue())

    print(f'Zip file {zip_file_key} created successfully in bucket {bucket_name}.')

if __name__ == '__main__':
    fire.Fire(zip_s3_files)