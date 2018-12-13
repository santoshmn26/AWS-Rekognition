import boto3
import sys
s3 = boto3.client('s3')
bucket = 'reko-face'
file_name = sys.argv[1]                 # First argument to pass the path of the file
key_name = sys.argv[2]              # Second argument to pass the name of the file to be stored in s3
s3.upload_file(file_name, bucket, key_name)