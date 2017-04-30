#
# Whoyou
# Function:    s3faceupload
# Version 1.0
# Date 25 April 2017
# Description
#
#
from __future__ import print_function

import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import json
import urllib
lambda_client = boto3.client('lambda')

print('Loading function')
rekognition = boto3.client('rekognition', region_name='eu-west-1')
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')


# --------------- Helper Functions to call Rekognition APIs ------------------


def search_faces(bucket_name, imagefile):
    ScannedFacesTable = dbresource.Table('ScannedFaces')
    collection_name = 'swiftarycelebrity'
    response = rekognition.search_faces_by_image(
              CollectionId=collection_name,
              Image={
                  'S3Object': {
                      'Bucket': bucket_name,
                      'Name': imagefile,
                  }
              },
          )
    print ('FaceId %s' % response ['FaceMatches'][0]['Face']['FaceId'])
    print ('ExternalImageId %s' % response ['FaceMatches'][0]['Face']['ExternalImageId'])
    print ('Confidence %s' % response ['FaceMatches'][0]['Face']['Confidence'])
    print ('ImageId %s' % response ['FaceMatches'][0]['Face']['ImageId'])
    FaceId          = response ['FaceMatches'][0]['Face']['FaceId']
    MatchDetails = { "TableName": "ScannedFaces", "FaceId": "68eb0884-5969-5ead-9d48-f3974fa64aa3" }
    invoke_response = lambda_client.invoke(FunctionName="FetchFaceDetails",
                                            InvocationType='RequestResponse',
                                            Payload=json.dumps(MatchDetails))
    FaceMatchResults = json.loads(invoke_response['Payload'].read())
    lv_FirstName   = FaceMatchResults['FirstName']
    lv_SurName     = FaceMatchResults['SurName']
    lv_FaceId      = FaceMatchResults['FaceId']
    # Return filename of Celeb
    # Include in table update

    print ('Celebrity Match %s %s' % ( lv_FirstName ,  lv_SurName))

    return response = {
        'FaceId'         : lv_FaceId,
        'FirstName'      : lv_FirstName,
        'SurName'        : lv_SurName
        }



# --------------- Main handler ------------------


def lambda_handler(event, context):
    # S3 trigger Rekognition APIs to detect faces, labels and index faces in S3 Object.
    # print("Received event: " + json.dumps(event, indent=2))
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    faceFile = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:

        #
        # Extract UserId and RequestId from File name
        #

        # Calls rekognition DetectFaces API to detect faces in S3 object
        response = search_faces(bucket, faceFile)

        #
        # Added step number to Request table and include in update function
        # Return filename of Celeb
        # Include in table update
        # Update Request with matching face details
        # lambda_client.invoke(FunctionName="UpdateRequestDetails", -- See above


        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(faceFile, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e

