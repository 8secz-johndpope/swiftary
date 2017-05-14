import boto3
import time
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import uuid

dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

def lambda_handler(event, context):

    print ('InsertRequest')

    lv_UserId    = event['UserId']
    
    lv_TableName = 'FaceRequest'
    lv_RequestId = str(uuid.uuid4())
    lv_DateTime  = str(time.strftime("%d%m%y:%H:%M:%S"))
    lv_ImageFile = '%s_%s_%s.jpg' %(str(lv_UserId), lv_RequestId, lv_DateTime)
    lv_Status    = 'Started'

    print ('lv_ImageFile %s ' %(lv_ImageFile ))

    FaceRequestTable = dbresource.Table(lv_TableName)


    response = FaceRequestTable.put_item(
       Item={
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId,
        'ImageFile'      : lv_ImageFile,
        'StartDateTime'  : lv_DateTime,
        'Status'         : lv_Status
        }
    )

    response = {
        'UserId'         : lv_UserId,
        'RequestId'      : lv_RequestId,
        'ImageFile'      : lv_ImageFile,
        'StartDateTime'  : lv_DateTime
        }

    return response

