# Import the SDK
import boto3
from botocore.exceptions import ClientError
import uuid

s3client = boto3.client('s3')
rekclient = boto3.client('rekognition','eu-west-1')
s3resource = boto3.resource('s3','eu-west-1')
bucket_name = 'swiftarycelebrity'
collection_name = 'swiftarycelebrity'

#
# List all images in the bucket
#

response = s3client.list_objects(
    Bucket=bucket_name,
    Delimiter=','
)

contents =response ['Contents']
for Images in contents:
    ImageName = Images ['Key']
    print ('Image_name %s' % ImageName )
    response = rekclient.index_faces( CollectionId=collection_name,
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': ImageName ,
            },
        },
        ExternalImageId=ImageName,
        DetectionAttributes=[ 'DEFAULT' ]
    )
    print ('FaceID %s' % response ['FaceRecords'][0]['Face']['FaceId'])
    print ('ImageID %s' % response ['FaceRecords'][0]['Face']['ImageId'])
    print ('ExternalImageId %s' % response ['FaceRecords'][0]['Face']['ExternalImageId'])

