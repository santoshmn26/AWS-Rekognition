import boto3
import sys
import cv2
import os

# =============================================================================================================
# Capture face using Open CV and Webcam

if __name__ == "__main__":
    name=input('Enter Name: ')
    capture=cv2.VideoCapture(0)
    while(capture.isOpened()):
        ret, frame = capture.read()
        if ret:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite(name+".jpg",frame)
                break
        else:
            capture.release()
            cv2.destroyAllWindows()
            break

    # =========================================================================================================
    # Upload the new face to Amazon S3 storage
    
    s3 = boto3.client('s3')
    bucket = 'reko-face'
    file_name = name+".jpg"             
    photo = name+".jpg"              
    s3.upload_file(file_name, bucket, photo)
    
    # =========================================================================================================
    # Add new face to collection
    
    collectionId='MyCollection'   
    client=boto3.client('rekognition')
    response=client.index_faces
    response=client.index_faces(CollectionId=collectionId,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])
                                
    # =========================================================================================================
    # Details about the new added face
    
    print ('Results for ' + photo) 	
    print('Faces indexed:')						
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
            
# =============================================================================================================
# Remove the temp file create to upload
os.remove(name+".jpg")