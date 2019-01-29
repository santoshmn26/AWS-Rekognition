import cv2
import boto3
import os
import face_recognition
import math


# Animation around the face
def draw_border(img, pt1, pt2, color, thickness, r, d,i=0):
    x1,y1 = pt1
    x2,y2 = pt2
    found_face=0
    
    if(r<10):
        r=10
        #color=(0,255,0)
    
    # Top left
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
    if((y1+r+i)<(y2-r)):
        cv2.line(img, (x1, y1+r), (x1, y1+r+i), color, thickness)
    
    #Check if the value of i is maxed and a face is found
    elif((y1+i)>(y2-r)):    
        found_face=1
        return(img,found_face)
        
    # Top right
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    # Condition true if a face is present in the frame of more than 3 secs
    if((x1+r+i)<(x2-r)):
        cv2.line(img, (x1+r, y1), (x1+r+i, y1), color, thickness)
    
    # Bottom left
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    if((x1+r)<(x2-r-i)):
        cv2.line(img, (x2-r, y2), (x2-r-i, y2), color, thickness) 
    
        
    # Bottom right
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)
    if((y2-r-i)>(y1+r)):
        cv2.line(img, (x2, y2-r), (x2, y2-r-i), color, thickness)
        
    return(img,found_face)


    
# Capturing face for login verification
def attempt_login(login_attempt):

    i,r,j=1,30,1                         
    found_face=0                         # Flag to check if a face is found
    login=0
    # Initial colors red=max, green=0 and blue=0
    # Color changing rate = 9
    red,green,dec_color=255,0,9
    # Capture input from webcam
    capture=cv2.VideoCapture(0)          
    while(capture.isOpened()):
        ret, frame = capture.read()
        if ret:
            faces=(faceCascade.detectMultiScale(frame))
            if(len(faces)):             # True if a face is detected in the frame
                if(found_face==0):      # Complete face not scanned yet    
                    # values (275,175), (375,275) center of frame to locate a face in the frame.
                    frame,found_face=draw_border(frame,(225,150), (400, 325), (0, green+dec_color, red-dec_color), 2, r, 30,i)
                    dec_color+=8
                    i+=6                 # Counter to increase line animation
                    #j+=1                # Counter to decrease radius of arc animation
                elif(found_face==1&len(faces)==1):     # Face found and screenshot captured
                    if(login==0):
                        cv2.imwrite("screenshot.jpg",frame)         # Capture a screenshot of user
                        frame=cv2.rectangle(frame,(225,150), (400, 325),(0,255,0),2)
                        response = call_aws()
                        if(response==-1):
                            os.remove("screenshot.jpg")                                                      # Removing the saved snapshot of the user
                            found_face=0
                            continue
                        faceMatches=response['FaceMatches']
                        for match in faceMatches:
                            match['Face']['ExternalImageId']=match['Face']['ExternalImageId'].split('.')     # Split the image file name
                            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")              # Confidence score
                            print('ExternalImageId:', match['Face']['ExternalImageId'][0])                   # Name of the image
                            face_name = match['Face']['ExternalImageId'][0]
                            print('Face ID: ',match['Face']['FaceId'])                                       # Unique faceID
                            os.remove("screenshot.jpg")                                                      # Removing the saved snapshot of the user
                        login=1
                    else:
                        frame=cv2.rectangle(frame,(225,150), (400, 325),(0,255,0),2)
                        frame=cv2.rectangle(frame,(225,325),(400,350),(0,255,0),2)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame,face_name,(225,345),font, 1, (0,255,0), 1, cv2.LINE_AA)
                        
            # If no face is detected in the frame reset the radius value        
            else:
                if(found_face==0):
                    i=1
                    r=25
                    #j=1
                    dec_color=9
                    frame,found_face=draw_border(frame,(225,150), (400, 325), (0, green, red), 2, 20, 20)
                
            # Trigger keys to exit '1' or 'q'    
            if cv2.waitKey(1) & 0xFF == ord('q'):   
                # Check if atleast one face is detected in the frame
                if(len(faceCascade.detectMultiScale(frame))==1):    
                    # Screenshot.jpg captured if a face is detected for more than 3 secs.
                    cv2.imwrite("screenshot.jpg",frame)             # Capture a screenshot from the webcam feed when pressed 'q' or '1'
                    #capture.release()   
                    #cv2.destroyAllWindows()
                    res = call_aws()     
                    return(res)
                    
                    
                # If more than one face found in the frame
                elif(len(faceCascade.detectMultiScale(frame))>1):
                    print("Found multiple faces")
                    
                # If no faces found in the frame    
                elif(len(faceCascade.detectMultiScale(frame))<1):
                    print("No faces found!")
            
            #Display frame        
            cv2.imshow('frame', frame)
            
def call_aws():   
    print("------------------------------")
    login_attempt=0
    try:
        imageFile="screenshot.jpg"     # Path/file for the generated snapshot of the user
        with open(imageFile, 'rb') as image:
            # Call the AWS-Rekognition service: search_faces_by_image
            response=client.search_faces_by_image(CollectionId=collectionId,
                                        Image={'Bytes': image.read()},
                                        FaceMatchThreshold=threshold,
                                        MaxFaces=maxFaces)
            return(response)           # Result for the face detected
            
    # Login failed!
    except:
        print("Failed to login!")
        #os.remove("screenshot.jpg")            # Removing the snapshot of the user
        login_attempt+=1                       # Count the user's login attempts
        if(login_attempt>4):                   # Login attempt exceeds 3 exit the program   
            exit()                              
        response=attempt_login(login_attempt)  # Login failed retry again
        return(-1)                       # Result for the face detected
            

            
# Main function
if __name__ == "__main__":
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    #faces=()
    collectionId='MyCollection'                  # Collection of faces stored
    threshold = 97                               # Confidence level of detection
    maxFaces=1                                   # Maximum number of faces to detect
    login_attempt=1                              # Count for login attempts
    client=boto3.client('rekognition')
    response=attempt_login(login_attempt)
    faceMatches=response['FaceMatches']
    for match in faceMatches:
        match['Face']['ExternalImageId']=match['Face']['ExternalImageId'].split('.')     # Split the image file name
        print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")              # Confidence score
        print('ExternalImageId:', match['Face']['ExternalImageId'][0])                   # Name of the image
        print('Face ID: ',match['Face']['FaceId'])                                       # Unique faceID
        os.remove("screenshot.jpg")                                                      # Removing the saved snapshot of the user
        

