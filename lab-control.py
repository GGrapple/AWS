#!/usr/bin/python
'''
Turn Core IRAD LAB equipment on and off
Usage lab-control.py [off|on]
'''
import sys
import os
import json
import boto3
from botocore.exceptions import ClientError

'''
need env variable below pointing to credentials
running get-token.py stores AWS credentials in below location
'''
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'
# uses saml profile to authenticate to AWS from above file
session = boto3.Session(profile_name='saml')
boto3.setup_default_session(profile_name='saml')
'''Core EC2 instance-id list'''
core_ids = ['i-0d31011b5a8ed713d', 'i-02c5e64af10a072fa', 'i-04c89ae97927a44a3', 'i-03ed974ba98ae0aec',
            'i-0ab6eacb8c2750952', 'i-03127918b624fc28b']
'''this is for EC2 stuff  there are other calls needed for S3 etc...'''
ec2 = boto3.client('ec2')
action = sys.argv[1].upper()
if action == 'ON':
    for id in core_ids:
        try:
            ec2.start_instances(InstanceIds=[id], DryRun=True)
        # print('On '+id)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        try:
            response = ec2.start_instances(InstanceIds=[id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
elif action == 'OFF':
    for id in core_ids:
        try:
            ec2.start_instances(InstanceIds=[id], DryRun=True)
            print('Off ' + id)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        try:
            response = ec2.stop_instances(InstanceIds=[id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
elif action == 'STATUS':
    for id in core_ids:
        instance_status = ec2.describe_instance_status(InstanceIds=[id])
        print(instance_status)
else:
    print('Error must use on or off')
