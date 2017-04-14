import json
import boto3
from botocore.exceptions import ClientError
import uuid
dbclient = boto3.client('dynamodb')

dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

ScannedFacesTable = dbresource.Table('ScannedFaces')

ScannedFaces = dbclient.scan(TableName='ScannedFaces')

#
# List all image records in table
#

for Images in ScannedFaces ['Items']:
    print ('FaceId %s' % Images ['FaceId'])
    print ('ImageId %s' % Images ['ImageId'])
    print ('ExternalImageId %s' % Images ['ExternalImageId'])
    print ('Infor %s' %json.dumps(Images)) 

    FaceId          = Images ['FaceId']
    ImageId         = Images ['ImageId']
    ExternalImageId = Images ['ExternalImageId']

    #ScannedFacesTable.update_item(Key={'FaceId':FaceId}, UpdateExpression="SET Name = Name" )

    #response = ScannedFacestable.put_item(
       #Item={
        #'FaceId'       : Images ['FaceId'],
        #'ImageId'      : Images ['ImageId'],
        #'ExternalImageId' : Images ['ExternalImageId'],
        #'Info'         : json.dumps(Images)
        #}
    #)

print("PutItem succeeded:")


