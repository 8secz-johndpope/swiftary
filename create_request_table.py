# Import the SDK
import boto3
from botocore.exceptions import ClientError
import uuid

dbclient   = boto3.client('dynamodb','eu-west-1')
dbresource = boto3.resource('dynamodb', region_name='eu-west-1')

response = dbclient.create_table(
    TableName='FaceRequest',
    KeySchema=[
        {
            'AttributeName': 'UserId',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'RequestId',
            'KeyType': 'RANGE'
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'UserId',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'RequestId',
            'AttributeType': 'S'
        },
    ],
ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    },
)
