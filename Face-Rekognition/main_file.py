import cv2
import boto3
import os

#-------------------------------------------------------------------------------------------------------------------------------
# Capturing face for login verification

def attempt_login(login_attempt):
    capture=cv2.VideoCapture(0)          # Capture input from webcam
    while(capture.isOpened()):
        ret, frame = capture.read()
        if ret:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite("screenshot.jpg",frame)     # Capture a screenshot from the webcam feed when pressed 'q'
                capture.release()
                cv2.destroyAllWindows()
                break

    try:
        imageFile="screenshot.jpg"     # Path for the generated snapshot 
        with open(imageFile, 'rb') as image:
            # Call the AWS-Rekognition service: search_faces_by_image
            response=client.search_faces_by_image(CollectionId=collectionId,
                                        Image={'Bytes': image.read()},
                                        FaceMatchThreshold=threshold,
                                        MaxFaces=maxFaces)
            return(response)           # Result for the face detected

    except:
        print("Failed to login!")
        os.remove("screenshot.jpg")    # Removing the snapshot of the user
        login_attempt+=1               # Count the user's login attempts
        if(login_attempt>4):           # Login attempt exceeds 3 exit the program
            exit()
        response=attempt_login(login_attempt)  # Login failed retry again
        return(response)               # Result for the face detected
        
#-------------------------------------------------------------------------------------------------------------------------------
# Main function

if __name__ == "__main__":
    collectionId='MyCollection'                  # Collection of faces stored
    threshold = 15                               # Confidence level of detection
    maxFaces=2                                   # Maximum number of faces to detect
    login_attempt=1
    client=boto3.client('rekognition')
    response=attempt_login(login_attempt)                       
    faceMatches=response['FaceMatches']
    for match in faceMatches:
        print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        match['Face']['ExternalImageId']=match['Face']['ExternalImageId'].split('.')
        print('ExternalImageId:', match['Face']['ExternalImageId'][0])
        os.remove("screenshot.jpg")             # Removing the saved snapshot of the user
        
#--------------------------------------------------------------------------------------------------------------------------------

