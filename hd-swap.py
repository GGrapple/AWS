#!/usr/bin/python
#test change for git commit
'''
boto3 is used as the interface to aws instead of the CLI version aws
need to add functions and store info from for loop posibly so can retreive it later?
'''
import sys
import os
import json
import boto3

'''
need env variable below pointing to credentials
running get-token.py stores AWS credentials in below location
'''
os.environ[
    'AWS_SHARED_CREDENTIALS_FILE'] = '~/.aws/credentials'  # uses saml profile to authenticate to AWS from above file
session = boto3.Session(profile_name='saml')
'''stuff I was doing before I moved to boto3, was based on aws cli'''
# aws = 'aws --profile saml'
# instance_table = 'ec2 describe-instances --query "Reservations[*].Instances[*].{ID:InstanceId,Pub:PublicIpAddress,Priv:PrivateIpAddress,State:State.Name,Name:Tags[?Key==`Name`] | [0].Value}" --output table --color off'
# describe_instances = 'aws --profile saml ec2 describe-instances --instance-ids i-06281b37da23f9714'
# cmd = os.system(aws+' '+describe_instances)
'''was trying to parse json message as first'''
# data = json.loads(cmd)
# print(my_json_dict)
# a_instances = my_json_dict['Instances']
# print(data)
'''this is for EC2 stuff  there are other calls needed for S3 etc...'''
ec2 = session.resource('ec2')
instance = ec2.Instance('id')
'''
this for loop looks for a host and displays information needed, have to run multiple loops
 for some reason to get all the data I wanted. There should be a better way to do all this
 '''
var_target = sys.argv[1]
# print(var_target)
ec2_target = {}
for instance in ec2.instances.all():
    for tag in instance.tags:
        if tag['Value'] == var_target:  # add variable instead of guac, used to specify instance
            # if tag['Key'] == 'Name': #pulls all instances with a name
            for bdm in instance.block_device_mappings:
                ec2_target = (
                tag['Value'], instance.id, instance.state['Name'], bdm['DeviceName'], bdm['Ebs']['VolumeId'])
                # print('Name[0], Istance ID[1], State[2], EBS Volume[3], Volume ID[4]')
                # print(ec2_target)
                # print(tag['Value'],instance.id,instance.state['Name'],bdm['DeviceName'],bdm['Ebs']['VolumeId'])
                # for bdm in instance.block_device_mappings:
                # print(bdm['Ebs']['VolumeId'])
                # if bdm[''] == 'DeviceName':
                # print(bdm['Value'])
print(ec2_target[4])
old_vol = ec2_target[4]
instance_id = ec2_target[1]
for volume in ec2.volumes.all():
    '''handels problem with no tags'''
    if volume.tags is None:
        # print(volume.id)
        continue
    for tag in volume.tags:
        # if tag['Key'] == 'Name': #see above
        if tag['Value'] == 'hd-dan-test-2-dev':
            new_vol = volume.id
            print(new_vol, tag['Value'])
# Remove old disk
ec2.Instance(instance_id).detach_volume(VolumeId=old_vol)
# Attach new disk
ec2.Instance(instance_id).attach_volume(VolumeId=new_vol, Device='/dev/sda1')
'''put in thing after this to swap the Tag Names? Should also track which one was the original, maybe add another tag?'''
