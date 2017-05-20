import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import js
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

def lambda_handler(event, context):
    
    TableName = event['TableName']
    FaceId     = event['FaceId']
    
    print ('FetchFaceDetails')
    ScannedFacesTable = dbresource.Table(TableName)
    print ('FaceId %s' % FaceId )

    ScannedFaces = ScannedFacesTable.query( 
         KeyConditionExpression=Key('FaceId').eq(FaceId)
    )

    for Images in ScannedFaces ['Items']:
      print ('Celebrity Match %s %s' % (Images ['FirstName'] ,  Images ['SurName']))
    
    response = {
                "FaceId" : Images ['FaceId'],
                "FirstName" : Images ['FirstName'],
                "SurName" : Images ['SurName'],
                "ExternalImageId" : Images ['ExternalImageId'],
                "Info" : Images ['Info']
    }
    
    #return response
    return response
