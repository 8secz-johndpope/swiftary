import boto3
import time
import json
import urllib
from boto3.dynamodb.conditions import Key
#from decimal import Decimal
#import uuid

lv_bucket_celebrity_name = 'swiftarycelebrity'
lv_bucket_match_name = 'swiftarycelebritymatch'
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')
rekognition = boto3.client('rekognition',region_name='eu-west-1')
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')
ScannedFacesTable = dbresource.Table('ScannedFaces')
FaceRequestTable = dbresource.Table('FaceRequest')
s3_client     = boto3.client('s3')

def lambda_handler(event, context):
    print ('MatchFace')
    print("Received event: " + json.dumps(event, indent=2))

    # Retrieve bucket and file details
    lv_Bucket = event['Records'][0]['s3']['bucket']['name']
    lv_ImageFile = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    lv_FileDetails  = lv_ImageFile.split("_")
    lv_UserId       = int(lv_FileDetails[0])
    lv_RequestId    = lv_FileDetails[1]  
    lv_Collection = 'swiftarycelebrity'
    lv_DateTime  = str(time.strftime("%d%m%y:%H:%M:%S"))

    print ('lv_UserId lv_RequestId    %s %s' % (lv_UserId,lv_RequestId))

    # Search faces in collection

    response = rekognition.search_faces_by_image(CollectionId=lv_Collection,Image={'S3Object': {'Bucket': lv_Bucket,'Name': lv_ImageFile,}},)
    lv_FaceId       = response ['FaceMatches'][0]['Face']['FaceId']
    lv_Status       = "Matched" 

    # Search for face in faces table

    ScannedFaces = ScannedFacesTable.query( KeyConditionExpression=Key('FaceId').eq(lv_FaceId))

    for Images in ScannedFaces ['Items']:
         lv_ExternalImageId = Images ['ExternalImageId']
         lv_FirstName       = Images ['FirstName']
         lv_SurName         = Images ['SurName']
         print ('Match Details %s %s %s' % (lv_FirstName,lv_SurName,lv_ExternalImageId))

         lv_MatchedFaceUrl = s3_client.generate_presigned_url( ClientMethod='get_object',
                                       Params={ 'Bucket': lv_bucket_celebrity_name,
                                                'Key': lv_ExternalImageId })

    #FaceRequest= FaceRequestTable.query( KeyConditionExpression=Key('RequestId').eq(lv_RequestId))

    response = FaceRequestTable.update_item(
       Key={
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId
        },
       UpdateExpression="set FaceId = :a, EndDateTime=:b, ExternalImageId=:c, Firstname=:d, SurName=:e,Request_Status=:f, MatchedFaceUrl=:g",
         ExpressionAttributeValues={
        ':a': lv_FaceId,
        ':b': lv_DateTime,
        ':c': lv_ExternalImageId ,
        ':d': lv_FirstName      ,
        ':e': lv_SurName         ,
        ':f': lv_Status         ,
        ':g': lv_MatchedFaceUrl 
    },
    ReturnValues="UPDATED_NEW"
    )

# Move file to Matched Directory

    lv_CopySource= "%s/%s" % (lv_Bucket,lv_ImageFile)
    s3_client.copy_object(Bucket=lv_bucket_match_name, CopySource=lv_CopySource ,Key=lv_ImageFile)
    s3_client.delete_object(Bucket=lv_Bucket, Key=lv_ImageFile)

    response = {
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId,
        'FaceId'         : lv_FaceId,
        'EndDateTime'    : lv_DateTime,
        'Status'         : lv_Status
        }

    return response

