import json
import boto3
from boto3.dynamodb.conditions import Key
import uuid
    #ExpressionAttributeValues={':FaceId': '80309e82-015b-5df3-a34c-db59bd131c63'}

dbresource = boto3.resource('dynamodb', region_name='eu-west-1')
ScannedFacesTable = dbresource.Table('ScannedFaces')
ScannedFaces = ScannedFacesTable.query( 
    KeyConditionExpression=Key('FaceId').eq('80309e82-015b-5df3-a34c-db59bd131c63')
)

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


