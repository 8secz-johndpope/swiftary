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
    #celebrity_match = return_celebrity_match('ScannedFaces',FaceId)
    #print ('FaceId %s' % FaceId )
    #ScannedFaces = ScannedFacesTable.query( 
    #     KeyConditionExpression=Key('FaceId').eq(FaceId)
    #)
    #for Images in ScannedFaces ['Items']:
    #  print ('Celebrity Match %s %s' % (Images ['FirstName'] ,  Images ['SurName']))
    #return response
    MatchDetails = { "TableName": "ScannedFaces", "FaceId": "68eb0884-5969-5ead-9d48-f3974fa64aa3" }
    invoke_response = lambda_client.invoke(FunctionName="FetchFaceDetails",
                                            InvocationType='RequestResponse',
                                            Payload=json.dumps(MatchDetails))
    FaceMatchResults = json.loads(invoke_response['Payload'].read())
    FirstName   = FaceMatchResults['FirstName']
    print (' FirstName %s ' % FirstName)
    SurName     = FaceMatchResults['SurName']
    FaceId      = FaceMatchResults['FaceId']
    print ('Celebrity Match %s %s' % ( FirstName ,  SurName))
    #def return_celebrity_match(table_name,FaceId):
    #print ('return_celebrity_match')
    #ScannedFacesTable = dbresource.Table(table_name)
    #print ('FaceId %s' % FaceId )
    #ScannedFaces = ScannedFacesTable.query( 
    #KeyConditionExpression=Key('FaceId').eq(FaceId)
    #)

    #for Images in ScannedFaces ['Items']:
    #print ('Celebrity Match %s %s' % (Images ['FirstName'] ,  Images ['SurName']))

    #return response

def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    #table = boto3.resource('dynamodb').Table('MyTable')
    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    #table.put_item(Item={'PK': key, 'Labels': labels})
    return response


def index_faces(bucket, key):
    # Note: Collection has to be created upfront. Use CreateCollection API to create a collecion.
    #rekognition.create_collection(CollectionId='BLUEPRINT_COLLECTION')
    response = rekognition.index_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}}, CollectionId="BLUEPRINT_COLLECTION")
    return response


# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    #print("Received event: " + json.dumps(event, indent=2))
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        # Calls rekognition DetectFaces API to detect faces in S3 object
        response = search_faces(bucket, key)

        # Calls rekognition DetectLabels API to detect labels in S3 object
        #response = detect_labels(bucket, key)

        # Calls rekognition IndexFaces API to detect faces in S3 object and index faces into specified collection
        #response = index_faces(bucket, key)

        # Print response to console.
    #    print(response)

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e

