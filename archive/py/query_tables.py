#
# Whoyou
# File:    query_tables
# Version 1.0
# Date 25 April 2017
# Description
#
#
#from __future__ import print_function
#
#import boto3
#from boto3.dynamodb.conditions import Key
#from decimal import Decimal
#import json
#import urllib
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

def return_celebrity_match(table_name,FaceId):
    print ('return_celebrity_match')
    ScannedFacesTable = dbresource.Table(table_name)
    print ('FaceId %s' % FaceId )

    ScannedFaces = ScannedFacesTable.query( 
         KeyConditionExpression=Key('FaceId').eq(FaceId)
    )

    for Images in ScannedFaces ['Items']:
      print ('Celebrity Match %s %s' % (Images ['FirstName'] ,  Images ['SurName']))

    #return response

