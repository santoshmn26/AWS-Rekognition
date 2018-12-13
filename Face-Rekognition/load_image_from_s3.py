import boto3

if __name__ == "__main__":

    imageFile="image.jpg"       # image file to detect labels
    client=boto3.client('rekognition')
    
    response = client.detect_labels(Image=imageFile)
        
    print('Detected labels in ' + imageFile)    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))

    print('Done...')
