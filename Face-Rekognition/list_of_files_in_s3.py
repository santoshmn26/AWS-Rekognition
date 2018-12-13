import boto3
import sys

bucket=sys.argv[1]

client=boto3.client('s3')

files=client.list_objects(Bucket=bucket)

for file in files['Contents']:
    print(file['Key'])
