import boto3
import time
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import uuid

dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

def main(event, context):

    print ('InsertRequest')

    lv_UserId    = event['UserId']
    lv_ImageFile = event['ImageFile']
    
    lv_TableName = 'FaceRequest'
    lv_RequestId = str(uuid.uuid4())
    lv_DateTime  = str(time.strftime("%c"))

    FaceRequestTable = dbresource.Table(lv_TableName)


    response = FaceRequestTable.put_item(
       Item={
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId,
        'ImageFile'      : lv_ImageFile,
        'StartDateTime'  : lv_DateTime
        }
    )

    response = {
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId,
        'ImageFile'      : lv_ImageFile,
        'StartDateTime'  : lv_DateTime
        }

    return response

