import boto3
import json

cluster_name = 'ecsTestCluster'
ecsclient = boto3.client('ecs')
ec2client = boto3.client('ec2')
services = ecsclient.list_services(
    cluster=cluster_name,
    launchType='FARGATE'
)

for service in services['serviceArns']:
    servicedetails=ecsclient.describe_services(
        cluster='ecsTestCluster',
        services= [service]
        )
    task_list = ecsclient.list_tasks(
    cluster =cluster_name,
    serviceName = service
        )
    print(task_list)
    task=task_list['taskArns'][0]
    task_details = ecsclient.describe_tasks(
        cluster = cluster_name,
        tasks = [
            task
        ]
    )
    eniId = task_details['tasks'][0]['attachments'][0]['details'][1]['value']
    print(eniId)
    eni_ip = ec2client.describe_network_interfaces(
            Filters=[
                {
                    'Name': 'network-interface-id',
                    'Values': [
                        eniId,
                    ]
                },
            ]
        )
    print(eni_ip['NetworkInterfaces'][0]['Association']['PublicIp'])

