import boto3
from boto3.dynamodb.conditions import Key

dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

def main(event, context):
  print ('main')
  lv_UserId    = event['UserId']
  lv_RequestId = event['RequestId']
  lv_TableName = 'FaceRequest'
  FaceRequestTable = dbresource.Table(lv_TableName)
  
  FaceRequests = FaceRequestTable.query(
           KeyConditionExpression=Key('UserId').eq(lv_UserId) & Key('RequestId').eq(lv_RequestId) 
  )

  for Requests in FaceRequests['Items']:
    lv_FaceId        = Requests ['FaceId']
    lv_StartDateTime = Requests ['StartDateTime']
    lv_EndDateTime   = Requests ['EndDateTime']
    lv_Status        = Requests ['Request_Status']

    #print ('User request details %s %s %s %s %s %s' % (str(lv_UserId), lv_RequestId, lv_FaceId , lv_StartDateTime , lv_EndDateTime   , lv_Status))
    #print ('User request details %s %s ' % (str(lv_UserId), lv_RequestId))

  response = { "UserId"         : lv_UserId, "RequestId"      : lv_RequestId, "FaceId"         : lv_FaceId, "StartDateTime"  : lv_StartDateTime, "EndDateTime"    : lv_EndDateTime, "Request_Status"         : lv_Status } 

  return response

