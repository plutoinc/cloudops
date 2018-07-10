import boto3
import logging
import json
import jmespath

from botocore.exceptions import ClientError

log = logging.getLogger()


REGIONS = [
    "us-east-1",
    # "us-east-2",
    # "us-west-1",
    # "us-west-2",
    # "ca-central-1",
    # "eu-west-1",
    # "eu-central-1",
    # "eu-west-2",
    # "ap-northeast-1",
    # "ap-northeast-2"
    # "ap-southeast-1",
    # "ap-southeast-2",
    # "ap-south-1",
    # "sa-east-1"
]


def ec2_instance(instance_id, regions=None):
    # aws ec2 describe-instances --output=json --query='Reservations[*].Instances[].{id:InstanceId, tags:Tags} '
    regions = regions or REGIONS
    for region in regions:
        log.info(">> %s" % region)
        ec2 = boto3.resource('ec2', region_name=region)
        instance = ec2.Instance(instance_id)
        try:
            if instance.tags:
                return instance
        except ClientError as e:
            pass

    return None


def ec2_instances_by_regions(filters=None, regions=None):
    # aws ec2 describe-instances --output=json --query='Reservations[*].Instances[].{id:InstanceId, tags:Tags} '
    regions = regions or boto3.session.Session().get_available_regions('ec2')
    instances = {}
    for region in regions:
        print 'Checking region:', region
        instances.update({region: [i for i in boto3.resource('ec2', region_name=region).instances.all()]})

    return instances


