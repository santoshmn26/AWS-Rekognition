import cv2
import boto3
import os

#---------------------------------------------------------------------
# Capturing face for login verification

def retry(login_attempt):
    capture=cv2.VideoCapture(0)
    while(capture.isOpened()):
        ret, frame = capture.read()
        if ret:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite("screenshot.jpg",frame)
                capture.release()
                cv2.destroyAllWindows()
                break

    try:
        imageFile="screenshot.jpg"     # Path for the generated file
        with open(imageFile, 'rb') as image:
            response=client.search_faces_by_image(CollectionId=collectionId,
                                        Image={'Bytes': image.read()},
                                        FaceMatchThreshold=threshold,
                                        MaxFaces=maxFaces)
            print("here")
            return(response)

    except:
        print("Failed to login!")
        os.remove("screenshot.jpg")
        login_attempt+=1
        if(login_attempt>4):
            exit()
        response=retry(login_attempt)
        return(response)
        
#---------------------------------------------------------------------

collectionId='MyCollection'                  # Collection of faces stored
threshold = 15                               # Confidence level of detection
maxFaces=2                                   # Maximum number of faces to detect
login_attempt=1
client=boto3.client('rekognition')
response=retry(login_attempt)                       
faceMatches=response['FaceMatches']
for match in faceMatches:
    print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
    match['Face']['ExternalImageId']=match['Face']['ExternalImageId'].split('.')
    print('ExternalImageId:', match['Face']['ExternalImageId'][0])

#---------------------------------------------------------------------

os.remove("screenshot.jpg")