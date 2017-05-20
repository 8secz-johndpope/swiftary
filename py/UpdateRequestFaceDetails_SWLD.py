import boto3
import time
#from boto3.dynamodb.conditions import Key
#from decimal import Decimal
#import uuid

dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

def lambda_handler(event, context):

    print ('UpdateRequestFaceDetails')

    lv_UserId    = event['UserId']
    lv_RequestId = event['RequestId']
    lv_FirstName = event['FirstName']
    lv_SurName   = event['SurName']
    lv_DOB       = event['DOB']
    lv_Status    = event['Status']
    
    lv_TableName = 'FaceRequest'
    lv_DateTime  = str(time.strftime("%d%m%y:%H:%M:%S"))

    FaceRequestTable = dbresource.Table(lv_TableName)


    response = FaceRequestTable.update_item(
       Key={
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId
        },
       UpdateExpression="set FirstName = :a, SurName = :b, DOB = :c, EndDateTime=:d, Request_Status=:e",
         ExpressionAttributeValues={
        ':a': lv_FirstName,
        ':b': lv_SurName,
        ':c': lv_DOB,
        ':d': lv_DateTime,
        ':e': lv_Status
    },
    ReturnValues="UPDATED_NEW"
    )

    response = {
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId,
        'FirstName'      : lv_FirstName,
        'SurName'        : lv_SurName,
        'DOB'             : lv_DOB,
        'EndDateTime'    : lv_DateTime,
        'Status'         : lv_Status
        }

    return response

