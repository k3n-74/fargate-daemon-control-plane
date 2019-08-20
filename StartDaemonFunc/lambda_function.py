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
    
    cluster = 'daemon-daemon-DaemonEcsCluster-OBWV6JAR18NG'
    taskDefinition = event.get('taskDefinition')
    launchType='FARGATE'
    networkConfiguration={
        'awsvpcConfiguration' : {
            'subnets' : ['subnet-03ea9b862022ca374','subnet-03ebf3acc84659532'],
            # 'securityGroups' : [ '' ],
            'assignPublicIp' : 'ENABLED'
        },
    }
    
    daemon_id = str(time.time())
    
    try:
        ecs = boto3.client('ecs')
        run_task_res = ecs.run_task(
                cluster=cluster,
                taskDefinition=taskDefinition,
                launchType=launchType,
                networkConfiguration=networkConfiguration,
                tags=[ { 'key' : 'DCP_DAEMON_ID' , 'value' : daemon_id } ]
            )
        
        
    except ClientError as e:
        traceback.print_exc()
        raise e
    
    except Exception as e:
        traceback.print_exc()
        raise e
    
    print(run_task_res)
    
    ret = {
        'taskArn' : run_task_res.get('tasks')[0].get('taskArn'),
        'daemon_id' : daemon_id
    }
    
    return ret
