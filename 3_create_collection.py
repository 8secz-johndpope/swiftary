# Import the SDK
import boto3
from botocore.exceptions import ClientError
import uuid

rekclient = boto3.client('rekognition','eu-west-1')
collection_name = 'swiftarycelebrity'

#
# List all images in the bucket
#

#collection_exists_waiter = rekclient.get_waiter('collection_exists')

response = rekclient.create_collection(
    CollectionId='collection_name'
)

#collection_exists_waiter.wait(Collection=collection_name)

