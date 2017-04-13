# Import the SDK
import boto3
from botocore.exceptions import ClientError
import uuid

dbclient   = boto3.client('dynamodb','eu-west-1')
#dbresource = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://localhost:8000")
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')


response = dbclient.create_table(
    TableName='ScannedFaces',
    KeySchema=[
        {
            'AttributeName': 'FaceID',
            'KeyType': 'HASH'
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'FaceID',
            'AttributeType': 'N'
        },
    ],
ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    },
)
