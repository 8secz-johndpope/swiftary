#
# Whoyou
# Function:    Main 
# Version 1.0
# Date 25 April 2017
# Description Main procedure for Lambda calls
#
#
from __future__ import print_function
import boto3
from decimal import Decimal
import json
import urllib

lv_bucket_temp_name = 'swiftarycelebritytemp'
lv_bucket_match_name = 'swiftarycelebritymatch'
lv_region     = 'eu-west-1'
lv_Local_ImageFile = 'matt_damon3.jpg'

lambda_client = boto3.client('lambda')
s3_client     = boto3.client('s3')
s3resource = boto3.resource('s3',lv_region)

def Main():

#
# Insert request record
#
    UserId          = 123456
    InsertRequest_Details = { "UserId": UserId}
    InsertRequest_Response = lambda_client.invoke(FunctionName="InsertRequest_SWLD",
                                           InvocationType='RequestResponse',
                                           Payload=json.dumps(InsertRequest_Details))

    InsertRequest_Results = json.loads(InsertRequest_Response['Payload'].read())

    lv_UserId        = InsertRequest_Results['UserId']
    lv_RequestId     = InsertRequest_Results['RequestId']
    lv_ImageFile     = InsertRequest_Results['ImageFile']
    lv_StartDateTime = InsertRequest_Results['StartDateTime']

    print ('Inserted Request Record %s %s %s %s' % (str(lv_UserId),lv_RequestId,lv_ImageFile,lv_StartDateTime))

#
# Upload the file to S3
#
    print ('Loading image into bucket %s' %lv_bucket_temp_name )
    s3_object_exists_waiter= s3_client.get_waiter('object_exists')
    s3resource.Object(lv_bucket_temp_name, lv_ImageFile).upload_file('../imagestemp/%s' %lv_Local_ImageFile)
    s3_object_exists_waiter.wait(Bucket=lv_bucket_temp_name, Key=lv_ImageFile)
    
#
# Update request record
#
    lv_Status = 'ImageUploaded'

    InsertRequest_Details = { 
          "UserId"    : lv_UserId, 
          "RequestId" : lv_RequestId,
          "FaceId"    :    "",
          "Status"    :    lv_Status
          }

    InsertRequest_Response = lambda_client.invoke(FunctionName="UpdateRequest_SWLD",
                                           InvocationType='RequestResponse',
                                           Payload=json.dumps(InsertRequest_Details))

    InsertRequest_Results = json.loads(InsertRequest_Response['Payload'].read())

    print ('Updated Request record ')

#
# wait for match file in s3
#
    print ('Waiting for image in bucket %s' %lv_bucket_match_name )
    s3_object_exists_waiter= s3_client.get_waiter('object_exists')
    s3_object_exists_waiter.wait(Bucket=lv_bucket_match_name, Key=lv_ImageFile)
    
#
# Fetch request details
#

    lv_FetchRequestDetails = { 
          "UserId"    : lv_UserId, 
          "RequestId" : lv_RequestId
          }

    lv_FetchRequestResponse = lambda_client.invoke(FunctionName="FetchRequestDetails_SWLD",
                                           InvocationType='RequestResponse',
                                           Payload=json.dumps(lv_FetchRequestDetails))

    lv_FetchtRequestResults = json.loads(lv_FetchRequestResponse['Payload'].read())

    lv_UserId           = lv_FetchtRequestResults['UserId']
    lv_RequestId        = lv_FetchtRequestResults['RequestId']
    lv_StartDateTime    = lv_FetchtRequestResults['StartDateTime']
    lv_EndDateTime      = lv_FetchtRequestResults['EndDateTime']
    lv_FaceId           = lv_FetchtRequestResults['FaceId']
    lv_Firstname        = lv_FetchtRequestResults['Firstname']
    lv_SurName          = lv_FetchtRequestResults['SurName']
    lv_ImageFile        = lv_FetchtRequestResults['ImageFile']
    lv_ExternalImageId  = lv_FetchtRequestResults['ExternalImageId']
    lv_Request_Status   = lv_FetchtRequestResults['Request_Status']
    lv_MatchedFaceUrl   = lv_FetchtRequestResults['MatchedFaceUrl']

    print ('Request Deatils %s %s %s %s %s %s %s %s %s %s %s ' %(
    lv_UserId           ,
    lv_RequestId        ,
    lv_StartDateTime    ,
    lv_EndDateTime      ,
    lv_FaceId           ,
    lv_Firstname        ,
    lv_SurName          ,
    lv_ImageFile        ,
    lv_ExternalImageId  ,
    lv_MatchedFaceUrl  ,
    lv_Request_Status   ))
#
# Update request record
#
    response = {
         'UserId'        : lv_UserId,
         'RequestId'     : lv_RequestId,
         'ImageFile'     : lv_ImageFile,
         'StartDateTime' : lv_StartDateTime
        }
    return response 

#
# Functions performed by Lambda trigger on s3.
# Poll for response onrecords update to Matched or Unmatched.
# Return record
#
Main ()
