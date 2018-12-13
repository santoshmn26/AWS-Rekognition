import boto3
import sys
if __name__ == "__main__":

    bucket='reko-face'
    collectionId='MyCollection'
    fileName=sys.argv[-1]
    threshold = 70
    maxFaces=2

    client=boto3.client('rekognition')

  
    response=client.search_faces_by_image(CollectionId=collectionId,
                                Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)

                                
    faceMatches=response['FaceMatches']
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            match['Face']['ExternalImageId']=match['Face']['ExternalImageId'].split('.')
            print('ExternalImageId:', match['Face']['ExternalImageId'][0])
            
            

