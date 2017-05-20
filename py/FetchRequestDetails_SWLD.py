import boto3
from boto3.dynamodb.conditions import Key

dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

def lambda_handler(event, context):
  print ('FetchRequestDetails')
  lv_UserId    = event['UserId']
  lv_RequestId = event['RequestId']
      
  lv_TableName = 'FaceRequest'
  FaceRequestTable = dbresource.Table(lv_TableName)
  
  FaceRequests = FaceRequestTable.query(
           KeyConditionExpression=Key('UserId').eq(lv_UserId) & Key('RequestId').eq(lv_RequestId) 
  )

  for Requests in FaceRequests['Items']:
     lv_UserId           = Requests ['UserId']
     lv_RequestId        = Requests ['RequestId']
     lv_StartDateTime    = Requests ['StartDateTime']
     lv_EndDateTime      = Requests ['EndDateTime']
     lv_FaceId           = Requests ['FaceId']
     lv_Firstname        = Requests ['Firstname']
     lv_SurName          = Requests ['SurName']
     lv_ImageFile        = Requests ['ImageFile']
     lv_ExternalImageId  = Requests ['ExternalImageId']
     lv_Request_Status   = Requests ['Request_Status']
	
    #print ('User request details %s %s %s %s %s %s' % (str(lv_UserId), lv_RequestId, lv_FaceId , lv_StartDateTime , lv_EndDateTime   , lv_Status))
    #print ('User request details %s %s ' % (str(lv_UserId), lv_RequestId))

  response = { "UserId"           : lv_UserId, 
               "RequestId"        : lv_RequestId, 
               "StartDateTime"    : lv_StartDateTime, 
               "EndDateTime"      : lv_EndDateTime, 
               "FaceId"           : lv_FaceId, 
               "Firstname"        : lv_Firstname,
               "SurName"          : lv_SurName,
               "ImageFile"        : lv_ImageFile,
               "ExternalImageId"  : lv_ExternalImageId,
               "Request_Status"   : lv_Request_Status  } 

  return response

