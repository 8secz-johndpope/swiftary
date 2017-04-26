#
# Whoyou
# Function:    FaceMatch
# Version 1.0
# Date 25 April 2017
# Description
#
#

from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib
from boto3.dynamodb.conditions import Key

print('Loading function')

rekognition = boto3.client('rekognition')


# --------------- Helper Functions to call Rekognition APIs ------------------


def Match_faces(bucket_name, imagefile):
# Match_faces
    collection_name = 'swiftarycelebrity'
    response = rekognition.search_faces_by_image(CollectionId=collection_name,Image={'S3Object': {'Bucket': bucket_name,'Name': imagefile,}},)
    return response

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
    dbresource = boto3.resource('dynamodb', region_name='eu-west-1')
    ScannedFacesTable = dbresource.Table('ScannedFaces')
    try:
        # Calls rekognition DetectFaces API to detect faces in S3 object
#        response = detect_faces(bucket, key)
        response = Match_faces(bucket, key)
        FaceId          = response ['FaceMatches'][0]['Face']['FaceId']
        ScannedFaces = ScannedFacesTable.query( KeyConditionExpression=Key('FaceId').eq(FaceId))
        for Images in ScannedFaces ['Items']:
          print ('ExternalImageId %s' % Images ['ExternalImageId'])

        # Calls rekognition DetectLabels API to detect labels in S3 object
        #response = detect_labels(bucket, key)

        # Calls rekognition IndexFaces API to detect faces in S3 object and index faces into specified collection
        #response = index_faces(bucket, key)

        # Print response to console.
        print(response)

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e

