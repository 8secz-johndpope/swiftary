# Import the SDK
import json
import boto3
from botocore.exceptions import ClientError
import uuid
#dbclient = boto3.client('dynamodb')
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

rekclient = boto3.client('rekognition','eu-west-1')
collection_name = 'swiftarycelebrity'

ScannedFacestable = dbresource.Table('ScannedFaces')

#
# List all images in the bucket
#


response = rekclient.list_faces( CollectionId=collection_name)
Faces =response ['Faces']
#print Faces

for Images in Faces:
    print ('FaceId %s' % Images ['FaceId'])
    print ('ImageId %s' % Images ['ImageId'])
    print ('ExternalImageId %s' % Images ['ExternalImageId'])
    print ('Infor %s' %json.dumps(Images)) 

    FaceId          = Images ['FaceId']
    ImageId         = Images ['ImageId']


    response = ScannedFacestable.put_item(
       Item={
        'FaceId'       : Images ['FaceId'],
        'ImageId'      : Images ['ImageId'],
        'ExternalImageId' : Images ['ExternalImageId'],
        'Info'         : json.dumps(Images)
        }
    )

print("PutItem succeeded:")
#print(json.dumps(response, indent=4, cls=DecimalEncoder))


