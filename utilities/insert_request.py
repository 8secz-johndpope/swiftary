import json
import boto3
from botocore.exceptions import ClientError
import uuid
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')
ScannedFacestable = dbresource.Table('FaceRequest')

#
# List all images in the bucket
#

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


