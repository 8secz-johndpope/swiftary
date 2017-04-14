# Import the SDK
import boto3
from botocore.exceptions import ClientError
import uuid

rekclient = boto3.client('rekognition','eu-west-1')
collection_name = 'swiftarycelebrity'

#
# List all images in the bucket
#


response = rekclient.list_faces( CollectionId=collection_name)
Faces =response ['Faces']
print Faces

for Images in Faces:
    print ('FaceId %s' % Images ['FaceId'])
    print ('ImageId %s' % Images ['ImageId'])
    print ('ExternalImageId %s' % Images ['ExternalImageId'])



       

