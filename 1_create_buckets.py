# Create Bucket change
# Import the SDK
import boto3
from botocore.exceptions import ClientError
import uuid

s3client = boto3.client('s3')
bucket_name = 'swiftarycelebrity'
bucket_name_temp = 'swiftarycelebritytemp'


s3_bucket_exists_waiter = s3client.get_waiter('bucket_exists')
s3client.create_bucket(Bucket=bucket_name,
                       ACL='public-read-write',
                       CreateBucketConfiguration={ 'LocationConstraint': 'eu-west-1' })
s3_bucket_exists_waiter.wait(Bucket=bucket_name)

s3_bucket_exists_waiter = s3client.get_waiter('bucket_exists')
s3client.create_bucket(Bucket=bucket_name_temp,
                       ACL='public-read-write',
                       CreateBucketConfiguration={ 'LocationConstraint': 'eu-west-1' })
s3_bucket_exists_waiter.wait(Bucket=bucket_name_temp)

