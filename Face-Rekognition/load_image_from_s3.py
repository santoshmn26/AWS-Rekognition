import boto3
import sys

if __name__ == "__main__":

    imageFile=sys.argv[1]       # image file to detect labels
    bucket=sys.argv[2]
    client=boto3.client('rekognition')
    
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':imageFile}})
        
    print('Detected labels in ' + imageFile)    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))

    print('Done...')
