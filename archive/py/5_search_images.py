# Import the SDK
import boto3
from boto3.dynamodb.conditions import Key
import uuid
s3client = boto3.client('s3','eu-west-1')
s3resource = boto3.resource('s3','eu-west-1')
rekclient = boto3.client('rekognition','eu-west-1')
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')
bucket_name = 'swiftarycelebritytemp'
collection_name = 'swiftarycelebrity'

bucket = s3resource.Bucket(bucket_name)
ScannedFacesTable = dbresource.Table('ScannedFaces')

#s3_object_exists_waiter= s3client.get_waiter('object_exists')

#
# List all images in the bucket
#

response = s3client.list_objects(
    Bucket=bucket_name,
    Delimiter=','
)

contents =response ['Contents']

for Images in contents:
    imagefile= Images ['Key']
    response = rekclient.search_faces_by_image(
              CollectionId=collection_name,
              Image={
                  'S3Object': {
                      'Bucket': bucket_name,
                      'Name': imagefile,
                  }
              },
          )
    #print ('FaceId %s' % response ['FaceMatches'][0]['Face']['FaceId'])
    #print ('ExternalImageId %s' % response ['FaceMatches'][0]['Face']['ExternalImageId'])
    #print ('Confidence %s' % response ['FaceMatches'][0]['Face']['Confidence'])
    #print ('ImageId %s' % response ['FaceMatches'][0]['Face']['ImageId'])
    #print ('FaceId %s' % response ['FaceMatches'][0]['Face']['FaceId'])
    #ImageId         = Images ['ImageId']
    #ExternalImageId = Images ['ExternalImageId']

    FaceId          = response ['FaceMatches'][0]['Face']['FaceId']
    ScannedFaces = ScannedFacesTable.query( KeyConditionExpression=Key('FaceId').eq(FaceId))
    for Images in ScannedFaces ['Items']:
      print ('ExternalImageId %s' % Images ['ExternalImageId'])

 

#
