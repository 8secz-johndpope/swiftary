import boto3
import time
#from boto3.dynamodb.conditions import Key
#from decimal import Decimal
#import uuid

dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

def lambda_handler(event, context):

    print ('InsertRequest')

    lv_UserId    = event['UserId']
    lv_RequestId = event['RequestId']
    lv_FaceId    = event['FaceId']
    lv_Status    = event['Status']
    
    lv_TableName = 'FaceRequest'
    lv_DateTime  = str(time.strftime("%d%m%y:%H:%M:%S"))

    FaceRequestTable = dbresource.Table(lv_TableName)


    response = FaceRequestTable.update_item(
       Key={
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId
        },
       UpdateExpression="set FaceId = :a, EndDateTime=:b, Status=:c",
         ExpressionAttributeValues={
        ':a': lv_FaceId,
        ':b': lv_DateTime,
        ':c': lv_Status
    },
    ReturnValues="UPDATED_NEW"
    )

    response = {
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId,
        'FaceId'         : lv_FaceId,
        'EndDateTime'    : lv_DateTime,
        'Status'         : lv_Status
        }

    return response

