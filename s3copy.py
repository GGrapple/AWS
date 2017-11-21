#!/usr/local/bin/python3
'''
S3 Copy
'''
import sys
import os
import json
import boto3
import configparser

'''
Setup Parser
'''
Config = configparser.ConfigParser()
Config.read('keys.ini')
Config.sections()
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

'''
need env variable below pointing to credentials
running get-token.py stores AWS credentials in below location
'''
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'
# uses saml profile to authenticate to AWS from above file
session = boto3.Session(profile_name='saml')
boto3.setup_default_session(profile_name='saml')

dest_bucket_name = ConfigSectionMap('Bucket')['bucket_name']
kms_key = ConfigSectionMap('Keys')['kms_id']
file_key = sys.argv[1]
dest_bucket_region = 'us-gov-west-1'

client = boto3.client('s3', dest_bucket_region)

response = client.upload_file(
    file_key,
    dest_bucket_name,
    file_key,
    ExtraArgs={
        'ServerSideEncryption':'aws:kms',
        'SSEKMSKeyId':kms_key
        }
    )

