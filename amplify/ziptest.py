import boto3
import zipfile
import io

print("Starting zipper!")

s3 = boto3.client('s3')
source_bucket = 'cadas-testing-data'
zip_file_key = 'zipped-datasets/datasets.zip'
zip_buffer = io.BytesIO()

print("Creating zip file")

with zipfile.ZipFile(zip_buffer, 'w') as z:
    # Listing files in the bucket
    response = s3.list_objects_v2(Bucket=source_bucket, Prefix='data/')
    for obj in response.get('Contents', []):
        print(obj)
        file_key = obj['Key']
        # Downloading file
        file_obj = s3.get_object(Bucket=source_bucket, Key=file_key)
        # Writing file to the zip archive
        file_data = file_obj['Body'].read()
        z.writestr(file_key, file_data)

print("Uploading...")
# Uploading the zip file to the bucket
zip_buffer.seek(0)
s3.put_object(Bucket=source_bucket, Key=zip_file_key, Body=zip_buffer.getvalue())

print(f'Zip file {zip_file_key} created successfully in bucket {source_bucket}.')