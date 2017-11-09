#!/usr/bin/python
'''
Tagging
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
'''stuff I was doing before I moved to boto3, was based on aws cli'''
# aws = 'aws --profile saml'
# aws --profile saml ec2 create-tags --resources i-03127918b624fc28b --tags 'Key=Name,Value=netmaster'
'''this is for EC2 stuff  there are other calls needed for S3 etc...'''
ec2 = boto3.resource('ec2')
'''
this for loop looks for a host and displays information needed, have to run multiple loops
 for some reason to get all the data I wanted. There should be a better way to do all this
 '''
for instance in ec2.instances.all():
    # for id in instance.id:
    print(instance.id)
    #	ec2.create_tags(Resources=[instance.id], Tags=[{'Key':'ExcludeDays', 'Value':'Saturday;Sunday'}])
