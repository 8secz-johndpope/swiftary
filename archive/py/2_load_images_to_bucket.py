# Import the SDK
import boto3
import os
from botocore.exceptions import ClientError
import uuid

s3client = boto3.client('s3')
s3resource = boto3.resource('s3','eu-west-1')
bucket_name = 'swiftarycelebrity'

print ('Loading images into bucket %s' %bucket_name )

bucket = s3resource.Bucket(bucket_name)

s3_object_exists_waiter= s3client.get_waiter('object_exists')

for imagefile in os.listdir('../images'):
       print (imagefile)
       s3resource.Object(bucket_name, imagefile).upload_file('../images/%s' %imagefile)
       s3_object_exists_waiter.wait(Bucket=bucket_name, Key=imagefile)

