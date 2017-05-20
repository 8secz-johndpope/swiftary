# Import the SDK
import json
import boto3
from botocore.exceptions import ClientError
import uuid
#dbclient = boto3.client('dynamodb')
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

rekclient = boto3.client('rekognition','eu-west-1')
collection_name = 'swiftarycelebrity'

ScannedFacestable = dbresource.Table('ScannedFaces')

#
# List all images in the bucket
#


response = rekclient.list_faces( CollectionId=collection_name)
Faces =response ['Faces']
#print Faces

for Images in Faces:
    lv_FaceId          = Images ['FaceId']
    lv_ImageId         = Images ['ImageId']
    lv_ExternalImageId = Images ['ExternalImageId'],
    lv_Names           = ExternalImageId.split("_")
    lv_Firstname       = lv_Names[0]
    lv_Surname         = lv_Names[1]

    print ('FaceId %s' % lv_FaceId)
    print ('ImageId %s' % lv_ImageId)
    print ('ExternalImageId %s' % lv_ExternalImageId)
    print ('Infor %s' %json.dumps(Images)) 
    print ('FirstName %s' % lv_FirstName )
    print ('SurName %s' % lv_SurName )


    #response = ScannedFacestable.put_item(
    #   Item={
    #    'FaceId'          : lv_FaceId,
    #    'ImageId'         : lv_ImageId,
    #    'ExternalImageId' : lv_ExternalImageId,
    #    'Firstname'       : lv_Firstname,
    #    'Surname'         : lv_Surname  ,
    #    'Info'            : json.dumps(Images)
    #    }
    #)

print("PutItem succeeded:")
#print(json.dumps(response, indent=4, cls=DecimalEncoder))


