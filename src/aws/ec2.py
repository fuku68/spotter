import boto3

from src.core.config import settings

def list():
    ec2 = boto3.resource('ec2',  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.REGION_NAME)
    instance_list = ec2.instances.filter()

    print(instance_list)
    return instance_list


def spot_request_list():
    client = boto3.client('ec2',  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.REGION_NAME)
    request = client.describe_spot_instance_requests()
    return request['SpotInstanceRequests']


def create_spot_instance(instance_type: str, user: str = ''):
    client = boto3.client('ec2',  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.REGION_NAME)
    request = client.request_spot_instances(
        # SpotPrice="0.03",
        InstanceCount=1,
        LaunchSpecification={
            "ImageId": 'ami-03a4d325b17d64671',
            "InstanceType": instance_type,
        },
        TagSpecifications=[{
            "ResourceType": "spot-instances-request",
            "Tags": [
                {
                    "Key": "created_by",
                    "Value": user,
                },
            ],
        }],
        # DryRun=False
    )
    print(request)


def terminate_instance(instance_id: str):
    client = boto3.client('ec2',  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.REGION_NAME)
    client.terminate_instances(
        InstanceIds=[instance_id]
    )


def cancel_spot_instance(spot_request_id: str):
    client = boto3.client('ec2',  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.REGION_NAME)
    client.cancel_spot_instance_requests(
        SpotInstanceRequestIds=[spot_request_id]
    )
