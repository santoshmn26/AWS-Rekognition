import boto3

if __name__ == "__main__":

    bucket='reko-face'
    imageFile='car.jpg'

    client=boto3.client('rekognition')

    with open(imageFile, 'rb') as image:
        response=client.detect_text(Image={'Bytes': image.read()})

                        
    textDetections=response['TextDetections']
    #print (response)
    #print ('Matching faces')
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])

