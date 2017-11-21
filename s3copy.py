#!/usr/local/bin/python3
'''
S3 Copy
'''
import sys
import os
import json
import boto3

'''
need env variable below pointing to credentials
running get-token.py stores AWS credentials in below location
'''
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'
# uses saml profile to authenticate to AWS from above file
session = boto3.Session(profile_name='saml')
boto3.setup_default_session(profile_name='saml')

dest_bucket_name = ''
kms_key = ''
file_key = sys.argv[1]
dest_bucket_region = 'us-gov-west-1'

client = boto3.client('s3', dest_bucket_region)
response = client.put_object(
    Bucket=dest_bucket_name,
    Key=file_key,
    ServerSideEncryption='aws:kms',
    StorageClass='STANDARD',
    SSEKMSKeyId=kms_key
    )