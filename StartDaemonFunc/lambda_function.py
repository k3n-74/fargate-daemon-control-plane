import json
import boto3
import time
from aws_xray_sdk.core import patch_all
from botocore.client import ClientError, Config
import traceback

patch_all()

run_task_res = None

def lambda_handler(event, context):
    
    print(json.dumps(event))
    
    try:
        
        daemon_id = str(time.time())
        ecs = boto3.client('ecs')
        cluster = 'daemon-daemon-DaemonEcsCluster-OBWV6JAR18NG'
        task_definition = event.get('taskDefinition')
        
        run_daemon_res = run_daemon(ecs, daemon_id, cluster, task_definition)
        
        return {
            'daemon_id' : daemon_id,
            'taskArn' : run_daemon_res.get('taskArn')
        }

    except ClientError as e:
        traceback.print_exc()
        raise e
    
    except Exception as e:
        traceback.print_exc()
        raise e
    

def run_daemon(ecs, daemon_id, cluster, task_definition):
    launch_type='FARGATE'
    network_configuration={
        'awsvpcConfiguration' : {
            'subnets' : ['subnet-03ea9b862022ca374','subnet-03ebf3acc84659532'],
            # 'securityGroups' : [ '' ],
            'assignPublicIp' : 'ENABLED'
        },
    }
    
    container_overrides = create_container_overrides( ecs, task_definition, daemon_id )
    overrides = {
        'containerOverrides' : container_overrides
    }

    run_task_res = ecs.run_task(
            cluster=cluster,
            taskDefinition=task_definition,
            launchType=launch_type,
            networkConfiguration=network_configuration,
            overrides=overrides,
            tags=[ { 'key' : 'DCP_DAEMON_ID' , 'value' : daemon_id } ]
        )
    
    print(run_task_res)
    
    return {
        'taskArn' : run_task_res.get('tasks')[0].get('taskArn'),
        'daemon_id' : daemon_id
    }


def create_container_overrides( ecs, task_definition, daemon_id ):
    
    res = ecs.describe_task_definition( taskDefinition=task_definition )
    
    container_definitions = res.get('taskDefinition').get('containerDefinitions')
    
    container_overrides = []
    
    for container_definition in container_definitions:
        name = container_definition.get('name')
        environment = container_definition.get('environment')
        environment.append({
            'name': 'DCP_DAEMON_ID',
            'value': daemon_id
        })
        
        container_overrides.append({
            'name': name,
            'environment': environment
        })

    return container_overrides
    
    