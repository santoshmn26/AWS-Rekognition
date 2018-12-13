import boto3
import sys
s3 = boto3.client('s3')
bucket = 'reko-face'                # Bucket name for storing the image in s3
file_name = sys.argv[1]             # First argument to pass the path of the file
key_name = sys.argv[2]              # Second argument to pass the name of the file to be stored in s3
s3.upload_file(file_name, bucket, key_name)  # upload_file API call to store the image in s3
